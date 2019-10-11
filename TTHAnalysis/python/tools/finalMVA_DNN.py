from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection as NanoAODCollection 

from CMGTools.TTHAnalysis.treeReAnalyzer import Collection as CMGCollection
from CMGTools.TTHAnalysis.tools.nanoAOD.friendVariableProducerTools import declareOutput, writeOutput
from CMGTools.TTHAnalysis.tools.tfTool import TFTool
import os 
from copy import deepcopy

class finalMVA_DNN(Module):
    def __init__(self):
        self.outVars = []
        vars_2lss = {'avg_dr_jet'          : lambda ev : ev.avg_dr_jet,
                     'ptmiss'              : lambda ev : ev.MET_pt if ev.year != 2017 else ev.METFixEE2017_pt, 
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
                     'jetForward1_pt'      : lambda ev : ev.FwdJet1_pt_Recl if ev.nFwdJet_Recl else 0,
                     'jetForward1_eta_abs' : lambda ev : abs(ev.FwdJet1_eta_Recl)  if ev.nFwdJet_Recl else -1,
                     'res-HTT_CSVsort4rd'  : lambda ev : ev.BDThttTT_eventReco_mvaValue,
                     'HadTop_pt_CSVsort4rd': lambda ev : ev.BDThttTT_eventReco_HadTop_pt,
                     'nJet'                : lambda ev : ev.nJet25_Recl,
                     'nBJetLoose'          : lambda ev : ev.nBJetLoose25_Recl,
                     'nBJetMedium'         : lambda ev : ev.nBJetMedium25_Recl,
                     'nElectron'           : lambda ev : int(abs(ev.LepGood_pdgId[int(ev.iLepFO_Recl[0])]) == 11 + abs(ev.LepGood_pdgId[int(ev.iLepFO_Recl[1])]) == 11 if ev.nLepFO_Recl > 1 else 0),
                     'sum_lep_charge'      : lambda ev : ev.LepGood_charge[int(ev.iLepFO_Recl[0])] + ev.LepGood_charge[int(ev.iLepFO_Recl[1])] if ev.nLepFO_Recl > 1 else 0,
                     'mvaOutput_Hj_tagger' : lambda ev : ev.BDThttTT_eventReco_Hj_score, 
        }
        
        cats_2lss = ['predictions_ttH', 'predictions_ttW', 'predictions_rest', 'predictions_tH']
        self.outVars.extend( ['DNN_2lss_' + x for x in cats_2lss])

        vars_2lss_jesTotalCorrUp = deepcopy(vars_2lss)
        vars_2lss_jesTotalCorrUp['avg_dr_jet'          ] =  lambda ev : ev.avg_dr_jet_jesTotalCorrUp
        vars_2lss_jesTotalCorrUp['ptmiss'              ] =  lambda ev : ev.MET_pt_jesTotalCorrUp if ev.year != 2017 else ev.METFixEE2017_pt_jesTotalCorrUp
        vars_2lss_jesTotalCorrUp['mbb_medium'          ] =  lambda ev : ev.mbb_jesTotalCorrUp
        vars_2lss_jesTotalCorrUp['jet1_pt'             ] =  lambda ev : ev.JetSel_Recl_jesTotalCorrUp_pt[0] if ev.nJetSel_Recl > 0 else 0
        vars_2lss_jesTotalCorrUp['jet2_pt'             ] =  lambda ev : ev.JetSel_Recl_jesTotalCorrUp_pt[1] if ev.nJetSel_Recl > 1 else 0
        vars_2lss_jesTotalCorrUp['jet3_pt'             ] =  lambda ev : ev.JetSel_Recl_jesTotalCorrUp_pt[2] if ev.nJetSel_Recl > 2 else 0
        vars_2lss_jesTotalCorrUp['jet4_pt'             ] =  lambda ev : ev.JetSel_Recl_jesTotalCorrUp_pt[3] if ev.nJetSel_Recl > 3 else 0
        vars_2lss_jesTotalCorrUp['lep1_mT'             ] =  lambda ev : ev.MT_met_lep1_jesTotalCorrUp
        vars_2lss_jesTotalCorrUp['lep1_min_dr_jet'     ] =  lambda ev : ev.mindr_lep1_jet_jesTotalCorrUp
        vars_2lss_jesTotalCorrUp['lep2_mT'             ] =  lambda ev : ev.MT_met_lep2_jesTotalCorrUp
        vars_2lss_jesTotalCorrUp['lep2_min_dr_jet'     ] =  lambda ev : ev.mindr_lep2_jet_jesTotalCorrUp
        vars_2lss_jesTotalCorrUp['nJetForward'         ] =  lambda ev : ev.nFwdJet_jecUp_Recl 
        vars_2lss_jesTotalCorrUp['jetForward1_pt'      ] =  lambda ev : ev.FwdJet1_pt_jecUp_Recl if ev.nFwdJet_jecUp_Recl else 0
        vars_2lss_jesTotalCorrUp['jetForward1_eta_abs' ] =  lambda ev : abs(ev.FwdJet1_eta_jecUp_Recl)  if ev.nFwdJet_jecUp_Recl else -1
        vars_2lss_jesTotalCorrUp['res-HTT_CSVsort4rd'  ] =  lambda ev : ev.BDThttTT_eventReco_mvaValue_jesTotalCorrUp
        vars_2lss_jesTotalCorrUp['HadTop_pt_CSVsort4rd'] =  lambda ev : ev.BDThttTT_eventReco_HadTop_pt_jesTotalCorrUp
        vars_2lss_jesTotalCorrUp['nJet'                ] =  lambda ev : ev.nJet25_jecUp_Recl
        vars_2lss_jesTotalCorrUp['nBJetLoose'          ] =  lambda ev : ev.nBJetLoose25_jecUp_Recl
        vars_2lss_jesTotalCorrUp['nBJetMedium'         ] =  lambda ev : ev.nBJetMedium25_jecUp_Recl
        vars_2lss_jesTotalCorrUp['mvaOutput_Hj_tagger' ] =  lambda ev : ev.BDThttTT_eventReco_Hj_score_jesTotalCorrUp
        self.outVars.extend( ['DNN_2lss_jesTotalCorrUp_' + x for x in cats_2lss])

        vars_2lss_jesTotalUnCorrUp = deepcopy(vars_2lss)
        vars_2lss_jesTotalUnCorrUp['avg_dr_jet'          ] =  lambda ev : ev.avg_dr_jet_jesTotalUnCorrUp
        vars_2lss_jesTotalUnCorrUp['ptmiss'              ] =  lambda ev : ev.MET_pt_jesTotalUnCorrUp if ev.year != 2017 else ev.METFixEE2017_pt_jesTotalUnCorrUp
        vars_2lss_jesTotalUnCorrUp['mbb_medium'          ] =  lambda ev : ev.mbb_jesTotalUnCorrUp
        vars_2lss_jesTotalUnCorrUp['jet1_pt'             ] =  lambda ev : ev.JetSel_Recl_jesTotalUnCorrUp_pt[0] if ev.nJetSel_Recl > 0 else 0
        vars_2lss_jesTotalUnCorrUp['jet2_pt'             ] =  lambda ev : ev.JetSel_Recl_jesTotalUnCorrUp_pt[1] if ev.nJetSel_Recl > 1 else 0
        vars_2lss_jesTotalUnCorrUp['jet3_pt'             ] =  lambda ev : ev.JetSel_Recl_jesTotalUnCorrUp_pt[2] if ev.nJetSel_Recl > 2 else 0
        vars_2lss_jesTotalUnCorrUp['jet4_pt'             ] =  lambda ev : ev.JetSel_Recl_jesTotalUnCorrUp_pt[3] if ev.nJetSel_Recl > 3 else 0
        vars_2lss_jesTotalUnCorrUp['lep1_mT'             ] =  lambda ev : ev.MT_met_lep1_jesTotalUnCorrUp
        vars_2lss_jesTotalUnCorrUp['lep1_min_dr_jet'     ] =  lambda ev : ev.mindr_lep1_jet_jesTotalUnCorrUp
        vars_2lss_jesTotalUnCorrUp['lep2_mT'             ] =  lambda ev : ev.MT_met_lep2_jesTotalUnCorrUp
        vars_2lss_jesTotalUnCorrUp['lep2_min_dr_jet'     ] =  lambda ev : ev.mindr_lep2_jet_jesTotalUnCorrUp
        vars_2lss_jesTotalUnCorrUp['nJetForward'         ] =  lambda ev : ev.nFwdJet_jecUp_Recl 
        vars_2lss_jesTotalUnCorrUp['jetForward1_pt'      ] =  lambda ev : ev.FwdJet1_pt_jecUp_Recl if ev.nFwdJet_jecUp_Recl else 0
        vars_2lss_jesTotalUnCorrUp['jetForward1_eta_abs' ] =  lambda ev : abs(ev.FwdJet1_eta_jecUp_Recl)  if ev.nFwdJet_jecUp_Recl else -1
        vars_2lss_jesTotalUnCorrUp['res-HTT_CSVsort4rd'  ] =  lambda ev : ev.BDThttTT_eventReco_mvaValue_jesTotalUnCorrUp
        vars_2lss_jesTotalUnCorrUp['HadTop_pt_CSVsort4rd'] =  lambda ev : ev.BDThttTT_eventReco_HadTop_pt_jesTotalUnCorrUp
        vars_2lss_jesTotalUnCorrUp['nJet'                ] =  lambda ev : ev.nJet25_jecUp_Recl
        vars_2lss_jesTotalUnCorrUp['nBJetLoose'          ] =  lambda ev : ev.nBJetLoose25_jecUp_Recl
        vars_2lss_jesTotalUnCorrUp['nBJetMedium'         ] =  lambda ev : ev.nBJetMedium25_jecUp_Recl
        vars_2lss_jesTotalUnCorrUp['mvaOutput_Hj_tagger' ] =  lambda ev : ev.BDThttTT_eventReco_Hj_score_jesTotalUnCorrUp
        self.outVars.extend( ['DNN_2lss_jesTotalUnCorrUp_' + x for x in cats_2lss])

        vars_2lss_jesTotalCorrDown = deepcopy(vars_2lss)
        vars_2lss_jesTotalCorrDown['avg_dr_jet'          ] =  lambda ev : ev.avg_dr_jet_jesTotalCorrDown
        vars_2lss_jesTotalCorrDown['ptmiss'              ] =  lambda ev : ev.MET_pt_jesTotalCorrDown if ev.year != 2017 else ev.METFixEE2017_pt_jesTotalCorrDown
        vars_2lss_jesTotalCorrDown['mbb_medium'          ] =  lambda ev : ev.mbb_jesTotalCorrDown
        vars_2lss_jesTotalCorrDown['jet1_pt'             ] =  lambda ev : ev.JetSel_Recl_jesTotalCorrDown_pt[0] if ev.nJetSel_Recl > 0 else 0
        vars_2lss_jesTotalCorrDown['jet2_pt'             ] =  lambda ev : ev.JetSel_Recl_jesTotalCorrDown_pt[1] if ev.nJetSel_Recl > 1 else 0
        vars_2lss_jesTotalCorrDown['jet3_pt'             ] =  lambda ev : ev.JetSel_Recl_jesTotalCorrDown_pt[2] if ev.nJetSel_Recl > 2 else 0
        vars_2lss_jesTotalCorrDown['jet4_pt'             ] =  lambda ev : ev.JetSel_Recl_jesTotalCorrDown_pt[3] if ev.nJetSel_Recl > 3 else 0
        vars_2lss_jesTotalCorrDown['lep1_mT'             ] =  lambda ev : ev.MT_met_lep1_jesTotalCorrDown
        vars_2lss_jesTotalCorrDown['lep1_min_dr_jet'     ] =  lambda ev : ev.mindr_lep1_jet_jesTotalCorrDown
        vars_2lss_jesTotalCorrDown['lep2_mT'             ] =  lambda ev : ev.MT_met_lep2_jesTotalCorrDown
        vars_2lss_jesTotalCorrDown['lep2_min_dr_jet'     ] =  lambda ev : ev.mindr_lep2_jet_jesTotalCorrDown
        vars_2lss_jesTotalCorrDown['nJetForward'         ] =  lambda ev : ev.nFwdJet_jecDown_Recl
        vars_2lss_jesTotalCorrDown['jetForward1_pt'      ] =  lambda ev : ev.FwdJet1_pt_jecDown_Recl if ev.nFwdJet_jecDown_Recl else 0
        vars_2lss_jesTotalCorrDown['jetForward1_eta_abs' ] =  lambda ev : abs(ev.FwdJet1_eta_jecDown_Recl)  if ev.nFwdJet_jecDown_Recl else -1
        vars_2lss_jesTotalCorrDown['res-HTT_CSVsort4rd'  ] =  lambda ev : ev.BDThttTT_eventReco_mvaValue_jesTotalCorrDown
        vars_2lss_jesTotalCorrDown['HadTop_pt_CSVsort4rd'] =  lambda ev : ev.BDThttTT_eventReco_HadTop_pt_jesTotalCorrDown
        vars_2lss_jesTotalCorrDown['nJet'                ] =  lambda ev : ev.nJet25_jecDown_Recl
        vars_2lss_jesTotalCorrDown['nBJetLoose'          ] =  lambda ev : ev.nBJetLoose25_jecDown_Recl
        vars_2lss_jesTotalCorrDown['nBJetMedium'         ] =  lambda ev : ev.nBJetMedium25_jecDown_Recl
        vars_2lss_jesTotalCorrDown['mvaOutput_Hj_tagger' ] =  lambda ev : ev.BDThttTT_eventReco_Hj_score_jesTotalCorrDown
        self.outVars.extend( ['DNN_2lss_jesTotalCorrDown_' + x for x in cats_2lss])

        vars_2lss_jesTotalUnCorrDown = deepcopy(vars_2lss)
        vars_2lss_jesTotalUnCorrDown['avg_dr_jet'          ] =  lambda ev : ev.avg_dr_jet_jesTotalUnCorrDown
        vars_2lss_jesTotalUnCorrDown['ptmiss'              ] =  lambda ev : ev.MET_pt_jesTotalUnCorrDown if ev.year != 2017 else ev.METFixEE2017_pt_jesTotalUnCorrDown
        vars_2lss_jesTotalUnCorrDown['mbb_medium'          ] =  lambda ev : ev.mbb_jesTotalUnCorrDown
        vars_2lss_jesTotalUnCorrDown['jet1_pt'             ] =  lambda ev : ev.JetSel_Recl_jesTotalUnCorrDown_pt[0] if ev.nJetSel_Recl > 0 else 0
        vars_2lss_jesTotalUnCorrDown['jet2_pt'             ] =  lambda ev : ev.JetSel_Recl_jesTotalUnCorrDown_pt[1] if ev.nJetSel_Recl > 1 else 0
        vars_2lss_jesTotalUnCorrDown['jet3_pt'             ] =  lambda ev : ev.JetSel_Recl_jesTotalUnCorrDown_pt[2] if ev.nJetSel_Recl > 2 else 0
        vars_2lss_jesTotalUnCorrDown['jet4_pt'             ] =  lambda ev : ev.JetSel_Recl_jesTotalUnCorrDown_pt[3] if ev.nJetSel_Recl > 3 else 0
        vars_2lss_jesTotalUnCorrDown['lep1_mT'             ] =  lambda ev : ev.MT_met_lep1_jesTotalUnCorrDown
        vars_2lss_jesTotalUnCorrDown['lep1_min_dr_jet'     ] =  lambda ev : ev.mindr_lep1_jet_jesTotalUnCorrDown
        vars_2lss_jesTotalUnCorrDown['lep2_mT'             ] =  lambda ev : ev.MT_met_lep2_jesTotalUnCorrDown
        vars_2lss_jesTotalUnCorrDown['lep2_min_dr_jet'     ] =  lambda ev : ev.mindr_lep2_jet_jesTotalUnCorrDown
        vars_2lss_jesTotalUnCorrDown['nJetForward'         ] =  lambda ev : ev.nFwdJet_jecDown_Recl
        vars_2lss_jesTotalUnCorrDown['jetForward1_pt'      ] =  lambda ev : ev.FwdJet1_pt_jecDown_Recl if ev.nFwdJet_jecDown_Recl else 0
        vars_2lss_jesTotalUnCorrDown['jetForward1_eta_abs' ] =  lambda ev : abs(ev.FwdJet1_eta_jecDown_Recl)  if ev.nFwdJet_jecDown_Recl else -1
        vars_2lss_jesTotalUnCorrDown['res-HTT_CSVsort4rd'  ] =  lambda ev : ev.BDThttTT_eventReco_mvaValue_jesTotalUnCorrDown
        vars_2lss_jesTotalUnCorrDown['HadTop_pt_CSVsort4rd'] =  lambda ev : ev.BDThttTT_eventReco_HadTop_pt_jesTotalUnCorrDown
        vars_2lss_jesTotalUnCorrDown['nJet'                ] =  lambda ev : ev.nJet25_jecDown_Recl
        vars_2lss_jesTotalUnCorrDown['nBJetLoose'          ] =  lambda ev : ev.nBJetLoose25_jecDown_Recl
        vars_2lss_jesTotalUnCorrDown['nBJetMedium'         ] =  lambda ev : ev.nBJetMedium25_jecDown_Recl
        vars_2lss_jesTotalUnCorrDown['mvaOutput_Hj_tagger' ] =  lambda ev : ev.BDThttTT_eventReco_Hj_score_jesTotalUnCorrDown
        self.outVars.extend( ['DNN_2lss_jesTotalUnCorrDown_' + x for x in cats_2lss])


        vars_2lss_jerUp = deepcopy(vars_2lss)
        vars_2lss_jerUp['avg_dr_jet'          ] =  lambda ev : ev.avg_dr_jet_jerUp
        vars_2lss_jerUp['ptmiss'              ] =  lambda ev : ev.MET_pt_jerUp if ev.year != 2017 else ev.METFixEE2017_pt_jerUp
        vars_2lss_jerUp['mbb_medium'          ] =  lambda ev : ev.mbb_jerUp
        vars_2lss_jerUp['jet1_pt'             ] =  lambda ev : ev.JetSel_Recl_jerUp_pt[0] if ev.nJetSel_Recl > 0 else 0
        vars_2lss_jerUp['jet2_pt'             ] =  lambda ev : ev.JetSel_Recl_jerUp_pt[1] if ev.nJetSel_Recl > 1 else 0
        vars_2lss_jerUp['jet3_pt'             ] =  lambda ev : ev.JetSel_Recl_jerUp_pt[2] if ev.nJetSel_Recl > 2 else 0
        vars_2lss_jerUp['jet4_pt'             ] =  lambda ev : ev.JetSel_Recl_jerUp_pt[3] if ev.nJetSel_Recl > 3 else 0
        vars_2lss_jerUp['lep1_mT'             ] =  lambda ev : ev.MT_met_lep1_jerUp
        vars_2lss_jerUp['lep1_min_dr_jet'     ] =  lambda ev : ev.mindr_lep1_jet_jerUp
        vars_2lss_jerUp['lep2_mT'             ] =  lambda ev : ev.MT_met_lep2_jerUp
        vars_2lss_jerUp['lep2_min_dr_jet'     ] =  lambda ev : ev.mindr_lep2_jet_jerUp
        vars_2lss_jerUp['nJetForward'         ] =  lambda ev : ev.nFwdJet_jerUp_Recl
        vars_2lss_jerUp['jetForward1_pt'      ] =  lambda ev : ev.FwdJet1_pt_jerUp_Recl if ev.nFwdJet_jerUp_Recl else 0
        vars_2lss_jerUp['jetForward1_eta_abs' ] =  lambda ev : abs(ev.FwdJet1_eta_jerUp_Recl) if ev.nFwdJet_jerUp_Recl else -1
        vars_2lss_jerUp['res-HTT_CSVsort4rd'  ] =  lambda ev : ev.BDThttTT_eventReco_mvaValue_jerUp
        vars_2lss_jerUp['HadTop_pt_CSVsort4rd'] =  lambda ev : ev.BDThttTT_eventReco_HadTop_pt_jerUp
        vars_2lss_jerUp['nJet'                ] =  lambda ev : ev.nJet25_jerUp_Recl
        vars_2lss_jerUp['nBJetLoose'          ] =  lambda ev : ev.nBJetLoose25_jerUp_Recl
        vars_2lss_jerUp['nBJetMedium'         ] =  lambda ev : ev.nBJetMedium25_jerUp_Recl
        vars_2lss_jerUp['mvaOutput_Hj_tagger' ] =  lambda ev : ev.BDThttTT_eventReco_Hj_score_jerUp
        self.outVars.extend( ['DNN_2lss_jerUp_' + x for x in cats_2lss])

        vars_2lss_jerDown = deepcopy(vars_2lss)
        vars_2lss_jerDown['avg_dr_jet'          ] =  lambda ev : ev.avg_dr_jet_jerDown
        vars_2lss_jerDown['ptmiss'              ] =  lambda ev : ev.MET_pt_jerDown if ev.year != 2017 else ev.METFixEE2017_pt_jerDown
        vars_2lss_jerDown['mbb_medium'          ] =  lambda ev : ev.mbb_jerDown
        vars_2lss_jerDown['jet1_pt'             ] =  lambda ev : ev.JetSel_Recl_jerDown_pt[0] if ev.nJetSel_Recl > 0 else 0
        vars_2lss_jerDown['jet2_pt'             ] =  lambda ev : ev.JetSel_Recl_jerDown_pt[1] if ev.nJetSel_Recl > 1 else 0
        vars_2lss_jerDown['jet3_pt'             ] =  lambda ev : ev.JetSel_Recl_jerDown_pt[2] if ev.nJetSel_Recl > 2 else 0
        vars_2lss_jerDown['jet4_pt'             ] =  lambda ev : ev.JetSel_Recl_jerDown_pt[3] if ev.nJetSel_Recl > 3 else 0
        vars_2lss_jerDown['lep1_mT'             ] =  lambda ev : ev.MT_met_lep1_jerDown
        vars_2lss_jerDown['lep1_min_dr_jet'     ] =  lambda ev : ev.mindr_lep1_jet_jerDown
        vars_2lss_jerDown['lep2_mT'             ] =  lambda ev : ev.MT_met_lep2_jerDown
        vars_2lss_jerDown['lep2_min_dr_jet'     ] =  lambda ev : ev.mindr_lep2_jet_jerDown
        vars_2lss_jerDown['nJetForward'         ] =  lambda ev : ev.nFwdJet_jerDown_Recl
        vars_2lss_jerDown['jetForward1_pt'      ] =  lambda ev : ev.FwdJet1_pt_jerDown_Recl if ev.nFwdJet_jerDown_Recl  else 0
        vars_2lss_jerDown['jetForward1_eta_abs' ] =  lambda ev : abs(ev.FwdJet1_eta_jerDown_Recl) if ev.nFwdJet_jerDown_Recl  else -1
        vars_2lss_jerDown['res-HTT_CSVsort4rd'  ] =  lambda ev : ev.BDThttTT_eventReco_mvaValue_jerDown
        vars_2lss_jerDown['HadTop_pt_CSVsort4rd'] =  lambda ev : ev.BDThttTT_eventReco_HadTop_pt_jerDown
        vars_2lss_jerDown['nJet'                ] =  lambda ev : ev.nJet25_jerDown_Recl
        vars_2lss_jerDown['nBJetLoose'          ] =  lambda ev : ev.nBJetLoose25_jerDown_Recl
        vars_2lss_jerDown['nBJetMedium'         ] =  lambda ev : ev.nBJetMedium25_jerDown_Recl
        vars_2lss_jerDown['mvaOutput_Hj_tagger' ] =  lambda ev : ev.BDThttTT_eventReco_Hj_score_jerDown
        self.outVars.extend( ['DNN_2lss_jerDown_' + x for x in cats_2lss])


        vars_2lss_unclUp = deepcopy(vars_2lss)
        vars_2lss_unclUp['lep1_mT'             ] =  lambda ev : ev.MT_met_lep1_unclustEnUp
        vars_2lss_unclUp['lep2_mT'             ] =  lambda ev : ev.MT_met_lep2_unclustEnUp

        vars_2lss_unclDown = deepcopy(vars_2lss)
        vars_2lss_unclDown['lep1_mT'             ] =  lambda ev : ev.MT_met_lep1_unclustEnDown
        vars_2lss_unclDown['lep2_mT'             ] =  lambda ev : ev.MT_met_lep2_unclustEnDown

        varorder = ['avg_dr_jet', 'ptmiss', 'mbb_medium', 'jet1_pt', 'jet2_pt', 'jet3_pt', 'jet4_pt', 'max_lep_eta', 'lep1_mT', 'lep1_conept', 'lep1_min_dr_jet', 'lep2_mT', 'lep2_conept', 'lep2_min_dr_jet', 'nJetForward', 'jetForward1_pt', 'jetForward1_eta_abs', 'res-HTT_CSVsort4rd', 'HadTop_pt_CSVsort4rd', 'nJet', 'nBJetLoose', 'nBJetMedium', 'nElectron', 'sum_lep_charge', 'mvaOutput_Hj_tagger']

        worker_2lss = TFTool('DNN_2lss', os.environ['CMSSW_BASE'] + '/src/CMGTools/TTHAnalysis/data/kinMVA/tth/test_model_2lss_ttH_tH_4cat_onlyTHQ_notEnrich_v4.pb',
                                   vars_2lss, cats_2lss, varorder)
        worker_2lss_jesTotalCorrUp = TFTool('DNN_2lss_jesTotalCorrUp', os.environ['CMSSW_BASE'] + '/src/CMGTools/TTHAnalysis/data/kinMVA/tth/test_model_2lss_ttH_tH_4cat_onlyTHQ_notEnrich_v4.pb',
                                        vars_2lss_jesTotalCorrUp, cats_2lss, varorder)
        worker_2lss_jesTotalUnCorrUp = TFTool('DNN_2lss_jesTotalUnCorrUp', os.environ['CMSSW_BASE'] + '/src/CMGTools/TTHAnalysis/data/kinMVA/tth/test_model_2lss_ttH_tH_4cat_onlyTHQ_notEnrich_v4.pb',
                                        vars_2lss_jesTotalUnCorrUp, cats_2lss, varorder)
        worker_2lss_jesTotalCorrDown = TFTool('DNN_2lss_jesTotalCorrDown', os.environ['CMSSW_BASE'] + '/src/CMGTools/TTHAnalysis/data/kinMVA/tth/test_model_2lss_ttH_tH_4cat_onlyTHQ_notEnrich_v4.pb',
                                        vars_2lss_jesTotalCorrDown, cats_2lss, varorder)
        worker_2lss_jesTotalUnCorrDown = TFTool('DNN_2lss_jesTotalUnCorrDown', os.environ['CMSSW_BASE'] + '/src/CMGTools/TTHAnalysis/data/kinMVA/tth/test_model_2lss_ttH_tH_4cat_onlyTHQ_notEnrich_v4.pb',
                                        vars_2lss_jesTotalUnCorrDown, cats_2lss, varorder)
        worker_2lss_jerUp        = TFTool('DNN_2lss_jerUp', os.environ['CMSSW_BASE'] + '/src/CMGTools/TTHAnalysis/data/kinMVA/tth/test_model_2lss_ttH_tH_4cat_onlyTHQ_notEnrich_v4.pb',
                                          vars_2lss_jerUp, cats_2lss, varorder)
        worker_2lss_jerDown      = TFTool('DNN_2lss_jerDown', os.environ['CMSSW_BASE'] + '/src/CMGTools/TTHAnalysis/data/kinMVA/tth/test_model_2lss_ttH_tH_4cat_onlyTHQ_notEnrich_v4.pb',
                                          vars_2lss_jerDown, cats_2lss, varorder)

        worker_2lss_unclUp        = TFTool('DNN_2lss_unclUp', os.environ['CMSSW_BASE'] + '/src/CMGTools/TTHAnalysis/data/kinMVA/tth/test_model_2lss_ttH_tH_4cat_onlyTHQ_notEnrich_v4.pb',
                                          vars_2lss_unclUp, cats_2lss, varorder)
        worker_2lss_unclDown      = TFTool('DNN_2lss_unclDown', os.environ['CMSSW_BASE'] + '/src/CMGTools/TTHAnalysis/data/kinMVA/tth/test_model_2lss_ttH_tH_4cat_onlyTHQ_notEnrich_v4.pb',
                                          vars_2lss_unclDown, cats_2lss, varorder)
        
        self._MVAs = [worker_2lss, worker_2lss_jesTotalCorrUp,worker_2lss_jesTotalUnCorrUp,worker_2lss_jesTotalCorrDown, worker_2lss_jesTotalUnCorrDown, worker_2lss_jerUp,worker_2lss_jerDown, worker_2lss_unclUp,worker_2lss_unclDown] 


    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        print self.outVars
        declareOutput(self, wrappedOutputTree, self.outVars)
        
    def analyze(self,event):
        myvars = [event.iLepFO_Recl[0],event.iLepFO_Recl[1],event.iLepFO_Recl[2]]
        ret = []
        for worker in self._MVAs:
            name = worker.name
            if not hasattr(event,"nJet25_jesDown_Recl") and ('_jes' in name or  '_jer' in name or '_uncl' in name): continue
            #if not ('_jes' in name or  '_jer' in name or '_uncl' in name) and event.event == 259935: worker.debug=True
            ret.extend( [(x,y) for x,y in worker(event).iteritems()])
            #if not ('_jes' in name or  '_jer' in name or '_uncl' in name) and event.event == 259935: worker.debug=False

            
        writeOutput(self, dict(ret))
        return True
