from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from CMGTools.TTHAnalysis.tools.nanoAOD.friendVariableProducerTools import loadHisto
from copy import deepcopy
import ROOT
import os 

class lepScaleFactors(Module):
    def __init__(self):
        self.looseToTight  = {} 
        self.recoToLoose   = {} 
        self.electronReco  = {} 
        self.triggerSF     = {}

        for year in '2016APV,2016,2017,2018'.split(','):
            self.looseToTight['%s,mu'%year] = loadHisto(os.environ['CMSSW_BASE'] + '/src/CMGTools/TTHAnalysis/data/leptonSF/muon/egammaEffi%s_EGM2D.root'%year, 'EGamma_SF2D')
            self.recoToLoose['%s,mu'%year]= loadHisto(os.environ['CMSSW_BASE'] + '/src/CMGTools/TTHAnalysis/data/leptonSF/muon/egammaEffi%s_iso_EGM2D.root'%(year), 'EGamma_SF2D')
        for year in '2016APV,2016,2017,2018'.split(','):
            for chan in '2lss,3l'.split(','):
                self.looseToTight['%s,%s,el'%(year,chan)] = loadHisto(os.environ['CMSSW_BASE'] + '/src/CMGTools/TTHAnalysis/data/leptonSF/elecNEWmva/egammaEffi%s_%s_EGM2D.root'%(year,chan), 'EGamma_SF2D')
            self.recoToLoose['%s,e'%year]= loadHisto(os.environ['CMSSW_BASE'] + '/src/CMGTools/TTHAnalysis/data/leptonSF/elec/egammaEffi%s_iso_EGM2D.root'%(year), 'EGamma_SF2D')
            self.recoToLoose['%s,e,extra'%year]= loadHisto(os.environ['CMSSW_BASE'] + '/src/CMGTools/TTHAnalysis/data/leptonSF/elec/egammaEffi%s_recoToloose_EGM2D.root'%(year), 'EGamma_SF2D')

            self.electronReco [year] = [loadHisto(os.environ['CMSSW_BASE'] + '/src/CMGTools/TTHAnalysis/data/leptonSF/elec/egammaEffi%s_ptAbove20_EGM2D.root'%year, "EGamma_SF2D"),
                        loadHisto(os.environ['CMSSW_BASE'] + '/src/CMGTools/TTHAnalysis/data/leptonSF/elec/egammaEffi%s_ptAbove20_EGM2D.root'%year, "EGamma_SF2D")] # first Et > 20, second Et < 20

        for year in '2016APV,2016,2017,2018'.split(','):
            for channel in ['sf_2l_ee','sf_2l_em', 'sf_2l_mm', 'sf_3l_eee','sf_3l_eem', 'sf_3l_emm','sf_3l_mmm']:
                self.triggerSF['%s %s'%(year,channel)]=loadHisto(os.environ['CMSSW_BASE'] + '/src/CMGTools/TTHAnalysis/data/triggerSF/triggerScaleFactors_%s.root'%year,channel )
                
                                

                                      



    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        for var in ',_el_up,_el_dn,_mu_up,_mu_dn'.split(','):
            self.out.branch('leptonSF_2lss%s'%var,'F')
            self.out.branch('leptonSF_3l%s'%var,'F')
            self.out.branch('leptonSF_4l%s'%var,'F')
        for var in ',_up,_dn'.split(','):
            self.out.branch('triggerSF_2lss%s'%var,'F')
            self.out.branch('triggerSF_3l%s'%var,'F')

    def getLooseToTight(self,lep,var_str,year,nlep):
        if abs(lep.pdgId) == 11:
            hist = self.looseToTight['%s,%s,el'%(year, '2lss' if nlep == 2 else '3l')]
        else:
            hist = self.looseToTight['%s,mu'%(year)]

        etabin = max(1, min(hist.GetNbinsX(), hist.GetXaxis().FindBin(abs(lep.eta))));
        ptbin  = max(1, min(hist.GetNbinsY(), hist.GetYaxis().FindBin(lep.pt)));

        var = 0 if abs(lep.pdgId) == 11 and 'mu' in var_str or  abs(lep.pdgId) == 13 and 'el' in var_str  else 1 if 'up' in var_str else -1

        out = hist.GetBinContent(etabin,ptbin) + var*hist.GetBinError(etabin,ptbin)
        return out

    def getRecoToLoose(self,lep,var_str,year):
        histList = []
        if abs(lep.pdgId) == 11:
            histList.append( self.recoToLoose['%s,e'%year] ) 
            histList.append( self.recoToLoose['%s,e,extra'%year] ) 
            reco = self.electronReco[year]
            recohist = reco[0] if lep.pt > 20 else reco[1]
            histList.append([recohist]) # recohist is a list so we can distinguish it afterwards :)

        if abs(lep.pdgId) == 13: 
            return 1 
        out = 1
        for hist in histList:
            if type(hist) == list: # stupid way of distinguishing etaSC and abs(eta) for reco
                eta = (lep.eta+lep.deltaEtaSC)
                hist = hist[0]
            else:
                eta = abs(lep.eta)
            etabin = max(1, min(hist.GetNbinsX(), hist.GetXaxis().FindBin(eta)));
            ptbin  = max(1, min(hist.GetNbinsY(), hist.GetYaxis().FindBin(lep.pt)));
            sf = hist.GetBinContent(etabin,ptbin)
            if '_mu_up' == var_str and abs(lep.pdgId) == 13: 
                sf = sf+hist.GetBinError(etabin,ptbin)
            if '_mu_dn' == var_str and abs(lep.pdgId) == 13: 
                sf = sf-hist.GetBinError(etabin,ptbin)
            if '_el_up' == var_str and abs(lep.pdgId) == 11: 
                sf = sf+hist.GetBinError(etabin,ptbin)
            if '_el_dn' == var_str and abs(lep.pdgId) == 11: 
                sf = sf-hist.GetBinError(etabin,ptbin)
            out = out*sf
            
        return out


    def getTriggerEff(self, leps, year):
        
        for var in ',_up,_dn'.split(","):
            if len(leps)>=2:
                comb = abs(leps[0].pdgId) + abs(leps[1].pdgId)
                if (comb == 22): channel = 'sf_2l_ee'
                if (comb == 24): channel = 'sf_2l_em'
                if (comb == 26): channel = 'sf_2l_mm'

                hist_2lss=self.triggerSF['%s %s'%(year,channel)]
                thebin=hist_2lss.FindBin( min(199.,leps[0].pt), min(199.,leps[1].pt) ) 
                shift= 0 if var == '' else 1 if 'up' in var else -1 
                self.out.fillBranch('triggerSF_2lss%s'%var, hist_2lss.GetBinContent(thebin) + shift*hist_2lss.GetBinContent(thebin))
            else:
                self.out.fillBranch('triggerSF_2lss%s'%var, 1)

        for var in ',_up,_dn'.split(","):
            if len(leps)>=3:
                comb = abs(leps[0].pdgId) + abs(leps[1].pdgId) + abs(leps[2].pdgId)
                if (comb == 33): channel = 'sf_3l_eee'
                if (comb == 35): channel = 'sf_3l_eem'
                if (comb == 37): channel = 'sf_3l_emm'
                if (comb == 39): channel = 'sf_3l_mmm'

                hist_3l=self.triggerSF['%s %s'%(year,channel)]
                thebin=hist_3l.FindBin( min(299.,leps[0].pt), abs(leps[0].eta ) )
                shift= 0 if var == '' else 1 if 'up' in var else -1 
                if channel == 'sf_3l_eee' and year == '2016APV' and leps[0].pt < 80 and abs(leps[0].eta) > 1.4:
                    scale_factor=1
                else:
                    scale_factor=hist_3l.GetBinContent(thebin) + shift*hist_3l.GetBinContent(thebin)
                self.out.fillBranch('triggerSF_3l%s'%var, scale_factor)

            else:
                self.out.fillBranch('triggerSF_3l%s'%var, 1)

    def analyze(self, event):
        year = event.year
        # leptons
        all_leps = [l for l in Collection(event,"LepGood")]
        nFO = getattr(event,"nLepFO_Recl")
        chosen = getattr(event,"iLepFO_Recl")
        leps = [all_leps[chosen[i]] for i in xrange(nFO)]
        

        year=str(event.year)
        if event.suberaId == 0 and year == '2016':
            year='2016APV'
        
        # trigger efficiency
        self.getTriggerEff(leps, year)


        for var in ',_el_up,_el_dn,_mu_up,_mu_dn'.split(','):
            leptonSF_2lss = 1
            leptonSF_3l   = 1
            leptonSF_4l   = 1
            if len(leps) >= 2:
                leptonSF_2lss = self.getLooseToTight(leps[0],var,year,2) * self.getLooseToTight(leps[1],var,year,2)
                leptonSF_2lss = leptonSF_2lss * self.getRecoToLoose(leps[0],var,year) * self.getRecoToLoose(leps[1],var,year)
            if len(leps) >= 3:
                leptonSF_3l   = self.getLooseToTight(leps[0],var,year,3) * self.getLooseToTight(leps[1],var,year,3) * self.getLooseToTight(leps[2],var,year,3)
                leptonSF_3l   = leptonSF_3l *  self.getRecoToLoose(leps[0],var,year) * self.getRecoToLoose(leps[1],var,year) * self.getRecoToLoose(leps[2],var,year)
            if len(leps) >= 4: 
                leptonSF_4l   = self.getLooseToTight(leps[0],'',year,3) * self.getLooseToTight(leps[1],'',year,3) * self.getLooseToTight(leps[2],'',year,3) * self.getLooseToTight(leps[3],'',year,3)
                leptonSF_4l   = leptonSF_4l *  self.getRecoToLoose(leps[0],var,year) * self.getRecoToLoose(leps[1],var,year) * self.getRecoToLoose(leps[2],var,year) * self.getRecoToLoose(leps[3],var,year)
            self.out.fillBranch('leptonSF_2lss%s'%var, leptonSF_2lss)
            self.out.fillBranch('leptonSF_3l%s'%var  , leptonSF_3l)
            self.out.fillBranch('leptonSF_4l%s'%var  , leptonSF_4l)
        

        return True
