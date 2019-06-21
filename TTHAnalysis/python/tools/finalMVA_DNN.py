from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection as NanoAODCollection 

from CMGTools.TTHAnalysis.treeReAnalyzer import Collection as CMGCollection
from CMGTools.TTHAnalysis.tools.nanoAOD.friendVariableProducerTools import declareOutput, writeOutput
from CMGTools.TTHAnalysis.tools.tfTool import TFTool
import os 


class finalMVA_DNN(Module):
    def __init__(self):
        self.outVars = []
        vars_2lss = {'avg_dr_jet'          : lambda ev : ev.avg_dr_jet,
                     'ptmiss'              : lambda ev : ev.MET_pt, 
                     'mbb_medium'          : lambda ev : ev.mbb,
                     'jet1_pt'             : lambda ev : ev.JetSel_Recl_pt[0] if ev.nJetSel_Recl > 0 else 0,
                     'jet2_pt'             : lambda ev : ev.JetSel_Recl_pt[1] if ev.nJetSel_Recl > 1 else 0,
                     'jet3_pt'             : lambda ev : ev.JetSel_Recl_pt[2] if ev.nJetSel_Recl > 2 else 0,
                     'jet4_pt'             : lambda ev : ev.JetSel_Recl_pt[3] if ev.nJetSel_Recl > 3 else 0,
                     'max_lep_eta'         : lambda ev : max(abs(ev.LepGood_eta[int(ev.iLepFO_Recl[0])]),abs(ev.LepGood_eta[int(ev.iLepFO_Recl[1])])) if ev.nLepFO_Recl > 1 else 0,
                     'lep1_mT'             : lambda ev : ev.MT_met_lep1,
                     'lep1_conept'         : lambda ev : ev.LepGood_conePt[int(ev.iLepFO_Recl[0])], 
                     'lep1_min_dr_jet'     : lambda ev : ev.mindr_lep1_jet,
                     'lep2_mT'             : lambda ev : ev.MT_met_lep2,
                     'lep2_conept'         : lambda ev : ev.LepGood_conePt[int(ev.iLepFO_Recl[1])],
                     'lep2_min_dr_jet'     : lambda ev : ev.mindr_lep2_jet,
                     'nJetForward'         : lambda ev : ev.nFwdJet_Recl,
                     'jetForward1_pt'      : lambda ev : ev.FwdJet1_pt_Recl,
                     'jetForward1_eta_abs' : lambda ev : abs(ev.FwdJet1_eta_Recl),
                     'res-HTT_CSVsort4rd'  : lambda ev : ev.BDThttTT_eventReco_mvaValue,
                     'HadTop_pt_CSVsort4rd': lambda ev : ev.BDThttTT_eventReco_HadTop_pt,
                     'nJet'                : lambda ev : ev.nJet25_Recl,
                     'nBJetLoose'          : lambda ev : ev.nBJetLoose25_Recl,
                     'nBJetMedium'         : lambda ev : ev.nBJetMedium25_Recl,
                     'nElectron'           : lambda ev : abs(ev.LepGood_pdgId[int(ev.iLepFO_Recl[0])]) == 11 + abs(ev.LepGood_pdgId[int(ev.iLepFO_Recl[1])]) == 11 if ev.nLepFO_Recl > 1 else 0,
                     'sum_lep_charge'      : lambda ev : ev.LepGood_charge[int(ev.iLepFO_Recl[0])] + ev.LepGood_charge[int(ev.iLepFO_Recl[1])] if ev.nLepFO_Recl > 1 else 0,
                     'mvaOutput_Hj_tagger' : lambda ev : ev.BDThttTT_eventReco_Hj_score, 
        }
        
        cats_2lss = ['predictions_ttH', 'predictions_ttW', 'predictions_rest', 'predictions_tH']
        self.outVars.extend( ['DNN_2lss_' + x for x in cats_2lss])

        vars_2lss_jesTotalUp = vars_2lss
        vars_2lss_jesTotalUp['avg_dr_jet'          ] =  lambda ev : ev.avg_dr_jet_jesTotalUp
        vars_2lss_jesTotalUp['ptmiss'              ] =  lambda ev : ev.MET_pt_jesTotalUp
        vars_2lss_jesTotalUp['mbb_medium'          ] =  lambda ev : ev.mbb_jesTotalUp
        vars_2lss_jesTotalUp['jet1_pt'             ] =  lambda ev : ev.JetSel_Recl_pt[0] if ev.nJetSel_Recl > 0 else 0
        vars_2lss_jesTotalUp['jet2_pt'             ] =  lambda ev : ev.JetSel_Recl_pt[1] if ev.nJetSel_Recl > 1 else 0
        vars_2lss_jesTotalUp['jet3_pt'             ] =  lambda ev : ev.JetSel_Recl_pt[2] if ev.nJetSel_Recl > 2 else 0
        vars_2lss_jesTotalUp['jet4_pt'             ] =  lambda ev : ev.JetSel_Recl_pt[3] if ev.nJetSel_Recl > 3 else 0
        vars_2lss_jesTotalUp['lep1_mT'             ] =  lambda ev : ev.MT_met_lep1_jesTotalUp
        vars_2lss_jesTotalUp['lep1_min_dr_jet'     ] =  lambda ev : ev.mindr_lep1_jet_jesTotalUp
        vars_2lss_jesTotalUp['lep2_mT'             ] =  lambda ev : ev.MT_met_lep2_jesTotalUp
        vars_2lss_jesTotalUp['lep2_min_dr_jet'     ] =  lambda ev : ev.mindr_lep2_jet_jesTotalUp
        vars_2lss_jesTotalUp['nJetForward'         ] =  lambda ev : ev.nFwdJet_jecUp_Recl
        vars_2lss_jesTotalUp['jetForward1_pt'      ] =  lambda ev : ev.FwdJet1_pt_jecUp_Recl
        vars_2lss_jesTotalUp['jetForward1_eta_abs' ] =  lambda ev : abs(ev.FwdJet1_eta_jecUp_Recl)
        vars_2lss_jesTotalUp['res-HTT_CSVsort4rd'  ] =  lambda ev : ev.BDThttTT_eventReco_mvaValue_jesTotalUp
        vars_2lss_jesTotalUp['HadTop_pt_CSVsort4rd'] =  lambda ev : ev.BDThttTT_eventReco_HadTop_pt_jesTotalUp
        vars_2lss_jesTotalUp['nJet'                ] =  lambda ev : ev.nJet25_jecUp_Recl
        vars_2lss_jesTotalUp['nBJetLoose'          ] =  lambda ev : ev.nBJetLoose25_jecUp_Recl
        vars_2lss_jesTotalUp['nBJetMedium'         ] =  lambda ev : ev.nBJetMedium25_jecUp_Recl
        vars_2lss_jesTotalUp['mvaOutput_Hj_tagger' ] =  lambda ev : ev.BDThttTT_eventReco_Hj_score_jesTotalUp
        self.outVars.extend( ['DNN_2lss_jesTotalUp_' + x for x in cats_2lss])

        vars_2lss_jesTotalDown = vars_2lss
        vars_2lss_jesTotalDown['avg_dr_jet'          ] =  lambda ev : ev.avg_dr_jet_jesTotalDown
        vars_2lss_jesTotalDown['ptmiss'              ] =  lambda ev : ev.MET_pt_jesTotalDown
        vars_2lss_jesTotalDown['mbb_medium'          ] =  lambda ev : ev.mbb_jesTotalDown
        vars_2lss_jesTotalDown['jet1_pt'             ] =  lambda ev : ev.JetSel_Recl_pt[0] if ev.nJetSel_Recl > 0 else 0
        vars_2lss_jesTotalDown['jet2_pt'             ] =  lambda ev : ev.JetSel_Recl_pt[1] if ev.nJetSel_Recl > 1 else 0
        vars_2lss_jesTotalDown['jet3_pt'             ] =  lambda ev : ev.JetSel_Recl_pt[2] if ev.nJetSel_Recl > 2 else 0
        vars_2lss_jesTotalDown['jet4_pt'             ] =  lambda ev : ev.JetSel_Recl_pt[3] if ev.nJetSel_Recl > 3 else 0
        vars_2lss_jesTotalDown['lep1_mT'             ] =  lambda ev : ev.MT_met_lep1_jesTotalDown
        vars_2lss_jesTotalDown['lep1_min_dr_jet'     ] =  lambda ev : ev.mindr_lep1_jet_jesTotalDown
        vars_2lss_jesTotalDown['lep2_mT'             ] =  lambda ev : ev.MT_met_lep2_jesTotalDown
        vars_2lss_jesTotalDown['lep2_min_dr_jet'     ] =  lambda ev : ev.mindr_lep2_jet_jesTotalDown
        vars_2lss_jesTotalDown['nJetForward'         ] =  lambda ev : ev.nFwdJet_jecDown_Recl
        vars_2lss_jesTotalDown['jetForward1_pt'      ] =  lambda ev : ev.FwdJet1_pt_jecDown_Recl
        vars_2lss_jesTotalDown['jetForward1_eta_abs' ] =  lambda ev : abs(ev.FwdJet1_eta_jecDown_Recl)
        vars_2lss_jesTotalDown['res-HTT_CSVsort4rd'  ] =  lambda ev : ev.BDThttTT_eventReco_mvaValue_jesTotalDown
        vars_2lss_jesTotalDown['HadTop_pt_CSVsort4rd'] =  lambda ev : ev.BDThttTT_eventReco_HadTop_pt_jesTotalDown
        vars_2lss_jesTotalDown['nJet'                ] =  lambda ev : ev.nJet25_jecDown_Recl
        vars_2lss_jesTotalDown['nBJetLoose'          ] =  lambda ev : ev.nBJetLoose25_jecDown_Recl
        vars_2lss_jesTotalDown['nBJetMedium'         ] =  lambda ev : ev.nBJetMedium25_jecDown_Recl
        vars_2lss_jesTotalDown['mvaOutput_Hj_tagger' ] =  lambda ev : ev.BDThttTT_eventReco_Hj_score_jesTotalDown
        self.outVars.extend( ['DNN_2lss_jesTotalDown_' + x for x in cats_2lss])


        worker_2lss = TFTool('DNN_2lss', os.environ['CMSSW_BASE'] + '/src/CMGTools/TTHAnalysis/data/kinMVA/tth/test_model_2lss_ttH_tH_4cat_onlyTHQ_notEnrich_v4.pb',
                                   vars_2lss, cats_2lss)
        worker_2lss_jesTotalUp = TFTool('DNN_2lss_jesTotalUp', os.environ['CMSSW_BASE'] + '/src/CMGTools/TTHAnalysis/data/kinMVA/tth/test_model_2lss_ttH_tH_4cat_onlyTHQ_notEnrich_v4.pb',
                                        vars_2lss_jesTotalUp, cats_2lss)
        worker_2lss_jesTotalDown = TFTool('DNN_2lss_jesTotalDown', os.environ['CMSSW_BASE'] + '/src/CMGTools/TTHAnalysis/data/kinMVA/tth/test_model_2lss_ttH_tH_4cat_onlyTHQ_notEnrich_v4.pb',
                                        vars_2lss_jesTotalDown, cats_2lss)
        self._MVAs = [worker_2lss, worker_2lss_jesTotalUp,worker_2lss_jesTotalDown] 


    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        print self.outVars
        declareOutput(self, wrappedOutputTree, self.outVars)
        
    def analyze(self,event):
        myvars = [event.iLepFO_Recl[0],event.iLepFO_Recl[1],event.iLepFO_Recl[2]]
        ret = []
        for worker in self._MVAs:
            ret.extend( [(x,y) for x,y in worker(event).iteritems()])
        writeOutput(self, dict(ret))
        return True
