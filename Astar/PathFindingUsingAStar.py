import pygame
from queue import PriorityQueue

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))  # display size
pygame.display.set_caption("A* PathFinding Algorithm")  # title

# color codes
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    # get position func
    def get_pos(self):
        return self.row, self.col

    # check if the node is visited
    def is_closed(self):
        return self.color == RED

    # to see if the node is in the open set list
    def is_open(self):
        return self.color == GREEN

    # to see if the node is a barrier node
    def is_barrier(self):
        return self.color == BLACK

    # if the node is the start node
    def is_start(self):
        return self.color == ORANGE

    # if the node is the end node
    def is_end(self):
        return self.color == TURQUOISE

    # turn all the node to white default
    def reset(self):
        self.color = WHITE

    # make the node closed or visited
    def make_closed(self):
        self.color = RED

    # make the node in the open set
    def make_open(self):
        self.color = GREEN

    # makes the node a barrier
    def make_barrier(self):
        self.color = BLACK

    def make_start(self):
        self.color = ORANGE

    # makes the node an end node
    def make_end(self):
        self.color = TURQUOISE

    # makes the node the pathway from start to end
    def make_path(self):
        self.color = BLUE

    # makes the square in the window
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    # checks up down left and right of the node i.e. its neighbors
    def update_neighbors(self, grid):
        self.neighbors = []

        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():    # [self.row + 1] -> going down
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():    # [self.row - 1] -> going up
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():    # [self.col + 1] -> going right
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():    # [self.col - 1] -> going left
            self.neighbors.append(grid[self.row][self.col - 1])


    def __lt__(self, other):
        return False




# heuristic function
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

# function to draw the path from start to end after finding the shortest distance
def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

# A-star algorithm
def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))   # (0, count, start) -> (f-score, no. of same f-score neighbor, start-node)
    came_from = {}    # to keep the track from where the last node came from
    g_score = {node: float("inf") for row in grid for node in row}    # adds infinity in g_score of all node
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}  # adds infinity in f_score of all node
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}   # to check if a node is in the priority-queue

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]    # [2] -> indexing 2 because we want to get the node from (f-score, no.of same f-score neighbor, node)
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True    # found the path to the end

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:     # if g_score of current neighbor is less than the other neighbor
                came_from[neighbor] = current        # change the path to the current neighbor
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False       # couldn't find the path to the end


# function making the grid area
def make_grid(rows, width):
    grid = []
    gap = width // rows

    for i in range(rows):    # rows
        grid.append([])
        for j in range(rows):     # columns
            node = Node(i, j, gap, rows)
            grid[i].append(node)

    return grid

# makes the grey grid lines
def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


# actual drawing function
def draw(win, grid, rows, width):
    win.fill(WHITE)
    # making nodes in every row in the grid
    for row in grid:
        for node in row:
            node.draw(win)
    # drawing the grid line after adding nodes in rows
    draw_grid(win, rows, width)
    pygame.display.update()

# helper function to get the mouse pointer position on the grid
def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col

# main loop
def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    start = None
    end = None

    run = True

    while run:
        draw(win, grid, ROWS, width)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # making start, end and barriers
            if pygame.mouse.get_pressed()[0]:                   # 0 -> left mouse button
                pos = pygame.mouse.get_pos()                    # gives the mouse-pointer pos on the pygame window
                row, col = get_clicked_pos(pos, ROWS, width)    # helper function to get the row and col pos of grid
                node = grid[row][col]                           # getting the node using the row and col

                if not start and node != end:
                    start = node
                    start.make_start()

                elif not end and node != start:
                    end = node
                    end.make_end()

                elif node != end and node != start:
                    node.make_barrier()

            # removing start, end or barriers
            elif pygame.mouse.get_pressed()[2]:                 # 2 -> right mouse button
                pos = pygame.mouse.get_pos()  # gives the mouse-pointer pos on the pygame window
                row, col = get_clicked_pos(pos, ROWS, width)  # helper function to get the row and col pos of grid
                node = grid[row][col]  # getting the node using the row and col
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None

            # pressing space to start the algorithm
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    # calling the Astar algorithm on the grid with start and end node
                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

                # pressing c to clear everything
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)


    pygame.quit()


main(WIN, WIDTH)
