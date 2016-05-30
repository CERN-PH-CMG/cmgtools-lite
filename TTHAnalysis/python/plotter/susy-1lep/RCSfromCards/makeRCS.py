#!/usr/bin/env python
#Script to read data cards and turn them either into a table that can be copied to Excel/OpenOffice
#1;2cor print out in latex format.

import shutil
import subprocess
import os
import sys
import glob
from multiprocessing import Pool
from ROOT import *
import math

def _getYieldsFromInput(inargs):

    (sample, cardDir, binName, ratDict) = inargs

    if len(inargs) < 1:
        return (binName,[0,0])

    cardName = cardDir+"/common/CnC2015X_"+binName+".input.root"

    #print "# Starting Bin:", binName

    cardf = TFile(cardName,"READ")

    hTT_DiLep = cardf.Get("x_TT_DiLep")
    nTT_DiLep = hTT_DiLep.Integral()
    nTTErr_DiLep = hTT_DiLep.GetBinError(1)
                             
    hTT_SemiLep = cardf.Get("x_TT_SemiLep")
    nTT_SemiLep = hTT_SemiLep.Integral()
    nTTErr_SemiLep = hTT_SemiLep.GetBinError(1)

    hTT_FullHad = cardf.Get("x_TT_FullHad")
    nTT_FullHad = hTT_FullHad.Integral()
    nTTErr_FullHad = hTT_FullHad.GetBinError(1)

    nTT_SemiLep=nTT_SemiLep+nTT_FullHad
    nTTErr_SemiLep = math.sqrt(nTTErr_SemiLep*nTTErr_SemiLep + nTTErr_FullHad*nTTErr_FullHad)

    nTT = nTT_SemiLep + nTT_DiLep
    nTTErr = math.sqrt(nTTErr_SemiLep*nTTErr_SemiLep + nTTErr_DiLep*nTTErr_DiLep)

    hSingleT = cardf.Get("x_SingleT")
    nSingleT = hSingleT.Integral()
    nSingleTErr = hSingleT.GetBinError(1)

    hTTV = cardf.Get("x_TTV")
    nTTV = hTTV.Integral()
    nTTVErr = hTTV.GetBinError(1)

    hWJets = cardf.Get("x_WJets")
    nWJets = hWJets.Integral()
    nWJetsErr = hWJets.GetBinError(1)

    hQCD = cardf.Get("x_QCD")
    nQCD = hQCD.Integral()
    nQCDErr = hQCD.GetBinError(1)

    hDY = cardf.Get("x_DY")
    nDY = hDY.Integral()
    nDYErr = hDY.GetBinError(1)

    cardf.Close()

    binName=binName.replace('CR','')
    binName=binName.replace('SR','')

    return (binName,[nTT, nTTErr, nTT_SemiLep, nTTErr_SemiLep, nTT_DiLep, nTTErr_DiLep, nTT_FullHad, nTTErr_FullHad,nSingleT, nSingleTErr, nTTV, nTTVErr, nWJets,  nWJetsErr, nQCD, nQCDErr, nDY, nDYErr])

