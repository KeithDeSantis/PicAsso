from sorting.hillclimb import HillClimber
from imaging.imageboard import ImageBoard
from imaging.imageprocessing import *
from sorting.expansiveSorter import *
from resources.textColors import *
from spotify import *
import sys
import os

#!  Main Entry Point for the Collage Art Functionality of PicAsso
# Refer to README.md for instructions on calling this script

# Get all the images to be used
covers = os.listdir('images_main/')
covers.remove('.gitignore')
if ".DS_Store" in covers:
    covers.remove('.DS_Store')

# Ensure the needed files exist
if(len(covers) < 4): 
    print(f'{FAIL}Please ensure images are loaded into /images_main directory. This can be done by running spotify.py.{ENDC}')

# Used for sampling from larger list, 
# set SAMPLE_SIZE variable in config.py
# COMMENT OUT THIS LINE TO USE EVERY IMAGE IN /images_main
#covers = random.sample(covers, SAMPLE_SIZE)

# Instantiate ImageProcesor class and determine dominant colors of images
imProc = ImageProcessor(covers)
imProc.get_all_colors()

# Default to Expansive Search with Touchup Hill Climbing
if (len(sys.argv) == 1):
    boards = []
    # Get a bunch of random starting covers and pick the one that gives the best fitness
    for color in (imProc.colors):
        print(f"Testing with starting color: {OKBLUE}{color}{ENDC}")
        # If you want a specific rows and columns replace r and c here
        es = ExpansiveSorter(ImageBoard(imProc.colors, r=ROWS, c=COLUMNS), imProc, color)
        boards.append(es.sort())
    fitnesses = [b.calculate_fitness() for b in boards]
    min_index = fitnesses.index(max(fitnesses))
    best_board = boards[min_index]
    # Run through hillclimbing in touchup_mode to help optimize the board
    print(f"{WARNING}Touching up with hillclimbing...{ENDC}")
    hillClimb = HillClimber(best_board, 60)
    best_board = hillClimb.run(touchup_mode=True)
# If we specify hill climbing
elif len(sys.argv) >= 2:
    print("Performing hillclimbing...")

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


# After desired method of collage organizing is finished,
# organize the image paths accordingly and call ImageProcessor's 
# create_collage function
grid = best_board.board
name_grid = [] # list in order of rows 0, 1, 2 but as one list
for row in grid:
    for color in row:
        # here we duplicate images unless we pass in a blacklist of images we've used already
        name_grid.append(imProc.get_image_name_from_color(color, blacklist=name_grid))

# Two functions used to ensure any parrallel lists in imProc are
# synchronized
imProc.rearrange(name_grid)
imProc.resize()

# Print out collage info
print(f"{OKCYAN}Rows: {str(best_board.rows)}\nColumns: {str(best_board.columns)}{ENDC}")
print(f"{OKGREEN}Individual image dimensions: {imProc.min_dimensions}{ENDC}")

# Create and save the collage to "collage.jpeg"
imProc.create_collage(best_board)
print(f"{OKGREEN}Collage generated at collage.jpeg!{ENDC}")