#!/usr/bin/env python
from classes.bidding import BidLog, CostCalculator
from classes.job import Job
import heapq


bl = BidLog()
cc = CostCalculator()
job1 = Job(1, 0.0, (1, 2, 3), (2, 3, 4))
job2 = Job(2, 0.0, (3, 4, 5), (2, 3, 4))
base = (0, 0, 0)
bl.note_bid(job1, 100.0)
bl.note_bid(job1, 200.0)
bl.note_bid(job2, 300.0)
bl.note_bid(job2, 500.0)
bl.note_bid(job1, 400.0)
bl.print_()
print(cc.calculate(job1, (0, 0, 0), 100))
print(bl.highest_bid(job1))
print(bl.highest_bid(job2))


jobList = list()
jobList.append(job1)
jobList.append(job2)

for job in jobList:
    my_bid = cc.calculate(job, (0, 0, 0), 500)
    print my_bid
    if my_bid > bl.highest_bid(job):
        print "I'm highest bidder for job %i!" % job.id

heap = []
heapq.heappush(heap, 2)
heapq.heappush(heap, 4)
print heapq.heappushpop(heap, 3)
