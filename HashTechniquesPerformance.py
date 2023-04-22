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
    thresholdList = [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33,36]
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
    average_hash_Rdict = hRDict['average_hash']
    phash_Rdict = hRDict['phash']
    dhash_Rdict = hRDict['dhash']
    whash_Rdict = hRDict['whash']
    
    average_hash_dict = hDict['average_hash']
    phash_dict = hDict['phash']
    dhash_dict = hDict['dhash']
    whash_dict = hDict['whash']

    plt.rcParams["figure.figsize"] = [7.00, 3.50]
    plt.rcParams["figure.autolayout"] = True

    df1 = pd.DataFrame.from_dict(average_hash_Rdict, orient='index')
    df2 = pd.DataFrame.from_dict(phash_Rdict, orient='index')
    df3 = pd.DataFrame.from_dict(dhash_Rdict, orient='index')
    df4 = pd.DataFrame.from_dict(whash_Rdict, orient='index')

    df5 = pd.DataFrame.from_dict(average_hash_dict, orient='index')
    df6 = pd.DataFrame.from_dict(phash_dict, orient='index')
    df7 = pd.DataFrame.from_dict(dhash_dict, orient='index')
    df8 = pd.DataFrame.from_dict(whash_dict, orient='index')

    df1.columns = ["aRobustness"]
    df2.columns = ["pRobustness"]
    df3.columns = ["dRobustness"]
    df4.columns = ["wRobustness"]

    df5.columns = ["aDP"]
    df6.columns = ["pDP"]
    df7.columns = ["dDP"]
    df8.columns = ["wDP"]



    df1.index.name = 'Threshold'
    df2.index.name = 'Threshold'
    df3.index.name = 'Threshold'
    df4.index.name = 'Threshold'
    df5.index.name = 'Threshold'
    df6.index.name = 'Threshold'
    df7.index.name = 'Threshold'
    df8.index.name = 'Threshold'
    df11 = df1.join(df2)
    df12 = df3.join(df4)
    df13 = df5.join(df6)
    df14 = df7.join(df8)
    dfr1 = df11.join(df12)
    dfd1 = df13.join(df14)

    fig, ax = plt.subplots()
    ax2 = ax.twinx()
    ax.set_xlabel("Threshold")
    ax.set_ylabel("Probablity(similar)")
    ax2.set_ylabel("Probablity(dissimilar)")
    dfr1.plot(y=["aRobustness","pRobustness", "dRobustness","wRobustness" ], ax=ax)
    dfd1.plot(y=['aDP', 'pDP',"dDP","wDP"], ax=ax2, title='Robusness and Discrimination probablity interaction',ls="--")
    plt.show()





