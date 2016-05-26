import rospy
import thread
from scipy.spatial import distance
from beginner_tutorials.msg import Pos
from beginner_tutorials.msg import Dst
from std_msgs.msg import String


class Turtle(object):
    def __init__(self, robot_id, base_x, base_y):
        # initiliaze
        rospy.init_node("turtle", anonymous=True)
        self.id = robot_id
        self.base = (1.0, base_x, base_y)
        self.distance = 8000
        self.robot_ids = list()
        self.r, self.m = 3, 3
        self.distanceMatrix = [[0 for x in range(self.r)] for y in range(self.m)]
        self.msg_count = 0
        self.listener()
    
    def gotGoal(self, data):
        if self.distance == 8000:
            goal = (data.goal_x, data.goal_y, 0.0)
            dst = distance.euclidean(goal, self.base)
            self.distance = dst
            rospy.loginfo("robot %i has distance %f to goal %i", self.id, dst, data.msg_id)
        if data.robot_id != self.id:
            if data.bid >= self.distance:
                pub = rospy.Publisher('goal', Dst, queue_size=10)
                msg = Dst()
                msg.msg_id = data.msg_id
                msg.goal_x = data.goal_x
                msg.goal_y = data.goal_y
                msg.bid = self.distance
                msg.robot_id = self.id
                pub.publish(msg)
                rospy.loginfo("robot %i is closest to goal %i", self.id, data.msg_id)
    
    def gotDistance(self, data):
        new_robot_id = data.robot_id
        message_id = data.msg_id
        self.msg_count += 1
        if new_robot_id != self.id:
            #rospy.loginfo("distance from other node received")
            self.robot_ids.append(new_robot_id)
            self.distanceMatrix[new_robot_id][message_id] = data.distance
        else:#own distances are written in the first line of the matrix
            self.distanceMatrix[0][message_id] = data.distance
            self.distanceMatrix[new_robot_id][message_id] = data.distance
    
        if self.msg_count == 10:
            shortest = 10000.0
            for i in range(self.m):
                for j in range(self.r):
                    c_dst = self.distanceMatrix[i][j]
                    print("%.2f" % round(c_dst,2)),
                    if c_dst > 0 and c_dst < shortest:
                        shortest = c_dst
                print
            print
            if self.distance < shortest:
               rospy.loginfo("robot %i will go to ", self.id)
            self.msg_count = 0

    def listener(self):
        rospy.Subscriber("goal", Dst, self.gotGoal)
        rospy.spin()

    def shutdown(self):
        rospy.loginfo("Stop TurtleBot")
        rospy.sleep(1)



if __name__ == '__main__':
    #thread.start_new_thread(Turtle,(1, 1.0, 1.0))
    
    Turtle(1, 1.0, 1.0)
