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
        self.listener()
        self.distance = 10000
        self.r, self.m = 8, 8
        self.distanceMatrix = [[0 for x in range(r)] for y in range(m)] 
    
    def gotGoal(self, data):
        pub = rospy.Publisher('distance', Dst, queue_size=10)
        msg = Dst()
        goal = (data.coord_x, data.coord_y, 0.0)
        dst = distance.euclidean(goal, self.base)
        self.distance = dst
        msg.distance = dst
        msg.robot_id = id
        pub.publish(msg)
    
    def gotDistance(self, data):
        new_robot_id = data.robot_id
        message_id = data.msg_id
        msg_count += 1
        if new_robot_id != self.id:
            rospy.loginfo("distance from other node received")
            if new_robot_id not in robot_ids:
                robot_ids.add(new_robot_id)
                distanceMatrix[new_robot_id][message_id] = data.distance
    
        if msg_count == 10:
            if self.distance < data.distance:
               rospy.loginfo("robot %i will go to ", self.id)
               msg_count = 0

    def listener(self):
        rospy.loginfo("listener1")
        rospy.Subscriber("goal", Pos, self.gotGoal)
        rospy.Subscriber("distance", Dst, self.gotDistance)
        rospy.spin()

    def shutdown(self):
        rospy.loginfo("Stop TurtleBot")
        rospy.sleep(1)



if __name__ == '__main__':
    Turtle(1)