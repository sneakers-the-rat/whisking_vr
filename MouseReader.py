from inputs import devices
#from threading import Timer
#import numpy as np


# Handle for getting mouse events
#mouse = devices.mice[0]
m = devices.mice[0]
m2 = devices.mice[1]
#mouse2 = devices.mice[1]
#mice = {'mouse_1':mouse}
#        'mouse_2':mouse2}

####################################
# Run the loop, monitor for movements.
movements = []
while 1:
    #for name, m in mice.items():
    events = m.read()
    for event in events:
        #if event.code == 'REL_X':
        print('{} - moved {} X: {}'.format(event.timestamp, event.code, event.state))
        #elif event.code == 'REL_Y':
        #    print('{} - moved {} Y: {}'.format(event.timestamp, name, event.state))


    #movements.extend([event.state for event in events if event.code == "REL_Y"])

while 1:
    events_mouse = m2.read()
    for event2 in events_mouse
        print('{} - moved {} X: {}'.format(event2.timestamp, event2.code, event2.state))


