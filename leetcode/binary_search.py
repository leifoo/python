# Time complexity O(logn)
# Space complexity O(1)

# return the index of the first target value
def binary_search(nums, target):

    if not nums:
        return -1
    
    start, end = 0, len(nums)

    while start + 1 < end:
        mid = (start + end) // 2

        if nums[mid] < target:
            start = mid
        elif nums[mid] == target:
            end = mid
        else:
            end = mid
        
    if nums[start] == target:
        return start
    if nums[end] == target:
        return end

    return -1

if __name__ == "__main__":
    x = [1, 2, 2, 4, 5, 6]
    print("Input:  {}".format(x))
    target = 2
    print('target = {}, index: {}'.format(target, binary_search(x, target)))
    target = 3
    print('target = {}, index: {}'.format(target, binary_search(x, target)))

