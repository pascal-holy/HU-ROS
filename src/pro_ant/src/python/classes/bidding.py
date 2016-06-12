#!/usr/bin/env python
from pprint import pprint
import numpy


class BidLog(object):
    def __init__(self):
        self.distances = dict()

    def note_bid(self, job_id, bid):
        if job_id in self.distances:
            if self.distances[job_id] < bid:
                self.distances[job_id] = bid
        else:
            self.distances[job_id] = bid

    def delete_bid(self, job_id):
        if job_id in self.distances:
            del self.distances[job_id]
        else:
            print("key %s not existent", job_id)

    def print_(self):
        pprint(self.distances)

    def highest_bid(self, job):
        return self.distances[job.id]


class CostCalculator(object):
    def __init__(self):
        cost = 0.0

    def calculate(self, job, base, charge):
        goal = job.source
        base_array = numpy.array(base)
        dist = numpy.linalg.norm(base_array - goal)
        return charge - dist
