from CMGTools.TTHAnalysis.treeReAnalyzer import *
from CMGTools.TTHAnalysis.tools.mvaTool import *

class KinMVA_2D_2lss_3l:
    def __init__(self, weights, skip_BDTv8 = False, skip_MEM = False, skip_Hj = False):
        self._MVAs = {}
        self._skip_BDTv8 = skip_BDTv8
        self._skip_Hj = skip_Hj
        self._skip_MEM = skip_MEM

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
        self._vars_ttV_2lss = [ 
            MVAVar("max_Lep_eta:=max(abs(LepGood_eta[iLepFO_Recl[0]]),abs(LepGood_eta[iLepFO_Recl[1]]))", func = lambda ev : max(abs(ev.LepGood_eta[int(ev.iLepFO_Recl[0])]),abs(ev.LepGood_eta[int(ev.iLepFO_Recl[1])]))),
            MVAVar("numJets_float:=nJet25_Recl", func = lambda ev : ev.nJet25_Recl),
            MVAVar("mindr_lep1_jet:=mindr_lep1_jet", func = lambda ev: ev.mindr_lep1_jet),
            MVAVar("mindr_lep2_jet:=mindr_lep2_jet", func = lambda ev: ev.mindr_lep2_jet),
            MVAVar("MT_met_lep1:=MT_met_lep1", func = lambda ev : ev.MT_met_lep1),
            MVAVar("LepGood_conePt[iLepFO_Recl[1]]:=LepGood_conePt[iLepFO_Recl[1]]", func = lambda ev : ev.LepGood_conePt[int(ev.iLepFO_Recl[1])]),
            MVAVar("LepGood_conePt[iLepFO_Recl[0]]:=LepGood_conePt[iLepFO_Recl[0]]", func = lambda ev : ev.LepGood_conePt[int(ev.iLepFO_Recl[0])]),
            ]
        self._vars_ttV_2lss_withHj = self._vars_ttV_2lss + [
            MVAVar("BDTv8_eventReco_Hj_score := max(-1.1,BDTv8_eventReco_Hj_score)", func = lambda ev : max(-1.1,ev.BDTv8_eventReco_Hj_score)),
#            MVAVar("BDTv8_eventReco_Hjj_score := max(-1.1,BDTv8_eventReco_Hjj_score)", func = lambda ev : max(-1.1,ev.BDTv8_eventReco_Hjj_score)),
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
        self._vars_ttV_2lss_jecUp = [ 
            MVAVar("max_Lep_eta:=max(abs(LepGood_eta[iLepFO_Recl[0]]),abs(LepGood_eta[iLepFO_Recl[1]]))", func = lambda ev : max(abs(ev.LepGood_eta[int(ev.iLepFO_Recl[0])]),abs(ev.LepGood_eta[int(ev.iLepFO_Recl[1])]))),
            MVAVar("numJets_float:=nJet25_Recl", func = lambda ev : ev.nJet25_jecUp_Recl),
            MVAVar("mindr_lep1_jet:=mindr_lep1_jet", func = lambda ev: ev.mindr_lep1_jet_jecUp),
            MVAVar("mindr_lep2_jet:=mindr_lep2_jet", func = lambda ev: ev.mindr_lep2_jet_jecUp),
            MVAVar("MT_met_lep1:=MT_met_lep1", func = lambda ev : ev.MT_met_lep1_jecUp),
            MVAVar("LepGood_conePt[iLepFO_Recl[1]]:=LepGood_conePt[iLepFO_Recl[1]]", func = lambda ev : ev.LepGood_conePt[int(ev.iLepFO_Recl[1])]),
            MVAVar("LepGood_conePt[iLepFO_Recl[0]]:=LepGood_conePt[iLepFO_Recl[0]]", func = lambda ev : ev.LepGood_conePt[int(ev.iLepFO_Recl[0])]),
            ]
        self._vars_ttV_2lss_withHj_jecUp = self._vars_ttV_2lss_jecUp + [
            MVAVar("BDTv8_eventReco_Hj_score := max(-1.1,BDTv8_eventReco_Hj_score)", func = lambda ev : max(-1.1,ev.BDTv8_eventReco_Hj_score_jecUp)),
#            MVAVar("BDTv8_eventReco_Hjj_score := max(-1.1,BDTv8_eventReco_Hjj_score)", func = lambda ev : max(-1.1,ev.BDTv8_eventReco_Hjj_score_jecUp)),
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
        self._vars_ttV_2lss_jecDown = [ 
            MVAVar("max_Lep_eta:=max(abs(LepGood_eta[iLepFO_Recl[0]]),abs(LepGood_eta[iLepFO_Recl[1]]))", func = lambda ev : max(abs(ev.LepGood_eta[int(ev.iLepFO_Recl[0])]),abs(ev.LepGood_eta[int(ev.iLepFO_Recl[1])]))),
            MVAVar("numJets_float:=nJet25_Recl", func = lambda ev : ev.nJet25_jecDown_Recl),
            MVAVar("mindr_lep1_jet:=mindr_lep1_jet", func = lambda ev: ev.mindr_lep1_jet_jecDown),
            MVAVar("mindr_lep2_jet:=mindr_lep2_jet", func = lambda ev: ev.mindr_lep2_jet_jecDown),
            MVAVar("MT_met_lep1:=MT_met_lep1", func = lambda ev : ev.MT_met_lep1_jecDown),
            MVAVar("LepGood_conePt[iLepFO_Recl[1]]:=LepGood_conePt[iLepFO_Recl[1]]", func = lambda ev : ev.LepGood_conePt[int(ev.iLepFO_Recl[1])]),
            MVAVar("LepGood_conePt[iLepFO_Recl[0]]:=LepGood_conePt[iLepFO_Recl[0]]", func = lambda ev : ev.LepGood_conePt[int(ev.iLepFO_Recl[0])]),
            ]
        self._vars_ttV_2lss_withHj_jecDown = self._vars_ttV_2lss_jecDown + [
            MVAVar("BDTv8_eventReco_Hj_score := max(-1.1,BDTv8_eventReco_Hj_score)", func = lambda ev : max(-1.1,ev.BDTv8_eventReco_Hj_score_jecDown)),
#            MVAVar("BDTv8_eventReco_Hjj_score := max(-1.1,BDTv8_eventReco_Hjj_score)", func = lambda ev : max(-1.1,ev.BDTv8_eventReco_Hjj_score_jecDown)),
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

        memvars = [
            MVAVar("MEM_LR := -log((0.00389464*MEM_TTLL*(MEM_TTLL<1) + 3.12221e-14*MEM_TTW*(MEM_TTW<1)) / (0.00389464*MEM_TTLL*(MEM_TTLL<1) + 3.12221e-14*MEM_TTW*(MEM_TTW<1)+9.99571e-05*(MEM_TTHfl*(MEM_TTHfl<1)+MEM_TTHsl*(MEM_TTHsl<1))/2))", func = lambda ev : -log((0.00389464*ev.MEM_TTLL + 3.12221e-14*ev.MEM_TTW) / (0.00389464*ev.MEM_TTLL + 3.12221e-14*ev.MEM_TTW+9.99571e-05*(ev.MEM_TTHfl+ev.MEM_TTHsl)/2)) if (ev.MEM_TTLL>=0 and ev.MEM_TTLL<1 and ev.MEM_TTW>=0 and ev.MEM_TTW<1 and ev.MEM_TTHfl>=0 and ev.MEM_TTHfl<1 and ev.MEM_TTHsl>=0 and ev.MEM_TTHsl<1 and not (ev.MEM_TTLL==0 and ev.MEM_TTW==0)) else 0)
            ]
        self._vars_ttV_3l_withMEM = self._vars_ttV_3l + memvars
        self._vars_ttV_3l_withMEM_jecUp = self._vars_ttV_3l_jecUp + memvars
        self._vars_ttV_3l_withMEM_jecDown = self._vars_ttV_3l_jecDown + memvars

        for var in self.systsJEC:

            self._MVAs["kinMVA_2lss_ttbar"+self.systsJEC[var]] = MVATool("2lss_ttbar"+self.systsJEC[var], weights%"2lss_ttbar", getattr(self,"_vars_ttbar_2lss"+self.systsJEC[var]), specs = self._specs)
            self._MVAs["kinMVA_2lss_ttbar_withBDTv8"+self.systsJEC[var]] = MVATool("2lss_ttbar_withBDTv8"+self.systsJEC[var], weights%"2lss_ttbar_withBDTv8", getattr(self,"_vars_ttbar_2lss_withBDTv8"+self.systsJEC[var]), specs = self._specs) if not self._skip_BDTv8 else self.put_minus_99
            self._MVAs["kinMVA_2lss_ttV"+self.systsJEC[var]] = MVATool("2lss_ttV"+self.systsJEC[var], weights%"2lss_ttV", getattr(self,"_vars_ttV_2lss"+self.systsJEC[var]), specs = self._specs)
            self._MVAs["kinMVA_2lss_ttV_withHj"+self.systsJEC[var]] = MVATool("2lss_ttV_withHj"+self.systsJEC[var], weights%"2lss_ttV_withHj", getattr(self,"_vars_ttV_2lss_withHj"+self.systsJEC[var]), specs = self._specs) if not self._skip_Hj else self.put_minus_99

            self._MVAs["kinMVA_3l_ttbar"+self.systsJEC[var]] = MVATool("3l_ttbar"+self.systsJEC[var], weights%"3l_ttbar", getattr(self,"_vars_ttbar_3l"+self.systsJEC[var]), specs = self._specs)
            self._MVAs["kinMVA_3l_ttV"+self.systsJEC[var]] = MVATool("3l_ttV"+self.systsJEC[var], weights%"3l_ttV", getattr(self,"_vars_ttV_3l"+self.systsJEC[var]), specs = self._specs)
            self._MVAs["kinMVA_3l_ttV_withMEM"+self.systsJEC[var]] = MVATool("3l_ttV_withMEM"+self.systsJEC[var], weights%"3l_ttV_withMEM", getattr(self,"_vars_ttV_3l_withMEM"+self.systsJEC[var]), specs = self._specs) if not self._skip_MEM else self.put_minus_99

        if self._skip_BDTv8: print 'WARNING: will set kinMVA_2lss_ttbar_withBDTv8 to dummy value (-99) as requested'
        if self._skip_Hj: print 'WARNING: will set kinMVA_2lss_ttV_withHj to dummy value (-99) as requested'
        if self._skip_MEM: print 'WARNING: will set kinMVA_3l_ttV_withMEM to dummy value (-99) as requested'

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
                if j in name and not hasattr(event,"nJet25"+j+'_Recl'): _mva = self._MVAs[name.replace(j,"")]
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

