from medianOfNinthersTranscription2 import *
from statistics import median
from copy import copy
import time
import random

def partition(r, end): # the partition function found in each of the algo files: ex bfprt_baseline.cpp
    # end is removed since it's only used for the lenght calculation
    l = len(r[:end])

    if (l < 5):
        return hoarePartition(r, l//2)
    
    j = 0

    i = 4
    while i < l:
        partition5(r, i - 4, i - 3, i, i -2 , i - 1)
        r[i], r[j] = r[j], r[i]

        i += 5
        j += 1

    quickselect(partition, r, j//2, j) # this might be incorrect
    return hoarePartition(r, j//2)

def new_median(list):
    # For no side effects
    manipList = copy(list)
    i = len(manipList)//2
    print(i)

    quickselect(partition, manipList, i, len(manipList))

    print("Manip list", manipList)
    return manipList[i]

# See bfprt_baseline.cpp for basline alg implementation

A = [9 - i for i in range(9)]

print("Before:", A)
print("New median:", new_median(A))
print("Statistics module: ", median(A))
print("After:", A)

# time the median and new_median functions with the same lists, both 10**6 elements

# print("Timing...")

# def time_median(list):
#     start = time.time()
#     print(median(list))
#     end = time.time()
#     return end - start

# def time_new_median(list):
#     start = time.time()
#     print(new_median(list))
#     end = time.time()
#     return end - start

# list = [random.randint(0,1000) for i in range(10**1-1)]
# print("Time for median:", time_median(list))
# print("Time for new_median:", time_new_median(list))
