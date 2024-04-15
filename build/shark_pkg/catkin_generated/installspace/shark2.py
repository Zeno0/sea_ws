#!/usr/bin/env python3

import math
import rospy
from turtlesim.srv import Spawn
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

x=0
y=0
yaw=0

def poseCallback(pose_message):
    global x
    global y, yaw
    x= pose_message.x
    y= pose_message.y
    yaw = pose_message.theta

def spawn_turtle(name, x, y):
    rospy.wait_for_service('/spawn')
    try:
        spawn = rospy.ServiceProxy('/spawn', Spawn)
        spawn(x, y, 0, name)
    except rospy.ServiceException as e:
        print("Service call failed:", e)

def move_turtle(name,distance, velocity,is_forward):
    velocity_message = Twist()
     #get current location 
    global x, y
    x0=x
    y0=y
    if (is_forward):
        velocity_message.linear.x =abs(velocity)
    else:
        velocity_message.linear.x =-abs(velocity)
    loop_rate = rospy.Rate(10) # we publish the velocity at 10 Hz (10 times a second)    
    velocity_publisher = rospy.Publisher('/%s/cmd_vel' % name, Twist, queue_size=10)
    while not rospy.is_shutdown():
        vel_msg = Twist()
        vel_msg.linear.x = velocity
        rospy.loginfo("Turtlesim moves forwards")
        velocity_publisher.publish(vel_msg)
        loop_rate.sleep()
        distance_moved = abs(0.5 * math.sqrt(((x-x0) ** 2) + ((y-y0) ** 2)))
        print  ('\t distance moved is ',distance_moved )   
        if  not (distance_moved<distance):
                    rospy.loginfo("reached")
                    break  

def main():
    rospy.init_node('multi_turtle_control', anonymous=True)
    # position_topic = "/turtle1/pose"
    # pose_subscriber = rospy.Subscriber(position_topic, Pose, poseCallback) 
    # Spawn turtles at different locations
    spawn_turtle("turtle1", 1, 1)
    spawn_turtle("turtle2", 5, 5)
    spawn_turtle("turtle3", 2, 2)

    # Move turtles along a trajectory
    move_turtle("turtle1",1, 1.0,True)
    move_turtle("turtle2",2, 0.3,True)
    move_turtle("turtle3",2, 0.3,True)

if __name__ == '__main__':
    main()