import RPi.GPIO as GPIO
from time import sleep
from datetime import datetime
from Queue import Queue
from Threading import Thread
import signal
import sys

class Stepper(object):
    def __init__(self, step_pin, direction_pin, multiplier=1, delay=0.000001, limits=None):
        GPIO.cleanup()
        GPIO.setmode(GPIO.BOARD)

        # multiplier that converts mouse movements to steps
        self.mult = multiplier
        # delay between pulses
        self.delay = delay

        # register cleanup function
        # close writer if ctrl+c

        signal.signal(signal.SIGINT, self._end)

        # setup pins
        self.p_step = step_pin
        self.p_dir  = direction_pin
        GPIO.setup(self.p_step, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.p_dir,  GPIO.OUT, initial=GPIO.LOW)



        if limits is not None:
            self.limits = limits
            self.pos = 0
        else:
            self.limits = None
            self.pos = None

        # start thread to run steps
        self.queue = Queue()
        self.pin_thread = Thread(target=self.run_pins, args=(self.queue,))
        self.pin_thread.start()

    def _end(self):
        # close writer if ctrl+c
        def close_writer(signum, frame):
            print('\nctrl+c pressed, closing pin controller')
            GPIO.cleanup()
            sys.exit(0)


    def run_pins(self, queue):
        # keep grabbing steps until we get some END signal
        for steps in iter(queue.get, 'END'):
            if self.limits is not None:
                # if we are limited, make sure we don't go over them
                if self.pos+steps > self.limits[1]:
                    # if steps would take us over the max, reduce
                    # if we're already at the max and is positive, will be zero
                    steps = self.limits[1]-self.pos
                elif self.pos+steps < self.limits[0]:
                    # vice versa for min
                    steps = self.limits[0]-self.pos

                # update position
                self.pos += steps

            # set step direction
            if steps<0:
                GPIO.output(self.p_dir, 1)
            else:
                GPIO.output(self.p_dir, 0)

            # do em
            for step in xrange(abs(steps)):
                GPIO.output(self.p_step, 1)
                GPIO.output(self.p_step, 0)
                sleep(self.delay)

    def step(self, steps):
        try:
            self.queue.put_nowait(int(steps))
            print('{}: stepping {}'.format(self.timestamp(), steps))
        except TypeError:
            print('type error, was steps an int?')



    def timestamp(self):
        return datetime.now().strftime("%m-%d-%H:%M:%S.%f")[:-3]





