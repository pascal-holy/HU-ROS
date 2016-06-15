#!/usr/bin/env python
import rospy
import random
from pro_ant.msg import JobOffer


def createMessage(new_id):
    msg = JobOffer()
    msg.id = new_id
    msg.source_x = random.uniform(0.0, 50.0)
    msg.source_y = random.uniform(0.0, 50.0)
    msg.dest_x = random.uniform(0.0, 50.0)
    msg.dest_y = random.uniform(0.0, 50.0)
    return msg


def start_auction():
    msg_count = 0
    wait_count = 0
    rospy.init_node("auctioneer", anonymous=True)
    pub = rospy.Publisher('job_offer', JobOffer, queue_size=10)
    r = rospy.Rate(0.5)  # 1hz
    msg = createMessage(1)
    msg2 = createMessage(2)

    while not rospy.is_shutdown():
        pub.publish(msg)
        rospy.loginfo(msg)
        r.sleep()
        # pub.publish(msg2)
        # r.sleep()


if __name__ == '__main__':
    start_auction()
