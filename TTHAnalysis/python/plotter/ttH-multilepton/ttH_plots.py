#!/usr/bin/env python
import sys
import re

ODIR=sys.argv[1]

doplots=True

def base(selection):

    CORE="-P /data1/peruzzi/TREES_76X_200216_jecV1M2_skimOnlyMC_reclv8 -F sf/t {P}/2_recleaner_v8_b1E2/evVarFriend_{cname}.root -F sf/t {P}/4_kinMVA_trainFeb23_v0/evVarFriend_{cname}.root -F sf/t {P}/5_eventBTagRWT_onlyJets_v1/evVarFriend_{cname}.root"

    CORE+=" -f -j 8 -l 2.26 --s2v --tree treeProducerSusyMultilepton --mcc ttH-multilepton/lepchoice-ttH-FO.txt --mcc ttH-multilepton/ttH_2lss3l_triggerdefs.txt"# --neg"
    if doplots: CORE+=" --lspam '#bf{CMS} #it{Preliminary}' --legendWidth 0.20 --legendFontSize 0.035 --showRatio --maxRatioRange 0 3  --showMCError --rebin 2"

    if selection=='2lss':
        GO="%s ttH-multilepton/mca-2lss-mc.txt ttH-multilepton/2lss_tight.txt "%CORE
        GO="%s -W 'puw(nTrueInt)*leptonSF_ttH(LepGood_pdgId[iF_Recl[0]],LepGood_pt[iF_Recl[0]],LepGood_eta[iF_Recl[0]],2)*leptonSF_ttH(LepGood_pdgId[iF_Recl[1]],LepGood_pt[iF_Recl[1]],LepGood_eta[iF_Recl[1]],2)*triggerSF_ttH(LepGood_pdgId[iF_Recl[0]],LepGood_pt[iF_Recl[0]],LepGood_pdgId[iF_Recl[1]],LepGood_pt[iF_Recl[1]],2)*eventBTagSF'"%GO
        if doplots: GO+=" ttH-multilepton/2lss_3l_plots.txt --xP 'lep3_.*' --xP '3lep_.*' --xP 'kinMVA_3l_.*' --xP 'kinMVA_input.*' "
    elif selection=='3l':
        GO="%s ttH-multilepton/mca-3l-mc.txt ttH-multilepton/3l_tight.txt "%CORE
        GO="%s -W 'puw(nTrueInt)*leptonSF_ttH(LepGood_pdgId[iF_Recl[0]],LepGood_pt[iF_Recl[0]],LepGood_eta[iF_Recl[0]],3)*leptonSF_ttH(LepGood_pdgId[iF_Recl[1]],LepGood_pt[iF_Recl[1]],LepGood_eta[iF_Recl[1]],3)*leptonSF_ttH(LepGood_pdgId[iF_Recl[2]],LepGood_pt[iF_Recl[2]],LepGood_eta[iF_Recl[2]],3)*triggerSF_ttH(LepGood_pdgId[iF_Recl[0]],LepGood_pt[iF_Recl[0]],LepGood_pdgId[iF_Recl[1]],LepGood_pt[iF_Recl[1]],3)*eventBTagSF'"%GO
        if doplots: GO+=" ttH-multilepton/2lss_3l_plots.txt --xP '2lep_.*' --xP 'kinMVA_2lss_.*' --xP 'kinMVA_input.*' "
    else:
        raise RuntimeError, 'Unknown selection'

    return GO

def procs(GO,mylist):
    return GO+' '+" ".join([ '-p %s'%l for l in mylist ])
def sigprocs(GO,mylist):
    return procs(GO,mylist)+' --showIndivSigs --noStackSig'
def runIt(GO,name,plots=[],noplots=[]):
    if '_74vs76' in name: GO = prep74vs76(GO)
    if doplots: print 'python mcPlots.py',"--pdir %s/%s"%(ODIR,name),GO,' '.join(['--sP %s'%p for p in plots]),' '.join(['--xP %s'%p for p in noplots]),' '.join(sys.argv[3:])
    else: print 'echo %s; python mcAnalysis.py'%name,GO,' '.join(sys.argv[3:])
def add(GO,opt):
    return '%s %s'%(GO,opt)
def setwide(x):
    x2 = add(x,'--wide')
    x2 = x2.replace('--legendWidth 0.35','--legendWidth 0.20')
    return x2
