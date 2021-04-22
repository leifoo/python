# Time complexity O(nlogn)
# Space complexity O(1)


class Solution:
    # @param {int[]} A an integer array
    # @return nothing
    def sortIntegers2(self, A):
        # Write your code here
        self.quickSort(A, 0, len(A) - 1)
    
    def quickSort(self, A, start, end):
        if start >= end:
            return
        
        left, right = start, end
        # key point 1: pivot is the value, not the index
        pivot = A[(start + end) // 2];

        # key point 2: every time you compare left & right, it should be 
        # left <= right not left < right
        while left <= right:
            while left <= right and A[left] < pivot:
                left += 1
            
            while left <= right and A[right] > pivot:
                right -= 1
            
            if left <= right:
                A[left], A[right] = A[right], A[left]
                
                left += 1
                right -= 1
        
        self.quickSort(A, start, right)
        self.quickSort(A, left, end)

if __name__ == "__main__":
    x = [2, 5, 1, 3, 4]
    print("Input:  {}".format(x))
    
    y = Solution()
    y.sortIntegers2(x)
    print('Output: {}'.format(x))

