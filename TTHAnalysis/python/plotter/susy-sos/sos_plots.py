#!/usr/bin/env python
import sys
import re

ODIR=sys.argv[1]

dowhat = "plots" 
#dowhat = "dumps" 
#dowhat = "yields" 


def base(selection):

    #CORE="-P /data1/botta/trees_SOS_newpresel_030616/"
    CORE="-P /data1/botta/trees_SOS_80X_170616/"
    CORE+=" -f -j 8 -l 5.0 --s2v --tree treeProducerSusyMultilepton --mcc susy-sos/mcc-lepWP.txt "#--mcc susy-sos/2los_triggerdefs.txt # --neg"
    if dowhat == "plots": CORE+=" --lspam CMSsimulation --legendWidth 0.14 --legendFontSize 0.04"

    if selection=='2los':
        GO="%s susy-sos/mca-2los-mc.txt susy-sos/2los_tight.txt "%CORE
        #GO="%s -W 'puw(nTrueInt)*leptonSF_ttH(LepGood_pdgId[iF_Recl[0]],LepGood_pt[iF_Recl[0]],LepGood_eta[iF_Recl[0]],2)*leptonSF_ttH(LepGood_pdgId[iF_Recl[1]],LepGood_pt[iF_Recl[1]],LepGood_eta[iF_Recl[1]],2)*triggerSF_ttH(LepGood_pdgId[iF_Recl[0]],LepGood_pt[iF_Recl[0]],LepGood_pdgId[iF_Recl[1]],LepGood_pt[iF_Recl[1]],2)*eventBTagSF'"%GO
        #GO="%s -W 'puw(nTrueInt)'"%GO
        GO="%s -W 'puw2016_vtx_4fb(nTrueInt)'"%GO
        if dowhat == "plots": GO+=" susy-sos/2los_plots.txt"
    else:
        raise RuntimeError, 'Unknown selection'

    return GO

def procs(GO,mylist):
    return GO+' '+" ".join([ '-p %s'%l for l in mylist ])
def sigprocs(GO,mylist):
    return procs(GO,mylist)+' --showIndivSigs --noStackSig'
