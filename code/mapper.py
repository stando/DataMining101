#!/usr/bin/env python2.7

import numpy as np
import random
import sys
from sets import Set


r = 5  #int(sys.argv[1])
b = 40 #int(sys.argv[2])
hashnum = 200
buckets = 10007 # number of buckets
buck = [set() for index in xrange(buckets)] # sets of bucket
Matrix = []
L = []

def partition(Line):
    for j in range(0,len(Line),1):
        M = []
        for i in range(0, hashnum,1):
            M.append(10001)
        video_id = int(Line[j][6:15])
        shingles = np.fromstring(Line[j][16:], sep=" ")
        for word in shingles:
            for i in range(0, hashnum,1):
                M[i] = min((hasha[i]*word+hashb[i])%10001, M[i])
        Matrix.append(M)

if __name__ == "__main__":
    # Very important. Make sure that each machine is using the
    # same seed when generating random numbers for the hash functions.
    np.random.seed(seed=42)
    #Generate hash function paramters
    hasha = np.random.randint(1,1001, hashnum)
    hashb = np.random.randint(1,1001, hashnum)
    hashc = np.random.randint(1, 1001, r+1)
    #hashd = np.random.randint(1, 1001, r)

    for line in sys.stdin:
        line = line.strip()
        L.append(line)
    partition(L)
    #Passing bucket sets to reducer
     #Mapping to buckets
    for i in range(0, hashnum, r):
        for k in range(0, len(Matrix) , 1):
            h = 0
            for j in range(0, r, 1):
                h = (h + Matrix[k][i + j] * hashc[j]) % buckets
            h = (h+hashc[r]) % buckets
            video_id = int(L[k][6:15])
            scheisse = []
            scheisse.append(video_id)
            shingles = np.fromstring(L[k][16:], sep=" ")
            for word in shingles:
                scheisse.append(int(word))
            print ('%s\t%s' % ((int(i/r),int(h)),scheisse))
        #line2 = str(int(i/r))+"%"+line
        #buck[int(h)].add(line2)

