# Import dependencies
import csv,sys
import pandas as pd
from hexhamming import hamming_distance_string

def calculateHammingDistance(hash1, hash2):
    HammingDistance = hamming_distance_string(hash1,hash2)
    return HammingDistance
        
if __name__ == "__main__":
    hash1_csvfilepath = sys.argv[1]
    hash2_csvfilepath = sys.argv[2]
    output_location_for_Robustness = sys.argv[3]
    output_location_for_Discrimination = sys.argv[4]
    RobustnessHeader = ['F_id', 'Hamming Distance']
    DiscriminationHeader = ['F_id1', 'F_id2','Hamming Distance']
    with open(hash1_csvfilepath, 'r') as f1, open(hash2_csvfilepath, 'r') as f2:
        hash1_readerDf = pd.read_csv(f1)
        hash2_readerDf = pd.read_csv(f2)
    HammingDistanceForRobustnessDict = {}
    for i in range(len(hash1_readerDf)): 
        HammingDistanceForRobustness = calculateHammingDistance(hash1_readerDf.loc[i,"Hash"],hash2_readerDf.loc[i,"Hash"])
        HammingDistanceForRobustnessDict[hash1_readerDf.loc[i,"F_id"]] = HammingDistanceForRobustness
    with open(output_location_for_Robustness, 'w') as f3:
        w = csv.writer(f3)
        w.writerow(RobustnessHeader)
        w.writerows(HammingDistanceForRobustnessDict.items())
    with open(hash1_csvfilepath, 'r') as f:
        hash_readerDf = pd.read_csv(f)
    HammingDistanceForDiscriminationList = []
    for i in range(len(hash_readerDf)):
        for j in range(i+1, len(hash_readerDf)):
            hdlist = []
            hdlist.append(hash_readerDf.loc[i,"F_id"])
            HammingDistanceForDiscrimination = calculateHammingDistance(hash_readerDf.loc[i,"Hash"],hash_readerDf.loc[j,"Hash"])
            hdlist.append(hash_readerDf.loc[j,"F_id"])
            hdlist.append(HammingDistanceForDiscrimination)
            HammingDistanceForDiscriminationList.append(hdlist)   
    with open(output_location_for_Discrimination, 'w') as f4:
        w = csv.writer(f4)
        w.writerow(DiscriminationHeader)
        w.writerows(HammingDistanceForDiscriminationList)
       

