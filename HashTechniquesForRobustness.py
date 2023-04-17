# Import dependencies
from PIL import Image
import imagehash
import glob
import csv,os,sys

def hashTechniquesForRobustness(hashTechnique, input_filepath1, input_dir2):
    fingerPrintWithHDList = []  #list of lists
    for filepath in input_filepath1:
        fingerPrintWithHD = []
        l = filepath.split('/')
        fileName = l[-1]
        input_filepath2 = input_dir2 + fileName

        #getting filename without extension
        fileName_without_ext = fileName[:fileName.rindex('.')]

        #putting the filename into the list
        fingerPrintWithHD.append("f_"+fileName_without_ext)

        match hashTechnique:
            case "average_hash":
                #computing hash values using average hash
                ahash1 = imagehash.average_hash(Image.open(filepath))
                ahash2 = imagehash.average_hash(Image.open(input_filepath2))

                #putting the hamming distance into the list
                fingerPrintWithHD.append(ahash1-ahash2)
            case "phash":
                #computing hash values using dct-based hash
                phash1 = imagehash.phash(Image.open(filepath))
                phash2 = imagehash.phash(Image.open(input_filepath2))

                #putting the hamming distance into the list
                fingerPrintWithHD.append(phash1-phash2)
            case "dhash":
                #computing hash values using difference hash
                dhash1 = imagehash.dhash(Image.open(filepath))
                dhash2 = imagehash.dhash(Image.open(input_filepath2))

                #putting the hamming distance into the list
                fingerPrintWithHD.append(dhash1-dhash2)
            case "whash":
                #computing hash values using dwt-based hash
                whash1 = imagehash.whash(Image.open(filepath))
                whash2 = imagehash.whash(Image.open(input_filepath2))

                #putting the hamming distance into the list
                fingerPrintWithHD.append(whash1-whash2)
            case _:
                print("Please input correct hash technique listed")

        #appending list to form list of lists
        fingerPrintWithHDList.append(fingerPrintWithHD)

    return fingerPrintWithHDList


    
if __name__ == "__main__":
    input_dir1 = input("Please provide the path to the extracted normal fingerprints folder: ")
    input_filepath1 = []
    dirs = os.listdir(input_dir1)
    for file in dirs:
        if file.endswith(".jpg"):
            input_filepath1.append(input_dir1 + file)
    
    input_dir2 = input("Please provide the path to the extracted distorted fingerprints folder: ")
    
    hashTechnique = input("Please input which hash technique you would like to work with(average_hash or phash or dhash or whash):")
    fingerPrintWithHDList = hashTechniquesForRobustness(hashTechnique, input_filepath1, input_dir2)

    
    header = ['F_id', 'hamming distance']
    output_loc = input("Please enter the csv file path for output:")
    #writing into csv file   
    with open(output_loc, 'w', newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(fingerPrintWithHDList)

#input examples
#input1 = /Users/rakshithanagendrappa/Desktop/NormalExtracted/
#input2 = /Users/rakshithanagendrappa/Desktop/DistortedExtracted/
#outputloc = /Users/rakshithanagendrappa/Desktop/Minutiae/MinutiaeRobustness/AverageHashHammingDistances.csv
