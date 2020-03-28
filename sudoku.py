#sudoku solver program
import numpy as np

grid = [[0,0,0,2,6,0,7,0,1],[6,8,0,0,7,0,0,9,0],[1,9,0,0,0,4,5,0,0],
       [8,2,0,1,0,0,0,4,0],[0,0,4,6,0,2,9,0,0],[0,5,0,0,0,3,0,2,8],
       [0,0,9,3,0,0,0,7,4],[0,4,0,0,5,0,0,3,6],[7,0,3,0,1,8,0,0,0]]

# grid = np.matrix(grid)

# print(grid)

# to check if a number can be inserted in a particular position 
def possible(y,x,n):
    global grid 
    for i in range(9):
        if grid[y][i] == n:
            return False
    for i in range(9):
        if grid[i][x] == n:
            return False
    # to check a number is already there in a particular square 
    x0 = (x//3)*3
    y0 = (y//3)*3
    for i in range(3):
        for j in range(3):
            if grid[y0+i][x0+j] == n:
                return False
    return True 

def solve():
    global grid 
    for y in range(9):
        for x in range(9):
            if grid[y][x] == 0:
                for n in range(1,10):
                    if(possible(y,x,n)):
                        grid[y][x] = n
                        solve()
                        grid[y][x] = 0 
                return 
    print(np.matrix(grid))
    input("More? ")

solve()