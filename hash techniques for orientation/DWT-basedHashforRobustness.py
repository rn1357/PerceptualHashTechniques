# Import dependencies
from PIL import Image
import imagehash
import glob
import csv

#input and output file paths
input_path1 = r'/Users/rakshithanagendrappa/Desktop/NormalOrientationMaps/*.jpg'
out_loc = '/Users/rakshithanagendrappa/Desktop/OrientationRobustness/DWT-basedHashHammingDistances.txt'

#Lists to store the values
fingerPrintWithHD = []
fingerPrintWithHDList = []  #list of lists

image_paths1 = list(glob.glob(input_path1))
for i in image_paths1:
    l = i.split('/')
    fileName = l[-1]
    input_path2 = r'/Users/rakshithanagendrappa/Desktop/DistortedOrientationMaps/'
    input_path2 = input_path2 + fileName

    #getting filename without extension
    fileName_without_ext = fileName[:fileName.rindex('.')]

    #putting the filename into the list
    fingerPrintWithHD.append(fileName_without_ext)

    #computing hash values using dwt-based hash
    whash1 = imagehash.whash(Image.open(i))
    whash2 = imagehash.whash(Image.open(input_path2))

    #putting the hamming distance into the list
    fingerPrintWithHD.append(whash1-whash2)

    #appending list to form list of lists
    fingerPrintWithHDList.append(fingerPrintWithHD)
    fingerPrintWithHD = []

#writing into csv file   
with open(out_loc, 'w', newline="") as f:
    writer = csv.writer(f)
    writer.writerows(fingerPrintWithHDList)
            





