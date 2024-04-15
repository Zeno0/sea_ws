#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math
import time
from std_srvs.srv import Empty

x=0
y=0
yaw=0

def poseCallback(pose_message):
    global x
    global y
    global yaw
    x= pose_message.x
    y= pose_message.y
    yaw = pose_message.theta
    # print(25*'*')
    # print ("pose callback")
    # # print(25*'*')
    # print ('x = {}'.format(pose_message.x)) #new in python 3
    # print ('y = %f' %pose_message.y) #used in python 2
    # print ('yaw = {}'.format(pose_message.theta)) #new in python 3

def move(speed, distance, is_forward):
    velocity_message = Twist()
    #get current location 
    global x, y
    x0=x
    y0=y
    if (is_forward):
        velocity_message.linear.x =abs(speed)
    else:
        velocity_message.linear.x =-abs(speed)
    distance_moved = 0.0
    loop_rate = rospy.Rate(10) # we publish the velocity at 10 Hz (10 times a second)    
    cmd_vel_topic='/turtle1/cmd_vel'
    velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size=10)
    while True :
        print(25*'#')
        rospy.loginfo("Turtlesim moves forwards")
        velocity_publisher.publish(velocity_message)
        loop_rate.sleep()
        #rospy.Duration(1.0)
        print('initial x is', x0)
        print('updated x by callback is', x)
        distance_moved = abs(0.5 * math.sqrt(((x-x0) ** 2) + ((y-y0) ** 2)))
        print  ('\t distance moved is ',distance_moved )     
        print(25*'#')         
        if  not (distance_moved<distance):
            rospy.loginfo("reached")
            break    
    #finally, stop the robot when the distance is moved
    velocity_message.linear.x =0
    velocity_publisher.publish(velocity_message)

def rotate(angular_speed_degree, relative_angle_degree, clockwise):
    global yaw
    velocity_message = Twist()
    #get current location 
    theta0=yaw
    angular_speed=math.radians(abs(angular_speed_degree))
    if (clockwise):
        velocity_message.angular.z =-abs(angular_speed)
    else:
        velocity_message.angular.z =abs(angular_speed) 

    angle_moved = 0.0
    loop_rate = rospy.Rate(10) # we publish the velocity at 10 Hz (10 times a second)    
    cmd_vel_topic='/turtle1/cmd_vel'
    velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size=10)
    t0 = rospy.Time.now().to_sec()
    while True :
        rospy.loginfo("Turtlesim rotates")
        print(50*'#')
        print('initial location', theta0)
        velocity_publisher.publish(velocity_message)
        t1 = rospy.Time.now().to_sec()
        current_angle_degree = (t1-t0)*angular_speed_degree
        print(current_angle_degree," covered")
        print(relative_angle_degree - current_angle_degree, " remaining")
        print('new location', yaw)
        print(50*'#')
        loop_rate.sleep()
        if  (current_angle_degree>relative_angle_degree):
            rospy.loginfo("reached")
            break
    #finally, stop the robot when the distance is moved
    velocity_message.angular.z =0
    velocity_publisher.publish(velocity_message)


def go_to_goal(x_goal, y_goal):
    global x
    global y, yaw
    velocity_message = Twist()
    cmd_vel_topic='/turtle1/cmd_vel'
    velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size=10)
    while (True):
        K_linear = 1 
        distance = abs(math.sqrt(((x_goal-x) ** 2) + ((y_goal-y) ** 2)))
        linear_speed = distance * K_linear
        K_angular = 4.0
        desired_angle_goal = math.atan2(y_goal-y, x_goal-x)
        angular_speed = (desired_angle_goal-yaw)*K_angular
        velocity_message.linear.x = linear_speed
        velocity_message.angular.z = angular_speed
        velocity_publisher.publish(velocity_message)
        print(50*'#')
        print ('vlinear_msg',velocity_message.linear.x)
        print ('vangular_msg',velocity_message.angular.z)
        print ('x=', x, 'y=',y)
        print(50*'#')
        if (distance <0.01):
            break

if __name__ == '__main__':
    try:
        rospy.init_node('turtlesim_motion_pose', anonymous=True)
        # cmd_vel_topic='/turtle1/cmd_vel'
        # velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size=10)
        position_topic = "/turtle1/pose"
        pose_subscriber = rospy.Subscriber(position_topic, Pose, poseCallback) 
        time.sleep(2)
        move (0.3, 0.5 , False)
        time.sleep(1.0)
        rotate (90, 90 , True)
        time.sleep(1.0)
        go_to_goal(1.0, 1.0)
    except rospy.ROSInterruptException:
        rospy.loginfo("node terminated.")