def runIt(GO,name,plots=[],noplots=[]):
    if '_74vs76' in name: GO = prep74vs76(GO)
    if   dowhat == "plots":  print 'python mcPlots.py',"--pdir %s/%s"%(ODIR,name),GO,' '.join(['--sP %s'%p for p in plots]),' '.join(['--xP %s'%p for p in noplots]),' '.join(sys.argv[3:])
    elif dowhat == "yields": print 'echo %s; python mcAnalysis.py'%name,GO,' '.join(sys.argv[3:])
    elif dowhat == "dumps":  print 'echo %s; python mcDump.py'%name,GO,' '.join(sys.argv[3:])
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

    if '2los_SR_vars' in torun:
        x = base('2los')
        if '_notrigger' in torun: x = add(x,'-X ^trigger ')
        if '_met200' in torun: x = add(x,'-E ^highMET ')
        if '_met100' in torun: x = add(x,'-E ^upperMET -E ^mm')
        if '_nminus1' in torun: 
            x = add(x,"--n-minus-one")
            x = x.replace('-f','')
        x = add(x,"--noStackSig --showIndivSigShapes --xp TChiNeuWZ_95,T2ttDeg_300,T2ttDeg_315")
        runIt(x,'%s/all'%torun,[],['SR_bins_EWKino','SR_bins_stop'])

    if '2los_SR_bins' in torun:
        x = base('2los')
        if '_notrigger' in torun: x = add(x,'-X ^trigger ')
        if '_ewk10_met100_mm' in torun: 
            x = add(x,"--xp TChiNeuWZ_95,TChiNeuWZ_80,T2ttDeg_300,T2ttDeg_315,T2ttDeg_330 -E ^sublepPt5 -E ^MT -E ^mm -E ^upperMET")
            runIt(x,'%s/all'%torun,['SR_bins_EWKino'])
        if '_ewk10_met200_mm' in torun: 
            x = add(x,"--xp TChiNeuWZ_95,TChiNeuWZ_80,T2ttDeg_300,T2ttDeg_315,T2ttDeg_330 -E ^sublepPt5 -E ^MT -E ^mm -E ^highMET")
            runIt(x,'%s/all'%torun,['SR_bins_EWKino'])
        if '_ewk10_met200_ee' in torun: 
            x = add(x,"--xp TChiNeuWZ_95,TChiNeuWZ_80,T2ttDeg_300,T2ttDeg_315,T2ttDeg_330 -E ^sublepPt5 -E ^MT -E ^ee -E ^highMET")
            runIt(x,'%s/all'%torun,['SR_bins_EWKino'])    
        if '_ewk20_met100_mm' in torun: 
            x = add(x,"--xp TChiNeuWZ_95,TChiNeuWZ_90,T2ttDeg_300,T2ttDeg_315,T2ttDeg_330 -E ^sublepPt5 -E ^MT -E ^mm -E ^upperMET")
            runIt(x,'%s/all'%torun,['SR_bins_EWKino'])
        if '_ewk20_met200_mm' in torun: 
            x = add(x,"--xp TChiNeuWZ_95,TChiNeuWZ_90,T2ttDeg_300,T2ttDeg_315,T2ttDeg_330 -E ^sublepPt5 -E ^MT -E ^mm -E ^highMET")
            runIt(x,'%s/all'%torun,['SR_bins_EWKino'])
        if '_ewk20_met200_ee' in torun: 
            x = add(x,"--xp TChiNeuWZ_95,TChiNeuWZ_90,T2ttDeg_300,T2ttDeg_315,T2ttDeg_330 -E ^sublepPt5 -E ^MT -E ^ee -E ^highMET")
            runIt(x,'%s/all'%torun,['SR_bins_EWKino'])
        if '_stop20_met100_mm' in torun: 
            x = add(x,"--xp TChiNeuWZ_95,TChiNeuWZ_90,TChiNeuWZ_80,T2ttDeg_300,T2ttDeg_315 -E ^sublepPt5 -E ^mm -E ^upperMET")
            runIt(x,'%s/all'%torun,['SR_bins_stop'])
        if '_stop20_met200_mm' in torun: 
            x = add(x,"--xp TChiNeuWZ_95,TChiNeuWZ_90,TChiNeuWZ_80,T2ttDeg_300,T2ttDeg_315 -E ^mm -E ^highMET")
            runIt(x,'%s/all'%torun,['SR_bins_stop'])
        if '_stop20_met200_ee' in torun: 
            x = add(x,"--xp TChiNeuWZ_95,TChiNeuWZ_90,TChiNeuWZ_80,T2ttDeg_300,T2ttDeg_315 -E ^ee -E ^highMET")
            runIt(x,'%s/all'%torun,['SR_bins_stop'])
        if '_stop20_met200_em' in torun: 
            x = add(x,"--xp TChiNeuWZ_95,TChiNeuWZ_90,TChiNeuWZ_80,T2ttDeg_300,T2ttDeg_315 -E ^em -E ^highMET")
            runIt(x,'%s/all'%torun,['SR_bins_stop'])  
        if '_stop35_met100_mm' in torun: 
            x = add(x,"--xp TChiNeuWZ_95,TChiNeuWZ_90,TChiNeuWZ_80,T2ttDeg_300,T2ttDeg_330 -E ^sublepPt5 -E ^mm -E ^upperMET")
            runIt(x,'%s/all'%torun,['SR_bins_stop'])
        if '_stop35_met200_mm' in torun: 
            x = add(x,"--xp TChiNeuWZ_95,TChiNeuWZ_90,TChiNeuWZ_80,T2ttDeg_300,T2ttDeg_330 -E ^mm -E ^highMET")
            runIt(x,'%s/all'%torun,['SR_bins_stop'])
        if '_stop35_met200_ee' in torun: 
            x = add(x,"--xp TChiNeuWZ_95,TChiNeuWZ_90,TChiNeuWZ_80,T2ttDeg_300,T2ttDeg_330 -E ^ee -E ^highMET")
            runIt(x,'%s/all'%torun,['SR_bins_stop'])
        if '_stop35_met200_em' in torun: 
            x = add(x,"--xp TChiNeuWZ_95,TChiNeuWZ_90,TChiNeuWZ_80,T2ttDeg_300,T2ttDeg_330 -E ^em -E ^highMET")
            runIt(x,'%s/all'%torun,['SR_bins_stop'])      
   

    if '2los_CR_DY_vars' in torun:
        x = base('2los')
        x = add(x,"--noStackSig --showIndivSigs --xp TChiNeuWZ_95")
        if '_notrigger' in torun: x = add(x,'-X ^triggerAll ')
        if '_data' in torun: 
            x = x.replace('mca-2los-mc.txt','mca-2los-mcdata.txt')
            x = add(x,"--showRatio --maxRatioRange 0 3") #--showMCError
        if '_met200' in torun:             
            x = add(x,"-X ^HT -X ^Upsilon_veto -R ^ISRjet noIDISRjet 'Jet1_pt > 25 && fabs(Jet1_eta)<2.4' -R ^ledlepPt NoUpledlepPtNoUp '5 < LepGood1_pt' -R METovHT relaxMETovHT '(met_pt/(htJet25-LepGood1_pt-LepGood2_pt))>(2/3)' -E ^highMET -E ^MT -R ^TT CRDYTT 'LepGood1_isTightCRDY && LepGood2_isTightCRDY' -R mtautau Invmtautau '0.<mass_tautau(met_pt,met_phi,LepGood1_pt,LepGood1_eta,LepGood1_phi,LepGood2_pt,LepGood2_eta,LepGood2_phi)&&mass_tautau(met_pt,met_phi,LepGood1_pt,LepGood1_eta,LepGood1_phi,LepGood2_pt,LepGood2_eta,LepGood2_phi)<160.'")
            x = x.replace('-l 5.0','-l 4.0')
        if '_met100' in torun:             
            x = add(x,"-E ^mm -E ^upperMET -E ^MT -R ^ledlepPt NoUpledlepPt '5 < LepGood1_pt' -R ^TT CRDYTT 'LepGood1_isTightCRDY && LepGood2_isTightCRDY' -R mtautau Invmtautau '0.<mass_tautau(met_pt,met_phi,LepGood1_pt,LepGood1_eta,LepGood1_phi,LepGood2_pt,LepGood2_eta,LepGood2_phi)&&mass_tautau(met_pt,met_phi,LepGood1_pt,LepGood1_eta,LepGood1_phi,LepGood2_pt,LepGood2_eta,LepGood2_phi)<160.' -E ^runRange")
            x = x.replace('-l 5.0','-l 1.4')        
        runIt(x,'%s/all'%torun,[],['SR_bins_EWKino','SR_bins_stop'])


    if '2los_CR_TT_vars' in torun:
        x = base('2los')
        x = add(x,"--noStackSig --showIndivSigs --xp TChiNeuWZ_95")
        if '_notrigger' in torun: x = add(x,'-X ^triggerAll ')
        if '_met200' in torun:             
            x = add(x,"-X ^HT -X ^Upsilon_veto -R ^ISRjet noIDISRjet 'Jet1_pt > 25 && fabs(Jet1_eta)<2.4' -R ^ledlepPt NoUpledlepPt '5 < LepGood1_pt' -R METovHT relaxMETovHT '(met_pt/(htJet25-LepGood1_pt-LepGood2_pt))>(2/3)' -E ^highMET -R ^TT CRTTTT 'LepGood1_isTightCRTT && LepGood2_isTightCRTT' -X ^bveto -E ^btag -X ^triggerAll -E ^triggerMET")
            if '_data' in torun: 
                x = x.replace('mca-2los-mc.txt','mca-2los-mcdata.txt')
                x = add(x,"--showRatio --maxRatioRange 0 3") #--showMCError
                x = x.replace('-l 5.0','-l 4.0')
        if '_met100' in torun:             
            x = add(x,"-E ^mm -E ^upperMET -R ^TT TTCRDY 'LepGood1_isTightCRTT && LepGood2_isTightCRTT' -X ^bveto -E ^btag")
            if '_data_singleMu' in torun: 
                x = x.replace('mca-2los-mc.txt','mca-2los-mcdatacr.txt')
                x = add(x,"--showRatio --maxRatioRange 0 3") #--showMCError
                x = x.replace('-l 5.0','-l 2.1')
                x = add(x,"-R ^ledlepPt ledlepPtNoUp '25 < LepGood1_pt' -E ^resEta -X ^triggerAll -E ^triggerMu ")
            if '_data_MET' in torun: 
                x = x.replace('mca-2los-mc.txt','mca-2los-mcdata.txt')
                x = add(x,"--showRatio --maxRatioRange 0 3") #--showMCError
                x = x.replace('-l 5.0','-l 1.4')    
                x = add(x,"-R ^ledlepPt ledlepPtNoUp '5 < LepGood1_pt' -E ^runRange -X ^triggerAll -E ^triggerDoubleMuMET")
        runIt(x,'%s/all'%torun,[],['SR_bins_EWKino','SR_bins_stop'])

  





    #### still to be adapted to SOS        
    # if '2lss_' in torun:
    #     x = base('2lss')
    #     if '_appl' in torun: x = add(x,'-I ^TT ')
    #     if '_1fo' in torun:
    #         x = add(x,"-A alwaystrue 1FO 'LepGood1_isTight+LepGood2_isTight==1'")
    #         x = x.replace("--xP 'nT_.*'","")
    #     if '_2fo' in torun: x = add(x,"-A alwaystrue 2FO 'LepGood1_isTight+LepGood2_isTight==0'")
    #     if '_relax' in torun: x = add(x,'-X ^TT ')
    #     if '_data' in torun: x = x.replace('mca-2lss-mc.txt','mca-2lss-mcdata.txt')
    #     if '_frdata' in torun:
    #         if not '_data' in torun: raise RuntimeError
    #         x = x.replace('mca-2lss-mcdata.txt','mca-2lss-mcdata-frdata.txt')
    #         if '_table' in torun:
    #             x = x.replace('mca-2lss-mcdata-frdata.txt','mca-2lss-mcdata-frdata-table.txt')
    #     if '_mll200' in torun:
    #         x = add(x,"-E ^mll200 ")

    #     if '_splitfakes' in torun:
    #         x = x.replace('mca-2lss-mc.txt','mca-2lss-mc-flavsplit.txt')
            
    #     if '_closuretest' in torun:
    #         x = x.replace('mca-2lss-mc.txt','mca-2lss-mc-closuretest.txt')
    #         x = x.replace("--maxRatioRange 0 3","--maxRatioRange 0.5 1.5")
    #         x = add(x,"--AP --plotmode nostack --sP kinMVA_2lss_ttbar --sP kinMVA_2lss_ttV")
    #         x = add(x,"--ratioDen FR_QCD --ratioNums FR_TT --errors")
    #         if '_closuretest_norm' in torun:
    #             x = x.replace("--plotmode nostack","--plotmode norm")
    #             x = add(x,"--fitRatio 1")
    #         if '_bloose' in torun: x = add(x,'-E ^BLoose ')
    #         if '_btight' in torun: x = add(x,'-E ^BTight ')
    #         if '_nobcut' in torun: x = add(x,'-X ^2b1B ')
    #         if '_notrigger' in torun: x = add(x,'-X ^trigger ')

    #     if '_varsFR' in torun:
    #         torun += "_"+sys.argv[-1]
    #         x = x.replace('mca-2lss-mc.txt','mca-2lss-data-frdata-%s.txt'%sys.argv[-1])
    #         x = x.replace("--maxRatioRange 0 3","--maxRatioRange 0 2")
    #         x = add(x,"--plotmode nostack --sP kinMVA_2lss_ttbar --sP kinMVA_2lss_ttV")
    #         x = add(x,"--ratioDen fakes_data --ratioNums fakes_data_%s --errors"%sys.argv[-1])
    #         if '_varsFR_norm' in torun:
    #             x = x.replace("--plotmode nostack","--plotmode norm")
    #             x = add(x,"--fitRatio 1")

    #     runIt(x,'%s/all'%torun)
    #     if '_flav' in torun:
    #         for flav in ['mm','ee','em']: runIt(add(x,'-E ^%s'%flav),'%s/%s'%(torun,flav))

    # if '3l_' in torun:
    #     x = base('3l')
    #     if '_appl' in torun: x = add(x,'-I ^TTT ')
    #     if '_1fo' in torun:
    #         x = add(x,"-A alwaystrue 1FO 'LepGood1_isTight+LepGood2_isTight+LepGood3_isTight==2'")
    #         x = x.replace("--xP 'nT_.*'","")
    #     if '_relax' in torun: x = add(x,'-X ^TTT ')
    #     if '_data' in torun: x = x.replace('mca-3l-mc.txt','mca-3l-mcdata.txt')
    #     if '_frdata' in torun:
    #         if not '_data' in torun: raise RuntimeError
    #         x = x.replace('mca-3l-mcdata.txt','mca-3l-mcdata-frdata.txt')
    #         if '_table' in torun:
    #             x = x.replace('mca-3l-mcdata-frdata.txt','mca-3l-mcdata-frdata-table.txt')
    #     if '_closuretest' in torun:
    #         x = x.replace('mca-3l-mc.txt','mca-3l-mc-closuretest.txt')
    #         x = x.replace("--maxRatioRange 0 3","--maxRatioRange 0.5 1.5")
    #         x = add(x,"--AP --plotmode nostack --sP kinMVA_3l_ttbar --sP kinMVA_3l_ttV")
    #         x = add(x,"--ratioDen FR_QCD --ratioNums FR_TT --errors")
    #         if '_closuretest_norm' in torun:
    #             x = x.replace("--plotmode nostack","--plotmode norm")
    #             x = add(x,"--fitRatio 1")
    #         if '_notrigger' in torun: x = add(x,'-X ^trigger ')
    #     if '_varsFR' in torun:
    #         torun += "_"+sys.argv[-1]
    #         x = x.replace('mca-3l-mc.txt','mca-3l-data-frdata-%s.txt'%sys.argv[-1])
    #         x = x.replace("--maxRatioRange 0 3","--maxRatioRange 0 2")
    #         x = add(x,"--plotmode nostack --sP kinMVA_3l_ttbar --sP kinMVA_3l_ttV")
    #         x = add(x,"--ratioDen fakes_data --ratioNums fakes_data_%s --errors"%sys.argv[-1])
    #         if '_varsFR_norm' in torun:
    #             x = x.replace("--plotmode nostack","--plotmode norm")
    #             x = add(x,"--fitRatio 1")
    #     if '_x2j' in torun:
    #         x = add(x,"-E ^x2j ")
    #     runIt(x,'%s'%torun)

    # if 'cr_3j' in torun:
    #     x = base('2lss')
    #     if '_data' in torun: x = x.replace('mca-2lss-mc.txt','mca-2lss-mcdata.txt')
    #     if '_frdata' in torun:
    #         if not '_data' in torun: raise RuntimeError
    #         x = x.replace('mca-2lss-mcdata.txt','mca-2lss-mcdata-frdata.txt')
    #     x = add(x,"-R ^4j 3j 'nJet25==3'")
    #     plots = ['nJet25','nBJetLoose25','nBJetMedium25','met','metLD','htJet25j','mhtJet25','mtWmin','htllv','kinMVA_2lss_ttbar','kinMVA_2lss_ttV','kinMVA_2lss_bins']
    #     runIt(x,'%s/all'%torun,plots)
    #     if '_flav' in torun:
    #         for flav in ['mm','ee','em']:
    #             runIt(add(x,'-E ^%s '%flav),'%s/%s'%(torun,flav),plots)

    # if 'cr_ttbar' in torun:
    #     x = base('2lss')
    #     x = fulltrees(x) # for mc same-sign
    #     x = x.replace('mca-2lss-mc.txt','mca-2lss-mcdata-ttbar.txt')
    #     if '_data' not in torun: x = add(x,'--xp data')
    #     if '_appl' in torun: x = add(x,'-I ^TT ')
    #     if '_1fo' in torun: x = add(x,"-A alwaystrue 1FO 'LepGood1_isTight+LepGood2_isTight==1'")
    #     if '_leadmupt25' in torun: x = add(x,"-A 'entry point' leadmupt25 'abs(LepGood1_pdgId)==13 && LepGood1_pt>25'")
    #     x = add(x,"-I same-sign -X ^4j -X ^2b1B -E ^2j -E ^em ")
    #     if '_highMetNoBCut' in torun: x = add(x,"-A 'entry point' highMET 'met_pt>60'")
    #     else: x = add(x,"-E ^1B ")
    #     plots = ['2lep_bestMVA','2lep_worseMVA','met','metLD','nVert','nJet25','nBJetMedium25','nBJetLoose25','nBJetLoose40','nBJetMedium40']
    #     runIt(x,'%s'%torun,plots)

    # if 'cr_zjets' in torun:
    #     x = base('2lss')
    #     x = fulltrees(x) # for mc same-sign
    #     x = x.replace('mca-2lss-mc.txt','mca-2lss-mcdata-ttbar.txt')
    #     x = x.replace('--maxRatioRange 0 3','--maxRatioRange 0.8 1.2')
    #     if '_data' not in torun: x = add(x,'--xp data')
    #     x = add(x,"-I same-sign -X ^2b1B -X ^Zee_veto -A alwaystrue mZ 'mZ1>60 && mZ1<120'")
    #     for flav in ['mm','ee']:
    #         runIt(add(x,'-E ^%s -X ^4j'%flav),'%s/%s'%(torun,flav))
    #         runIt(add(x,'-E ^%s -X ^4j -E ^2j '%flav),'%s_2j/%s'%(torun,flav))
    #         runIt(add(x,'-E ^%s '%flav),'%s_4j/%s'%(torun,flav))

    # if 'cr_wz' in torun:
    #     x = base('3l')
    #     if '_data' in torun: x = x.replace('mca-3l-mc.txt','mca-3l-mcdata.txt')
    #     if '_frdata' in torun:
    #         if not '_data' in torun: raise RuntimeError
    #         x = x.replace('mca-3l-mcdata.txt','mca-3l-mcdata-frdata.txt')
    #     x = add(x,"-I 'Zveto' -X ^2b1B -E ^Bveto ")
    #     plots = ['lep3_pt','metLD','nBJetLoose25','3lep_worseIso','minMllAFAS','3lep_worseMVA','3lep_mtW']
    #     runIt(x,'%s'%torun,plots)

    # if 'cr_ttz' in torun:
    #     x = base('3l')
    #     if '_data' in torun: x = x.replace('mca-3l-mc.txt','mca-3l-mcdata.txt')
    #     if '_frdata' in torun:
    #         if not '_data' in torun: raise RuntimeError
    #         x = x.replace('mca-3l-mcdata.txt','mca-3l-mcdata-frdata.txt')
    #     plots = ['lep2_pt','met','nJet25','mZ1']
    #     x = add(x,"-I 'Zveto' -X ^2b1B -E ^gt2b -E ^1B ")
    #     runIt(x,'%s'%torun,plots)
    #     x = add(x,"-E ^4j ")
    #     runIt(x,'%s_4j'%torun,plots)

