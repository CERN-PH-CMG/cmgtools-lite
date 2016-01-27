#!/usr/bin/env python
import sys

ODIR=sys.argv[1]

lumi = 2.16

def base(selection):

    CORE="-P /data1/p/peruzzi/TREES_74X_140116_MiniIso_tauClean_Mor16lepMVA -F sf/t {P}/2_recleaner_v4_vetoCSVM/evVarFriend_{cname}.root -F sf/t {P}/4_kinMVA_trainMarcoJan27_v0/evVarFriend_{cname}.root"

    CORE+=" -l 2.26 --neg --s2v --tree treeProducerSusyMultilepton --mcc ttH-multilepton/lepchoice-ttH-FO.txt --mcc ttH-multilepton/ttH_2lss3l_triggerdefs.txt -F sf/t {P}/2_recleaner_v3/evVarFriend_{cname}.root"
    CORE+=" -f -j 8 --lspam '#bf{CMS} #it{Preliminary}' --legendWidth 0.20 --legendFontSize 0.035 --showRatio --maxRatioRange 0 3  --showMCError"

    if selection=='2lss':
        GO="python mcPlots.py %s ttH-multilepton/mca-2lss-mc.txt ttH-multilepton/2lss_tight.txt ttH-multilepton/2lss_3l_plots.txt --xP 'lep3_.*' --xP '3lep_.* --xP 'kinMVA_3l_.*'' "%CORE
    elif selection=='3l':
        GO="python mcPlots.py %s ttH-multilepton/mca-3l-mc.txt ttH-multilepton/3l_tight.txt ttH-multilepton/2lss_3l_plots.txt --xP '2lep_.*' --xP 'kinMVA_2lss_.*' "%CORE
    else:
        raise RuntimeError, 'Unknown selection'

    return GO

def procs(GO,mylist):
    return GO+' '+" ".join([ '-p %s'%l for l in mylist ])
def sigprocs(GO,mylist):
    return procs(GO,mylist)+' --showIndivSigs --noStackSig'
def runIt(GO,name,plots=[],noplots=[]):
    print GO,' '.join(['--sP %s'%p for p in plots]),' '.join(['--xP %s'%p for p in noplots]),"--pdir %s/%s"%(ODIR,name)
def add(GO,opt):
    return '%s %s'%(GO,opt)
def setwide(x):
    x2 = add(x,'--wide')
    x2 = x2.replace('--legendWidth 0.35','--legendWidth 0.20')
    return x2

if __name__ == '__main__':

    torun = None
    if len(sys.argv)>2: torun = sys.argv[2:]

    if not torun or '2lss_SR' in torun:
        x = base('2lss')
        runIt(x,'2lss_SR/all')
        for flav in ['mm','ee','em']: runIt(add(x,'-E %s'%flav),'2lss_SR/%s'%flav)

    if not torun or '3l_SR' in torun:
        x = base('3l')
        runIt(x,'3l_SR')

# x = procs(x,['ttH'])# to plot only ttH
# x = add(x,"-E 2B") # b-tight selection
