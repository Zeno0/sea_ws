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
# turtle1_pose.x=0
# turtle1_pose.y=0
# turtle1_pose.theta=0
turtle2_pose = Pose()
# turtle2_pose.x=0
# turtle2_pose.y=0
# turtle2_pose.theta=0
turtle3_pose = Pose()
# turtle3_pose.x=0
# turtle3_pose.y=0
# turtle3_pose.theta=0

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

def kill_turtle(name):
    killed = rospy.ServiceProxy('kill',turtlesim.srv.Kill)
    killed(name)
    # rospy.wait_for_service('/' + name + '/kill')
    # try:
    #     kill = rospy.ServiceProxy('/' + name + '/kill', Empty)
    #     kill()
    #     print("Turtle {} has been killed.".format(name))
    # except rospy.ServiceException as e:
    #     print("Service call failed:", e)

def move_turtle1(name,distance, velocity,is_forward):
    velocity_message = Twist()
    #get current location 
    global turtle1_pose
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
        distance_moved = abs(math.sqrt(((turtle1_pose.x-x0) ** 2) + ((turtle1_pose.y-y0) ** 2)))
        print  ('\t \t distance moved is ',distance_moved )   
        if  not (distance_moved<distance):
            rospy.loginfo("reached")
            break  
    velocity_message.linear.x =0
    velocity_publisher.publish(velocity_message)

def move_turtle2(name,distance, velocity,is_forward):
    velocity_message = Twist()
    #get current location 
    global turtle2_pose
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
        distance_moved = abs(math.sqrt(((turtle2_pose.x-x0) ** 2) + ((turtle2_pose.y-y0) ** 2)))
        print  ('\t \t distance moved is ',distance_moved )   
        if  not (distance_moved<distance):
            rospy.loginfo("reached")
            break 
    velocity_message.linear.x =0
    velocity_publisher.publish(velocity_message)     
      
def move_turtle3(name,distance, velocity,is_forward):
    velocity_message = Twist()
    #get current location 
    global turtle3_pose
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
        distance_moved = abs(math.sqrt(((turtle3_pose.x-x0) ** 2) + ((turtle3_pose.y-y0) ** 2)))
        print  ('\t distance moved is ',distance_moved )   
        if  not (distance_moved<distance):
            rospy.loginfo("reached")
            break 
    velocity_message.linear.x =0
    velocity_publisher.publish(velocity_message)

def move_turtles(distance, speed1, speed2, speed3):
    pub1 = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    pub2 = rospy.Publisher('/turtle2/cmd_vel', Twist, queue_size=10)
    pub3 = rospy.Publisher('/turtle3/cmd_vel', Twist, queue_size=10)
    rate = rospy.Rate(10)  # 10Hz
    global turtle1_pose
    global turtle2_pose
    global turtle3_pose
    x1=turtle1_pose.x 
    x2=turtle2_pose.x 
    x3=turtle3_pose.x 
    y1=turtle1_pose.y
    y2=turtle2_pose.y 
    y3=turtle3_pose.y 
    while not rospy.is_shutdown():
        # Calculate distance traveled by each turtle
        distance_traveled1 = abs(math.sqrt((x1- turtle1_pose.x)**2 + (y1 - turtle1_pose.y)**2))
        distance_traveled2 = abs(math.sqrt((x2- turtle2_pose.x)**2 + (y2 - turtle2_pose.y)**2))
        distance_traveled3 = abs(math.sqrt((x3- turtle3_pose.x)**2 + (y3- turtle3_pose.y)**2))
        
        # Stop each turtle when it has traveled the desired distance
        if distance_traveled1 < distance:
            vel_msg1 = Twist()
            vel_msg1.linear.x = speed1
            pub1.publish(vel_msg1)
        else:
            vel_msg1 = Twist()
            pub1.publish(vel_msg1)
        
        if distance_traveled2 < distance:
            vel_msg2 = Twist()
            vel_msg2.linear.x = speed2
            pub2.publish(vel_msg2)
        else:
            vel_msg2 = Twist()
            pub2.publish(vel_msg2)
        
        if distance_traveled3 < distance:
            vel_msg3 = Twist()
            vel_msg3.linear.x = speed3
            pub3.publish(vel_msg3)
        else:
            vel_msg3 = Twist()
            pub3.publish(vel_msg3)
            
        if not ((distance_traveled1 < distance) and (distance_traveled1 < distance)  and (distance_traveled1 < distance)):
            break

        rate.sleep()

def rotate_turtle1(angular_speed_degree, relative_angle_degree, clockwise):
    velocity_message = Twist()
    #get current location 
    theta0=turtle1_pose.theta
    angular_speed=math.radians(abs(angular_speed_degree))
    if (clockwise):
        velocity_message.angular.z =-abs(angular_speed)
    else:
        velocity_message.angular.z =abs(angular_speed) 
    # angle_moved = 0.0
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
        print('new location', turtle1_pose.theta)
        print(50*'#')
        loop_rate.sleep()
        if  (current_angle_degree>relative_angle_degree):
            rospy.loginfo("reached")
            break
    #finally, stop the robot when the distance is moved
    velocity_message.angular.z =0
    velocity_publisher.publish(velocity_message)

