import math # This is for floor

# Minimum comparison median https://stackoverflow.com/a/28887340/
def median3(A, a, b, c):
    x = A[a] - A[b]
    y = A[b] - A[c]
    z = A[a] - A[c]
    if(x*y > 0): return b
    if(x*z > 0): return c
    return a

def quickselect(partitionFnc,A,k): 
    """
    Puts kth smallest element of A in A[k] and partitions A around it and returns the kth element. 
    """

    while True:
        p = partitionFnc(A)
    
        if p == k:
            return A[k]
        
        if p > k:
            A = A[0:p]
        
        else:
            k = k - p - 1
            A = A[p + 1: len(A)]


def hoarePartition(A,p):
    """
    Partitions A at A[p'] and returns p' the new position of A[p] passed in
    """

    temp = A[0]
    A[0] = A[p]
    A[p] = temp

    a = 1
    b = len(A) - 1

    while True:
        while a <= b and A[a] < A[0]:
            a += 1

        while A[0] < A[b]:
            b -= 1

        if a >= b:
            break

        temp = A[a]
        A[a] = A[b]
        A[b] = temp
        
        a += 1
        b -= 1

    temp = A[0]
    A[0] = A[a - 1]
    A[a - 1] = temp

    return a - 1



def ninther(A, i1, i2, i3, i4, i5, i6, i7, i8, i9):
    """
    Median of 3 medians, swaps i__ to the middle position
    """
    i1_ = median3(A, i1, i2, i3)
    i2_ = median3(A, i4, i5, i6)
    i3_ = median3(A, i7, i8, i9)

    i__ = median3(A, i1_, i2_, i3_)

    temp = A[i__]
    A[i__] = A[i5]
    A[i5] = temp

    return 

# The next three functions are an almost direct C++ -> Python translation of the functions outlined in the paper https://github.com/andralex/MedianOfNinthers/blob/9fa75b267e74d67b15dbd555311f1ea5f8568e1b/src/common.h#L384

def expandPartitionRight(r, hi, right):
    pivot = 0
    assert(hi > 0)
    assert(right > hi)

    while (pivot < hi):
        if (right == hi):
            temp = r[0]
            r[0] = r[pivot]
            r[pivot] = temp

            return pivot
        
        if (r[right] >= r[0]):
            continue

        pivot += 1

        temp = r[right]
        r[right] = r[pivot]
        r[pivot] = temp

        right -= 1

    while (right > pivot):
        if (r[right] >= r[0]):
            continue

        while (right > pivot):
            pivot += 1

            if (r[0] < r[pivot]):
                temp = r[right]
                r[right] = r[pivot]
                r[pivot] = temp
                break

        right -= 1

    temp = r[0]
    r[0] = r[pivot]
    r[pivot] = temp

    return pivot

def expandPartitionLeft(r, lo, pivot):
    assert (lo > 0 and lo <= pivot)
    left = 0
    oldPivot = pivot

    while(lo < pivot):
        if (left == lo):
            temp = r[oldPivot]
            r[oldPivot] = r[pivot]
            r[pivot] = temp
            
            return pivot

        if (r[oldPivot] >= r[left]):
            continue

        pivot -= 1
        
        temp = r[left]
        r[left] = r[pivot]
        r[pivot] = temp

        left += 1

    while left != pivot:

        if (r[oldPivot] >= r[left]):
            continue

        while True:
            if (left == pivot):
                temp = r[oldPivot]
                r[oldPivot] = r[pivot]
                r[pivot] = temp

                return pivot
            
            pivot -= 1

            if (r[pivot] < r[oldPivot]):
                temp = r[left]
                r[left] = r[pivot]
                r[pivot] = temp
                
                break
            
        left += 1

    temp = r[oldPivot]
    r[oldPivot] = r[pivot]
    r[pivot] = temp

    return pivot

def expandPartition(r, lo, p, hi, length):
    assert(lo <= p and p < hi and hi <= length)

    hi -= 1
    length -= 1

    left = 0

    while True:
        while r[length] <= r[p]:

            if (left == lo):
                return p + expandPartitionRight(r + p, hi - p, length - p)

            left += 1
        
        while r[p] <= r[length]:

            if (left == hi):
                return left + expandPartitionLeft(r + left, lo - left, p - left)

            length -= 1

        temp = r[left]
        r[left] = r[length]
        r[length] = temp

        left += 1
        length -= 1

def medianOfNinthers(A):
    """
    O is the φ expressed in the paper. It's 1/64 for arrays up to 2^17 elements long, and 1/1024 after that, but should be analysed futher 
    Returns p and Partitions A at A[p]
    """
    O = 1//64
    if len(A) > 2 ** 17:
        O = 1//1024

    n = len(A)
    n_ = math.floor((O * n)//3)

    if n_ < 3:
        return hoarePartition(A, len(A)//2)

    g = (n - 3 * n_) // 4
    m = 2 * g + n_
    Am = A[m: m + n_]

    l = g
    r = 3 * g + 2 * n_

    for i in range(n_//3 - 1): # not 100% sure on this line, if errors arrise investigate futher
        ninther(A, l, m, r, l + 1, m + n_//3, r + 1, l + 2, m + 2 * n_//3, r + 2, m, m + n_//3, m + 2 * n_//3)
        m += 1
        l += 3
        r += 3

    quickselect(medianOfNinthers, Am, n_ // 2)
    return expandPartition(A, 2 * g + n_, 2 * g + 1.5 * n_, 2 * (g + n))

    