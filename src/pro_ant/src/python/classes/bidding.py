#!/usr/bin/env python
from pprint import pprint
import numpy


class BidLog(object):
    def __init__(self):
        self.distances = dict()

    def note_bid(self, job_id, bid):
        if job_id in self.distances:
            if self.distances[job_id] > bid:
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

    def best_bid(self, job_id):
        if job_id in self.distances:
            return self.distances[job_id]
        else:
            return 10000


class CostCalculator(object):
    def __init__(self):
        cost = 0.0

    def calculate(self, new_job, base, charge, job_queue, distances, speed):
        sum_distance = 0
        first = True
        last_job = None
        for job in job_queue:
            sum_distance += distances[job.source_id, job.destination_id]
            if not first:
                sum_distance += distances[last_job.destination, job.source]
                first = False
            last_job = job
        dist = sum_distance
        dist += distances[new_job.source_id, new_job.destination_id]
        return dist * speed