def rotate_turtle2(angular_speed_degree, relative_angle_degree, clockwise):
    velocity_message = Twist()
    #get current location 
    theta0=turtle2_pose.theta
    angular_speed=math.radians(abs(angular_speed_degree))
    if (clockwise):
        velocity_message.angular.z =-abs(angular_speed)
    else:
        velocity_message.angular.z =abs(angular_speed) 
    # angle_moved = 0.0
    loop_rate = rospy.Rate(10) # we publish the velocity at 10 Hz (10 times a second)    
    cmd_vel_topic='/turtle2/cmd_vel'
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
        print('new location', turtle2_pose.theta)
        print(50*'#')
        loop_rate.sleep()
        if  (current_angle_degree>relative_angle_degree):
            rospy.loginfo("reached")
            break
    #finally, stop the robot when the distance is moved
    velocity_message.angular.z =0
    velocity_publisher.publish(velocity_message)

def rotate_turtle3(angular_speed_degree, relative_angle_degree, clockwise):
    velocity_message = Twist()
    #get current location 
    theta0=turtle3_pose.theta
    angular_speed=math.radians(abs(angular_speed_degree))
    if (clockwise):
        velocity_message.angular.z =-abs(angular_speed)
    else:
        velocity_message.angular.z =abs(angular_speed) 
    # angle_moved = 0.0
    loop_rate = rospy.Rate(10) # we publish the velocity at 10 Hz (10 times a second)    
    cmd_vel_topic='/turtle3/cmd_vel'
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
        print('new location', turtle3_pose.theta)
        print(50*'#')
        loop_rate.sleep()
        if  (current_angle_degree>relative_angle_degree):
            rospy.loginfo("reached")
            break
    #finally, stop the robot when the distance is moved
    velocity_message.angular.z =0
    velocity_publisher.publish(velocity_message)

def rotate_turtles(relative_angle_degree):
    pub1 = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    pub2 = rospy.Publisher('/turtle2/cmd_vel', Twist, queue_size=10)
    pub3 = rospy.Publisher('/turtle3/cmd_vel', Twist, queue_size=10)
    rate = rospy.Rate(10)  # 10Hz
    # theta1=turtle1_pose.theta
    # theta2=turtle2_pose.theta
    # theta3=turtle3_pose.theta
    angular_speed=math.radians(abs(50))
    t10 = rospy.Time.now().to_sec()
    t20 = rospy.Time.now().to_sec()
    t30 = rospy.Time.now().to_sec()
    while not rospy.is_shutdown():
        # Calculate distance traveled by each turtle
        t11 = rospy.Time.now().to_sec()
        t21 = rospy.Time.now().to_sec()
        t31 = rospy.Time.now().to_sec()
        current_angle_degree_T1 = (t11-t10)*50
        current_angle_degree_T2 = (t21-t20)*50
        current_angle_degree_T3 = (t31-t30)*50
        # Stop each turtle when it has traveled the desired distance
        if (current_angle_degree_T1 < relative_angle_degree):
            vel_msg1 = Twist()
            vel_msg1.angular.z = abs(angular_speed)
            print(current_angle_degree_T1," covered")
            print(relative_angle_degree - current_angle_degree_T1, " remaining")
            pub1.publish(vel_msg1)
        else:
            vel_msg1 = Twist()
            pub1.publish(vel_msg1)
            # break
        
        if (current_angle_degree_T1 < relative_angle_degree):
            vel_msg2 = Twist()
            vel_msg2.angular.z = abs(angular_speed)
            print(current_angle_degree_T1," covered")
            print(relative_angle_degree - current_angle_degree_T1, " remaining")
            pub2.publish(vel_msg2)
        else:
            vel_msg2 = Twist()
            pub2.publish(vel_msg2)
            # break
        
        if (current_angle_degree_T1 < relative_angle_degree):
            vel_msg3 = Twist()
            vel_msg3.angular.z = abs(angular_speed)
            print(current_angle_degree_T1," covered")
            print(relative_angle_degree - current_angle_degree_T1, " remaining")
            pub3.publish(vel_msg3)
        else:
            vel_msg3 = Twist()
            pub3.publish(vel_msg3)
            # break
        rate.sleep()
        if not (current_angle_degree_T1 < relative_angle_degree):
            break

def main():
    rospy.init_node('multi_turtle_control', anonymous=True)
    rospy.Subscriber("/turtle1/pose", Pose, turtle1_callback) 
    rospy.Subscriber("/turtle2/pose", Pose, turtle2_callback) 
    rospy.Subscriber("/turtle3/pose", Pose, turtle3_callback) 
    time.sleep(0.5)
    # Spawn turtles at different locations
    kill_turtle("turtle1")
    spawn_turtle("turtle1", 2, 6) 
    spawn_turtle("turtle2", 2, 4)
    spawn_turtle("turtle3", 2, 2)
    time.sleep(2)
    # Move turtles along a trajectory
    # move_turtle1("turtle1",4, 1.0,True)
    # move_turtle2("turtle2",4, 1.0,True)
    # move_turtle3("turtle3",4, 1.0,True)

    move_turtles(4,1,2,3)
    time.sleep(2)
    # rotate_turtle1(50,100,True)
    # rotate_turtle2(70,140,False)
    # rotate_turtle3(100,200,True)

    # move_turtles(4)
    rotate_turtles(90)
    time.sleep(2)
    move_turtles(4,1,2,3)
    time.sleep(2)
    rotate_turtles(90)
    time.sleep(2)
    move_turtles(4,1,2,3)
    time.sleep(2)
    rotate_turtles(90)
    time.sleep(2)
    move_turtles(4,1,2,3)

if __name__ == '__main__':
    main()
