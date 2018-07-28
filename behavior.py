from motors import Stepper

from inputs import devices
from threading import Thread, Event
from Queue import Queue, Empty
import pandas as pd
import signal
import sys

import numpy as np
import time


def poll_mouse(mouse, out_queue, stop_sig):
    while True:
        events = mouse.read()
        frame = {}
        for event in events:
            if event.code == "REL_X":
                out_queue.put_nowait([event.state, 0])
            elif event.code == "REL_Y":
                out_queue.put_nowait([0, event.state])

        if stop_sig.is_set():
            break

def queue_get_all(q):
    items = []
    while 1:
        try:
            items.append(q.get_nowait())
        except Empty, e:
            break
    return items

def get_movements(queues):
    dfs = []
    for queue in queues:
        events = queue_get_all(queue)
        if len(events) == 0:
            xy = np.array([0,0], dtype=np.float)
            dfs.append(xy)
        else:
            xy = np.sum(np.array(events),0)
            dfs.append(xy)

    return dfs

def stop_run(sig, frame):
    #stop_sig.set()
    sys.exit(0)

def main():
    # register stop
    signal.signal(signal.SIGINT, stop_run)

    # setup mice
    mice = {'mouse_0': devices.mice[0],
            'mouse_1': devices.mice[1]}

    # start threads
    queues = []
    mouse_threads = []
    stop_sig = Event()
    for m_name, mouse in mice.items():
        queues.append(Queue())
        mouse_threads.append(Thread(name=m_name, target=poll_mouse, args=(mouse, queues[-1], stop_sig)))

    for thread in mouse_threads:
        thread.start()

    # start motors
    middle = Stepper(direction_pin=13, step_pin=19, limits=[0, 100000])
    top = Stepper(direction_pin=20, step_pin=21)

    # start loop
    while True:
        moves = get_movements(queues)
        middle.step(moves[0][1])



