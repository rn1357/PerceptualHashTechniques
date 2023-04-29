# Import dependencies
from PIL import Image
import imagehash
import csv,os,sys

def hashCalculation(hashTechnique, input_filepath, output_loc):
    HashValuesList = []
    header = ['F_id', 'Hash']
    for filepath in input_filepath:
        HashValues = []
        l = filepath.split('/')
        fileName = l[-1]
        #getting filename without extension
        fileName_without_ext = fileName[:fileName.rindex('.')]
        #putting the filename into the list
        HashValues.append("f_"+fileName_without_ext)
        match hashTechnique:
            case "average_hash":
                #computing hash values using average hash
                Ahash = imagehash.average_hash(Image.open(filepath))
                HashValues.append(str(Ahash))
            case "phash":
                #computing hash values using dct-based hash
                dcthash = imagehash.phash(Image.open(filepath))
                HashValues.append(str(dcthash))
            case "dhash":
                #computing hash values using difference hash
                Dhash = imagehash.dhash(Image.open(filepath))
                HashValues.append(str(Dhash))
            case "whash":
                #computing hash values using dwt-based hash
                dwthash = imagehash.whash(Image.open(filepath))
                HashValues.append(str(dwthash))
            case _:
                print("Please input correct hash technique listed")
        HashValuesList.append(HashValues)
    #writing into csv file   
    with open(output_loc, 'w', newline="") as f1:
        writer = csv.writer(f1)
        writer.writerow(header)
        writer.writerows(HashValuesList)

if __name__ == "__main__":
    hashTechnique = sys.argv[1]
    input_dir = sys.argv[2]
    input_filepath = []
    dirs = os.listdir(input_dir)
    for file in dirs:
        if file.endswith(".jpg"):
            input_filepath.append(os.path.join(input_dir,file))
    output_for_hashes = sys.argv[3]
    hashCalculation(hashTechnique, input_filepath, output_for_hashes)
    



