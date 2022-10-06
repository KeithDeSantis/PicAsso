from hillclimb import HillClimber
from imageboard import ImageBoard
import old_files.ga as ga
import sys
import os
from imageprocessing import *
from sorting import *

if __name__ == "__main__":
    runtime = sys.argv[1]
    covers = os.listdir('images/')
    if ".DS_Store" in covers:
        covers.remove('.DS_Store')
    imProc = ImageProcessor(covers)
    imProc.get_all_colors()
    hillClimb = HillClimber(ImageBoard([int(x, base=16) for x in imProc.colors]), runtime)

    hillClimb.run()

    '''
    grid = hillClimb.image_board.board
    name_grid = []
    for r_index, row in enumerate(grid):
        name_grid.append([])
        for c_index, color in enumerate(row):
            name_grid[r_index].append(imProc.get_image_name_from_color(hex(color)))
    print(name_grid)
    '''

    write_rgb_values(hillClimb.image_board.board, hillClimb.image_board.columns, imProc)

    os.system("python3 testColors.py")

    pass