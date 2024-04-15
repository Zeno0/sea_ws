#!/usr/bin/env python

import math
import rospy
from turtlesim.srv import Spawn
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

turtle1_pose = Pose()
turtle2_pose = Pose()
turtle3_pose = Pose()

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
    turtle3_pose.x = pose_message.x
    turtle3_pose.y = pose_message.y
    turtle3_pose.theta = pose_message.theta

def spawn_turtle(name, x, y):
    rospy.wait_for_service('/spawn')
    try:
        spawn = rospy.ServiceProxy('/spawn', Spawn)
        spawn(x, y, 0, name)
    except rospy.ServiceException as e:
        print("Service call failed:", e)

def move_turtle1(name,distance, velocity,is_forward):
    velocity_message = Twist()
    #get current location 
    x0=turtle1_pose.x
    y0=turtle1_pose.y
    if (is_forward):
        velocity_message.linear.x =abs(velocity)
    else:
        velocity_message.linear.x =-abs(velocity)
    loop_rate = rospy.Rate(10) # we publish the velocity at 10 Hz (10 times a second)    
    velocity_publisher = rospy.Publisher('/%s/cmd_vel' % name, Twist, queue_size=10)
    while not rospy.is_shutdown():
        rospy.loginfo("Turtlesim moves forwards")
        velocity_publisher.publish(velocity_message)
        loop_rate.sleep()
        print(25*'-')
        print('\tx of turtle1 is ',turtle1_pose.x)
        print('\tinitial x is ',x0)
        print('\ty of turtle1 is  ',turtle1_pose.y)
        print('\tinitial y is ',y0)
        print(25*'-')
        distance_moved = abs(0.5 * math.sqrt(((turtle1_pose.x-x0) ** 2) + ((turtle1_pose.y-y0) ** 2)))
        print  ('\t \t distance moved is ',distance_moved )   
        if  not (distance_moved<distance):
            rospy.loginfo("reached")
            break  
    velocity_message.linear.x =0
    velocity_publisher.publish(velocity_message)

def move_turtle2(name,distance, velocity,is_forward):
    velocity_message = Twist()
    #get current location 
    x0=turtle2_pose.x
    y0=turtle2_pose.y
    if (is_forward):
        velocity_message.linear.x =abs(velocity)
    else:
        velocity_message.linear.x =-abs(velocity)
    loop_rate = rospy.Rate(10) # we publish the velocity at 10 Hz (10 times a second)    
    velocity_publisher = rospy.Publisher('/%s/cmd_vel' % name, Twist, queue_size=10)
    while not rospy.is_shutdown():
        rospy.loginfo("Turtlesim moves forwards")
        velocity_publisher.publish(velocity_message)
        loop_rate.sleep()
        print(25*'-')
        print('\t x of turtle1 is ',turtle2_pose.x)
        print('\t initial x is ',x0)
        print('\t y of turtle1 is  ',turtle2_pose.y)
        print('\t initial y is ',y0)
        print(25*'-')
        distance_moved = abs(0.5 * math.sqrt(((turtle2_pose.x-x0) ** 2) + ((turtle2_pose.y-y0) ** 2)))
        print  ('\t \t distance moved is ',distance_moved )   
        if  not (distance_moved<distance):
            rospy.loginfo("reached")
            break 
    velocity_message.linear.x =0
    velocity_publisher.publish(velocity_message)     
      
def move_turtle3(name,distance, velocity,is_forward):
    velocity_message = Twist()
    #get current location 
    x0=turtle3_pose.x
    y0=turtle3_pose.y
    if (is_forward):
        velocity_message.linear.x =abs(velocity)
    else:
        velocity_message.linear.x =-abs(velocity)
    loop_rate = rospy.Rate(10) # we publish the velocity at 10 Hz (10 times a second)    
    velocity_publisher = rospy.Publisher('/%s/cmd_vel' % name, Twist, queue_size=10)
    while not rospy.is_shutdown():
        rospy.loginfo("Turtlesim moves forwards")
        velocity_publisher.publish(velocity_message)
        loop_rate.sleep()
        print(25*'-')
        print('\t x of turtle1 is ',turtle3_pose.x)
        print('\t initial x is ',x0)
        print('\t y of turtle1 is  ',turtle3_pose.y)
        print('\t initial y is ',y0)
        print(25*'-')
        distance_moved = abs(0.5 * math.sqrt(((turtle3_pose.x-x0) ** 2) + ((turtle3_pose.y-y0) ** 2)))
        print  ('\t distance moved is ',distance_moved )   
        if  not (distance_moved<distance):
            rospy.loginfo("reached")
            break 
    velocity_message.linear.x =0
    velocity_publisher.publish(velocity_message)

def move_turtles(distance):
    pub1 = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    pub2 = rospy.Publisher('/turtle2/cmd_vel', Twist, queue_size=10)
    pub3 = rospy.Publisher('/turtle3/cmd_vel', Twist, queue_size=10)
    rate = rospy.Rate(10)  # 10Hz
    x1=turtle1_pose.x 
    x2=turtle2_pose.x 
    x3=turtle3_pose.x 
    y1=turtle1_pose.y
    y2=turtle2_pose.y 
    y3=turtle3_pose.y 
    while not rospy.is_shutdown():
        # Calculate distance traveled by each turtle
        distance_traveled1 = math.sqrt((x1- turtle1_pose.x)**2 + (y1 - turtle1_pose.y)**2)
        distance_traveled2 = math.sqrt((x2- turtle2_pose.x)**2 + (y2 - turtle2_pose.y)**2)
        distance_traveled3 = math.sqrt((x3- turtle3_pose.x)**2 + (y3- turtle3_pose.y)**2)
        
        # Stop each turtle when it has traveled the desired distance
        if distance_traveled1 < distance:
            vel_msg1 = Twist()
            vel_msg1.linear.x = 1.0
            pub1.publish(vel_msg1)
        else:
            vel_msg1 = Twist()
            pub1.publish(vel_msg1)
        
        if distance_traveled2 < distance:
            vel_msg2 = Twist()
            vel_msg2.linear.x = 0.5
            pub2.publish(vel_msg2)
        else:
            vel_msg2 = Twist()
            pub2.publish(vel_msg2)
        
        if distance_traveled3 < distance:
            vel_msg3 = Twist()
            vel_msg3.linear.x = 0.3
            pub3.publish(vel_msg3)
        else:
            vel_msg3 = Twist()
            pub3.publish(vel_msg3)
        
        rate.sleep()
def main():
    rospy.init_node('multi_turtle_control', anonymous=True)
    rospy.Subscriber("/turtle1/pose", Pose, turtle1_callback) 
    rospy.Subscriber("/turtle2/pose", Pose, turtle2_callback) 
    rospy.Subscriber("/turtle3/pose", Pose, turtle3_callback) 
    # Spawn turtles at different locations
    # spawn_turtle("turtle1", 1, 1) no need for this
    spawn_turtle("turtle2", 5, 5)
    spawn_turtle("turtle3", 2, 2)

    # Move turtles along a trajectory
    # move_turtle1("turtle1",1, 1.0,True)
    # move_turtle2("turtle2",1, 1.0,True)
    # move_turtle3("turtle3",1, 1.0,True)

    move_turtles(2)

if __name__ == '__main__':
    main()
