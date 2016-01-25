#!/usr/bin/env python

ODIR="test_tthplots_jan26"

lumi = 2.16

def base(selection='2lss'):

    T="-P /data/p/peruzzi/TREES_74X_140116_MiniIso_tauClean_Mor16lepMVA"
    CORE="%s --neg --s2v --tree treeProducerSusyMultilepton --mcc ttH-multilepton/lepchoice-ttH-FO.txt --mcc ttH-multilepton/ttH_2lss3l_triggerdefs.txt -F sf/t {P}/2_recleaner_v3_ttHvariations/evVarFriend_{cname}.root"%T

    if selection=='2lss':
        GO="python mcPlots.py %s ttH-multilepton/mca-2lss-mc.txt ttH-multilepton/2lss_tight.txt -f -j 8 --lspam '#bf{CMS} #it{Preliminary}' --legendWidth 0.20 --legendFontSize 0.035 --showRatio --maxRatioRange 0 3 ttH-multilepton/check_FO_def_plots.txt --showMCError"%CORE
#    elif selection=='3l':
#        GO="python mcPlots.py %s ttH-multilepton/mca-3l-Mor16.txt ttH-multilepton/3l_Mor16.txt -f -j 8 --lspam '#bf{CMS} #it{Preliminary}' --legendWidth 0.20 --legendFontSize 0.035 --showRatio --maxRatioRange 0 3 ttH-multilepton/cr_3l_plots.txt --showMCError"%CORE
    else:
        raise RuntimeError, 'Unknown selection'

    withpu = "%s -l %f"%(GO,lumi)
#    PU_ALL = " --FMC sf/t {P}/1_purew_mix_true_nvtx/evVarFriend_{cname}.root -W 'vtxWeight*btagMediumSF_Mini*triggerSF_Loop*leptonSF_Loop' -l %f"%lumi_all
    return withpu

def procs(GO,mylist):
    return GO+' '+" ".join([ '-p %s'%l for l in mylist ])
def sigprocs(GO,mylist):
    return procs(GO,mylist)+' --showIndivSigs --noStackSig'
def runIt(GO,name,plots=[],noplots=[]):
    print GO,' '.join(['--sP %s'%p for p in plots]),' '.join(['--xP %s'%p for p in noplots]),"--pdir /afs/cern.ch/user/p/peruzzi/www/%s/%s"%(ODIR,name)
def add(GO,opt):
    return '%s %s'%(GO,opt)
def setwide(x):
    x2 = add(x,'--wide')
    x2 = x2.replace('--legendWidth 0.35','--legendWidth 0.20')
    return x2

if __name__ == '__main__':

    x = base('2lss')
    x = procs(x,['ttH'])
    runIt(x,'2lss_SR')

#    x = base('2lss')
#    x = procs(x,['ttH'])
#    x = add(x,"-R mt2FO_2Tight mt2FO_mt2Tight 'nLepFO>=2 && nLepTight>=2'")
#    x = add(x, "-A alwaystrue noHtautau 'GenHiggsDecayMode!=15'")
#    runIt(x,'2lss_SR')
#    x2 = add(x,"-X 4j -X 2b1B")
#    runIt(x2,'2lss_SR_nojetcut')
#
#    x3 = add(x2,"-R pt2010 pt2015 'LepGood1_conePt>20 && LepGood2_conePt>15' ")
#    runIt(x3,'2lss_SR_nojetcut_cut15')
#
#    for mod in ["ReclConept15","ReclBtagTightVeto","ReclBtagMediumVeto"]:
#
#        x = base('2lss')
#        x = procs(x,['ttH'])
#        x = add(x,"-R mt2FO_2Tight mt2FO_mt2Tight 'nLepFO>=2 && nLepTight>=2'")
#        x = add(x, "-A alwaystrue noHtautau 'GenHiggsDecayMode!=15'")
#        x = x.replace('lepchoice-ttH-FO.txt','lepchoice-ttH-FO-%s.txt'%mod)
#        runIt(x,'2lss_SR_%s'%mod)
#        x2 = add(x,"-X 4j -X 2b1B")
#        runIt(x2,'2lss_SR_nojetcut_%s'%mod)

#    x = base('2lss')
#    x = x.replace('mca-2lss-mc.txt','mca-2lss-mc-appl.txt')
#    x = x.replace('2_recleaner_v3_ttHvariations','2_recleaner_v3')
#    runIt(x,'2lss_SR_appl')


#    x = base('3l')
#    x = procs(x,['ttH'])
#    runIt(x,'3l_SR')
