import sys
import matplotlib.pylab as plt
import pandas as pd
from scipy.integrate import simpson

if __name__ == "__main__":
    Robustness_csvfilepath = sys.argv[1]
    Discrimination_csvfilepath = sys.argv[2]
    with open(Robustness_csvfilepath, 'r') as f1, open(Discrimination_csvfilepath, 'r') as f2:
        Robustness_readerDf = pd.read_csv(f1)
        Discrimination_readerDf = pd.read_csv(f2)
    print(Robustness_readerDf)
    print(Discrimination_readerDf)
    plt.rcParams["figure.figsize"] = [7.00, 3.50]
    plt.rcParams["figure.autolayout"] = True
    Robustness_readerDf.columns = ["Threshold","Robustness"]
    Discrimination_readerDf.columns = ["Threshold","Discrimination Capability"]
    fig, ax = plt.subplots()
    ax2 = ax.twinx()
    ax.set_xlabel("Threshold")
    ax.set_ylabel("Robustness")
    ax2.set_ylabel("Discrimination Capability")
    Robustness_readerDf.plot(x="Threshold", y="Robustness", ax=ax, color='Black', style='+-')
    Discrimination_readerDf.plot(x="Threshold",y="Discrimination Capability", ax=ax2, title='Robusness and Discrimination Capability interaction',color='Black', style='.--')
    # plt.show()
    Robustness_readerDf.index.name = 'Threshold'
    Discrimination_readerDf.index.name = 'Threshold'
    df3 = pd.merge(Robustness_readerDf, Discrimination_readerDf, left_index=True, right_index=True)
    # print(df3.head())
    ax2.set_xlabel("Robustness")
    ax2.set_ylabel("Discrimination Capability")
    df3.plot(x = 'Robustness', y = 'Discrimination Capability', title='Robustness and Discrimination Capability correlation', color='Black', style='+-')
    # plt.show()

    #area calculation
    y = df3['Discrimination Capability']
    area = simpson(y, dx=0.2)
    print("area =", area)
