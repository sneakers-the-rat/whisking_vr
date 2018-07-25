from inputs import devices
#from threading import Timer
#import numpy as np


# Handle for getting mouse events
#mouse = devices.mice[0]
#m = devices.mice[0]
#m2 = devices.mice[1]
#mouse2 = devices.mice[1]
#mice = {'mouse_1':m}
 #       'mouse_2':m2}

####################################
# Run the loop, monitor for movements.
#movements = []
#while 1:
 #   for name, m in mice.items():
  #  events = m.read()
   # for event in events:
        #if event.code == 'REL_X':
        #print('{} - moved {} X: {}'.format(event.timestamp, event.code, event.state))
        #elif event.code == 'REL_Y':
        #    print('{} - moved {} Y: {}'.format(event.timestamp, name, event.state))
    #data_temp[0] = event.timestamp
    #data_temp[1] = (event[0].code+
    #data_temp[2] =
    #data_temp[3] =
    
###################### Let's try with thread ###########
import threading
from inputs import devices
m = devices.mice[0]
m2 = devices.mice[1]


def mouse1():
    event = m.read()
    print('{} - moved {} X: {}'.format(event.timestamp, event.code, event.state))

def mouse2():
    event = m2.read()
    print('{} - moved {} X: {}'.format(event.timestamp, event.code, event.state))

mouse_1 = threading.Thread(name='mouse1', target=mouse1)
mouse_2 = threading.Thread(name='mouse2', target=mouse2)

mouse_1.start()
mouse_2.start()

