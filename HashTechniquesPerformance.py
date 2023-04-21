# Import dependencies
from PIL import Image
import imagehash
import csv,os,sys
import matplotlib.pylab as plt
import pandas as pd

def hashTechniquesForRobustness(hashTechnique, input_filepath1, input_dir2, thresholdList):
    fingerPrintWithHDListforRobustness = []  #list of lists
    header = ['F_id', 'Hamming Distance']
    HammingDistanceListforRobustness = []
    for filepath in input_filepath1:
        fingerPrintWithHDforRobustness = []
        l = filepath.split('/')
        fileName = l[-1]
        input_filepath2 = input_dir2 + fileName
        #getting filename without extension
        fileName_without_ext = fileName[:fileName.rindex('.')]
        #putting the filename into the list
        fingerPrintWithHDforRobustness.append("f_"+fileName_without_ext)
        match hashTechnique:
            case "average_hash":
                #computing hash values using average hash
                ahash1 = imagehash.average_hash(Image.open(filepath))
                ahash2 = imagehash.average_hash(Image.open(input_filepath2))
                HammingDistanceListforRobustness.append(ahash1-ahash2)
                #putting the hamming distance into the list
                fingerPrintWithHDforRobustness.append(ahash1-ahash2)
            case "phash":
                #computing hash values using dct-based hash
                phash1 = imagehash.phash(Image.open(filepath))
                phash2 = imagehash.phash(Image.open(input_filepath2))
                HammingDistanceListforRobustness.append(phash1-phash2)
                #putting the hamming distance into the list
                fingerPrintWithHDforRobustness.append(phash1-phash2)
            case "dhash":
                #computing hash values using difference hash
                dhash1 = imagehash.dhash(Image.open(filepath))
                dhash2 = imagehash.dhash(Image.open(input_filepath2))
                HammingDistanceListforRobustness.append(dhash1-dhash2)
                #putting the hamming distance into the list
                fingerPrintWithHDforRobustness.append(dhash1-dhash2)
            case "whash":
                #computing hash values using dwt-based hash
                whash1 = imagehash.whash(Image.open(filepath))
                whash2 = imagehash.whash(Image.open(input_filepath2))
                HammingDistanceListforRobustness.append(whash1-whash2)
                #putting the hamming distance into the list
                fingerPrintWithHDforRobustness.append(whash1-whash2)
            case _:
                print("Please input correct hash technique listed")
        #appending list to form list of lists
        fingerPrintWithHDListforRobustness.append(fingerPrintWithHDforRobustness)
        
    RDict = {}
    for threshold in thresholdList:
        numberOfFPs = tableforRobustness(HammingDistanceListforRobustness, threshold)
        #add threshold and x to dictionary
        RDict[threshold] = round(numberOfFPs,4)
    output_loc = input("Please enter the csv file path for robustness output:")
    #writing into csv file   
    with open(output_loc, 'w', newline="") as f1:
        writer = csv.writer(f1)
        writer.writerow(header)
        writer.writerows(fingerPrintWithHDListforRobustness)
        
    return RDict

def tableforRobustness(HammingDistanceListforRobustness,  threshold):
    count = 0
    for i in HammingDistanceListforRobustness:
        if i <= threshold:
            count+=1
    return count/len(HammingDistanceListforRobustness)


def hashTechniquesForDP(hashTechnique, input_filepath1,output_loc, thresholdList):
    fingerPrintWithHDListforDP = []#list of lists
    HammingDistanceListforDP = []
    header = ['F_id1', 'F_id2', 'Hamming Distance']
    for i in range (0, len(input_filepath1)):
        #getting filename without extension
        #l = filepath1.split('/')
        l = input_filepath1[i].split('/')
        fileName1 = l[-1]
        fileName_without_ext = fileName1[:fileName1.rindex('.')]
        F_id1 = "f_"+ fileName_without_ext  
        for j in range (i+1, len(input_filepath1)):
            l1 = input_filepath1[j].split('/')
            fileName2 = l1[-1]
            fileName_without_ext = fileName2[:fileName2.rindex('.')]
            F_id2 = "f_"+ fileName_without_ext
            fingerPrintWithHDforDP = []
            fingerPrintWithHDforDP.append(F_id1)
            #putting the filename into the list
            fingerPrintWithHDforDP.append(F_id2)    
            match hashTechnique:
                case "average_hash":
                    #computing hash values using average hash
                    ahash1 = imagehash.average_hash(Image.open(input_filepath1[i]))
                    ahash2 = imagehash.average_hash(Image.open(input_filepath1[j]))
                    HammingDistanceListforDP.append(ahash1-ahash2)
                    #putting the hamming distance into the list
                    fingerPrintWithHDforDP.append(ahash1-ahash2)    
                case "phash":
                    #computing hash values using dct-based hash
                    phash1 = imagehash.phash(Image.open(input_filepath1[i]))
                    phash2 = imagehash.phash(Image.open(input_filepath1[j]))
                    HammingDistanceListforDP.append(phash1-phash2)
                    #putting the hamming distance into the list
                    fingerPrintWithHDforDP.append(phash1-phash2)
                case "dhash":
                    #computing hash values using difference hash
                    dhash1 = imagehash.dhash(Image.open(input_filepath1[i]))
                    dhash2 = imagehash.dhash(Image.open(input_filepath1[j]))
                    HammingDistanceListforDP.append(dhash1-dhash2)
                    #putting the hamming distance into the list
                    fingerPrintWithHDforDP.append(dhash1-dhash2)
                case "whash":
                    #computing hash values using dwt-based hash
                    whash1 = imagehash.whash(Image.open(input_filepath1[i]))
                    whash2 = imagehash.whash(Image.open(input_filepath1[j]))
                    HammingDistanceListforDP.append(whash1-whash2)
                    #putting the hamming distance into the list
                    fingerPrintWithHDforDP.append(whash1-whash2)                    
                case _:
                    print("Please input correct hash technique")
            fingerPrintWithHDListforDP.append(fingerPrintWithHDforDP)
    
    Dict = {}
    for threshold in thresholdList:
        numberOfFPs = tableforDP(HammingDistanceListforDP,threshold)
        #add threshold and x to dictionary
        Dict[threshold] = round(numberOfFPs,4)   
    #writing into csv file   
    with open(output_loc, 'w', newline="") as f2:
        writer = csv.writer(f2)
        writer.writerow(header)
        writer.writerows(fingerPrintWithHDListforDP)
        
    return Dict

