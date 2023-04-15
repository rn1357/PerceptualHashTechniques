# Import dependencies
from PIL import Image
import imagehash
import glob
import csv

#input and output file paths
input_path1 = r'/Users/rakshithanagendrappa/Desktop/NormalExtracted/*.jpg'
out_loc = '/Users/rakshithanagendrappa/Desktop/MinutiaeRobustness/DCT-basedHashHammingDistances.txt'

#Lists to store the values
fingerPrintWithHD = []
fingerPrintWithHDList = []  #list of lists
header = ['F_id', 'HashTech']
image_paths1 = list(glob.glob(input_path1))
for i in image_paths1:
    l = i.split('/')
    fileName = l[-1]
    input_path2 = r'/Users/rakshithanagendrappa/Desktop/DistortedExtracted/'
    input_path2 = input_path2 + fileName

    #getting filename without extension
    fileName_without_ext = fileName[:fileName.rindex('.')]

    #putting the filename into the list
    fingerPrintWithHD.append(fileName_without_ext)

    #computing hash values using dct-based hash
    phash1 = imagehash.phash(Image.open(i))
    phash2 = imagehash.phash(Image.open(input_path2))

    #putting the hamming distance into the list
    fingerPrintWithHD.append(phash1-phash2)

    #appending list to form list of lists
    fingerPrintWithHDList.append(fingerPrintWithHD)
    fingerPrintWithHD = []

#writing into csv file   
with open(out_loc, 'w', newline="") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(fingerPrintWithHDList)
            

