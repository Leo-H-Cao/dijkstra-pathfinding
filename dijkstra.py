import pygame
import math
import heapq as hq
import sys

WIDTH = 800
WINDOW = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption('Dijkstra Path Finding Algorithm')

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
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
        self.width  = width
        self.total_rows = total_rows
        self.neighbors = []
        self.color = WHITE
        self.distance = sys.maxint

    def get_pos(self):
        return self.row, self.col
    
    def get_distance(self):
        return self.distance

    def set_distance(self, dist):
        self.disance = dist
    
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

    def is_start(self):
        return self.color == TURQUOISE
    
    def is_end(self):
        return self.color == ORANGE
    
    def is_border(self):
        return self.color == BLACK
    
    def is_open(self):
        return self.color == GREEN

    def is_closed(self):
        return self.color == RED

    def draw(self, window):   
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.width)) 
    
    def update_neighbors(self, grid):

        if self.row < self.total_rows-1 and not grid[self.row+1][self.col].is_barrier(): #DOWN
            self.neighbors.append(grid[self.row+1][self.col])

        if self.row > 0 and not grid[self.row-1][self.col].is_barrier(): #UP
            self.neighbors.append(grid[self.row-1][self.col])

        if self.col < self.total_rows-1 and not grid[self.row][self.col+1].is_barrier(): #RIGHT
            self.neighbors.append(grid[self.row][self.col+1])

        if self.col > 0 and not grid [self.row][self.col-1].is_barrier(): #LEFT
            self.neighbors.append(grid[self.row][self.col-1])


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
    
    for row in range(total_rows):
        for spot in grid[row]:
            spot.draw(window)

    draw_grid(window, width, total_rows)
    pygame.display.update()

def algorithm(draw, grid, start, end):
    pq = []
    came_from = {}
    for row in grid:
        for spot in row:
            spot.update_neighbors(grid)
            if spot != start:
                pq.append((spot.get_distance(), spot))
            elif spot == start:
                spot.set_distance(0)
                pq.append(spot.get_distance(), spot)

    hq.heapify(pq)

    while len(pq):
        uv = hq.heappop(hq)
        current = uv[1]
        current.make_closed()
        for neighbor in current.neighbors:
            if neighbor.is_closed():
                continue
            if not (neighbor.is_start() or neighbor.is_end() or neighbor.is_border()):
                neighbor.make_open()

            new_dist = current.get_distance() + 1

            if new_dist < neighbor.get_distance():
                neighbor.set_distance(new_dist)
                came_from[neighbor] = current

        while len(pq):
            hq.heappop(pq)
        pq = [(spot.get_distance(), spot) for row in grid for spot in row if not spot.is_closed()]
        hq.heapify(pq)

def main(window, width):
    total_rows = 50
    grid = make_grid(width, total_rows)
            





            

    


