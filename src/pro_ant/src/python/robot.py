import rospy
from proAnt.msg import Dst
from classes.bidding import BidLog, CostCalculator
from classes.job import Job, Bid
import heapq


class Robot():
    def __init__(self):
        self.autoInit()
        self.id = rospy.get_param('~robot_id')
        self.base = (rospy.get_param('~base_x'),
                     rospy.get_param('~base_y'),
                     0.0)
        self.charge = 200.0
        self.rec_messages = list()
        self.heap = []
        self.bl = BidLog()
        # short sleep
        rospy.sleep(rospy.get_param('~sleep'))
        # init done
        self.listener()

    def listener(self):
        rospy.Subscriber("bid", Bid, self.gotBid)
        rospy.Subscriber("job_offer", Job, self.gotJobOffer)
        rospy.spin()

    def auto_init(self):
        rospy.set_param('~robot_id', 1)
        rospy.set_param('~base_x', 0.0)
        rospy.set_param('~base_y', 0.0)

    def gotBid(self, data):
        if data.bidder_id is not self.id:
            self.rec_messages.append(data.job_id)
            self.bl.note_bid(data.job_id, data.value)

    def gotJobOffer(self, data):
        cc = CostCalculator()
        job = Job(data.id, 0.0, (data.source_x,
                                 data.source_y,
                                 0.0), (data.dest_x,
                                        data.dest_y,
                                        0.0))
        my_bid = cc.calculate(job, self.base, self.charge)
        if my_bid > self.bl.highest_bid(job.id):
            pub = rospy.Publisher('bid', Dst, queue_size=10)
            bid_msg = Bid()
            bid_msg.job_id = job.id
            bid_msg.bidder_id = self.id
            bid_msg.value = my_bid
            pub.publish(bid_msg)


if __name__ == '__main__':
    rospy.init_node("turtle", anonymous=True)
    try:
        turt = Robot()
    except rospy.ROSInterruptException:
        pass
