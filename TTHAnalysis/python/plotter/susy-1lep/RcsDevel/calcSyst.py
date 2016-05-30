#!/usr/bin/env python
#import re, sys, os, os.path

from numpy import *
import glob, os, sys, math
from math import hypot
from ROOT import *

from readYields import getYield

def getDirNames(fname):

    tfile = TFile(fname,"READ")

    dirList = [dirKey.ReadObj().GetName() for dirKey in gDirectory.GetListOfKeys() if dirKey.IsFolder() == 1]

    tfile.Close()

    return dirList

def getHnames(fname,tdir):

    tfile = TFile(fname,"READ")
    tfile.cd(tdir)

    hnames = []

    for key in gDirectory.GetListOfKeys():

        obj = key.ReadObj()
        hnames.append(obj.GetName())

    tfile.Close()

    return hnames

def getSystHist(tfile, hname, syst = "Xsec"):
    print tfile, hname, syst
    if "Env" in syst or "RMS" in syst:
        hNorm = tfile.Get(hname)
        if hNorm: print "", #"got it", hname
        else: 
            print "ERROR!", hname
            return 0
#        print hNorm.GetName() + '_' + syst + '_syst'
        hSyst = hNorm.Clone(hNorm.GetName() + '_' + syst + '_syst')
        histDict = {}
        for i in range (0,200):
            hnameIter = hname + '_' + syst + str(i)
            tempImport = tfile.Get(hnameIter)
            if tempImport: 
                hVar = hNorm.Clone(hNorm.GetName() + '_' + syst + '_Var'+str(i))
                hVar.Add(tempImport,-1)
                histDict[i] = hVar
        # find maximum deviations
        for xbin in range(1,hSyst.GetNbinsX()+1):
            for ybin in range(1,hSyst.GetNbinsY()+1):
                # reset bins
                hSyst.SetBinContent(xbin,ybin,0)
                hSyst.SetBinError(xbin,ybin,0)
    
                maxDev = 0
                maxErr = 0
                
                DevUp, DevDn = -999, -999
#                print DevUp, DevDn
                print len(histDict), "variations taken into account; determining envelope"
                collectDevs = []
                for key, value in histDict.iteritems():
                    Dev = abs(value.GetBinContent(xbin,ybin))
                    collectDevs.append(Dev)
                    if DevUp==-999 or Dev>DevUp: DevUp=Dev
                    if DevDn==-999 or Dev<DevDn: DevDn=Dev
                    if Dev>maxDev: 
                        maxDev = Dev
#                        print key, Dev, hname

                a = array(collectDevs)
#                print collectDevs, a.mean(), a.std()
                maxDev = (DevUp-DevDn)/2#WARNING: HERE DOING ONLY AN ENVELOPE OF THE VARIATIONS!
                print DevUp, DevDn, maxDev
                # limit max deviation to 200%
                if "RMS" in syst: maxDev = a.std()

                maxDev = min(maxDev,2.0)
    
                hSyst.SetBinContent(xbin,ybin,maxDev)
                hSyst.SetBinError(xbin,ybin,maxErr)
                if maxDev>1 and "Kappa" in hname: print hname, maxDev, xbin, ybin, tfile
        #return hSyst
        return (hSyst,hSyst,hSyst)
            
    else:
    
        upName = hname + '_' + syst + '-Up'
        dnName = hname + '_' + syst + '-Down'
    
        #print tfile, hname, upName, dnName
    
        hNorm = tfile.Get(hname)
        hUp = tfile.Get(upName)
        hDown = tfile.Get(dnName)
    
        if not hUp and hDown:
            # Replace missing Up with Down
            hUp = hDown
        elif not hDown and hUp:
            # Replace missing Down with Up
            hDown = hUp
        elif not hUp or not hDown:
            print 'No systematics found!'
            print tfile, hname, upName, dnName
            return 0
    
        hSyst = hNorm.Clone(hNorm.GetName() + '_' + syst + '_syst')
    
        hUpVar = hNorm.Clone(hNorm.GetName() + '_' + syst + '_upVar')
        hUpVar.Add(hUp,-1)
    
        hDownVar = hNorm.Clone(hNorm.GetName() + '_' + syst + '_downVar')
        hDownVar.Add(hDown,-1)
    
        # find maximum deviations
        for xbin in range(1,hSyst.GetNbinsX()+1):
            for ybin in range(1,hSyst.GetNbinsY()+1):
    
                # reset bins
                hSyst.SetBinContent(xbin,ybin,0)
                hSyst.SetBinError(xbin,ybin,0)
    
                maxDev = 0
                maxErr = 0
    
                # fill maximum deviation
    #            if abs(hUpVar.GetBinContent(xbin,ybin)) > abs(hDownVar.GetBinContent(xbin,ybin)):
    #                maxDev = abs(hUpVar.GetBinContent(xbin,ybin))
    #            else:
    #                maxDev = abs(hDownVar.GetBinContent(xbin,ybin))
    
                #fill with average deviation
                maxDev = 1/2.*(math.fabs(hUpVar.GetBinContent(xbin,ybin))+math.fabs(hDownVar.GetBinContent(xbin,ybin)))
                #maxDev = 1/2 * (abs(hUpVar.GetBinContent(xbin,ybin))+ abs(hDownVar.GetBinContent(xbin,ybin)))
    
                if hNorm.GetBinContent(xbin,ybin) > 0:
                    maxDev /= hNorm.GetBinContent(xbin,ybin)
                #    maxErr = hypot(maxErr,hNorm.GetBinError(xbin,ybin))
    
                # limit max deviation to 200%
                maxDev = min(maxDev,2.0)
                # put at least 0.00001 as dummy
                maxDev = max(maxDev,0.00001)
    
                hSyst.SetBinContent(xbin,ybin,maxDev)
                hSyst.SetBinError(xbin,ybin,maxErr)
    
        #return hSyst
        return (hSyst,hUpVar,hDownVar)

