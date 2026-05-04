import pygame
import sys 
import random

CELL_SIZE = 40
MARGIN = 40 #padding around the maze



WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0,   0)
BLUE  = (0,   0,   255)
GREEN = (0,   200, 0)

#coordinate helper function

def cell_to_pixel(row, col, rows):
    x = MARGIN + col * CELL_SIZE
    y = MARGIN + (rows-1-row) * CELL_SIZE # to flip y-axis since row 0 is our bottom row
    return x, y


def initialize_maze(rows,cols):
    north_wall = [[True]* cols for _ in range(rows+1)]
    east_wall =  [[True]* (cols+1) for _ in range(rows)]
    return north_wall, east_wall
def set_visited(rows,cols):
    visited = [[False]* cols for _ in range(rows)]
    return visited


def draw_maze(screen, north_wall,east_wall, rows, cols):
    screen.fill(WHITE)

    for row in range(rows):
        for col in range(cols):
            x,y = cell_to_pixel(row,col,rows)

            #draw north wall of the cell
            if north_wall[row+1][col]:
                pygame.draw.line(screen, BLACK, (x,y), (x+CELL_SIZE,y), 2)

            #draw east wall of the cell
            if east_wall[row][col+1]:
                pygame.draw.line(screen, BLACK, (x+CELL_SIZE,y), (x+CELL_SIZE,y+CELL_SIZE), 2)

            
            #draw the left border
            if east_wall[row][0]:
                pygame.draw.line(screen, BLACK, (x,y), (x,y+CELL_SIZE), 2)
    
    for col in range(cols):
        x,y = cell_to_pixel(0,col,rows)
        #draw the bottom border
        if north_wall[0][col]:
            
            pygame.draw.line(screen, BLACK, (x,y+CELL_SIZE), (x+CELL_SIZE,y+CELL_SIZE), 2)
    pygame.display.flip()



#maze generation

#getting unvisited neighbors of a cell
def get_unvisited_neighbors(row,col,visited, rows,cols):
    neighbors = []

    if row +1 < rows and not visited[row+1][col]:
        neighbors.append((row+1, col, 'N'))
    if row -1 >= 0 and not visited[row-1][col]:
        neighbors.append((row-1, col, 'S'))
    if col +1 < cols and not visited[row][col+1]:
        neighbors.append((row, col+1, 'E'))
    if col -1 >= 0 and not visited[row][col-1]:
        neighbors.append((row, col-1, 'W'))
    return neighbors

#remove wall

def remove_wall(row, col, direction, north_wall, east_wall):
    if direction == 'N':
        north_wall[row+1][col] = False
    elif direction == 'E':
        east_wall[row][col+1] = False   
    elif direction == 'S':
        north_wall[row][col] = False
    elif direction == 'W':
        east_wall[row][col] = False

def generate_maze( north_wall, east_wall, visited, rows, cols,screen=None,clock=None, animate=False,):
    #picking random start

    start_row = random.randint(0, rows-1)
    start_col = random.randint(0, cols-1)
    
    visited[start_row][start_col] = True
    stack = [(start_row, start_col)]
    current = (start_row,start_col)

    while stack:
        row,col = current
        neighbors = get_unvisited_neighbors(row,col,visited,rows,cols)

        if neighbors:
            chosen_neighbor = random.choice(neighbors)

            remove_wall(row, col, chosen_neighbor[2], north_wall, east_wall)
            visited[chosen_neighbor[0]][chosen_neighbor[1]] = True
            stack.append((chosen_neighbor[0], chosen_neighbor[1]))
            current = (chosen_neighbor[0], chosen_neighbor[1])

            if animate and screen:
                draw_maze(screen, north_wall, east_wall, rows, cols)
                pygame.time.delay(30)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
        else:
            #backtrack - dead end reached
            current = stack.pop()



def main():
    pygame.init()

    ROWS = int(input("Enter number of rows: "))
    COLS = int(input("Enter number of columns: "))
    WIDTH = COLS * CELL_SIZE + 2 * MARGIN
    HEIGHT = ROWS * CELL_SIZE + 2 * MARGIN
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Maze Visualization")

    north_wall, east_wall = initialize_maze(ROWS, COLS)
    visited = set_visited(ROWS, COLS)

    draw_maze(screen, north_wall, east_wall, ROWS, COLS)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()

if __name__ == "__main__":
    
    main()

