from mimetypes import init
import numpy as np
import random
import math

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


class Sorter():

    def __init__(self, initial_pool):
        self.board = np.array(initial_pool).astype('int')
        self.board.sort()
        shape = find_shape(len(initial_pool))
        self.rows = shape[0]
        self.columns = shape[1]
        self.board = self.board.reshape(self.rows, self.columns)

    ''' Overrides str()  '''
    def __str__(self):

        string = ""
        for row in self.board:
            for item in row:
                string += f'{str(hex(item))} '
            string += "\n"
        return string


if __name__ == "__main__":
    pool = []
    pop_size = 100

    for color in range(pop_size):
        pool.append(int(hex(random.randint(0,16777215)), base=16))

    sorter = Sorter(pool)

    print(sorter)