# Time complexity O(n^2)
# Space complexity O(1)

def insertion_sort(A):
    
    for j in range(1, len(A)):
        key = A[j]
        
        # Insert A[j] into the sorted sequence A[1], ..., A[j-1]
        i = j - 1
        
        while i >= 0 and A[i] > key:
            A[i+1] = A[i]
            i -= 1
        
        A[i+1] = key

    return A

if __name__ == "__main__":
    x = [2, 5, 1, 3, 4]
    print("Input:  {}".format(x))
    print('Output: {}'.format(insertion_sort(x)))

