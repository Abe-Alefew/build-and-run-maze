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
            pygame.draw.line(screen, BLACK, (MARGIN,y), (MARGIN,y+CELL_SIZE), 2)
    
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
            stack.append(current)
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

def create_entrance_exit(rows,cols,north_wall,east_wall):
    # as entrance, let's open a random-cell's west wall on left edge
    entrance_row = random.randint(0, rows-1)
    east_wall[entrance_row][0] = False

    #as exit, let's open a random-cell's east wall on right edge
    exit_row = random.randint(0, rows-1)
    east_wall[exit_row][cols] = False

    return entrance_row, exit_row


#Maze -solving with DFS backtracking

#finding entrance and exit cells

def find_entrance_exit(rows,cols,east_wall):
    entrance = None
    exit_cell = None
    for row in range(rows):
        if not east_wall[row][0]:
            entrance = (row, 0)
        if not east_wall[row][cols]:
            exit_cell = (row, cols-1)
    return entrance, exit_cell

#checking if we can move in a direction from current cell
def can_move(row, col, direction, north_wall, east_wall, rows, cols):
    if direction == 'N':
        if row+ 1 < rows and not north_wall[row+1][col]:
            return True
    elif direction == 'E':
        if col+ 1 < cols and not east_wall[row][col+1]:
            return True
    elif direction == 'S':
        if row- 1 >= 0 and not north_wall[row][col]:
            return True
    elif direction == 'W':
        if col- 1 >= 0 and not east_wall[row][col]:
            return True
    return False

#checking reachable neighbors for maze solving
def get_reachable_neighbors(row, col, north_wall, east_wall, rows, cols, visited_solver):
    neighbors = []
    for direction in ['N', 'E', 'S', 'W']:
        if can_move(row, col, direction, north_wall, east_wall, rows, cols):
            #get neighbor coordinates based on direction
            dr = { 'N':1, 'E':0, 'S':-1, 'W':0}
            dc = { 'N':0, 'E':1, 'S':0, 'W':-1}
            if not visited_solver[row + dr[direction]][col + dc[direction]]:
                neighbors.append((row + dr[direction], col + dc[direction], direction))
    return neighbors

#solving the maze with DFS backtracking
def solve_maze(rows,cols,north_wall, east_wall,screen, animate=False):

    entrance,exit_cell = find_entrance_exit(rows,cols,east_wall)

    if not entrance or not exit_cell:
        print("Entrance or exit not found")
        return [], []

    visited_solver = set_visited(rows,cols)
    stack = []
    dead_ends = set()

    current = entrance
    visited_solver[current[0]][current[1]] = True

    while current != exit_cell:
        neighbors = get_reachable_neighbors(current[0], current[1], north_wall, east_wall, rows, cols, visited_solver)
        if neighbors:
            next_cell = neighbors[0]
            stack.append(current)
            visited_solver[next_cell[0]][next_cell[1]] = True
            current = (next_cell[0], next_cell[1])
        else:
            dead_ends.add(current)
            current = stack.pop()
        
        if animate and screen:
            draw_maze(screen,north_wall,east_wall, rows,cols,path=stack,dead_ends=dead_ends,current=current)
            pygame.time.delay(50)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
    return stack, dead_ends

def main():
    pygame.init()

    ROWS = int(input("Enter number of rows: "))
    COLS = int(input("Enter number of columns: "))
    WIDTH = COLS * CELL_SIZE + 2 * MARGIN
    HEIGHT = ROWS * CELL_SIZE + 2 * MARGIN
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Maze Visualization")
    clock= pygame.time.Clock()

    north_wall, east_wall = initialize_maze(ROWS, COLS)
    visited = set_visited(ROWS, COLS)

    #generate maze with animation
    generate_maze(north_wall, east_wall, visited, ROWS, COLS, screen=screen, animate=True,clock=clock)
    
    # unvisited = sum(1 for i in range(ROWS) for j in range(COLS) if not visited[i][j])
    # print(f"Unvisited cells: {unvisited}")  # Must be 0
    create_entrance_exit(ROWS, COLS, north_wall, east_wall)

    draw_maze(screen, north_wall, east_wall, ROWS, COLS)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()

if __name__ == "__main__":
    
    main()

