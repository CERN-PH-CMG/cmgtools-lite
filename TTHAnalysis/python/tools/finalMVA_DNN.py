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

        vars_2lss = { "jet3_pt"          : lambda ev : ev.JetSel_Recl_pt[2] if ev.nJet25_Recl > 2 else -9,
                      "jet3_eta"         : lambda ev : abs(ev.JetSel_Recl_eta[2]) if ev.nJet25_Recl > 2 else 9,
                      "lep1_eta"         : lambda ev : ev.LepGood_eta[int(ev.iLepFO_Recl[0])] if ev.nLepFO_Recl >= 1 else 0,
                      "jet2_pt"          : lambda ev : ev.JetSel_Recl_pt[1] if ev.nJet25_Recl > 1 else -9,
                      "jet1_pt"          : lambda ev : ev.JetSel_Recl_pt[0] if ev.nJet25_Recl > 0 else -9,
                      "jetFwd1_eta"      : lambda ev : abs(ev.FwdJet1_eta_Recl) if ev.nFwdJet_Recl else 9,
                      "mT_lep1"          : lambda ev : ev.MT_met_lep1,
                      "mT_lep2"          : lambda ev : ev.MT_met_lep2,
                      "jet4_phi"         : lambda ev : ev.JetSel_Recl_phi[3] if ev.nJet25_Recl > 3 else -9,
                      "lep2_conePt"      : lambda ev : ev.LepGood_conePt[int(ev.iLepFO_Recl[1])],
                      "hadTop_BDT"       : lambda ev : ev.BDThttTT_eventReco_mvaValue if ev.BDThttTT_eventReco_mvaValue > 0 else -9,
                      "jet1_phi"         : lambda ev : ev.JetSel_Recl_phi[0] if ev.nJet25_Recl > 0 else -9,
                      "jet2_eta"         : lambda ev : abs(ev.JetSel_Recl_eta[1]) if ev.nJet25_Recl > 1 else 9,
                      "n_presel_jetFwd"  : lambda ev : ev.nFwdJet_Recl, 
                      "n_presel_jet"     : lambda ev : ev.nJet25_Recl,
                      "lep1_charge"      : lambda ev : ev.LepGood_charge[int(ev.iLepFO_Recl[0])],
                      "avg_dr_jet"       : lambda ev : ev.avg_dr_jet,
                      "lep1_phi"         : lambda ev : (ev.LepGood_phi[int(ev.iLepFO_Recl[0])]) if ev.nLepFO_Recl >= 1 else -9,
                      "Hj_tagger_hadTop" : lambda ev : ev.BDThttTT_eventReco_Hj_score if ev.BDThttTT_eventReco_Hj_score > 0 else -9 ,
                      "nBJetLoose"       : lambda ev : ev.nBJetLoose25_Recl,
                      "jet4_pt"          : lambda ev : ev.JetSel_Recl_pt[3] if ev.nJet25_Recl > 3 else -9,
                      "mindr_lep1_jet"   : lambda ev : ev.mindr_lep1_jet,
                      "lep1_conePt"      : lambda ev : ev.LepGood_conePt[int(ev.iLepFO_Recl[0])], 
                      "jetFwd1_pt"       : lambda ev : ev.FwdJet1_pt_Recl if ev.nFwdJet_Recl else -9,
                      "lep2_phi"         : lambda ev : (ev.LepGood_phi[int(ev.iLepFO_Recl[1])]) if ev.nLepFO_Recl >= 2 else -9,
                      "jet2_phi"         : lambda ev : ev.JetSel_Recl_phi[1] if ev.nJet25_Recl >= 2 else -9,
                      "lep2_eta"         : lambda ev : ev.LepGood_eta[int(ev.iLepFO_Recl[1])] if ev.nLepFO_Recl >= 2 else -9,
                      "mbb"              : lambda ev : ev.mbb_medium if ev.mbb_medium!=0 else -9,
                      "mindr_lep2_jet"   : lambda ev : ev.mindr_lep2_jet,                   
                      "jet4_eta"         : lambda ev : abs(ev.JetSel_Recl_eta[3]) if ev.nJet25_Recl > 3 else 9,
                      "nBJetMedium"      : lambda ev : ev.nBJetMedium25_Recl,
                      "Dilep_pdgId"      : lambda ev : (28 - abs(ev.LepGood_pdgId[int(ev.iLepFO_Recl[0])]) - abs(ev.LepGood_pdgId[int(ev.iLepFO_Recl[1])]))/2,
                      "metLD"            : lambda ev : (ev.MET_pt if ev.year != 2017 else ev.METFixEE2017_pt) *0.6 + ev.mhtJet25_Recl*0.4,
                      "jet3_phi"         : lambda ev : ev.JetSel_Recl_phi[2] if ev.nJet25_Recl >= 3 else -9,
                      "maxeta"           : lambda ev : max( [abs(ev.LepGood_eta[int(ev.iLepFO_Recl[0])]), abs(ev.LepGood_eta[int(ev.iLepFO_Recl[1])])]),
                      "jet1_eta"         : lambda ev : abs(ev.JetSel_Recl_eta[0]) if ev.nJet25_Recl > 0 else 9,
                  }
        cats_2lss = ['predictions_ttH','predictions_Rest','predictions_ttW','predictions_tHQ']
        self.outVars.extend( ['DNN_2lss_' + x for x in cats_2lss])

        vars_2lss_jesTotalCorrUp = deepcopy(vars_2lss)
        vars_2lss_jesTotalCorrUp["jet3_pt"          ] =  lambda ev : ev.JetSel_Recl_pt_jesTotalCorrUp[2] if ev.nJet25_jesTotalCorrUp_Recl > 2 else -9
        vars_2lss_jesTotalCorrUp["jet2_pt"          ] =  lambda ev : ev.JetSel_Recl_pt_jesTotalCorrUp[1] if ev.nJet25_jesTotalCorrUp_Recl > 1 else -9
        vars_2lss_jesTotalCorrUp["jet1_pt"          ] =  lambda ev : ev.JetSel_Recl_pt_jesTotalCorrUp[0] if ev.nJet25_jesTotalCorrUp_Recl > 0 else -9
        vars_2lss_jesTotalCorrUp["mT_lep1"          ] =  lambda ev : ev.MT_met_lep1_jesTotalCorrUp
        vars_2lss_jesTotalCorrUp["mT_lep2"          ] =  lambda ev : ev.MT_met_lep2_jesTotalCorrUp
        vars_2lss_jesTotalCorrUp["hadTop_BDT"       ] =  lambda ev : ev.BDThttTT_eventReco_mvaValue_jesTotalCorrUp  if ev.BDThttTT_eventReco_mvaValue_jesTotalCorrUp > 0 else -9
        vars_2lss_jesTotalCorrUp["n_presel_jetFwd"  ] =  lambda ev : ev.nFwdJet_jesTotalCorrUp_Recl
        vars_2lss_jesTotalCorrUp["n_presel_jet"     ] =  lambda ev : ev.nJet25_jesTotalCorrUp_Recl
        vars_2lss_jesTotalCorrUp["Hj_tagger_hadTop" ] =  lambda ev : ev.BDThttTT_eventReco_Hj_score_jesTotalCorrUp if ev.BDThttTT_eventReco_Hj_score_jesTotalCorrUp > 0 else -9
        vars_2lss_jesTotalCorrUp["nBJetLoose"       ] =  lambda ev : ev.nBJetLoose25_jesTotalCorrUp_Recl
        vars_2lss_jesTotalCorrUp["jet4_pt"          ] =  lambda ev : ev.JetSel_Recl_pt_jesTotalCorrUp[3] if ev.nJet25_jesTotalCorrUp_Recl > 3 else -9
        vars_2lss_jesTotalCorrUp["jetFwd1_pt"       ] =  lambda ev : ev.FwdJet1_pt_jesTotalCorrUp_Recl if ev.nFwdJet_jesTotalCorrUp_Recl else -9
        vars_2lss_jesTotalCorrUp["mbb"              ] =  lambda ev : ev.mbb_medium_jesTotalCorrUp if ev.mbb_medium_jesTotalCorrUp !=0 else -9
        vars_2lss_jesTotalCorrUp["nBJetMedium"      ] =  lambda ev : ev.nBJetMedium25_jesTotalCorrUp_Recl
        vars_2lss_jesTotalCorrUp["metLD"            ] =  lambda ev : (ev.MET_pt_jesTotalCorrUp if ev.year != 2017 else ev.METFixEE2017_pt_jesTotalCorrUp) *0.6 + ev.mhtJet25_jesTotalCorrUp_Recl*0.4
        self.outVars.extend( ['DNN_2lss_jesTotalCorrUp_' + x for x in cats_2lss])

        vars_2lss_jesTotalCorrDown = deepcopy(vars_2lss)
        vars_2lss_jesTotalCorrDown["jet3_pt"          ] =  lambda ev : ev.JetSel_Recl_pt_jesTotalCorrDown[2] if ev.nJet25_jesTotalCorrDown_Recl > 2 else -9 
        vars_2lss_jesTotalCorrDown["jet2_pt"          ] =  lambda ev : ev.JetSel_Recl_pt_jesTotalCorrDown[1] if ev.nJet25_jesTotalCorrDown_Recl > 1 else -9
        vars_2lss_jesTotalCorrDown["jet1_pt"          ] =  lambda ev : ev.JetSel_Recl_pt_jesTotalCorrDown[0] if ev.nJet25_jesTotalCorrDown_Recl > 0 else -9
        vars_2lss_jesTotalCorrDown["mT_lep1"          ] =  lambda ev : ev.MT_met_lep1_jesTotalCorrDown
        vars_2lss_jesTotalCorrDown["mT_lep2"          ] =  lambda ev : ev.MT_met_lep2_jesTotalCorrDown
        vars_2lss_jesTotalCorrDown["hadTop_BDT"       ] =  lambda ev : ev.BDThttTT_eventReco_mvaValue_jesTotalCorrDown if ev.BDThttTT_eventReco_mvaValue_jesTotalCorrDown > 0 else -9
        vars_2lss_jesTotalCorrDown["n_presel_jetFwd"  ] =  lambda ev : ev.nFwdJet_jesTotalCorrDown_Recl
        vars_2lss_jesTotalCorrDown["n_presel_jet"     ] =  lambda ev : ev.nJet25_jesTotalCorrDown_Recl
        vars_2lss_jesTotalCorrDown["Hj_tagger_hadTop" ] =  lambda ev : ev.BDThttTT_eventReco_Hj_score_jesTotalCorrDown if ev.BDThttTT_eventReco_Hj_score_jesTotalCorrDown > 0 else -9
        vars_2lss_jesTotalCorrDown["nBJetLoose"       ] =  lambda ev : ev.nBJetLoose25_jesTotalCorrDown_Recl
        vars_2lss_jesTotalCorrDown["jet4_pt"          ] =  lambda ev : ev.JetSel_Recl_pt_jesTotalCorrDown[3] if ev.nJet25_jesTotalCorrDown_Recl > 3 else -9
        vars_2lss_jesTotalCorrDown["jetFwd1_pt"       ] =  lambda ev : ev.FwdJet1_pt_jesTotalCorrDown_Recl if ev.nFwdJet_jesTotalCorrDown_Recl else -9
        vars_2lss_jesTotalCorrDown["mbb"              ] =  lambda ev : ev.mbb_medium_jesTotalCorrDown if ev.mbb_medium_jesTotalCorrDown != 0 else -9
        vars_2lss_jesTotalCorrDown["nBJetMedium"      ] =  lambda ev : ev.nBJetMedium25_jesTotalCorrDown_Recl
        vars_2lss_jesTotalCorrDown["metLD"            ] =  lambda ev : (ev.MET_pt_jesTotalCorrDown if ev.year != 2017 else ev.METFixEE2017_pt_jesTotalCorrDown) *0.6 + ev.mhtJet25_jesTotalCorrDown_Recl*0.4
        self.outVars.extend( ['DNN_2lss_jesTotalCorrDown_' + x for x in cats_2lss])


        vars_2lss_jesTotalUnCorrUp = deepcopy(vars_2lss)
        vars_2lss_jesTotalUnCorrUp["jet3_pt"          ] =  lambda ev : ev.JetSel_Recl_pt_jesTotalUnCorrUp[2] if ev.nJet25_jesTotalUnCorrUp_Recl > 2 else -9
        vars_2lss_jesTotalUnCorrUp["jet2_pt"          ] =  lambda ev : ev.JetSel_Recl_pt_jesTotalUnCorrUp[1] if ev.nJet25_jesTotalUnCorrUp_Recl > 1 else -9
        vars_2lss_jesTotalUnCorrUp["jet1_pt"          ] =  lambda ev : ev.JetSel_Recl_pt_jesTotalUnCorrUp[0] if ev.nJet25_jesTotalUnCorrUp_Recl > 0 else -9
        vars_2lss_jesTotalUnCorrUp["mT_lep1"          ] =  lambda ev : ev.MT_met_lep1_jesTotalUnCorrUp
        vars_2lss_jesTotalUnCorrUp["mT_lep2"          ] =  lambda ev : ev.MT_met_lep2_jesTotalUnCorrUp
        vars_2lss_jesTotalUnCorrUp["hadTop_BDT"       ] =  lambda ev : ev.BDThttTT_eventReco_mvaValue_jesTotalUnCorrUp if ev.BDThttTT_eventReco_mvaValue_jesTotalUnCorrUp > 0 else -9
        vars_2lss_jesTotalUnCorrUp["n_presel_jetFwd"  ] =  lambda ev : ev.nFwdJet_jesTotalUnCorrUp_Recl
        vars_2lss_jesTotalUnCorrUp["n_presel_jet"     ] =  lambda ev : ev.nJet25_jesTotalUnCorrUp_Recl
        vars_2lss_jesTotalUnCorrUp["Hj_tagger_hadTop" ] =  lambda ev : ev.BDThttTT_eventReco_Hj_score_jesTotalUnCorrUp if ev.BDThttTT_eventReco_Hj_score_jesTotalUnCorrUp > 0 else -9
        vars_2lss_jesTotalUnCorrUp["nBJetLoose"       ] =  lambda ev : ev.nBJetLoose25_jesTotalUnCorrUp_Recl
        vars_2lss_jesTotalUnCorrUp["jet4_pt"          ] =  lambda ev : ev.JetSel_Recl_pt_jesTotalUnCorrUp[3] if ev.nJet25_jesTotalUnCorrUp_Recl > 3 else -9
        vars_2lss_jesTotalUnCorrUp["jetFwd1_pt"       ] =  lambda ev : ev.FwdJet1_pt_jesTotalUnCorrUp_Recl if ev.nFwdJet_jesTotalUnCorrUp_Recl else -9
        vars_2lss_jesTotalUnCorrUp["mbb"              ] =  lambda ev : ev.mbb_medium_jesTotalUnCorrUp if ev.mbb_medium_jesTotalUnCorrUp != 0 else -9
        vars_2lss_jesTotalUnCorrUp["nBJetMedium"      ] =  lambda ev : ev.nBJetMedium25_jesTotalUnCorrUp_Recl
        vars_2lss_jesTotalUnCorrUp["metLD"            ] =  lambda ev : (ev.MET_pt_jesTotalUnCorrUp if ev.year != 2017 else ev.METFixEE2017_pt_jesTotalUnCorrUp) *0.6 + ev.mhtJet25_jesTotalUnCorrUp_Recl*0.4
        self.outVars.extend( ['DNN_2lss_jesTotalUnCorrUp_' + x for x in cats_2lss])

        vars_2lss_jesTotalUnCorrDown = deepcopy(vars_2lss)
        vars_2lss_jesTotalUnCorrDown["jet3_pt"          ] =  lambda ev : ev.JetSel_Recl_pt_jesTotalUnCorrDown[2] if ev.nJet25_jesTotalUnCorrDown_Recl > 2 else -9
        vars_2lss_jesTotalUnCorrDown["jet2_pt"          ] =  lambda ev : ev.JetSel_Recl_pt_jesTotalUnCorrDown[1] if ev.nJet25_jesTotalUnCorrDown_Recl > 1 else -9
        vars_2lss_jesTotalUnCorrDown["jet1_pt"          ] =  lambda ev : ev.JetSel_Recl_pt_jesTotalUnCorrDown[0] if ev.nJet25_jesTotalUnCorrDown_Recl > 0 else -9
        vars_2lss_jesTotalUnCorrDown["mT_lep1"          ] =  lambda ev : ev.MT_met_lep1_jesTotalUnCorrDown
        vars_2lss_jesTotalUnCorrDown["mT_lep2"          ] =  lambda ev : ev.MT_met_lep2_jesTotalUnCorrDown
        vars_2lss_jesTotalUnCorrDown["hadTop_BDT"       ] =  lambda ev : ev.BDThttTT_eventReco_mvaValue_jesTotalUnCorrDown if ev.BDThttTT_eventReco_mvaValue_jesTotalUnCorrDown > 0 else -9
        vars_2lss_jesTotalUnCorrDown["n_presel_jetFwd"  ] =  lambda ev : ev.nFwdJet_jesTotalUnCorrDown_Recl
        vars_2lss_jesTotalUnCorrDown["n_presel_jet"     ] =  lambda ev : ev.nJet25_jesTotalUnCorrDown_Recl
        vars_2lss_jesTotalUnCorrDown["Hj_tagger_hadTop" ] =  lambda ev : ev.BDThttTT_eventReco_Hj_score_jesTotalUnCorrDown if ev.BDThttTT_eventReco_Hj_score_jesTotalUnCorrDown > 0 else -9
        vars_2lss_jesTotalUnCorrDown["nBJetLoose"       ] =  lambda ev : ev.nBJetLoose25_jesTotalUnCorrDown_Recl
        vars_2lss_jesTotalUnCorrDown["jet4_pt"          ] =  lambda ev : ev.JetSel_Recl_pt_jesTotalUnCorrDown[3] if ev.nJet25_jesTotalUnCorrDown_Recl > 3 else -9
        vars_2lss_jesTotalUnCorrDown["jetFwd1_pt"       ] =  lambda ev : ev.FwdJet1_pt_jesTotalUnCorrDown_Recl if ev.nFwdJet_jesTotalUnCorrDown_Recl else -9
        vars_2lss_jesTotalUnCorrDown["mbb"              ] =  lambda ev : ev.mbb_medium_jesTotalUnCorrDown if ev.mbb_medium_jesTotalUnCorrDown != 0 else -9
        vars_2lss_jesTotalUnCorrDown["nBJetMedium"      ] =  lambda ev : ev.nBJetMedium25_jesTotalUnCorrDown_Recl
        vars_2lss_jesTotalUnCorrDown["metLD"            ] =  lambda ev : (ev.MET_pt_jesTotalUnCorrDown if ev.year != 2017 else ev.METFixEE2017_pt_jesTotalUnCorrDown) *0.6 + ev.mhtJet25_jesTotalUnCorrDown_Recl*0.4
        self.outVars.extend( ['DNN_2lss_jesTotalUnCorrDown_' + x for x in cats_2lss])



        vars_2lss_jerUp = deepcopy(vars_2lss)
        vars_2lss_jerUp["jet3_pt"          ] =  lambda ev : ev.JetSel_Recl_pt_jerUp[2] if ev.nJet25_jerUp_Recl > 2 else -9
        vars_2lss_jerUp["jet2_pt"          ] =  lambda ev : ev.JetSel_Recl_pt_jerUp[1] if ev.nJet25_jerUp_Recl > 1 else -9
        vars_2lss_jerUp["jet1_pt"          ] =  lambda ev : ev.JetSel_Recl_pt_jerUp[0] if ev.nJet25_jerUp_Recl > 0 else -9
        vars_2lss_jerUp["mT_lep1"          ] =  lambda ev : ev.MT_met_lep1_jerUp
        vars_2lss_jerUp["mT_lep2"          ] =  lambda ev : ev.MT_met_lep2_jerUp
        vars_2lss_jerUp["hadTop_BDT"       ] =  lambda ev : ev.BDThttTT_eventReco_mvaValuejerUp if ev.BDThttTT_eventReco_mvaValuejerUp > 0 else -9
        vars_2lss_jerUp["n_presel_jetFwd"  ] =  lambda ev : ev.nFwdJet_jerUp_Recl
        vars_2lss_jerUp["n_presel_jet"     ] =  lambda ev : ev.nJet25_jerUp_Recl
        vars_2lss_jerUp["Hj_tagger_hadTop" ] =  lambda ev : ev.BDThttTT_eventReco_Hj_scorejerUp if ev.BDThttTT_eventReco_Hj_scorejerUp > 0 else -9
        vars_2lss_jerUp["nBJetLoose"       ] =  lambda ev : ev.nBJetLoose25_jerUp_Recl
        vars_2lss_jerUp["jet4_pt"          ] =  lambda ev : ev.JetSel_Recl_pt_jerUp[3] if ev.nJet25_jerUp_Recl > 3 else -9
        vars_2lss_jerUp["jetFwd1_pt"       ] =  lambda ev : ev.FwdJet1_pt_jerUp_Recl if ev.nFwdJet_jerUp_Recl else -9
        vars_2lss_jerUp["mbb"              ] =  lambda ev : ev.mbb_medium_jerUp if ev.mbb_medium_jerUp != 0 else -9
        vars_2lss_jerUp["nBJetMedium"      ] =  lambda ev : ev.nBJetMedium25_jerUp_Recl
        vars_2lss_jerUp["metLD"            ] =  lambda ev : (ev.MET_pt_jerUp if ev.year != 2017 else ev.METFixEE2017_pt_jerUp) *0.6 + ev.mhtJet25_jerUp_Recl*0.4
        self.outVars.extend( ['DNN_2lss_jerUp_' + x for x in cats_2lss])

        vars_2lss_jerDown = deepcopy(vars_2lss)
        vars_2lss_jerDown["jet3_pt"          ] =  lambda ev : ev.JetSel_Recl_pt_jerDown[2] if ev.nJet25_jerDown_Recl > 2 else -9
        vars_2lss_jerDown["jet2_pt"          ] =  lambda ev : ev.JetSel_Recl_pt_jerDown[1] if ev.nJet25_jerDown_Recl > 1 else -9
        vars_2lss_jerDown["jet1_pt"          ] =  lambda ev : ev.JetSel_Recl_pt_jerDown[0] if ev.nJet25_jerDown_Recl > 0 else -9
        vars_2lss_jerDown["mT_lep1"          ] =  lambda ev : ev.MT_met_lep1_jerDown
        vars_2lss_jerDown["mT_lep2"          ] =  lambda ev : ev.MT_met_lep2_jerDown
        vars_2lss_jerDown["hadTop_BDT"       ] =  lambda ev : ev.BDThttTT_eventReco_mvaValuejerDown if ev.BDThttTT_eventReco_mvaValuejerDown > 0 else -9
        vars_2lss_jerDown["n_presel_jetFwd"  ] =  lambda ev : ev.nFwdJet_jerDown_Recl
        vars_2lss_jerDown["n_presel_jet"     ] =  lambda ev : ev.nJet25_jerDown_Recl
        vars_2lss_jerDown["Hj_tagger_hadTop" ] =  lambda ev : ev.BDThttTT_eventReco_Hj_scorejerDown if ev.BDThttTT_eventReco_Hj_scorejerDown > 0 else -9
        vars_2lss_jerDown["nBJetLoose"       ] =  lambda ev : ev.nBJetLoose25_jerDown_Recl
        vars_2lss_jerDown["jet4_pt"          ] =  lambda ev : ev.JetSel_Recl_pt_jerDown[3] if ev.nJet25_jerDown_Recl > 3 else -9
        vars_2lss_jerDown["jetFwd1_pt"       ] =  lambda ev : ev.FwdJet1_pt_jerDown_Recl if ev.nFwdJet_jerDown_Recl else -9
        vars_2lss_jerDown["mbb"              ] =  lambda ev : ev.mbb_medium_jerDown if ev.mbb_medium_jerDown != 0 else -9
        vars_2lss_jerDown["nBJetMedium"      ] =  lambda ev : ev.nBJetMedium25_jerDown_Recl
        vars_2lss_jerDown["metLD"            ] =  lambda ev : (ev.MET_pt_jerDown if ev.year != 2017 else ev.METFixEE2017_pt_jerDown) *0.6 + ev.mhtJet25_jerDown_Recl*0.4
        self.outVars.extend( ['DNN_2lss_jerDown_' + x for x in cats_2lss])


        vars_2lss_unclUp = deepcopy(vars_2lss)
        vars_2lss_unclUp["metLD"            ] =  lambda ev : (ev.MET_pt_unclustEnUp if ev.year != 2017 else ev.METFixEE2017_pt_unclustEnUp) *0.6 + ev.mhtJet25_Recl*0.4
        vars_2lss_unclUp["mT_lep1"          ] =  lambda ev : ev.MT_met_lep1_unclustEnUp
        vars_2lss_unclUp["mT_lep2"          ] =  lambda ev : ev.MT_met_lep2_unclustEnUp
        self.outVars.extend( ['DNN_2lss_unclUp_' + x for x in cats_2lss])

        vars_2lss_unclDown = deepcopy(vars_2lss)
        vars_2lss_unclDown["metLD"            ] =  lambda ev : (ev.MET_pt_unclustEnDown if ev.year != 2017 else ev.METFixEE2017_pt_unclustEnDown) *0.6 + ev.mhtJet25_Recl*0.4
        vars_2lss_unclDown["mT_lep1"          ] =  lambda ev : ev.MT_met_lep1_unclustEnDown
        vars_2lss_unclDown["mT_lep2"          ] =  lambda ev : ev.MT_met_lep2_unclustEnDown
        self.outVars.extend( ['DNN_2lss_unclDown_' + x for x in cats_2lss])

        varorder = ["jet3_pt","jet3_eta","lep1_eta","jet2_pt","jet1_pt","jetFwd1_eta","mT_lep1","mT_lep2","jet4_phi","lep2_conePt","hadTop_BDT","jet1_phi","jet2_eta","n_presel_jetFwd","n_presel_jet","lep1_charge","avg_dr_jet","lep1_phi","Hj_tagger_hadTop","nBJetLoose","jet4_pt","mindr_lep1_jet","lep1_conePt","jetFwd1_pt","lep2_phi","jet2_phi","lep2_eta","mbb","mindr_lep2_jet","jet4_eta","nBJetMedium","Dilep_pdgId","metLD","jet3_phi","maxeta","jet1_eta"]

        worker_2lss = TFTool('DNN_2lss', os.environ['CMSSW_BASE'] + '/src/CMGTools/TTHAnalysis/data/kinMVA/tth/NN_2lss_0tau_2017.pb',
                             vars_2lss, cats_2lss, varorder)
        worker_2lss_jesTotalCorrUp = TFTool('DNN_2lss_jesTotalCorrUp', os.environ['CMSSW_BASE'] + '/src/CMGTools/TTHAnalysis/data/kinMVA/tth/NN_2lss_0tau_2017.pb',
                                            vars_2lss_jesTotalCorrUp, cats_2lss, varorder)
        worker_2lss_jesTotalUnCorrUp = TFTool('DNN_2lss_jesTotalUnCorrUp', os.environ['CMSSW_BASE'] + '/src/CMGTools/TTHAnalysis/data/kinMVA/tth/NN_2lss_0tau_2017.pb',
                                              vars_2lss_jesTotalUnCorrUp, cats_2lss, varorder)
        worker_2lss_jesTotalCorrDown = TFTool('DNN_2lss_jesTotalCorrDown', os.environ['CMSSW_BASE'] + '/src/CMGTools/TTHAnalysis/data/kinMVA/tth/NN_2lss_0tau_2017.pb',
                                              vars_2lss_jesTotalCorrDown, cats_2lss, varorder)
        worker_2lss_jesTotalUnCorrDown = TFTool('DNN_2lss_jesTotalUnCorrDown', os.environ['CMSSW_BASE'] + '/src/CMGTools/TTHAnalysis/data/kinMVA/tth/NN_2lss_0tau_2017.pb',
                                                vars_2lss_jesTotalUnCorrDown, cats_2lss, varorder)
        worker_2lss_jerUp        = TFTool('DNN_2lss_jerUp', os.environ['CMSSW_BASE'] + '/src/CMGTools/TTHAnalysis/data/kinMVA/tth/NN_2lss_0tau_2017.pb',
                                          vars_2lss_jerUp, cats_2lss, varorder)
        worker_2lss_jerDown      = TFTool('DNN_2lss_jerDown', os.environ['CMSSW_BASE'] + '/src/CMGTools/TTHAnalysis/data/kinMVA/tth/NN_2lss_0tau_2017.pb',
                                          vars_2lss_jerDown, cats_2lss, varorder)

        worker_2lss_unclUp        = TFTool('DNN_2lss_unclUp', os.environ['CMSSW_BASE'] + '/src/CMGTools/TTHAnalysis/data/kinMVA/tth/NN_2lss_0tau_2017.pb',
                                           vars_2lss_unclUp, cats_2lss, varorder)
        worker_2lss_unclDown      = TFTool('DNN_2lss_unclDown', os.environ['CMSSW_BASE'] + '/src/CMGTools/TTHAnalysis/data/kinMVA/tth/NN_2lss_0tau_2017.pb',
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
            if not hasattr(event,"nJet25_jesTotalCorrDown_Recl") and ('_jes' in name or  '_jer' in name or '_uncl' in name): continue
            ret.extend( [(x,y) for x,y in worker(event).iteritems()])
        writeOutput(self, dict(ret))
        return True
