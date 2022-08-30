# A new attempt a full C++ to Python translation of the algorithm.
# Most of this is not very nice to read and very dense, but attempts to be as close to the C++ as possible.
# Transcription notes:
#    - goto commands are replicated by repeating the code after the goto
#    - most pointer magic is removed, and replaced with simple index tracking, or ocasional reassignment
#    - there are extra adjustments to array indexes like `mid` and `pivot` since in C++ they are "absolute", while in Python they are relative to the array start
# TODO:
#    - restructure code flow to avoid copy pasted code implementing the goto commands

def sort3(r: list, a: int, b:int, c:int): 
    if (r[b] < r[a]):
        if (r[c] < r[b]):
            r[a], r[c] = r[c], r[a]
        else:
            t = r[a]
            r[a] = r[b]
            if (r[c] < t):
                r[b] = r[c]
                r[c] = t
            else:
                r[b] = t
    elif (r[c] < r[b]):
        t = r[c]
        r[c] = r[b]
        if (t < r[a]):
            r[b] = r[a]
            r[a] = t
        else:
            r[b] = t

    assert (r[a] <= r[b] and r[b] <= r[c])

def partition4(r: list, a: int, b: int, c: int, d: int):
    assert (a != b and a != c and a != d and b != c and b != d and c != d)
    # We are just going to lean left
    if (r[c] < r[a]):
        r[a], r[c] = r[c], r[a]
    
    if (r[d] < r[b]):
        r[b], r[d] = r[d], r[b]

    if (r[d] < r[c]):
        r[c], r[d] = r[d], r[c]
        r[a], r[b] = r[b], r[a]

    if (r[c] < r[b]):
        r[b], r[c] = r[c], r[b]

    assert(r[a] <= r[c] and r[b] <= r[c] and r[c] <= r[d])

def partition5(r: list, a: int, b: int, c: int, d: int, e: int):
    assert(a != b and a != c and a != d and a != e and b != c and b != d and b != e and c != d and c != e and d != e)

    if (r[c] < r[a]):
        r[a], r[c] = r[c], r[a]

    if (r[d] < r[b]):
        r[b], r[d] = r[d], r[b]

    if (r[d] < r[c]):
        r[c], r[d] = r[d], r[c]
        r[a], r[b] = r[b], r[a]

    if (r[e] < r[b]):
        r[b], r[e] = r[e], r[b]
    
    if (r[e] < r[c]):
        r[c], r[e] = r[e], r[c]
        if (r[c] < r[a]):
            r[a], r[c] = r[c], r[a]

    else:
        if (r[c] < r[b]):
            r[b], r[c] = r[c], r[b]

    assert(r[a] <= r[c] and r[b] <= r[c] and r[c] <= r[d] and r[c] <= r[e])

def hoarePartition(r: list, p: int):
    length = len(r)
    assert(p < length) # be sure that p dosent fall out of the array
    r[0], r[p] = r[p], r[0]
    lo = 1
    hi = length - 1
    while True:
        while True:
            if (lo > hi):
                # goto command
                lo -= 1
                r[lo], r[0] = r[0], r[lo]
                return lo # return the index of the pivot plus 0
            
            if (r[lo] >= r[0]):
                break
            
            lo += 1
        
        assert(lo <= hi)

        while r[0] < r[hi]:
            hi -= 1

        if (lo >= hi):
            break

        assert(r[lo] >= r[hi])
        r[lo], r[hi] = r[hi], r[lo]

        lo += 1
        hi -= 1
    
    lo -= 1
    r[lo], r[0] = r[0], r[lo]
    return lo # technically different to what the cpp version returns, it's actions are replicated back in quickselect

def quickselect(partitionalgo, r: list, mid: int, end: int):
    if (0 == end or mid >= end): # 0 here to replicate the original refference to the array start
        return
    assert(0 <= mid and mid < end)
    
    while True:
        match (end): # - r removed since it's redundant because it's 0 in Python  
            case 1:
                return 
            case 2:
                if (r[0] > r[1]):
                    r[0], r[1] = r[1], r[0]
                return
            case 3:
                sort3(r, 0, 1, 2)
                return
            case 4:
                match (mid): # - r removed since it's redundant because it's 0 in Python    
                    case 0: # goto command
                        # select_min
                        pivotIndex = 0 # insted of pointer magic, we will keep track of an index

                        mid += 1
                        while (mid < end):
                            if (r[mid] < r[pivotIndex]): 
                                pivotIndex = mid 
                            mid += 1

                        r[0], r[pivotIndex] = r[pivotIndex], r[0]
                        return
                    case 1:
                        partition4(r, 0, 1, 2, 3)
                        return # breaks replaced with return that would be reached by breaking
                    case 2:
                        partition4(r, 0, 1, 2, 3)
                        return
                    case 3: #goto command
                        # select_max
                        pivotIndex = 0

                        mid = 1
                        while (mid < end):
                            if (r[pivotIndex] < r[mid]):
                                pivotIndex = mid
                            mid += 1

                        r[0], r[end - 1] = r[pivotIndex], r[0]
                        return

                    case _: # default
                        assert(False)

                # there would be a return here but it's inacessible
            
            case _: # default  

                assert(end > 4) # - r removed since it's redundant because it's 0 in Python
                if (0 == mid):
                    # select_min
                    pivotIndex = 0 # insted of pointer magic, we will keep track of an index
                    mid += 1
                    while (mid < end):
                        if (r[mid] < r[pivotIndex]): 
                            pivotIndex = mid 
                        mid += 1

                    r[0], r[pivotIndex] = r[pivotIndex], r[0]
                    return
                if (mid + 1 == end):
                    # select_max
                    pivotIndex = 0

                    mid = 1
                    while (mid < end):
                        if (r[pivotIndex] < r[mid]):
                            pivotIndex = mid
                        mid += 1

                    r[0], r[end - 1] = r[pivotIndex], r[0]
                    return

                pivot  = partitionalgo(r, end)
                if (pivot == mid):
                    return
                
                if (pivot > mid):
                    end = pivot
                else:
                    r = r[pivot + 1:] # Should be correct, dosn't backwards propagate the pointer magic
                    mid -= pivot + 1 # Replicate the absoluteness of C++
                    end -= pivot + 1 