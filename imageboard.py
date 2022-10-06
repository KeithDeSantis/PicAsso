from audioop import findfactor
from email.mime import image
from functools import reduce, total_ordering
from turtle import pensize
import random
import math
import numpy as np
import copy

NEIGHBORING_DIRECTIONS = [
    (-1,-1), # Up Left 
    (-1,0), # Up 
    (-1,1), # Up Right
    (0,-1), # Left
    (0,1), # Right
    (1,-1), # Down Left
    (1,0), # Down
    (1,1) # Down Right
    ]

''' Find the squarest factors of a number, to determine the shape of the matrix '''
def find_shape(number):
    factors = []
    for i in range(1, math.ceil((number**(0.5)))):
       if number % i == 0:
           factors.append((i, (number/i)))
    shape = factors[0]
    squareness = abs(shape[0] - shape[1])
    for f in factors:
        if abs(f[0]-f[1]) < squareness:
            shape = (int(f[0]), int(f[1]))
            squareness = abs(f[0]-f[1])
    return shape

# FITNESS FUNCTIONS ----------------------------------------------------------
''' Calculates fitness based on sum of average difference between a cell and it's neighbors colors '''
def neighbor_based_fitness(image_board):
    score = 0

    for row_num in range(len(image_board.board)):
        for col_num in range(len(image_board.board[0])):
            cell_score = 0
            current_cell = image_board.get(row_num, col_num)
            num_neighbors = 0
            for direction in NEIGHBORING_DIRECTIONS:
                try:
                    neighbor = image_board.get(row_num + direction[0], col_num + direction[1])
                    num_neighbors += 1
                    cell_score += abs(current_cell - neighbor)
                except:
                    pass
            score += (cell_score/num_neighbors)

    return 1/score

''' Move that swaps one color for another '''
def move_normal(image_board, r1, c1, r2, c2):
    el1 = image_board.get(r1, c1)
    el2 = image_board.get(r2,c2)
    image_board.set(r1,c1,el2)
    image_board.set(r2,c2,el1)
    return

class ImageBoard:

    def __init__(self,
                 initial_pool, # the initial pool of pictures TODO gonna leave these as just hex colors for now
                 move_function=move_normal, # the function used for mutation
                 fitness_function=neighbor_based_fitness, # the function used to determine fitness
                 ):
        self.totalPictures = len(initial_pool)
        self.board = np.array(initial_pool).astype('int')
        np.random.shuffle(self.board)
        shape = find_shape(self.totalPictures)
        self.rows = int(shape[0])
        self.columns = int(shape[1])
        self.board = self.board.reshape(self.rows, self.columns)
        self.initial_pool = initial_pool
        self.move_function = move_function
        self.fitness_function = fitness_function
        self.fitness = self.calculate_fitness()
        pass

    ''' Returns the calculated fitness of the organism '''
    def calculate_fitness(self):
        self.fitness = self.fitness_function(self)  # use whatever fitness function was defined
        return self.fitness

    ''' Get the value at row and column '''
    def get(self, row, column):
        return self.board[row][column]

    ''' Set the value at row and column '''
    def set(self, row, column, value):
        self.board[row][column] = value

    ''' Swaps the two elements '''
    def move(self, r1, c1, r2, c2):
        self.move_function(self, r1, c1, r2, c2)  # call the move function on self
        self.calculate_fitness()
        pass

    ''' Return random (row, col, element) tuple '''
    def random_element(self):
        row = random.randrange(0,self.rows)
        col = random.randrange(0,self.columns)
        return row, col, self.board[row][col]

    ''' Return the row, col of a given color '''
    def locate_element(self, color):
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                if self.board[row][col] == color:
                    return row, col

    ''' Randomly shuffle the board '''
    def shuffle(self):
        np.random.shuffle(self.board)

    ''' Overrides equals '''
    def __eq__(self, other):
        return self.fitness == other.fitness

    ''' Overrides > based on fitness '''
    def __gt__(self, other):
        return self.fitness > other.fitness

    ''' Overrides < based on fitness '''
    def __lt__(self, other):
        return self.fitness < other.fitness

    ''' Overrides str()  '''
    def __str__(self):

        def get_color_escape(r, g, b):
            return '\033[{};2;{};{};{}m\033[0m'.format(38, r, g, b)

        string = ""
        for row in self.board:
            for item in row:
                string += f'{get_color_escape(0xFF, 0x00, 0x00)} {str(hex(item))}'
            string += "\n"
        return string


if __name__ == "__main__":
    print("Hello World.")