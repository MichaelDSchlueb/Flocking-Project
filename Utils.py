# File containing utility functions for the application

import math
import numpy as np

def distance(vectorA, vectorB):
    diff1 = vectorA[0] - vectorB[0]
    diff2 = vectorA[1] - vectorB[1]
    return(math.sqrt(diff1*diff1+diff2*diff2))

def isZero(vec):
    return(np.all(vec == 0))

def length(vec):
    return(math.sqrt(vec[0]*vec[0] + vec[1]*vec[1]))

def normalize(vec):
    if len(vec) != 2:
        print("Error: trying to normalize an invalid 2d vector")
        return(vec)
    x, y = vec[0], vec[1]
    mag = math.sqrt(x*x + y*y)
    if mag == 0:
        return 0
    normalVec = vec / mag
    return(normalVec)

def difference(vectorA, vectorB):
    diffs = np.array([0,0])
    diffs[0] = vectorA[0] - vectorB[0]
    diffs[1] = vectorB[1] - vectorB[1]
    return diffs

def average(vector, averagingFactor):
    avg = np.array([0,0])
    avg[0] = vector[0]/averagingFactor
    avg[1] = vector[1]/averagingFactor
    return avg