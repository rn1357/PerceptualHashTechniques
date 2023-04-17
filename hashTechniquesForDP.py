# Import dependencies
from PIL import Image
import imagehash
import glob
import csv, os, sys

def hashTechniquesForDP(hashTechnique, input_filepath1,output_loc):
    fingerPrintWithHDList = []  #list of lists
    header = ['F_id']
    for filepath1 in input_filepath1:
        fingerPrintWithHD = []
        #getting filename without extension
        l = filepath1.split('/')
        fileName = l[-1]
        fileName_without_ext = fileName[:fileName.rindex('.')]

        F_id = "f"+ fileName_without_ext
        #putting the filename into the list
        fingerPrintWithHD.append(F_id)
        header.append(F_id)
        for filepath2 in input_filepath1:
            match hashTechnique:
                case "average_hash":
                    #computing hash values using average hash
                    ahash1 = imagehash.average_hash(Image.open(filepath1))
                    ahash2 = imagehash.average_hash(Image.open(filepath2))

                    #putting the hamming distance into the list
                    fingerPrintWithHD.append(ahash1-ahash2)
                    
                case "phash":
                    #computing hash values using dct-based hash
                    phash1 = imagehash.phash(Image.open(filepath1))
                    phash2 = imagehash.phash(Image.open(filepath2))

                    #putting the hamming distance into the list
                    fingerPrintWithHD.append(phash1-phash2)

                case "dhash":
                    #computing hash values using difference hash
                    dhash1 = imagehash.dhash(Image.open(filepath1))
                    dhash2 = imagehash.dhash(Image.open(filepath2))

                    #putting the hamming distance into the list
                    fingerPrintWithHD.append(dhash1-dhash2)

                case "whash":
                    #computing hash values using dwt-based hash
                    whash1 = imagehash.whash(Image.open(filepath1))
                    whash2 = imagehash.whash(Image.open(filepath2))

                    #putting the hamming distance into the list
                    fingerPrintWithHD.append(whash1-whash2)                    

                case _:print("Please input correct hash technique")
        
        #appending list to form list of lists
        fingerPrintWithHDList.append(fingerPrintWithHD)
        
    #writing into csv file   
    with open(output_loc, 'w', newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(fingerPrintWithHDList)


if __name__ == "__main__":
    input_dir1 = input("Please provide the path to the extracted normal fingerprints folder: ")
    input_filepath1 = []
    dirs = os.listdir(input_dir1)
    for file in dirs:
        if file.endswith(".jpg"):
            input_filepath1.append(input_dir1 + file)

    
    hashTechnique = input("Please input which hash technique you would like to work with(average_hash or phash or dhash or whash):")
    output_loc = input("Please enter the csv file path for output:")
    fingerPrintWithHDList = hashTechniquesForDP(hashTechnique, input_filepath1,output_loc)

#input examples
#input1 = /Users/rakshithanagendrappa/Desktop/NormalExtracted/
#outputloc = /Users/rakshithanagendrappa/Desktop/Minutiae/DPm/DWT-basedHashHammingDistances.csv
