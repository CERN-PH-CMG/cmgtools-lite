#!/usr/bin/env python
import sys
import re

ODIR=sys.argv[1]

dowhat = "plots" 
#dowhat = "dumps" 
#dowhat = "yields" 

def base(selection):

    CORE="-P /afs/cern.ch/user/f/folguera/workdir/trees/ewkino/TREES_76X_160502 -F sf/t {P}/2_lepMVA/evVarFriend_{cname}.root -F sf/t {P}/3_recleaner_mva/evVarFriend_{cname}.root "

    CORE+=" -f -j 12 -l 10 --s2v --tree treeProducerSusyMultilepton --mcc susy-ewkino/lepchoice-ss2l-FO.txt --mcc susy-ewkino/susy_ss2l_triggerdefs.txt --neg"
    if dowhat == "plots": CORE+=" --lspam '#bf{CMS} #it{Preliminary}' --legendWidth 0.20 --legendFontSize 0.035 --showRatio --maxRatioRange 0 3  --showMCError --rebin 4"

    if selection=='ss2l':
        GO="%s susy-ewkino/mca-ss2l-mc.txt susy-ewkino/susy_ss2l_cuts.txt  "%CORE
        if dowhat == "plots": GO+=" susy-ewkino/ss2l_plots.txt "
##    elif selection=='3l':
##        ### NEED TO CHANGE IT TO RUN THE EWKINO MULTILEPTON
##        GO="%s ttH-multilepton/mca-3l-mc.txt ttH-multilepton/3l_tight.txt "%CORE
##        GO="%s -W 'puw(nTrueInt)*leptonSF_ttH(LepGood_pdgId[iF_Recl[0]],LepGood_pt[iF_Recl[0]],LepGood_eta[iF_Recl[0]],3)*leptonSF_ttH(LepGood_pdgId[iF_Recl[1]],LepGood_pt[iF_Recl[1]],LepGood_eta[iF_Recl[1]],3)*leptonSF_ttH(LepGood_pdgId[iF_Recl[2]],LepGood_pt[iF_Recl[2]],LepGood_eta[iF_Recl[2]],3)*triggerSF_ttH(LepGood_pdgId[iF_Recl[0]],LepGood_pt[iF_Recl[0]],LepGood_pdgId[iF_Recl[1]],LepGood_pt[iF_Recl[1]],3)*eventBTagSF'"%GO
##        if dowhat == "plots": GO+=" ttH-multilepton/2lss_3l_plots.txt --xP '2lep_.*' --xP 'kinMVA_2lss_.*'  --xP 'nT_.*' --xP 'debug_.*' "
    else:
        raise RuntimeError, 'Unknown selection'

    return GO

def procs(GO,mylist):
    return GO+' '+" ".join([ '-p %s'%l for l in mylist ])
def sigprocs(GO,mylist):
    return procs(GO,mylist)+' --showIndivSigs --noStackSig'
def runIt(GO,name,plots=[],noplots=[]):
    if   dowhat == "plots":  print 'python mcPlots.py',"--pdir %s/%s"%(ODIR,name),GO,' '.join(['--sP %s'%p for p in plots]),' '.join(['--xP %s'%p for p in noplots]),' '.join(sys.argv[3:])
    elif dowhat == "yields": print 'echo %s; python mcAnalysis.py'%name,GO,' '.join(sys.argv[3:])
    elif dowhat == "dumps":  print 'echo %s; python mcDump.py'%name,GO,' '.join(sys.argv[3:])
def add(GO,opt):
    return '%s %s'%(GO,opt)
def setwide(x):
    x2 = add(x,'--wide')
    x2 = x2.replace('--legendWidth 0.35','--legendWidth 0.20')
    return x2

    
if __name__ == '__main__':
    
    print ODIR
    torun = sys.argv[2]
    print torun

    if 'ss2l' in torun:
        x = base('ss2l')

        runIt(x,'%s'%torun)
        if '_flav' in torun:
            for flav in ['mm','ee','em']: runIt(add(x,'-E ^%s'%flav),'%s/%s'%(torun,flav))



