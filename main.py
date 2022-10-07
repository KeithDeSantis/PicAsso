from hillclimb import HillClimber
from imageboard import ImageBoard
import os
from imageprocessing import *
from expansiveSorter import *
import sys
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

if __name__ == "__main__":

    f = open('tokens.txt', 'r')
    TOKEN = f.readline()
    os.system(f'curl -X "GET" "https://api.spotify.com/v1/me/tracks" -H "Accept: application/json" -H "Content-Type: application/json" -H "Authorization: Bearer {TOKEN}" > songs.json')

    covers = os.listdir('images/')
    if ".DS_Store" in covers:
        covers.remove('.DS_Store')
    imProc = ImageProcessor(covers)
    imProc.get_all_colors()

   #! Expansive Sort
    boards = []
    # Get a bunch of random starting covers and pick the one that gives the best fitness
    for color in (imProc.colors):
        print("Color: " + str(color))
        es = ExpansiveSorter(ImageBoard([int(x, base=16) for x in imProc.colors]), imProc, color)
        boards.append(es.sort())
    fitnesses = [b.calculate_fitness() for b in boards]
    min_index = fitnesses.index(max(fitnesses))
    best_board = boards[min_index]

   #! Hill Climbing
    #runtime = sys.argv[1]
    #hillClimb = HillClimber(ImageBoard([int(x, base=16) for x in imProc.colors]), runtime)
    #best_board = hillClimb.run()

    grid = best_board.board
    name_grid = [] # list in order of rows 0, 1, 2 but as one list
    for r_index, row in enumerate(grid):
        for c_index, color in enumerate(row):
            name_grid.append(imProc.get_image_name_from_color(hex(color)))
    imProc.rearrange(name_grid)
    imProc.resize()
    imProc.create_collage(best_board)


    #! Color Testing
    #write_rgb_values(hillClimb.image_board.board, hillClimb.image_board.columns, imProc)
    #os.system("python3 testColors.py")