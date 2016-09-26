#!/usr/bin/env python
import sys
import re

ODIR=sys.argv[1]

dowhat = "plots" 
#dowhat = "dumps" 
#dowhat = "yields" 
#dowhat = "limits"

if dowhat == "limits":
    # SYST="susy-sos/syst/susy_sos_dummy.txt" ## change file for systematics here
    SYST="susy-sos/syst/susy_sos_syst_scan.txt"
    PLOTandCUTS="" ## check later where is initialized. You need to specify there the mca, since they will not be replaced as for "plots" (due to different input order of combineCards)


def base(selection):

    
    CORE="-P /data1/botta/trees_SOS_80X_130716_Scans/ --FMCs {P}/eventBTagWeight"
    CORE+=" -f -j 8 -l 12.9 --s2v --tree treeProducerSusyMultilepton --mcc susy-sos/mcc-lepWP.txt --mcc susy-sos/mcc-sf1.txt --neg" #--mcc susy-sos/2los_triggerdefs.txt # "
    if dowhat == "plots": CORE+=" --lspam 'CMS Preliminary' --legendWidth 0.14 --legendFontSize 0.04"
    GO = ""
    if selection=='2los':
        if (dowhat != "limits") : GO="susy-sos/susy-sos/mca-2los-mc.txt susy-sos/2los_tight.txt "
        GO="%s %s"%(CORE,GO) 
        GO="%s -L susy-sos/lepton_trigger_SF.cc -W 'leptonSF_SOS(LepGood1_pdgId,LepGood1_pt,LepGood1_eta,0)*leptonSF_SOS(LepGood2_pdgId,LepGood2_pt,LepGood2_eta,0)*triggerSF_SOS(met_pt,metmm_pt(LepGood1_pdgId,LepGood1_pt,LepGood1_phi,LepGood2_pdgId,LepGood2_pt,LepGood2_phi,met_pt,met_phi),0)*puw2016_vtx_13fb(nVert)*eventBTagSF'"%GO 
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
    elif (dowhat == "limits" and ('_unblind' in name)): 
        # comment: for the moment recycling plots and noplots as a container for histo name and binning when running 'limits' mode (to be improved) 
        print 'echo %s; python makeShapeCardsSusy.py'%name,PLOTandCUTS,' '.join(['%s'%p for p in plots]),' '.join(['%s'%p for p in noplots]),SYST,' -o %s'%name,' ',GO," --od %s"%(ODIR),' '.join(sys.argv[3:])
    elif (dowhat == "limits" and ('_unblind' in name)==0 ):
        # comment: for the moment recycling plots and noplots as a container for histo name and binning when running in 'limits' mode (to be improved) 
        print 'echo %s; python makeShapeCardsSusy.py'%name,PLOTandCUTS,' '.join(['%s'%p for p in plots]),' '.join(['%s'%p for p in noplots]),SYST,' -o %s'%name,' ',GO," --od %s"%(ODIR),' --asimov',' '.join(sys.argv[3:])
    else:
        raise RuntimeError, 'Unknown selection'
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

    if '_ddbkg' in torun:
        PLOTandCUTS="susy-sos/mca-2los-mc-frdata.txt susy-sos/2los_tight.txt"
    elif '_unblind' in torun:
        if(('CR_TT_' in torun) or ('CR_DY_' in torun)): 
            #PLOTandCUTS="susy-sos/mca-2los-mcdata-mcfakes.txt susy-sos/2los_tight.txt"
            PLOTandCUTS="susy-sos/mca-2los-mcdata-mcfakes_FastSimTChi.txt susy-sos/2los_tight.txt" ## for running on scan 
        else:
            #PLOTandCUTS="susy-sos/mca-2los-mcdata-frdata.txt susy-sos/2los_tight.txt"
            PLOTandCUTS="susy-sos/mca-2los-mcdata-mcfakes_FastSimTChi.txt susy-sos/2los_tight.txt" ## for running on scan 
    else:
        PLOTandCUTS="susy-sos/mca-2los-mc.txt susy-sos/2los_tight.txt" 
        

    ### MC Distributions with Signal shapes normalized to Bkg, n-minus1 option
    if '2los_SR_vars' in torun:
        x = base('2los')
        if 'ewk_met200' in torun: 
            x = add(x,"-E ^highMET -X ^triggerAll -E ^triggerMET -E ^SF -E ^pt5sublep -E ^MT") 
            if '_unblind' in torun:
                x = add(x,"--noStackSig --showIndivSigs --showRatio --maxRatioRange -2 5 --showMCError") 
                #x = add(x,"--plotmode norm")
                x = x.replace('-l 12.9','-l 12.9')
                x = x.replace('mca-2los-mc.txt','mca-2los-mcdata-frdata.txt') #remove signal
                x = x.replace('mcc-sf1.txt','mcc-sf-highmet.txt') 
        if 'ewk_met125' in torun: 
            x = add(x,"-E ^upperMET -E ^mm -E ^runRange -X ^triggerAll -E ^triggerDoubleMuMET -E ^pt5sublep -E ^MT")
            if '_unblind' in torun:
                x = add(x,"--noStackSig --showIndivSigs --showRatio --maxRatioRange -2 5 --showMCError") 
                #x = add(x,"--plotmode norm")
                x = x.replace('-l 12.9','-l 10.1')
                x = x.replace('puw2016_vtx_4fb(nVert)', 'puw2016_vtx_postTS_1p4fb(nVert)' )
                x = x.replace('mca-2los-mc.txt','mca-2los-mcdata-frdata.txt') #remove signal
                x = x.replace('mcc-sf1.txt','mcc-sf-lowmet.txt')
        if 'stop_met200' in torun: 
            x = add(x,"-E ^highMET -X ^triggerAll -E ^triggerMET ") 
            if '_unblind' in torun:
                x = add(x,"--noStackSig --showIndivSigs --showRatio --maxRatioRange -2 5 --showMCError") 
                #x = add(x,"--plotmode norm")
                x = x.replace('-l 12.9','-l 12.9')
                x = x.replace('mca-2los-mc.txt','mca-2los-mcdata-frdata.txt') #remove signal
                x = x.replace('mcc-sf1.txt','mcc-sf-highmet.txt')
        if 'stop_met125' in torun: 
            x = add(x,"-E ^upperMET -E ^mm -E ^runRange -X ^triggerAll -E ^triggerDoubleMuMET -E ^pt5sublep ")
            if '_unblind' in torun:
                x = add(x,"--noStackSig --showIndivSigs --showRatio --maxRatioRange -2 5 --showMCError") 
                #x = add(x,"--plotmode norm")
                x = x.replace('-l 12.9','-l 10.1')
                x = x.replace('puw2016_vtx_4fb(nVert)', 'puw2016_vtx_postTS_1p4fb(nVert)' )
                x = x.replace('mca-2los-mc.txt','mca-2los-mcdata-frdata.txt') #remove signal
                x = x.replace('mcc-sf1.txt','mcc-sf-lowmet.txt')
        if '_nminus1' in torun: 
            x = add(x,"--n-minus-one")
            x = x.replace('-f','')
            x = add(x,"--noStackSig --showIndivSigShapes --xp TChiNeuWZ_95,T2ttDeg_300,T2ttDeg_315")
            #x = add(x,"--plotmode norm")
        runIt(x,'%s/all'%torun,[],['SR_bins_EWKino','SR_bins_stop'])



    ### SR plots: Pure MC Sig+Bkg, Data-Driven Bkgs, Variations for TT and DY syst, Application region Bins, DATA!
    if '2los_SR_bins' in torun:
        x = base('2los')
        if(dowhat != "limits"): x = add(x,"--perBin")
        if '_ewk10_met125_mm' in torun: 
            x = add(x,"--xp TChiNeuWZ_95,TChiNeuWZ_80,T2ttDeg_300,T2ttDeg_315,T2ttDeg_330 -E ^pt5sublep -E ^MT -E ^mm -E ^upperMET -E ^runRange -X ^triggerAll -E ^triggerDoubleMuMET ")  
            #x = add(x,"-E ^pt5sublep -E ^MT -E ^mm -E ^upperMET -E ^runRange -X ^triggerAll -E ^triggerDoubleMuMET ")  ## (for scan)
            x = x.replace('-l 12.9','-l 10.1')  
            x = x.replace('puw2016_vtx_4fb(nVert)', 'puw2016_vtx_postTS_1p4fb(nVert)' )
            if '_syst' in torun: 
                x = add(x,"--plotmode nostack -F sf/t /data1/botta/trees_SOS_80X_170616/SOS13TeV_Friends/evVarFriend_{cname}.root")
                if '_TT' in torun:
                    x = x.replace('mca-2los-mc.txt','mca-2los-mc-syst-tt.txt')
                if '_DY' in torun:
                    x = x.replace('mca-2los-mc.txt','mca-2los-mc-syst-dy.txt')
            if '_ddbkg' in torun: 
                x = x.replace('mca-2los-mc.txt','mca-2los-mc-frdata.txt')
                if(dowhat != "limits"):x = x.replace('mcc-sf1.txt','mcc-sf-lowmet.txt') 
            if '_appl' in torun:
                x = x.replace('mca-2los-mc.txt','mca-2los-mcdata.txt')
                x = add(x,"-I ^TT ")
            if '_unblind' in torun:
                if(dowhat != "limits"):x = add(x,"--noStackSig --showIndivSigs --showRatio --maxRatioRange -2 5 --showMCError") 
                x = x.replace('mca-2los-mc.txt','mca-2los-mcdata-frdata.txt')
                if(dowhat != "limits"):x = x.replace('mcc-sf1.txt','mcc-sf-lowmet.txt') 
            if dowhat == "limits":
                runIt(x,torun,["m2l"],["'[4,10,20,30,50]'"])
            else:
                runIt(x,'%s/all'%torun,['SR_bins_EWKino'])                 
        if '_ewk10_met200' in torun: 
            x = add(x,"--xp TChiNeuWZ_95,TChiNeuWZ_80,T2ttDeg_300,T2ttDeg_315,T2ttDeg_330 -E ^pt5sublep -E ^MT -E ^SF -E ^highMET -X ^triggerAll -E ^triggerMET ")
            #x = add(x,"-E ^pt5sublep -E ^MT -E ^SF -E ^highMET -X ^triggerAll -E ^triggerMET ") ## (for scan)
            if '_syst' in torun: 
                x = add(x,"--plotmode nostack -F sf/t /data1/botta/trees_SOS_80X_170616/SOS13TeV_Friends/evVarFriend_{cname}.root")
                if '_TT' in torun:
                    x = x.replace('mca-2los-mc.txt','mca-2los-mc-syst-tt.txt')
                if '_DY' in torun:
                    x = x.replace('mca-2los-mc.txt','mca-2los-mc-syst-dy.txt')
            if '_ddbkg' in torun: 
                x = x.replace('mca-2los-mc.txt','mca-2los-mc-frdata.txt')
                if(dowhat != "limits"):x = x.replace('mcc-sf1.txt','mcc-sf-highmet.txt') 
            if '_appl' in torun:
                x = x.replace('mca-2los-mc.txt','mca-2los-mcdata.txt')
                x = add(x,"-I ^TT ")
            if '_unblind' in torun:
                if(dowhat != "limits"):x = add(x,"--noStackSig --showIndivSigs --showRatio --maxRatioRange -2 5 --showMCError") 
                x = x.replace('mca-2los-mc.txt','mca-2los-mcdata-frdata.txt') 
                if(dowhat != "limits"):x = x.replace('mcc-sf1.txt','mcc-sf-highmet.txt') 
            if dowhat == "limits":
                runIt(x,torun,["m2l"],["'[4,10,20,30,50]'"])
            else:
                runIt(x,'%s/all'%torun,['SR_bins_EWKino'])
        ###############################    
        if '_ewk20_met125_mm' in torun: 
            x = add(x,"--xp TChiNeuWZ_95,TChiNeuWZ_90,T2ttDeg_300,T2ttDeg_315,T2ttDeg_330 -E ^pt5sublep -E ^MT -E ^mm -E ^upperMET -E ^runRange -X ^triggerAll -E ^triggerDoubleMuMET ")
            x = x.replace('-l 12.9','-l 10.1') 
            x = x.replace('puw2016_vtx_4fb(nVert)', 'puw2016_vtx_postTS_1p4fb(nVert)' )
            if '_syst' in torun: 
                x = add(x,"--plotmode nostack -F sf/t /data1/botta/trees_SOS_80X_170616/SOS13TeV_Friends/evVarFriend_{cname}.root")
                if '_TT' in torun:
                    x = x.replace('mca-2los-mc.txt','mca-2los-mc-syst-tt.txt')
                if '_DY' in torun:
                    x = x.replace('mca-2los-mc.txt','mca-2los-mc-syst-dy.txt')
            if '_ddbkg' in torun: 
                x = x.replace('mca-2los-mc.txt','mca-2los-mc-frdata.txt')
                if(dowhat != "limits"):x = x.replace('mcc-sf1.txt','mcc-sf-lowmet.txt') 
            if '_appl' in torun:
                x = x.replace('mca-2los-mc.txt','mca-2los-mcdata.txt')
                x = add(x,"-I ^TT ")  
            if '_unblind' in torun:
                if(dowhat != "limits"):x = add(x,"--noStackSig --showIndivSigs --showRatio --maxRatioRange -2 5 --showMCError") 
                x = x.replace('mca-2los-mc.txt','mca-2los-mcdata-frdata.txt') 
                if(dowhat != "limits"):x = x.replace('mcc-sf1.txt','mcc-sf-lowmet.txt') 
            if dowhat == "limits":
                runIt(x,torun,["m2l"],["'[4,10,20,30,50]'"])
            else:
                runIt(x,'%s/all'%torun,['SR_bins_EWKino'])
        if '_ewk20_met200' in torun: 
            x = add(x,"--xp TChiNeuWZ_95,TChiNeuWZ_90,T2ttDeg_300,T2ttDeg_315,T2ttDeg_330 -E ^pt5sublep -E ^MT -E ^SF -E ^highMET -X ^triggerAll -E ^triggerMET ")
            if '_syst' in torun: 
                x = add(x,"--plotmode nostack -F sf/t /data1/botta/trees_SOS_80X_170616/SOS13TeV_Friends/evVarFriend_{cname}.root")
                if '_TT' in torun:
                    x = x.replace('mca-2los-mc.txt','mca-2los-mc-syst-tt.txt')
                if '_DY' in torun:
                    x = x.replace('mca-2los-mc.txt','mca-2los-mc-syst-dy.txt')
            if '_ddbkg' in torun: 
                x = x.replace('mca-2los-mc.txt','mca-2los-mc-frdata.txt')
                if(dowhat != "limits"):x = x.replace('mcc-sf1.txt','mcc-sf-highmet.txt') 
            if '_appl' in torun:
                x = x.replace('mca-2los-mc.txt','mca-2los-mcdata.txt') 
                x = add(x,"-I ^TT ")
            if '_unblind' in torun:
                if(dowhat != "limits"):x = add(x,"--noStackSig --showIndivSigs --showRatio --maxRatioRange -2 5 --showMCError") 
                x = x.replace('mca-2los-mc.txt','mca-2los-mcdata-frdata.txt') 
                if(dowhat != "limits"):x = x.replace('mcc-sf1.txt','mcc-sf-highmet.txt')
            if dowhat == "limits":
                runIt(x,torun,["m2l"],["'[4,10,20,30,50]'"])
            else:
                runIt(x,'%s/all'%torun,['SR_bins_EWKino'])
        ###############################    
        if '_stop20_met125_mm' in torun: 
            x = add(x,"--xp TChiNeuWZ_95,TChiNeuWZ_90,TChiNeuWZ_80,T2ttDeg_300,T2ttDeg_315 -E ^pt5sublep -E ^mm -E ^upperMET -E ^runRange -X ^triggerAll -E ^triggerDoubleMuMET ")
            #x = add(x,"-E ^pt5sublep -E ^mm -E ^upperMET -E ^runRange -X ^triggerAll -E ^triggerDoubleMuMET ")
            x = x.replace('-l 12.9','-l 10.1')
            x = x.replace('puw2016_vtx_4fb(nVert)', 'puw2016_vtx_postTS_1p4fb(nVert)' )
            if '_syst' in torun: 
                x = add(x,"--plotmode nostack -F sf/t /data1/botta/trees_SOS_80X_170616/SOS13TeV_Friends/evVarFriend_{cname}.root")
                if '_TT' in torun:
                    x = x.replace('mca-2los-mc.txt','mca-2los-mc-syst-tt.txt')
                if '_DY' in torun:
                    x = x.replace('mca-2los-mc.txt','mca-2los-mc-syst-dy.txt')
            if '_ddbkg' in torun: 
                x = x.replace('mca-2los-mc.txt','mca-2los-mc-frdata.txt')
                if(dowhat != "limits"):x = x.replace('mcc-sf1.txt','mcc-sf-lowmet.txt') 
            if '_appl' in torun:
                x = x.replace('mca-2los-mc.txt','mca-2los-mcdata.txt')
                x = add(x,"-I ^TT ")
            if '_unblind' in torun:
                if(dowhat != "limits"):x = add(x,"--noStackSig --showIndivSigs --showRatio --maxRatioRange -2 5 --showMCError") 
                x = x.replace('mca-2los-mc.txt','mca-2los-mcdata-frdata.txt')  
                if(dowhat != "limits"):x = x.replace('mcc-sf1.txt','mcc-sf-lowmet.txt') 
            if dowhat == "limits":
                runIt(x,torun,["LepGood1_pt"],["'[5,12,20,30]'"])
            else:
                runIt(x,'%s/all'%torun,['SR_bins_stop'])
        if '_stop20_met200' in torun: 
            x = add(x,"--xp TChiNeuWZ_95,TChiNeuWZ_90,TChiNeuWZ_80,T2ttDeg_300,T2ttDeg_315 -E ^highMET -X ^triggerAll -E ^triggerMET ")
            #x = add(x,"-E ^highMET -X ^triggerAll -E ^triggerMET ")
            if '_syst' in torun: 
                x = add(x,"--plotmode nostack -F sf/t /data1/botta/trees_SOS_80X_170616/SOS13TeV_Friends/evVarFriend_{cname}.root")
                if '_TT' in torun:
                    x = x.replace('mca-2los-mc.txt','mca-2los-mc-syst-tt.txt')
                if '_DY' in torun:
                    x = x.replace('mca-2los-mc.txt','mca-2los-mc-syst-dy.txt')
            if '_ddbkg' in torun: 
                x = x.replace('mca-2los-mc.txt','mca-2los-mc-frdata.txt')
                if(dowhat != "limits"):x = x.replace('mcc-sf1.txt','mcc-sf-highmet.txt')
            if '_appl' in torun:
                x = x.replace('mca-2los-mc.txt','mca-2los-mcdata.txt')
                x = add(x,"-I ^TT ")   
            if '_unblind' in torun:
                if(dowhat != "limits"):x = add(x,"--noStackSig --showIndivSigs --showRatio --maxRatioRange -2 5 --showMCError") 
                x = x.replace('mca-2los-mc.txt','mca-2los-mcdata-frdata.txt')  
                if(dowhat != "limits"):x = x.replace('mcc-sf1.txt','mcc-sf-highmet.txt') 
            if dowhat == "limits":
                runIt(x,torun,["LepGood1_pt"],["'[5,12,20,30]'"])
            else:
                runIt(x,'%s/all'%torun,['SR_bins_stop'])    
        ###############################        
        if '_stop35_met125_mm' in torun: 
            x = add(x,"--xp TChiNeuWZ_95,TChiNeuWZ_90,TChiNeuWZ_80,T2ttDeg_300,T2ttDeg_330 -E ^pt5sublep -E ^mm -E ^upperMET -E ^runRange -X ^triggerAll -E ^triggerDoubleMuMET ")
            x = x.replace('-l 12.9','-l 10.1') 
            x = x.replace('puw2016_vtx_4fb(nVert)', 'puw2016_vtx_postTS_1p4fb(nVert)' )
            if '_syst' in torun: 
                x = add(x,"--plotmode nostack -F sf/t /data1/botta/trees_SOS_80X_170616/SOS13TeV_Friends/evVarFriend_{cname}.root")
                if '_TT' in torun:
                    x = x.replace('mca-2los-mc.txt','mca-2los-mc-syst-tt.txt')
                if '_DY' in torun:
                    x = x.replace('mca-2los-mc.txt','mca-2los-mc-syst-dy.txt')
            if '_ddbkg' in torun: 
                x = x.replace('mca-2los-mc.txt','mca-2los-mc-frdata.txt')
                if(dowhat != "limits"):x = x.replace('mcc-sf1.txt','mcc-sf-lowmet.txt') 
            if '_appl' in torun:
                x = x.replace('mca-2los-mc.txt','mca-2los-mcdata.txt')
                x = add(x,"-I ^TT ")
            if '_unblind' in torun:
                if(dowhat != "limits"):x = add(x,"--noStackSig --showIndivSigs --showRatio --maxRatioRange -2 5 --showMCError") 
                x = x.replace('mca-2los-mc.txt','mca-2los-mcdata-frdata.txt')
                if(dowhat != "limits"):x = x.replace('mcc-sf1.txt','mcc-sf-lowmet.txt')
            if dowhat == "limits":
                runIt(x,torun,["LepGood1_pt"],["'[5,12,20,30]'"])
            else:
                runIt(x,'%s/all'%torun,['SR_bins_stop'])
        if '_stop35_met200' in torun: 
            x = add(x,"--xp TChiNeuWZ_95,TChiNeuWZ_90,TChiNeuWZ_80,T2ttDeg_300,T2ttDeg_330 -E ^highMET -X ^triggerAll -E ^triggerMET ")
            if '_syst' in torun: 
                x = add(x,"--plotmode nostack -F sf/t /data1/botta/trees_SOS_80X_170616/SOS13TeV_Friends/evVarFriend_{cname}.root")
                if '_TT' in torun:
                    x = x.replace('mca-2los-mc.txt','mca-2los-mc-syst-tt.txt')
                if '_DY' in torun:
                    x = x.replace('mca-2los-mc.txt','mca-2los-mc-syst-dy.txt')
            if '_ddbkg' in torun: 
                x = x.replace('mca-2los-mc.txt','mca-2los-mc-frdata.txt')
                if(dowhat != "limits"):x = x.replace('mcc-sf1.txt','mcc-sf-highmet.txt')
            if '_appl' in torun:
                x = x.replace('mca-2los-mc.txt','mca-2los-mcdata.txt')
                x = add(x,"-I ^TT ")
            if '_unblind' in torun:
                if(dowhat != "limits"):x = add(x,"--noStackSig --showIndivSigs --showRatio --maxRatioRange -2 5 --showMCError") 
                x = x.replace('mca-2los-mc.txt','mca-2los-mcdata-frdata.txt') 
                if(dowhat != "limits"):x = x.replace('mcc-sf1.txt','mcc-sf-highmet.txt')
            if dowhat == "limits":
                runIt(x,torun,["LepGood1_pt"],["'[5,12,20,30]'"])
            else:
                runIt(x,'%s/all'%torun,['SR_bins_stop'])
            


    ### FR Application region, Data-MC, LowMET and HighMET 
    if '2los_CR_FF_vars' in torun:
        x = base('2los')
        x = add(x,"--noStackSig --showIndivSigs --xp TChiNeuWZ_95")
        if '_data' in torun: 
            x = x.replace('mca-2los-mc.txt','mca-2los-mcdata.txt')
            x = add(x,"--showRatio --maxRatioRange -2 5 ") #--showMCError 
        if '_met200_ewk_all' in torun:             
            x = add(x,"-E ^highMET -X ^triggerAll -E ^triggerMET -I ^TT -E ^pt5sublep -E ^SF -E ^MT") 
            x = x.replace('-l 12.9','-l 12.9')
        if '_met125_ewk_all' in torun: 
            x = x.replace('puw2016_vtx_4fb(nVert)', 'puw2016_vtx_postTS_1p4fb(nVert)' )
            x = add(x,"-E ^mm -E ^upperMET -E ^runRange -X ^triggerAll -E ^triggerDoubleMuMET -I ^TT -E ^pt5sublep -E ^MT") 
            x = x.replace('-l 12.9','-l 10.1')  
        if '_met200_stop_all' in torun:             
            x = add(x,"-E ^highMET -X ^triggerAll -E ^triggerMET -I ^TT") 
            x = x.replace('-l 12.9','-l 12.9')
        if '_met125_stop_all' in torun: 
            x = x.replace('puw2016_vtx_4fb(nVert)', 'puw2016_vtx_postTS_1p4fb(nVert)' )
            x = add(x,"-E ^mm -E ^upperMET -E ^runRange -X ^triggerAll -E ^triggerDoubleMuMET -I ^TT -E ^pt5sublep") 
            x = x.replace('-l 12.9','-l 10.1')  
        if '_met200_ewk_1T1F' in torun:             
            x = add(x,"-E ^highMET -X ^triggerAll -E ^triggerMET -E ^pt5sublep -E ^SF -E ^MT -X ^TT -E ^TnotT") 
            x = x.replace('-l 12.9','-l 12.9')
        if '_met125_ewk_1T1F' in torun: 
            x = x.replace('puw2016_vtx_4fb(nVert)', 'puw2016_vtx_postTS_1p4fb(nVert)' )
            x = add(x,"-E ^mm -E ^upperMET -E ^runRange -X ^triggerAll -E ^triggerDoubleMuMET -E ^pt5sublep -E ^MT -X ^TT -E ^TnotT") 
            x = x.replace('-l 12.9','-l 10.1')  
        if '_met200_stop_1T1F' in torun:             
            x = add(x,"-E ^highMET -X ^triggerAll -E ^triggerMET -X ^TT -E ^TnotT")  
            x = x.replace('-l 12.9','-l 12.9')
        if '_met125_stop_1T1F' in torun: 
            x = x.replace('puw2016_vtx_4fb(nVert)', 'puw2016_vtx_postTS_1p4fb(nVert)' )
            x = add(x,"-E ^mm -E ^upperMET -E ^runRange -X ^triggerAll -E ^triggerDoubleMuMET -E ^pt5sublep -X ^TT -E ^TnotT") 
            x = x.replace('-l 12.9','-l 10.1')
        if '_met200_ewk_1F1F' in torun:             
            x = add(x,"-E ^highMET -X ^triggerAll -E ^triggerMET -E ^pt5sublep -E ^SF -E ^MT -X ^TT -E ^notTnotT") 
            x = x.replace('-l 12.9','-l 12.9')
        if '_met125_ewk_1F1F' in torun: 
            x = x.replace('puw2016_vtx_4fb(nVert)', 'puw2016_vtx_postTS_1p4fb(nVert)' )
            x = add(x,"-E ^mm -E ^upperMET -E ^runRange -X ^triggerAll -E ^triggerDoubleMuMET -E ^pt5sublep -E ^MT -X ^TT -E ^notTnotT") 
            x = x.replace('-l 12.9','-l 10.1')  
        if '_met200_stop_1F1F' in torun:             
            x = add(x,"-E ^highMET -X ^triggerAll -E ^triggerMET -X ^TT -E ^notTnotT")  
            x = x.replace('-l 12.9','-l 12.9')
        if '_met125_stop_1F1F' in torun: 
            x = x.replace('puw2016_vtx_4fb(nVert)', 'puw2016_vtx_postTS_1p4fb(nVert)' )
            x = add(x,"-E ^mm -E ^upperMET -E ^runRange -X ^triggerAll -E ^triggerDoubleMuMET -E ^pt5sublep -X ^TT -E ^notTnotT") 
            x = x.replace('-l 12.9','-l 10.1')         
        runIt(x,'%s/all'%torun,[],['SR_bins_EWKino','SR_bins_stop'])


        
    ### FR WJets closure
    if '2los_FR_Closure_vars' in torun:
        x = base('2los')
        x = add(x,"--plotmode nostack")
        x = x.replace('mca-2los-mc.txt','mca-2los-mc-closuretest.txt')
        x = add(x,"-X lowMET -X HT -X METovHT --showRatio --maxRatioRange 0.5 1.5 --ratioDen QCDFR_WJets --ratioNums WJets") 
        runIt(x,'%s/all'%torun)



   ### SS Stop-like Control Regio (high MET)

    if '2los_CR_SS' in torun: 
        x = base('2los')
        x = add(x,"-E ^highMET -X ^triggerAll -E ^triggerMET -X ^opposite-sign -E ^same-sign")
        if(dowhat != "limits"): x = add(x,"--noStackSig --showIndivSigs --xp TChiNeuWZ_95")
        #elif '_ewk20'in torun : x = add(x,"--xp TChiNeuWZ_95,TChiNeuWZ_90,T2ttDeg_300,T2ttDeg_315,T2ttDeg_330")
        #elif '_ewk10'in torun : x = add(x,"--xp TChiNeuWZ_95,TChiNeuWZ_80,T2ttDeg_300,T2ttDeg_315,T2ttDeg_330")
        #elif '_stop20'in torun : x = add(x,"--xp TChiNeuWZ_95,TChiNeuWZ_90,TChiNeuWZ_80,T2ttDeg_300,T2ttDeg_315")
        #elif '_stop35'in torun : x = add(x,"--xp TChiNeuWZ_95,TChiNeuWZ_90,TChiNeuWZ_80,T2ttDeg_300,T2ttDeg_330")
        else: 1==1 
        if '_syst' in torun: 
            x = add(x,"--plotmode nostack -F sf/t /data1/botta/trees_SOS_80X_170616/SOS13TeV_Friends/evVarFriend_{cname}.root")
            if '_TT' in torun:
                x = x.replace('mca-2los-mc.txt','mca-2los-mc-syst-tt.txt')
            if '_DY' in torun:
                x = x.replace('mca-2los-mc.txt','mca-2los-mc-syst-dy.txt')
        if '_ddbkg' in torun: 
            x = x.replace('mca-2los-mc.txt','mca-2los-mc-frdata.txt')
            if(dowhat != "limits"):x = x.replace('mcc-sf1.txt','mcc-sf-highmet.txt')
        if '_appl' in torun:
            x = x.replace('mca-2los-mc.txt','mca-2los-mcdata.txt')
            x = add(x,"-I ^TT ")   
        if '_unblind' in torun:
            if(dowhat != "limits"):x = add(x,"--noStackSig --showIndivSigs --showRatio --maxRatioRange -2 5 --showMCError") 
            if(dowhat != "limits"):x = x.replace('mcc-sf1.txt','mcc-sf-highmet.txt') 
            x = x.replace('mca-2los-mc.txt','mca-2los-mcdata-frdata.txt')  
        if dowhat == "limits":
            runIt(x,torun,["LepGood1_pt"],["'[5,12,20,30]'"])
        else:
            runIt(x,'%s/all'%torun,['SR_bins_stop'])    

    #####################################

    
    ### DY Control Region Data-MC and syst variations, LowMET and HighMET     
    if '2los_CR_DY_vars' in torun:
        x = base('2los')
        if(dowhat != "limits"): x = add(x,"--noStackSig --showIndivSigs --xp TChiNeuWZ_95")
        #elif '_ewk20'in torun : x = add(x,"--xp TChiNeuWZ_95,TChiNeuWZ_90,T2ttDeg_300,T2ttDeg_315,T2ttDeg_330")
        #elif '_ewk10'in torun : x = add(x,"--xp TChiNeuWZ_95,TChiNeuWZ_80,T2ttDeg_300,T2ttDeg_315,T2ttDeg_330")
        #elif '_stop20'in torun : x = add(x,"--xp TChiNeuWZ_95,TChiNeuWZ_90,TChiNeuWZ_80,T2ttDeg_300,T2ttDeg_315")
        #elif '_stop35'in torun : x = add(x,"--xp TChiNeuWZ_95,TChiNeuWZ_90,TChiNeuWZ_80,T2ttDeg_300,T2ttDeg_330")
        else: 1==1 #print "NO SIGNAL specified \n"
        if '_data' in torun: 
            if(dowhat != "limits"):x = x.replace('mca-2los-mc.txt','mca-2los-mcdata.txt') 
            #if(dowhat != "limits"):x = x.replace('mca-2los-mc.txt','mca-2los-mcdata-frdata.txt') ## ( FR from data ) 
            if(dowhat != "limits"): x = add(x,"--showRatio --maxRatioRange -2 5") #--showMCError
        if '_met200' in torun:             
            x = add(x,"-E ^highMET -E ^MT -R ^TT CRDYTT 'LepGood1_isTightCRDY && LepGood2_isTightCRDY' -R ^ledlepPt NoUpledlepPt '20 < LepGood1_pt || fabs(LepGood1_dxy)>0.01 || fabs(LepGood1_dz)>0.01 || fabs(LepGood2_dxy)>0.01 || fabs(LepGood2_dz)>0.01' -R mtautau Invmtautau '0.<mass_tautau(met_pt,met_phi,LepGood1_pt,LepGood1_eta,LepGood1_phi,LepGood2_pt,LepGood2_eta,LepGood2_phi)&&mass_tautau(met_pt,met_phi,LepGood1_pt,LepGood1_eta,LepGood1_phi,LepGood2_pt,LepGood2_eta,LepGood2_phi)<160.' -X ^triggerAll -E ^triggerMET")
            x = x.replace('-l 12.9','-l 12.9')
            if '_syst' in torun: 
                x = x.replace('mca-2los-mc.txt','mca-2los-mc-syst-dy.txt')
                x = add(x,"--plotmode nostack -F sf/t /data1/botta/trees_SOS_80X_170616/SOS13TeV_Friends/evVarFriend_{cname}.root")  
                x = add(x,"--sP yields")
        if '_met125' in torun:
            x = x.replace('puw2016_vtx_4fb(nVert)', 'puw2016_vtx_postTS_1p4fb(nVert)' )
            x = add(x,"-E ^mm -E ^upperMET -E ^MT -R ^TT CRDYTT 'LepGood1_isTightCRDY && LepGood2_isTightCRDY' -R ^ledlepPt NoUpledlepPt '20 < LepGood1_pt || fabs(LepGood1_dxy)>0.01 || fabs(LepGood1_dz)>0.01 || fabs(LepGood2_dxy)>0.01 || fabs(LepGood2_dz)>0.01' -R mtautau Invmtautau '0.<mass_tautau(met_pt,met_phi,LepGood1_pt,LepGood1_eta,LepGood1_phi,LepGood2_pt,LepGood2_eta,LepGood2_phi)&&mass_tautau(met_pt,met_phi,LepGood1_pt,LepGood1_eta,LepGood1_phi,LepGood2_pt,LepGood2_eta,LepGood2_phi)<160.' -E ^runRange -X ^triggerAll -E ^triggerDoubleMuMET -E ^pt5sublep")
            x = x.replace('-l 12.9','-l 10.1') 
            if '_syst' in torun: 
                x = x.replace('mca-2los-mc.txt','mca-2los-mc-syst-dy.txt')
                x = add(x,"--plotmode nostack -F sf/t /data1/botta/trees_SOS_80X_170616/SOS13TeV_Friends/evVarFriend_{cname}.root")  
                x = add(x,"--sP yields")
        if dowhat == "limits":
            runIt(x,torun,["nLepGood"],["1,-0.5,0.5"])
        else:
            runIt(x,'%s/all'%torun,[],['SR_bins_EWKino','SR_bins_stop'])


    ### TT Control Region Data-MC and syst variations, LowMET and HighMET         
    if '2los_CR_TT_vars' in torun:
        x = base('2los')
        if(dowhat != "limits"): x = add(x,"--noStackSig --showIndivSigs --xp TChiNeuWZ_95 --xp TChiNeuWZ_90")
        #elif '_ewk20'in torun : x = add(x,"--xp TChiNeuWZ_95,TChiNeuWZ_90,T2ttDeg_300,T2ttDeg_315,T2ttDeg_330")
        #elif '_ewk10'in torun : x = add(x,"--xp TChiNeuWZ_95,TChiNeuWZ_80,T2ttDeg_300,T2ttDeg_315,T2ttDeg_330")
        #elif '_stop20'in torun : x = add(x,"--xp TChiNeuWZ_95,TChiNeuWZ_90,TChiNeuWZ_80,T2ttDeg_300,T2ttDeg_315")
        #elif '_stop35'in torun : x = add(x,"--xp TChiNeuWZ_95,TChiNeuWZ_90,TChiNeuWZ_80,T2ttDeg_300,T2ttDeg_330")
        else: 1==1 #print "NO SIGNAL specified \n"
        if ('_data' in torun and dowhat != "limits") : x = add(x,"--showRatio --maxRatioRange -2 5") #--showMCError
        if '_met200' in torun:             
            x = add(x,"-E ^highMET -R ^TT CRTTTT 'LepGood1_isTightCRTT && LepGood2_isTightCRTT' -X ^bveto -E ^btag")
            #x = add(x,"-E ^highMET -R ^TT CRTTTT 'LepGood1_isTightCRTT && LepGood2_isTightCRTT' -X ^bveto -E ^ISRnobtag -E ^btag")
            #x = add(x,"-E ^highMET -R ^TT CRTTTT 'LepGood1_isTightCRTT && LepGood2_isTightCRTT' -X ^bveto -E ^ISRnobtag -E ^btag -X METovHT")
            if '_datasingleMu' in torun: 
                x = x.replace('mca-2los-mc.txt','mca-2los-mcdatacr.txt')
                x = x.replace('-l 12.9','-l 12.9')               
                x = add(x,"-E ^mm -R ^ledlepPt NoUpledlepPt '25 < LepGood1_pt' -E ^resEta -X ^triggerAll -E ^triggerMu ")   
                x = add(x,"--xP SR_bins_EWKino,SR_bins_stop")
            if '_dataMET' in torun: 
                if(dowhat != "limits"):x = x.replace('mca-2los-mc.txt','mca-2los-mcdata.txt')  
                #if(dowhat != "limits"):x = x.replace('mca-2los-mc.txt','mca-2los-mcdata-frdata.txt') ##  (FR from data)
                x = x.replace('-l 12.9','-l 12.9')
                x = add(x,"-R ^ledlepPt NoUpledlepPt '5 < LepGood1_pt' -X ^triggerAll -E ^triggerMET")
                if(dowhat != "limits"):x = add(x,"--xP SR_bins_EWKino,SR_bins_stop") 
            if '_syst' in torun: 
                x = x.replace('mca-2los-mc.txt','mca-2los-mc-syst-tt.txt')
                x = x.replace('-l 12.9','-l 12.9')
                x = add(x,"--plotmode nostack -F sf/t /data1/botta/trees_SOS_80X_170616/SOS13TeV_Friends/evVarFriend_{cname}.root")   
                x = add(x,"-R ^ledlepPt NoUpledlepPt '5 < LepGood1_pt' -X ^triggerAll -E ^triggerMET")
                x = add(x,"--sP yields")
        if '_met125' in torun:             
            x = add(x,"-E ^mm -E ^upperMET -R ^TT CRTTTT 'LepGood1_isTightCRTT && LepGood2_isTightCRTT' -X ^bveto -E ^btag -E ^pt5sublep ")
            #x = add(x,"-E ^mm -E ^upperMET -R ^TT CRTTTT 'LepGood1_isTightCRTT && LepGood2_isTightCRTT' -X ^bveto -E ^ISRnobtag -E ^btag")
            #x = add(x,"-E ^mm -E ^upperMET -R ^TT CRTTTT 'LepGood1_isTightCRTT && LepGood2_isTightCRTT' -X ^bveto -E ^ISRnobtag -E ^btag -X METovHT")
            if '_datasingleMu' in torun: 
                x = x.replace('mca-2los-mc.txt','mca-2los-mcdatacr.txt')
                x = x.replace('-l 12.9','-l 12.9')
                x = add(x,"-R ^ledlepPt NoUpledlepPt '25 < LepGood1_pt' -E ^resEta -X ^triggerAll -E ^triggerMu ")
                x = add(x,"--xP SR_bins_EWKino,SR_bins_stop")
            if '_dataMET' in torun: 
                x = x.replace('puw2016_vtx_4fb(nVert)', 'puw2016_vtx_postTS_1p4fb(nVert)' )
                if(dowhat != "limits"):x = x.replace('mca-2los-mc.txt','mca-2los-mcdata.txt')
                #if(dowhat != "limits"):x = x.replace('mca-2los-mc.txt','mca-2los-mcdata-frdata.txt') ## (FR from data)
                x = x.replace('-l 12.9','-l 10.1')    
                x = add(x," -R ^ledlepPt NoUpledlepPt '5 < LepGood1_pt' -E ^runRange -X ^triggerAll -E ^triggerDoubleMuMET")
                if(dowhat != "limits"):x = add(x,"--xP SR_bins_EWKino,SR_bins_stop")
            if '_syst' in torun: 
                x = x.replace('puw2016_vtx_4fb(nVert)', 'puw2016_vtx_postTS_1p4fb(nVert)' )
                x = x.replace('mca-2los-mc.txt','mca-2los-mc-syst-tt.txt')
                x = x.replace('-l 12.9','-l 10.1')    
                x = add(x,"--plotmode nostack -F sf/t /data1/botta/trees_SOS_80X_170616/SOS13TeV_Friends/evVarFriend_{cname}.root")   
                x = add(x," -R ^ledlepPt NoUpledlepPt '5 < LepGood1_pt' -E ^runRange -X ^triggerAll -E ^triggerDoubleMuMET")
                x = add(x,"--sP yields")    
        if dowhat == "limits":
            runIt(x,torun,["nLepGood"],["1,-0.5,0.5"])
        else:
            runIt(x,'%s/all'%torun)


    ### WW Control Region, Data-MC, HighMET             
    if '2los_CR_WW_vars' in torun:
        x = base('2los')
        x = add(x,"--noStackSig --showIndivSigs --xp TChiNeuWZ_95,T2ttDeg_300")
        if '_data' in torun: 
            x = x.replace('mca-2los-mc.txt','mca-2los-mcdata.txt')
            x = add(x,"--showRatio --maxRatioRange -2 5") #--showMCError
        if '_met200' in torun:             
            x = add(x,"-E ^highMET -R ^TT CRTTTT 'LepGood1_isTightCRTT && LepGood2_isTightCRTT' -R ^ledlepPt NoUpledlepPt '20 < LepGood1_pt' -E ^ZVeto -X ^MT -E ^InvMT -X ^triggerAll -E ^triggerMET")
            x = x.replace('-l 12.9','-l 12.9')
        if '_met125' in torun:    
            x = x.replace('puw2016_vtx_4fb(nVert)', 'puw2016_vtx_postTS_1p4fb(nVert)' )
            x = add(x,"-E ^mm -E ^upperMET -R ^TT CRTTTT 'LepGood1_isTightCRTT && LepGood2_isTightCRTT' -R ^ledlepPt NoUpledlepPt '20 < LepGood1_pt' -E ^ZVeto -X ^MT -E ^InvMT -E ^runRange -X ^triggerAll -E ^triggerDoubleMuMET -E ^pt5sublep")
            x = x.replace('-l 12.9','-l 10.1')          
        runIt(x,'%s/all'%torun,[],['SR_bins_EWKino','SR_bins_stop'])
        

    
