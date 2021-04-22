# 同向双指针
# Time complexity  O(n)
# Space complexity O(1)

class Solution:
    """
    @param A: a list of integers
    @return an integer
    """
    def removeDuplicates(self, A):
        # write your code here
        if not A:
            return 0

        index = 0
        for i in range(1, len(A)):
            if A[index] != A[i]:
                index += 1
                A[index] = A[i]

        return index + 1

if __name__ == "__main__":
    x = [1, 2, 2, 3, 4, 5]
    print("Input:  {}".format(x))

    y = Solution()
    new_len = y.removeDuplicates(x)
    print('Output: {}'.format(x[:new_len]))
    print('new_len = {}'.format(new_len))