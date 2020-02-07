#!/usr/bin/env python

import rospy, time
from geometry_msgs.msg import Twist
from create_node.msg import TurtlebotSensorState
from cylinder.msg import cylDataArray
from sensor_msgs.msg import Image
import cv2
import sys, select, termios, tty
import os
from std_msgs.msg import Float64
import math


def getKey():
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key


# the feedback control, use the difference signal to calculate the angular velocity    
def signal_callback(msg):
    global adturn
    #const = 0.009
    const=0.005
    diff = msg.data
    adturn = diff * const

    
    
# red object detect function, if the sum is greater than 10000, then a red object is detected    
def red_callback(msg):
    global redtape
    red = msg.data
    if red > 100000:
    	redtape = 1 + redtape

# get the signals from the cylinder detection package
# =============================================================================
def callback(msg):
 	global label, Zrobot, Xrobot
 	if (len(msg.cylinders)>0):
 		Zrobot = msg.cylinders[0].Zrobot
 		Xrobot = msg.cylinders[0].Xrobot
 		label = msg.cylinders[0].label
 		print Zrobot, Xrobot, label
 	else:
 		print 'no cylinder'
 
# =============================================================================
def vels(speed, turn):
    return "currently:\tspeed %s\tturn %s " % (speed, turn)


speed = 0.2
turn = 1

if __name__ == "__main__":
    settings = termios.tcgetattr(sys.stdin)
    rospy.init_node('cyl')
    rospy.Subscriber("/cylinderTopic", cylDataArray, callback)
    rospy.Subscriber("/zero_signal", Float64, signal_callback)
    rospy.Subscriber("/red_signal", Float64, red_callback)
    pub = rospy.Publisher('/cmd_vel_mux/input/teleop', Twist, queue_size=5)


    x = 0
    th = 0
    control_speed = 0
    control_turn = 0
# durT, realT and startT for control before red tape    
    durT = 0
    realT = 0
    startT = 0
    adturn = 0
    redtape = 0
    switch = 0
    sound = 0
    label = 0
    Xrobot = 0
    Zrobot = 0
    turn_list=[]
    
    try:
        
        while (1):
            key = getKey()
            realT = time.time()
            print 'red',redtape
            print 'switch',switch
# start task 1            
            if key == 'k':
                switch = 1
                sound = 1

# start task 2                
            if key == 'j':
            	 switch = 4

# stop the turtlebot                
            if key == ' ':
                switch =0
                sound = 0
                redtape = 0
                durT = 0
                
            if (key =='\x03'):
                break

# play sound before start running
            if sound == 1:
            	os.system("aplay /home/turtlebot/catkin_ws/src/group6/src/beep.wav")
            	sound = 0
            
            
# use close loop control to follow the black tape, if red tape is detected, then use the open loop control
###remind to turn para back!!!!!            		
            if switch == 1:
                x = 0.4
                th = adturn*0.8
                #turn_list.append(adturn/0.005)
                #print turn_list
                #print 'th',th
                if redtape>0:
            	    switch = 2

# stop the turtlebot
            if switch == 0:
            	x = 0
            	th = 0

# when the red is detected, use open loop control to make the robot continue running for approximately 0.6 meters, and then play music           
            if switch == 2:
            	startT=time.time()
            	switch = 3
            if switch == 3:
            	durT = realT - startT
            	if 0<durT <= 3.5:
			x = 1
                	th = 0.05
                elif durT > 3:
                	switch = 0		
	            	os.system("aplay /home/turtlebot/catkin_ws/src/group6/src/beep.wav")
            
# =============================================================================
# # when task 2 start, robot starts rotation, if Xrobot is less than 20, the robot detected the cylinder 4
            if switch == 4:
 		th = 0.1
 		if label == 4:
 			if -0.05<Xrobot<0.0:
 				switch =5
                                distance=Zrobot
                                startT=time.time()
                                os.system('spd-say "label 4"')
# =============================================================================
		
# =============================================================================
# # when detected the cylinder 4, stop rotating a nd move forward the cylinder           
            if switch == 5:
               
                
                
                th = 0
                x =0.3

                dur=(distance-0.2)/0.3-0.5
                #print 'dis',distance
                #print 'dur',dur
                if (realT - startT)<dur:
                    th=0
                    x=0.3/speed
                else:
                    switch=0
                    os.system('spd-say "the distance is thirty five centimeters"')
                






#                if Zrobot<=1.00:
# 			switch = 6
# =============================================================================
#           if switch == 6:
#            	startT=time.time()
#            	switch = 7
#            if switch == 7:
#            	durT = realT - startT
#            	if 0<durT <= 6.7:
#			x = 0.5
#                	th = 0
#                elif durT > 5:
#                	switch = 0		
#	            	os.system("aplay /home/turtlebot/catkin_ws/src/group6/src/beep.wav")

            control_speed = speed * x
            control_turn = turn * th
            twist = Twist()
            twist.linear.x = control_speed;
            twist.linear.y = 0;
            twist.linear.z = 0
            twist.angular.x = 0;
            twist.angular.y = 0;
            twist.angular.z = control_turn
            pub.publish(twist)
       
     # except:
     #     print
     #     e

    finally:
        twist = Twist()
        twist.linear.x = 0;
        twist.linear.y = 0;
        twist.linear.z = 0
        twist.angular.x = 0;
        twist.angular.y = 0;
        twist.angular.z = 0
        pub.publish(twist)

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)