def fulltrees(x):
    return x.replace('TREES_76X_200216_jecV1M2_skimOnlyMC_reclv8','TREES_76X_200216_jecV1M2')

if __name__ == '__main__':

    torun = sys.argv[2]

    if 'data' in torun and not any([re.match(x.strip()+'$',torun) for x in ['.*_appl.*','cr_.*','2lss_SR_.*_data_frdata','3l_SR_.*_data_frdata']]): raise RuntimeError, 'You are trying to unblind!'

    if '2lss_' in torun:
        x = base('2lss')
        if '_appl' in torun: x = add(x,'-I TT')
        if '_1fo' in torun: x = add(x,"-A alwaystrue 1FO 'LepGood1_isTight+LepGood2_isTight==1'")
        if '_2fo' in torun: x = add(x,"-A alwaystrue 2FO 'LepGood1_isTight+LepGood2_isTight==0'")
        if '_relax' in torun: x = add(x,'-X TT')
        if '_data' in torun: x = x.replace('mca-2lss-mc.txt','mca-2lss-mcdata.txt')
        if '_frdata' in torun:
            if not '_data' in torun: raise RuntimeError
            x = fulltrees(x) # for the flips
            x = add(x,"--xp data")
            x = x.replace('mca-2lss-mcdata.txt','mca-2lss-mcdata-frdata.txt')

        if '_splitfakes' in torun:
            x = x.replace('mca-2lss-mc.txt','mca-2lss-mc-flavsplit.txt')
            
        if '_closuretest' in torun:
            x = x.replace('mca-2lss-mc.txt','mca-2lss-mc-closuretest.txt')
#            x = x.replace("--xP 'kinMVA_input.*'","--sP 'kinMVA_input.*'")
            x = x.replace("--maxRatioRange 0 3","--maxRatioRange 0.5 1.5")
            x = add(x,"--AP --plotmode nostack --sP kinMVA_2lss_ttbar --sP kinMVA_2lss_ttV")
            x = add(x,"--ratioDen FR_QCD --ratioNums FR_TT --rebin 4 --errors")
            if '_closuretest_norm' in torun:
                x = x.replace("--plotmode nostack","--plotmode norm")
                x = add(x,"--fitRatio 1")
            if '_bloose' in torun: x = add(x,'-E BLoose')
            if '_btight' in torun: x = add(x,'-E BTight')
            if '_nobcut' in torun: x = add(x,'-X 2b1B')
            if '_notrigger' in torun: x = add(x,'-X trigger')

        if '_varsFR' in torun:
            torun += "_"+sys.argv[-1]
            x = x.replace('mca-2lss-mc.txt','mca-2lss-data-frdata-%s.txt'%sys.argv[-1])
            x = x.replace("--maxRatioRange 0 3","--maxRatioRange 0 2")
            x = add(x,"--plotmode nostack --sP kinMVA_2lss_ttbar --sP kinMVA_2lss_ttV")
            x = add(x,"--ratioDen fakes_data --ratioNums fakes_data_%s --rebin 4 --errors"%sys.argv[-1])
            if '_varsFR_norm' in torun:
                x = x.replace("--plotmode nostack","--plotmode norm")
                x = add(x,"--fitRatio 1")

        runIt(x,'%s/all'%torun)
        if '_flav' in torun:
            for flav in ['mm','ee','em']: runIt(add(x,'-E %s'%flav),'%s/%s'%(torun,flav))

    if '3l_' in torun:
        x = base('3l')
        if '_appl' in torun: x = add(x,'-I TTT')
        if '_relax' in torun: x = add(x,'-X TTT')
        if '_data' in torun: x = x.replace('mca-3l-mc.txt','mca-3l-mcdata.txt')
        if '_frdata' in torun:
            if not '_data' in torun: raise RuntimeError
            x = add(x,"--xp data")
            x = x.replace('mca-3l-mcdata.txt','mca-3l-mcdata-frdata.txt')
        if '_closuretest' in torun:
            x = x.replace('mca-3l-mc.txt','mca-3l-mc-closuretest.txt')
