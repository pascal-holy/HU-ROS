#!/usr/bin/env python
import rospy
from pro_ant.msg import JobOffer, Bid, Shotgun
from classes.bidding import BidLog, CostCalculator
from classes.job import Job
from classes.movement import MoveController
import numpy as np
import heapq


class Robot():
    def __init__(self):
        if rospy.has_param('~robot_id'):
            print "autoinit"
        else:
            self.auto_init()
        self.id = rospy.get_param('~robot_id')
        self.base = (rospy.get_param('~base_x'),
                     rospy.get_param('~base_y'),
                     0.0)
        self.charge = 200.0
        self.avg_speed = 1.0
        self.max_load = 1000
        self.job_started = '00'
        self.leading = 0
        # self.rec_messages = list()
        self.jobs = list()
        self.bl = BidLog()
        self.stations = list()
        self.stations.append((1.0, 2.0, 0))
        self.stations.append((-0.5, 0.0, 0))
        self.stations.append((2.0, -0.5, 0))
        self.distances = np.matrix([[0, 2, 3], [2, 0, 3], [3, 2, 0]])
        self.navigator = MoveController()
        # short sleep
        rospy.sleep(rospy.get_param('~sleep'))
        # init done
        # navigator.calc_distance(p1, p2)
        self.listener()

    def listener(self):
        rospy.Subscriber("bid", Bid, self.gotBid)
        rospy.Subscriber("job_offer", JobOffer, self.got_job_offer)
        rospy.spin()

    def auto_init(self):
        rospy.set_param('~robot_id', 1)
        rospy.set_param('~base_x', 0.0)
        rospy.set_param('~base_y', 0.0)
        rospy.set_param('~sleep', 1.0)

    def gotBid(self, data):
        if data.bidder_id is not self.id:
            # self.rec_messages.append(data.job_id)
            self.bl.note_bid(data.job_id, data.value)

    def got_job_offer(self, data):
        cc = CostCalculator()
        job = Job(data.id, 0.0,
                  self.stations[data.source_id], data.source_id,
                  self.stations[data.destination_id], data.destination_id, 1)
        my_bid = cc.calculate(job, self.base, self.charge, self.jobs,
                              self.distances, self.avg_speed)
        if my_bid < self.bl.best_bid(job.id):
            self.bl.note_bid(job.id, my_bid)
            pub = rospy.Publisher('bid', Bid, queue_size=10)
            bid_msg = Bid()
            bid_msg.job_id = job.id
            bid_msg.bidder_id = self.id
            bid_msg.value = my_bid
            pub.publish(bid_msg)
            rospy.loginfo(bid_msg)
        if my_bid == self.bl.best_bid(job.id):
            if self.leading == 5:
                self.leading = 0  # theoretisch pro Auftrag
                print "I got the job"
                seller = rospy.Publisher('Shotgun', Shotgun, queue_size=10)
                shotgun = Shotgun()
                shotgun.bidder_id = self.id
                shotgun.job_id = job.id
                seller.publish(shotgun)
                self.jobs.append(job)
                position = {'x': job.source[0], 'y': job.source[1]}
                quaternion = {'r1': 0.000, 'r2': 0.000,
                              'r3': 0.000, 'r4': 1.000}
                rospy.loginfo("Go to (%s, %s) pose",
                              position['x'], position['y'])
                # success = self.navigator.goto(position, quaternion)
            self.leading += 1


if __name__ == '__main__':
    rospy.init_node("turtle", anonymous=True)
    try:
        turt = Robot()
    except rospy.ROSInterruptException:
        pass
