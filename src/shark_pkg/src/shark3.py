#!/usr/bin/env python

import math
import time
import rospy
from turtlesim.srv import Spawn
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from std_srvs.srv import Empty
import turtlesim.srv

turtle1_pose = Pose()
turtle2_pose = Pose()
turtle3_pose = Pose()

def spawn_turtle(name, x, y):
    rospy.wait_for_service('/spawn')
    try:
        spawn = rospy.ServiceProxy('/spawn', Spawn)
        spawn(x, y, 0, name)
    except rospy.ServiceException as e:
        print("Service call failed:", e)

def kill_turtle(name):
    killed = rospy.ServiceProxy('kill',turtlesim.srv.Kill)
    killed(name)

def turtle1_callback(pose_message):
    global turtle1_pose
    turtle1_pose.x = pose_message.x
    turtle1_pose.y = pose_message.y
    turtle1_pose.theta = pose_message.theta

def turtle2_callback(pose_message):
    global turtle2_pose
    turtle2_pose.x = pose_message.x
    turtle2_pose.y = pose_message.y
    turtle2_pose.theta = pose_message.theta

def turtle3_callback(pose_message):
    global turtle3_pose
    turtle3_pose.x = pose_message.x
    turtle3_pose.y = pose_message.y
    turtle3_pose.theta = pose_message.theta

def move_spiral(name):
    loop_rate = rospy.Rate(1)
    pub = rospy.Publisher('/%s/cmd_vel' % name, Twist, queue_size=10)
    wk = 4
    rk = 0
    # print('current x is ', turtle2_pose.x )
    # print('current y is ', turtle2_pose.y)
    while(( turtle2_pose.x<9.5) and (turtle2_pose.y<9.5)):
        vel_msg = Twist()
        rk=rk+0.7
        vel_msg.linear.x =rk
        vel_msg.angular.z =wk
        pub.publish(vel_msg)
        print('updated x is ', turtle2_pose.x)
        print('updated y is ', turtle2_pose.y)
        loop_rate.sleep()
    vel_msg.linear.x = 0
    vel_msg.angular.z = 0
    pub.publish(vel_msg)

def rec_square1(pub):
    for _ in range(5):
        # Move forward
        vel_msg = Twist()
        vel_msg.linear.x = 1
        pub.publish(vel_msg)
        rospy.sleep(1)

        # Stop
        vel_msg.linear.x = 0
        pub.publish(vel_msg)

        # Turn
        vel_msg.angular.z = -(math.pi / 2 ) # 90 degrees
        pub.publish(vel_msg)
        rospy.sleep(2)

def rec_square2(pub):
    for _ in range(5):
        # Move forward
        vel_msg = Twist()
        vel_msg.linear.x = 1
        pub.publish(vel_msg)
        rospy.sleep(1)

        # Stop
        vel_msg.linear.x = 0
        pub.publish(vel_msg)

        # Turn
        vel_msg.angular.z = (math.pi / 2 ) # 90 degrees
        pub.publish(vel_msg)
        rospy.sleep(2)

def move_square(name):
    pub = rospy.Publisher('/%s/cmd_vel' % name, Twist, queue_size=10)
    rospy.Rate(1)  # 0.5Hz
    rec_square1(pub)
    rec_square2(pub)
    rec_square1(pub)
    rec_square2(pub)

# Function to make a turtle follow a oval-like trajectory
def move_ovals(name):
    # Create a publisher to send velocity commands to the turtle
    pub = rospy.Publisher('/%s/cmd_vel' % name, Twist, queue_size=10)
    rate = rospy.Rate(10)  # Set the publishing rate to 10 Hz
    t = 0  # Initialize the time parameter
    while not rospy.is_shutdown():  # Continue until ROS is shutdown
        # Calculate the velocity components for the flower-like trajectory
        vel_msg = Twist()
        vel_msg.linear.x = (2 * math.cos(t) * (math.cos(t) ** 2))*2
        vel_msg.linear.y = (2 * math.sin(t) * (math.cos(t) ** 2))*2
        # Publish the velocity command
        pub.publish(vel_msg)
        t += 0.2  # Increment the time parameter
        rate.sleep()  # Wait for the specified rate
        print(t)
        if (t >80):
            break

# Function to make a turtle follow a figure-eight trajectory
def move_figure_eight(name):
    # Create a publisher to send velocity commands to the turtle
    pub = rospy.Publisher('/%s/cmd_vel' % name, Twist, queue_size=10)
    rate = rospy.Rate(10)  # Set the publishing rate to 10 Hz
    t = 0  # Initialize the time parameter
    while not rospy.is_shutdown():  # Continue until ROS is shutdown
        # Calculate the velocity components for the figure-eight trajectory
        vel_msg = Twist()
        vel_msg.linear.x = 2 * math.sin(t)
        vel_msg.angular.z = 2 * math.sin(2 * t)
        # Publish the velocity command
        pub.publish(vel_msg)
        t += 0.1  # Increment the time parameter
        rate.sleep()  # Wait for the specified rate

def main():
    rospy.init_node('multi_turtle_control', anonymous=True)
    rospy.Subscriber("/turtle1/pose", Pose, turtle1_callback) 
    rospy.Subscriber("/turtle2/pose", Pose, turtle2_callback) 
    rospy.Subscriber("/turtle3/pose", Pose, turtle3_callback) 

    time.sleep(0.5)
    # Spawn turtles at different locations
    kill_turtle("turtle1")
    spawn_turtle("turtle1", 3, 3)
    spawn_turtle("turtle2", 7.5, 5.5)
    spawn_turtle("turtle3", 4, 8)

    time.sleep(1)
    # Move turtles along a spiral trajectory
    move_spiral("turtle2")
    time.sleep(1)
    # Move turtles along a square trajectory
    move_square("turtle1")
    time.sleep(1)
    # Move turtle3 along a square trajectory
    move_ovals("turtle3")

if __name__ == '__main__':
    main()