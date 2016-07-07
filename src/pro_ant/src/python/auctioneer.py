#!/usr/bin/env python
import rospy
import random
from pro_ant.msg import JobOffer


def create_message(new_id):
    msg = JobOffer()
    msg.id = new_id
    msg.source_id = random.randint(0, 2)
    msg.destination_id = random.randint(0, 2)
    while msg.source_id == msg.destination_id:
        msg.destination_id = random.randint(0, 2)
    return msg


def start_auction():
    msg_count = 0
    wait_count = 0
    rospy.init_node('auctioneer', anonymous=True)
    pub = rospy.Publisher('job_offer', JobOffer, queue_size=10)
    r = rospy.Rate(0.5)  # 1hz
    msg = create_message(msg_count)

    while not rospy.is_shutdown():
        if wait_count < 10:
            wait_count += 1
            pub.publish(msg)
            rospy.loginfo(msg)
            r.sleep()
        else:
            wait_count = 0
            msg_count += 1
            msg = create_message(msg_count)


if __name__ == '__main__':
    start_auction()