# to be added if we want to relax these cuts in CR with MET>200
#-X ^HT -X ^Upsilon_veto -R ^ISRjet noIDISRjet 'Jet1_pt > 25 && fabs(Jet1_eta)<2.4' -R METovHT relaxMETovHT '(met_pt/(htJet25-LepGood1_pt-LepGood2_pt))>(2/3)'


    # ### WZ Control Region, Data-MC, HighMET         
    # if '2los_CR_WZ_vars' in torun:
    #     x = base('2los')
    #     x = add(x,"--noStackSig --showIndivSigs --xp TChiNeuWZ_95")
    #     if '_data' in torun: 
    #         x = x.replace('mca-2los-mc.txt','mca-2los-mcdata.txt')
    #         x = add(x,"--showRatio --maxRatioRange -2 5") #--showMCError
    #     if '_met200' in torun:             
    #         x = add(x,"-E ^highMET -E ^MT -R ^TT CRTTTT 'LepGood1_isTightCRTT && LepGood2_isTightCRTT' -R ^ledlepPt NoUpledlepPt '20 < LepGood1_pt' -X ^dilep -X ^opposite-sign -X ^Mll -E ^minMll -E ^triLep -E ^Zpeak -X ^triggerAll -E ^triggerMET -X ^HT -X ^Upsilon_veto -R METovHT relaxMETovHT '(met_pt/(htJet25-LepGood1_pt-LepGood2_pt))>(2/3)' ")
    #         x = x.replace('-l 12.9','-l 12.9')
    #     runIt(x,'%s/all'%torun,[],['SR_bins_EWKino','SR_bins_stop'])
