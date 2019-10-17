from __future__ import division 
import ROOT
import numpy as np
from root_numpy import root2array, tree2array

## open the files and get the tree
## -------------------------------
f = ROOT.TFile.Open("./2016_no_top_tagger_new/TTHnobb_pow_Friend.root")
#f = ROOT.TFile.Open("./TTHnobb_pow_Friend.root")
#f = ROOT.TFile.Open("./2017/evVarFriend_TTH_amc_2017.root")
#f = ROOT.TFile.Open("./2018/evVarFriend_TTH_amc_2018.root")
t = f.Get("Friends")

## select branches and apply selection: only events of which visible pT is constructed
## -----------------------------------------------------------------------------------
array1 = tree2array(t, branches=['Hreco_pTHvis'], selection ='Hreco_pTHvis >= 0 ')
array2 = tree2array(t, branches=['Hreco_pTHgen'], selection ='Hreco_pTHvis >= 0 ')
array3 = tree2array(t, branches=['Hreco_pTHvis'], selection ='Hreco_pTHvis < 0  ')


print ("length of vis array   = "   + str(len(array1))) 
print ("length of gen array   = "   + str(len(array2))) 
print ("length of unvis array = "   + str(len(array3)))
a = len(array1)
b = len(array3)
c = (a/(a+b))*100
#/(len(array1)+len(array3))
print ("fraction of reconstruced events is " + str(c) + "% of the total number of events")
## set the arrays to float type
## ----------------------------
X = np.asarray(array1 ,float)
Y = np.asarray(array2 ,float)

print ("corr of vis with gen = "   + str(np.corrcoef(X,Y)[0,1]))
#print ("corr of vis with itself    = "+ str(np.corrcoef(X)))
#print ("corr of gen with itself    = "+ str(np.corrcoef(Y)))

from scipy.stats import pearsonr

## print the pearson corrleation
## -----------------------------
print ("Pearson corr of vis with gen = " + str(pearsonr(X,Y)))

import matplotlib.pyplot as plt

## scatter plot of both arrays
## ---------------------------
#plt.scatter(X,Y)
#plt.xlabel('vis')
#plt.ylabel('gen')
#plt.show()

## method to produce two randomly generated datasets with a prechosen correlation
## check http://www.uvm.edu/~dhowell/StatPages/More_Stuff/CorrGen.html
## ------------------------------------------------------------------------------

from math import sqrt
## pre-determined coeff. to reproduce
## ----------------------------------
#r = 0.6
#a  = r/sqrt(1-(r*r))
## randomly generated datasets
## ---------------------------
#r1 = np.random.normal(0,1,500)
#D  = np.asarray(r1, float)

#r2 = np.random.normal(0,1,500)
#E  = np.asarray(r2, float)

#r3 = (a*D)+E
#F  = np.asarray(r3, float)

## this coeff should be similar to r
## ---------------------------------
#print np.corrcoef(D,F)[0,1]







