#!/usr/bin/env python2.7

import numpy as np
import sys
from sets import Set

key_count = 0
buck_count = 0
video_id = []
buckets = 256
buck = [set() for index in xrange(buckets)]
hashnum = 128

for line in sys.stdin:
    line = line.strip()
    bucknr, ert = line.split(":")
    buck[int(bucknr)].add(ert)

for i in range(0, buckets, 1):
    buck[i] = np.unique(buck[i])
    for j in range(0, len(buck[i]), 1):
        video_j = int(buck[i][j][7:16])
        num_j= np.fromstring(buck[i][j][17:], dtype = int, sep = " ")
        set_j=Set()
        for x in num_j:
            set_j.add(x)
        for k in range(j+1, len(buck[i]), 1):
            video_k = int(buck[i][k][7:16])
            num_k= np.fromstring(buck[i][k][17:], dtype = int, sep = " ")
            set_k=Set()
            for x in num_k:
                set_k.add(x)
            if len(set_j.intersection(set_k))*1.0/ len(set_j.union(set_k)) >= 0.85:
                print "%s\t%s" % (min(video_j, video_k),
                                  max(video_j, video_k))


