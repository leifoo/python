class solution(object):
    def generateMatrix(self, n):
        
        if n < 1:
            return []

        count, total = 0, n*n

        direction = [[0, 1], [1, 0], [0, -1], [-1, 0]]
        i_dir = 0
        left, right, up, down = 0, n-1, 0, n-1
        row, col = 0, 0
        
        # List comprehension, or * operator
        result = [ [ 0 for i in range(n) ] for j in range(n) ]       
        # result = [ [0 for i in range(n)] * n] 

        while count < total:

            result[row][col] = count + 1
            
            if i_dir == 0 and col == right:
                i_dir += 1
                up += 1
            elif i_dir == 1 and row == down:
                i_dir += 1
                right -= 1
            elif i_dir == 2 and col == left:
                i_dir += 1 
                down -= 1
            elif i_dir == 3 and row == up:
                i_dir += 1
                left += 1

            i_dir = i_dir % 4

            row += direction[i_dir][0]             
            col += direction[i_dir][1]
            count += 1

        return result

if __name__ == "__main__":
    y = solution()
    n = 3
    print('Please type the dimension n of the n*n matrix:')
    try:
        n = int(input())
        print('n = ', n, y.generateMatrix(n))
    except:
        print('Invalid input !')

