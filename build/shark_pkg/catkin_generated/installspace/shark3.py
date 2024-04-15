#!/usr/bin/env python3

import rospy
from turtlesim.srv import Spawn
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math

# Global variables to store the current pose of each turtle
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

def turtle1_callback(msg):
    global turtle1_pose
    turtle1_pose = msg

def turtle2_callback(msg):
    global turtle2_pose
    turtle2_pose = msg

def turtle3_callback(msg):
    global turtle3_pose
    turtle3_pose = msg

def move_turtle(name, velocity, goal_x, goal_y):
    pub = rospy.Publisher('/%s/cmd_vel' % name, Twist, queue_size=10)
    rate = rospy.Rate(10)  # 10Hz
    while not rospy.is_shutdown():
        vel_msg = Twist()
        vel_msg.linear.x = velocity
        
        # Calculate distance to goal
        distance = math.sqrt((goal_x - globals()[name + "_pose"].x)**2 + (goal_y - globals()[name + "_pose"].y)**2)
        
        # If turtle is close to the goal, stop moving
        if distance < 0.1:
            vel_msg.linear.x = 0
        pub.publish(vel_msg)
        rate.sleep()

def main():
    rospy.init_node('multi_turtle_control', anonymous=True)

    # Spawn turtles at different locations
    spawn_turtle("turtle1", 1, 1)
    spawn_turtle("turtle2", 2, 2)
    spawn_turtle("turtle3", 5, 5)

    # Subscribe to the pose topics of each turtle
    rospy.Subscriber('/turtle1/pose', Pose, turtle1_callback)
    rospy.Subscriber('/turtle2/pose', Pose, turtle2_callback)
    rospy.Subscriber('/turtle3/pose', Pose, turtle3_callback)

    # Move turtles along a straight line
    move_turtle("turtle1", 1.0, 10, 1)
    move_turtle("turtle2", 0.5, 10, 5)
    move_turtle("turtle3", 0.3, 10, 9)

if __name__ == '__main__':
    main()