def makeSystHists(fileList):

    # filter
    #fileList = [fname for fname in fileList if 'NB3' not in fname]

    #hnames = ["T1tttt_Scan"] # process name
    #hnames = ["EWK"] # process name
    hnames = ["EWK","TTJets","WJets","SingleTop","DY","TTV"] # process name
    #hnames = ['T_tWch','TToLeptons_tch','TBar_tWch', 'EWK', 'TToLeptons_sch'] # process name
    #hnames = ["TTJets","WJets","SingleTop","DY","TTV"] # process name
    #hnames = getHnames(fileList[0],'SR_MB') # get process names from file
    #print 'Found these hists:', hnames

    #systNames = ["Xsec"]
    #systNames = ["PU"]
    #systNames = ["topPt"]
    #systNames = ["Wxsec"]
    systNames = ["ScaleMatchVar-Env"]
    #systNames = ["PDFUnc-RMS"]
    #systNames = ["Wxsec"]
    #systNames = ["TTVxsec"]
    systNames = ["lepSF"]
    #systNames = ["JEC"]
    #systNames = ["DLSlope"]
    #systNames = ["DLConst"]
    #systNames = ["JER"]
    #systNames = ["Wpol"]
    #systNames = ["btagHF","btagLF"]
    #systNames = ["ISR"]

    #bindirs =  ['SR_MB','CR_MB','SR_SB','CR_SB']
    #bindirs =  ['SR_MB','CR_MB','SR_SB','CR_SB','Kappa','Rcs_MB','Rcs_SB']
    bindirs = getDirNames(fileList[0])# + [""]
    print "Found those dirs:", bindirs

    # dir to store
    sysdir = os.path.dirname(fileList[0]) + "/syst/"
    if not os.path.exists(sysdir): os.makedirs(sysdir)

    for fname in fileList:
        tfile = TFile(fname,"UPDATE")
        #tfile = TFile(fname,"READ")
        #sysname = sysdir + os.path.basename(fname)
        #sfile = TFile(sysname,"RECREATE")

        for bindir in bindirs:

            for hname in hnames:
                for syst in systNames:

                    if bindir != "":
                        (hSyst,hUp,hDown) = getSystHist(tfile, bindir+'/'+ hname, syst)
                    else:
                        (hSyst,hUp,hDown) = getSystHist(tfile, hname, syst)

                    if hSyst:
                        tfile.cd(bindir)
                        #sfile.mkdir(bindir)
                        #sfile.cd(bindir)
                        hSyst.Write("",TObject.kOverwrite)
                        #hUp.Write("",TObject.kOverwrite)
                        #hDown.Write("",TObject.kOverwrite)

            '''
            # create Syst folder structure
            if not tfile.GetDirectory(bindir+"/Syst"):
                tfile.mkdir(bindir+"/Syst")

                for hname in hnames:
                    for syst in systNames:

                        tfile.cd(bindir+"/Syst")
                        hSyst = getSystHist(tfile, bindir+'/'+ hname, syst)
                        hSyst.Write()
            else:
                print 'Already found syst'
            '''

        tfile.Close()
        #sfile.Close()

    return 1


if __name__ == "__main__":

    ## remove '-b' option
    _batchMode = False

    if '-b' in sys.argv:
        sys.argv.remove('-b')
        _batchMode = True

    if len(sys.argv) > 1:
        pattern = sys.argv[1]
        print '# pattern is', pattern
    else:
        print "No pattern given!"
        exit(0)

    # append / if pattern is a dir
    if os.path.isdir(pattern): pattern += "/"

    # find files matching pattern
    fileList = glob.glob(pattern+"*.root")

    makeSystHists(fileList)

    print 'Finished'
