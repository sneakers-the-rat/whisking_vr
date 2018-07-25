from inputs import devices
#from threading import Timer
import numpy as np


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
#import threading
#from inputs import devices
#M1 = devices.mice[0]
#M2 = devices.mice[1]

#class Ball():
 #   def mouse(m):
  #      while True:
   #         print 'I read this line at least'
    #        event = m.read()
     #       print('{} - moved {} X: {}'.format(event.timestamp, event.code, event.state))

#def mouse2():
 #   while True:
  #      print 'I read this line at least'
   #     event2 = m2.read()
    #    print('{} - moved {} X: {}'.format(event2.timestamp, event2.code, event2.state))

#mouse_1 = threading.Thread(name='mouse1', target=mouse, args = (M1,))
#mouse_2 = threading.Thread(name='mouse2', target=mouse, args = (M2,))

#mouse_1.start()
#mouse_2.start()




##### Let's have fun!!
# Handle for getting mouse events
#mouse = devices.mice[0]
m = devices.mice[0]
m2 = devices.mice[1]
#mouse2 = devices.mice[1]
#mice = {'mouse_1':m}
 #       'mouse_2':m2}

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
while 1:
    events = m.read()
    try:
        for event in events:
            if event.code == 'REL_X':
                #print('{} - moved {} X: {}'.format(event.timestamp, event.code, event.state))
                x1 = event.state
                t = event.timestamp
                #print x1
         elif event.code == 'REL_Y':
                #print('{} - moved {} Y: {}'.format(event.timestamp, name, event.state))
                y1 = event.state
                #print y1
    #events2 = m2.read()
    #for event2 in events2:
     #   if event2.code == 'REL_X':
      #      #print('{} - moved {} X: {}'.format(event.timestamp, event.code, event.state))
       #     x2 = event2.state
        #    t2 = event2.timestamp
        #elif event.code == 'REL_Y':
            #print('{} - moved {} Y: {}'.format(event.timestamp, name, event.state))
         #   y2 = event2.state
         #   t2 = event2.timestamp
         except:
             pass
        
    BdX = (x1+x2)/(2*COS45)
    BdY = (y1-y2)/(2*COS45)
    BdTheta = -1*(x1+x2)/(ballDiameter)
            # Coordinate system with +x (forward), +y (right), +theta (clockwise)
    DeltaPos = np.array([BdX, BdY, BdTheta]) 
            
    lastX = data[-1, 8]
    lastY = data[-1, 9]
    lastTheta = data[-1, 10]
            
    BX = lastX + (BdX*np.cos(lastTheta)-BdY*np.sin(lastTheta))
    BY = lastY + (BdX*np.sin(lastTheta)+BdY*np.cos(lastTheta))
    BTheta = lastTheta + BdTheta
            
    #return np.hstack((time1, time2, BdX, BdY, BdTheta, BX, BY, BTheta))
    print BX
        #plotTraj(self):
        #X = self.data[:,5]
        #Y = self.data[:,6]

        #plt.plot(X,Y)
        #plt.axis('equal')
        #plt.hold(True)
       # plt.draw()
      #  plt.show(block=False)
     #   
    #def plotHeading(self):
     #   t = self.data[:,0]
     #   Theta = self.data[:,7]

 #       plt.plot(t, Theta)
#        plt.hold(True)
   #     plt.draw()
  #      plt.show(block=False)
#
#
#
#
