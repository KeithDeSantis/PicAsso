from pickle import NONE
from hillclimb import HillClimber
from imageboard import ImageBoard
import os
from imageprocessing import *
from expansiveSorter import *
import sys
from config import *
from spotify import *
import random

if __name__ == "__main__":

    #! Spotify loading
    iterations = NUMBER_LIKED_SONGS//50
    remainder = NUMBER_LIKED_SONGS%50

    #for it in range(iterations):
    #    write_songs_to_json(50,it*50)
    #    user_playlist_tracks_full(50,it*50, PLAYLIST_ID) # used for playlist
    #    save_images_from_json()
    #if(remainder > 0):
    #    write_songs_to_json(remainder,iterations*50)
    #    user_playlist_tracks_full(remainder, iterations*50, PLAYLIST_ID) # used for playlist
    #    save_images_from_json()

    covers = os.listdir('images_main/')
    if ".DS_Store" in covers:
        covers.remove('.DS_Store')
    #covers = random.sample(covers, SAMPLE_SIZE) # used for sampling from larger list
    imProc = ImageProcessor(covers)
    imProc.get_all_colors()

   #! Expansive Sort
    boards = []
    # Get a bunch of random starting covers and pick the one that gives the best fitness
    for color in (imProc.colors):
        print("Testing with starting color: " + str(color))
        # If you want a specific rows and columns replace r and c here
        es = ExpansiveSorter(ImageBoard([int(x, base=16) for x in imProc.colors], r=None, c=None), imProc, color)
        boards.append(es.sort())
    fitnesses = [b.calculate_fitness() for b in boards]
    min_index = fitnesses.index(max(fitnesses))
    best_board = boards[min_index]
    # Run through hillclimbing in touchup_mode to help optimize the board
    hillClimb = HillClimber(best_board, 600)
    best_board = hillClimb.run(touchup_mode=True)

   #! Hill Climbing
    #runtime = sys.argv[1]
    #hillClimb = HillClimber(ImageBoard([int(x, base=16) for x in imProc.colors]), runtime)
    #best_board = hillClimb.run()

    grid = best_board.board
    name_grid = [] # list in order of rows 0, 1, 2 but as one list
    for r_index, row in enumerate(grid):
        for c_index, color in enumerate(row):
            # here we duplicate images unless we pass in a blacklist of images we've used already
            name_grid.append(imProc.get_image_name_from_color(hex(color), blacklist=name_grid))
    imProc.rearrange(name_grid)
    imProc.resize()
    print(f"Rows: {str(best_board.rows)}\nColumns: {str(best_board.columns)}")
    print(f"Individual image dimesions: {imProc.min_dimensions}")
    imProc.create_collage(best_board)


    #! Color Testing
    #write_rgb_values(hillClimb.image_board.board, hillClimb.image_board.columns, imProc)
    #os.system("python3 testColors.py")