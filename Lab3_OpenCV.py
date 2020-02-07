#!/usr/bin/python2
import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from scipy import ndimage
from std_msgs.msg import Float64
import os
import numpy as np
import time


class image_converter:
#/Users/pft/Downloads/opencv_ros.py
  def __init__(self):
    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("/camera/rgb/image_raw",Image,self.callback)

  def callback(self,data):
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
      print(e)
# crop the image and then change it to binary inverted image
    crop_img = cv_image[430:469, 0:640] ##450:469
#    gray_image = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)    
#    ret,th1 = cv2.threshold(gray_image,50,160,cv2.THRESH_BINARY_INV)  
## reverse 1 and 0
#    th1[th1==1]=2
#    th1[th1==0]=1
#    th1[th1==2]=0

# Transform the image from RGB to HSV
    HSV = cv2.cvtColor(crop_img, cv2.COLOR_BGR2HSV)
    H, S, V = cv2.split(HSV)

# set the mask to extract blue object
    LowerBlue = np.array([60, 36, 39])
    UpperBlue = np.array([140, 255, 255])
    mask = cv2.inRange(HSV, LowerBlue, UpperBlue)
# extract blue object
    th1 = cv2.bitwise_and(crop_img, crop_img, mask = mask)
# convert to binary
    ground,th1=cv2.threshold(th1,100,255,cv2.THRESH_BINARY)
# opening and closing to remove noise and conpensate waned blue path
    kernel=np.ones((5,5),np.uint8)
    kernel2=np.ones((2,2),np.uint8)
    th1=cv2.morphologyEx(th1,cv2.MORPH_CLOSE, kernel)
    th1=cv2.morphologyEx(th1,cv2.MORPH_OPEN, kernel2)
    #th1=cv2.dilate(th1,kernel,iterations=2)


# convert from BGR to HSV    
#    HSV = cv2.cvtColor(crop_img, cv2.COLOR_BGR2HSV)
#    H, S, V = cv2.split(HSV)

# set the mask to extract red object
    #LowerRed = np.array([0, 60, 60])
    #UpperRed = np.array([10, 255, 255])
    LowerRed = np.array([20, 155, 0])
    UpperRed = np.array([40, 255, 255])
    mask_red = cv2.inRange(HSV, LowerRed, UpperRed)
# extract red object
    RedThings = cv2.bitwise_and(crop_img, crop_img, mask = mask_red)
##convert to binary
    ret,RedThings=cv2.threshold(RedThings,100,255,cv2.THRESH_BINARY)
    print "y,x,the number of channels", RedThings.shape
  
    
    #cv2.imshow("cropped window", gray_image)
    cv2.imshow("cropped window", th1)
    cv2.imshow("red",RedThings)

    cv2.waitKey(3)

# calculate the middle of the matrix and the difference   
    midd = ndimage.measurements.center_of_mass(th1)
    diff = (320 - midd[1])  #midd[1] means the center of x cordinate #250 for offset test
    if -10 < diff < 10:
        diff = diff
    else:
        diff = diff -70
    print (midd)
    print (diff)
    
# calculate the sum of the red object matrix
    redd = np.sum(RedThings[:,:,1]) #[y, x, Saturation]
    print "the area of yellow",(redd)

# define the type of signal    
    signal = Float64()
    signal = diff   
    signalred = redd
    
# publish signal
    #time.sleep(0.01)
    pub.publish(signal)
    pub1.publish(signalred)   


if __name__ == '__main__':
    ic = image_converter()
    rospy.init_node('image_converter', anonymous=True)
# publish signal to two different topic
    pub = rospy.Publisher('zero_signal', Float64, queue_size=5)
    pub1 = rospy.Publisher('red_signal', Float64, queue_size=5)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
    cv2.destroyAllWindows()
