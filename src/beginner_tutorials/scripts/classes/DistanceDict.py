#!/usr/bin/env python
from pprint import pprint
import numpy


class DistanceDict(object):
    def __init__(self):
        self.distances = dict()

    def set_distance(self, job, base, robot_id):
        goal = job.source
        base_array = numpy.array(base)
        dist = numpy.linalg.norm(base_array - goal)
        self.distances[job.id] = str(robot_id) + "-" + str(dist)

    def print_(self):
        pprint(self.distances)