def makeTable(yieldDict, yieldDict2, format = "text", option = "CRSR"):

    # sort by bin name
    ykeys = sorted(yieldDict.keys())
    #print 'KEYS', sorted(ykeys)

    if format == "text":

        # Print yields
        print 80*'#'
        print "Yields with zero selected"
        print "Bin: | TT | SingleT | TTV | WJets | QCD | DY | allbkg | sig"

        for bin in ykeys:#yieldDict:

            (nTT, nTTErr, nTT_SemiLep, nTTErr_SemiLep, nTT_DiLep, nTTErr_DiLep, nTT_FullHad, nTTErr_FullHad, nSingleT, nSingleTErr, nTTV, nTTVErr, nWJets,  nWJetsErr, nQCD, nQCDErr, nDY, nDYErr) = yieldDict[bin]
            (nTT2, nTTErr2, nTT_SemiLep2, nTTErr_SemiLep2, nTT_DiLep2, nTTErr_DiLep2, nTT_FullHad2, nTTErr_FullHad2, nSingleT2, nSingleTErr2, nTTV2, nTTVErr2, nWJets2,  nWJetsErr2, nQCD2, nQCDErr2, nDY2, nDYErr2) = yieldDict2[bin]
            
            allbkg = nTT + nSingleT + nTTV + nWJets + nQCD + nDY
            if allbkg > 0.5:
                print "%s:|%2.2f +/- %2.2f|%2.2f +/- %2.2f|%2.2f +/- %2.2f|%2.2f +/- %2.2f|%2.2f +/- %2.2f|%2.2f +/- %2.2f " % ( bin, nTT, nTTErr, nSingleT, nSingleTErr, nTTV, nTTVErr, nWJets,  nWJetsErr, nQCD, nQCDErr, nDY, nDYErr , allbkg1)
            else:
                print "%s:|%2.2f +/- %2.2f|%2.2f +/- %2.2f|%2.2f +/- %2.2f|%2.2f +/- %2.2f|%2.2f +/- %2.2f|%2.2f +/- %2.2f  COMBINE" % ( bin, nTT, nTTErr, nSingleT, nSingleTErr, nTTV, nTTVErr, nWJets,  nWJetsErr, nQCD, nQCDErr, nDY, nDYErr , allbkg)
#                print bin, "| | | | | | | %2.2f | %2.2f +/- %2.2f " % (allbkg, nSig,nSigErr)

    if format == "latex":
        print '%',80*'#'
        print '%Going to print out LaTeX tables'
        print '%',80*'#'

        nColumns = 11
        if option == "ratio":
            nColumns = 16
        if option == "CRSR":
            nColumns = 12

        print "\\begin{table}[!hbtp]"
        print "\\begin{center}"
        print "\\scriptsize"
        print "\\caption{}"
