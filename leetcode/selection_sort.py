# Time complexity O(n^2)
# Space complexity O(1)

def selection_sort(A):
    
    for i in range(len(A)):
        min_idx = i 

        for j in range(i+1, len(A)):
            if A[min_idx] > A[j]:
                min_idx = j

        A[min_idx], A[i] = A[i], A[min_idx]

if __name__ == "__main__":
    x = [2, 5, 1, 3, 4]
    print("Input:  {}".format(x))
    selection_sort(x)
    print('Output: {}'.format(x))

