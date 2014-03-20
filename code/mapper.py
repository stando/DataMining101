#!/usr/bin/env python

import numpy as np
import sys

nRow = 5
nBand = 40
nHash = nRow * nBand
nBucket = 10007
maxShingle = 10000

def makeHashFunc(a, b, c):
    return lambda x: (a * x + b) % c 


def batchHashFunc(nHashFunc, nShingles):
    # randomly generate a group of (a, b) for linear hashing functions
    A = np.random.randint(1, 1001, size=(nHashFunc,) )
    B = np.random.randint(1, 1001, size=(nHashFunc,) )
    c = nShingles
    
    F = []
    
    for i in range(nHashFunc):
        f = makeHashFunc(A[i], B[i], c)
        F.append(f)
        
    return F


def printKVPair(video_id, shingles, hashTable):
    # Output all (key, value) pairs for one single band. 
    # key:=(band_id, bucket_id)
    # value:=(video_id, shingles)
    
    for band_id, bucket_id in enumerate(hashTable):
        for (vi, si, bi) in zip(video_id, shingles, bucket_id):
            key = (band_id, bi)
            # first element is the video id, the rest are shingles
            value = [vi] + si     
            print('%s\t%s' % (key, value))    
    
    return

def minHash(shingles):
    # Min Hash algorithm with jarccard distance
    
    [nShingles, nData] = shingles.shape
    
    signature = np.ndarray(shape=(nHash, nData), dtype=int)
    signature.fill(sys.maxint)  # Filled with dummy value

    # Generate hash functions (a*i+b uniformly at random)
    hfs = batchHashFunc(nHash, nShingles)
    
    # Step through each row and update signature matrix if shringles[r][c] = 1
    # TODO: Is it even a good idea?
    for i, row in enumerate(shingles):
        hashValues = [hf(i) for hf in hfs]
        for j, element in enumerate(row):
            if element == 1:
                # Update the minimum values for each hash function
                signature[:, j] = np.minimum(signature[:, j], hashValues)
                
    return signature


def lsh(signature):
    # Locality Sensitive Hashing on signature matrix. Note that only AND operation is considered here. OR operation is implicitly done in the pipeline of MapReduce.
    
    [_, nData] = signature.shape
    hashTable = np.ndarray(shape=(nBand, nData), dtype=int)
    hashTable.fill(0)
    
    # Split signature matrix into multiple bands
    bands = np.vsplit(signature, nBand)
    
    # Linear hash function (A*S+b uniformly at random)
    # TODO: Should we generate different hash functions for different bands
    # Simple hack, we use homogeneous coordinates here
    W = np.random.randint(1, 1001, size=(nRow+1,))
         
    # Calculate hash values. One band at a time.     
    for band, col in zip(bands, hashTable):
            col[:] = (np.dot(W[0:-1], band) + np.tile(W[-1], nData)) % nBucket
                
    return hashTable


def mapper(video_id, video_shingle, raw_shingle):
    # main body for lsh mapper
    
    # transform list video_shingle into a numpy 2d array. Each row represent a shingle and each col is a video
    shingles = np.array(video_shingle).transpose()
    
    signature = minHash(shingles)
    hashTable = lsh(signature)
    printKVPair(video_id, raw_shingle, hashTable)
    
    return

def convertToIndex(shingles):
    # Convert shingles into an index representation

    idx = [0] * (maxShingle + 1)
        
    for shingle in shingles:
        idx[shingle] = 1
        
    return idx

if __name__ == "__main__":
    # Very important. Make sure that each machine is using the
    # same seed when generating random numbers for the hash functions.
    np.random.seed(seed=100)
    video_id = []
    video_shingle = []
    raw_shingle = []
    
    # TODO: comment this out
    #   f = open('../data/toy.txt', 'r+')
    #   for line in f:
        
    for line in sys.stdin:
        line = line.strip()
        vid = int(line[6:15])
        shingles = np.fromstring(line[16:], dtype=int, sep=" ")
        raw_shingle.append(shingles.tolist())
        shingleIdx = convertToIndex(shingles)
        video_id.append(vid)
        video_shingle.append(shingleIdx)
    
    mapper(video_id, video_shingle, raw_shingle)
        
