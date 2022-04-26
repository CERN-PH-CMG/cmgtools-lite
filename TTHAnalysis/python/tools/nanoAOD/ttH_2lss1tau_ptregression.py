from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection as NanoAODCollection 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection as Collection 
from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR, deltaPhi

from CMGTools.TTHAnalysis.treeReAnalyzer import Collection as CMGCollection
from CMGTools.TTHAnalysis.tools.nanoAOD.friendVariableProducerTools import declareOutput, writeOutput
from CMGTools.TTHAnalysis.tools.tfTool import TFTool
import os 
from copy import deepcopy
import ROOT

class ttH_2lss1tau_ptregression(Module):


    def __init__(self, variations=[], doSystJEC=True): 





        varorder=['SelJet1_eta','SelJet1_phi','SelJet1_pt','SelJet1_isFromHadTop','SelJet1_btagDeepFlavB','SelJet2_eta' ,'SelJet2_phi' ,'SelJet2_pt','SelJet2_isFromHadTop','SelJet2_btagDeepFlavB', 'Lep1_pt','Lep2_pt','Lep1_eta','Lep2_eta','Lep1_phi','Lep2_phi','nSelJets','met','HTT_score','visHiggs_pt','visHiggs_eta','mT_lep2','mT_lep1','Hj_tagger_hadTop','avg_dr_jet','mTTH_2lss1tau','Tau_pt','Tau_eta','Tau_phi']

        self.systsJEC = {0:"",\
                         1:"_jesTotalCorrUp"  , -1:"_jesTotalCorrDown",\
                         2:"_jesTotalUnCorrUp", -2: "_jesTotalUnCorrDown",\
                         3:"_jerUp", -3: "_jerDown",\
                     } if doSystJEC else {0:""}
        if len(variations): 
            self.systsJEC = {0:""}
            for i,var in enumerate(variations):
                self.systsJEC[i+1]   ="_%sUp"%var
        self._MVAs=[]
        self.outVars=[]

        for var in self.systsJEC: 
            self._MVAs.append(TFTool('ttH_higgs_pt_2lss1tau%s'%self.systsJEC[var], os.environ['CMSSW_BASE'] + '/src/CMGTools/TTHAnalysis/data/kinMVA/tth/diff/weights.pb', 
                                     self.getVarForVar(self.systsJEC[var]), [''], varorder, outputNodename=ROOT.std.string("Identity")))
            self.outVars.extend( ['ttH_higgs_pt_2lss1tau%s_'%self.systsJEC[var] ])
            

    def getVarForVar(self, var):
        return { 
            'SelJet1_pt'            : lambda ev : getattr(ev,'JetSel_Recl_pt%s'%var)[0] if getattr(ev,'nJet25%s_Recl'%var) > 0 else 0,
            'SelJet1_eta'           : lambda ev : ev.JetSel_Recl_eta[0] if getattr(ev,'nJet25%s_Recl'%var) > 0 else 0,
            'SelJet1_phi'           : lambda ev : ev.JetSel_Recl_phi[0] if getattr(ev,'nJet25%s_Recl'%var) > 0 else 0,
            'SelJet1_isFromHadTop'  : lambda ev : getattr(ev,'jetobjects')[0].isFromHadTop if getattr(ev,'nJet25%s_Recl'%var) > 0 else 0,
            'SelJet2_isFromHadTop'  : lambda ev : getattr(ev,'jetobjects')[1].isFromHadTop if getattr(ev,'nJet25%s_Recl'%var) > 1 else 0,
            'SelJet1_btagDeepFlavB' : lambda ev : ev.JetSel_Recl_btagDeepFlavB[0] if getattr(ev,'nJet25%s_Recl'%var) > 0 else 0,
            'SelJet2_pt'            : lambda ev : getattr(ev,'JetSel_Recl_pt%s'%var)[1] if getattr(ev,'nJet25%s_Recl'%var) > 1 else 0,             
            'SelJet2_eta'           : lambda ev : ev.JetSel_Recl_eta[1] if getattr(ev,'nJet25%s_Recl'%var) > 1 else 0,
            'SelJet2_phi'           : lambda ev : ev.JetSel_Recl_phi[1] if getattr(ev,'nJet25%s_Recl'%var) > 1 else 0,
            'SelJet2_btagDeepFlavB' : lambda ev : ev.JetSel_Recl_btagDeepFlavB[1] if getattr(ev,'nJet25%s_Recl'%var) > 1 else 0,
            'Lep1_pt'               : lambda ev : ev.LepGood_conePt[int(ev.iLepFO_Recl[0])],
            'Lep2_pt'               : lambda ev : ev.LepGood_conePt[int(ev.iLepFO_Recl[1])],
            'Lep1_eta'              : lambda ev : ev.LepGood_eta[int(ev.iLepFO_Recl[0])],
            'Lep2_eta'              : lambda ev : ev.LepGood_eta[int(ev.iLepFO_Recl[1])],
            'Lep1_phi'              : lambda ev : ev.LepGood_phi[int(ev.iLepFO_Recl[0])],
            'Lep2_phi'              : lambda ev : ev.LepGood_phi[int(ev.iLepFO_Recl[1])],
            'nSelJets'              : lambda ev : getattr(ev,'nJet25%s_Recl'%var),
            'met'                   : lambda ev : getattr(ev,'MET_pt%s'%var) if ev.year != 2017 else getattr(ev,'METFixEE2017_pt%s'%var),
            'HTT_score'             : lambda ev : getattr(ev,'BDThttTT_eventReco_mvaValue%s'%(var)) if getattr(ev,'BDThttTT_eventReco_mvaValue%s'%(var)) > 0 else 0,
            'visHiggs_pt'           : lambda ev : ev.visHiggs_pt,
            'visHiggs_eta'          : lambda ev : ev.visHiggs_eta,
            'mT_lep2'               : lambda ev : getattr(ev,'MT_met_lep2%s'%var),
            'mT_lep1'               : lambda ev : getattr(ev,'MT_met_lep1%s'%var),
            'Hj_tagger_hadTop'      : lambda ev : getattr(ev,'BDThttTT_eventReco_Hj_score%s'%(var)) if getattr(ev,'BDThttTT_eventReco_Hj_score%s'%(var)) > 0 else 0 ,
            'avg_dr_jet'            : lambda ev : getattr(ev,'avg_dr_jet%s'%var) if  getattr(ev,'avg_dr_jet%s'%var) > 0 else -9,
            'mTTH_2lss1tau'         : lambda ev : ev.mTTH_2lss1tau,
            'Tau_pt'                : lambda ev : getattr(ev,'thetau').pt  if getattr(ev,'thetau') else 0,
            'Tau_eta'               : lambda ev : getattr(ev,'thetau').eta if getattr(ev,'thetau') else 0,
            'Tau_phi'               : lambda ev : getattr(ev,'thetau').phi if getattr(ev,'thetau') else 0,
        }


    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        declareOutput(self, wrappedOutputTree, self.outVars)

    def analyze(self,event):
        taus = [ t for t in Collection(event,'TauSel_Recl')]
        setattr(event , 'thetau', taus[int(event.Tau_tight2lss1tau_idx)] if event.Tau_tight2lss1tau_idx > -1 else None)
        all_leps = [l for l in Collection(event,"LepGood")]
        nFO = getattr(event,"nLepFO_Recl")
        chosen = getattr(event,"iLepFO_Recl")
        leps = [all_leps[chosen[i]] for i in xrange(nFO)]
        jets = [j for j in Collection(event,"JetSel_Recl")]

        if event.thetau and len(leps)>1:
            higgsLepton = leps[0] if deltaR(event.thetau,leps[0]) < deltaR(event.thetau,leps[1]) else leps[1]
            visHiggs = higgsLepton.p4() + event.thetau.p4()


            tthSystem = higgsLepton.p4() + event.thetau.p4()
            for j in [j for j in jets if j.pt >= 25][:4]:
                tthSystem+=j.p4()
            vmet=ROOT.TLorentzVector()
            vmet.SetPtEtaPhiM(event.MET_pt, 0, event.MET_phi, 0)
            tthSystem+=vmet


            setattr(event, 'visHiggs_pt' , visHiggs.Pt())
            setattr(event, 'visHiggs_eta', visHiggs.Eta())
            setattr(event, 'mTTH_2lss1tau', tthSystem.M())
        else:
            setattr(event, 'visHiggs_pt' , 0)
            setattr(event, 'visHiggs_eta', 0)
            setattr(event, 'mTTH_2lss1tau', 0)
        jets = [j for j in Collection(event,"JetSel_Recl")]
        for j in jets: 
            setattr(j, 'isFromHadTop', jets.index(j) in [int(event.BDThttTT_eventReco_iJetSel1), int(event.BDThttTT_eventReco_iJetSel2), int(event.BDThttTT_eventReco_iJetSel3)])
        setattr(event, 'jetobjects', jets)
        ret=[]
        for worker in self._MVAs:
            name = worker.name
            if ( not hasattr(event,"nJet25_jerUp_Recl") and not hasattr(event, "nJet25_jesBBEC1_yearDown_Recl")) and ('_jes' in name or  '_jer' in name or '_uncl' in name): continue # using jer bc components wont change
            scale = 0.00125436
            mini = -0.8
            data_min = 0.26197815
            ret.extend( [(x,(y - mini)/scale + data_min) for x,y in worker(event).iteritems()])
#            if event.event == 5704300:
#                print kk 
        writeOutput( self,  dict(ret))

        return True


