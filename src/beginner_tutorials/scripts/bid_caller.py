<<<<<<< HEAD
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
=======
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
>>>>>>> d78b5470288fbadf80e1fa26a45a0ec13870c224

    def listener(self):
        rospy.Subscriber("goal", Dst, self.gotGoal)
        rospy.spin()

<<<<<<< HEAD
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
=======
    def shutdown(self):
        rospy.loginfo("Stop TurtleBot")
        rospy.sleep(1)



if __name__ == '__main__':
    #thread.start_new_thread(Turtle,(1, 1.0, 1.0))
    
    Turtle(1, 1.0, 1.0)
>>>>>>> d78b5470288fbadf80e1fa26a45a0ec13870c224
