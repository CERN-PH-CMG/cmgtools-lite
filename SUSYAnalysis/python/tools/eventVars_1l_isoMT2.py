from CMGTools.TTHAnalysis.treeReAnalyzer import *
from ROOT import TLorentzVector, TVector2, std
import ROOT
import time
import itertools
import PhysicsTools.Heppy.loadlibs
import array
import operator

ROOT.gInterpreter.GenerateDictionary("vector<TLorentzVector>","TLorentzVector.h;vector")

mt2wSNT = ROOT.heppy.mt2w_bisect.mt2w()

mt2obj = ROOT.heppy.Davismt2.Davismt2()


## CSV v2 (CSV-IVF)

# WP as defined in base btag_MediumWP
bTagWP = 0.800

# min dR between good lep and iso track 
minDR = 0.1

def getPhysObjectArray(j): # https://github.com/HephySusySW/Workspace/blob/72X-master/RA4Analysis/python/mt2w.py
    px = j.pt*cos(j.phi )
    py = j.pt*sin(j.phi )
    pz = j.pt*sinh(j.eta )
    E = sqrt(px*px+py*py+pz*pz) #assuming massless particles...
    return array.array('d', [E, px, py,pz])

class EventVars1L_isoMT2:

    def __init__(self):
        self.branches = [ "MT2W", "iso_had", "iso_pt","iso_MT2" ]

    def listBranches(self):
        return self.branches[:]

    def __call__(self,event,base):

        # output dict:
        ret = {}

        # get some collections from initial tree
        leps = [l for l in Collection(event,"LepGood","nLepGood")]
        jets = [j for j in Collection(event,"Jet","nJet")]
        trks = [j for j in Collection(event,"isoTrack","nisoTrack")]

        njet = len(jets); nlep = len(leps)

        # MET
        metp4 = ROOT.TLorentzVector(0,0,0,0)
        metp4.SetPtEtaPhiM(event.met_pt,event.met_eta,event.met_phi,event.met_mass)
        pmiss  =array.array('d',[event.met_pt * cos(event.met_phi), event.met_pt * sin(event.met_phi)] )

        ####################################
        # import output from previous step #
        #base = keyvals
        ####################################

        # get selected leptons
        tightLeps = []
        tightLepsIdx = base['tightLepsIdx']
        tightLeps = [leps[idx] for idx in tightLepsIdx]
        nTightLeps = len(tightLeps)

        # get selected jets
        centralJet30 = []
        centralJet30idx = base['Jets30Idx']
        centralJet30 = [jets[idx] for idx in centralJet30idx]
        nCentralJet30 = len(centralJet30)


        # B jets
        BJetMedium30 = []
        BJetMedium30idx = []
        NonBJetMedium30 = []
        for i,j in enumerate(centralJet30):
           if j.btagCSV>bTagWP:
               BJetMedium30.append(j)
               BJetMedium30idx.append(centralJet30idx[i])
           else:
               NonBJetMedium30.append(j)
                
        nBJetMedium30 = len(BJetMedium30)

        ##################################################################
        # The following variables need to be double-checked for validity #
        ##################################################################

        mt2w_values=[]

        if nTightLeps>=1:
            lep = getPhysObjectArray(tightLeps[0])
            if nBJetMedium30==0 and nCentralJet30>=3: #All combinations from the highest three light (or b-) jets
                consideredJets = [ getPhysObjectArray(jet) for jet in NonBJetMedium30[:3] ] # only throw arrays into the permutation business
                ftPerms = itertools.permutations(consideredJets, 2)
                for perm in ftPerms:
                    mt2wSNT.set_momenta(lep, perm[0], perm[1], pmiss)
                    mt2w_values.append(mt2wSNT.get_mt2w())
            elif nBJetMedium30==1 and nCentralJet30>=2: #All combinations from one b and the highest two light jets
                consideredJets = [ getPhysObjectArray(jet) for jet in NonBJetMedium30[:2] ] # only throw arrays into the permutation business
                consideredJets.append(getPhysObjectArray(BJetMedium30[0]))
                ftPerms = itertools.permutations(consideredJets, 2)
                for perm in ftPerms:
                    mt2wSNT.set_momenta(lep, perm[0], perm[1], pmiss)
                    mt2w_values.append(mt2wSNT.get_mt2w())
            elif nBJetMedium30==2:
                consideredJets = [ getPhysObjectArray(jet) for jet in BJetMedium30[:2] ] # only throw arrays into the permutation business
                ftPerms = itertools.permutations(consideredJets, 2)
                for perm in ftPerms:
                    mt2wSNT.set_momenta(lep, perm[0], perm[1], pmiss)
                    mt2w_values.append(mt2wSNT.get_mt2w())
            elif nBJetMedium30>=3: #All combinations from the highest three b jets
                consideredJets = [ getPhysObjectArray(jet) for jet in BJetMedium30[:3] ] # only throw arrays into the permutation business
                ftPerms = itertools.permutations(consideredJets, 2)
                for perm in ftPerms:
                    mt2wSNT.set_momenta(lep, perm[0], perm[1], pmiss)
                    mt2w_values.append(mt2wSNT.get_mt2w())

        if len(mt2w_values)>0:
            ret["MT2W"]=min(mt2w_values)
        else:
            ret["MT2W"]=-999

        # flag for iso track: 0,1,999 <-> leptonic , hadronic , undefined        
        ret["iso_had"]=999        
        ret["iso_pt"]=999        
        if (nTightLeps>=1) :
            if len(trks)==0:
                ret["iso_MT2"]=999        
            else:
                for i,t in enumerate(trks):
                    if tightLeps[0].charge == t.charge: continue
                    dR = t.p4().DeltaR(tightLeps[0].p4())
                    if minDR>dR: continue
                    ret["iso_had"]=1
                    if abs(t.pdgId)>10 and abs(t.pdgId)<14: # leptonic
                        ret["iso_had"]=0
                    p1=tightLeps[0].p4()
                    p2=t.p4()
                    a=array.array('d', [ p1.M(), p1.Px(), p1.Py() ])                    
                    b=array.array('d', [ p2.M(), p2.Px(), p2.Py() ])                    
                    c=array.array('d', [ metp4.M(), metp4.Px(), metp4.Py() ])                    
                    mt2obj.set_momenta( a, b, c )
                    mt2obj.set_mn(0)
                    ret["iso_MT2"]=mt2obj.get_mt2()
                    ret["iso_pt"]=p2.Pt()
                    break
            if ret["iso_had"]==999: ret["iso_MT2"]=999
        # return branches
        return ret

if __name__ == '__main__':
    from sys import argv
    file = ROOT.TFile(argv[1])
    tree = file.Get("tree")
    class Tester(Module):
        def __init__(self, name):
            Module.__init__(self,name,None)
            self.sf = EventVars1L()
        def analyze(self,ev):
            print "\nrun %6d lumi %4d event %d: leps %d" % (ev.run, ev.lumi, ev.evt, ev.nLepGood)
            print self.sf(ev)
    el = EventLoop([ Tester("tester") ])
    el.loop([tree], maxEvents = 50)
