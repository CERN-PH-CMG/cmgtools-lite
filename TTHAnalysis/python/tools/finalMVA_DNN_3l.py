from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection as NanoAODCollection 

from CMGTools.TTHAnalysis.treeReAnalyzer import Collection as CMGCollection
from CMGTools.TTHAnalysis.tools.nanoAOD.friendVariableProducerTools import declareOutput, writeOutput
from CMGTools.TTHAnalysis.tools.tfTool import TFTool
import os 
from copy import deepcopy

class finalMVA_DNN_3l(Module):
    def __init__(self):
        self.outVars = []
        vars_3l = {'avg_dr_jet'             : lambda ev : ev.avg_dr_jet,
                   'min_dr_Lep'             : lambda ev : min([ev.drlep12, ev.drlep13, ev.drlep23]),
                   'jet1_pt'                : lambda ev : ev.JetSel_Recl_pt[0] if ev.nJet25_Recl > 0 else 0,
                   'lep1_conePt'            : lambda ev : ev.LepGood_conePt[int(ev.iLepFO_Recl[0])], 
                   'mindr_lep1_jet'         : lambda ev : ev.mindr_lep1_jet,
                   'jet2_pt'                : lambda ev : ev.JetSel_Recl_pt[1] if ev.nJet25_Recl > 1 else 0,
                   'leadFwdJet_pt'          : lambda ev : ev.FwdJet1_pt_Recl if ev.nFwdJet_Recl else 0,
                   'lep3_conePt'            : lambda ev : ev.LepGood_conePt[int(ev.iLepFO_Recl[2])],
                   'mindr_lep2_jet'         : lambda ev : ev.mindr_lep2_jet,                   
                   'nBJetMedium'            : lambda ev : ev.nBJetMedium25_Recl,
                   'mindr_lep3_jet'         : lambda ev : ev.mindr_lep3_jet, #### 
                   'mbb_loose'              : lambda ev : ev.mbb_loose,
                   'met_LD'                 : lambda ev : (ev.MET_pt if ev.year != 2017 else ev.METFixEE2017_pt) *0.6 + ev.mhtJet25_Recl*0.4,
                   'lep2_conePt'            : lambda ev : ev.LepGood_conePt[int(ev.iLepFO_Recl[1])],
                   'jet1_eta'               : lambda ev : abs(ev.JetSel_Recl_eta[0]) if ev.nJet25_Recl > 0 else 0,
                   'jet3_pt'                : lambda ev : ev.JetSel_Recl_pt[2] if ev.nJet25_Recl > 2 else 0,
                   'HadTop_pt'              : lambda ev : ev.BDThttTT_eventReco_HadTop_pt if ev.BDThttTT_eventReco_mvaValue > 0 else 0,
                   'has_SFOS'               : lambda ev : ev.hasOSSF3l,
                   'sum_Lep_charge'         : lambda ev : (ev.LepGood_charge[int(ev.iLepFO_Recl[0])]+ev.LepGood_charge[int(ev.iLepFO_Recl[1])]+ev.LepGood_charge[int(ev.iLepFO_Recl[2])]) if ev.nLepFO_Recl >= 3 else 0,
                   'nJet'                   : lambda ev : ev.nJet25_Recl,
                   'lep3_eta'               : lambda ev : abs(ev.LepGood_eta[int(ev.iLepFO_Recl[2])]) if ev.nLepFO_Recl >= 3 else 0,
                   'res_HTT'                : lambda ev : ev.BDThttTT_eventReco_mvaValue if ev.BDThttTT_eventReco_mvaValue > 0 else 0,
                   'lep1_eta'               : lambda ev : abs(ev.LepGood_eta[int(ev.iLepFO_Recl[0])]) if ev.nLepFO_Recl >= 1 else 0,
                   'lep2_eta'               : lambda ev : abs(ev.LepGood_eta[int(ev.iLepFO_Recl[1])]) if ev.nLepFO_Recl >= 2 else 0,
                   'lep3_eta'               : lambda ev : abs(ev.LepGood_eta[int(ev.iLepFO_Recl[2])]) if ev.nLepFO_Recl >= 3 else 0,
                   'min_Deta_leadfwdJet_jet': lambda ev : ev.min_Deta_leadfwdJet_jet,
                   'jet2_phi'               : lambda ev : ev.JetSel_Recl_phi[1] if ev.nJet25_Recl >= 2 else 0,
                   'jet1_phi'               : lambda ev : ev.JetSel_Recl_phi[0] if ev.nJet25_Recl >= 1 else 0,
                   'lep3_phi'               : lambda ev : (ev.LepGood_phi[int(ev.iLepFO_Recl[2])]) if ev.nLepFO_Recl >= 3 else 0,
                   'lep2_phi'               : lambda ev : (ev.LepGood_phi[int(ev.iLepFO_Recl[1])]) if ev.nLepFO_Recl >= 2 else 0,
                   'leadFwdJet_eta'         : lambda ev : abs(ev.FwdJet1_eta_Recl) if ev.nFwdJet_Recl else 0,
                   'jet3_eta'               : lambda ev : abs(ev.JetSel_Recl_eta[2]) if ev.nJet25_Recl >= 3 else 0,
                   'jet2_eta'               : lambda ev : abs(ev.JetSel_Recl_eta[1]) if ev.nJet25_Recl >= 2 else 0,
                   'nElectron'              : lambda ev : ((abs(ev.LepGood_pdgId[int(ev.iLepFO_Recl[0])]) == 11) + (abs(ev.LepGood_pdgId[int(ev.iLepFO_Recl[1])]) == 11) + (abs(ev.LepGood_pdgId[int(ev.iLepFO_Recl[2])]) == 11)) if ev.nLepFO_Recl >= 3 else 0,
                   'lep1_phi'               : lambda ev : (ev.LepGood_phi[int(ev.iLepFO_Recl[0])]) if ev.nLepFO_Recl >= 1 else 0,
                   'jet3_phi'               : lambda ev : ev.JetSel_Recl_phi[2] if ev.nJet25_Recl >= 3 else 0,
                   'nBJetLoose'             : lambda ev : ev.nBJetLoose25_Recl,
                   'nJetForward'            : lambda ev : ev.nFwdJet_Recl
        }
        cats_3l = ["predictions_ttH",  "predictions_rest", "predictions_tH"]
        varorder = ['lep1_conePt', 'lep1_eta', 'lep1_phi', 'lep2_conePt', 'lep2_eta', 'lep2_phi', 'lep3_conePt', 'lep3_eta', 'lep3_phi', 'mindr_lep1_jet', 'mindr_lep2_jet', 'mindr_lep3_jet', 'min_dr_Lep', 'avg_dr_jet', 'met_LD', 'mbb_loose', 'leadFwdJet_eta', 'leadFwdJet_pt', 'min_Deta_leadfwdJet_jet', 'jet1_pt', 'jet1_eta', 'jet1_phi', 'jet2_pt', 'jet2_eta', 'jet2_phi', 'jet3_pt', 'jet3_eta', 'jet3_phi', 'sum_Lep_charge', 'HadTop_pt', 'res_HTT', 'nJet', 'nBJetLoose', 'nBJetMedium', 'nJetForward', 'nElectron', 'has_SFOS']
        self.outVars.extend( ['DNN_3l_' + x for x in cats_3l])

        vars_3l_jesTotalCorrUp = deepcopy(vars_3l)
        vars_3l_jesTotalCorrUp['avg_dr_jet'             ] =  lambda ev : ev.avg_dr_jet_jesTotalCorrUp
        vars_3l_jesTotalCorrUp['jet1_pt'                ] =  lambda ev : ev.JetSel_Recl_pt_jesTotalCorrUp[0] if ev.nJet25_jesTotalCorrUp_Recl > 0 else 0
        vars_3l_jesTotalCorrUp['jet2_pt'                ] =  lambda ev : ev.JetSel_Recl_pt_jesTotalCorrUp[1] if ev.nJet25_jesTotalCorrUp_Recl > 1 else 0
        vars_3l_jesTotalCorrUp['leadFwdJet_pt'          ] =  lambda ev : ev.FwdJet1_pt_jesTotalCorrUp_Recl if ev.nFwdJet_jesTotalCorrUp_Recl else 0
        vars_3l_jesTotalCorrUp['nBJetMedium'            ] =  lambda ev : ev.nBJetMedium25_jesTotalCorrUp_Recl
        vars_3l_jesTotalCorrUp['mbb_loose'              ] =  lambda ev : ev.mbb_loose_jesTotalCorrUp
        vars_3l_jesTotalCorrUp['met_LD'                 ] =  lambda ev : (ev.MET_pt_jesTotalCorrUp if ev.year != 2017 else ev.METFixEE2017_pt_jesTotalCorrUp) *0.6 + ev.mhtJet25_jesTotalCorrUp_Recl*0.4
        vars_3l_jesTotalCorrUp['jet3_pt'                ] =  lambda ev : ev.JetSel_Recl_pt_jesTotalCorrUp[2] if ev.nJet25_jesTotalCorrUp_Recl > 2 else 0
        vars_3l_jesTotalCorrUp['HadTop_pt'              ] =  lambda ev : ev.BDThttTT_eventReco_HadTop_pt_jesTotalCorrUp if ev.BDThttTT_eventReco_mvaValue_jesTotalCorrUp > 0 else 0
        vars_3l_jesTotalCorrUp['nJet'                   ] =  lambda ev : ev.nJet25_jesTotalCorrUp_Recl
        vars_3l_jesTotalCorrUp['res_HTT'                ] =  lambda ev : ev.BDThttTT_eventReco_mvaValue_jesTotalCorrUp if ev.BDThttTT_eventReco_mvaValue_jesTotalCorrUp > 0 else 0
        vars_3l_jesTotalCorrUp['jet3_phi'               ] =  lambda ev : ev.JetSel_Recl_phi[2] if ev.nJet25_Recl >= 3 else 0
        vars_3l_jesTotalCorrUp['nBJetLoose'             ] =  lambda ev : ev.nBJetLoose25_jesTotalCorrUp_Recl
        vars_3l_jesTotalCorrUp['nJetForward'            ] =  lambda ev : ev.nFwdJet_jesTotalCorrUp_Recl
        self.outVars.extend( ['DNN_3l_jesTotalCorrUp_' + x for x in cats_3l])


        vars_3l_jesTotalCorrDown = deepcopy(vars_3l)
        vars_3l_jesTotalCorrDown['avg_dr_jet'             ] =  lambda ev : ev.avg_dr_jet_jesTotalCorrDown
        vars_3l_jesTotalCorrDown['jet1_pt'                ] =  lambda ev : ev.JetSel_Recl_pt_jesTotalCorrDown[0] if ev.nJet25_jesTotalCorrDown_Recl > 0 else 0
        vars_3l_jesTotalCorrDown['jet2_pt'                ] =  lambda ev : ev.JetSel_Recl_pt_jesTotalCorrDown[1] if ev.nJet25_jesTotalCorrDown_Recl > 1 else 0
        vars_3l_jesTotalCorrDown['leadFwdJet_pt'          ] =  lambda ev : ev.FwdJet1_pt_jesTotalCorrDown_Recl if ev.nFwdJet_jesTotalCorrDown_Recl else 0
        vars_3l_jesTotalCorrDown['nBJetMedium'            ] =  lambda ev : ev.nBJetMedium25_jesTotalCorrDown_Recl
        vars_3l_jesTotalCorrDown['mbb_loose'              ] =  lambda ev : ev.mbb_loose_jesTotalCorrDown
        vars_3l_jesTotalCorrDown['met_LD'                 ] =  lambda ev : (ev.MET_pt_jesTotalCorrDown if ev.year != 2017 else ev.METFixEE2017_pt_jesTotalCorrDown) *0.6 + ev.mhtJet25_jesTotalCorrDown_Recl*0.4
        vars_3l_jesTotalCorrDown['jet3_pt'                ] =  lambda ev : ev.JetSel_Recl_pt_jesTotalCorrDown[2] if ev.nJet25_jesTotalCorrDown_Recl > 2 else 0
        vars_3l_jesTotalCorrDown['HadTop_pt'              ] =  lambda ev : ev.BDThttTT_eventReco_HadTop_pt_jesTotalCorrDown if ev.BDThttTT_eventReco_mvaValue_jesTotalCorrDown > 0 else 0 
        vars_3l_jesTotalCorrDown['nJet'                   ] =  lambda ev : ev.nJet25_jesTotalCorrDown_Recl
        vars_3l_jesTotalCorrDown['res_HTT'                ] =  lambda ev : ev.BDThttTT_eventReco_mvaValue_jesTotalCorrDown if ev.BDThttTT_eventReco_mvaValue_jesTotalCorrDown > 0 else 0 
        vars_3l_jesTotalCorrDown['jet3_phi'               ] =  lambda ev : ev.JetSel_Recl_phi[2] if ev.nJet25_Recl >= 3 else 0
        vars_3l_jesTotalCorrDown['nBJetLoose'             ] =  lambda ev : ev.nBJetLoose25_jesTotalCorrDown_Recl
        vars_3l_jesTotalCorrDown['nJetForward'            ] =  lambda ev : ev.nFwdJet_jesTotalCorrDown_Recl
        self.outVars.extend( ['DNN_3l_jesTotalCorrDown_' + x for x in cats_3l])



        vars_3l_jesTotalUnCorrUp = deepcopy(vars_3l)
        vars_3l_jesTotalUnCorrUp['avg_dr_jet'             ] =  lambda ev : ev.avg_dr_jet_jesTotalUnCorrUp
        vars_3l_jesTotalUnCorrUp['jet1_pt'                ] =  lambda ev : ev.JetSel_Recl_pt_jesTotalUnCorrUp[0] if ev.nJet25_jesTotalUnCorrUp_Recl > 0 else 0
        vars_3l_jesTotalUnCorrUp['jet2_pt'                ] =  lambda ev : ev.JetSel_Recl_pt_jesTotalUnCorrUp[1] if ev.nJet25_jesTotalUnCorrUp_Recl > 1 else 0
        vars_3l_jesTotalUnCorrUp['leadFwdJet_pt'          ] =  lambda ev : ev.FwdJet1_pt_jesTotalUnCorrUp_Recl if ev.nFwdJet_jesTotalUnCorrUp_Recl else 0
        vars_3l_jesTotalUnCorrUp['nBJetMedium'            ] =  lambda ev : ev.nBJetMedium25_jesTotalUnCorrUp_Recl
        vars_3l_jesTotalUnCorrUp['mbb_loose'              ] =  lambda ev : ev.mbb_loose_jesTotalUnCorrUp
        vars_3l_jesTotalUnCorrUp['met_LD'                 ] =  lambda ev : (ev.MET_pt_jesTotalUnCorrUp if ev.year != 2017 else ev.METFixEE2017_pt_jesTotalUnCorrUp) *0.6 + ev.mhtJet25_jesTotalUnCorrUp_Recl*0.4
        vars_3l_jesTotalUnCorrUp['jet3_pt'                ] =  lambda ev : ev.JetSel_Recl_pt_jesTotalUnCorrUp[2] if ev.nJet25_jesTotalUnCorrUp_Recl > 2 else 0
        vars_3l_jesTotalUnCorrUp['HadTop_pt'              ] =  lambda ev : ev.BDThttTT_eventReco_HadTop_pt_jesTotalUnCorrUp if ev.BDThttTT_eventReco_mvaValue_jesTotalUnCorrUp > 0 else 0
        vars_3l_jesTotalUnCorrUp['nJet'                   ] =  lambda ev : ev.nJet25_jesTotalUnCorrUp_Recl
        vars_3l_jesTotalUnCorrUp['res_HTT'                ] =  lambda ev : ev.BDThttTT_eventReco_mvaValue_jesTotalUnCorrUp if ev.BDThttTT_eventReco_mvaValue_jesTotalUnCorrUp > 0 else 0
        vars_3l_jesTotalUnCorrUp['jet3_phi'               ] =  lambda ev : ev.JetSel_Recl_phi[2] if ev.nJet25_Recl >= 3 else 0
        vars_3l_jesTotalUnCorrUp['nBJetLoose'             ] =  lambda ev : ev.nBJetLoose25_jesTotalUnCorrUp_Recl
        vars_3l_jesTotalUnCorrUp['nJetForward'            ] =  lambda ev : ev.nFwdJet_jesTotalUnCorrUp_Recl
        self.outVars.extend( ['DNN_3l_jesTotalUnCorrUp_' + x for x in cats_3l])


        vars_3l_jesTotalUnCorrDown = deepcopy(vars_3l)
        vars_3l_jesTotalUnCorrDown['avg_dr_jet'             ] =  lambda ev : ev.avg_dr_jet_jesTotalUnCorrDown
        vars_3l_jesTotalUnCorrDown['jet1_pt'                ] =  lambda ev : ev.JetSel_Recl_pt_jesTotalUnCorrDown[0] if ev.nJet25_jesTotalUnCorrDown_Recl > 0 else 0
        vars_3l_jesTotalUnCorrDown['jet2_pt'                ] =  lambda ev : ev.JetSel_Recl_pt_jesTotalUnCorrDown[1] if ev.nJet25_jesTotalUnCorrDown_Recl > 1 else 0
        vars_3l_jesTotalUnCorrDown['leadFwdJet_pt'          ] =  lambda ev : ev.FwdJet1_pt_jesTotalUnCorrDown_Recl if ev.nFwdJet_jesTotalUnCorrDown_Recl else 0
        vars_3l_jesTotalUnCorrDown['nBJetMedium'            ] =  lambda ev : ev.nBJetMedium25_jesTotalUnCorrDown_Recl
        vars_3l_jesTotalUnCorrDown['mbb_loose'              ] =  lambda ev : ev.mbb_loose_jesTotalUnCorrDown
        vars_3l_jesTotalUnCorrDown['met_LD'                 ] =  lambda ev : (ev.MET_pt_jesTotalUnCorrDown if ev.year != 2017 else ev.METFixEE2017_pt_jesTotalUnCorrDown) *0.6 + ev.mhtJet25_jesTotalUnCorrDown_Recl*0.4
        vars_3l_jesTotalUnCorrDown['jet3_pt'                ] =  lambda ev : ev.JetSel_Recl_pt_jesTotalUnCorrDown[2] if ev.nJet25_jesTotalUnCorrDown_Recl > 2 else 0
        vars_3l_jesTotalUnCorrDown['HadTop_pt'              ] =  lambda ev : ev.BDThttTT_eventReco_HadTop_pt_jesTotalUnCorrDown if ev.BDThttTT_eventReco_mvaValue_jesTotalUnCorrDown > 0 else 0 
        vars_3l_jesTotalUnCorrDown['nJet'                   ] =  lambda ev : ev.nJet25_jesTotalUnCorrDown_Recl
        vars_3l_jesTotalUnCorrDown['res_HTT'                ] =  lambda ev : ev.BDThttTT_eventReco_mvaValue_jesTotalUnCorrDown if ev.BDThttTT_eventReco_mvaValue_jesTotalUnCorrDown > 0 else 0 
        vars_3l_jesTotalUnCorrDown['jet3_phi'               ] =  lambda ev : ev.JetSel_Recl_phi[2] if ev.nJet25_Recl >= 3 else 0
        vars_3l_jesTotalUnCorrDown['nBJetLoose'             ] =  lambda ev : ev.nBJetLoose25_jesTotalUnCorrDown_Recl
        vars_3l_jesTotalUnCorrDown['nJetForward'            ] =  lambda ev : ev.nFwdJet_jesTotalUnCorrDown_Recl
        self.outVars.extend( ['DNN_3l_jesTotalUnCorrDown_' + x for x in cats_3l])



        vars_3l_jerUp = deepcopy(vars_3l)
        vars_3l_jerUp['avg_dr_jet'             ] =  lambda ev : ev.avg_dr_jet_jerUp
        vars_3l_jerUp['jet1_pt'                ] =  lambda ev : ev.JetSel_Recl_pt_jerUp[0] if ev.nJet25_jerUp_Recl > 0 else 0
        vars_3l_jerUp['jet2_pt'                ] =  lambda ev : ev.JetSel_Recl_pt_jerUp[1] if ev.nJet25_jerUp_Recl > 1 else 0
        vars_3l_jerUp['leadFwdJet_pt'          ] =  lambda ev : ev.FwdJet1_pt_jerUp_Recl if ev.nFwdJet_jerUp_Recl else 0
        vars_3l_jerUp['nBJetMedium'            ] =  lambda ev : ev.nBJetMedium25_jerUp_Recl
        vars_3l_jerUp['mbb_loose'              ] =  lambda ev : ev.mbb_loose_jerUp
        vars_3l_jerUp['met_LD'                 ] =  lambda ev : (ev.MET_pt_jerUp if ev.year != 2017 else ev.METFixEE2017_pt_jerUp) *0.6 + ev.mhtJet25_jerUp_Recl*0.4
        vars_3l_jerUp['jet3_pt'                ] =  lambda ev : ev.JetSel_Recl_pt_jerUp[2] if ev.nJet25_jerUp_Recl > 2 else 0
        vars_3l_jerUp['HadTop_pt'              ] =  lambda ev : ev.BDThttTT_eventReco_HadTop_ptjerUp if ev.BDThttTT_eventReco_mvaValuejerUp> 0 else 0 
        vars_3l_jerUp['nJet'                   ] =  lambda ev : ev.nJet25_jerUp_Recl
        vars_3l_jerUp['res_HTT'                ] =  lambda ev : ev.BDThttTT_eventReco_mvaValuejerUp if ev.BDThttTT_eventReco_mvaValuejerUp> 0 else 0 
        vars_3l_jerUp['jet3_phi'               ] =  lambda ev : ev.JetSel_Recl_phi[2] if ev.nJet25_Recl >= 3 else 0
        vars_3l_jerUp['nBJetLoose'             ] =  lambda ev : ev.nBJetLoose25_jerUp_Recl
        vars_3l_jerUp['nJetForward'            ] =  lambda ev : ev.nFwdJet_jerUp_Recl
        self.outVars.extend( ['DNN_3l_jerUp_' + x for x in cats_3l])


        vars_3l_jerDown = deepcopy(vars_3l)
        vars_3l_jerDown['avg_dr_jet'             ] =  lambda ev : ev.avg_dr_jet_jerDown
        vars_3l_jerDown['jet1_pt'                ] =  lambda ev : ev.JetSel_Recl_pt_jerDown[0] if ev.nJet25_jerDown_Recl > 0 else 0
        vars_3l_jerDown['jet2_pt'                ] =  lambda ev : ev.JetSel_Recl_pt_jerDown[1] if ev.nJet25_jerDown_Recl > 1 else 0
        vars_3l_jerDown['leadFwdJet_pt'          ] =  lambda ev : ev.FwdJet1_pt_jerDown_Recl if ev.nFwdJet_jerDown_Recl else 0
        vars_3l_jerDown['nBJetMedium'            ] =  lambda ev : ev.nBJetMedium25_jerDown_Recl
        vars_3l_jerDown['mbb_loose'              ] =  lambda ev : ev.mbb_loose_jerDown
        vars_3l_jerDown['met_LD'                 ] =  lambda ev : (ev.MET_pt_jerDown if ev.year != 2017 else ev.METFixEE2017_pt_jerDown) *0.6 + ev.mhtJet25_jerDown_Recl*0.4
        vars_3l_jerDown['jet3_pt'                ] =  lambda ev : ev.JetSel_Recl_pt_jerDown[2] if ev.nJet25_jerDown_Recl > 2 else 0
        vars_3l_jerDown['HadTop_pt'              ] =  lambda ev : ev.BDThttTT_eventReco_HadTop_ptjerDown if ev.BDThttTT_eventReco_mvaValuejerDown > 0 else 0 
        vars_3l_jerDown['nJet'                   ] =  lambda ev : ev.nJet25_jerDown_Recl
        vars_3l_jerDown['res_HTT'                ] =  lambda ev : ev.BDThttTT_eventReco_mvaValuejerDown if ev.BDThttTT_eventReco_mvaValuejerDown > 0 else 0 
        vars_3l_jerDown['jet3_phi'               ] =  lambda ev : ev.JetSel_Recl_phi[2] if ev.nJet25_Recl >= 3 else 0
        vars_3l_jerDown['nBJetLoose'             ] =  lambda ev : ev.nBJetLoose25_jerDown_Recl
        vars_3l_jerDown['nJetForward'            ] =  lambda ev : ev.nFwdJet_jerDown_Recl
        self.outVars.extend( ['DNN_3l_jerDown_' + x for x in cats_3l])


        vars_3l_unclEnUp = deepcopy(vars_3l)
        vars_3l_unclEnUp['met_LD'                 ] =  lambda ev : (ev.MET_pt_unclustEnUp if ev.year != 2017 else ev.METFixEE2017_pt_unclustEnUp) *0.6 + ev.mhtJet25_Recl*0.4

        vars_3l_unclEnDown = deepcopy(vars_3l)
        vars_3l_unclEnDown['met_LD'                 ] =  lambda ev : (ev.MET_pt_unclustEnDown if ev.year != 2017 else ev.METFixEE2017_pt_unclustEnDown) *0.6 + ev.mhtJet25_Recl*0.4



        worker_3l = TFTool('DNN_3l', os.environ['CMSSW_BASE'] + '/src/CMGTools/TTHAnalysis/data/kinMVA/tth/test_sig_2_rest_2_th_2_withWZ_2.pb',
                                   vars_3l, cats_3l, varorder)

        worker_3l_jesTotalCorrUp = TFTool('DNN_3l_jesTotalCorrUp', os.environ['CMSSW_BASE'] + '/src/CMGTools/TTHAnalysis/data/kinMVA/tth/test_sig_2_rest_2_th_2_withWZ_2.pb',
                           vars_3l_jesTotalCorrUp, cats_3l, varorder)
        worker_3l_jesTotalCorrDown = TFTool('DNN_3l_jesTotalCorrDown', os.environ['CMSSW_BASE'] + '/src/CMGTools/TTHAnalysis/data/kinMVA/tth/test_sig_2_rest_2_th_2_withWZ_2.pb',
                                  vars_3l_jesTotalCorrDown, cats_3l, varorder)

        worker_3l_jesTotalUnCorrUp = TFTool('DNN_3l_jesTotalUnCorrUp', os.environ['CMSSW_BASE'] + '/src/CMGTools/TTHAnalysis/data/kinMVA/tth/test_sig_2_rest_2_th_2_withWZ_2.pb',
                           vars_3l_jesTotalUnCorrUp, cats_3l, varorder)
        worker_3l_jesTotalUnCorrDown = TFTool('DNN_3l_jesTotalUnCorrDown', os.environ['CMSSW_BASE'] + '/src/CMGTools/TTHAnalysis/data/kinMVA/tth/test_sig_2_rest_2_th_2_withWZ_2.pb',
                                  vars_3l_jesTotalUnCorrDown, cats_3l, varorder)

        worker_3l_jerUp = TFTool('DNN_3l_jerUp', os.environ['CMSSW_BASE'] + '/src/CMGTools/TTHAnalysis/data/kinMVA/tth/test_sig_2_rest_2_th_2_withWZ_2.pb',
                           vars_3l_jerUp, cats_3l, varorder)
        worker_3l_jerDown = TFTool('DNN_3l_jerDown', os.environ['CMSSW_BASE'] + '/src/CMGTools/TTHAnalysis/data/kinMVA/tth/test_sig_2_rest_2_th_2_withWZ_2.pb',
                                  vars_3l_jerDown, cats_3l, varorder)

        worker_3l_unclEnUp = TFTool('DNN_3l_unclEnUp', os.environ['CMSSW_BASE'] + '/src/CMGTools/TTHAnalysis/data/kinMVA/tth/test_sig_2_rest_2_th_2_withWZ_2.pb',
                           vars_3l_unclEnUp, cats_3l, varorder)
        worker_3l_unclEnDown = TFTool('DNN_3l_unclEnDown', os.environ['CMSSW_BASE'] + '/src/CMGTools/TTHAnalysis/data/kinMVA/tth/test_sig_2_rest_2_th_2_withWZ_2.pb',
                                  vars_3l_unclEnDown, cats_3l, varorder)

    
        self._MVAs = [worker_3l, 
                      worker_3l_jesTotalCorrUp, worker_3l_jesTotalCorrDown,
                      worker_3l_jesTotalUnCorrUp, worker_3l_jesTotalUnCorrDown,
                      worker_3l_jerUp, worker_3l_jerDown]


    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        print self.outVars
        declareOutput(self, wrappedOutputTree, self.outVars)
        
    def analyze(self,event):
        myvars = [event.iLepFO_Recl[0],event.iLepFO_Recl[1],event.iLepFO_Recl[2]]
        ret = []
        for worker in self._MVAs:
            name = worker.name
            if not hasattr(event,"nJet25_jerUp_Recl") and ('_jes' in name or  '_jer' in name or '_uncl' in name): continue # using jer bc components wont change
            #if not ('_jes' in name or  '_jer' in name or '_uncl' in name) and event.event == 259935: worker.debug=True
            ret.extend( [(x,y) for x,y in worker(event).iteritems()])
            #if not ('_jes' in name or  '_jer' in name or '_uncl' in name) and event.event == 259935: worker.debug=False

            
        writeOutput(self, dict(ret))
        return True
