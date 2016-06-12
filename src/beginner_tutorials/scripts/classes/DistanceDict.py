#!/usr/bin/env python
from classes.job import Job
import numpy


class DistanceDict(object):
    def __init__(self):
        self.distances = dict()

    def set_distance(self, job, my_base):
        job2 = Job()
        goal = job.source
        base = my_base
        dist = numpy.linalg.norm(base - goal)
        if self.distances[job.id]
        self.distances[job.id] = dist

    def 
