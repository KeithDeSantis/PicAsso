from sorting.hillclimb import HillClimber
from imaging.imageboard import ImageBoard
from imaging.imageprocessing import *
from sorting.expansiveSorter import *
from resources.textColors import *
from spotify import *
import random
import sys
import os

if __name__ == "__main__":

    covers = os.listdir('images_main/')
    covers.remove('.gitignore')
    if ".DS_Store" in covers:
        covers.remove('.DS_Store')
    if(len(covers) < 4): print(f'{FAIL}Please ensure images are loaded into /images_main directory. This can be done by running spotify.py.{ENDC}')

    # Used for sampling from larger list, uncomment for random sampling and set SAMPLE_SIZE in config.py
    #covers = random.sample(covers, SAMPLE_SIZE)
    
    imProc = ImageProcessor(covers)
    imProc.get_all_colors()

    # Default to Expansive Search with Touchup Hill Climbing
    if (len(sys.argv) == 1):
        boards = []
        # Get a bunch of random starting covers and pick the one that gives the best fitness
        for color in (imProc.colors):
            print("Testing with starting color: " + str(color))
            # If you want a specific rows and columns replace r and c here
            es = ExpansiveSorter(ImageBoard(imProc.colors, r=ROWS, c=COLUMNS), imProc, color)
            boards.append(es.sort())
        fitnesses = [b.calculate_fitness() for b in boards]
        min_index = fitnesses.index(max(fitnesses))
        best_board = boards[min_index]
        # Run through hillclimbing in touchup_mode to help optimize the board
        print("Touching up with hillclimbing...")
        hillClimb = HillClimber(best_board, 60)
        best_board = hillClimb.run(touchup_mode=True)
    # If we specify hill climbing
    elif len(sys.argv) >= 2:

        hill_climb_arg_list = ['H', 'HILL',
        'HILLCLIMB', 'HILLCLIMBING']

        if sys.argv[1].upper() in hill_climb_arg_list:
            try:
                runtime = sys.argv[2]
            except:
                print(f'{FAIL}Please provide a number of seconds to run for as an argument.{ENDC}')
                exit()
            hillClimb = HillClimber(ImageBoard(imProc.colors), runtime)
            best_board = hillClimb.run()
        else:
            print(f"{FAIL}Unexpected argument: {sys.argv[1]}{ENDC}")
            exit()
    else:
        print(f'{FAIL}Unexpected number of arguments.{ENDC}')
        exit()


    grid = best_board.board
    name_grid = [] # list in order of rows 0, 1, 2 but as one list
    for row in grid:
        for color in row:
            # here we duplicate images unless we pass in a blacklist of images we've used already
            name_grid.append(imProc.get_image_name_from_color(color, blacklist=name_grid))
    imProc.rearrange(name_grid)
    imProc.resize()
    print(f"{OKCYAN}Rows: {str(best_board.rows)}\nColumns: {str(best_board.columns)}{ENDC}")
    print(f"{OKGREEN}Individual image dimensions: {imProc.min_dimensions}{ENDC}")
    imProc.create_collage(best_board)