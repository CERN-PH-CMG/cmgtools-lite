from CMGTools.TTHAnalysis.treeReAnalyzer import *
from ROOT import TFile,TH1F
import ROOT, copy, os
import array, math


# FIXME: additional variables were once written to the LepSel but now commented in order
# to keep the leptonBuilder from becoming too fat



## TauFakesBuilder
## ___________________________________________________________________
class TauFakesBuilder:


    ## __init__
    ## _______________________________________________________________
    def __init__(self, inputlabel):

        ###self.mt2maker = mt2_bisect.mt2()
        self.inputlabel = '_' + inputlabel

        # Why do I need specifically JEC? I need all syst, in principle. Why is the treatment different?
        self.systsJEC = {0: "", 1: "_jecUp"   , -1: "_jecDown"  }

        self.debug=0


    ## __call__
    ## _______________________________________________________________
    def __call__(self, event):

        if self.debug==1: print("Now reset memory")
        self.resetMemory()
        if self.debug==1: print("Now collect objects")
        self.collectObjects(event)
        if self.debug==1: print("Now write tau sel")
        self.writeFakeTaus()
        if self.debug==1: print("Now return")
        return self.ret



    ## collectObjects
    ## _______________________________________________________________
    def collectObjects(self, event):

        ## light leptons
        self.leps       = [l             for l  in Collection(event, "LepGood", "nLepGood")  ]

        ## taus
        self.inclusivetaus       = [t          for t  in Collection(event, "TauGood" , "nTauGood"  )]
        ############  self.inclusivetaus.extend( [t          for t  in Collection(event, "TauOther", "nTauOther" )] )
        self.tausFO = self.inclusivetaus
        # not sure I really need to define tausFO

        ## Non-tau-cleaned jets
        self.uncleanJets = [t            for t  in Collection(event, "Jet", "nJet")]
        # jetsc[var] = [j for j in Collection(event,"Jet"+self.systsJEC[_var],"nJet"+self.systsJEC[_var])]
        # jetsd[var] = [j for j in Collection(event,"DiscJet"+self.systsJEC[_var],"nDiscJet"+self.systsJEC[_var])]

        if self.debug==2: print("Now match jets with taus")

        self.matchJetWithTau()

        # Eventually have multiple selections.



    def deltaR(self, a, b):
        # Let's see if that works
        return a.deltaR(b)

    def matchJetWithTau(self):

        if self.debug==1: print "Full jets collection has length: ", len(self.uncleanJets)
        if self.debug==1: print "Full taus collection has length: ", len(self.tausFO)
        
        for ijet in range(len(self.uncleanJets)):
            jet = self.uncleanJets[ijet]
            jetIsMatched=False
            for itau in range(len(self.tausFO)):
                tau = self.tausFO[itau]
                if deltaR(jet, tau) < 0.3:
                    jetIsMatched=True
            if jetIsMatched:
                self.matchedJets.append(ijet)
            else:
                if self.debug==1: print "Appending jet with index ", ijet, " to the unmatchedJets array"
                self.unmatchedJets.append(ijet)

        if self.debug==1: print "Matched jets: ", len(self.matchedJets)
        if self.debug==1: print "Unmatched jets: ", len(self.unmatchedJets)

        if self.debug==4:
            if len(self.tausFO) != len(self.matchedJets):
                print "---------------------------------------------------------"
                print "Full jets collection has length: ", len(self.uncleanJets)
                print "Full taus collection has length: ", len(self.tausFO)
                print "Matched jets: ", len(self.matchedJets)
                print "Unmatched jets: ", len(self.unmatchedJets)


        return None

    ## findTau
    ## _______________________________________________________________
    def findTau(self, event, tau):
        #if not event.iTauSel_Mini: return None
        #idx = int(event.iTauSel_Mini)
        #if   idx > 0: return self.goodtaus[idx     ]
        #elif idx < 0: return self.disctaus[-1*idx+1]
        #return None
        idx = self.isIn(tau, self.inclusivetaus)
        if idx > -1: return self.inclusivetaus[idx]
        return None


    ## isIn
    ## _______________________________________________________________
    def isIn(self, object, collection):
        delta = math.pow(10,-6)
        if self.debug==2: print "Collection size", len(collection)
        for i in range(len(collection)):
            it = collection[i]
            if self.debug: print it
            if abs(it.pt-object.pt) < delta and abs(it.eta-object.eta)<delta and abs(it.phi-object.phi)<delta and abs(it.mass-object.mass)<delta: return i
        return -1


    ## listBranches
    ## _______________________________________________________________
    def listBranches(self):

        if self.debug==1: print "Creating branches"
        biglist = [

            ("nJetMatchedToTau_y", "I"),
            ("nJetMatchedToTau_n", "I"),
            ("JetMatchedToTau_y" , "F",  20, "nJetMatchedToTau_y"),
            ("JetMatchedToTau_n" , "F",  20, "nJetMatchedToTau_n")

            ]
        if self.debug==1: print " branch created"
        return biglist


    ## resetMemory
    ## _______________________________________________________________
    def resetMemory(self):

        self.matchedJets   = []
        self.unmatchedJets = []

        self.ret = {};

        self.ret["nJetMatchedToTau_y"   ] = 0
        self.ret["nJetMatchedToTau_n"   ] = 0
        self.ret["JetMatchedToTau_y"    ] = [0.]*20
        self.ret["JetMatchedToTau_n"    ] = [0.]*20




    ## writeFakeTaus
    ## _______________________________________________________________
    def writeFakeTaus(self):

        ### HERE MUST SAVE JETS

        if self.debug==2: print "len unmatchedJets: ", len(self.unmatchedJets)
        
        self.ret["nJetMatchedToTau_n"   ] = len(self.unmatchedJets)
        for iJet, iInd in enumerate(self.unmatchedJets):
            if self.debug==3: print "IJET: ", iJet, " IIND: ", iInd
            if self.debug==3: print "umatchedJets[", iJet, "] = ", self.unmatchedJets[iJet]
            if self.debug==3: print "control"
            self.ret[ "JetMatchedToTau_n" ][iJet] = self.unmatchedJets[iJet]

        if self.debug==2: print "len matchedJets: ", len(self.matchedJets)
        
        self.ret["nJetMatchedToTau_y"   ] = len(self.matchedJets)
        for iJet, iInd in enumerate(self.matchedJets):
            if self.debug==3: print "IJET: ", iJet, " IIND: ", iInd
            if self.debug==3: print "matchedJets[", iJet, "] = ", self.matchedJets[iJet]
            if self.debug==3: print "control"
            self.ret[ "JetMatchedToTau_y" ][iJet] = self.matchedJets[iJet]





