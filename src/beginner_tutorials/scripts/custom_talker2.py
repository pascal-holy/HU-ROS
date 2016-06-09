#!/usr/bin/env python
import rospy
import random
from beginner_tutorials.msg import Pos

def talker():
    pub = rospy.Publisher('goal', Pos, queue_size=10)
    rospy.init_node('custom_talker', anonymous=True)
    r = rospy.Rate(1) #1hz
    msg = Pos()
    msg.id = 2
    msg.coord_x = random.uniform(0.0, 5.0)
    msg.coord_y = random.uniform(0.0, 5.0)

    while not rospy.is_shutdown():
        rospy.loginfo(msg)
        pub.publish(msg)
        r.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException: pass
