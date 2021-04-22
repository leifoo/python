# Time complexity O(n)
# Space complexity O(n)

# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution:
    def maxPathSum(self, root: TreeNode) -> int:
        
        self.ans = -sys.maxsize
        self.helper(root)
        return self.ans
    
    def helper(self, node):
        if not node:
            return -sys.maxsize
        
        l = max(0, self.helper(node.left))
        r = max(0, self.helper(node.right))
        
        self.ans = max(self.ans, node.val + l + r)
        
        return node.val + max(l, r)
