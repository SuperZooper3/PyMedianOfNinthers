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

    while True: # TODO: SKIP HAVING TO DO A DOUBLE BREAK
        breakFlag = False # roundabout way of double breaking, like described in the paper

        while True:
            if a > b:
                breakFlag = True
                break
            if A[a] >= A[0]:
                break
            a += 1

        if breakFlag: break

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

    return i__

# The next three functions are an almost direct C++ -> Python translation of the functions outlined in the paper https://github.com/andralex/MedianOfNinthers/blob/9fa75b267e74d67b15dbd555311f1ea5f8568e1b/src/common.h#L384
## TODO: DEBUG, NOT WORKING CORRECTLY, PROBABLY A MISSINTERPRETATION OF THE PAPER
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
            right -= 1 # right here to repliacte the --rite in the C# code
            continue

        pivot += 1

        temp = r[right]
        r[right] = r[pivot]
        r[pivot] = temp

        right -= 1


    while (right > pivot):
        if (r[right] >= r[0]):
            right -= 1
            continue

        while (right > pivot):
            pivot += 1

            if (r[0] < r[pivot]):
                temp = r[right]
                r[right] = r[pivot]
                r[pivot] = temp
                break

        right -= 1

    # done
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
            left += 1
            continue

        pivot -= 1
        
        temp = r[left]
        r[left] = r[pivot]
        r[pivot] = temp

        left += 1

    while True:

        if (left == pivot): # This should be able to be removed, but trying to stay as close to C++ version as possible
            break

        if (r[oldPivot] >= r[left]):
            left += 1
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

    # done

    temp = r[oldPivot]
    r[oldPivot] = r[pivot]
    r[pivot] = temp

    return pivot

def expandPartition(partitionList, lo, pivot, hi, length):
    """
    Partition r[lo..hi] around pivot r[p]
    """
    assert(lo <= pivot and pivot < hi and hi <= length) # Precondition, they must fall inside bounds

    hi -= 1 # The pivot is smaller than high so we can skip the first step
    length -= 1 # Same for the length

    left = 0 

    while True:
        while True:
            if (left == lo):
                return pivot + expandPartitionRight(partitionList[pivot:], hi - pivot, length - pivot) # stumped on what this line is supposed to be
                # r + pivot is being translated to python with [pivot:]

            if (partitionList[length] > partitionList[pivot]):
                break

            left += 1
        
        while True:
            if (left == hi):
                return left + expandPartitionLeft(partitionList[left:], lo - left, pivot - left)

            if (partitionList[pivot] >= partitionList[length]):
                break

            length -= 1

        temp = partitionList[left]
        partitionList[left] = partitionList[length]
        partitionList[length] = temp

        left += 1
        length -= 1

def medianOfNinthers(A):
    """
    Returns p and Partitions A at A[p]
    """
    O = 1//64 # O is the φ expressed in the paper. It's 1/64 for arrays up to 2^17 elements long, and 1/1024 after that, but should be analysed futher for performance
    if len(A) > 2 ** 17:
        O = 1//1024

    n = len(A)
    n_ = (O * n)//3

    if n_ < 3:
        return hoarePartition(A, len(A)//2)

    # These variables are all defined in the paper, but make almost no sense. Completly different from what apears in the GH source code
    g = (n - 3 * n_) // 4
    m = 2 * g + n_
    Am = A[m: m + n_]

    l = g
    r = 3 * g + 2 * n_

    for i in range(n_//3 - 1): # TODO: not 100% sure on this line, if errors arrise investigate futher
        ninther(A, l, m, r, l + 1, m + n_//3, r + 1, l + 2, m + (2 * n_)//3, r + 2, m, m + (n_//3), m + (2 * n_)//3)
        m += 1
        l += 3
        r += 3

    quickselect(medianOfNinthers, Am, n_ // 2)
    return expandPartition(A, m, 2 * g + n_ + n_//2, m + n)

    