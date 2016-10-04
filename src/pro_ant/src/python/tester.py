#!/usr/bin/env python
from classes.bidding import BidLog, CostCalculator
from classes.movement import MoveController
from classes.job import Job
from geometry_msgs.msg import Point
import heapq
import numpy as np
import time


bl = BidLog()
cc = CostCalculator()
job1 = Job(1, 0.0, (1, 2, 3), 0, (2, 3, 4), 1, 1)
job2 = Job(2, 0.0, (3, 4, 5), 2, (2, 3, 4), 1, 1)
base = (0, 0, 0)
distMatrix = np.matrix([[0, 2, 3], [2, 0, 3], [3, 2, 0]])
jobQueue = list()

bl.note_bid(1, 100.0)
bl.note_bid(1, 200.0)
bl.note_bid(2, 300.0)
bl.note_bid(2, 500.0)
bl.note_bid(1, 400.0)
# bl.print_()

# print distMatrix[0, 0]
# print(cc.calculate(job1, (0, 0, 0), 100, jobQueue, distMatrix, 1.0))
print(bl.best_bid(1))
print(bl.best_bid(2))


jobList = list()
# jobList.append(job1)
# jobList.append(job2)


# for job in jobList:
#     my_bid = cc.calculate(job, (0, 0, 0), 500, jobQueue, distMatrix, 1.0)
#     print my_bid
#     if my_bid > bl.highest_bid(job.id):
#         print "I'm highest bidder for job %i!" % job.id

# heap = []
# heapq.heappush(heap, 2)
# heapq.heappush(heap, 4)
# # print heapq.heappushpop(heap, 3)

# navigator = MoveController()

# p1 = Point(float(-3), float(1), 0.0)
# p2 = Point(float(-3), float(-2), 0.0)
# print 'distance %f' % navigator.calc_distance(p1, p2)
# p1 = Point(float(1), float(1), 0.0)
# p2 = Point(float(0), float(0), 0.0)
# start = time.time()
# print 'distance %f' % navigator.calc_distance(p1, p2)
# end = time.time()
# delta = end - start
# print delta