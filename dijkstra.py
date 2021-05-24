import pygame
import math
import heapq as hq
import sys

WIDTH = 800
WINDOW = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption('Dijkstra Path Finding Algorithm')

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


class Spot():

    def __init__(self, row, col, width, total_rows ):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.width  = width
        self.total_rows = total_rows
        self.neighbors = []
        self.color = WHITE
        self.distance = 999
        self.visited = False

    
    def get_distance(self):
        return self.distance

    def set_distance(self, dist):
        self.distance = dist

    def set_visited(self, visited):
        self.visited = visited

    def make_start(self):
        self.color = TURQUOISE

    def make_end(self):
        self.color = ORANGE
    
    def make_border(self):
        self.color = BLACK
    
    def make_open(self):
        self.color = RED
    
    def make_closed(self):
        self.color = GREEN
    
    def make_path(self):
        self.color = BLUE
    
    def reset(self):
        self.color = WHITE

    def is_start(self):
        return self.color == TURQUOISE
    
    def is_end(self):
        return self.color == ORANGE
    
    def is_border(self):
        return self.color == BLACK
    
    def is_open(self):
        return self.color == RED

    def is_closed(self):
        return self.color == GREEN

    def draw(self, window):   
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.width)) 
    
    def update_neighbors(self, grid):

        if self.row < self.total_rows-1 and not grid[self.row+1][self.col].is_border(): #DOWN
            self.neighbors.append(grid[self.row+1][self.col])

        if self.row > 0 and not grid[self.row-1][self.col].is_border(): #UP
            self.neighbors.append(grid[self.row-1][self.col])

        if self.col < self.total_rows-1 and not grid[self.row][self.col+1].is_border(): #RIGHT
            self.neighbors.append(grid[self.row][self.col+1])

        if self.col > 0 and not grid [self.row][self.col-1].is_border(): #LEFT
            self.neighbors.append(grid[self.row][self.col-1])

def get_clicked_pos(pos, total_rows, width):
    gap = width//total_rows

    row = pos[0] // gap
    col = pos[1] // gap

    return row, col


def make_grid(width, total_rows):
    grid = []
    gap = width // total_rows
    for row in range(total_rows):
        new_row = []
        for col in range(total_rows):
            new_row.append(Spot(row, col, gap, total_rows))
        grid.append(new_row)
    return grid

def draw_grid(window, width, rows):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(window, GREY, (0, i*gap), (width, i*gap ))
    for j in range(rows):
        pygame.draw.line(window, GREY, (j*gap, 0), (j*gap, width))

def draw_all(window, grid, width, total_rows):
    window.fill(WHITE)
    
    for row in grid:
        for spot in row:
            spot.draw(window)

    draw_grid(window, width, total_rows)
    pygame.display.update()

def reconstruct_path(came_from, start, end, draw):
    current = came_from[end]
    while current != start:
        current.make_path()
        current = came_from[current]
        draw()

def algorithm(draw, grid, start, end):
    pq = []
    came_from = {}
    count = 1
    for row in grid:
        for spot in row:
            if spot != start:
                pq.append((spot.get_distance(), count, spot))
                count += 1
            elif spot == start:
                spot.set_distance(0)
                pq.append((spot.get_distance(), 0, spot))

    hq.heapify(pq)

    while len(pq):
        #only thing user can do after algorithm starts is quit, cannot add additional borders, change start, end
        for event in pygame.event.get():   
            if event.type == pygame.QUIT:
                pygame.quit()

        uv = hq.heappop(pq)
        current = uv[2]
        current.set_visited(True)
   
        if current == end:
            break

        # if current != start:
        #     current.make_closed()

        for neighbor in current.neighbors:
            if neighbor.visited:  
                 continue
            # if neighbor.is_closed() or spot.is_start():
            #     continue

            if not (neighbor.is_start() or neighbor.is_end() or neighbor.is_border()):
                neighbor.make_open()

            new_dist = current.get_distance() + 1

            if new_dist < neighbor.get_distance():
                neighbor.set_distance(new_dist)
                came_from[neighbor] = current

        while len(pq):
            hq.heappop(pq)
        count = 0
        for row in grid:
            for spot in row:
                if not (spot.is_closed() or spot.is_start()):
                    pq.append((spot.get_distance(), count, spot))
                    count += 1
        
        if current != start:
            current.make_closed()
        hq.heapify(pq)
        
        draw()
    reconstruct_path(came_from, start, end, draw)

def main(window, width):
    ROWS = 50
    grid = make_grid(width, ROWS)

    start = None
    end = None

    run = True

    while run: 
        draw_all(window, grid, width, ROWS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                if not start and spot != end:
                    spot.make_start()
                    start = spot
                elif not end and spot != start:
                    spot.make_end()
                    end = spot
                else:
                    if spot != end and spot != start:
                        spot.make_border()
            
            if pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                

                if spot.is_start():
                    start = None
                    spot.reset()
                    
                if spot.is_end():
                    end = None
                    spot.reset()

                elif spot.is_border():
                    spot.reset()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)

                    algorithm(lambda: draw_all(window, grid, width, ROWS), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(width, ROWS)
        
    pygame.quit()


main(WINDOW, WIDTH)





            

    