#            x = x.replace("--xP 'kinMVA_input.*'","--sP 'kinMVA_input.*'")
            x = x.replace("--maxRatioRange 0 3","--maxRatioRange 0.5 1.5")
            x = add(x,"--AP --plotmode nostack --sP kinMVA_3l_ttbar --sP kinMVA_3l_ttV")
            x = add(x,"--ratioDen FR_QCD --ratioNums FR_TT --rebin 4 --errors")
            if '_closuretest_norm' in torun:
                x = x.replace("--plotmode nostack","--plotmode norm")
                x = add(x,"--fitRatio 1")
            if '_notrigger' in torun: x = add(x,'-X trigger')
        if '_varsFR' in torun:
            torun += "_"+sys.argv[-1]
            x = x.replace('mca-3l-mc.txt','mca-3l-data-frdata-%s.txt'%sys.argv[-1])
            x = x.replace("--maxRatioRange 0 3","--maxRatioRange 0 2")
            x = add(x,"--plotmode nostack --sP kinMVA_3l_ttbar --sP kinMVA_3l_ttV")
            x = add(x,"--ratioDen fakes_data --ratioNums fakes_data_%s --rebin 4 --errors"%sys.argv[-1])
            if '_varsFR_norm' in torun:
                x = x.replace("--plotmode nostack","--plotmode norm")
                x = add(x,"--fitRatio 1")
        runIt(x,'%s'%torun)

    if 'cr_3j' in torun:
        x = base('2lss')
        if '_data' in torun: x = x.replace('mca-2lss-mc.txt','mca-2lss-mcdata.txt')
        if '_frdata' in torun:
            if not '_data' in torun: raise RuntimeError
            x = fulltrees(x) # for the flips
            x = x.replace('mca-2lss-mcdata.txt','mca-2lss-mcdata-frdata.txt')
        x = add(x,"-R 4j 3j 'nJet25==3' --rebin 2")
        plots = ['nJet25','nBJetLoose25','nBJetMedium25','met','metLD','htJet25j','mhtJet25','mtWmin','htllv','kinMVA_2lss_ttbar','kinMVA_2lss_ttV']
        runIt(x,'%s/all'%torun,plots)
        if '_flav' in torun:
            for flav in ['mm','ee','em']:
                runIt(add(x,'-E %s'%flav),'%s/%s'%(torun,flav),plots)
#                if flav=='ee': runIt(add(x,'-E %s -X ee_metLD'%flav),'%s/%s_relaxMetLD'%(torun,flav),plots)

    if 'cr_ttbar' in torun:
        x = base('2lss')
        x = fulltrees(x)
        x = x.replace('mca-2lss-mc.txt','mca-2lss-mcdata-ttbar.txt')
        if '_data' not in torun: x = add(x,'--xp data')
        if '_appl' in torun: x = add(x,'-I TT')
        if '_1fo' in torun: x = add(x,"-A alwaystrue 1FO 'LepGood1_isTight+LepGood2_isTight==1'")
        if '_leadmupt25' in torun: x = add(x,"-A 'entry point' leadmupt25 'abs(LepGood1_pdgId)==13 && LepGood1_pt>25'")
        x = add(x,"-I same-sign -X 4j -X 2b1B -E 2j -E em")
        if '_highMetNoBCut' in torun: x = add(x,"-A 'entry point' highMET 'met_pt>60'")
        else: x = add(x,"-E 1B")
        plots = ['2lep_bestMVA','2lep_worseMVA','met','metLD','nVert','nJet25','nBJetMedium25','nBJetLoose25','nBJetLoose40','nBJetMedium40']
        runIt(x,'%s'%torun,plots)

    if 'cr_wz' in torun:
        x = base('3l')
        if '_data' in torun: x = x.replace('mca-3l-mc.txt','mca-3l-mcdata.txt')
        x = add(x,"-I 'Z veto' -X 4j -X 2b1B -E Bveto --rebin 4")
        plots = ['lep3_pt','metLD','nBJetLoose25','3lep_worseIso','minMllAFAS','3lep_worseMVA','3lep_mtW']
        runIt(x,'%s'%torun,plots)

    if 'cr_ttz' in torun:
        x = base('3l')
        if '_data' in torun: x = x.replace('mca-3l-mc.txt','mca-3l-mcdata.txt')
        if '_frdata' in torun:
            if not '_data' in torun: raise RuntimeError
            x = add(x,"--xp data")
            x = x.replace('mca-3l-mcdata.txt','mca-3l-mcdata-frdata.txt')
        plots = ['lep2_pt','met','nJet25','mZ1']
        x = add(x,"-I 'Z veto' -X 2b1B -E 2b -E 1B --rebin 4")
        runIt(x,'%s'%torun,plots)
        x = add(x,"-E 4j")
        runIt(x,'%s_4j'%torun,plots)

