from collections import deque

class Solution:
    def floodFill(self, image, sr: int, sc: int, color: int):
        self.dfs(image, sr, sc, color, image[sr][sc])
        return image
                    
    def dfs(self, image, sr, sc, nc, oc):
        if sr < 0 or sr >= len(image) or sc < 0 or sc >= len(image[0]) \
        or image[sr][sc] != oc or image[sr][sc] == nc:
            return
        else:
            image[sr][sc] = nc
            
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            self.dfs(image, sr + dx, sc + dy, nc, oc)
            
    
    
    def floodFill2(self, image, sr: int, sc: int, color: int):
        # BFS
        
        if not image or not image[0]:
            return image
        
        m, n = len(image), len(image[0])
        
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        color_orig = image[sr][sc]
        
        if color_orig == color:
            return image
        
        queue = deque([(sr, sc)])
        
        while queue:
            row, col = queue.popleft()
            image[row][col] = color            
            
            
            for dx, dy in directions:
                x = row + dx
                y = col + dy
                
                if 0<= x < m and 0 <= y < n and image[x][y] == color_orig:
                    queue.append((x, y))
                    
        return image
                

if __name__ == "__main__":
    image = [[1,1,1],[1,1,0],[1,0,1]]
    print("Input:  {}".format(image))

    y = Solution()
    y.floodFill(image, 1, 1, 2)
    print('Output: {}'.format(image))