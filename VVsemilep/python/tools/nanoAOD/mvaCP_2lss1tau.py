from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection as Collection 
from CMGTools.TTHAnalysis.tools.nanoAOD.friendVariableProducerTools import writeOutput
from CMGTools.TTHAnalysis.tools.mvaTool import *

from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR

def getTauThings(ev,var):
    if ev.Tau_tight2lss1tau_idx > -1: 
        return getattr(ev,'TauSel_Recl_%s'%var) [int(ev.Tau_tight2lss1tau_idx)]
    else: 
        return 0

class mvaCP_2lss1tau(Module):
    def __init__(self, variations, doSystJEC=False):
        self._MVAs = []
        self.systsJEC = {0:"",\
                         1:"_jesTotalCorrUp"  , -1:"_jesTotalCorrDown",\
                         2:"_jesTotalUnCorrUp", -2: "_jesTotalUnCorrDown",\
                         3:"_jerUp", -3: "_jerDown",\
                     } if doSystJEC else {0:""}
        if len(variations): 
            self.systsJEC = {0:""}
            for i,var in enumerate(variations):
                self.systsJEC[i+1]   ="_%sUp"%var
                self.systsJEC[-(i+1)]="_%sDown"%var

        P = os.environ["CMSSW_BASE"] + '/src/CMGTools/TTHAnalysis/data/kinMVA/tth/cp/ttHCP_2lss1tau.xml' 


        for var in self.systsJEC: 
            self._MVAs.append(('mvaCP_2lss1tau%s'%self.systsJEC[var], MVATool("BDTG",P, self.getVarsForVariation(self.systsJEC[var]))))
        self._MVAs = dict(self._MVAs)


    def getVarsForVariation(self,var):
        return [
            MVAVar("Lep1_pt", func = lambda ev : (ev.LepGood_conePt[int(ev.iLepFO_Recl[0])]) if ev.nLepFO_Recl >= 1 else 0),
            MVAVar("Lep2_pt", func = lambda ev : (ev.LepGood_conePt[int(ev.iLepFO_Recl[1])]) if ev.nLepFO_Recl >= 2 else 0),
            MVAVar("Lep1_eta", func = lambda ev : (ev.LepGood_eta[int(ev.iLepFO_Recl[0])]) if ev.nLepFO_Recl >= 1 else 0),
            MVAVar("Lep2_eta", func = lambda ev : (ev.LepGood_eta[int(ev.iLepFO_Recl[1])]) if ev.nLepFO_Recl >= 2 else 0),
            MVAVar("Lep1_phi", func = lambda ev : (ev.LepGood_phi[int(ev.iLepFO_Recl[0])]) if ev.nLepFO_Recl >= 1 else 0),
            MVAVar("Lep2_phi", func = lambda ev : (ev.LepGood_phi[int(ev.iLepFO_Recl[1])]) if ev.nLepFO_Recl >= 2 else 0),
            MVAVar("nSelJets", func = lambda ev : getattr(ev,'nJet25%s_Recl'%var)),
            MVAVar("met", func = lambda ev : (getattr(ev,'MET_pt%s'%var) if ev.year != 2017 else getattr(ev,'METFixEE2017_pt%s'%var))),
            MVAVar("met_phi", func = lambda ev : ev.MET_phi),
            MVAVar("HTT_score", func = lambda ev : getattr(ev,'BDThttTT_eventReco_mvaValue%s'%(var))),
            MVAVar("Hj_tagger_hadTop", func = lambda ev: getattr(ev,'BDThttTT_eventReco_Hj_score%s'%(var))),
            MVAVar("mindr_lep2_jet", func = lambda ev : getattr(ev,'mindr_lep2_jet%s'%var)),
            MVAVar("mindr_lep1_jet", func = lambda ev : getattr(ev,'mindr_lep1_jet%s'%var)),
            MVAVar("avg_dr_jet", func = lambda ev : getattr(ev,'avg_dr_jet%s'%var)),
            MVAVar("dPhiLL_BBframe_2lss", func = lambda ev : getattr(ev,'dPhiLL_BBframe_2lss%s'%var)),
            MVAVar("dEtaLL_BBframe_2lss", func = lambda ev : getattr(ev,'dEtaLL_BBframe_2lss%s'%var)),
            MVAVar("dPhiBB_LLframe_2lss", func = lambda ev : getattr(ev,'dPhiBB_LLframe_2lss%s'%var)),            
            MVAVar("dEtaBB_LLframe_2lss", func = lambda ev : getattr(ev,'dEtaBB_LLframe_2lss%s'%var)),            
            MVAVar("dEtaBB_2lss", func = lambda ev : getattr(ev,'dEtaBB_2lss%s'%var)),
            MVAVar("mTTH_2lss1tau", func = lambda ev : getattr(ev,'mTTH_2lss1tau%s'%var)),
            MVAVar("theta_higgs_ttbar_TTHsystem_2lss1tau",  func = lambda ev : getattr(ev, 'theta_higgs_ttbar_TTHsystem_2lss1tau%s'%var)),
            MVAVar("thetaTopTop_ttbarframe_2lss1tau",  func = lambda ev : getattr(ev, 'thetaTopTop_ttbarframe_2lss1tau%s'%var)),
            MVAVar("Tau_pt",   func = lambda ev : getTauThings(ev,'pt')),
            MVAVar("Tau_eta",  func = lambda ev : getTauThings(ev,'eta')),
            MVAVar("Tau_phi",  func = lambda ev : getTauThings(ev,'phi')),
        ]

            
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.wrappedOutputTree = wrappedOutputTree
        for out in self._MVAs.keys():
            self.wrappedOutputTree.branch(out,'F')

    def analyze(self, event):
        myvars = [event.iLepFO_Recl[0],event.iLepFO_Recl[1],event.iLepFO_Recl[2], event.Tau_tight2lss1tau_idx]
        writeOutput(self, dict([ (name, mva(event)) for name, mva in self._MVAs.iteritems()]))
        return True

