#!/usr/bin/env python
# from vectors import Point


class Job(object):

    def __init__(self, id, cost, source,
                 destination, type):
        self.id = id
        self.cost = cost
        self.source = source
        self.source_id = source_id
        self.destination = destination
        self.destination_id = destination_id
        self.payload = ""
        self.type = type

    def printJob(self):
        print "id: %s" % self.id
        print "cost: %s" % self.cost
        print "source: (%s, %s, %s)" % (self.source[0],
                                        self.source[1],
                                        self.source[2])
        print "destination: (%s, %s, %s)" % (self.destination[0],
                                             self.destination[1],
                                             self.destination[2])
        print "payload: %s" % self.payload
