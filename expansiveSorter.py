from calendar import c
from imageboard import *
import copy
import random
import math

class ExpansiveSorter:

    def __init__(self, image_board, image_processor):
        self.image_board = image_board
        self.image_processor = image_processor
        self.unused_colors = copy.deepcopy(self.image_board.initial_pool)
        self.rows = image_board.rows
        self.columns = image_board.columns
        # Sorted Board Starts as an Empty Image Board. Use numuber one above hex max for color (6 digit hex assumption)
        self.sorted_board = ImageBoard([0]*self.columns*self.rows)

        # set the starting image to a random one
        starting_color = image_board.random_element()[2]
        self.sorted_board.set(0, 0, starting_color)
        self.unused_colors.remove(starting_color)

        # expand_queue of spots (row,col) that will have their neighbors expanded (start at top left)
        self.expand_queue = [(0,0)]

    ''' Returns list of tuples of row,col of valid neighbors to the given row,col'''
    def get_neighbors(self, row, col):
        neighbors = []
        for direction in NEIGHBORING_DIRECTIONS:
            new_r = row + direction[0]
            new_c = col + direction[1]
            # make sure it is in the bounds
            if new_r >= 0 and new_r < self.rows and new_c >= 0 and new_c < self.columns and self.sorted_board.get(new_r, new_c) == 0:
                neighbor = (new_r, new_c)
                neighbors.append(neighbor)
        return neighbors

    ''' Sort the hex color values expansively '''
    def sort(self):

        # While there are items in the expand_queue
        while (self.expand_queue):
            # Get the next in the expand_queue
            current_coords = self.expand_queue[0]
            self.expand_queue.remove(current_coords)
            # Get it's neighbors
            neighbors = self.get_neighbors(current_coords[0], current_coords[1])
            # Add neighbors to expand_queue
            for n in neighbors:
                self.expand_queue.append(n)
            # Shuffle so we don't tend in one direction
            random.shuffle(self.expand_queue)
            random.shuffle(neighbors)

            # Now color in each neighbor (removing that color from the unused list as you go)
            for n in neighbors:
                close_color = self.next_closest(current_coords)
                self.sorted_board.set(n[0],n[1], close_color)
                self.unused_colors.remove(close_color)

        return self.sorted_board

    ''' Find the closest color, and return it '''
    #! DOES NOT REMOVE IT FROM UNUSED_COLORS
    def next_closest(self, current_coords):

        # Get the color at the current space
        current_color = self.sorted_board.get([current_coords[0]], [current_coords[1]])
        # Parallel list whose minimum is the closest value to current color
        abs_value_list = []
        for c in self.unused_colors:
            abs_value_list.append(abs(current_color - c))
        
        minimum = min(abs_value_list)
        index_of_closest = abs_value_list.index(minimum)
        closest = self.unused_colors[index_of_closest]

        return closest