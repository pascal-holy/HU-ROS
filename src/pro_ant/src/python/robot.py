#!/usr/bin/env python
import rospy
from pro_ant.msg import JobOffer, Bid
from classes.bidding import BidLog, CostCalculator
from classes.job import Job
import heapq


class Robot():
    def __init__(self):
        self.auto_init()
        self.id = rospy.get_param('~robot_id')
        self.base = (rospy.get_param('~base_x'),
                     rospy.get_param('~base_y'),
                     0.0)
        self.charge = 200.0
        self.leading = 0
        self.rec_messages = list()
        self.heap = []
        self.bl = BidLog()
        # short sleep
        rospy.sleep(rospy.get_param('~sleep'))
        # init done
        self.listener()

    def listener(self):
        rospy.Subscriber("bid", Bid, self.gotBid)
        rospy.Subscriber("job_offer", JobOffer, self.got_job_offer)
        rospy.spin()

    def auto_init(self):
        rospy.set_param('~robot_id', 1)
        rospy.set_param('~base_x', 0.0)
        rospy.set_param('~base_y', 0.0)
        rospy.set_param('~sleep', 0.0)

    def gotBid(self, data):
        if data.bidder_id is not self.id:
            self.rec_messages.append(data.job_id)
            self.bl.note_bid(data.job_id, data.value)

    def got_job_offer(self, data):
        cc = CostCalculator()
        print "got job"
        job = Job(data.id, 0.0, (data.source_x,
                                 data.source_y,
                                 0.0), (data.dest_x,
                                        data.dest_y,
                                        0.0))
        my_bid = cc.calculate(job, self.base, self.charge)
        if my_bid > self.bl.highest_bid(job.id):
            self.bl.note_bid(job.id, my_bid)
            pub = rospy.Publisher('bid', Bid, queue_size=10)
            bid_msg = Bid()
            bid_msg.job_id = job.id
            bid_msg.bidder_id = self.id
            bid_msg.value = my_bid
            pub.publish(bid_msg)
            rospy.loginfo(bid_msg)
        if my_bid == self.bl.highest_bid(job.id):
            if self.leading == 5:
                print "I got the job"
            self.leading += 1


if __name__ == '__main__':
    rospy.init_node("turtle", anonymous=True)
    try:
        turt = Robot()
    except rospy.ROSInterruptException:
        pass
