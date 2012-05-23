#!/usr/bin/python
import os
from numpy import *

class cluster(object):

    def __init__(self, data_file):
        self.data = fromfile(data_file, float, -1, " ")
        self.data = self.data.reshape((len(self.data)/2, 2))
        for item in self.data:
            print item

    def kmeans(self, k):
        #self.label = array
        pass

    def _distance(point1, point2):
        s = 0
        for x in point1:
            for y in point2:
                pass


if __name__ == '__main__':
    c = cluster('exercise3-data.txt')
    c.kmeans(4)

