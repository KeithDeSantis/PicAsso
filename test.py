import os
from  imaging.imageprocessing import *

covers = os.listdir('images_main/')
covers.remove('.gitignore')
if ".DS_Store" in covers:
    covers.remove('.DS_Store')

reference_img = "reference_picture.jpeg"
imProc = ImageProcessor(covers)
imProc.get_all_colors()

imProc.pic_from_reference(reference_img)