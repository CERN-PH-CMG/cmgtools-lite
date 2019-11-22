from __future__ import division 
import ROOT
import numpy as np
from root_numpy import root2array, tree2array

from optparse import OptionParser
parser = OptionParser(usage="%prog [options]")
# common options, independent of the flavour chosen
parser.add_option("-i", "--inputFile", dest="inputFile",  type="string", default="./skimmedTrees_16/2lss_diff_NoTop-tagged/TTHnobb_fxfx_Friend.root", help="Friend tree with the needed information");
(options, args) = parser.parse_args()

## open the files and get the tree. Make sure of the path!
## ------------------------------------------------------
f = ROOT.TFile.Open(options.inputFile)
if not f:
    raise ValueError('File not opened')
t = f.Get("Friends")
if not t:
    raise ValueError('Tree not loaded')
## select branches and apply selection: only events of which visible pT is constructed
## -----------------------------------------------------------------------------------
hreco_pthvis = tree2array(t, branches=['Hreco_pTHvis'], selection ='Hreco_pTHvis >= 0 ')
hreco_pthgen = tree2array(t, branches=['Hreco_pTHgen'], selection ='Hreco_pTHvis >= 0 ')
hreco_pthvis_recoFail = tree2array(t, branches=['Hreco_pTHvis'], selection ='Hreco_pTHvis < 0  ')
hreco_onematchedparton = tree2array(t, branches=['Hreco_matchedpartons'], selection ='Hreco_matchedpartons == 1 ')
hreco_twomatchedpartons = tree2array(t, branches=['Hreco_matchedpartons'], selection ='Hreco_matchedpartons == 2 ')
hreco_nmatchedpartonsall = tree2array(t, branches=['Hreco_matchedpartons'], selection ='Hreco_matchedpartons >= 0 ')

print ("length of vis array              = " + str(len(hreco_pthvis))) 
#print ("length of gen array              = " + str(len(hreco_pthgen))) 
print ("length of unvis array            = " + str(len(hreco_pthvis_recoFail)))
print ("length of 1 matchedpartons       = " + str(len(hreco_onematchedparton)))
print ("length of 2 matchedpartons       = " + str(len(hreco_twomatchedpartons)))
print ("length of 1 or 2  matchedpartons = " + str(len(hreco_nmatchedpartonsall)))

n_hreco_pthvis = len(hreco_pthvis)
n_hreco_pthvis_recoFail = len(hreco_pthvis_recoFail)
n_hreco_onematchedparton = len(hreco_onematchedparton)
n_hreco_twomatchedpartons = len(hreco_twomatchedpartons)
n_hreco_matchedpartonsall = len(hreco_nmatchedpartonsall)

fraction_pthvis_is_reconstructed = (n_hreco_pthvis/(n_hreco_pthvis+n_hreco_pthvis_recoFail))*100
fraction_onematchedparton = (n_hreco_onematchedparton/n_hreco_matchedpartonsall)*100
fraction_twomatchedpartons = (n_hreco_twomatchedpartons/n_hreco_matchedpartonsall)*100

print ("fraction of reconstruced events is " + str(fraction_pthvis_is_reconstructed) + "% of the total number of events")
print ("fraction of reconstructed events in which one parton is matched to a jet " + str(fraction_onematchedparton) + "% of the total number of reconstructed events")
print ("fraction of reconstructed events in which two partons are matched to two jets " + str(fraction_twomatchedpartons) + "% of the total number of reconstructed events")

## set the arrays to float type
## ----------------------------
X = np.asarray(hreco_pthvis ,float)
Y = np.asarray(hreco_pthgen ,float)

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