#        print "\\caption{Expected event yields for search bins as defined in Table~\\ref{tab:1b_sigreg_3fb}. The \\DF is adjusted for each \\ST bin.}"
        print "\\label{tab:qcdYieldsHTbin}"
        print "\\begin{tabular}{|l|"+(nColumns-1)*'c|'+"}"

        print "\\hline"
        if option == "ratio":
            print "Bin                 &  \multicolumn{ 1 } {c} {      TT (2l)   }  & \multicolumn{ 1 } {c} {      TT (rest)   } & \multicolumn{ 1 } {c} {      frac dilep SR  } & \multicolumn{ 1 } {c} {      frac semil SR  }  & \multicolumn{ 1 } {c} {      TT (2l)   } &  \multicolumn{ 1 } {c} {      TT (rest)    }  & \multicolumn{ 1 } {c} {      frac dilep CR   \
 }& \multicolumn{ 1 } {c} {      frac semil CR  } & \multicolumn{ 1 } {c} {      RCS   }\\\ "
        elif option == "CRSR":
            print "Bin                 &  \multicolumn{ 1 } {c} {      TT (2l) SR  }  & \multicolumn{ 1 } {c} {      TT (rest)SR   } & \multicolumn{ 1 } {c} {      Rest SR   } & \multicolumn{ 1 } {c} {    AllBkg SR }   &  \multicolumn{ 1 } {c} {      TT (2l) CR   }  & \multicolumn{ 1 } {c} {      TT (rest) CR   } & \multicolumn{ 1 } {c} {      Rest CR  } & \multicolumn{ 1 } {c} {    AllBkg CR} & \multicolumn{ 1 } {c} {      RCSall }\\\ "
        else:
            print "Bin                 &  \multicolumn{ 1 } {c} {      TT (2l)   }  & \multicolumn{ 1 } {c} {      TT (rest)   } & \multicolumn{ 1 } {c} {      Single top   } & \multicolumn{ 1 } {c} {      TTV    } & \multicolumn{ 1 } {c} {     WJets  } & \multicolumn{ 1 } {c} {   QCD } & \multicolumn{ 1 } {c} {      DY   } & \multicolumn{ 1 } {c} {    ALL BKG } \\\ "
        print "\\hline"
        print "\\hline"

        for bin in ykeys:#yieldDict:
            (nTT, nTTErr, nTT_SemiLep, nTTErr_SemiLep, nTT_DiLep, nTTErr_DiLep, nTT_FullHad, nTTErr_FullHad, nSingleT, nSingleTErr, nTTV, nTTVErr, nWJets,  nWJetsErr, nQCD, nQCDErr, nDY, nDYErr) = yieldDict[bin]
            (nTT2, nTTErr2, nTT_SemiLep2, nTTErr_SemiLep2, nTT_DiLep2, nTTErr_DiLep2, nTT_FullHad2, nTTErr_FullHad2, nSingleT2, nSingleTErr2, nTTV2, nTTVErr2, nWJets2,  nWJetsErr2, nQCD2, nQCDErr2, nDY2, nDYErr2) = yieldDict2[bin]
            
            allbkg = nTT + nSingleT + nTTV + nWJets + nQCD + nDY
            allbkgErr = math.sqrt(nTTErr*nTTErr + nSingleTErr*nSingleTErr +nTTVErr*nTTVErr+ nWJetsErr*nWJetsErr +nQCDErr*nQCDErr+nDYErr*nDYErr)

            allbkg2 = nTT2 + nSingleT2 + nTTV2 + nWJets2 + nQCD2 + nDY2
            allbkgErr2 = math.sqrt(nTTErr2*nTTErr2 + nSingleTErr2*nSingleTErr2 +nTTVErr2*nTTVErr2+ nWJetsErr2*nWJetsErr2 +nQCDErr2*nQCDErr2+nDYErr2*nDYErr2)

            allbkgNoTT = nSingleT + nTTV + nWJets + nQCD + nDY
            allbkgErrNoTT = math.sqrt(nSingleTErr*nSingleTErr +nTTVErr*nTTVErr+ nWJetsErr*nWJetsErr +nQCDErr*nQCDErr+nDYErr*nDYErr)

            allbkgNoTT2 = nSingleT2 + nTTV2 + nWJets2 + nQCD2 + nDY2
            allbkgErrNoTT2 = math.sqrt(nSingleTErr2*nSingleTErr2 +nTTVErr2*nTTVErr2+ nWJetsErr2*nWJetsErr2 +nQCDErr2*nQCDErr2+nDYErr2*nDYErr2)
            bin = bin.replace('_', ' $;$ ')

            RCSall = 0
            if (allbkg2)>0:
                RCSall = (allbkg)/(allbkg2)
            if option == "CRSR":

                print "%s & %2.2f & %2.2f &%2.2f  & %2.2f  & %2.2f  & %2.2f  & %2.2f  & %2.2f & %2.4f  \\\ " % ( bin, nTT_DiLep,nTT_SemiLep, allbkgNoTT, allbkg, nTT_DiLep2,nTT_SemiLep2, allbkgNoTT2, allbkg2, RCSall)
#            print "%s & %2.2f & %2.2f &%2.2f  & %2.2f  & %2.2f  & %2.2f  & %2.2f  & %2.2f  \\\ " % ( bin, nTT_DiLep,nTT_SemiLep, nSingleT,  nTTV, nWJets,  nQCD,  nDY, allbkgNoTT)
            RCS = 0
            if (nTT_SemiLep+nTT_DiLep)>0:
                RCS = (nTT_SemiLep+nTT_DiLep)/(nTT_SemiLep2+nTT_DiLep2)
            fSemilep = 0
            fDilep = 0
            fSemilep2 = 0
            fDilep2 = 0
            if nTT_SemiLep+nTT_DiLep >0 :
                fSemilep = nTT_SemiLep/(nTT_DiLep+nTT_SemiLep)
                fDilep = nTT_DiLep/(nTT_DiLep+nTT_SemiLep)
            if nTT_SemiLep2+nTT_DiLep2 >0 :
                fSemilep2 = nTT_SemiLep2/(nTT_DiLep2+nTT_SemiLep2)
                fDilep2 = nTT_DiLep2/(nTT_DiLep2+nTT_SemiLep2)
#            print "%s & %2.2f & %2.2f &%2.2f  & %2.2f &  %2.2f & %2.2f &%2.2f  & %2.2f & %2.4f\\\ " % ( bin, nTT_DiLep,nTT_SemiLep, fDilep, fSemilep, nTT_DiLep2,nTT_SemiLep2, fDilep2, fSemilep2, RCS)
#            print nTT, nTT_DiLep, nTT_SemiLep, nTT_FullHad
        print "\\hline"
        print "\end{tabular}"
        print"\\end{center}"

        print "\\end{table}"


    return 1

