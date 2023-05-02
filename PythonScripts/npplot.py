import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import LineString
import sys

if __name__ == "__main__":
    Robustness_csvfilepath = sys.argv[1]
    Discrimination_csvfilepath = sys.argv[2]
    with open(Robustness_csvfilepath, 'r') as f1, open(Discrimination_csvfilepath, 'r') as f2:
        Robustness_readerDf = pd.read_csv(f1)
        Discrimination_readerDf = pd.read_csv(f2)
    
    Robustness = Robustness_readerDf['Robustness']
    Discrimination = Discrimination_readerDf['Discrimination Capability']
    Threshold = Discrimination_readerDf['Threshold']

    line1 = LineString(np.column_stack((Robustness, Threshold)))
    line2 = LineString(np.column_stack((Discrimination, Threshold)))
    intersection1 = line1.intersection(line2)

    plt.plot(*intersection1.xy,'ro')
    plt.show()