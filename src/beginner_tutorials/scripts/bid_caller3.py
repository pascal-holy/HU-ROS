#!/usr/bin/env python
import rospy
import numpy
from scipy.spatial import distance
from beginner_tutorials.msg import Dst

class Turtle(object):
    def __init__(self):
        self.distance = 8000.0
        self.msg_count = 0
        self.robot_id = rospy.get_param('~robot_id')
        self.rec_messages = list()
        rospy.sleep(rospy.get_param('~sleep'))
        #init done
        self.listener()

    def gotGoal(self, data):
        if data.sender_id == 0:
            #message is from auctioneer
            if data.msg_id not in self.rec_messages:
                self.rec_messages.append(data.msg_id)
                goal = (data.goal_x, data.goal_y, 0.0)
                base = numpy.array((rospy.get_param('~base_x'), rospy.get_param('~base_y'), 0.0))
                dst = numpy.linalg.norm(base-goal)
                #dst = distance.euclidean(base2, base2)
                self.distance = dst.item()
                #rospy.logdebug("robot %i has distance %f to goal %i", self.robot_id, dst, data.msg_id)
                self.msg_count = 0
            if data.bid >= self.distance:
                #I'm closest to the goal do a bid
                pub = rospy.Publisher('goal', Dst, queue_size=10)
                msg = Dst()
                msg.msg_id = data.msg_id
                msg.sender_id = self.robot_id
                msg.goal_x = data.goal_x
                msg.goal_y = data.goal_y
                msg.bid = self.distance
                msg.robot_id = self.robot_id
                rospy.loginfo("robot %i is closest to goal %i", self.robot_id, data.msg_id)
                if self.msg_count > 5:
                    rospy.loginfo("robot %i took the job %i", self.robot_id, data.msg_id)
                    msg.bid = 0.0
                    self.msg_count = 0
                    self.moveToGoal()
                else:
                    pub.publish(msg)
                    self.msg_count += 1

    def listener(self):
        rospy.Subscriber("goal", Dst, self.gotGoal)
        rospy.spin()

    def moveToGoal(self):
        rospy.loginfo("moving TurtleBot")
        rospy.sleep(self.distance * 10)



if __name__ == '__main__':
    rospy.init_node("turtle", anonymous=True)
    try:
        turt = Turtle()
    except rospy.ROSInterruptException: pass
