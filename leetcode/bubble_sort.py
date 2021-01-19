# Time complexity O(n^2)
# Space complexity O(1)

def bubble_sort(A):
    
    for i in range(len(A) - 1):
        for j in range(len(A) - 1 - i):
            if A[j] > A[j+1]:
                A[j], A[j+1] = A[j+1], A[j]

if __name__ == "__main__":
    x = [2, 5, 1, 3, 4]
    print("Input:  {}".format(x))
    bubble_sort(x)
    print('Output: {}'.format(x))

