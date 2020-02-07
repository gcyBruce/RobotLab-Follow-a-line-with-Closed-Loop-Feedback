# RobotLab-Follow-a-line-with-Closed-Loop-Feedback-and-Reach-the-cylinder-number-4

Task 1:
Within a work space and starting at a marked location (a red perpendicular line), the Turtlebot is required to navigate an arcdoor path and stop on the ending point that is marked.
Your robot must announce the start of its journey by beeping three times.
When your robot completes this task, and stops at the finish line, it must play the song three blind mice” to declare its ”mission completed”.
There will be a tape on the floor to guide the robot. Your robot must use its onboard Kinect sensor to perform this task. No modification, no change of position of the kinect sensor is allowed. The entire task must be completed within reasonable time duration, say around 3–5 minutes.
The performance of your final DEMO will be based on quality of tracking the path as determined by the marker.
Figure 1: Path


Task 2: Reach the cylinder number 4:
In this task four cylinders are arranged to surround the turtlebot, as is shown in Figure 2 map, the position of each cylinder is aleatory. To do this task a cylinder detector package is provided to you which has been explained in the Tutorial 3 (https://github.com/crodriguezo/cylinderDetector).
You have to program the robot to autonomously turn towards the cylinder number 4 as soon it is detected and get closer to it (do not hit the cylinder). After the robot is facing the cylinder it has to call the number/label of the cylinder and the distance to it.
Note: Because the closest distance that the Kinect sensor/camera can de- tect/see is 0.6 metres, there is a 0.6 metres or so ”blind zone” in front of the Turtlebot. Within this about 0.6m, your turtlebot may not be able see anything.
