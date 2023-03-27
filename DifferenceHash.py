# Import dependencies
from PIL import Image
import imagehash
import numpy as np
import glob
import sys

input_path1 = r'/Users/rakshithanagendrappa/Desktop/NormalExtracted/*.jpg'
out_loc = '/Users/rakshithanagendrappa/Desktop/DifferenceHashHammingDistances.txt'

original_stdout = sys.stdout

image_paths1 = list(glob.glob(input_path1))
for i in image_paths1:
    l = i.split('/')
    fileName = l[-1]
    input_path2 = r'/Users/rakshithanagendrappa/Desktop/DistortedExtracted/'
    input_path2 = input_path2 + fileName

    dhash1 = imagehash.dhash(Image.open(i))
    dhash2 = imagehash.dhash(Image.open(input_path2))
    with open(out_loc, 'a') as f:
        sys.stdout = f 
        print(dhash1-dAhash2)    #Computing hamming distance

sys.stdout = original_stdout