def makeRCS(yieldDictSR, yieldDictCR):
    RCSval={}
    print "                                                          "
    print "bin | Nsignal +/- Err| NControl +/- Err |  RCS +/- Err| "
    
    ykeys = sorted(yieldDictSR.keys())
    for bin in ykeys:
        (nTTSR, nTTSRErr, nTTSR_SemiLep, nTTSRErr_SemiLep, nTTSR_DiLep, nTTSRErr_DiLep, nTTSR_FullHad, nTTSRErr_FullHad, nSingleTSR, nSingleTSRErr, nTTVSR, nTTVSRErr, nWJetsSR,  nWJetsSRErr, nQCDSR, nQCDSRErr, nDYSR, nDYSRErr) = yieldDictSR[bin]
        
        (nTTCR, nTTCRErr, nTTCR_SemiLep, nTTCRErr_SemiLep, nTTCR_DiLep, nTTCRErr_DiLep, nTTCR_FullHad, nTTCRErr_FullHad, nSingleTCR, nSingleTCRErr, nTTVCR, nTTVCRErr, nWJetsCR,  nWJetsCRErr, nQCDCR, nQCDCRErr, nDYCR, nDYCRErr) = yieldDictCR[bin]
        
#        allBkgSR = nTTSR + nSingleTSR + nTTVSR + nWJetsSR + nQCDSR + nDYSR
#        allBkgSRErr = math.sqrt(nTTSRErr*nTTSRErr + nSingleTSRErr*nSingleTSRErr +nTTVSRErr*nTTVSRErr+ nWJetsSRErr*nWJetsSRErr +nQCDSRErr*nQCDSRErr+nDYSRErr*nDYSRErr)
        allBkgSR = nTTSR + nSingleTSR + nTTVSR + nWJetsSR + nDYSR
        allBkgSRErr = math.sqrt(nTTSRErr*nTTSRErr + nSingleTSRErr*nSingleTSRErr +nTTVSRErr*nTTVSRErr+ nWJetsSRErr*nWJetsSRErr+nDYSRErr*nDYSRErr)
#        allBkgSR = 1
#        if nTTSR_DiLep>0.01:
#            allBkgSR = nTTSR_DiLep

        
        allBkgCR = nTTCR + nSingleTCR + nTTVCR + nWJetsCR + nQCDCR + nDYCR
        allBkgCRErr = math.sqrt(nTTCRErr*nTTCRErr + nSingleTCRErr*nSingleTCRErr +nTTVCRErr*nTTVCRErr+ nWJetsCRErr*nWJetsCRErr +nDYCRErr*nDYCRErr) 
#        allBkgCRErr = math.sqrt(nTTCRErr*nTTCRErr + nSingleTCRErr*nSingleTCRErr +nTTVCRErr*nTTVCRErr+ nWJetsCRErr*nWJetsCRErr +nQCDCRErr*nQCDCRErr+nDYCRErr*nDYCRErr) 
#        allBkgCR = nTTCR + nSingleTCR + nTTVCR + nWJetsCR + nDYCR
#        allBkgCR = 1
#        if nTTCR_DiLep>0.01:
#            allBkgCR = nTTCR_DiLep
 
        
        RCS = allBkgSR/allBkgCR
        RCS_Err = RCS * math.sqrt(allBkgSRErr/allBkgSR*allBkgSRErr/allBkgSR + allBkgCRErr/allBkgCR*allBkgCRErr/allBkgCR)
        print "%s:|%2.2f +/- %2.2f | %2.2f +/- %2.2f |%2.4f +/- %2.4f" % ( bin, allBkgSR, allBkgSRErr,allBkgCR, allBkgCRErr, RCS, RCS_Err)

        RCSval[bin] = [RCS, RCS_Err] 

    return RCSval

