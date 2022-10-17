from  imaging.imageprocessing import *
from resources.textColors import *
import os

#! Main Entry Point for the Pixelizing Reference Art Functionality of PicAsso

# Get all images to be used as pixels
covers = os.listdir('images_main/')
covers.remove('.gitignore')
if ".DS_Store" in covers:
    covers.remove('.DS_Store')

# Check that necessary files exist
if (len(covers) < 4): 
    print(f'{FAIL}Please ensure images are loaded into /images_main directory. This can be done by running spotify.py.{ENDC}')
if (not os.path.exists("reference_picture.jpeg")):
    print(f'{FAIL}Please ensure the file "reference_picture.jpeg" is present in the current directory to pixelize.{ENDC}')

# Create the pixelized image
reference_img = "reference_picture.jpeg"
imProc = ImageProcessor(covers)
imProc.get_all_colors()
imProc.pic_from_reference(reference_img)
print(f"{OKGREEN}Pixelized image generated at pixeled.jpeg!{ENDC}")