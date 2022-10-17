from CMGTools.TTHAnalysis.treeReAnalyzer import *
from CMGTools.TTHAnalysis.tools.mvaTool import *

class KinMVA_2D_2lss_3l:
    def __init__(self, weights, useTT_2lss = '', useMEM_3l = False):
        self._MVAs = {}
        self._useTT_2lss = useTT_2lss
        self._useMEM_3l = useMEM_3l

        self.systsJEC = {0:"", 1:"_jecUp", -1:"_jecDown"}

        self._specs = [
            MVAVar("iF0 := iLepFO_Recl[0]", func = lambda ev : ev.iLepFO_Recl[0]),
            MVAVar("iF1 := iLepFO_Recl[1]", func = lambda ev : ev.iLepFO_Recl[1]),
            MVAVar("iF2 := iLepFO_Recl[2]", func = lambda ev : ev.iLepFO_Recl[2]),
            ]

        self._vars_ttbar_2lss = [ 
            MVAVar("max_Lep_eta:=max(abs(LepGood_eta[iLepFO_Recl[0]]),abs(LepGood_eta[iLepFO_Recl[1]]))", func = lambda ev : max(abs(ev.LepGood_eta[int(ev.iLepFO_Recl[0])]),abs(ev.LepGood_eta[int(ev.iLepFO_Recl[1])]))),
            MVAVar("numJets_float:=nJet25_Recl", func = lambda ev : ev.nJet25_Recl),
            MVAVar("mindr_lep1_jet:=mindr_lep1_jet", func = lambda ev: ev.mindr_lep1_jet),
            MVAVar("mindr_lep2_jet:=mindr_lep2_jet", func = lambda ev: ev.mindr_lep2_jet),
            MVAVar("MT_met_lep1:=MT_met_lep1", func = lambda ev : ev.MT_met_lep1),
#            MVAVar("met:=min(met_pt, 400)", func = lambda ev : min(ev.met_pt, 400)),
#            MVAVar("avg_dr_jet:=avg_dr_jet", func = lambda ev : ev.avg_dr_jet),
            ]
        self._vars_ttbar_2lss_withBDTv8 = self._vars_ttbar_2lss + [
            MVAVar("BDTv8_eventReco_mvaValue := max(-1.1,BDTv8_eventReco_mvaValue)", func = lambda ev : max(-1.1,ev.BDTv8_eventReco_mvaValue)),
            ]
        self._vars_ttbar_2lss_withBDTrTT = self._vars_ttbar_2lss + [
            MVAVar("BDTrTT_eventReco_mvaValue := max(-1.1,BDTrTT_eventReco_mvaValue)", func = lambda ev : max(-1.1,ev.BDTrTT_eventReco_mvaValue)),
            ]
        self._vars_ttbar_2lss_withBDThttTT = self._vars_ttbar_2lss + [
            MVAVar("BDThttTT_eventReco_mvaValue := max(-1.1,BDThttTT_eventReco_mvaValue)", func = lambda ev : max(-1.1,ev.BDThttTT_eventReco_mvaValue)),
            ]
        self._vars_ttV_2lss = [ 
            MVAVar("max_Lep_eta:=max(abs(LepGood_eta[iLepFO_Recl[0]]),abs(LepGood_eta[iLepFO_Recl[1]]))", func = lambda ev : max(abs(ev.LepGood_eta[int(ev.iLepFO_Recl[0])]),abs(ev.LepGood_eta[int(ev.iLepFO_Recl[1])]))),
            MVAVar("numJets_float:=nJet25_Recl", func = lambda ev : ev.nJet25_Recl),
            MVAVar("mindr_lep1_jet:=mindr_lep1_jet", func = lambda ev: ev.mindr_lep1_jet),
            MVAVar("mindr_lep2_jet:=mindr_lep2_jet", func = lambda ev: ev.mindr_lep2_jet),
            MVAVar("MT_met_lep1:=MT_met_lep1", func = lambda ev : ev.MT_met_lep1),
            MVAVar("LepGood_conePt[iLepFO_Recl[1]]:=LepGood_conePt[iLepFO_Recl[1]]", func = lambda ev : ev.LepGood_conePt[int(ev.iLepFO_Recl[1])]),
            MVAVar("LepGood_conePt[iLepFO_Recl[0]]:=LepGood_conePt[iLepFO_Recl[0]]", func = lambda ev : ev.LepGood_conePt[int(ev.iLepFO_Recl[0])]),
            ]
        self._vars_ttV_2lss_withHj_v8 = self._vars_ttV_2lss + [
            MVAVar("BDTv8_eventReco_Hj_score := max(-1.1,BDTv8_eventReco_Hj_score)", func = lambda ev : max(-1.1,ev.BDTv8_eventReco_Hj_score)),
#            MVAVar("BDTv8_eventReco_Hjj_score := max(-1.1,BDTv8_eventReco_Hjj_score)", func = lambda ev : max(-1.1,ev.BDTv8_eventReco_Hjj_score)),
            ]
        self._vars_ttV_2lss_withHj_rTT = self._vars_ttV_2lss + [
            MVAVar("BDTrTT_eventReco_Hj_score := max(-1.1,BDTrTT_eventReco_Hj_score)", func = lambda ev : max(-1.1,ev.BDTrTT_eventReco_Hj_score)),
#            MVAVar("BDTrTT_eventReco_Hjj_score := max(-1.1,BDTrTT_eventReco_Hjj_score)", func = lambda ev : max(-1.1,ev.BDTrTT_eventReco_Hjj_score)),
            ]
        self._vars_ttV_2lss_withHj_httTT = self._vars_ttV_2lss + [
            MVAVar("BDThttTT_eventReco_Hj_score := max(-1.1,BDThttTT_eventReco_Hj_score)", func = lambda ev : max(-1.1,ev.BDThttTT_eventReco_Hj_score)),
#            MVAVar("BDThttTT_eventReco_Hjj_score := max(-1.1,BDThttTT_eventReco_Hjj_score)", func = lambda ev : max(-1.1,ev.BDThttTT_eventReco_Hjj_score)),
            ]

        self._vars_ttbar_3l = [ 
            MVAVar("max_Lep_eta:=max(abs(LepGood_eta[iLepFO_Recl[0]]),abs(LepGood_eta[iLepFO_Recl[1]]))", func = lambda ev : max(abs(ev.LepGood_eta[int(ev.iLepFO_Recl[0])]),abs(ev.LepGood_eta[int(ev.iLepFO_Recl[1])]))),
            MVAVar("numJets_float:=nJet25_Recl", func = lambda ev : ev.nJet25_Recl),
            MVAVar("mindr_lep1_jet:=mindr_lep1_jet", func = lambda ev: ev.mindr_lep1_jet),
            MVAVar("mindr_lep2_jet:=mindr_lep2_jet", func = lambda ev: ev.mindr_lep2_jet),
            MVAVar("MT_met_lep1:=MT_met_lep1", func = lambda ev : ev.MT_met_lep1),
#            MVAVar("mhtJet25:=mhtJet25_Recl", func = lambda ev : ev.mhtJet25_Recl),
#            MVAVar("avg_dr_jet:=avg_dr_jet", func = lambda ev : ev.avg_dr_jet),
            ]
        self._vars_ttV_3l = [ 
            MVAVar("max_Lep_eta:=max(abs(LepGood_eta[iLepFO_Recl[0]]),abs(LepGood_eta[iLepFO_Recl[1]]))", func = lambda ev : max(abs(ev.LepGood_eta[int(ev.iLepFO_Recl[0])]),abs(ev.LepGood_eta[int(ev.iLepFO_Recl[1])]))),
            MVAVar("numJets_float:=nJet25_Recl", func = lambda ev : ev.nJet25_Recl),
            MVAVar("mindr_lep1_jet:=mindr_lep1_jet", func = lambda ev: ev.mindr_lep1_jet),
            MVAVar("mindr_lep2_jet:=mindr_lep2_jet", func = lambda ev: ev.mindr_lep2_jet),
            MVAVar("MT_met_lep1:=MT_met_lep1", func = lambda ev : ev.MT_met_lep1),
            MVAVar("LepGood_conePt[iLepFO_Recl[2]]:=LepGood_conePt[iLepFO_Recl[2]]", func = lambda ev : ev.LepGood_conePt[int(ev.iLepFO_Recl[2])]),
            MVAVar("LepGood_conePt[iLepFO_Recl[0]]:=LepGood_conePt[iLepFO_Recl[0]]", func = lambda ev : ev.LepGood_conePt[int(ev.iLepFO_Recl[0])]),
            ]

        self._vars_ttbar_2lss_jecUp = [ 
            MVAVar("max_Lep_eta:=max(abs(LepGood_eta[iLepFO_Recl[0]]),abs(LepGood_eta[iLepFO_Recl[1]]))", func = lambda ev : max(abs(ev.LepGood_eta[int(ev.iLepFO_Recl[0])]),abs(ev.LepGood_eta[int(ev.iLepFO_Recl[1])]))),
            MVAVar("numJets_float:=nJet25_Recl", func = lambda ev : ev.nJet25_jecUp_Recl),
            MVAVar("mindr_lep1_jet:=mindr_lep1_jet", func = lambda ev: ev.mindr_lep1_jet_jecUp),
            MVAVar("mindr_lep2_jet:=mindr_lep2_jet", func = lambda ev: ev.mindr_lep2_jet_jecUp),
            MVAVar("MT_met_lep1:=MT_met_lep1", func = lambda ev : ev.MT_met_lep1_jecUp),
#            MVAVar("met:=min(met_pt, 400)", func = lambda ev : min(ev.met_jecUp_pt, 400)),
#            MVAVar("avg_dr_jet:=avg_dr_jet", func = lambda ev : ev.avg_dr_jet_jecUp),
            ]
        self._vars_ttbar_2lss_withBDTv8_jecUp = self._vars_ttbar_2lss_jecUp + [
            MVAVar("BDTv8_eventReco_mvaValue := max(-1.1,BDTv8_eventReco_mvaValue)", func = lambda ev : max(-1.1,ev.BDTv8_eventReco_mvaValue_jecUp)),
            ]
        self._vars_ttbar_2lss_withBDTrTT_jecUp = self._vars_ttbar_2lss_jecUp + [
            MVAVar("BDTrTT_eventReco_mvaValue := max(-1.1,BDTrTT_eventReco_mvaValue)", func = lambda ev : max(-1.1,ev.BDTrTT_eventReco_mvaValue_jecUp)),
            ]
        self._vars_ttbar_2lss_withBDThttTT_jecUp = self._vars_ttbar_2lss_jecUp + [
            MVAVar("BDThttTT_eventReco_mvaValue := max(-1.1,BDThttTT_eventReco_mvaValue)", func = lambda ev : max(-1.1,ev.BDThttTT_eventReco_mvaValue_jecUp)),
            ]
        self._vars_ttV_2lss_jecUp = [ 
            MVAVar("max_Lep_eta:=max(abs(LepGood_eta[iLepFO_Recl[0]]),abs(LepGood_eta[iLepFO_Recl[1]]))", func = lambda ev : max(abs(ev.LepGood_eta[int(ev.iLepFO_Recl[0])]),abs(ev.LepGood_eta[int(ev.iLepFO_Recl[1])]))),
            MVAVar("numJets_float:=nJet25_Recl", func = lambda ev : ev.nJet25_jecUp_Recl),
            MVAVar("mindr_lep1_jet:=mindr_lep1_jet", func = lambda ev: ev.mindr_lep1_jet_jecUp),
            MVAVar("mindr_lep2_jet:=mindr_lep2_jet", func = lambda ev: ev.mindr_lep2_jet_jecUp),
            MVAVar("MT_met_lep1:=MT_met_lep1", func = lambda ev : ev.MT_met_lep1_jecUp),
            MVAVar("LepGood_conePt[iLepFO_Recl[1]]:=LepGood_conePt[iLepFO_Recl[1]]", func = lambda ev : ev.LepGood_conePt[int(ev.iLepFO_Recl[1])]),
            MVAVar("LepGood_conePt[iLepFO_Recl[0]]:=LepGood_conePt[iLepFO_Recl[0]]", func = lambda ev : ev.LepGood_conePt[int(ev.iLepFO_Recl[0])]),
            ]
        self._vars_ttV_2lss_withHj_v8_jecUp = self._vars_ttV_2lss_jecUp + [
            MVAVar("BDTv8_eventReco_Hj_score := max(-1.1,BDTv8_eventReco_Hj_score)", func = lambda ev : max(-1.1,ev.BDTv8_eventReco_Hj_score_jecUp)),
#            MVAVar("BDTv8_eventReco_Hjj_score := max(-1.1,BDTv8_eventReco_Hjj_score)", func = lambda ev : max(-1.1,ev.BDTv8_eventReco_Hjj_score_jecUp)),
            ]
        self._vars_ttV_2lss_withHj_rTT_jecUp = self._vars_ttV_2lss_jecUp + [
            MVAVar("BDTrTT_eventReco_Hj_score := max(-1.1,BDTrTT_eventReco_Hj_score)", func = lambda ev : max(-1.1,ev.BDTrTT_eventReco_Hj_score_jecUp)),
#            MVAVar("BDTrTT_eventReco_Hjj_score := max(-1.1,BDTrTT_eventReco_Hjj_score)", func = lambda ev : max(-1.1,ev.BDTrTT_eventReco_Hjj_score_jecUp)),
            ]
        self._vars_ttV_2lss_withHj_httTT_jecUp = self._vars_ttV_2lss_jecUp + [
            MVAVar("BDThttTT_eventReco_Hj_score := max(-1.1,BDThttTT_eventReco_Hj_score)", func = lambda ev : max(-1.1,ev.BDThttTT_eventReco_Hj_score_jecUp)),
#            MVAVar("BDThttTT_eventReco_Hjj_score := max(-1.1,BDThttTT_eventReco_Hjj_score)", func = lambda ev : max(-1.1,ev.BDThttTT_eventReco_Hjj_score_jecUp)),
            ]
        self._vars_ttbar_3l_jecUp = [ 
            MVAVar("max_Lep_eta:=max(abs(LepGood_eta[iLepFO_Recl[0]]),abs(LepGood_eta[iLepFO_Recl[1]]))", func = lambda ev : max(abs(ev.LepGood_eta[int(ev.iLepFO_Recl[0])]),abs(ev.LepGood_eta[int(ev.iLepFO_Recl[1])]))),
            MVAVar("numJets_float:=nJet25_Recl", func = lambda ev : ev.nJet25_jecUp_Recl),
            MVAVar("mindr_lep1_jet:=mindr_lep1_jet", func = lambda ev: ev.mindr_lep1_jet_jecUp),
            MVAVar("mindr_lep2_jet:=mindr_lep2_jet", func = lambda ev: ev.mindr_lep2_jet_jecUp),
            MVAVar("MT_met_lep1:=MT_met_lep1", func = lambda ev : ev.MT_met_lep1_jecUp),
#            MVAVar("mhtJet25:=mhtJet25_Recl", func = lambda ev : ev.mhtJet25_jecUp_Recl),
#            MVAVar("avg_dr_jet:=avg_dr_jet", func = lambda ev : ev.avg_dr_jet_jecUp),
            ]
        self._vars_ttV_3l_jecUp = [ 
            MVAVar("max_Lep_eta:=max(abs(LepGood_eta[iLepFO_Recl[0]]),abs(LepGood_eta[iLepFO_Recl[1]]))", func = lambda ev : max(abs(ev.LepGood_eta[int(ev.iLepFO_Recl[0])]),abs(ev.LepGood_eta[int(ev.iLepFO_Recl[1])]))),
            MVAVar("numJets_float:=nJet25_Recl", func = lambda ev : ev.nJet25_jecUp_Recl),
            MVAVar("mindr_lep1_jet:=mindr_lep1_jet", func = lambda ev: ev.mindr_lep1_jet_jecUp),
            MVAVar("mindr_lep2_jet:=mindr_lep2_jet", func = lambda ev: ev.mindr_lep2_jet_jecUp),
            MVAVar("MT_met_lep1:=MT_met_lep1", func = lambda ev : ev.MT_met_lep1_jecUp),
            MVAVar("LepGood_conePt[iLepFO_Recl[2]]:=LepGood_conePt[iLepFO_Recl[2]]", func = lambda ev : ev.LepGood_conePt[int(ev.iLepFO_Recl[2])]),
            MVAVar("LepGood_conePt[iLepFO_Recl[0]]:=LepGood_conePt[iLepFO_Recl[0]]", func = lambda ev : ev.LepGood_conePt[int(ev.iLepFO_Recl[0])]),
            ]

        self._vars_ttbar_2lss_jecDown = [ 
            MVAVar("max_Lep_eta:=max(abs(LepGood_eta[iLepFO_Recl[0]]),abs(LepGood_eta[iLepFO_Recl[1]]))", func = lambda ev : max(abs(ev.LepGood_eta[int(ev.iLepFO_Recl[0])]),abs(ev.LepGood_eta[int(ev.iLepFO_Recl[1])]))),
            MVAVar("numJets_float:=nJet25_Recl", func = lambda ev : ev.nJet25_jecDown_Recl),
            MVAVar("mindr_lep1_jet:=mindr_lep1_jet", func = lambda ev: ev.mindr_lep1_jet_jecDown),
            MVAVar("mindr_lep2_jet:=mindr_lep2_jet", func = lambda ev: ev.mindr_lep2_jet_jecDown),
            MVAVar("MT_met_lep1:=MT_met_lep1", func = lambda ev : ev.MT_met_lep1_jecDown),
#            MVAVar("met:=min(met_pt, 400)", func = lambda ev : min(ev.met_jecDown_pt, 400)),
#            MVAVar("avg_dr_jet:=avg_dr_jet", func = lambda ev : ev.avg_dr_jet_jecDown),
            ]
        self._vars_ttbar_2lss_withBDTv8_jecDown = self._vars_ttbar_2lss_jecDown + [
            MVAVar("BDTv8_eventReco_mvaValue := max(-1.1,BDTv8_eventReco_mvaValue)", func = lambda ev : max(-1.1,ev.BDTv8_eventReco_mvaValue_jecDown)),
            ]
        self._vars_ttbar_2lss_withBDTrTT_jecDown = self._vars_ttbar_2lss_jecDown + [
            MVAVar("BDTrTT_eventReco_mvaValue := max(-1.1,BDTrTT_eventReco_mvaValue)", func = lambda ev : max(-1.1,ev.BDTrTT_eventReco_mvaValue_jecDown)),
            ]
        self._vars_ttbar_2lss_withBDThttTT_jecDown = self._vars_ttbar_2lss_jecDown + [
            MVAVar("BDThttTT_eventReco_mvaValue := max(-1.1,BDThttTT_eventReco_mvaValue)", func = lambda ev : max(-1.1,ev.BDThttTT_eventReco_mvaValue_jecDown)),
            ]
        self._vars_ttV_2lss_jecDown = [ 
            MVAVar("max_Lep_eta:=max(abs(LepGood_eta[iLepFO_Recl[0]]),abs(LepGood_eta[iLepFO_Recl[1]]))", func = lambda ev : max(abs(ev.LepGood_eta[int(ev.iLepFO_Recl[0])]),abs(ev.LepGood_eta[int(ev.iLepFO_Recl[1])]))),
            MVAVar("numJets_float:=nJet25_Recl", func = lambda ev : ev.nJet25_jecDown_Recl),
            MVAVar("mindr_lep1_jet:=mindr_lep1_jet", func = lambda ev: ev.mindr_lep1_jet_jecDown),
            MVAVar("mindr_lep2_jet:=mindr_lep2_jet", func = lambda ev: ev.mindr_lep2_jet_jecDown),
            MVAVar("MT_met_lep1:=MT_met_lep1", func = lambda ev : ev.MT_met_lep1_jecDown),
            MVAVar("LepGood_conePt[iLepFO_Recl[1]]:=LepGood_conePt[iLepFO_Recl[1]]", func = lambda ev : ev.LepGood_conePt[int(ev.iLepFO_Recl[1])]),
            MVAVar("LepGood_conePt[iLepFO_Recl[0]]:=LepGood_conePt[iLepFO_Recl[0]]", func = lambda ev : ev.LepGood_conePt[int(ev.iLepFO_Recl[0])]),
            ]
        self._vars_ttV_2lss_withHj_v8_jecDown = self._vars_ttV_2lss_jecDown + [
            MVAVar("BDTv8_eventReco_Hj_score := max(-1.1,BDTv8_eventReco_Hj_score)", func = lambda ev : max(-1.1,ev.BDTv8_eventReco_Hj_score_jecDown)),
#            MVAVar("BDTv8_eventReco_Hjj_score := max(-1.1,BDTv8_eventReco_Hjj_score)", func = lambda ev : max(-1.1,ev.BDTv8_eventReco_Hjj_score_jecDown)),
            ]
        self._vars_ttV_2lss_withHj_rTT_jecDown = self._vars_ttV_2lss_jecDown + [
            MVAVar("BDTrTT_eventReco_Hj_score := max(-1.1,BDTrTT_eventReco_Hj_score)", func = lambda ev : max(-1.1,ev.BDTrTT_eventReco_Hj_score_jecDown)),
#            MVAVar("BDTrTT_eventReco_Hjj_score := max(-1.1,BDTrTT_eventReco_Hjj_score)", func = lambda ev : max(-1.1,ev.BDTrTT_eventReco_Hjj_score_jecDown)),
            ]
        self._vars_ttV_2lss_withHj_httTT_jecDown = self._vars_ttV_2lss_jecDown + [
            MVAVar("BDThttTT_eventReco_Hj_score := max(-1.1,BDThttTT_eventReco_Hj_score)", func = lambda ev : max(-1.1,ev.BDThttTT_eventReco_Hj_score_jecDown)),
#            MVAVar("BDThttTT_eventReco_Hjj_score := max(-1.1,BDThttTT_eventReco_Hjj_score)", func = lambda ev : max(-1.1,ev.BDThttTT_eventReco_Hjj_score_jecDown)),
            ]
        self._vars_ttbar_3l_jecDown = [ 
            MVAVar("max_Lep_eta:=max(abs(LepGood_eta[iLepFO_Recl[0]]),abs(LepGood_eta[iLepFO_Recl[1]]))", func = lambda ev : max(abs(ev.LepGood_eta[int(ev.iLepFO_Recl[0])]),abs(ev.LepGood_eta[int(ev.iLepFO_Recl[1])]))),
            MVAVar("numJets_float:=nJet25_Recl", func = lambda ev : ev.nJet25_jecDown_Recl),
            MVAVar("mindr_lep1_jet:=mindr_lep1_jet", func = lambda ev: ev.mindr_lep1_jet_jecDown),
            MVAVar("mindr_lep2_jet:=mindr_lep2_jet", func = lambda ev: ev.mindr_lep2_jet_jecDown),
            MVAVar("MT_met_lep1:=MT_met_lep1", func = lambda ev : ev.MT_met_lep1_jecDown),
#            MVAVar("mhtJet25:=mhtJet25_Recl", func = lambda ev : ev.mhtJet25_jecDown_Recl),
#            MVAVar("avg_dr_jet:=avg_dr_jet", func = lambda ev : ev.avg_dr_jet_jecDown),
            ]
        self._vars_ttV_3l_jecDown = [ 
            MVAVar("max_Lep_eta:=max(abs(LepGood_eta[iLepFO_Recl[0]]),abs(LepGood_eta[iLepFO_Recl[1]]))", func = lambda ev : max(abs(ev.LepGood_eta[int(ev.iLepFO_Recl[0])]),abs(ev.LepGood_eta[int(ev.iLepFO_Recl[1])]))),
            MVAVar("numJets_float:=nJet25_Recl", func = lambda ev : ev.nJet25_jecDown_Recl),
            MVAVar("mindr_lep1_jet:=mindr_lep1_jet", func = lambda ev: ev.mindr_lep1_jet_jecDown),
            MVAVar("mindr_lep2_jet:=mindr_lep2_jet", func = lambda ev: ev.mindr_lep2_jet_jecDown),
            MVAVar("MT_met_lep1:=MT_met_lep1", func = lambda ev : ev.MT_met_lep1_jecDown),
            MVAVar("LepGood_conePt[iLepFO_Recl[2]]:=LepGood_conePt[iLepFO_Recl[2]]", func = lambda ev : ev.LepGood_conePt[int(ev.iLepFO_Recl[2])]),
            MVAVar("LepGood_conePt[iLepFO_Recl[0]]:=LepGood_conePt[iLepFO_Recl[0]]", func = lambda ev : ev.LepGood_conePt[int(ev.iLepFO_Recl[0])]),
            ]

        memvars_ttV = [
            MVAVar("MEM_LR_ttHttV := -log((0.00389464*MEM_TTLL*(MEM_TTLL<1)+3.12221e-14*MEM_TTW*(MEM_TTW<1))/(0.00389464*MEM_TTLL*(MEM_TTLL<1)+3.12221e-14*MEM_TTW*(MEM_TTW<1)+9.99571e-05*(MEM_TTH_mean*(MEM_TTH_mean<1))))",
                   func = lambda ev : -log((0.00389464*ev.MEM_TTLL + 3.12221e-14*ev.MEM_TTW) / (0.00389464*ev.MEM_TTLL + 3.12221e-14*ev.MEM_TTW+9.99571e-05*ev.MEM_TTH_mean)) if (ev.MEM_TTLL>=0 and ev.MEM_TTLL<1 and ev.MEM_TTW>=0 and ev.MEM_TTW<1 and ev.MEM_TTH_mean>=0 and ev.MEM_TTH_mean<1 and not (ev.MEM_TTLL==0 and ev.MEM_TTW==0)) else 0)
            ]
        memvars_ttV_jecUp = [
            MVAVar("MEM_LR_ttHttV := -log((0.00389464*MEM_TTLL*(MEM_TTLL<1)+3.12221e-14*MEM_TTW*(MEM_TTW<1))/(0.00389464*MEM_TTLL*(MEM_TTLL<1)+3.12221e-14*MEM_TTW*(MEM_TTW<1)+9.99571e-05*(MEM_TTH_mean*(MEM_TTH_mean<1))))",
                   func = lambda ev : -log((0.00389464*ev.MEM_TTLL_jecUp + 3.12221e-14*ev.MEM_TTW_jecUp) / (0.00389464*ev.MEM_TTLL_jecUp + 3.12221e-14*ev.MEM_TTW_jecUp+9.99571e-05*ev.MEM_TTH_mean_jecUp)) if (ev.MEM_TTLL_jecUp>=0 and ev.MEM_TTLL_jecUp<1 and ev.MEM_TTW_jecUp>=0 and ev.MEM_TTW_jecUp<1 and ev.MEM_TTH_mean_jecUp>=0 and ev.MEM_TTH_mean_jecUp<1 and not (ev.MEM_TTLL_jecUp==0 and ev.MEM_TTW_jecUp==0)) else 0)
            ]
        memvars_ttV_jecDown = [
            MVAVar("MEM_LR_ttHttV := -log((0.00389464*MEM_TTLL*(MEM_TTLL<1)+3.12221e-14*MEM_TTW*(MEM_TTW<1))/(0.00389464*MEM_TTLL*(MEM_TTLL<1)+3.12221e-14*MEM_TTW*(MEM_TTW<1)+9.99571e-05*(MEM_TTH_mean*(MEM_TTH_mean<1))))",
                   func = lambda ev : -log((0.00389464*ev.MEM_TTLL_jecDown + 3.12221e-14*ev.MEM_TTW_jecDown) / (0.00389464*ev.MEM_TTLL_jecDown + 3.12221e-14*ev.MEM_TTW_jecDown+9.99571e-05*ev.MEM_TTH_mean_jecDown)) if (ev.MEM_TTLL_jecDown>=0 and ev.MEM_TTLL_jecDown<1 and ev.MEM_TTW_jecDown>=0 and ev.MEM_TTW_jecDown<1 and ev.MEM_TTH_mean_jecDown>=0 and ev.MEM_TTH_mean_jecDown<1 and not (ev.MEM_TTLL_jecDown==0 and ev.MEM_TTW_jecDown==0)) else 0)
            ]

        memvars_ttbar = [
            MVAVar("MEM_LR_ttHttbar := -log((MEM_TTbarfl*(MEM_TTbarfl<1)+MEM_TTbarsl*(MEM_TTbarsl<1))/(MEM_TTH_mean*(MEM_TTH_mean<1)))",
                   func = lambda ev : -log((ev.MEM_TTbarfl+ev.MEM_TTbarsl)/ev.MEM_TTH_mean) if (ev.MEM_TTbarfl>=0 and ev.MEM_TTbarfl<1 and ev.MEM_TTbarsl>=0 and ev.MEM_TTbarsl<1 and ev.MEM_TTH_mean>0 and ev.MEM_TTH_mean<1 and not (ev.MEM_TTbarfl==0 and ev.MEM_TTbarsl==0)) else 0)
            ]
        memvars_ttbar_jecUp = [
            MVAVar("MEM_LR_ttHttbar := -log((MEM_TTbarfl*(MEM_TTbarfl<1)+MEM_TTbarsl*(MEM_TTbarsl<1))/(MEM_TTH_mean*(MEM_TTH_mean<1)))",
                   func = lambda ev : -log((ev.MEM_TTbarfl_jecUp+ev.MEM_TTbarsl_jecUp)/ev.MEM_TTH_mean_jecUp) if (ev.MEM_TTbarfl_jecUp>=0 and ev.MEM_TTbarfl_jecUp<1 and ev.MEM_TTbarsl_jecUp>=0 and ev.MEM_TTbarsl_jecUp<1 and ev.MEM_TTH_mean_jecUp>0 and ev.MEM_TTH_mean_jecUp<1 and not (ev.MEM_TTbarfl_jecUp==0 and ev.MEM_TTbarsl_jecUp==0)) else 0)
            ]
        memvars_ttbar_jecDown = [
            MVAVar("MEM_LR_ttHttbar := -log((MEM_TTbarfl*(MEM_TTbarfl<1)+MEM_TTbarsl*(MEM_TTbarsl<1))/(MEM_TTH_mean*(MEM_TTH_mean<1)))",
                   func = lambda ev : -log((ev.MEM_TTbarfl_jecDown+ev.MEM_TTbarsl_jecDown)/ev.MEM_TTH_mean_jecDown) if (ev.MEM_TTbarfl_jecDown>=0 and ev.MEM_TTbarfl_jecDown<1 and ev.MEM_TTbarsl_jecDown>=0 and ev.MEM_TTbarsl_jecDown<1 and ev.MEM_TTH_mean_jecDown>0 and ev.MEM_TTH_mean_jecDown<1 and not (ev.MEM_TTbarfl_jecDown==0 and ev.MEM_TTbarsl_jecDown==0)) else 0)
            ]

        self._vars_ttV_3l_withMEM = self._vars_ttV_3l + memvars_ttV
        self._vars_ttV_3l_withMEM_jecUp = self._vars_ttV_3l_jecUp + memvars_ttV_jecUp
        self._vars_ttV_3l_withMEM_jecDown = self._vars_ttV_3l_jecDown + memvars_ttV_jecDown

        self._vars_ttbar_3l_withMEM = self._vars_ttbar_3l + memvars_ttbar
        self._vars_ttbar_3l_withMEM_jecUp = self._vars_ttbar_3l_jecUp + memvars_ttbar_jecUp
        self._vars_ttbar_3l_withMEM_jecDown = self._vars_ttbar_3l_jecDown + memvars_ttbar_jecDown

        for var in self.systsJEC:

            self._MVAs["kinMVA_2lss_ttbar"+self.systsJEC[var]] = MVATool("2lss_ttbar"+self.systsJEC[var], weights%"2lss_ttbar", getattr(self,"_vars_ttbar_2lss"+self.systsJEC[var]), specs = self._specs)
            self._MVAs["kinMVA_2lss_ttbar_withBDTv8"+self.systsJEC[var]] = MVATool("2lss_ttbar_withBDTv8"+self.systsJEC[var], weights%"2lss_ttbar_withBDTv8", getattr(self,"_vars_ttbar_2lss_withBDTv8"+self.systsJEC[var]), specs = self._specs) if ('v8' in self._useTT_2lss) else self.put_minus_99
            self._MVAs["kinMVA_2lss_ttbar_withBDTrTT"+self.systsJEC[var]] = MVATool("2lss_ttbar_withBDTrTT"+self.systsJEC[var], weights%"2lss_ttbar_withBDTrTT", getattr(self,"_vars_ttbar_2lss_withBDTrTT"+self.systsJEC[var]), specs = self._specs) if ('rTT' in self._useTT_2lss) else self.put_minus_99
            self._MVAs["kinMVA_2lss_ttbar_withBDThttTT"+self.systsJEC[var]] = MVATool("2lss_ttbar_withBDThttTT"+self.systsJEC[var], weights%"2lss_ttbar_withBDThttTT", getattr(self,"_vars_ttbar_2lss_withBDThttTT"+self.systsJEC[var]), specs = self._specs) if ('httTT' in self._useTT_2lss) else self.put_minus_99
            self._MVAs["kinMVA_2lss_ttV"+self.systsJEC[var]] = MVATool("2lss_ttV"+self.systsJEC[var], weights%"2lss_ttV", getattr(self,"_vars_ttV_2lss"+self.systsJEC[var]), specs = self._specs)
            self._MVAs["kinMVA_2lss_ttV_withHj_v8"+self.systsJEC[var]] = MVATool("2lss_ttV_withHj_v8"+self.systsJEC[var], weights%"2lss_ttV_withHj_v8", getattr(self,"_vars_ttV_2lss_withHj_v8"+self.systsJEC[var]), specs = self._specs) if ('v8' in self._useTT_2lss) else self.put_minus_99
            self._MVAs["kinMVA_2lss_ttV_withHj_rTT"+self.systsJEC[var]] = MVATool("2lss_ttV_withHj_rTT"+self.systsJEC[var], weights%"2lss_ttV_withHj_rTT", getattr(self,"_vars_ttV_2lss_withHj_rTT"+self.systsJEC[var]), specs = self._specs) if ('rTT' in self._useTT_2lss) else self.put_minus_99
            self._MVAs["kinMVA_2lss_ttV_withHj_httTT"+self.systsJEC[var]] = MVATool("2lss_ttV_withHj_httTT"+self.systsJEC[var], weights%"2lss_ttV_withHj_httTT", getattr(self,"_vars_ttV_2lss_withHj_httTT"+self.systsJEC[var]), specs = self._specs) if ('httTT' in self._useTT_2lss) else self.put_minus_99
            self._MVAs["kinMVA_3l_ttbar"+self.systsJEC[var]] = MVATool("3l_ttbar"+self.systsJEC[var], weights%"3l_ttbar", getattr(self,"_vars_ttbar_3l"+self.systsJEC[var]), specs = self._specs)
            self._MVAs["kinMVA_3l_ttbar_withMEM"+self.systsJEC[var]] = MVATool("3l_ttbar_withMEM"+self.systsJEC[var], weights%"3l_ttbar_withMEM", getattr(self,"_vars_ttbar_3l_withMEM"+self.systsJEC[var]), specs = self._specs) if self._useMEM_3l else self.put_minus_99
            self._MVAs["kinMVA_3l_ttV"+self.systsJEC[var]] = MVATool("3l_ttV"+self.systsJEC[var], weights%"3l_ttV", getattr(self,"_vars_ttV_3l"+self.systsJEC[var]), specs = self._specs)
            self._MVAs["kinMVA_3l_ttV_withMEM"+self.systsJEC[var]] = MVATool("3l_ttV_withMEM"+self.systsJEC[var], weights%"3l_ttV_withMEM", getattr(self,"_vars_ttV_3l_withMEM"+self.systsJEC[var]), specs = self._specs) if self._useMEM_3l else self.put_minus_99

        if not ('v8' in self._useTT_2lss): print 'WARNING: will set kinMVA_2lss_ttbar_withBDTv8 and kinMVA_2lss_ttV_withHj_v8 to dummy value (-99) as requested'
        if not ('rTT' in self._useTT_2lss): print 'WARNING: will set kinMVA_2lss_ttbar_withBDTrTT and kinMVA_2lss_ttV_withHj_rTT to dummy value (-99) as requested'
        if not ('httTT' in self._useTT_2lss): print 'WARNING: will set kinMVA_2lss_ttbar_withBDThttTT and kinMVA_2lss_ttV_withHj_httTT to dummy value (-99) as requested'
        if not self._useMEM_3l: print 'WARNING: will set kinMVA_3l_ttbar_withMEM and kinMVA_3l_ttV_withMEM to dummy value (-99) as requested'

    def put_minus_99(self,event):
        return -99
    def listBranches(self):
        return self._MVAs.keys()
    def __call__(self,event):
        out = {}
        myvars = [event.iLepFO_Recl[0],event.iLepFO_Recl[1],event.iLepFO_Recl[2]]
        for name, mva in self._MVAs.iteritems():
            _mva = mva
            for i,j in self.systsJEC.iteritems():
                if j in name and (event.isData or not hasattr(event,"nJet25"+j+'_Recl')): _mva = self._MVAs[name.replace(j,"")] # do not calculate jecUp/jecDown on data, put them to nominal
            if '2lss' in name: out[name] = _mva(event) if event.nLepFO_Recl>=2 else -99
            elif '3l' in name: out[name] = _mva(event) if event.nLepFO_Recl>=3 else -99
        return out

if __name__ == '__main__':
    from sys import argv
    file = ROOT.TFile(argv[1])
    tree = file.Get("treeProducerSusyMultilepton")
    file = ROOT.TFile(argv[1])
    tree = file.Get("tree")
    tree.vectorTree = True
    tree.AddFriend("sf/t",argv[2]) # recleaner
    if len(argv)>3: tree.AddFriend("sf/t",argv[3]) # kinvars if as a separate friend tree
              
    class Tester(Module):
        def __init__(self, name):
            Module.__init__(self,name,None)
            self.sf = KinMVA_2D_2lss_3l(weights = './weights/%s_BDTG.weights.xml')
        def analyze(self,ev):
            print "\nrun %6d lumi %4d event %d: leps %d" % (ev.run, ev.lumi, ev.evt, ev.nLepGood)
            print self.sf(ev)
    el = EventLoop([ Tester("tester") ])
    el.loop([tree], maxEvents = 50)

