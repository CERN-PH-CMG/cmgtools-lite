from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from copy import deepcopy
import ROOT
import os 

class lepScaleFactors(Module):
    def __init__(self):
        self.looseToTight  = {} 
        self.recoToLoose   = {} 
        self.recoToLoose['mu1_lt30'] = self.loadHisto(os.environ['CMSSW_BASE'] + '/src/CMGTools/TTHAnalysis/data/leptonSF/mu_scaleFactors_ptLt30.root','NUM_LooseID_DEN_genTracks_pt_abseta')
        self.recoToLoose['mu1_gt30'] = self.loadHisto(os.environ['CMSSW_BASE'] + '/src/CMGTools/TTHAnalysis/data/leptonSF/mu_scaleFactors_ptGt30.root','NUM_LooseID_DEN_genTracks_pt_abseta')
        self.recoToLoose['mu2']      = self.loadHisto(os.environ['CMSSW_BASE'] + '/src/CMGTools/TTHAnalysis/data/leptonSF/scaleFactors_mu_DxyDzSip8mIso04_over_LooseID.root','NUM_ttHLoo_DEN_LooseID')
        self.recoToLoose['el']       = self.loadHisto(os.environ['CMSSW_BASE'] + '/src/CMGTools/TTHAnalysis/data/leptonSF/egammaEffi.txt_EGM2D_looseTTH_2017.root',"EGamma_SF2D")
        self.recoToLoose['gsf_lt20'] = self.loadHisto(os.environ['CMSSW_BASE'] + '/src/CMGTools/TTHAnalysis/data/leptonSF/el_scaleFactors_gsf_ptLt20.root',"EGamma_SF2D")
        self.recoToLoose['gsf_gt20'] = self.loadHisto(os.environ['CMSSW_BASE'] + '/src/CMGTools/TTHAnalysis/data/leptonSF/el_scaleFactors_gsf_ptGt20.root',"EGamma_SF2D")

        for chan in ['2lss','3l']:
            for fl in ['e','m']:
                # FIXME hardcoded to 2017
                self.looseToTight['2016,%s,%s'%(fl,chan)] = self.loadHisto(os.environ['CMSSW_BASE'] + '/src/CMGTools/TTHAnalysis/data/leptonSF/lepMVAEffSF_%s_%s.root'%(fl,chan), 'sf')
                self.looseToTight['2017,%s,%s'%(fl,chan)] = self.loadHisto(os.environ['CMSSW_BASE'] + '/src/CMGTools/TTHAnalysis/data/leptonSF/lepMVAEffSF_%s_%s.root'%(fl,chan), 'sf')
                self.looseToTight['2018,%s,%s'%(fl,chan)] = self.loadHisto(os.environ['CMSSW_BASE'] + '/src/CMGTools/TTHAnalysis/data/leptonSF/lepMVAEffSF_%s_%s.root'%(fl,chan), 'sf')

    def loadHisto(self, fil, hist):
        tf = ROOT.TFile.Open(fil)
        if not tf: raise RuntimeError("No such file %s"%fil)
        hist = tf.Get(hist)
        if not hist: raise RuntimeError("No such object %s in %s"%(hist,fil))
        ret = deepcopy(hist)
        tf.Close()
        return ret


    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        for var in ',_el_up,_el_dn,_mu_up,_mu_dn'.split(','):
            self.out.branch('leptonSF_2lss%s'%var,'F')
            self.out.branch('leptonSF_3l%s'%var,'F')
            self.out.branch('leptonSF_4l%s'%var,'F')
        for var in ',_up,_dn'.split(','):
            self.out.branch('triggerSF_2lss%s'%var,'F')
            self.out.branch('triggerSF_3l%s'%var,'F')

    def getLooseToTight(self,lep,year,nlep):
        hist = self.looseToTight['%d,%s,%s'%(year, 'e' if abs(lep.pdgId) == 11 else 'm', '2lss' if nlep == 2 else '3l')]
        ptbin  = max(1, min(hist.GetNbinsX(), hist.GetXaxis().FindBin(lep.pt)));
        etabin = max(1, min(hist.GetNbinsY(), hist.GetYaxis().FindBin(abs(lep.eta))));
        return hist.GetBinContent(ptbin,etabin)

    def getRecoToLoose(self,lep,var_str,year):
        # hardcoded to 2017 # FIXME
        out = 1 
        if abs(lep.pdgId) == 13: 
            var = 0 if var_str == '' or 'mu' not in var_str else  1 if 'up' in var_str else -1 
            hist = self.recoToLoose['mu1_lt30'] if (lep.pt < 30)  else self.recoToLoose['mu1_gt30']
            ptbin  = max(1, min(hist.GetNbinsX(), hist.GetXaxis().FindBin(lep.pt)));
            etabin = max(1, min(hist.GetNbinsY(), hist.GetYaxis().FindBin(abs(lep.eta))));
            out  = out * ( 1 if (lep.pt >= 15 and lep.pt < 30 and abs(lep.eta) >= 2.1 and abs(lep.eta) < 2.4) else hist.GetBinContent(ptbin,etabin)+var*hist.GetBinError(ptbin,etabin))
            hist = self.recoToLoose['mu2']
            ptbin  = max(1, min(hist.GetNbinsX(), hist.GetXaxis().FindBin(lep.pt)));
            etabin = max(1, min(hist.GetNbinsY(), hist.GetYaxis().FindBin(abs(lep.eta))));
            out  = out * hist.GetBinContent(ptbin,etabin)+var*hist.GetBinError(ptbin,etabin)

        if abs(lep.pdgId) == 11:
            var = 0 if var_str == '' or 'el' not in var_str else  1 if 'up' in var_str else -1 
            hist = self.recoToLoose['el']
            etabin =max(1, min(hist.GetNbinsX(), hist.GetXaxis().FindBin(lep.eta))); # careful, different convention
            ptbin  =max(1, min(hist.GetNbinsY(), hist.GetYaxis().FindBin(lep.pt)));
            out = out * hist.GetBinContent(etabin,ptbin)+var*hist.GetBinError(etabin,ptbin)
            
            hist = self.recoToLoose['gsf_gt20'] if lep.pt > 20 else self.recoToLoose['gsf_lt20']
            etabin =max(1, min(hist.GetNbinsX(), hist.GetXaxis().FindBin(lep.eta))); # careful, different convention
            ptbin  =max(1, min(hist.GetNbinsY(), hist.GetYaxis().FindBin(lep.pt)));
            out = out * hist.GetBinContent(etabin,ptbin)+var*hist.GetBinError(etabin,ptbin)
            
        return out

    def analyze(self, event):
        year = event.year
        
        # leptons
        all_leps = [l for l in Collection(event,"LepGood")]
        nFO = getattr(event,"nLepFO_Recl")
        chosen = getattr(event,"iLepFO_Recl")
        leps = [all_leps[chosen[i]] for i in xrange(nFO)]
        
        # trigger efficiency
        if year == 2016:
            for var, shift in zip(',_up,_dn'.split(','),[0,1,-1]):
                self.out.fillBranch('triggerSF_3l%s'%var, 1.+shift*0.03)
                triggerSF_2lss = 1 
                if len(leps) >= 2: 
                    comb = abs(leps[0].pdgId) + abs(leps[1].pdgId)
                    if (comb == 22): triggerSF_2lss = (1.01+shift*0.02)
                    if (comb == 24): triggerSF_2lss = (1.01+shift*0.01)
                    if (comb == 26): triggerSF_2lss = (1   +shift*0.01)
                self.out.fillBranch('triggerSF_2lss%s'%var, triggerSF_2lss)

        if year == 2017:
            for var, shift in zip(',_up,_dn'.split(','),[0,1,-1]):
                self.out.fillBranch('triggerSF_3l%s'%var, 1.+shift*0.05)
                triggerSF_2lss = 1
                if len(leps) >= 2: 
                    comb = abs(leps[0].pdgId) + abs(leps[1].pdgId)
                    pt1 = leps[0].pt
                    if (comb == 22): triggerSF_2lss = (0.937+shift*0.027)  if pt1 < 30 else (0.991+shift*0.002)
                    if (comb == 24): triggerSF_2lss = (0.952+shift*0.008)  if pt1 < 35 else (0.983+shift*0.003) if pt1 < 50 else 1.0+shift*0.001
                    if (comb == 26): triggerSF_2lss = (0.972+shift*0.006)  if pt1 < 35 else (0.994+shift*0.001)
                self.out.fillBranch('triggerSF_2lss%s'%var, triggerSF_2lss)

        if year == 2018: # using 2016 ones as placeholder
            for var, shift in zip(',_up,_dn'.split(','),[0,1,-1]):
                self.out.fillBranch('triggerSF_3l%s'%var, 1.+shift*0.03)
                triggerSF_2lss = 1 
                if len(leps) >= 2: 
                    comb = abs(leps[0].pdgId) + abs(leps[1].pdgId)
                    if (comb == 22): triggerSF_2lss = (1.01+shift*0.02)
                    if (comb == 24): triggerSF_2lss = (1.01+shift*0.01)
                    if (comb == 26): triggerSF_2lss = (1   +shift*0.01)
                self.out.fillBranch('triggerSF_2lss%s'%var, triggerSF_2lss)


        # lepton scale factors
        for var in ',_el_up,_el_dn,_mu_up,_mu_dn'.split(','):
            leptonSF_2lss = 1
            leptonSF_3l   = 1
            leptonSF_4l   = 1
            if len(leps) >= 2:
                leptonSF_2lss = self.getLooseToTight(leps[0],year,2) * self.getLooseToTight(leps[1],year,2)
                leptonSF_2lss = leptonSF_2lss * self.getRecoToLoose(leps[0],var,year) * self.getRecoToLoose(leps[1],var,year)
            if len(leps) >= 3:
                leptonSF_3l   = self.getLooseToTight(leps[0],year,3) * self.getLooseToTight(leps[1],year,3) * self.getLooseToTight(leps[2],year,3)
                leptonSF_3l   = leptonSF_3l *  self.getRecoToLoose(leps[0],var,year) * self.getRecoToLoose(leps[1],var,year) * self.getRecoToLoose(leps[2],var,year)
            if len(leps) >= 4: 
                leptonSF_4l   = self.getLooseToTight(leps[0],year,3) * self.getLooseToTight(leps[1],year,3) * self.getLooseToTight(leps[2],year,3) * self.getLooseToTight(leps[3],year,3)
                leptonSF_4l   = leptonSF_4l *  self.getRecoToLoose(leps[0],var,year) * self.getRecoToLoose(leps[1],var,year) * self.getRecoToLoose(leps[2],var,year) * self.getRecoToLoose(leps[3],var,year)

            self.out.fillBranch('leptonSF_2lss%s'%var, leptonSF_2lss)
            self.out.fillBranch('leptonSF_3l%s'%var  , leptonSF_3l)
            self.out.fillBranch('leptonSF_4l%s'%var  , leptonSF_4l)
        return True
