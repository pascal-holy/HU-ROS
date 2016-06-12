import rospy
from classes.bidding import BidLog, CostCalculator
from classes.job import Job
import heapq


class Robot():
    def __init__(self):
        self.autoInit()
        self.id = rospy.get_param('~robot_id')
        self.base = (rospy.get_param('~base_x'),
                     rospy.get_param('~base_y'),
                     0.0)
        self.rec_messages = list()
        self.heap = []
        # short sleep
        rospy.sleep(rospy.get_param('~sleep'))
        # init done
        self.listener()

    def listener(self):
        rospy.Subscriber("goal", Dst, self.gotGoal)
        rospy.spin()

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

if __name__ == '__main__':
    rospy.init_node("turtle", anonymous=True)
    try:
        turt = Robot()
    except rospy.ROSInterruptException:
        pass
