#!/usr/bin/python
import os
from numpy import *

class cluster(object):

    def __init__(self, data_file):
        self.data = fromfile(data_file, float, -1, " ")
        print self.data
    def kmeans(self, k):
        #self.label = array
        pass



if __name__ == '__main__':
    c = cluster('exercise3-data.txt')
    c.kmeans(4)

