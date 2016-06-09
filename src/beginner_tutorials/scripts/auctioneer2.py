#!/usr/bin/env python
import rospy
import random
from beginner_tutorials.msg import Dst

def createMessage(new_id):
    msg = Dst()
    msg.msg_id = new_id
    msg.goal_x = random.uniform(0.0, 5.0)
    msg.goal_y = random.uniform(0.0, 5.0)
    rospy.set_param('~bid', 8000.0)
    rospy.set_param('~robot_id', 0)
    return msg

def startAuction():
    msg_count = 0
    wait_count = 0
    rospy.init_node("auctioneer", anonymous=True)
    pub = rospy.Publisher('goal', Dst, queue_size=10)
    rospy.Subscriber("goal", Dst, gotDistance)
    r = rospy.Rate(0.5) #1hz
    msg = createMessage(1)

    while not rospy.is_shutdown():
        c_bid = rospy.get_param('~bid')
        c_robot_id = rospy.get_param('~robot_id')
        if c_bid == 8000.0:
            wait_count += 1
            if wait_count > 5:
                rospy.logwarn('no robot available')
                wait_count = 0
        else:
            wait_count = 0
        if c_bid == 0.0:
            #a robot took the job
            msg = createMessage(msg.msg_id + 1)
            msg_count = 0  
            c_bid = rospy.get_param('~bid')
            c_robot_id = rospy.get_param('~robot_id')
        if msg_count > 8:
            #robot didn't take the job
            rospy.set_param('~bid', 8000.0)
            rospy.set_param('~robot_id', 0)
            msg_count = 0
        msg.bid = c_bid
        msg.sender_id = 0
        msg.robot_id = c_robot_id
        rospy.loginfo(msg)
        pub.publish(msg)
        msg_count += 1
        r.sleep()

def gotDistance(data):
    if data.sender_id != 0:
        rospy.set_param('~bid', data.bid)
        rospy.set_param('~robot_id', data.robot_id)
        


if __name__ == '__main__':
    startAuction()
