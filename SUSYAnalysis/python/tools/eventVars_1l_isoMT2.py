from CMGTools.TTHAnalysis.treeReAnalyzer import *
from ROOT import TLorentzVector, TVector2, std
import ROOT
import time
import itertools
import PhysicsTools.Heppy.loadlibs
import array
import operator

ROOT.gInterpreter.GenerateDictionary("vector<TLorentzVector>","TLorentzVector.h;vector")
mt2obj = ROOT.heppy.Davismt2.Davismt2()

# min dR between good lep and iso track 
minDR = 0.1
# MT2 cuts for hadronic and leptonic veto tracks
hadMT2cut = 60
lepMT2cut = 80

def getPhysObjectArray(j): # https://github.com/HephySusySW/Workspace/blob/72X-master/RA4Analysis/python/mt2w.py
    px = j.pt*cos(j.phi )
    py = j.pt*sin(j.phi )
    pz = j.pt*sinh(j.eta )
    E = sqrt(px*px+py*py+pz*pz) #assuming massless particles...
    return array.array('d', [E, px, py,pz])

class EventVars1L_isoMT2:

    def __init__(self):
        self.branches = [ "iso_had", "iso_pt","iso_MT2","iso_Veto" ]

    def listBranches(self):
        return self.branches[:]

    def __call__(self,event,base):

        # output dict:
        ret = {}

        # get some collections from initial tree
        leps = [l for l in Collection(event,"LepGood","nLepGood")]
        trks = [j for j in Collection(event,"isoTrack","nisoTrack")]

        nlep = len(leps)

        # MET
        metp4 = ROOT.TLorentzVector(0,0,0,0)
        metp4.SetPtEtaPhiM(event.met_pt,event.met_eta,event.met_phi,event.met_mass)
        pmiss  =array.array('d',[event.met_pt * cos(event.met_phi), event.met_pt * sin(event.met_phi)] )

        ####################################
        # import output from previous step #
        #base = keyvals
        ####################################

        # get selected leptons
        tightLeps    = []
        tightLepsIdx = base['tightLepsIdx']
        tightLeps    = [leps[idx] for idx in tightLepsIdx]
        nTightLeps   = len(tightLeps)

        # flag for iso track: 0,1,999 <-> leptonic , hadronic , undefined        
        ret["iso_had"]  = 999        
        ret["iso_pt"]   = 999
        ret["iso_MT2"]  = 999
        ret["iso_Veto"] = False
        if (nTightLeps>=1) and len(trks)>=1:
            for i,t in enumerate(trks):
                # looking for opposite charged tracks
                if tightLeps[0].charge == t.charge: continue
                dR = t.p4().DeltaR(tightLeps[0].p4())
                if minDR>dR: continue
                p1=tightLeps[0].p4()
                p2=t.p4()
                a=array.array('d', [ p1.M(), p1.Px(), p1.Py() ])                    
                b=array.array('d', [ p2.M(), p2.Px(), p2.Py() ])                    
                c=array.array('d', [ metp4.M(), metp4.Px(), metp4.Py() ])                    
                mt2obj.set_momenta( a, b, c )
                mt2obj.set_mn(0)
                ret["iso_MT2"] = mt2obj.get_mt2()
                ret["iso_pt"]  = p2.Pt()
                # cuts on MT2 as defined above
                if abs(t.pdgId)>10 and abs(t.pdgId)<14:
                    ret["iso_had"] = 0  #leptonic
                    cut=lepMT2cut
                else: 
                    ret["iso_had"] = 1  #hadronic track
                    cut=hadMT2cut
                if ret["iso_MT2"]<=cut: ret["iso_Veto"]=True
                break
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
