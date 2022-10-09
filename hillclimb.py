import time
import random
import copy


class HillClimber:

    def __init__(self, image_board, time_to_run=60):
        self.time_to_run = time_to_run
        self.image_board = image_board
        self.best_board = copy.deepcopy(self.image_board)

    ''' Hill Climb and Find a Best Board '''
    def run(self, touchup_mode=False):
        start = time.time()
        best_fitness = self.best_board.fitness
        possible_pairings = self.get_all_pairings()
        local_max_flag = False
        # Used for print outs
        old_max_fitness = self.image_board.fitness
        number_new_maxes = 0

        while time.time() - start < float(self.time_to_run):

            if(not local_max_flag):
                local_max_flag = True # assume we're at a global max
                random.shuffle(possible_pairings)
                for move in possible_pairings: # shuffle so we randomize where on the board we start
                    # make the move
                    self.image_board.move(move[0][0], move[0][1], move[1][0], move[1][1]) # r1,c1,r2,c2
                    # check if it's better
                    if self.image_board.fitness > best_fitness:
                        best_fitness = self.image_board.fitness
                        self.best_board = copy.deepcopy(self.image_board)
                        local_max_flag = False # if we found an improvement then we weren't at a global max
                        # leave the change...
                        break
                    # if it wasn't better, undo the move and do a different move
                    else:
                        self.image_board.move(move[0][0], move[0][1], move[1][0], move[1][1])

            else:
                # Then no move was an improvement
                if (old_max_fitness < self.image_board.fitness):
                    print(f"Local Maximum #{number_new_maxes} Found of fitness {self.image_board.fitness} > {old_max_fitness}, resetting...")
                    old_max_fitness = self.image_board.fitness
                    number_new_maxes += 1
                    # in touchup mode we only go once
                    if(touchup_mode): return self.best_board
                self.image_board.shuffle()
                local_max_flag = False # reset
  
        return self.best_board
    
    ''' Get all pairings of colors that could be switched'''
    def get_all_pairings(self):

        image_board = self.image_board
        rows = self.image_board.rows
        cols = self.image_board.columns

        pairings_indices = []
        pairings = []

        for row_one in range(rows):
            for col_one in range(cols):
                for row_two in range(rows):
                    for col_two in range(cols):
                        if (row_one != row_two) and (col_one != col_two):
                            pairings_indices.append(((row_one,col_one), (row_two,col_two)))
                            pairings.append((image_board.get(row_one, col_one), image_board.get(row_two, col_two)))

        return pairings_indices


    