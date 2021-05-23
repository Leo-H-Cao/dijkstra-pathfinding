import pygame
import math

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
        self.x = row*width
        self.y = col*width
        self.neighbors = []
        self.color = WHITE

    def get_pos(self):
        return self.row, self.col
    
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
        return self.color == RED

    def is_closed(self):
        return self.color == GREEN

    def draw(self, window):   
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.width)) 

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
            
grid = make_grid(WIDTH, 50)
while True: 
    draw_all(WINDOW, grid, WIDTH, 50)

    


