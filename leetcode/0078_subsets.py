class Solution:
    def subsets(self, nums):

        if not nums:
            return

        n = len(nums)
        result = []

        def helper(j, temp):
            # print(j, type(temp), type(temp[:]), temp, temp[:], len(temp), k)
            if len(temp) == k:
                result.append(temp[:])

            for i in range(j, n):
                temp.append(nums[i])
                helper(i + 1, temp)
                temp.pop()

        for k in range(n+1):
            helper(0, [])

        return result

if __name__ == "__main__": 
    y = Solution()
    x = [1, 2, 3]
    print("subsets(", x, ') = ', y.subsets(x))