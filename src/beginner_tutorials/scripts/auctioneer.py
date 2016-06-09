#!/usr/bin/env python
import rospy
import random
from beginner_tutorials.msg import Dst

class Auctioneer(object):
    def __init__(self):
        # initiliaze
        rospy.init_node("auctioneer", anonymous=True)
        self.bid = 8000.0
        self.talker()

    def talker(self):
        pub = rospy.Publisher('goal', Dst, queue_size=10)
        rospy.Subscriber("goal", Dst, self.gotDistance)
        r = rospy.Rate(1) #1hz
        msg = Dst()
        msg.msg_id = 1
        msg.goal_x = random.uniform(0.0, 5.0)
        msg.goal_y = random.uniform(0.0, 5.0)

        while not rospy.is_shutdown():
            msg.bid = self.bid
            rospy.loginfo(msg)
            pub.publish(msg)
            r.sleep()

    def gotDistance(self, data):
        if data.robot_id != 0:
            self.bid = data.bid
            


if __name__ == '__main__':
    Auctioneer()
