from CMGTools.TTHAnalysis.treeReAnalyzer import *
from CMGTools.TTHAnalysis.tools.mvaTool import *

class KinMVA_2D_2lss_3l:
    def __init__(self, weights):
        self._MVAs = {}

        self._specs = [
            MVAVar("iF0 := iF_Recl_0", func = lambda ev : ev.iF_Recl[0]),
            MVAVar("iF1 := iF_Recl_1", func = lambda ev : ev.iF_Recl[1]),
            MVAVar("iF2 := iF_Recl_2", func = lambda ev : ev.iF_Recl[2]),
        ]

        self._vars_ttbar_2lss = [ 
                 MVAVar("max_Lep_eta:=max(abs(LepGood_eta[iF_Recl_0]),abs(LepGood_eta[iF_Recl_1]))", func = lambda ev : max(abs(ev.LepGood_eta[ev.iF_Recl[0]]),abs(ev.LepGood_eta[ev.iF_Recl[1]]))),
		 MVAVar("L_phi:=L_phi", func = lambda ev : ev.L_phi),
		 MVAVar("DR_l_b_medium2:=DR_l_b_medium2", func = lambda ev : ev.DR_l_b_medium2),
		 MVAVar("MT_met_lep1:=MT_met_lep1", func = lambda ev : ev.MT_met_lep1),
		 MVAVar("numJets_float:=nJet25_Recl", func = lambda ev : ev.nJet25_Recl),
		 MVAVar("mhtJet25:=mhtJet25_Recl", func = lambda ev : ev.mhtJet25_Recl),
        ]
        self._vars_ttV_2lss = [ 
		MVAVar("L_phi:=L_phi", func = lambda ev : ev.L_phi),
		MVAVar("DR_l_b_medium1:=DR_l_b_medium1", func = lambda ev : ev.DR_l_b_medium2),
		MVAVar("mindr_lep2_jet:=mindr_lep2_jet", func = lambda ev: ev.mindr_lep2_jet),
		MVAVar("numJets_float:=nJet25_Recl", func = lambda ev : ev.nJet25_Recl),
		MVAVar("max_Lep_eta:=max(abs(LepGood_eta[iF_Recl_0]),abs(LepGood_eta[iF_Recl_1]))", func = lambda ev : max(abs(ev.LepGood_eta[ev.iF_Recl[0]]),abs(ev.LepGood_eta[ev.iF_Recl[1]]))),
		MVAVar("met:=min(met_pt, 400)", func = lambda ev : min(ev.met_pt, 400)),
        ]
        
        self._vars_ttbar_3l = [ 
		MVAVar("avg_dr_jet:=avg_dr_jet", func = lambda ev : ev.avg_dr_jet),
		MVAVar("numJets_float:=nJet25_Recl", func = lambda ev : ev.nJet25_Recl),
		MVAVar("LepGood_pt[1]:=LepGood_pt[iF_Recl_1]", func = lambda ev : ev.LepGood_pt[ev.iF_Recl[1]]),
		MVAVar("max_Lep_eta:=max(abs(LepGood_eta[iF_Recl_0]),abs(LepGood_eta[iF_Recl_1]))", func = lambda ev : max(abs(ev.LepGood_eta[ev.iF_Recl[0]]),abs(ev.LepGood_eta[ev.iF_Recl[1]]))),
		MVAVar("L_phi:=L_phi", func = lambda ev : ev.L_phi),
		MVAVar("mindr_lep1_jet:=mindr_lep1_jet", func = lambda ev: ev.mindr_lep1_jet),
		MVAVar("mindr_lep2_jet:=mindr_lep2_jet", func = lambda ev: ev.mindr_lep2_jet),
        ]
        self._vars_ttV_3l = [ 
	        MVAVar("LepGood_pt[1]:=LepGood_pt[iF_Recl_1]", func = lambda ev : ev.LepGood_pt[ev.iF_Recl[1]]),
		MVAVar("max_Lep_eta:=max(abs(LepGood_eta[iF_Recl_0]),abs(LepGood_eta[iF_Recl_1]))", func = lambda ev : max(abs(ev.LepGood_eta[ev.iF_Recl[0]]),abs(ev.LepGood_eta[ev.iF_Recl[1]]))),
		MVAVar("L_phi:=L_phi", func = lambda ev : ev.L_phi),
		MVAVar("minMllAFSS:=minMllAFSS_Recl", func = lambda ev : ev.minMllAFSS_Recl),
		MVAVar("numJets_float:=nJet25_Recl", func = lambda ev : ev.nJet25_Recl),
        ]

	self._MVAs["kinMVA_2lss_ttbar"] = MVATool("2lss_ttbar", weights%"2lss_ttbar", self._vars_ttbar_2lss, specs = self._specs)
	self._MVAs["kinMVA_2lss_ttV"] = MVATool("2lss_ttV", weights%"2lss_ttV", self._vars_ttV_2lss, specs = self._specs)
	self._MVAs["kinMVA_3l_ttbar"] = MVATool("3l_ttbar", weights%"3l_ttbar", self._vars_ttbar_3l, specs = self._specs)
	self._MVAs["kinMVA_3l_ttV"] = MVATool("3l_ttV", weights%"3l_ttV", self._vars_ttV_3l, specs = self._specs)

    def listBranches(self):
        return self._MVAs.keys()
    def __call__(self,event):
        out = {}
        for name, mva in self._MVAs.iteritems():
            if '2lss' in name: out[name] = mva(event) if event.nLepFO_Recl>=2 else -99
            elif '3l' in name: out[name] = mva(event) if event.nLepFO_Recl>=3 else -99
        return out

if __name__ == '__main__':
    from sys import argv
    file = ROOT.TFile(argv[1])
    tree = file.Get("treeProducerSusyMultilepton")
    file = ROOT.TFile(argv[1])
    tree = file.Get("tree")
    tree.vectorTree = True
    tree.AddFriend("sf/t",argv[2]) # recleaner
    tree.AddFriend("sf/t",argv[3]) # kinvars
              
    class Tester(Module):
        def __init__(self, name):
            Module.__init__(self,name,None)
            self.sf = KinMVA_2D_2lss_3l(weights = './weights/%s_BDTG.weights.xml')
        def analyze(self,ev):
            print "\nrun %6d lumi %4d event %d: leps %d" % (ev.run, ev.lumi, ev.evt, ev.nLepGood)
            print self.sf(ev)
    el = EventLoop([ Tester("tester") ])
    el.loop([tree], maxEvents = 50)

