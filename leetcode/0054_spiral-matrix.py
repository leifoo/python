class solution:
    def spiralOrder(self, matrix: [List[int]]) -> List[int]:
        
        result = []

        if not List:
            return result

        direction = [[0, 1], [1, 0], [0, -1], [-1, 0]]
        n_row = len(matrix)
        n_col = len(matrix[0])
        row, col = 0, 0
        total = n_row * n_col
        i_dir = 0


        while row and col:
            result.append(matrix[row][col])

            if row == n_row - 1 or row == 0:
                i_dir = (i_dir + 1) / 4
                n_col -= 1
            if col == n_col - 1 or col == 0:
                i_dir = (i_dir + 1) / 4 
                n_row -= 1

            row += direction[i_dir][0]
            col += direction[i_dir][1]


        return result

if __name__ == "__main__":
    y = solution()
    x = [[1,2,3], [4,5,6], [7,8,9]]
    print("x = ", x, ", y = ", y(x))

