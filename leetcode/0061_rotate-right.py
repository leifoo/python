class ListNode:
    def __int__(self, x):
        self.val = x
        self.next = None

class Solution:
    def rotateRight(self, head: ListNode, k: int) -> ListNode:

        if not head:
            return 

        cur = head
        size = 1

        while cur.next:
            size += 1
            cur = cur.next

        k = k % size 

        # important
        if k == 0:
        return head

        left = head
        for i in range(size - k - 1):
            left = left.next

        cur.next = head
        head = left.next
        left.next = None

        return head

