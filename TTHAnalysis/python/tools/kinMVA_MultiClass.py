from CMGTools.TTHAnalysis.treeReAnalyzer import *
from CMGTools.TTHAnalysis.tools.mvaTool import *

class KinMVA_MultiClass:
    def __init__(self, weights):
        self._MVAs = {}

        self.systsJEC = {0:"", 1:"_jecUp", -1:"_jecDown"}
        self.catnames = ["ttH", "ttV", "ttbar"] # must be same order as given in training (classID)

        self._specs = [
            MVAVar("iF0 := iF_Recl[0]", func = lambda ev : ev.iF_Recl[0]),
            MVAVar("iF1 := iF_Recl[1]", func = lambda ev : ev.iF_Recl[1]),
            MVAVar("iF2 := iF_Recl[2]", func = lambda ev : ev.iF_Recl[2]),
            ]

        self._vars = [
            MVAVar("higher_Lep_eta := max(abs(LepGood_eta[iF_Recl[0]]),abs(LepGood_eta[iF_Recl[1]]))", func = lambda ev : max(abs(ev.LepGood_eta[int(ev.iF_Recl[0])]),abs(ev.LepGood_eta[int(ev.iF_Recl[1])]))),
            MVAVar("MT_met_lep1:=MT_met_lep1", func = lambda ev : ev.MT_met_lep1),
            MVAVar("numJets_float:=nJet25_Recl", func = lambda ev : ev.nJet25_Recl),
            MVAVar("mindr_lep1_jet:=mindr_lep1_jet", func = lambda ev: ev.mindr_lep1_jet),
            MVAVar("mindr_lep2_jet:=mindr_lep2_jet", func = lambda ev: ev.mindr_lep2_jet),
            MVAVar("LepGood_conePt[iF_Recl[0]]:=LepGood_conePt[iF_Recl[0]]", func = lambda ev : ev.LepGood_conePt[int(ev.iF_Recl[0])]),
            MVAVar("LepGood_conePt[iF_Recl[1]]:=LepGood_conePt[iF_Recl[1]]", func = lambda ev : ev.LepGood_conePt[int(ev.iF_Recl[1])]),
            MVAVar("avg_dr_jet : = avg_dr_jet", func = lambda ev : ev.avg_dr_jet),
            MVAVar("met := min(met_pt, 400)", func = lambda ev : ev.met_pt),
            ]

        self._vars_jecUp = [
            MVAVar("higher_Lep_eta := max(abs(LepGood_eta[iF_Recl[0]]),abs(LepGood_eta[iF_Recl[1]]))", func = lambda ev : max(abs(ev.LepGood_eta[int(ev.iF_Recl[0])]),abs(ev.LepGood_eta[int(ev.iF_Recl[1])]))),
            MVAVar("MT_met_lep1:=MT_met_lep1", func = lambda ev : ev.MT_met_lep1_jecUp),
            MVAVar("numJets_float:=nJet25_Recl", func = lambda ev : ev.nJet25_Recl_jecUp),
            MVAVar("mindr_lep1_jet:=mindr_lep1_jet", func = lambda ev: ev.mindr_lep1_jet_jecUp),
            MVAVar("mindr_lep2_jet:=mindr_lep2_jet", func = lambda ev: ev.mindr_lep2_jet_jecUp),
            MVAVar("LepGood_conePt[iF_Recl[0]]:=LepGood_conePt[iF_Recl[0]]", func = lambda ev : ev.LepGood_conePt[int(ev.iF_Recl[0])]),
            MVAVar("LepGood_conePt[iF_Recl[1]]:=LepGood_conePt[iF_Recl[1]]", func = lambda ev : ev.LepGood_conePt[int(ev.iF_Recl[1])]),
            MVAVar("avg_dr_jet : = avg_dr_jet", func = lambda ev : ev.avg_dr_jet),
            MVAVar("met := min(met_pt, 400)", func = lambda ev : ev.met_jecUp_pt),
            ]

        self._vars_jecDown = [
            MVAVar("higher_Lep_eta := max(abs(LepGood_eta[iF_Recl[0]]),abs(LepGood_eta[iF_Recl[1]]))", func = lambda ev : max(abs(ev.LepGood_eta[int(ev.iF_Recl[0])]),abs(ev.LepGood_eta[int(ev.iF_Recl[1])]))),
            MVAVar("MT_met_lep1:=MT_met_lep1", func = lambda ev : ev.MT_met_lep1_jecDown),
            MVAVar("numJets_float:=nJet25_Recl", func = lambda ev : ev.nJet25_Recl_jecDown),
            MVAVar("mindr_lep1_jet:=mindr_lep1_jet", func = lambda ev: ev.mindr_lep1_jet_jecDown),
            MVAVar("mindr_lep2_jet:=mindr_lep2_jet", func = lambda ev: ev.mindr_lep2_jet_jecDown),
            MVAVar("LepGood_conePt[iF_Recl[0]]:=LepGood_conePt[iF_Recl[0]]", func = lambda ev : ev.LepGood_conePt[int(ev.iF_Recl[0])]),
            MVAVar("LepGood_conePt[iF_Recl[1]]:=LepGood_conePt[iF_Recl[1]]", func = lambda ev : ev.LepGood_conePt[int(ev.iF_Recl[1])]),
            MVAVar("avg_dr_jet : = avg_dr_jet", func = lambda ev : ev.avg_dr_jet),
            MVAVar("met := min(met_pt, 400)", func = lambda ev : ev.met_jecDown_pt),
            ]

        for var in self.systsJEC:
            self._MVAs["kinMVA_2lss_MultiClass"+self.systsJEC[var]] = MVATool("2lss_MultiClass"+self.systsJEC[var], weights%"2lss", getattr(self,"_vars"+self.systsJEC[var]), specs = self._specs, nClasses=3)
            self._MVAs["kinMVA_3l_MultiClass"+self.systsJEC[var]] = MVATool("3l_MultiClass"+self.systsJEC[var], weights%"3l", getattr(self,"_vars"+self.systsJEC[var]), specs = self._specs, nClasses=3)

    def listBranches(self):
        return [ '%s_%s'%(i,self.catnames[j]) for i in self._MVAs.keys() for j in xrange(3)]
    def __call__(self,event):
        out = {}
        for name, mva in self._MVAs.iteritems():
            _mva = mva
            for i,j in self.systsJEC.iteritems():
                if j in name and not hasattr(event,"nJet"+j): _mva = self._MVAs[name.replace(j,"")]
            if '2lss' in name: x = _mva(event) if event.nLepFO_Recl>=2 else [-99]*3
            if '3l' in name: x = _mva(event) if event.nLepFO_Recl>=3 else [-99]*3
            for i in xrange(3):
                out['%s_%s'%(name,self.catnames[i])] = x[i]
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
            self.sf = KinMVA_MultiClass(weights = './weights/MultiClassICHEP16_%s_BDTG.weights.xml')
        def analyze(self,ev):
            print "\nrun %6d lumi %4d event %d: leps %d" % (ev.run, ev.lumi, ev.evt, ev.nLepGood)
            print self.sf(ev)
    el = EventLoop([ Tester("tester") ])
    el.loop([tree], maxEvents = 50)

