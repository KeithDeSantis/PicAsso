from __future__ import print_function
from imaging.imageboard import *
from PIL import Image
import scipy.cluster
import numpy as np
import scipy.misc
import binascii
import warnings
import scipy
import math

#! Class that handles image processing and maintains parallel lists of:
#! image paths
#! image objects
#! image dominant color hexes
class ImageProcessor():

    def __init__(self, image_paths):
        warnings.filterwarnings('ignore')

        self.image_paths = image_paths

        # Get all images as objects
        self.images = [Image.open("images_main/" + impath) for impath in image_paths]
        self.colors = []

        # Resize all images
        self.min_dimensions = 0,0
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
            self.images[index] = self.images[index].resize((self.min_dimensions))
    
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
        index_max = scipy.argmax(counts)                    # find most frequent
        peak = codes[index_max]
        colour = binascii.hexlify(bytearray(int(c) for c in peak)).decode('ascii')
        str_dom_color = "0x" + colour
        main_color = hex(int(str_dom_color, 16))
        return main_color

    ''' Get list of all the dominant colors in the image '''
    def get_all_colors(self):
        self.colors = []
        for image in self.images:
            path = self.image_paths[self.images.index(image)]
            print("Determining dominant color of image: " + path + "...")
            try:
                self.colors.append(self.get_main_color(image))
            except:
                print("Image sized poorly...")
            print(str(self.colors[-1]) + " : " + path)
        return self.colors

    ''' Get the image name from the color. If the image name is in the blacklist, skip it '''
    def get_image_name_from_color(self, color, blacklist=[]):

        for index in range(len(self.image_paths)):
            if(self.image_paths[index] not in blacklist):
                if(self.colors[index] == color):
                    return self.image_paths[index]

    def get_color_from_image(self, image):
        return self.colors[self.image.index(image)]

    ''' Get the RGB values of all colors (as tuples)'''
    def get_rgbs(self):
        rgbs = []
        for color in self.colors:
            rgbs.append(hex_to_rgb(color))
        return rgbs

    ''' Rearrange the color and name arrays by a new name array order '''
    def rearrange(self, new_image_order):
        new_color_array = []

        for image in new_image_order:
            new_color_array.append(self.colors[self.image_paths.index(image)])
        
        self.colors = new_color_array
        self.image_paths = new_image_order
        self.images = [Image.open("images_main/" + impath) for impath in self.image_paths]

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
                #TODO here might be the duplication issue

                # Need to ensure we aren't duplicating images with the same dominant colors
                for ind, img in enumerate(self.images):
                    # If the color matches and hasn't been used yet
                    if (self.colors[ind] == str(hex(image_board.get(row,col))) and img not in used_images):
                        # Add it and add it to the used image list
                        collage.paste(im=img, box=(col*ind_height,row*ind_width))
                        used_images.append(img)
                        # Break out of the loop, otherwise we'd overlay some images 
                        # if they have the same color and haven't been used yet
                        break

        collage.save('./collage.jpeg')

    ''' Make the reference picture with small versions of self.images as pixels '''
    def pic_from_reference(self, reference_picture):
        pass




def hex_to_rgb(value):
    value = value.lstrip('0x')
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
            f.write('>\n') # mark the end of a row
            counter = 0
        rgb = hex_to_rgb(color)
        f.write(str(rgb[0]) + '\t' + str(rgb[1]) + '\t' + str(rgb[2]) + '\n')
        counter += 1

if __name__ == "__main__":
    
    
    '''
    covers = os.listdir('images_main/')
    covers.remove('.DS_Store')
    imProc = ImageProcessor(covers)
    f = open("./rgb_values.txt", 'w')
    f.write('')
    f.close()
    for color in imProc.get_all_colors():
        rgb = hex_to_rgb(color)
        f = open("./rgb_values.txt", 'a')
        f.write(str(rgb[0]) + '\t' + str(rgb[1]) + '\t' + str(rgb[2]) + '\n')
    '''
    pass