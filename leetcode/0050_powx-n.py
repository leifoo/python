class Solution:
    def myPow(self, x: float, n: int) -> float:

        # bitewise operators

        if n < 0:
            n = -n
            x = 1 / x

        ans = 1

        while n:
            if n & 1:
                ans *= x
            x *= x
            n >>= 1
    
        return ans

if __name__ == "__main__": 
    y = Solution()
    print("myPow(", 2.0, ', ', -3, ') = ', y.myPow(2.0, -3))
