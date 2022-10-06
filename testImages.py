from PIL import Image
import os
from imageboard import find_shape

image_paths = os.listdir('images/')
if ".DS_Store" in image_paths:
    image_paths.remove('.DS_Store')

images = [Image.open("images/" + impath) for impath in image_paths]

min_dimensions = 0,0
minimum_area = 999999999999999999999999999999999999999
for pic in images:
    area = pic.size[0]*pic.size[1]
    if area < minimum_area:
        minimum_area = area
        min_dimensions = pic.size
for index in range(len(images)):
    images[index] = images[index].resize((min_dimensions))

num_row, num_col = find_shape(len(images))
num_row = int(num_row)
num_col = int(num_col)
width = min_dimensions[0] * num_col
height = min_dimensions[1] * num_row

collage = Image.new('RGB', (width, height))

for row in range(num_row):
    for col in range(num_col):
        collage.paste(im=images[row*num_col+col], box=(col*min_dimensions[1],row*min_dimensions[0]))

collage.save('./test.jpeg')
