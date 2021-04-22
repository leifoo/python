# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:

     # 概念是當使用inorder traversal時 出現的數字在BST一定會由小而大排序 錯誤的兩點一定會發生在: 
     # 1. 第一次遇到previous value > current value的時候的previous node 
     # 2. 第二次遇到previous value > current value的時候的current node 
     # 所以如果有找到這兩點的時候 把兩點的數值交換即可~
     
     # Time: O(N)
     # Space: O(1)

    def recoverTree(self, root):
        if root is None:
            return None
        self.pre = None
        self.first = None
        self.second = None
        
        self.inOrder(root)
        # Swap
        if self.first != None:
            self.first.val, self.second.val = self.second.val, self.first.val
        
        return root
        
    def inOrder(self, root):
        if root is None:
            return
        self.inOrder(root.left)
        if self.pre != None:
            if self.first == None and self.pre.val > root.val:
                self.first = self.pre
                self.second = root
            elif self.first != None and self.pre.val > root.val:
                self.second = root
        self.pre = root
        self.inOrder(root.right)


    def recoverTree2(self, root: TreeNode) -> None:
        """
        Do not return anything, modify root in-place instead.
        """
    
        # inorder遍历取到数组里，对数组排序之后按顺序将排序后的值赋回给节点。
        # sort() function is very similar to sorted() but unlike sorted it returns nothing 
        # and makes changes to the original sequence.
        
        list_val, list_node = [], []
        self.inorder(root, list_val, list_node)
        list_val.sort()
        for i, node in enumerate(list_node):
            node.val = list_val[i]
        
    
    def inorder(self, node, list_val, list_node):
        if not node:
            return
        
        self.inorder(node.left, list_val, list_node)
        list_val.append(node.val)
        list_node.append(node)
        self.inorder(node.right, list_val, list_node)


   