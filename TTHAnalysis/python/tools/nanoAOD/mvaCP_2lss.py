from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection as Collection 
from CMGTools.TTHAnalysis.tools.nanoAOD.friendVariableProducerTools import writeOutput
from CMGTools.TTHAnalysis.tools.mvaTool import *

class mvaCP_2lss(Module):
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
        P = os.environ["CMSSW_BASE"] + '/src/CMGTools/TTHAnalysis/data/kinMVA/tth/cp/xgboost_2lss.xml' 


        for var in self.systsJEC: 
            self._MVAs.append(('mvaCP_2lss%s'%self.systsJEC[var], MVATool("BDTG",P, self.getVarsForVariation(self.systsJEC[var]))))
        self._MVAs = dict(self._MVAs)


    def getVarsForVariation(self,var):
        return [
            MVAVar("f0", func = lambda ev : (ev.LepGood_conePt[int(ev.iLepFO_Recl[0])]) if ev.nLepFO_Recl >= 1 else 0),
            MVAVar("f1", func = lambda ev : (ev.LepGood_conePt[int(ev.iLepFO_Recl[1])]) if ev.nLepFO_Recl >= 2 else 0),
            MVAVar("f2", func = lambda ev : (ev.LepGood_eta[int(ev.iLepFO_Recl[0])]) if ev.nLepFO_Recl >= 1 else 0),
            MVAVar("f3", func = lambda ev : (ev.LepGood_eta[int(ev.iLepFO_Recl[1])]) if ev.nLepFO_Recl >= 2 else 0),
            MVAVar("f4", func = lambda ev : (ev.LepGood_phi[int(ev.iLepFO_Recl[0])]) if ev.nLepFO_Recl >= 1 else 0),
            MVAVar("f5", func = lambda ev : (ev.LepGood_phi[int(ev.iLepFO_Recl[1])]) if ev.nLepFO_Recl >= 2 else 0),
            MVAVar("f6", func = lambda ev : getattr(ev,'nJet25%s_Recl'%var)),
            MVAVar("f7", func = lambda ev : (getattr(ev,'MET_pt%s'%var) if ev.year != 2017 else getattr(ev,'METFixEE2017_pt%s'%var))),
            MVAVar("f8", func = lambda ev : ev.MET_phi),
            MVAVar("f9", func = lambda ev : getattr(ev,'BDThttTT_eventReco_mvaValue%s'%(var))),
            MVAVar("f10", func = lambda ev : getattr(ev,'MT_met_lep2%s'%var)),
            MVAVar("f11", func = lambda ev : getattr(ev,'MT_met_lep1%s'%var)),
            MVAVar("f12", func = lambda ev : getattr(ev,'mindr_lep2_jet%s'%var)),
            MVAVar("f13", func = lambda ev : getattr(ev,'mindr_lep1_jet%s'%var)),
            MVAVar("f14", func = lambda ev : getattr(ev,'avg_dr_jet%s'%var)),
            MVAVar("f15", func = lambda ev : getattr(ev,'dEtaLL_BBframe_2lss%s'%var)),
            MVAVar("f16", func = lambda ev : getattr(ev,'dEtaBB_LLframe_2lss%s'%var)),
            MVAVar("f17", func = lambda ev : getattr(ev,'dEtaBB_2lss%s'%var)),
            MVAVar("f18", func = lambda ev : getattr(ev,'mTTH_2lss%s'%var)),
        ]

            
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.wrappedOutputTree = wrappedOutputTree
        for out in self._MVAs.keys():
            self.wrappedOutputTree.branch(out,'F')

    def analyze(self, event):
        myvars = [event.iLepFO_Recl[0],event.iLepFO_Recl[1],event.iLepFO_Recl[2]]
        writeOutput(self, dict([ (name, mva(event)) for name, mva in self._MVAs.iteritems()]))
        return True