nameDict = {}
nameDict['ST1'] = " LT > 250 &&  LT < 350)"                                                                           
nameDict['ST2'] = " LT > 350  && LT < 450)"
nameDict['ST3'] = " LT > 450 && LT < 600)"                                                                              
nameDict['ST4'] = " LT > 600)"
nameDict['1B'] = "if ((nB == 1) && "
nameDict['2B'] = "if ((nB == 2) && "
nameDict['3B'] = "if ((nB >= 3) && "

def convLine(line):          
    line = line.replace('_45j_HT012','')
    line = line.replace('_','')
    for key in nameDict.keys(): 
        if key in line: 
            line = ' '+line   
            line = line.replace(key,nameDict[key]) 
            cline = line

    return cline 

def printRCSfunction(RCS_SB):
    ykeys = sorted(RCS_SB.keys())
    nkeys = nameDict.keys()
    for bin in ykeys:
        print convLine(bin), ' weight = ' + str(RCS_SB[bin][0])+ ';'
    


def makeKfactor(RCS_SB, RCS_SR):
    #doesn't quite work
    #would need to add up bjet multiplicity doesn't quite work yet
    STbins = ['ST1','ST2','ST3','ST4']
    names_SB = RCS_SB.keys()
    names_SR = RCS_SR.keys()
    for ST in STbins:
        for name_SB in names_SB:
            for name_SR in names_SR:
                if ST in name_SB and ST in name_SR:
                    print name_SB, name_SR, ST, RCS_SR[name_SR][0]/RCS_SB[name_SB][0]
                    

# MAIN
if __name__ == "__main__":

    nJobs = 12

    # read f-ratios
    ratDict = {}
