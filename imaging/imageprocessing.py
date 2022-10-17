from __future__ import print_function
from imaging.imageboard import *
from PIL import Image
from resources.textColors import *
import scipy.cluster
import numpy as np
import scipy.misc
import binascii
import warnings
import scipy
import math
import os
import threading
import ctypes
from constants import *

REFERENCE_IMG_DIMENSION = 50

#! Class that handles image processing and maintains parallel lists of:
#! image paths
#! image objects
#! image dominant colors


class ImageProcessor():

    def __init__(self, image_paths):
        warnings.filterwarnings('ignore')

        self.image_paths = image_paths

        # Get all images as objects
        self.images = [Image.open("images_main/" + impath)
                       for impath in image_paths]
        self.colors = []
        # TODO eventually improve this, for now dict is only for reference imaging
        self.img_color_dict = {}

        self.threads = []

        # Resize all images
        self.min_dimensions = 0, 0
        minimum_area = 999999999999999999999999999999999999999
        for pic in self.images:
            area = pic.size[0]*pic.size[1]
            # ensure we're only doing squares
            if area < minimum_area and math.sqrt(area) == pic.size[0]:
                minimum_area = area
                self.min_dimensions = pic.size
        self.resize()
        pass

    ''' Resize all images '''

    def resize(self):
        for index in range(len(self.images)):
            self.images[index] = self.images[index].resize(
                (self.min_dimensions))

    ''' Get the dominant color in an image. Takes in an image object '''

    def get_main_color(self, im):
        NUM_CLUSTERS = 5
        ar = np.asarray(im)
        shape = ar.shape
        try:
            ar = ar.reshape(scipy.product(shape[:2]), shape[2]).astype(float)
        except:
            raise
        codes, dist = scipy.cluster.vq.kmeans(ar, NUM_CLUSTERS)
        vecs, dist = scipy.cluster.vq.vq(ar, codes)         # assign codes
        counts, bins = scipy.histogram(vecs, len(codes))    # count occurrences
        # find most frequent
        index_max = scipy.argmax(counts)
        peak = codes[index_max]
        colour = binascii.hexlify(bytearray(int(c)
                                  for c in peak)).decode('ascii')
        str_dom_color = "0x" + colour
        main_color = hex_to_rgb(hex(int(str_dom_color, 16)))
        return main_color

    #! Depreciated
    ''' Get list of all the dominant colors in the image
    def get_all_colors(self):
        self.colors = []
        for image in self.images:
            path = self.image_paths[self.images.index(image)]
            print("Determining dominant color of image: " + path + "...")
            try:
                self.colors.append(self.get_main_color(image))
                # Add color:image pair to dictionary
                 # TODO maybe resize the images to be smaller or bigger...
                self.img_color_dict[self.colors[-1]] = image.resize(
                    (REFERENCE_IMG_DIMENSION, REFERENCE_IMG_DIMENSION))
            except:
                print("Image sized poorly...")
            print(str(self.colors[-1]) + " : " + path)

        self.thread_all_colors()
        return self.colors
        '''

    ''' get_all_colors() but using threading '''
    def get_all_colors(self):
        for i in self.images:
            t = threading.Thread(target=self.get_color_per_image, args=(i,))
            self.threads.append(t)
        for thread in self.threads:
            thread.start()
        for thread in self.threads:
            thread.join()
        return self.colors

    ''' Function to get an image's color and add it to the colors. Used for threading '''
    def get_color_per_image(self, image):
        thread_id = threading.get_native_id()
        path = self.image_paths[self.images.index(image)]
        print(f"{OKGREEN}THREAD {thread_id}:{ENDC} Determining dominant color of image: {path} ...")
        try:
                clr = self.get_main_color(image)
                self.colors.append(clr)
                # Add color:image pair to dictionary
                self.img_color_dict[clr] = image.resize(
                    (REFERENCE_IMG_DIMENSION, REFERENCE_IMG_DIMENSION))
                print(f"{OKGREEN}THREAD {thread_id}:{ENDC} {clr}: {path}")
        except:
                print(f"{FAIL}THREAD {thread_id}:{ENDC} Image sized poorly...")

    ''' Get the image name from the color. If the image name is in the blacklist, skip it '''
    def get_image_name_from_color(self, color, blacklist=[]):

        for index in range(len(self.image_paths)):
            if (self.image_paths[index] not in blacklist):
                #print(f'SelfRED: {self.colors[index][RED]}\nColorRED: {color[RED]}\nSelfGREEN: {self.colors[index][GREEN]}\nColorGREEN: {color[GREEN]}\nSelfBLUE: {self.colors[index][BLUE]}\nColorBLUE: {color[BLUE]}')
                if (self.colors[index][RED] == color[RED] and self.colors[index][GREEN] == color[GREEN] and self.colors[index][BLUE] == color[BLUE]):
                    return self.image_paths[index]
        return 'balls'


    def get_color_from_image(self, image):
        return self.colors[self.image.index(image)]

    ''' DEPRECIATED Get the RGB values of all colors (as tuples)
    def get_rgbs(self):
        rgbs = []
        for color in self.colors:
            rgbs.append(hex_to_rgb(color))
        return rgbs
    '''

    ''' Rearrange the color and name arrays by a new name array order '''
    def rearrange(self, new_image_order):
        new_color_array = []

        for image in new_image_order:
            new_color_array.append(self.colors[self.image_paths.index(image)])

        self.colors = new_color_array
        self.image_paths = new_image_order
        self.images = [Image.open("images_main/" + impath)
                       for impath in self.image_paths]

    ''' Stitch together images in order of imageboard '''
    def create_collage(self, image_board):
        rows = image_board.rows
        columns = image_board.columns
        ind_width = self.min_dimensions[0]
        ind_height = self.min_dimensions[1]
        width = self.min_dimensions[0] * columns
        height = self.min_dimensions[1] * rows

        collage = Image.new('RGB', (width, height))

        #! When the min_dimension columns is x smaller than the rows, it leads to x tall black lines between rows in the collage

        used_images = []
        for row in range(rows):
            for col in range(columns):
                # TODO here might be the duplication issue

                # Need to ensure we aren't duplicating images with the same dominant colors
                for ind, img in enumerate(self.images):
                    # If the color matches and hasn't been used yet
                    if (rgbs_equal(self.colors[ind], image_board.get(row, col)) and img not in used_images):
                        # Add it and add it to the used image list
                        collage.paste(im=img, box=(
                            col*ind_height, row*ind_width))
                        used_images.append(img)
                        # Break out of the loop, otherwise we'd overlay some images
                        # if they have the same color and haven't been used yet
                        break

        collage.save('./collage.jpeg')

    ''' Make the reference picture with small versions of self.images as pixels '''
    def pic_from_reference(self, reference_picture):

        print("Generating collage from reference...")

        reference = Image.open(reference_picture)
        # Tuple of width and height
        size = reference.size
        width = size[0]
        height = size[1]

        rgb_pixels = reference.load()
        pixels = []
        for x in range(width):
            for y in range(height):
                rgb = rgb_pixels[x, y]
                pixels.append((rgb[RED], rgb[GREEN], rgb[BLUE]))
                    #TODO old method of getting hex hex(int(f'0x{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}', 16)))

        new_image = Image.new(
            'RGB', (width*REFERENCE_IMG_DIMENSION, height*REFERENCE_IMG_DIMENSION))

        pixel_number = 0
        for x in range(width):
            for y in range(height):
                # TODO put the closest album cover in that spot
                new_image.paste(im=self.img_color_dict[self.get_closest_color(
                    pixels[pixel_number])], box=(x*REFERENCE_IMG_DIMENSION, y*REFERENCE_IMG_DIMENSION))
                pixel_number += 1

        new_image.save('./pixeled.jpeg')

    ''' Get the closest color to the given color from all the image colors '''

    def get_closest_color(self, pixel_color):

        closest_color = None
        smallest_difference_sum = 99999999
        for color in self.img_color_dict.keys():
            difference = sum_rgb_difference(pixel_color, color)
            if difference < smallest_difference_sum:
                smallest_difference_sum = difference
                closest_color = color

        return closest_color


