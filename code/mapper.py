#!/usr/bin/env python2.7

import numpy as np
import random
import sys
from sets import Set


r = 8  #int(sys.argv[1])
b = 16 #int(sys.argv[2])
hashnum = 128
buckets = 256 # number of buckets
buck = [set() for index in xrange(buckets)] # sets of bucket

def partition(video_id, shingles):
    key = ""
    for word in shingles:
        for i in range(0, hashnum,1):
            M[i] = min((hasha[i]*word+hashb[i])%10001, M[i])
    #Passing signature matrix to reducer
    print "M,",
    for i in range(0,hashnum,1):
        print int(M[i]), '\t',
    print
    #Mapping to buckets
    for i in range(0, hashnum, r):
        h = 0
        for j in range(0, r, 1):
            h = (M[i + j] * hashc[j] + hashd[j]) % buckets
        buck[int(h)].add(video_id)


if __name__ == "__main__":
    # Very important. Make sure that each machine is using the
    # same seed when generating random numbers for the hash functions.
    np.random.seed(seed=42)
    hasha = []
    hashb = []
    #Generate hash function paramters
    hasha = np.random.randint(1,10001, hashnum)
    hashb = np.random.randint(1,10001, hashnum)
    hashc = np.random.randint(1, buckets, r)
    hashd = np.random.randint(1, buckets, r)

    for line in sys.stdin:
        line = line.strip()
        video_id = int(line[6:15])
        shingles = np.fromstring(line[16:], sep=" ")
        M = []
        for i in range(0, hashnum,1):
            M.append(10001)
        partition(video_id, shingles)
    #Passing bucket sets to reducer
    for i in range(0, buckets ,1):
        if len(buck[i]) > 0 :
            print 'B,',
            for j in buck[i]:
                print j, '\t',
            print