#    ratDict = readRatios()

    ## usage: python read.py cardDir textformat

    if len(sys.argv) > 1:
        cardDirectory = sys.argv[1]
    else:
        cardDirectory="yields/QCD_yields_3fb_test3"

    if len(sys.argv) > 2:
        pfmt = sys.argv[3]
    else:
        pfmt = "text"


    cardDirectory = os.path.abspath(cardDirectory)
    cardDirName = os.path.basename(cardDirectory)

    print 'Using cards from', cardDirName
    commondir = 'common'
    cardPattern = 'CnC2015X'

    limitdict = {}
    sigdict = {}


    #print 80*'#'
    #print "Yields for", QCDdir

    # get card file list
    inDir = cardDirectory+'/'+commondir
    cardFnames = glob.glob(inDir+'/'+ cardPattern + '_*.root')
    cardNames = [os.path.basename(name) for name in cardFnames]

    cardNames = [(name.replace(cardPattern+'_','')).replace('.input.root','') for name in cardNames]

    SB = '45j'
    cardNamesSR_SB = [name for name in cardNames if name.find('SR_' + SB) > 0 and (name.find('a') <0 and name.find('012') <0)]
    cardNamesCR_SB = [name for name in cardNames if name.find('CR_' + SB) > 0 and (name.find('a') <0 and name.find('012') <0)]

    SB = '45j'
    cardNamesSR_SBa = [name for name in cardNames if name.find('SR_' + SB) > 0 and (name.find('a') >0 or name.find('012') >0)]
    cardNamesCR_SBa = [name for name in cardNames if name.find('CR_' + SB) > 0 and (name.find('a') >0 or name.find('012') >0)]

    nj68 = '68j'
    cardNamesSR_nj68 = [name for name in cardNames if name.find('SR_' + nj68) > 0]
    cardNamesCR_nj68 = [name for name in cardNames if name.find('CR_' + nj68) > 0]

    nj9Inf = '9Infj'
    cardNamesSR_nj9Inf = [name for name in cardNames if name.find('SR_' + nj9Inf) > 0]
    cardNamesCR_nj9Inf = [name for name in cardNames if name.find('CR_' + nj9Inf) > 0]

    #for kappa determination
    cardNamesSR_K = [name for name in cardNames if name.find('SRK_6') > 0 or name.find('SRK_9') > 0]
    cardNamesCR_K = [name for name in cardNames if name.find('CRK_6') > 0 or name.find('CRK_9') > 0]


    cardNamesSR_SB_K = [name for name in cardNames if name.find('SRK_4') > 0]
    cardNamesCR_SB_K = [name for name in cardNames if name.find('CRK_4') > 0]


    argTupleSR_SB = [(commondir, cardDirectory, name, ratDict) for name in cardNamesSR_SB]
    argTupleCR_SB = [(commondir, cardDirectory, name, ratDict) for name in cardNamesCR_SB]
    pool = Pool(nJobs)
    yieldDictSR_SB = dict(pool.map(_getYieldsFromInput, argTupleSR_SB))             
    yieldDictCR_SB = dict(pool.map(_getYieldsFromInput, argTupleCR_SB))                   

    argTupleSR_SBa = [(commondir, cardDirectory, name, ratDict) for name in cardNamesSR_SBa]
    argTupleCR_SBa = [(commondir, cardDirectory, name, ratDict) for name in cardNamesCR_SBa]
    pool = Pool(nJobs)
    yieldDictSR_SBa = dict(pool.map(_getYieldsFromInput, argTupleSR_SBa))             
    yieldDictCR_SBa = dict(pool.map(_getYieldsFromInput, argTupleCR_SBa))                   

    argTupleSR_nj68 = [(commondir, cardDirectory, name, ratDict) for name in cardNamesSR_nj68]
    argTupleCR_nj68 = [(commondir, cardDirectory, name, ratDict) for name in cardNamesCR_nj68]
    pool = Pool(nJobs)
    yieldDictSR_nj68 = dict(pool.map(_getYieldsFromInput, argTupleSR_nj68))             
    yieldDictCR_nj68 = dict(pool.map(_getYieldsFromInput, argTupleCR_nj68))                   

    argTupleSR_nj9Inf = [(commondir, cardDirectory, name, ratDict) for name in cardNamesSR_nj9Inf]
    argTupleCR_nj9Inf = [(commondir, cardDirectory, name, ratDict) for name in cardNamesCR_nj9Inf]
    pool = Pool(nJobs)
    yieldDictSR_nj9Inf = dict(pool.map(_getYieldsFromInput, argTupleSR_nj9Inf))             
    yieldDictCR_nj9Inf = dict(pool.map(_getYieldsFromInput, argTupleCR_nj9Inf))                   

    argTupleSR_K = [(commondir, cardDirectory, name, ratDict) for name in cardNamesSR_K]
    argTupleCR_K = [(commondir, cardDirectory, name, ratDict) for name in cardNamesCR_K]
    pool = Pool(nJobs)
    yieldDictSR_K = dict(pool.map(_getYieldsFromInput, argTupleSR_K))             
    yieldDictCR_K = dict(pool.map(_getYieldsFromInput, argTupleCR_K))                   

    argTupleSR_SB_K = [(commondir, cardDirectory, name, ratDict) for name in cardNamesSR_SB_K]
    argTupleCR_SB_K = [(commondir, cardDirectory, name, ratDict) for name in cardNamesCR_SB_K]
    pool = Pool(nJobs)
    yieldDictSR_SB_K = dict(pool.map(_getYieldsFromInput, argTupleSR_SB_K))             
    yieldDictCR_SB_K = dict(pool.map(_getYieldsFromInput, argTupleCR_SB_K))                   

                            
    RCS_SB = makeRCS(yieldDictSR_SB,yieldDictCR_SB)
    RCS_nj68 = makeRCS(yieldDictSR_nj68,yieldDictCR_nj68)
    RCS_nj9Inf = makeRCS(yieldDictSR_nj9Inf,yieldDictCR_nj9Inf)

    RCS_K = makeRCS(yieldDictSR_K,yieldDictCR_K)
    RCS_SB_K = makeRCS(yieldDictSR_SB_K,yieldDictCR_SB_K)


    makeTable(yieldDictSR_SB,yieldDictCR_SB,"latex")
    makeTable(yieldDictSR_SBa,yieldDictCR_SBa,"latex")
    makeTable(yieldDictSR_K,yieldDictCR_K,"latex")
    makeTable(yieldDictSR_nj68,yieldDictCR_nj68,"latex")
    makeTable(yieldDictSR_nj9Inf,yieldDictCR_nj9Inf,"latex")



#    printRCSfunction(RCS_SB)

    
#    makeKfactor(RCS_SB_K, RCS_K)
