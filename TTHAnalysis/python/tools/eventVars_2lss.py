from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection as NanoAODCollection 

from CMGTools.TTHAnalysis.treeReAnalyzer import Collection as CMGCollection
from CMGTools.TTHAnalysis.tools.nanoAOD.friendVariableProducerTools import declareOutput, writeOutput

from math import sqrt, cos
from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR
from PhysicsTools.Heppy.physicsobjects.Jet import _btagWPs

class EventVars2LSS(Module):
    def __init__(self, label="", recllabel='Recl', doSystJEC=True, variations=[]):
        self.namebranches = [ "mindr_lep1_jet",
                              "mindr_lep2_jet",
                              "mindr_lep3_jet",
                              "avg_dr_jet",
                              "MT_met_lep1",
                              "MT_met_lep2",
                              "MT_met_lep3",
                              'mbb_loose',
                              'mbb_medium',
                              'min_Deta_leadfwdJet_jet',
                              ]
        self.label = "" if (label in ["",None]) else ("_"+label)
        self.systsJEC = {0:"",\
                         1:"_jesTotalCorrUp"  , -1:"_jesTotalCorrDown",\
                         2:"_jesTotalUnCorrUp", -2: "_jesTotalUnCorrDown",\
                         3:"_jerUp", -3: "_jerDown",\
                     } if doSystJEC else {0:""}
        if len(variations): 
            self.systsJEC = {0:""}
            for i,var in enumerate(variations):
                self.systsJEC[i+1]   ="_%sUp"%var
                self.systsJEC[-(i+1)]="_%sDown"%var


        self.inputlabel = '_'+recllabel
        self.branches = []
        for var in self.systsJEC: self.branches.extend([br+self.label+self.systsJEC[var] for br in self.namebranches])
        if len(self.systsJEC) > 1: 
            self.branches.extend([br+self.label+'_unclustEnUp' for br in self.namebranches if 'met' in br])
            self.branches.extend([br+self.label+'_unclustEnDown' for br in self.namebranches if 'met' in br])
        self.branches.extend( ['drlep12','drlep13','drlep23', 'hasOSSF4l','hasOSSF3l','m4l'])

    # old interface (CMG)
    def listBranches(self):
        return self.branches[:]
    def __call__(self,event):
        return self.run(event, CMGCollection, "met")

    # new interface (nanoAOD-tools)
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        declareOutput(self, wrappedOutputTree, self.branches)
    def analyze(self, event):
        writeOutput(self, self.run(event, NanoAODCollection))
        return True

    # logic of the algorithm
    def run(self,event,Collection):
        allret = {}

        all_leps = [l for l in Collection(event,"LepGood")]
        nFO = getattr(event,"nLepFO"+self.inputlabel)
        chosen = getattr(event,"iLepFO"+self.inputlabel)
        leps = [all_leps[chosen[i]] for i in xrange(nFO)]
        if nFO >= 2: 
            allret['drlep12'] = deltaR(leps[0],leps[1])
        else: 
            allret['drlep12'] = 0 
        if nFO >= 3: 
            allret['drlep13'] = deltaR(leps[0],leps[2])
            allret['drlep23'] = deltaR(leps[1],leps[2])
        else:
            allret['drlep13'] = 0 
            allret['drlep23'] = 0 
        
        allret['hasOSSF3l'] = False
        allret['hasOSSF4l'] = False
        allret['m4l']       = -99
        if nFO >= 3:
            leps3 = [leps[0], leps[1], leps[2]]
            for l1 in leps3:
                for l2 in leps3: 
                    if l1 == l2: continue
                    if l1.pdgId * l2.pdgId > 0: continue
                    if abs(l1.pdgId) != abs(l2.pdgId): continue
                    allret['hasOSSF3l'] = True

        if nFO >= 4:
            allret['m4l'] = (leps[0].p4()+leps[1].p4()+leps[2].p4()+leps[3].p4()).M()
            leps4 = [leps[0], leps[1], leps[2], leps[3]]
            for l1 in leps4:
                for l2 in leps4: 
                    if l1 == l2: continue
                    if l1.pdgId * l2.pdgId > 0: continue
                    if abs(l1.pdgId) != abs(l2.pdgId): continue
                    allret['hasOSSF4l'] = True

        for var in self.systsJEC:
            # prepare output
            ret = dict([(name,0.0) for name in self.namebranches])
            _var = var
            if not hasattr(event,"nJet25"+self.systsJEC[var]+self.inputlabel): 
                _var = 0; 
            jets = [j for j in Collection(event,"JetSel"+self.inputlabel)]
            jetptcut = 25
            jets = filter(lambda x : getattr(x,'pt%s'%self.systsJEC[_var]) > jetptcut, jets)


            if getattr(event, 'nFwdJet%s_Recl'%self.systsJEC[_var]) > 0 and len(jets):
                ret['min_Deta_leadfwdJet_jet'] = min( [ abs( getattr(event, 'FwdJet1_eta%s_Recl'%self.systsJEC[_var]) - j.eta) for j in jets])
            else: 
                ret['min_Deta_leadfwdJet_jet'] = 0
                
            bmedium = filter(lambda x : x.btagDeepFlavB > _btagWPs["DeepFlav_%d_%s"%(event.year,"M")][1], jets)
            bloose  = filter(lambda x : x.btagDeepFlavB > _btagWPs["DeepFlav_%d_%s"%(event.year,"L")][1], jets)
            if len(bmedium) >1: 
                bmedium.sort(key = lambda x : getattr(x,'pt%s'%self.systsJEC[_var]), reverse = True)
                b1 = bmedium[0].p4()
                b2 = bmedium[1].p4()
                b1.SetPtEtaPhiM(getattr(bmedium[0],'pt%s'%self.systsJEC[_var]),bmedium[0].eta,bmedium[0].phi,bmedium[0].mass)
                b2.SetPtEtaPhiM(getattr(bmedium[1],'pt%s'%self.systsJEC[_var]),bmedium[1].eta,bmedium[1].phi,bmedium[1].mass)
                ret['mbb_medium'] = (b1+b2).M()
            if len(bloose) >1: 
                bloose.sort(key = lambda x : getattr(x,'pt%s'%self.systsJEC[_var]), reverse = True)
                b1 = bloose[0].p4()
                b2 = bloose[1].p4()
                b1.SetPtEtaPhiM(getattr(bloose[0],'pt%s'%self.systsJEC[_var]),bloose[0].eta,bloose[0].phi,bloose[0].mass)
                b2.SetPtEtaPhiM(getattr(bloose[1],'pt%s'%self.systsJEC[_var]),bloose[1].eta,bloose[1].phi,bloose[1].mass)
                ret['mbb_loose'] = (b1+b2).M()

            ### USE ONLY ANGULAR JET VARIABLES IN THE FOLLOWING!!!

            njet = len(jets); nlep = len(leps)
            # fill output
            if njet >= 1:
                ret["mindr_lep1_jet"] = min([deltaR(j,leps[0]) for j in jets]) if nlep >= 1 else 0;
                ret["mindr_lep2_jet"] = min([deltaR(j,leps[1]) for j in jets]) if nlep >= 2 else 0;
                ret["mindr_lep3_jet"] = min([deltaR(j,leps[2]) for j in jets]) if nlep >= 3 else 0;
            if njet >= 2:
                sumdr, ndr = 0, 0
                for i,j in enumerate(jets):
                    for i2,j2 in enumerate(jets[i+1:]):
                        ndr   += 1
                        sumdr += deltaR(j,j2)
                ret["avg_dr_jet"] = sumdr/ndr if ndr else 0;

            metName = 'METFixEE2017' if event.year == 2017 else 'MET'

            met = getattr(event,metName+"_pt"+self.systsJEC[_var])
            metphi = getattr(event,metName+"_phi"+self.systsJEC[_var])

            if nlep > 0:
                ret["MT_met_lep1"] = sqrt( 2*leps[0].conePt*met*(1-cos(leps[0].phi-metphi)) )
            if nlep > 1:
                ret["MT_met_lep2"] = sqrt( 2*leps[1].conePt*met*(1-cos(leps[1].phi-metphi)) )
            if nlep > 2:
                ret["MT_met_lep3"] = sqrt( 2*leps[2].conePt*met*(1-cos(leps[2].phi-metphi)) )

            if not _var and hasattr(event, '%s_pt_unclustEnUp'%metName):
                met_up = getattr(event,metName+"_pt_unclustEnUp")
                metphi_up = getattr(event,metName+"_phi_unclustEnUp")
                met_down = getattr(event,metName+"_pt_unclustEnDown")
                metphi_down = getattr(event,metName+"_phi_unclustEnDown")
                if nlep > 0:
                    allret["MT_met_lep1" + self.label + '_unclustEnUp'] = sqrt( 2*leps[0].conePt*met_up*(1-cos(leps[0].phi-metphi_up)) )
                    allret["MT_met_lep1" + self.label + '_unclustEnDown'] = sqrt( 2*leps[0].conePt*met_down*(1-cos(leps[0].phi-metphi_down)) )
                if nlep > 1:
                    allret["MT_met_lep2" + self.label + '_unclustEnUp'] = sqrt( 2*leps[1].conePt*met_up*(1-cos(leps[1].phi-metphi_up)) )
                    allret["MT_met_lep2" + self.label + '_unclustEnDown'] = sqrt( 2*leps[1].conePt*met_down*(1-cos(leps[1].phi-metphi_down)) )
                if nlep > 2:
                    allret["MT_met_lep3" + self.label + '_unclustEnUp'] = sqrt( 2*leps[2].conePt*met_up*(1-cos(leps[2].phi-metphi_up)) )
                    allret["MT_met_lep3" + self.label + '_unclustEnDown'] = sqrt( 2*leps[2].conePt*met_down*(1-cos(leps[2].phi-metphi_down)) )

            for br in self.namebranches:
                allret[br+self.label+self.systsJEC[_var]] = ret[br]
	 	
	return allret


if __name__ == '__main__':
    from sys import argv
    file = ROOT.TFile(argv[1])
    tree = file.Get("tree")
    tree.vectorTree = True
    tree.AddFriend("sf/t",argv[2])
    class Tester(Module):
        def __init__(self, name):
            Module.__init__(self,name,None)
            self.sf = EventVars2LSS('','Recl')
        def analyze(self,ev):
            print "\nrun %6d lumi %4d event %d: leps %d" % (ev.run, ev.lumi, ev.evt, ev.nLepGood)
            print self.sf(ev)
    el = EventLoop([ Tester("tester") ])
    el.loop([tree], maxEvents = 50)

        
