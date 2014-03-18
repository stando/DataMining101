#!/usr/bin/env python2.7

import numpy as np
import sys

"""
def print_duplicates(videos):
    unique = np.unique(videos)
    for i in xrange(len(unique)):
        for j in xrange(i + 1, len(unique)):
            print "%d\t%d" % (min(unique[i], unique[j]),
                              max(unique[i], unique[j]))
"""

last_key = None
key_count = 0
buck_count = 0
duplicates = []
video_id = []
keystore = []
buckstore = []
hashnum = 128

for line in sys.stdin:
    line = line.strip()
    key, video= line.split(",")
    if key == 'M':
        keystore.append(video.split("\t"))
        key_count = key_count + 1
    else:
        buckstore.append(video.split("\t"))
        buck_count = buck_count + 1

    #video_id.append(video)
    #keystore.append(key.split("\t"))

for i in range(0, buck_count, 1):
    for j in range(0, len(buckstore[i]), 1):
        id_j = int(buckstore[i][j])
        for k in range(j+1, len(buckstore[i]), 1):
            id_k = int(buckstore[i][k])
            ans = 0
            for l in range(0, hashnum, 1):
                if keystore[id_j][l]==keystore[id_k][l]:
                    ans = ans + 1
            if ans * 1.0 / hashnum >= 0.85:
                print "%s\t%s" % (min(id_j, id_k),
                                  max(id_j, id_k))


        """
    if last_key is None:
        last_key = key

    if key == last_key:
        duplicates.append(int(video_id))
    else:
        # Key changed (previous line was k=x, this line is k=y)
        print_duplicates(duplicates)
        duplicates = [int(video_id)]
        last_key = key

if len(duplicates) > 0:
    print_duplicates(duplicates)
    """
