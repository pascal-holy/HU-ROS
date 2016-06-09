#!/usr/bin/env python
#from classes.job import Job


class DistanceMatrix(object):
    def __init__(self, maxRobots, maxJobs, base):
        self.r = maxRobots
        self.j = maxJobs
        self.distanceMatrix = [[0 for x in range(self.r)]
                               for y in range(self.j)]

    def addMessage(self, id, robot, src, base):
        
        self.distanceMatrix[robot][id] = base


