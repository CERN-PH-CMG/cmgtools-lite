#!/usr/bin/env python
import os.path, types
import ROOT

from array import array
from math import log, exp

from CMGTools.TTHAnalysis.treeReAnalyzer import Collection
from itertools import combinations
from PhysicsTools.HeppyCore.utils.deltar import deltaPhi


BTAGWP = 0.8 # 0.8 is for medium tags, might want to try others

class tHqEventVariableFriend:
    def __init__(self):
        self.branches = [] # (branchname, default value)
        self.branches.append(("maxEtaJet25", -99.9))

        #####added by jmonroy sep 2016

        self.branches.append(("nJet1", -99.9)) # number of jets with |eta|>1.0
        self.branches.append(("dEtaFwdJetBJet", -99.9)) # delta eta: max fwd jet and hardest bjet 
        self.branches.append(("dEtaFwdJetClosestLep",-99.9)) # delta eta: max fwd jet and closest lepton 
        self.branches.append(("dPhiHighestPtSSPair", -99.9)) # delta phi highest pt same sign lepton pair

    # add more here...

    def listBranches(self):
        """Return a list of branch names that are added"""
        return [bn for bn,_ in self.branches]

    def getJetCollection(self, event, jec_syst=""):
        """Get a jet collection, either default or systematic variations"""
        if not hasattr(event, "nJet"+jec_syst): jec_syst = ""
        jets      = [j for j in Collection(event, "Jet"    +jec_syst, "nJet"    +jec_syst)]
        jets_disc = [j for j in Collection(event, "DiscJet"+jec_syst, "nDiscJet"+jec_syst)]

        # Will have to use recleaned jets at some point:
        try:
            _ijets_list = getattr(event, "iJSel_%s%s" % (self.recllabel, jec_syst))
            return [(jets[ij] if ij>=0 else jets_disc[-ij-1]) for ij in _ijets_list]
        # For now just take the default
        except AttributeError:
            return jets

    def __call__(self, event):
        # Set up dictionary with default values
        ret = {k:v for k,v in self.branches}

        # Get some object collections
        jets    = self.getJetCollection(event, jec_syst="")
        fjets   = Collection(event, "JetFwd", "nJetFwd")

        # Additional collections (not needed so far):
        leptons = Collection(event, "LepGood", "nLepGood")

        sspairs = [(l1, l2) for l1, l2 in combinations(leptons, 2) if l1.pdgId*l2.pdgId > 0]

        dphi=-99.9
        
        if len(sspairs): 
            lep1,lep2= sorted(sspairs, key=lambda x:x[1],reverse=True)[0] #highest pt pair
            dphi=abs(deltaPhi(lep1.phi,lep2.phi)) 
            #print 'deltaPhi',dphi

        ret['dPhiHighestPtSSPair']=dphi

        bjets = [j for j in jets if j.btagCSV > BTAGWP]
        bjets.sort(key=lambda x:x.pt, reverse=True)

        # All non-btagged jets with pt > 25 GeV
        light_jets =  [j for j in jets  if (j.pt > 25. and j.btagCSV < BTAGWP)]
        light_jets += [j for j in fjets if (j.pt > 25. and j.btagCSV < BTAGWP)]
        light_jets.sort(key=lambda x:x.pt, reverse=True)

        # Get the most forward of these save its value
        if len(light_jets):
            maxjet = sorted(light_jets, key=lambda x:abs(x.eta), reverse=True)[0]
            ret['maxEtaJet25'] = abs(maxjet.eta)
            if len(bjets):
                ret['dEtaFwdJetBJet'] = abs(maxjet.eta - bjets[0].eta)

            detas = [abs(lep.eta - maxjet.eta) for lep in leptons]
            ret['dEtaFwdJetClosestLep'] = sorted(detas)[0]



        ret['nJet1'] = len([j for j in light_jets if abs(j.eta)>1.0]) 
    
        return ret
##################################################
# Test this friend producer like so:
# python tHqEventVariables.py tree.root

if __name__ == '__main__':
    from sys import argv
    treefile = ROOT.TFile.Open(argv[1])
    tree = treefile.Get("tree")
    tree.vectorTree = True
    print "... processing %s" % argv[1]

    try:
        friendfile = ROOT.TFile.Open(argv[2])
        friendtree = friendfile.Get("sf/t")
        tree.AddFriend(friendtree)
        print "... adding friend tree from %s" % argv[2]
    except IndexError:
        pass

    from CMGTools.TTHAnalysis.treeReAnalyzer import EventLoop, Module

    class Tester(Module):
        def __init__(self, name):
            Module.__init__(self,name,None)
            self.thqf = tHqEventVariableFriend()
            print "Adding these branches:", self.thqf.listBranches()

        def analyze(self,ev):
            print ("\nrun %6d lumi %4d event %d: jets %d, fwdJets %d, isdata=%d" %
                      (ev.run, ev.lumi, ev.evt, ev.nJet25, ev.nJetFwd, int(ev.isData)))
            ret = self.thqf(ev)

            print 'maxEtaJet25:', ret['maxEtaJet25']
            print 'nJet1:', ret['nJet1']
            print 'dEtaFwdJetBJet',ret['dEtaFwdJetBJet']
            print 'dEtaFwdJetClosestLep',ret['dEtaFwdJetClosestLep']
            print 'dPhiHighestPtSSPair', ret['dPhiHighestPtSSPair']
            # add additional printout here to make sure everything is consistent

        def done(self):
            pass

    T = Tester("tester")
    el = EventLoop([ T ])
    el.loop([tree], maxEvents = 10)
    T.done()
