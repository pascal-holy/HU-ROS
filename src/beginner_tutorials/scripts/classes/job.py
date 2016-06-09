#!/usr/bin/env python
# from vectors import Point


class Job(object):

    def __init__(self, id, source, destination):
        self.id = id
        self.source = source
        self.destination = destination

    def printJob(self):
        print "id: %s" % self.id
        print "source: (%s, %s, %s)" % (self.source[0],
                                        self.source[1],
                                        self.source[2])
        print "destination: (%s, %s, %s)" % (self.destination[0],
                                             self.destination[1],
                                             self.destination[2])
