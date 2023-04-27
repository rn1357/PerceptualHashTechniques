# Import dependencies
from PIL import Image
import imagehash
import csv,os,sys
import matplotlib.pylab as plt
import pandas as pd


def hashTechniquesForRobustness(hashTechnique, input_filepath1, input_dir2, thresholdList, output_location_for_robustness):
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
    #writing into csv file   
    with open(output_location_for_robustness, 'w', newline="") as f1:
        writer = csv.writer(f1)
        writer.writerow(header)
        writer.writerows(fingerPrintWithHDListforRobustness)
            
    RobustnessDict = {}
    for threshold in thresholdList:
        numberOfFPs = tableforRobustness(HammingDistanceListforRobustness, threshold)
        #add threshold and x to dictionary
        RobustnessDict[threshold] = round(numberOfFPs,4)
    return RobustnessDict

def tableforRobustness(HammingDistanceListforRobustness,  threshold):
    count = 0
    for i in HammingDistanceListforRobustness:
        if i <= threshold:
            count+=1
    return count/len(HammingDistanceListforRobustness)


def hashTechniquesForDiscrimination(hashTechnique, input_filepath1, output_location_for_Discrimination, thresholdList):
    fingerPrintWithHDListforDiscrimination = []#list of lists
    HammingDistanceListforDiscrimination = []
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
            fingerPrintWithHDforDiscrimination = []
            fingerPrintWithHDforDiscrimination.append(F_id1)
            #putting the filename into the list
            fingerPrintWithHDforDiscrimination.append(F_id2)    
            match hashTechnique:
                case "average_hash":
                    #computing hash values using average hash
                    ahash1 = imagehash.average_hash(Image.open(input_filepath1[i]))
                    ahash2 = imagehash.average_hash(Image.open(input_filepath1[j]))
                    
                    
                    HammingDistanceListforDiscrimination.append(ahash1-ahash2)
                    #putting the hamming distance into the list
                    fingerPrintWithHDforDiscrimination.append(ahash1-ahash2)    
                case "phash":
                    #computing hash values using dct-based hash
                    phash1 = imagehash.phash(Image.open(input_filepath1[i]))
                    phash2 = imagehash.phash(Image.open(input_filepath1[j]))
                    HammingDistanceListforDiscrimination.append(phash1-phash2)
                    #putting the hamming distance into the list
                    fingerPrintWithHDforDiscrimination.append(phash1-phash2)
                case "dhash":
                    #computing hash values using difference hash
                    dhash1 = imagehash.dhash(Image.open(input_filepath1[i]))
                    dhash2 = imagehash.dhash(Image.open(input_filepath1[j]))
                    HammingDistanceListforDiscrimination.append(dhash1-dhash2)
                    #putting the hamming distance into the list
                    fingerPrintWithHDforDiscrimination.append(dhash1-dhash2)
                case "whash":
                    #computing hash values using dwt-based hash
                    whash1 = imagehash.whash(Image.open(input_filepath1[i]))
                    whash2 = imagehash.whash(Image.open(input_filepath1[j]))
                    HammingDistanceListforDiscrimination.append(whash1-whash2)
                    #putting the hamming distance into the list
                    fingerPrintWithHDforDiscrimination.append(whash1-whash2)                    
                case _:
                    print("Please input correct hash technique")
            fingerPrintWithHDListforDiscrimination.append(fingerPrintWithHDforDiscrimination)
    #writing into csv file   
    with open(output_location_for_Discrimination, 'w', newline="") as f2:
        writer = csv.writer(f2)
        writer.writerow(header)
        writer.writerows(fingerPrintWithHDListforDiscrimination)
        
    Dict = {}
    for threshold in thresholdList:
        numberOfFPs = tableforDiscrimination(HammingDistanceListforDiscrimination,threshold)
        #add threshold and x to dictionary
        Dict[threshold] = round(numberOfFPs,4)   
    return Dict

def tableforDiscrimination(HammingDistanceListforDiscrimination,  threshold):
    count = 0
    for i in HammingDistanceListforDiscrimination:
        if i >= threshold:
            count+=1
    return count/len(HammingDistanceListforDiscrimination)

    
if __name__ == "__main__":
    RobustnessDict = {}
    Dict = {}  
    hashTechnique = sys.argv[1]
    thresholdList = [3,6,9,12,15,18,21,24,27,30,33,36]
    input_dir1 = sys.argv[2]
    input_filepath1 = []
    dirs = os.listdir(input_dir1)
    for file in dirs:
        if file.endswith(".jpg"):
            input_filepath1.append(os.path.join(input_dir1, file))
    input_dir2 = sys.argv[3]
    #robustness
    output_location_for_robustness = sys.argv[4]
    RobustnessDict = hashTechniquesForRobustness(hashTechnique, input_filepath1, input_dir2, thresholdList, output_location_for_robustness)
    #discriminationProbablity
    output_location_for_Discrimination = sys.argv[5]
    Dict = hashTechniquesForDiscrimination(hashTechnique, input_filepath1,output_location_for_Discrimination, thresholdList)

    
    plt.rcParams["figure.figsize"] = [7.00, 3.50]
    plt.rcParams["figure.autolayout"] = True

    df1 = pd.DataFrame.from_dict(RobustnessDict, orient='index')
    df2 = pd.DataFrame.from_dict(Dict, orient='index')
    df1.columns = ["Robustness"]
    df2.columns = ["Discrimination Capability"]
    fig, ax = plt.subplots()
    ax2 = ax.twinx()
    ax.set_xlabel("Threshold")
    ax.set_ylabel("Robustness")
    ax2.set_ylabel("Discrimination Capability")
    df1.plot(y=["Robustness"], ax=ax, color='Black', style='+-')
    df2.plot(y=["Discrimination Capability"], ax=ax2, title='Robusness and Discrimination Capability interaction',color='Black', style='.--')
    plt.show()
    df1.index.name = 'Threshold'
    df2.index.name = 'Threshold'
    df3 = pd.merge(df1, df2, left_index=True, right_index=True)
    ax2.set_xlabel("Robustness")
    ax2.set_ylabel("Discrimination Capability")
    df3.plot(x = 'Robustness', y = 'Discrimination Capability', title='Robustness and Discrimination Capability correlation', color='Black', style='+-')
    plt.show()
