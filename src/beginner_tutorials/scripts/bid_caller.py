#!/usr/bin/env python
import rospy
import numpy
from beginner_tutorials.msg import Dst
from classes.job import Job, DistanceMatrix


class Turtle(object):

    def __init__(self):
        self.autoInit()
        self.distance = 8000.0
        self.msg_count = 0
        self.robot_id = rospy.get_param('~robot_id')
        self.base = (rospy.get_param('~base_x'),
                     rospy.get_param('~base_y'),
                     0.0)
        self.rec_messages = list()
        self.jobList = list()
        self.distanceMatrix = DistanceMatrix(3, 3, base)
        job = Job(1, (1.0, 2.0, 3.0), (2.0, 3.0, 4.0))
        self.jobList.append(job)
        job.printJob()
        # short sleep
        rospy.sleep(rospy.get_param('~sleep'))
        # init done
        self.listener()

    def gotGoal(self, data):
        if data.msg_id not in self.rec_messages:
            self.rec_messages.append(data.msg_id)
            goal = (data.goal_x, data.goal_y, 0.0)
            base = numpy.array(self.base)
            dst = numpy.linalg.norm(base - goal)
            

            self.distance = dst.item()
            # rospy.logdebug("robot %i has distance %f to goal %i", self.robot_id, dst, data.msg_id) # noqa
            self.msg_count = 0
        if data.bid >= self.distance:
            # I'm closest to the goal do a bid
            pub = rospy.Publisher('goal', Dst, queue_size=10)
            msg = Dst()
            msg.msg_id = data.msg_id
            msg.sender_id = self.robot_id
            msg.goal_x = data.goal_x
            msg.goal_y = data.goal_y
            msg.bid = self.distance
            msg.robot_id = self.robot_id
            rospy.loginfo("robot %i is closest to goal %i",
                          self.robot_id, data.msg_id)
            if self.msg_count > 5:
                rospy.loginfo(
                    "robot %i took the job %i", self.robot_id, data.msg_id)
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

    def autoInit(self):
        if not rospy.has_param('robot_id'):
            print('autoconfig')
            rospy.set_param('~robot_id', 1)
            rospy.set_param('~sleep', 0.0)
            rospy.set_param('~base_x', 1.1)
            rospy.set_param('~base_y', 1.1)

if __name__ == '__main__':

    rospy.init_node("turtle", anonymous=True)
    try:
        turt = Turtle()
    except rospy.ROSInterruptException:
        pass
