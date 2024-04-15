import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math
import time
from std_srvs.srv import Empty

if __name__ == '__main__':
    try:
        print ('start reset: ')
        rospy.wait_for_service('reset')
        reset_turtle = rospy.ServiceProxy('reset', Empty)
        reset_turtle()
        print ('end reset: ')
        # rospy.spin()
    except rospy.ROSInterruptException:
        rospy.loginfo("node terminated.")