from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection as NanoAODCollection 

from CMGTools.TTHAnalysis.treeReAnalyzer import Collection as CMGCollection
from CMGTools.TTHAnalysis.tools.nanoAOD.friendVariableProducerTools import declareOutput, writeOutput
from CMGTools.TTHAnalysis.tools.tfTool import TFTool
import os 
class finalMVA_DNN():
    def __init__(self):
        print 'here'
        self._MVAs = {}
        vars_2lss = {'avg_dr_jet'          : lambda ev : ev.avg_dr_jet,
                     'ptmiss'              : lambda ev : ev.MET_pt, 
                     'mbb_medium'          : lambda ev : ev.mbb,
                     'jet1_pt'             : lambda ev : ev.JetSel_Recl_pt[0] if ev.nJetSel_Recl > 0 else 0,
                     'jet2_pt'             : lambda ev : ev.JetSel_Recl_pt[1] if ev.nJetSel_Recl > 1 else 0,
                     'jet3_pt'             : lambda ev : ev.JetSel_Recl_pt[2] if ev.nJetSel_Recl > 2 else 0,
                     'jet4_pt'             : lambda ev : ev.JetSel_Recl_pt[3] if ev.nJetSel_Recl > 3 else 0,
                     'max_lep_eta'         : lambda ev : max(abs(ev.LepGood1_eta),abs(ev.LepGood2_eta)),
                     'lep1_mT'             : lambda ev : ev.MT_met_lep1,
                     'lep1_conept'         : lambda ev : ev.LepGood1_conept,
                     'lep1_min_dr_jet'     : lambda ev : ev.mindr_lep1_jet,
                     'lep2_mT'             : lambda ev : ev.MT_met_lep2,
                     'lep2_conept'         : lambda ev : ev.LepGood2_conept,
                     'lep2_min_dr_jet'     : lambda ev : ev.mindr_lep2_jet,
                     'nJetForward'         : lambda ev : ev.nFwdJet_Recl,
                     'jetForward1_pt'      : lambda ev : 0, # to do! 
                     'jetForward1_eta_abs' : lambda ev : 0, # to do! 
                     'res-HTT_CSVsort4rd'  : lambda ev : ev.BDThttTT_eventReco_mvaValue,
                     'HadTop_pt_CSVsort4rd': lambda ev : ev.BDThttTT_eventReco_HadTop_pt,
                     'nJet'                : lambda ev : ev.nJetSel_Recl,
                     'nBJetLoose'          : lambda ev : ev.nBJetLoose25,
                     'nBJetMedium'         : lambda ev : ev.nBJetMedium25,
                     'nElectron'           : lambda ev : abs(ev.Lep1_pdgId) == 11 + abs(ev.Lep2_pdgId) == 11,
                     'sum_lep_charge'      : lambda ev : ev.Lep1_charge + ev.Lep2_charge,
                     'mvaOutput_Hj_tagger' : lambda ev : ev.BDThttTT_eventReco_Hj_score, 
        }
        cats_2lss = ['predictions_ttH', 'predictions_ttW', 'predictions_rest', 'predictions_tH']

        #vars_2lss_jecUp = vars_2lss
        #vars_2lss_jecUp['modifythis']
        self.worker_2lss = TFTool('DNN_2lss', os.environ['CMSSW_BASE'] + '/src/CMGTools/TTHAnalysis/data/kinMVA/tth/test_model_2lss_ttH_tH_4cat_onlyTHQ_notEnrich_v4.pb',
                                   vars_2lss, cats_2lss)
    def analyze(self,event):
        print self.worker_2lss(event)
