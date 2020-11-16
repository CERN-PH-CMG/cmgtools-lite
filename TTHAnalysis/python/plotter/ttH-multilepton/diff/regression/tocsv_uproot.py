import os
import numpy as np
import pandas as pd
import uproot



import argparse
import ROOT

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--idir',      help='Folder to convert to csv', default='./temp')
args = parser.parse_args()




mydir = args.idir

for f in os.listdir(mydir):
    print('Converting ', f)
    fileIn = f
    fileOut = f
    treename = 'Friends'
    print "Reading tree {} in file {}".format(treename, fileIn)
    data = uproot.open("%s/%s"%(mydir,fileIn))[treename]

    names = data.keys()

    print ("Tree has the following branches:")
    print ("  [{}]".format(', '.join(names)))

    #data.arrays(names)
    dfObj = data.pandas.df()
    #dfObj = pd.DataFrame.from_dict(data.arrays(names))
    outfilename = fileOut.replace('.root', '.csv')
    dfObj.to_csv("%s/%s"%(mydir,outfilename))
    




