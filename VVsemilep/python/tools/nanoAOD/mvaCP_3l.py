from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection as Collection 
from CMGTools.TTHAnalysis.tools.nanoAOD.friendVariableProducerTools import writeOutput
from CMGTools.TTHAnalysis.tools.mvaTool import *

from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR

class mvaCP_3l(Module):
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

        P = os.environ["CMSSW_BASE"] + '/src/CMGTools/TTHAnalysis/data/kinMVA/tth/cp/ttHCP_3l_xgb_AK.xml' 


        for var in self.systsJEC: 
            self._MVAs.append(('mvaCP_3l%s'%self.systsJEC[var], MVATool("BDTG",P, self.getVarsForVariation(self.systsJEC[var]))))
        self._MVAs = dict(self._MVAs)


    def getVarsForVariation(self,var):
        return [
            MVAVar("Lep1_pt", func = lambda ev : (ev.LepGood_conePt[int(ev.iLepFO_Recl[0])]) if ev.nLepFO_Recl >= 1 else 0),
            MVAVar("Lep2_pt", func = lambda ev : (ev.LepGood_conePt[int(ev.iLepFO_Recl[1])]) if ev.nLepFO_Recl >= 2 else 0),
            MVAVar("Lep3_pt", func = lambda ev : (ev.LepGood_eta[int(ev.iLepFO_Recl[0])]) if ev.nLepFO_Recl >= 1 else 0),
            MVAVar("jetpt1", func = lambda ev : getattr(ev,'JetSel_Recl_pt%s'%var)[0] if getattr(ev,'nJet25%s_Recl'%var) > 0 else 0),
            MVAVar("jetpt2", func = lambda ev : getattr(ev,'JetSel_Recl_pt%s'%var)[1] if getattr(ev,'nJet25%s_Recl'%var) > 1 else 0),
            MVAVar("mindr_lep2_jet", func = lambda ev : getattr(ev,'mindr_lep2_jet%s'%var)),
            MVAVar("mindr_lep1_jet", func = lambda ev : getattr(ev,'mindr_lep1_jet%s'%var)),
            MVAVar("mTTH_3l", func = lambda ev : getattr(ev,'mTTH_3l%s'%var)),
            MVAVar("dEtaBB_2lss", lambda ev : getattr(ev,'dEtaBB_2lss%s'%var)),
            MVAVar("dEtaL1L2_BBframe_3l", func = lambda ev : getattr(ev,'dEtaL1L2_BBframe_3l%s'%var)),
            MVAVar("dEtaL1L3_BBframe_3l", func = lambda ev : getattr(ev,'dEtaL1L3_BBframe_3l%s'%var)),
            MVAVar("dRlep31", func = lambda ev : deltaR( ev.LepGood_eta[int(ev.iLepFO_Recl[0])], ev.LepGood_phi[int(ev.iLepFO_Recl[0])], ev.LepGood_eta[int(ev.iLepFO_Recl[2])], ev.LepGood_phi[int(ev.iLepFO_Recl[2])]) if ev.nLepFO_Recl > 2 else 0),
            MVAVar("dRlep12", func = lambda ev : deltaR( ev.LepGood_eta[int(ev.iLepFO_Recl[0])], ev.LepGood_phi[int(ev.iLepFO_Recl[0])], ev.LepGood_eta[int(ev.iLepFO_Recl[1])], ev.LepGood_phi[int(ev.iLepFO_Recl[2])]) if ev.nLepFO_Recl > 2 else 0),
            MVAVar("dRlep23", func = lambda ev : deltaR( ev.LepGood_eta[int(ev.iLepFO_Recl[1])], ev.LepGood_phi[int(ev.iLepFO_Recl[1])], ev.LepGood_eta[int(ev.iLepFO_Recl[1])], ev.LepGood_phi[int(ev.iLepFO_Recl[2])]) if ev.nLepFO_Recl > 2 else 0),
            MVAVar("detajet1_2", func = lambda ev : getattr(ev,'JetSel_Recl_eta')[0]-getattr(ev,'JetSel_Recl_eta')[1] if getattr(ev,'nJet25_Recl') > 1 else 0),
            MVAVar("ptsum8", func = lambda ev : getattr(ev,'JetSel_Recl_pt%s'%var)[0]+getattr(ev,'JetSel_Recl_pt%s'%var)[1]+getattr(ev,'JetSel_Recl_pt%s'%var)[2]+(getattr(ev,'MET_pt%s'%var) if ev.year != 2017 else getattr(ev,'METFixEE2017_pt%s'%var)) if getattr(ev,'nJet25%s_Recl'%var) > 2 else 0),
        ]

            
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.wrappedOutputTree = wrappedOutputTree
        for out in self._MVAs.keys():
            self.wrappedOutputTree.branch(out,'F')

    def analyze(self, event):
        myvars = [event.iLepFO_Recl[0],event.iLepFO_Recl[1],event.iLepFO_Recl[2]]
        writeOutput(self, dict([ (name, mva(event)) for name, mva in self._MVAs.iteritems()]))
        return True

