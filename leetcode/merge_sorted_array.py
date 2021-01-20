# Time complexity O(n)
# Space complexity O(1)

def merge_sorted_array(A, m, B, n):
    
    pos = m + n - 1
    i, j = m - 1, n - 1

    while i >= 0  and j >= 0:
        if A[i] >= B[j]:
            A[pos] = A[i]
            pos -= 1
            i -= 1
        else:
            A[pos] = B[j]
            pos -= 1
            j -= 1

    if j >= 0:
        A[pos] = B[j]
        pos -= 1
        j -= 1

if __name__ == "__main__":
    A = [1, 3, 4, None, None, None]
    B = [2, 5]
    m, n = len([x for x in A if x is not None]), len(B)
    print("Input: \n  A = {}, m = {}  \n  B = {}, n = {}".format(A, m, B, n))
    merge_sorted_array(A, m, B, n)
    print('Output: {}'.format(A))

