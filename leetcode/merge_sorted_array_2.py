# Time complexity O(n)
# Space complexity O(n)

def merge_sorted_array_2(A, B):
    
    new_list = []
    i, j = 0, 0

    while i < len(A) and j < len(B):
        if A[i] <= B[j]:
            new_list.append(A[i])
            i += 1
        else:
            new_list.append(B[j])
            j += 1

    while i < len(A):
        new_list.append(A[i])
        i += 1

    while j < len(B):
        new_list.append(B[j])
        j += 1

    return new_list

if __name__ == "__main__":
    A = [1, 3, 4]
    B = [2, 5]
    print("Input: \n  A = {}  \n  B = {}".format(A, B))
    C = merge_sorted_array_2(A, B)
    print('Output: {}'.format(C))

