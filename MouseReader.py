from inputs import devices
from threading import Thread, Event
from Queue import Queue, Empty
import pandas as pd
import signal

import numpy as np
import time
# Handle for getting mouse events
#mouse = devices.mice[0]

####################################
#Run the loop, monitor for movements.
#movements = []

data = np.zeros((1,8))
COS45 = np.cos(np.pi/4)
ballDiameter = 150.  #more or less
x1 = 0
y1 = 0
y2 = 0
x2 = 0
t = 0
t2 = 0

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

            
            # Y events and X events can happen independently
            # yet we always want to return x and y for data consistency
            # simultaneous x and y events will have the same timestamp
            # we stash the timestamp, then compare each next event to see if it matches
            # if so, we assume we got the other one and send the frame
            # if not, we assign the missing value zero and send it.
            #frame['x'] = 1
            #frame['y'] = 1
            #out_queue.put_nowait(frame)
##            frame = {}
##            if len(frame) == 0:
##                if event.code == 'REL_X':
##                    frame['ts'] = event.timestamp
##                    frame['x'] = event.state
##                elif event.code == 'REL_Y':
##                    frame['ts'] = event.timestamp
##                    frame['y'] = event.state
##            else:
##                if event.timestamp == frame['ts']:
##                    if event.code == 'REL_X':
##                        frame['ts'] = event.timestamp
##                        frame['x'] = event.state
##                        out_queue.put_nowait(frame)
##                        frame = {}
##                    elif event.code == 'REL_Y':
##                        frame['ts'] = event.timestamp
##                        frame['y'] = event.state
##                        out_queue.put_nowait(frame)
##                        frame = {}
##                else:
##                    if 'x' in frame.keys():
##                        frame['y'] = 0.
##                        out_queue.put_nowait(frame)
##                        frame = {}
##                    else:
##                        frame['x'] = 0.
##                        out.queue.put_nowait(frame)
##                        frame = {}
                        
                    

mice = {'mouse_0':devices.mice[0],
        'mouse_1':devices.mice[1]}
queues = []
mouse_threads = []
stop_sig = Event()
for m_name, mouse in mice.items():
    queues.append(Queue())
    mouse_threads.append(Thread(name=m_name, target=poll_mouse, args=(mouse, queues[-1], stop_sig)))

for thread in mouse_threads:
    thread.start()

def queue_get_all(q):
    items = []
    while 1:
        try:
            items.append(q.get_nowait())
        except Empty, e:
            break
    return items

# register stop
def stop_run(sig, frame):
    stop_sig.set()
signal.signal(signal.SIGINT, stop_run)

while True:
    A = time.time()
    dfs = []
    for queue in queues:
        events = queue_get_all(queue)
        if len(events) == 0:
            xy = np.array([0,0], dtype=np.float)
            dfs.append(xy)
        else:
            xy = np.sum(np.array(events),0)
            dfs.append(xy)
        
        
##        if len(events) == 0:
##            dfs.append(pd.DataFrame({'x' : [0], 'y' : [0]}).sum(0))
##        else:
##            dfs.append(pd.DataFrame.from_records(events).sum(0))
##
##    x1 = dfs[0].x
##    x2 = dfs[1].x
##    y1 = dfs[0].y
##    y2 = dfs[1].y

    x1 = dfs[0][0]
    x2 = dfs[1][0]
    y1 = dfs[0][1]
    y2 = dfs[1][1]
    
    
    BdX = (x1+x2)/(2*COS45)
    BdY = (y1-y2)/(2*COS45)
    BdTheta = -1.*(x1+x2)/(ballDiameter)
    
    B = time.time()
    #print BX
    #print('cycle time: {}, dx: {}, dy: {}, theta: {}'.format(B-A, BdX, BdY, BdTheta))
    print('cycle time: {}, x1: {}, y1: {}, x2 : {}, y2 : {}'.format(B-A, x1, y1, x2, y2))
    time.sleep(0.1)
