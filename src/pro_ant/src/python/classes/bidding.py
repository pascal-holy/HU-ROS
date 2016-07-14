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
    def __init__(self, navigator):
        cost = 0.0
        self.navigator = navigator

    def calculate(self, new_job, base, charge, job_queue, distances, speed):
        sum_distance = 0
        first = True
        last_job = None
        for job in job_queue:
            try:
                sum_distance += distances[(job.source, job.destination)]
            except KeyError:
                dist_start_end = navigator.calc_distance(job.source, job.destination)
                distances.add((job.source, job.destination), dist_start_end)
                sum_distance += dist_start_end
            if not first:
                try:
                    sum_distance += distances[(last_job.destination, job.source)]
                except KeyError:
                    dist_lastend_start = navigator.calc_distance(last_job.destination, job.source)
                    distances.add((last_job.destination, job.source), dist_lastend_start)    
                    sum_distance += dist_lastend_start
                first = False

            last_job = job
        dist = sum_distance
        try:
            dist += distances[(new_job.source_id, new_job.destination_id)]
        except KeyError:
            dist_newstart_end = navigator.calc_distance(new_job.source_id, new_job.destination_id)
            distances.add((new_job.source_id, new_job.destination_id), dist_newstart_end)
            dist *= dist_newstart_end
        return dist * speed
