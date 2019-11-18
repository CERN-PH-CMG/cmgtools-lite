from __future__ import division 
import ROOT
import numpy as np
from root_numpy import root2array, tree2array

## open the files and get the tree. Make sure of the path!
## ------------------------------------------------------
f = ROOT.TFile.Open("/home/ucl/cp3/elfaham/CMSSW_10_4_0/src/CMGTools/TTHAnalysis/macros/diff/TTHnobb_fxfx_Friend.root")
t = f.Get("Friends")
## select branches and apply selection: only events of which visible pT is constructed
## -----------------------------------------------------------------------------------
array1 = tree2array(t, branches=['Hreco_pTHvis'], selection ='Hreco_pTHvis >= 0 ')
array2 = tree2array(t, branches=['Hreco_pTHgen'], selection ='Hreco_pTHvis >= 0 ')
array3 = tree2array(t, branches=['Hreco_pTHvis'], selection ='Hreco_pTHvis < 0  ')
array4 = tree2array(t, branches=['Hreco_matchedpartons'], selection ='Hreco_matchedpartons == 1 ')
array5 = tree2array(t, branches=['Hreco_matchedpartons'], selection ='Hreco_matchedpartons == 2 ')
array6 = tree2array(t, branches=['Hreco_matchedpartons'], selection ='Hreco_matchedpartons >= 0 ')

print ("length of vis array              = " + str(len(array1))) 
#print ("length of gen array              = " + str(len(array2))) 
print ("length of unvis array            = " + str(len(array3)))
print ("length of 1 matchedpartons       = " + str(len(array4)))
print ("length of 2 matchedpartons       = " + str(len(array5)))
print ("length of 1 or 2  matchedpartons = " + str(len(array6)))

a = len(array1)
b = len(array3)
d = len(array4)
e = len(array5)
f = len(array6)

c = (a/(a+b))*100
c_1 = (d/f)*100
c_2 = (e/f)*100

print ("fraction of reconstruced events is " + str(c) + "% of the total number of events")
print ("fraction of reconstructed events in which one parton is matched to a jet " + str(c_1) + "% of the total number of reconstructed events")
print ("fraction of reconstructed events in which two partons are matched to two jets " + str(c_2) + "% of the total number of reconstructed events")

## set the arrays to float type
## ----------------------------
X = np.asarray(array1 ,float)
Y = np.asarray(array2 ,float)

print ("corr of vis with gen = "   + str(np.corrcoef(X,Y)[0,1]))
#print ("corr of vis with itself    = "+ str(np.corrcoef(X)))
#print ("corr of gen with itself    = "+ str(np.corrcoef(Y)))

## print the pearson corrleation
## -----------------------------
from scipy.stats import pearsonr
print ("Pearson corr of vis with gen = " + str(pearsonr(X,Y)))

## scatter plot of both arrays
## ---------------------------
import matplotlib.pyplot as plt
#plt.scatter(X,Y)
#plt.xlabel('vis')
#plt.ylabel('gen')
#plt.show()

## method to produce two randomly generated datasets with a prechosen correlation
## check http://www.uvm.edu/~dhowell/StatPages/More_Stuff/CorrGen.html
## pre-determined coeff. to reproduce
## ------------------------------------------------------------------------------
from math import sqrt
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
