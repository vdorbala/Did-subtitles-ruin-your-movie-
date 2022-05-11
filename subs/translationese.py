import pandas as pd
import os
import math
def getinfo(formats,movie):
    type1 = formats[0]
    type2 = formats[1]
    fldr1 = type1+"-stats"
    fldr2 = type2+"-stats"
    file1 = movie+"-stats-"+type1+".csv"
    file2 = movie+"-stats-"+type2+".csv"
    path1 = os.path.join(type1,fldr1,file1)
    path2 = str (os.path.join(type2,fldr2,file2))
    df1 = pd.read_csv(path1,header = None)
    df2 = pd.read_csv(path2,header = None)
    
    df = pd.DataFrame()
    df["ttrdiff"]=  (df1[1]-df2[1]).abs()
    df["hardendiff"] = (df1[2]-df2[2]).abs()
    ttr = df["ttrdiff"].max()
    harden = df["hardendiff"].max()
    # print(ttr,harden)
    return ttr,harden
    
# getinfo(["fr",'en'],"Adam")