## _susyEWK_tauId_CBloose
## _______________________________________________________________
def _susyEWK_tauId_CBloose(tau):
    return (tau.pt > 20 and abs(tau.eta)<2.3 and abs(tau.dxy)<1000 and abs(tau.dz)<0.2 and tau.idMVAOldDMRun2 >= 1 and tau.idDecayMode and tau.idAntiE >= 2 and tau.idAntiMu >= 1)


## _susyEWK_tauId_CBtight
## _______________________________________________________________
def _susyEWK_tauId_CBtight(tau):
    if not _susyEWK_tauId_CBloose(tau): return False
    return (tau.idMVAOldDMRun2 >= 4)

def _reclTauId(tau):
    return (1+_susyEWK_tauId_CBtight(tau))

if __name__ == '__main__':
    from sys import argv
    file = ROOT.TFile(argv[1])
    tree = file.Get("tree")
    tree.vectorTree = True
    class Tester(Module):
        def __init__(self, name):
            Module.__init__(self,name,None)
            self.sf1 = LeptonChoiceEWK("Old", 
                lambda lep : lep.relIso03 < 0.5, 
                lambda lep : lep.relIso03 < 0.1 and lep.sip3d < 4 and _susy2lss_lepId_CB(lep),
                cleanJet = lambda lep,jet,dr : (lep.pt > 10 and dr < 0.4))
            self.sf2 = LeptonChoiceEWK("PtRel", 
                lambda lep : lep.relIso03 < 0.4 or lep.jetPtRel > 5, 
                lambda lep : (lep.relIso03 < 0.1 or lep.jetPtRel > 14) and lep.sip3d < 4 and _susy2lss_lepId_CB(lep),
                cleanJet = lambda lep,jet,dr : (lep.pt > 10 and dr < 0.4))
            self.sf3 = LeptonChoiceEWK("MiniIso", 
                lambda lep : lep.miniRelIso < 0.4, 
                lambda lep : lep.miniRelIso < 0.05 and lep.sip3d < 4 and _susy2lss_lepId_CB(lep),
                cleanJet = lambda lep,jet,dr : (lep.pt > 10 and dr < 0.4))
            self.sf4 = LeptonChoiceEWK("PtRelJC", 
                lambda lep : lep.relIso03 < 0.4 or lep.jetPtRel > 5, 
                lambda lep : (lep.relIso03 < 0.1 or lep.jetPtRel > 14) and lep.sip3d < 4 and _susy2lss_lepId_CB(lep),
                cleanJet = lambda lep,jet,dr : (lep.pt > 10 and dr < 0.4 and not (lep.jetPtRel > 5 and lep.pt*(1/lep.jetPtRatio-1) > 25)))
            self.sf5 = LeptonChoiceEWK("MiniIsoJC", 
                lambda lep : lep.miniRelIso < 0.4, 
                lambda lep : lep.miniRelIso < 0.05 and lep.sip3d < 4 and _susy2lss_lepId_CB(lep),
                cleanJet = lambda lep,jet,dr : (lep.pt > 10 and dr < 0.4 and not (lep.jetDR > 0.5*10/min(50,max(lep.pt,200)) and lep.pt*(1/lep.jetPtRatio-1) > 25)))
        def analyze(self,ev):
            print "\nrun %6d lumi %4d event %d: leps %d" % (ev.run, ev.lumi, ev.evt, ev.nLepGood)
            print self.sf1(ev)
            print self.sf2(ev)
            print self.sf3(ev)
            print self.sf4(ev)
            print self.sf5(ev)
    el = EventLoop([ Tester("tester") ])
    el.loop([tree], maxEvents = 50)