''' Get the sum of the differences of each corresponding color of two rgb tuples '''
# TODO test squaring each individually before summing
def sum_rgb_difference(rgb_tuple1, rgb_tuple2):
    return abs(rgb_tuple1[RED]-rgb_tuple2[RED]) + abs(rgb_tuple1[GREEN]-rgb_tuple2[GREEN]) + abs(rgb_tuple1[BLUE]-rgb_tuple2[BLUE])


''' Turns hex to rgb 3 tuple '''
def hex_to_rgb(value):
    value = value.lstrip('0x')
    if (len(value) < 6):
        # add leading zeros
        value = '0'*(6-len(value)) + value
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


''' Write RGB values to file'''
def write_rgb_values(covers, width, imProc):
    # Get the covers in a list for ImageProcessor
    list_covers = []
    for row in covers:
        for cover in row:
            list_covers.append(imProc.get_image_name_from_color(hex(cover)))
    imProc.rearrange(list_covers)
    f = open("./rgb_values.txt", 'w')
    f.write('')
    f.close()
    f = open("./rgb_values.txt", 'a')
    counter = 0
    for color in imProc.colors:
        if (counter >= width):
            f.write('>\n')  # mark the end of a row
            counter = 0
        rgb = color
        f.write(str(rgb[RED]) + '\t' + str(rgb[GREEN]) + '\t' + str(rgb[BLUE]) + '\n')
        counter += 1

''' Helper to check that every value in 2 rgb tuples are equal '''
def rgbs_equal(rgb_tuple1, rgb_tuple2):
    return rgb_tuple1[RED] == rgb_tuple2[RED] and rgb_tuple1[GREEN] and rgb_tuple2[GREEN] and rgb_tuple1[BLUE] == rgb_tuple2[BLUE]