# 同向双指针
# Time complexity  O(n^2)
# Space complexity O(1)

class Solution():
    def twoSum(self, nums, target):
        start, end = 0, len(nums) - 1
        while start < end:
            s = nums[start] + nums[end]
            if s > target:
                end -= 1
            elif s < target:
                start += 1
            else:
                return (start + 1, end + 1)

    def twoSum2(self, nums, target):

        for i in range(len(nums) - 1):
            value = target - nums[i]
            j = i + 1

            # Have to check index j before compare values
            while j < len(nums) and nums[j] <= value:
                if nums[j] == value:
                    return i, j
                else:
                    j += 1

        return False

if __name__ == "__main__":
    x = [2, 7, 11, 15]
    target = 13
    print("Input:  {}; Target = {}".format(x, target))

    y = Solution()
    print('Output: {}'.format(y.twoSum(x, target)))





