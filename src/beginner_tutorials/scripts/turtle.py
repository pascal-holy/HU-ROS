import rospy
from scipy.spatial import distance
from beginner_tutorials.msg import Pos
from beginner_tutorials.msg import Dst
from std_msgs.msg import String


class Turtle(object):
    def __init__(self, robot_id):
        # initiliaze
        rospy.init_node("turtle", anonymous=True)
        self.id = robot_id
        self.base = (1.0, 2.0, 3.0)
        self.distance = 10000
        self.robot_ids = list()
        self.r, self.m = 3, 3
        self.distanceMatrix = [[0 for x in range(self.r)] for y in range(self.m)]
        self.msg_count = 0
        self.listener()
    
    def gotGoal(self, data):
        pub = rospy.Publisher('distance', Dst, queue_size=10)
        msg = Dst()
        goal = (data.coord_x, data.coord_y, 0.0)
        dst = distance.euclidean(goal, self.base)
        self.distance = dst
        rospy.loginfo("robot %i has distance %f to message %i", self.id, dst, data.id)
        msg.distance = dst
        msg.robot_id = self.id
        msg.msg_id = data.id
        pub.publish(msg)
    
    def gotDistance(self, data):
        new_robot_id = data.robot_id
        message_id = data.msg_id
        self.msg_count += 1
        if new_robot_id != self.id:
            #rospy.loginfo("distance from other node received")
            self.robot_ids.append(new_robot_id)
            self.distanceMatrix[new_robot_id][message_id] = data.distance
        else:#own distances are written in the first lie of the matrix
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
        rospy.Subscriber("goal", Pos, self.gotGoal)
        rospy.Subscriber("distance", Dst, self.gotDistance)
        rospy.spin()

    def shutdown(self):
        rospy.loginfo("Stop TurtleBot")
        rospy.sleep(1)



if __name__ == '__main__':
    Turtle(1)