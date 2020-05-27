class solution:
    def getPermutation(self, n: int, k: int) -> str:
        
        mylist = []
        num = [x for x in range(1, n + 1)]
        res = ''

        x = 1
        for i in range(1, n):
            x *= i
            mylist.append(x)

        # mylist.reverse()

        k -= 1 # indexing

        for i in range(n-1, 0, -1):
            index = k // mylist[i-1] 
            k = k % mylist[i-1]
            res = res + str(num[index])
            del num[index]

        res += str(num[0])

        return res


if __name__ == "__main__":
    y = solution()
    

    n, k = list(map(int, input('Please type the number n and position k:').split()))
    print(n, k, y.getPermutation(n, k))

"""
    try:
        n, k = list(map(int, input('Please type the number n and position k:').split()))
        print(n, k, y.getPermutation(n, k))
    except:
        pass #print('Invalid input!')
"""
