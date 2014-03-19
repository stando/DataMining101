#!/usr/bin/env python

import sys


last_key = None
key_count = 0
threshold = 0.85
duplicates = []


class Video:
    idx = 0
    shingles = set()
    def __init__(self, idx = 0, shingles = set()):
        self.idx = idx
        self.shingles = shingles
    def __eq__(self, v):
        if not isinstance(v, Video):
            return False
        
        return self.idx == v.idx


def jaccard_dist(video_a, video_b):
    return len(video_a.shingles.intersection(video_b.shingles)) / \
            len(video_a.shingles.union(video_b.shingles))

def print_duplicates(videos):
    # print all duplicates after eliminating possible false positives
    
    # Rid of possible duplicates
    unique = list(set(videos))
    for i in xrange(len(unique)):
        for j in xrange(i + 1, len(unique)):
            if jaccard_dist(unique[i], unique[j]) >= threshold:
                print "%d\t%d" % (min(unique[i].idx, unique[j].idx), \
                                  max(unique[i].idx, unique[j].idx))


for line in sys.stdin:
    line = line.strip()
    key, val = line.split("\t")
    
    # Strip video id and shingles
    val = [int(v) for v in val[1:-1].split(', ')]
    
    video = Video(val[0], set(val[1:]))

    if last_key is None:
        last_key = key

    if key == last_key:
        duplicates.append(video)
    else:
        # Key changed (previous line was k=x, this line is k=y)
        print_duplicates(duplicates)
        duplicates = [video]
        last_key = key

if len(duplicates) > 0:
    print_duplicates(duplicates)
