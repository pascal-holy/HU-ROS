#!/usr/bin/env python
import rospy
import actionlib
from actionlib_msgs.msg import *
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import PoseStamped, Pose, Point, Quaternion
from nav_msgs.srv import GetPlan
from std_msgs.msg import Header
from pprint import pprint
import math


class MoveController():
    def __init__(self):
        self.goal_sent = False
        # rospy.init_node("MC", anonymous=True)
        # What to do if shut down (e.g. Ctrl-C or failure)
        rospy.on_shutdown(self.shutdown)

        # Tell the action client that we want to spin a thread by default
        self.move_base = actionlib.SimpleActionClient("move_base",
                                                      MoveBaseAction)
        rospy.loginfo("Wait for the action server to come up")

        # Allow up to 5 seconds for the action server to come up
        # self.move_base.wait_for_server()
        rospy.loginfo("action server up")

    def goto(self, pos, quat):

        # Send a goal
        self.goal_sent = True
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = 'map'
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose = Pose(Point(pos['x'], pos['y'], 0.000),
                                     Quaternion(quat['r1'],
                                                quat['r2'],
                                                quat['r3'],
                                                quat['r4']))

        # Start moving
        self.move_base.send_goal(goal)

        # Allow TurtleBot up to 60 seconds to complete task
        success = self.move_base.wait_for_result(rospy.Duration(60))

        state = self.move_base.get_state()
        result = False

        if success and state == GoalStatus.SUCCEEDED:
            # We made it!
            result = True
        else:
            self.move_base.cancel_goal()

        self.goal_sent = False
        return result

    def calc_distance(self, p1, p2):
        service_name = "/move_base/make_plan"
        rospy.wait_for_service(service_name)
        planpath = rospy.ServiceProxy(service_name, GetPlan)
        posestampeds = PoseStamped()
        posestampeds.header = Header()
        posestampeds.header.frame_id = 'map'
        posestampeds.header.stamp = rospy.Time.now()
        # Orientation not important for distance calculation
        quaternion = Quaternion(float(0), float(0), float(0), float(0))
        posestampeds.pose = Pose(p1, quaternion)
        posestampede = PoseStamped()
        posestampede.header = Header()
        posestampede.header.frame_id = 'map'
        posestampede.header.stamp = rospy.Time.now()
        posestampede.pose = Pose(p2, quaternion)

        try:
            poses = planpath(posestampeds, posestampede, 0.1).plan.poses
            distance = 0.0
            for i in range(0, len(poses)-1):
                startpoint = poses[i].pose.position
                endpoint = poses[i+1].pose.position
                distance += math.sqrt((startpoint.x - endpoint.x)**2 
                            + (startpoint.y - endpoint.y)**2)
            return distance
        except rospy.ServiceException as exc:
            print("Service did not process request: " + str(exc))
            return None

    def shutdown(self):
        if self.goal_sent:
            self.move_base.cancel_goal()
        rospy.loginfo("Stop")
        rospy.sleep(1)