def tableforDP(HammingDistanceListforDP,  threshold):
    count = 0
    for i in HammingDistanceListforDP:
        if i >= threshold:
            count+=1
    return count/len(HammingDistanceListforDP)

    
if __name__ == "__main__":
    thresholdList = [3, 6, 9, 12, 15, 18, 21, 24, 27]
    input_dir1 = input("Please provide the path to the extracted normal fingerprints folder: ")
    input_filepath1 = []
    dirs = os.listdir(input_dir1)
    for file in dirs:
        if file.endswith(".jpg"):
            input_filepath1.append(input_dir1 + file)
    input_dir2 = input("Please provide the path to the extracted distorted fingerprints folder: ")
    #hashTechnique = input("Please input which hash technique you would like to work with(average_hash or phash or dhash or whash):")
    hashTechniques = ['average_hash', 'phash', 'dhash', 'whash']
    hRDict = {}
    hDict = {}
    for hashTechnique in hashTechniques:
        RDict = {}
        Dict = {}
        #robustness
        RDict = hashTechniquesForRobustness(hashTechnique, input_filepath1, input_dir2, thresholdList)
        hRDict[hashTechnique] = RDict
        #discriminationProbablity
        output_location_for_DP = input("Please enter the csv file path for discrimination probablity output:")
        Dict = hashTechniquesForDP(hashTechnique, input_filepath1,output_location_for_DP, thresholdList)
        hDict[hashTechnique] = Dict

    


'''
Dictionary of dictionaries for robustness - hRDict
dict_keys(['average_hash', 'phash', 'dhash', 'whash'])
dict_values([{3: 0.1187, 6: 0.4125, 9: 0.7031, 12: 0.8906, 15: 0.9656, 18: 1.0, 21: 1.0, 24: 1.0, 27: 1.0},
             {3: 0.0, 6: 0.0063, 9: 0.0094, 12: 0.0563, 15: 0.1, 18: 0.2125, 21: 0.2812, 24: 0.4281, 27: 0.5188},
             {3: 0.0219, 6: 0.125, 9: 0.3375, 12: 0.625, 15: 0.8219, 18: 0.8969, 21: 0.95, 24: 0.9875, 27: 0.9938},
             {3: 0.0625, 6: 0.2281, 9: 0.4875, 12: 0.7156, 15: 0.8438, 18: 0.9281, 21: 0.9781, 24: 0.9938, 27: 1.0}])
'''

'''
Dictionary of dictionaries for DP - Dict
dict_keys([3, 6, 9, 12, 15, 18, 21, 24, 27])
dict_keys(['average_hash', 'phash', 'dhash', 'whash'])
dict_values([{3: 0.9499, 6: 0.7129, 9: 0.3727, 12: 0.1333, 15: 0.0402, 18: 0.0122, 21: 0.0049, 24: 0.0016, 27: 0.0002},
             {3: 0.9998, 6: 0.9992, 9: 0.9923, 12: 0.9831, 15: 0.9403, 18: 0.9043, 21: 0.7966, 24: 0.7172, 27: 0.5109},
             {3: 0.9964, 6: 0.9639, 9: 0.8407, 12: 0.6204, 15: 0.3861, 18: 0.1953, 21: 0.0796, 24: 0.0242, 27: 0.0044},
             {3: 0.9527, 6: 0.7824, 9: 0.5362, 12: 0.3106, 15: 0.1525, 18: 0.0734, 21: 0.0332, 24: 0.0128, 27: 0.0051}])
'''






