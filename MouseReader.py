from inputs import devices
from threading import Thread
from Queue import Queue, Empty
import pandas as pd

import numpy as np
import time
# Handle for getting mouse events
#mouse = devices.mice[0]
m = devices.mice[1]
m2 = devices.mice[2]

####################################
#Run the loop, monitor for movements.
#movements = []

data = np.zeros((1,8))
COS45 = np.cos(np.pi/4)
ballDiameter = 23  #mas o menos
x1 = 0
y1 = 0
y2 = 0
x2 = 0
t = 0
t2 = 0

def poll_mouse(mouse, out_queue):
    while True:
        events = m.read()
        frame = {}
        for event in events:
            # Y events and X events can happen independently
            # yet we always want to return x and y for data consistency
            # simultaneous x and y events will have the same timestamp
            # we stash the timestamp, then compare each next event to see if it matches
            # if so, we assume we got the other one and send the frame
            # if not, we assign the missing value zero and send it.
            frame['x'] = 1
            frame['y'] = 1
            out_queue.put_nowait(frame)
            frame = {}
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
##                        
                    

mice = {'mouse_0':devices.mice[1],
        'mouse_1':devices.mice[2]}
queues = []
mouse_threads = []
for m_name, mouse in mice.items():
    queues.append(Queue())
    mouse_threads.append(Thread(name=m_name, target=poll_mouse, args=(mouse, queues[-1])))

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

while True:
    A = time.time()
    dfs = []
    for queue in queues:
        events = queue_get_all(queue)
        if len(events) == 0:
            dfs.append(pd.DataFrame({'x' : [0], 'y' : [0]}))
        else:
            dfs.append(pd.DataFrame.from_records(events).sum(0))

    x1 = dfs[0].x
    x2 = dfs[1].x
    y1 = dfs[0].y
    y2 = dfs[1].y                                
    
    
    BdX = (x1+x2)/(2*COS45)
    BdY = (y1-y2)/(2*COS45)
    BdTheta = -1*(x1+x2)/(ballDiameter)
    B = time.time()
    #print BX
    print('cycle time: {}, dx: {}, dy: {}, theta: {}'.format(B-A, BdX, BdY, BdTheta))
    time.sleep(0.1)
