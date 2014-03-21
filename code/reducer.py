#!/usr/bin/env python2.7

import numpy as np
import sys
#from sets import Set

key_count = 0
buck_count = 0
video_id = []
duplicates = []
buckets = 10007
buck = set() #for index in xrange(buckets)]
hashnum = 200
last_key= None

def print_duplicates(buck):
    for j in range(0, len(buck), 1):
        video_j = buck[j][0]
        set_j=set()
        for x in range(1,len(buck[j]),1):
            set_j.add(buck[j][x])
        for k in range(j+1, len(buck), 1):
            video_k = int(buck[k][0])
            set_k=set()
            for x in range(1,len(buck[k]),1):
                set_k.add(buck[k][x])
            th = float(len(set_j.intersection(set_k)))/ len(set_j.union(set_k))
            if th>= 0.85:
                print "%d\t%d" % (min(video_j, video_k),
                                  max(video_j, video_k))


for line in sys.stdin:
    line = line.strip()
    bucknr, ert = line.split("\t")
    ert = [int(v) for v in ert[1:-1].split(', ')]
    ert = list(ert)

   #buck[int(bucknr)].add(ert)
    if last_key is None:
        last_key = bucknr

    if bucknr == last_key:
        duplicates.append(ert)
    else :
        print_duplicates(duplicates)
        duplicates = [ert]
        last_key = bucknr
if len(duplicates)>0:
    print_duplicates(duplicates)


