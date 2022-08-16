from statistics import median
from medianOfNinthers import *
from random import randint, shuffle

# Test all different cases of medians3 function
def test_median3_zeros():
    a = [0,0,0]
    assert median3(a,0,1,2) == a.index(median(a))

def test_median3_equal():
    a = [1,1,1]
    assert median3(a,0,1,2) == a.index(median(a))

def test_median3_zero_one():
    a = [0,1,2]
    assert median3(a,0,1,2) == a.index(median(a))

def test_median3_first():
    a = [2,1,3]
    assert median3(a,0,1,2) == a.index(median(a))

def test_median3_second():
    a = [1,2,3]
    assert median3(a,0,1,2) == a.index(median(a))

def test_median3_second_flip():
    a = [3,2,1]
    assert median3(a,0,1,2) == a.index(median(a))

def test_median3_third():
    a = [1,3,2]
    assert median3(a,0,1,2) == a.index(median(a))

def test_median_negative():
    a = [-1,-2,-3]
    assert median3(a,0,1,2) == a.index(median(a))

def test_median_mix():
    a = [1,-2,3]
    assert median3(a,0,1,2) == a.index(median(a))


# Partion check
def check_partition(A, p):
    """
    Checks if the partition is correct
    """
    for i in range(len(A)):
        if i < p and not (A[i] <= A[p]):
            return False 
        elif i > p and not (A[p] <= A[i]):
            return False
    return True

## hoareParition tests
def test_hoare_correct():
    a = [1,2,3,4,5]
    e = hoarePartition(a,2) # e is here because the partitioned index has been moved (mabye)
    assert check_partition(a,e)

def test_hoare_1down():
    a = [1,3,2,4,5]
    e = hoarePartition(a,1) 
    assert check_partition(a,e)

def test_hoare_1up():
    a = [1,2,4,3,5]
    e = hoarePartition(a,2) # partition the 4
    assert check_partition(a,e)

def test_hoare_equal():
    a = [1,1,1,1,1,1,1,1,1]
    e = hoarePartition(a,len(a)//2) 
    assert check_partition(a,e)

def test_hoare_even():
    a = [1,2,3,4,5,6,7,8,9,10]
    shuffle(a)
    e = hoarePartition(a,len(a)//2) 
    assert check_partition(a,e)

def test_hoare_odd():
    a = [1,2,3,4,5,6,7,8,9,10,11]
    shuffle(a)
    e = hoarePartition(a,len(a)//2) 
    assert check_partition(a,e)

def test_hoare_random():
    for i in range(100):
        a = [randint(-100,100) for i in range(10)]
        e = hoarePartition(a,randint(0,9))
        assert check_partition(a,e)

## ninther tests
def test_ninther_ordered():
    a = [1,2,3,4,5,6,7,8,9]
    i = ninther(a,0,1,2,3,4,5,6,7,8)
    assert a[4] == 5

def test_ninther_leftshift1():
    a = [2,3,1,5,6,4,8,9,7]
    i = ninther(a,0,1,2,3,4,5,6,7,8)
    assert a[4] == 5

def test_ninther_rightshift1():
    a = [3,1,2,6,4,5,9,7,8]
    i = ninther(a,0,1,2,3,4,5,6,7,8)
    assert a[4] == 5

def test_ninther_shuffledGroups():
    a = [4,5,6,7,8,9,1,2,3] # the groups of three have been moved around here, shouldnt change much
    i = ninther(a,0,1,2,3,4,5,6,7,8)
    assert a[4] == 5