from CMGTools.TTHAnalysis.treeReAnalyzer import *
from CMGTools.TTHAnalysis.tools.mvaTool import *

class KinMVA_2D_2lss_3l:
    def __init__(self, weights, skip_BDTv8 = False, skip_MEM = False):
        self._MVAs = {}
        self._skip_BDTv8 = skip_BDTv8
        self._skip_MEM = skip_MEM

        self.systsJEC = {0:"", 1:"_jecUp", -1:"_jecDown"}

        self._specs = [
            MVAVar("iF0 := iF_Recl[0]", func = lambda ev : ev.iF_Recl[0]),
            MVAVar("iF1 := iF_Recl[1]", func = lambda ev : ev.iF_Recl[1]),
            MVAVar("iF2 := iF_Recl[2]", func = lambda ev : ev.iF_Recl[2]),
            ]

        self._vars_ttbar_2lss = [ 
            MVAVar("max_Lep_eta:=max(abs(LepGood_eta[iF_Recl[0]]),abs(LepGood_eta[iF_Recl[1]]))", func = lambda ev : max(abs(ev.LepGood_eta[int(ev.iF_Recl[0])]),abs(ev.LepGood_eta[int(ev.iF_Recl[1])]))),
            MVAVar("numJets_float:=nJet25_Recl", func = lambda ev : ev.nJet25_Recl),
            MVAVar("mindr_lep1_jet:=mindr_lep1_jet", func = lambda ev: ev.mindr_lep1_jet),
            MVAVar("mindr_lep2_jet:=mindr_lep2_jet", func = lambda ev: ev.mindr_lep2_jet),
            MVAVar("MT_met_lep1:=MT_met_lep1", func = lambda ev : ev.MT_met_lep1),
            MVAVar("met:=min(met_pt, 400)", func = lambda ev : min(ev.met_pt, 400)),
            MVAVar("avg_dr_jet:=avg_dr_jet", func = lambda ev : ev.avg_dr_jet),
            ]
        self._vars_ttbar_2lss_withBDTv8 = self._vars_ttbar_2lss + [
            MVAVar("BDTv8_eventReco_mvaValue := max(-0.2,BDTv8_eventReco_mvaValue)", func = lambda ev : max(-0.2,ev.BDTv8_eventReco_mvaValue)),
            MVAVar("BDTv8_eventReco_bJet_fromHadTop_CSV := max(-0.2,BDTv8_eventReco_bJet_fromHadTop_CSV)", func = lambda ev : max(-0.2,ev.BDTv8_eventReco_bJet_fromHadTop_CSV)),
            MVAVar("BDTv8_eventReco_HadTop_pT := max(-10,BDTv8_eventReco_HadTop_pT)", func = lambda ev : max(-10,ev.BDTv8_eventReco_HadTop_pT)),
            MVAVar("BDTv8_eventReco_HadTop_mass := max(-10,BDTv8_eventReco_HadTop_mass)", func = lambda ev : max(-10,ev.BDTv8_eventReco_HadTop_mass)),
            ]
        self._vars_ttV_2lss = [ 
            MVAVar("max_Lep_eta:=max(abs(LepGood_eta[iF_Recl[0]]),abs(LepGood_eta[iF_Recl[1]]))", func = lambda ev : max(abs(ev.LepGood_eta[int(ev.iF_Recl[0])]),abs(ev.LepGood_eta[int(ev.iF_Recl[1])]))),
            MVAVar("numJets_float:=nJet25_Recl", func = lambda ev : ev.nJet25_Recl),
            MVAVar("mindr_lep1_jet:=mindr_lep1_jet", func = lambda ev: ev.mindr_lep1_jet),
            MVAVar("mindr_lep2_jet:=mindr_lep2_jet", func = lambda ev: ev.mindr_lep2_jet),
            MVAVar("MT_met_lep1:=MT_met_lep1", func = lambda ev : ev.MT_met_lep1),
            MVAVar("LepGood_conePt[iF_Recl[1]]:=LepGood_conePt[iF_Recl[1]]", func = lambda ev : ev.LepGood_conePt[int(ev.iF_Recl[1])]),
            MVAVar("LepGood_conePt[iF_Recl[0]]:=LepGood_conePt[iF_Recl[0]]", func = lambda ev : ev.LepGood_conePt[int(ev.iF_Recl[0])]),
            ]
        self._vars_ttbar_3l = [ 
            MVAVar("max_Lep_eta:=max(abs(LepGood_eta[iF_Recl[0]]),abs(LepGood_eta[iF_Recl[1]]))", func = lambda ev : max(abs(ev.LepGood_eta[int(ev.iF_Recl[0])]),abs(ev.LepGood_eta[int(ev.iF_Recl[1])]))),
            MVAVar("numJets_float:=nJet25_Recl", func = lambda ev : ev.nJet25_Recl),
            MVAVar("mindr_lep1_jet:=mindr_lep1_jet", func = lambda ev: ev.mindr_lep1_jet),
            MVAVar("mindr_lep2_jet:=mindr_lep2_jet", func = lambda ev: ev.mindr_lep2_jet),
            MVAVar("MT_met_lep1:=MT_met_lep1", func = lambda ev : ev.MT_met_lep1),
            MVAVar("mhtJet25:=mhtJet25_Recl", func = lambda ev : ev.mhtJet25_Recl),
            MVAVar("avg_dr_jet:=avg_dr_jet", func = lambda ev : ev.avg_dr_jet),
            ]
        self._vars_ttV_3l = [ 
            MVAVar("max_Lep_eta:=max(abs(LepGood_eta[iF_Recl[0]]),abs(LepGood_eta[iF_Recl[1]]))", func = lambda ev : max(abs(ev.LepGood_eta[int(ev.iF_Recl[0])]),abs(ev.LepGood_eta[int(ev.iF_Recl[1])]))),
            MVAVar("numJets_float:=nJet25_Recl", func = lambda ev : ev.nJet25_Recl),
            MVAVar("mindr_lep1_jet:=mindr_lep1_jet", func = lambda ev: ev.mindr_lep1_jet),
            MVAVar("mindr_lep2_jet:=mindr_lep2_jet", func = lambda ev: ev.mindr_lep2_jet),
            MVAVar("MT_met_lep1:=MT_met_lep1", func = lambda ev : ev.MT_met_lep1),
            MVAVar("LepGood_conePt[iF_Recl[2]]:=LepGood_conePt[iF_Recl[2]]", func = lambda ev : ev.LepGood_conePt[int(ev.iF_Recl[2])]),
            MVAVar("LepGood_conePt[iF_Recl[0]]:=LepGood_conePt[iF_Recl[0]]", func = lambda ev : ev.LepGood_conePt[int(ev.iF_Recl[0])]),
            ]

        self._vars_ttbar_2lss_jecUp = [ 
            MVAVar("max_Lep_eta:=max(abs(LepGood_eta[iF_Recl[0]]),abs(LepGood_eta[iF_Recl[1]]))", func = lambda ev : max(abs(ev.LepGood_eta[int(ev.iF_Recl[0])]),abs(ev.LepGood_eta[int(ev.iF_Recl[1])]))),
            MVAVar("numJets_float:=nJet25_Recl", func = lambda ev : ev.nJet25_Recl_jecUp),
            MVAVar("mindr_lep1_jet:=mindr_lep1_jet", func = lambda ev: ev.mindr_lep1_jet_jecUp),
            MVAVar("mindr_lep2_jet:=mindr_lep2_jet", func = lambda ev: ev.mindr_lep2_jet_jecUp),
            MVAVar("MT_met_lep1:=MT_met_lep1", func = lambda ev : ev.MT_met_lep1_jecUp),
            MVAVar("met:=min(met_pt, 400)", func = lambda ev : min(ev.met_jecUp_pt, 400)),
            MVAVar("avg_dr_jet:=avg_dr_jet", func = lambda ev : ev.avg_dr_jet_jecUp),
            ]
        self._vars_ttbar_2lss_withBDTv8_jecUp = self._vars_ttbar_2lss_jecUp + [
            MVAVar("BDTv8_eventReco_mvaValue := max(-0.2,BDTv8_eventReco_mvaValue)", func = lambda ev : max(-0.2,ev.BDTv8_eventReco_mvaValue_jecUp)),
            MVAVar("BDTv8_eventReco_bJet_fromHadTop_CSV := max(-0.2,BDTv8_eventReco_bJet_fromHadTop_CSV)", func = lambda ev : max(-0.2,ev.BDTv8_eventReco_bJet_fromHadTop_CSV_jecUp)),
            MVAVar("BDTv8_eventReco_HadTop_pT := max(-10,BDTv8_eventReco_HadTop_pT)", func = lambda ev : max(-10,ev.BDTv8_eventReco_HadTop_pT_jecUp)),
            MVAVar("BDTv8_eventReco_HadTop_mass := max(-10,BDTv8_eventReco_HadTop_mass)", func = lambda ev : max(-10,ev.BDTv8_eventReco_HadTop_mass_jecUp)),
            ]
        self._vars_ttV_2lss_jecUp = [ 
            MVAVar("max_Lep_eta:=max(abs(LepGood_eta[iF_Recl[0]]),abs(LepGood_eta[iF_Recl[1]]))", func = lambda ev : max(abs(ev.LepGood_eta[int(ev.iF_Recl[0])]),abs(ev.LepGood_eta[int(ev.iF_Recl[1])]))),
            MVAVar("numJets_float:=nJet25_Recl", func = lambda ev : ev.nJet25_Recl_jecUp),
            MVAVar("mindr_lep1_jet:=mindr_lep1_jet", func = lambda ev: ev.mindr_lep1_jet_jecUp),
            MVAVar("mindr_lep2_jet:=mindr_lep2_jet", func = lambda ev: ev.mindr_lep2_jet_jecUp),
            MVAVar("MT_met_lep1:=MT_met_lep1", func = lambda ev : ev.MT_met_lep1_jecUp),
            MVAVar("LepGood_conePt[iF_Recl[1]]:=LepGood_conePt[iF_Recl[1]]", func = lambda ev : ev.LepGood_conePt[int(ev.iF_Recl[1])]),
            MVAVar("LepGood_conePt[iF_Recl[0]]:=LepGood_conePt[iF_Recl[0]]", func = lambda ev : ev.LepGood_conePt[int(ev.iF_Recl[0])]),
            ]
        self._vars_ttbar_3l_jecUp = [ 
            MVAVar("max_Lep_eta:=max(abs(LepGood_eta[iF_Recl[0]]),abs(LepGood_eta[iF_Recl[1]]))", func = lambda ev : max(abs(ev.LepGood_eta[int(ev.iF_Recl[0])]),abs(ev.LepGood_eta[int(ev.iF_Recl[1])]))),
            MVAVar("numJets_float:=nJet25_Recl", func = lambda ev : ev.nJet25_Recl_jecUp),
            MVAVar("mindr_lep1_jet:=mindr_lep1_jet", func = lambda ev: ev.mindr_lep1_jet_jecUp),
            MVAVar("mindr_lep2_jet:=mindr_lep2_jet", func = lambda ev: ev.mindr_lep2_jet_jecUp),
            MVAVar("MT_met_lep1:=MT_met_lep1", func = lambda ev : ev.MT_met_lep1_jecUp),
            MVAVar("mhtJet25:=mhtJet25_Recl", func = lambda ev : ev.mhtJet25_Recl_jecUp),
            MVAVar("avg_dr_jet:=avg_dr_jet", func = lambda ev : ev.avg_dr_jet_jecUp),
            ]
        self._vars_ttV_3l_jecUp = [ 
            MVAVar("max_Lep_eta:=max(abs(LepGood_eta[iF_Recl[0]]),abs(LepGood_eta[iF_Recl[1]]))", func = lambda ev : max(abs(ev.LepGood_eta[int(ev.iF_Recl[0])]),abs(ev.LepGood_eta[int(ev.iF_Recl[1])]))),
            MVAVar("numJets_float:=nJet25_Recl", func = lambda ev : ev.nJet25_Recl_jecUp),
            MVAVar("mindr_lep1_jet:=mindr_lep1_jet", func = lambda ev: ev.mindr_lep1_jet_jecUp),
            MVAVar("mindr_lep2_jet:=mindr_lep2_jet", func = lambda ev: ev.mindr_lep2_jet_jecUp),
            MVAVar("MT_met_lep1:=MT_met_lep1", func = lambda ev : ev.MT_met_lep1_jecUp),
            MVAVar("LepGood_conePt[iF_Recl[2]]:=LepGood_conePt[iF_Recl[2]]", func = lambda ev : ev.LepGood_conePt[int(ev.iF_Recl[2])]),
            MVAVar("LepGood_conePt[iF_Recl[0]]:=LepGood_conePt[iF_Recl[0]]", func = lambda ev : ev.LepGood_conePt[int(ev.iF_Recl[0])]),
            ]

        self._vars_ttbar_2lss_jecDown = [ 
            MVAVar("max_Lep_eta:=max(abs(LepGood_eta[iF_Recl[0]]),abs(LepGood_eta[iF_Recl[1]]))", func = lambda ev : max(abs(ev.LepGood_eta[int(ev.iF_Recl[0])]),abs(ev.LepGood_eta[int(ev.iF_Recl[1])]))),
            MVAVar("numJets_float:=nJet25_Recl", func = lambda ev : ev.nJet25_Recl_jecDown),
            MVAVar("mindr_lep1_jet:=mindr_lep1_jet", func = lambda ev: ev.mindr_lep1_jet_jecDown),
            MVAVar("mindr_lep2_jet:=mindr_lep2_jet", func = lambda ev: ev.mindr_lep2_jet_jecDown),
            MVAVar("MT_met_lep1:=MT_met_lep1", func = lambda ev : ev.MT_met_lep1_jecDown),
            MVAVar("met:=min(met_pt, 400)", func = lambda ev : min(ev.met_jecDown_pt, 400)),
            MVAVar("avg_dr_jet:=avg_dr_jet", func = lambda ev : ev.avg_dr_jet_jecDown),
            ]
        self._vars_ttbar_2lss_withBDTv8_jecDown = self._vars_ttbar_2lss_jecDown + [
            MVAVar("BDTv8_eventReco_mvaValue := max(-0.2,BDTv8_eventReco_mvaValue)", func = lambda ev : max(-0.2,ev.BDTv8_eventReco_mvaValue_jecDown)),
            MVAVar("BDTv8_eventReco_bJet_fromHadTop_CSV := max(-0.2,BDTv8_eventReco_bJet_fromHadTop_CSV)", func = lambda ev : max(-0.2,ev.BDTv8_eventReco_bJet_fromHadTop_CSV_jecDown)),
            MVAVar("BDTv8_eventReco_HadTop_pT := max(-10,BDTv8_eventReco_HadTop_pT)", func = lambda ev : max(-10,ev.BDTv8_eventReco_HadTop_pT_jecDown)),
            MVAVar("BDTv8_eventReco_HadTop_mass := max(-10,BDTv8_eventReco_HadTop_mass)", func = lambda ev : max(-10,ev.BDTv8_eventReco_HadTop_mass_jecDown)),
            ]
        self._vars_ttV_2lss_jecDown = [ 
            MVAVar("max_Lep_eta:=max(abs(LepGood_eta[iF_Recl[0]]),abs(LepGood_eta[iF_Recl[1]]))", func = lambda ev : max(abs(ev.LepGood_eta[int(ev.iF_Recl[0])]),abs(ev.LepGood_eta[int(ev.iF_Recl[1])]))),
            MVAVar("numJets_float:=nJet25_Recl", func = lambda ev : ev.nJet25_Recl_jecDown),
            MVAVar("mindr_lep1_jet:=mindr_lep1_jet", func = lambda ev: ev.mindr_lep1_jet_jecDown),
            MVAVar("mindr_lep2_jet:=mindr_lep2_jet", func = lambda ev: ev.mindr_lep2_jet_jecDown),
            MVAVar("MT_met_lep1:=MT_met_lep1", func = lambda ev : ev.MT_met_lep1_jecDown),
            MVAVar("LepGood_conePt[iF_Recl[1]]:=LepGood_conePt[iF_Recl[1]]", func = lambda ev : ev.LepGood_conePt[int(ev.iF_Recl[1])]),
            MVAVar("LepGood_conePt[iF_Recl[0]]:=LepGood_conePt[iF_Recl[0]]", func = lambda ev : ev.LepGood_conePt[int(ev.iF_Recl[0])]),
            ]
        self._vars_ttbar_3l_jecDown = [ 
            MVAVar("max_Lep_eta:=max(abs(LepGood_eta[iF_Recl[0]]),abs(LepGood_eta[iF_Recl[1]]))", func = lambda ev : max(abs(ev.LepGood_eta[int(ev.iF_Recl[0])]),abs(ev.LepGood_eta[int(ev.iF_Recl[1])]))),
            MVAVar("numJets_float:=nJet25_Recl", func = lambda ev : ev.nJet25_Recl_jecDown),
            MVAVar("mindr_lep1_jet:=mindr_lep1_jet", func = lambda ev: ev.mindr_lep1_jet_jecDown),
            MVAVar("mindr_lep2_jet:=mindr_lep2_jet", func = lambda ev: ev.mindr_lep2_jet_jecDown),
            MVAVar("MT_met_lep1:=MT_met_lep1", func = lambda ev : ev.MT_met_lep1_jecDown),
            MVAVar("mhtJet25:=mhtJet25_Recl", func = lambda ev : ev.mhtJet25_Recl_jecDown),
            MVAVar("avg_dr_jet:=avg_dr_jet", func = lambda ev : ev.avg_dr_jet_jecDown),
            ]
        self._vars_ttV_3l_jecDown = [ 
            MVAVar("max_Lep_eta:=max(abs(LepGood_eta[iF_Recl[0]]),abs(LepGood_eta[iF_Recl[1]]))", func = lambda ev : max(abs(ev.LepGood_eta[int(ev.iF_Recl[0])]),abs(ev.LepGood_eta[int(ev.iF_Recl[1])]))),
            MVAVar("numJets_float:=nJet25_Recl", func = lambda ev : ev.nJet25_Recl_jecDown),
            MVAVar("mindr_lep1_jet:=mindr_lep1_jet", func = lambda ev: ev.mindr_lep1_jet_jecDown),
            MVAVar("mindr_lep2_jet:=mindr_lep2_jet", func = lambda ev: ev.mindr_lep2_jet_jecDown),
            MVAVar("MT_met_lep1:=MT_met_lep1", func = lambda ev : ev.MT_met_lep1_jecDown),
            MVAVar("LepGood_conePt[iF_Recl[2]]:=LepGood_conePt[iF_Recl[2]]", func = lambda ev : ev.LepGood_conePt[int(ev.iF_Recl[2])]),
            MVAVar("LepGood_conePt[iF_Recl[0]]:=LepGood_conePt[iF_Recl[0]]", func = lambda ev : ev.LepGood_conePt[int(ev.iF_Recl[0])]),
            ]

        memvars = [
            MVAVar("MEM_TTH := min(0,log(max(3.72e-44,MEM_TTH)))", func = lambda ev : min(0,log(max(3.72e-44,ev.MEM_TTH)))),
            MVAVar("MEM_TTW := min(0,log(max(3.72e-44,MEM_TTW)))", func = lambda ev : min(0,log(max(3.72e-44,ev.MEM_TTW)))),
            MVAVar("MEM_TTZ := min(0,log(max(3.72e-44,MEM_TTLL)))", func = lambda ev : min(0,log(max(3.72e-44,ev.MEM_TTLL)))),
            ]
        self._vars_ttV_3l_withMEM = self._vars_ttV_3l + memvars
        self._vars_ttV_3l_withMEM_jecUp = self._vars_ttV_3l_jecUp + memvars
        self._vars_ttV_3l_withMEM_jecDown = self._vars_ttV_3l_jecDown + memvars

        for var in self.systsJEC:

            self._MVAs["kinMVA_2lss_ttbar"+self.systsJEC[var]] = MVATool("2lss_ttbar"+self.systsJEC[var], weights%"2lss_ttbar", getattr(self,"_vars_ttbar_2lss"+self.systsJEC[var]), specs = self._specs)
            self._MVAs["kinMVA_2lss_ttbar_withBDTv8"+self.systsJEC[var]] = MVATool("2lss_ttbar_withBDTv8"+self.systsJEC[var], weights%"2lss_ttbar_withBDTv8", getattr(self,"_vars_ttbar_2lss_withBDTv8"+self.systsJEC[var]), specs = self._specs) if not self._skip_BDTv8 else self.put_minus_99
            self._MVAs["kinMVA_2lss_ttV"+self.systsJEC[var]] = MVATool("2lss_ttV"+self.systsJEC[var], weights%"2lss_ttV", getattr(self,"_vars_ttV_2lss"+self.systsJEC[var]), specs = self._specs)

            self._MVAs["kinMVA_3l_ttbar"+self.systsJEC[var]] = MVATool("3l_ttbar"+self.systsJEC[var], weights%"3l_ttbar", getattr(self,"_vars_ttbar_3l"+self.systsJEC[var]), specs = self._specs)
            self._MVAs["kinMVA_3l_ttV"+self.systsJEC[var]] = MVATool("3l_ttV"+self.systsJEC[var], weights%"3l_ttV", getattr(self,"_vars_ttV_3l"+self.systsJEC[var]), specs = self._specs)
            self._MVAs["kinMVA_3l_ttV_withMEM"+self.systsJEC[var]] = MVATool("3l_ttV_withMEM"+self.systsJEC[var], weights%"3l_ttV_withMEM", getattr(self,"_vars_ttV_3l_withMEM"+self.systsJEC[var]), specs = self._specs) if not self._skip_MEM else self.put_minus_99

        if self._skip_BDTv8: print 'WARNING: will set kinMVA_2lss_ttbar_withBDTv8 to dummy value (-99) as requested'
        if self._skip_MEM: print 'WARNING: will set kinMVA_3l_ttV_withMEM to dummy value (-99) as requested'

    def put_minus_99(self,event):
        return -99
    def listBranches(self):
        return self._MVAs.keys()
    def __call__(self,event):
        out = {}
        for name, mva in self._MVAs.iteritems():
            _mva = mva
            for i,j in self.systsJEC.iteritems():
                if j in name and not hasattr(event,"nJet"+j): _mva = self._MVAs[name.replace(j,"")]
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

