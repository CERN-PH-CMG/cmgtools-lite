from CMGTools.TTHAnalysis.treeReAnalyzer import *
from CMGTools.TTHAnalysis.tools.leptonJetReCleaner import passMllTLVeto, passTripleMllVeto
from ROOT import TFile,TH1F
import ROOT, copy, os
import array, math

if "mt2_bisect_cc.so" not in ROOT.gSystem.GetLibraries():
    if os.path.isdir('/pool/ciencias/' ):
        ROOT.gROOT.LoadMacro("/pool/ciencias/HeppyTrees/RA7/additionalReferenceCode/mt2_bisect.cpp")
        print "Loaded from Oviedo"
    elif os.path.isdir('/mnt/t3nfs01/'):
        ROOT.gROOT.LoadMacro("/mnt/t3nfs01/data01/shome/cheidegg/s/mT2code/mt2_bisect.cc")
        print "Loaded from PSI"
    else:
        ROOT.gROOT.LoadMacro("/afs/cern.ch/user/c/cheidegg/public/mT2code/mt2_bisect.cc")

from ROOT import mt2_bisect

# FIXME: additional variables were once written to the LepSel but now commented in order
# to keep the leptonBuilder from becoming too fat


## OSpair
## ___________________________________________________________________
class OSpair:

    ## __init__
    ## _______________________________________________________________
    def __init__(self, l1, l2):
        self.l1   = l1
        self.l2   = l2
        self.load()

    ## debug
    ## _______________________________________________________________
    def debug(self):
        add = "SF" if self.isSF else "OF"
        return "OSpair (%s, %3.1f) made up of (%3.1f, %d) and (%3.1f, %d)" % (add, self.mll, self.l1.pt, self.l1.pdgId, self.l2.pt, self.l2.pdgId)


    ## load
    ## _______________________________________________________________
    def load(self):

        self.isSF = False
        self.wTau = False

        if     self.l1.pdgId  ==          -self.l2.pdgId       : self.isSF = True
        if abs(self.l1.pdgId) == 15 or abs(self.l2.pdgId) == 15: self.wTau = True

        if   self.isSF                                           : self.target = 91
        elif abs(self.l1.pdgId) == 15 or abs(self.l2.pdgId) == 15: self.target = 60
        else                                                     : self.target = 50
  
        self.mll  = (self.l1.p4(self.l1.conePt) + self.l2.p4(self.l2.conePt)).M()
        self.mllR = (self.l1.p4()               + self.l2.p4()              ).M()
        self.diff = abs(self.target - self.mll)


    ## test
    ## _______________________________________________________________
    def test(self, leps):
        if len(leps) > 3: return False
        ll = [self.l1, self.l2, self.l3]
        return all([l in ll for l in leps])
            


## LeptonBuilderEWK
## ___________________________________________________________________
class LeptonBuilderEWK:


    ## __init__
    ## _______________________________________________________________
    def __init__(self, inputlabel):

        self.mt2maker = mt2_bisect.mt2()
        self.inputlabel = '_' + inputlabel

        self.systsJEC = {0: "", 1: "_jecUp"   , -1: "_jecDown"  }


    ## __call__
    ## _______________________________________________________________
    def __call__(self, event):

        self.resetMemory()
        self.collectObjects(event)
        self.analyzeTopology()
        self.writeLepSel()
        return self.ret


    ## analyzeTopology
    ## _______________________________________________________________
    def analyzeTopology(self):

        self.passCleverPtCut()
        if not self.passPtAndMll(): return
        
        self.ret["passPtMll"] = 1 # the sanity bit

        if len(self.lepSelFO)>=3: self.ret["is_3l"] = 1
        if len(self.lepSelFO)>=4: self.ret["is_4l"] = 1
        if len(self.lepSelFO)>=5: self.ret["is_5l"] = 1

        self.collectOSpairs(3)
        self.makeMass(3)
        self.makeMt2(3)
        self.findBestOSpair(3)
        self.findMtMin(3)
        self.findBestOSpair(3, "mllL", True , False)
        self.findMtMin(3, "L")
        self.findBestOSpair(3, "mllT", False, True )
        self.findMtMin(3, "T")

        self.collectOSpairs(4, True)
        self.makeMass(4)
        self.makeMt2(4)
        self.findBestOSpair(4)
        self.findMtMin(4)
        self.findBestOSpair(4, "mllL", True , False)
        self.findMtMin(4, "L")
        self.findBestOSpair(4, "mllT", False, True )
        self.findMtMin(4, "T")


    ## collectObjects
    ## _______________________________________________________________
    def collectObjects(self, event):

        ## light leptons
        self.leps       = [l             for l  in Collection(event, "LepGood", "nLepGood")  ]
        self.lepsFO     = [self.leps[il] for il in list(getattr   (event, "iF" + self.inputlabel))[0:int(getattr(event,"nLepFO"+self.inputlabel))]]
        self.lepsT      = [self.leps[il] for il in list(getattr   (event, "iT" + self.inputlabel))[0:int(getattr(event,"nLepTight"+self.inputlabel))]]

        ## taus
        self.goodtaus   = [t             for t  in Collection(event, "TauGood" , "nTauGood" )]
        self.disctaus   = [t             for t  in Collection(event, "TauOther", "nTauOther")]
        self.taus       = [t             for t  in Collection(event, "TauSel" + self.inputlabel , "nTauSel" + self.inputlabel )]
        for t in self.taus: t.conePt = t.pt
        self.tausFO     = self.taus

        ## FO, both flavors
        self.lepSelFO   = self.lepsFO  + self.tausFO
        self.setAttributes(event, self.lepSelFO, event.isData)
        self.lepSelFO.sort(key = lambda x: x.conePt, reverse=True)

        ## tight leptons, both flavors
        self.lepsTT = []
        for t in self.lepSelFO: 
            if not t.isTight: continue
            self.lepsTT.append(t)
 
        self.met        = {}
        self.met[0]     = event.met_pt
        self.met[1]     = getattr(event, "met_jecUp_pt"  , event.met_pt)
        self.met[-1]    = getattr(event, "met_jecDown_pt", event.met_pt)

        self.metphi     = {}
        self.metphi[0]  = event.met_phi
        self.metphi[1]  = getattr(event, "met_jecUp_phi"  , event.met_phi)
        self.metphi[-1] = getattr(event, "met_jecDown_phi", event.met_phi)

        self.metgen        = {}
        self.metgen[0]     = event.met_genPt if not event.isData else event.met_pt
        self.metgen[1]     = getattr(event, "met_jecUp_genPt"  , event.met_genPt if not event.isData else event.met_pt)
        self.metgen[-1]    = getattr(event, "met_jecDown_genPt", event.met_genPt if not event.isData else event.met_pt)

        self.metgenphi     = {}
        self.metgenphi[0]  = event.met_genPhi if not event.isData else event.met_phi
        self.metgenphi[1]  = getattr(event, "met_jecUp_genPhi"  , event.met_genPhi if not event.isData else event.met_phi)
        self.metgenphi[-1] = getattr(event, "met_jecDown_genPhi", event.met_genPhi if not event.isData else event.met_phi)

        self.OS = []

            
    ## collectOSpairs
    ## _______________________________________________________________
    def collectOSpairs(self, max, useBuffer = False, withTaus = False):
        ## useBuffer = True if you want to know the number of OSSF pairs
        ## useBuffer is only for OSSF pairs used

        self.OS = []
        for i in range(min(max, len(self.lepSelFO))):
            for j in range(i+1,min(max, len(self.lepSelFO))):
                ##if not withTaus and abs(self.lepSelFO[i].pdgId) == 15 and abs(self.lepSelFO[j].pdgId) == 15: continue # no SF tautau
                if useBuffer and abs(self.lepSelFO[i].pdgId) != abs(self.lepSelFO[j].pdgId): continue # if buffer then SF
                if self.lepSelFO[i].pdgId * self.lepSelFO[j].pdgId < 0: 
                    self.OS.append(OSpair(self.lepSelFO[i], self.lepSelFO[j]))

        ## loop over all pairs, only keep the best OSSF ones, and make sure that they do not overlap
        if useBuffer:
            self.OS.sort(key=lambda x: x.diff)
            buffer = self.OS
            self.OS = []
            used = []
            for os in buffer:
                if not os.l1 in used and not os.l2 in used:
                    self.OS.append(os)
                    used.append(os.l1); used.append(os.l2)

        self.ret["nOSSF_"  + str(max) + "l"] = self.countOSSF(max              )
        self.ret["nOSSFL_" + str(max) + "l"] = self.countOSSF(max, True , False)
        self.ret["nOSSFT_" + str(max) + "l"] = self.countOSSF(max, False, True )
        self.ret["nOSLF_"  + str(max) + "l"] = self.countOSLF(max              )
        self.ret["nOSTF_"  + str(max) + "l"] = self.countOSTF(max              )


    ## countOSLF
    ## _______________________________________________________________
    def countOSLF(self, max):
        return sum(1 if not os.wTau else 0 for os in self.OS)


    ## countOSTF
    ## _______________________________________________________________
    def countOSTF(self, max):
        return sum(1 if os.wTau else 0 for os in self.OS)


    ## countOSSF
    ## _______________________________________________________________
    def countOSSF(self, max, onlyLight = False, onlyTau = False):
        return sum(1 if os.isSF and (not onlyLight or not os.wTau) and (not onlyTau or os.wTau) else 0 for os in self.OS)


    ## countOSTF
    ## _______________________________________________________________
    def countOSTF(self, max):
        return sum(1 if os.wTau else 0 for os in self.OS)


    ## findBestOSpair
    ## _______________________________________________________________
    def findBestOSpair(self, max, name = "mll", onlyLight = False, onlyTaus = False):

        self.bestOSPair = None

        all = []
        for os in self.OS:
            if onlyLight and os.isSF and     os.wTau: continue
            if onlyTaus  and os.isSF and not os.wTau: continue
            all.append((0 if os.isSF else 1, os.diff, os)) # priority to SF, then difference to target

        if all:
            all.sort()
            self.bestOSPair = all[0][2]
            self.ret[name + "_" + str(max) + "l"] = self.bestOSPair.mll
            return

        self.ret[name + "_" + str(max) + "l"] = -1


    ## findMtMin
    ## _______________________________________________________________
    def findMtMin(self, max, name=""):

        self.mTmin = {}
        used = [self.bestOSPair.l1, self.bestOSPair.l2] if self.bestOSPair else []
        leps = []

        for i in range(min(max,len(self.lepSelFO))):
            if self.lepSelFO[i] in used: continue
            leps.append(self.lepSelFO[i])

        for var in self.systsJEC:
            bufferPF  = [] 
            bufferGEN = [] 
            for l in leps:
                bufferPF .append(self.mtW(l, var      ))
                bufferGEN.append(self.mtW(l, var, True))

            if len(bufferPF):
                bufferPF.sort()
                self.ret["mT"+name+"_" + str(max) + "l" + self.systsJEC[var]] = bufferPF[0]
            else:
                self.ret["mT"+name+"_" + str(max) + "l" + self.systsJEC[var]] = -1

            if len(bufferGEN):
                bufferGEN.sort()
                self.ret["mT"+name+"_" + str(max) + "l_gen" + self.systsJEC[var]] = bufferGEN[0]
            else:
                self.ret["mT"+name+"_" + str(max) + "l_gen" + self.systsJEC[var]] = -1


    ## findTau
    ## _______________________________________________________________
    def findTau(self, event, tau):
        #if not event.iTauSel_Mini: return None
        #idx = int(event.iTauSel_Mini)
        #if   idx > 0: return self.goodtaus[idx     ]
        #elif idx < 0: return self.disctaus[-1*idx+1]
        #return None
        idx = self.isIn(tau, self.goodtaus)
        if idx > -1: return self.goodtaus[idx]
        idx = self.isIn(tau, self.disctaus)
        if idx > -1: return self.disctaus[idx]
        return None


    ## isIn
    ## _______________________________________________________________
    def isIn(self, object, collection):
        delta = math.pow(10,-6)
        for i in range(len(collection)):
            it = collection[i]
            if abs(it.pt-object.pt) < delta and abs(it.eta-object.eta)<delta and abs(it.phi-object.phi)<delta and abs(it.mass-object.mass)<delta: return i
        return -1


    ## listBranches
    ## _______________________________________________________________
    def listBranches(self):

        biglist = [
            ("passPtMll"   , "I"),
            ("is_3l"       , "I"),
            ("is_4l"       , "I"),
            ("is_5l"       , "I"),
            ("nOSSF_3l"    , "I"),
            ("nOSSFL_3l"   , "I"),
            ("nOSSFT_3l"   , "I"),
            ("nOSLF_3l"    , "I"),
            ("nOSTF_3l"    , "I"),
            ("mll_3l"      , "F"),
            ("mllL_3l"     , "F"),
            ("mllT_3l"     , "F"),
            ("m3L"         , "F"),
            ("nOSSF_4l"    , "I"),
            ("nOSSFL_4l"   , "I"),
            ("nOSSFT_4l"   , "I"),
            ("nOSLF_4l"    , "I"),
            ("nOSTF_4l"    , "I"),
            ("mll_4l"      , "F"),
            ("mllL_4l"     , "F"),
            ("mllT_4l"     , "F"),
            ("m4L"         , "F")]

        biglist.append(("nOS"   , "I"))
        biglist.append(("mll"   , "F", 20, "nOS"))
        biglist.append(("mll_fl", "I", 20, "nOS"))
        biglist.append(("mll_i1", "I", 20, "nOS"))
        biglist.append(("mll_i2", "I", 20, "nOS"))

        biglist.append(("nLepSel"   , "I"))
        for var in ["pt", "eta", "phi", "mass", "conePt", "dxy", "dz", "sip3d", "miniRelIso", "relIso", "ptratio", "ptrel", "mva"]:
            biglist.append(("LepSel_" + var, "F", 4))
        for var in ["pdgId", "isTight", "mcMatchId", "mcMatchAny", "mcPromptGamma", "mcUCSX", "trIdx"]:
            biglist.append(("LepSel_" + var, "I", 4))
  
        for var in self.systsJEC:
            biglist.append(("mT_3l"       + self.systsJEC[var], "F"))
            biglist.append(("mTL_3l"      + self.systsJEC[var], "F"))
            biglist.append(("mTT_3l"      + self.systsJEC[var], "F"))
            biglist.append(("mT2L_3l"     + self.systsJEC[var], "F"))
            biglist.append(("mT2T_3l"     + self.systsJEC[var], "F"))
            biglist.append(("mT_4l"       + self.systsJEC[var], "F"))
            biglist.append(("mTL_4l"      + self.systsJEC[var], "F"))
            biglist.append(("mTT_4l"      + self.systsJEC[var], "F"))
            biglist.append(("mT2L_4l"     + self.systsJEC[var], "F"))
            biglist.append(("mT2T_4l"     + self.systsJEC[var], "F"))
            biglist.append(("mT_3l_gen"   + self.systsJEC[var], "F"))
            biglist.append(("mTL_3l_gen"  + self.systsJEC[var], "F"))
            biglist.append(("mTT_3l_gen"  + self.systsJEC[var], "F"))
            biglist.append(("mT2L_3l_gen" + self.systsJEC[var], "F"))
            biglist.append(("mT2T_3l_gen" + self.systsJEC[var], "F"))
            biglist.append(("mT_4l_gen"   + self.systsJEC[var], "F"))
            biglist.append(("mTL_4l_gen"  + self.systsJEC[var], "F"))
            biglist.append(("mTT_4l_gen"  + self.systsJEC[var], "F"))
            biglist.append(("mT2L_4l_gen" + self.systsJEC[var], "F"))
            biglist.append(("mT2T_4l_gen" + self.systsJEC[var], "F"))

        return biglist


    ## makeMass
    ## _______________________________________________________________
    def makeMass(self, max):
       
        if len(self.lepSelFO) < 3: return 
        sum = self.lepSelFO[0].p4()
        for i in range(1,min(max,len(self.lepSelFO))):
            sum += self.lepSelFO[i].p4()
        self.ret["m" + str(max) + "L"] = sum.M()


    ## makeMt2
    ## _______________________________________________________________
    def makeMt2(self, max):
        ## building two sets of MT2
        ## mT2L = two light flavor leptons from the OS pair (category C, D)
        ## mT2T = hardest light lepton and one tau (category E, F)

        if not self.mt2maker: return False

        anyPairs = []
        for i in range(min(max, len(self.lepSelFO))):
            for j in range(i+1,min(max, len(self.lepSelFO))):
                if abs(self.lepSelFO[i].pdgId) == 15 or abs(self.lepSelFO[j].pdgId) == 15:
                    anyPairs.append(OSpair(self.lepSelFO[i], self.lepSelFO[j]))

        mt2t = []
        mt2l = []
        for os in anyPairs:
            if os.wTau and abs(os.l1.pdgId) != 15 or  abs(os.l2.pdgId) != 15: mt2t.append((os.l1.pt+os.l2.pt, os))
        for os in self.OS:
            if             abs(os.l1.pdgId) != 15 and abs(os.l2.pdgId) != 15: mt2l.append((os.l1.pt+os.l2.pt, os))

        mt2t.sort(reverse=True) # we want the hardest leptons here! 
        mt2l.sort(reverse=True) # we want the hardest leptons here! 

        for var in self.systsJEC:
            if len(mt2t)>0: 
                self.ret["mT2T_" + str(max) + "l"     + self.systsJEC[var]] = self.mt2(mt2t[0][1].l1, mt2t[0][1].l2, var)
                self.ret["mT2T_" + str(max) + "l_gen" + self.systsJEC[var]] = self.mt2(mt2t[0][1].l1, mt2t[0][1].l2, var, True)
            if len(mt2l)>0: 
                self.ret["mT2L_" + str(max) + "l"     + self.systsJEC[var]] = self.mt2(mt2l[0][1].l1, mt2l[0][1].l2, var)
                self.ret["mT2L_" + str(max) + "l_gen" + self.systsJEC[var]] = self.mt2(mt2l[0][1].l1, mt2l[0][1].l2, var, True)


    ## mt  
    ## _______________________________________________________________
    def mt(self, pt1, pt2, phi1, phi2):
        return sqrt(2*pt1*pt2*(1-cos(phi1-phi2)))


    ## mt2
    ## _______________________________________________________________
    def mt2(self, obj1, obj2, var, useGenMet = False):
            
        vector_met     = array.array('d', [0, self.met[var]*cos(self.metphi[var]), self.met[var]*sin(self.metphi[var])])
        vector_obj1    = array.array('d', [obj1.mass, obj1.p4(obj1.conePt).Px(), obj1.p4(obj1.conePt).Py()])
        vector_obj2    = array.array('d', [obj2.mass, obj2.p4(obj2.conePt).Px(), obj2.p4(obj2.conePt).Py()])

        if useGenMet:
            vector_met = array.array('d', [0, self.metgen[var]*cos(self.metgenphi[var]), self.metgen[var]*sin(self.metgenphi[var])])

        self.mt2maker.set_momenta(vector_obj1, vector_obj2, vector_met)
        self.mt2maker.set_mn(0)

        return self.mt2maker.get_mt2()
    
    
    ## mtW
    ## _______________________________________________________________
    def mtW(self, lep, var, useGenMet = False):
        if useGenMet: return self.mt(lep.conePt, self.metgen[var], lep.phi, self.metgenphi[var])
        return self.mt(lep.conePt, self.met[var], lep.phi, self.metphi[var])


    ## passCleverPtCut
    ## _______________________________________________________________
    def passCleverPtCut(self):
        ## following Lesya's mail
        ## pT cut for muon at 25GeV if MuEG trigger fired
        ## selection is per lepton (e.g. reject muon if it doesn't pass)
        ## in following categories:
        ## - mu ee (3l: A and B)
        ## - mu etau (3l: D and E)
        ## - mu eee (4l: H)
        ## - mu ee tau (4l: I)
    
        if len(self.lepSelFO) < 3: return
        l1 = self.lepSelFO[0]
        l2 = self.lepSelFO[1]
        l3 = self.lepSelFO[2]
        l4 = None
        if len(self.lepSelFO) >= 4: 
            l4 = self.lepSelFO[3]
    
        if not (abs(l1.pdgId) == 13 and abs(l2.pdgId) == 11): return
    
        if (l4 == None                         and (abs(l3.pdgId) == 11 or abs(l3.pdgId) == 13)) or \
            (l4 != None and abs(l3.pdgId) == 11 and (abs(l4.pdgId) == 11 or abs(l4.pdgId) == 15)):
            if l1.conePt < 25:
                self.lepSelFO.pop(0)


    ## passPtAndMll
    ## _______________________________________________________________
    def passPtAndMll(self):
        ## we can throw away the event if the pt cut is not passed because we already take the three hardest leps
        if len(self.lepSelFO) >= 3: 
            l1 = self.lepSelFO[0]; l2 = self.lepSelFO[1]; l3 = self.lepSelFO[2] 
            if not (passTripleMllVeto(l1, l2, l3, 0, 12, True) and passPtCutTriple(l1, l2, l3)): return False
        if len(self.lepSelFO) >= 4:
            l4 = self.lepSelFO[3]
            if l4.conePt < 10 or not passMllTLVeto(l4, [l1,l2,l3], 0, 12, True): return False
        return True


    ## resetMemory
    ## _______________________________________________________________
    def resetMemory(self):

        self.ret = {};

        self.ret["passPtMll"            ] = 0
        self.ret["is_3l"                ] = 0
        self.ret["is_4l"                ] = 0
        self.ret["is_5l"                ] = 0
        self.ret["nOSSF_3l"             ] = 0
        self.ret["nOSSFL_3l"            ] = 0
        self.ret["nOSSFT_3l"            ] = 0
        self.ret["nOSLF_3l"             ] = 0
        self.ret["nOSTF_3l"             ] = 0
        self.ret["mll_3l"               ] = 0
        self.ret["mllL_3l"              ] = 0
        self.ret["mllT_3l"              ] = 0
        self.ret["m3L"                  ] = 0
        self.ret["nOSSF_4l"             ] = 0
        self.ret["nOSSFL_4l"            ] = 0
        self.ret["nOSSFT_4l"            ] = 0
        self.ret["nOSLF_4l"             ] = 0
        self.ret["nOSTF_4l"             ] = 0
        self.ret["mll_4l"               ] = 0
        self.ret["mllL_4l"              ] = 0
        self.ret["mllT_4l"              ] = 0
        self.ret["m4L"                  ] = 0

        self.ret["nOS"   ] = 0
        self.ret["mll"   ] = [0]*20
        self.ret["mll_fl"] = [0]*20
        self.ret["mll_i1"] = [-1]*20
        self.ret["mll_i2"] = [-1]*20

        self.ret["nLepSel"] = 0
        for var in ["pt", "eta", "phi", "mass", "conePt", "dxy", "dz", "sip3d", "miniRelIso", "relIso", "ptratio", "ptrel", "mva"]:
            self.ret["LepSel_" + var] = [0.]*20
        for var in ["pdgId", "isTight", "mcMatchId", "mcMatchAny", "mcPromptGamma", "mcUCSX", "trIdx"]:
            self.ret["LepSel_" + var] = [0 ]*20

        for var in self.systsJEC:
            self.ret["mT_3l"       + self.systsJEC[var]] = 0.
            self.ret["mTL_3l"      + self.systsJEC[var]] = 0.
            self.ret["mTT_3l"      + self.systsJEC[var]] = 0.
            self.ret["mT2L_3l"     + self.systsJEC[var]] = 0.  
            self.ret["mT2T_3l"     + self.systsJEC[var]] = 0. 
            self.ret["mT_4l"       + self.systsJEC[var]] = 0.
            self.ret["mTL_4l"      + self.systsJEC[var]] = 0.
            self.ret["mTT_4l"      + self.systsJEC[var]] = 0.
            self.ret["mT2L_4l"     + self.systsJEC[var]] = 0.  
            self.ret["mT2T_4l"     + self.systsJEC[var]] = 0. 
            self.ret["mT_3l_gen"   + self.systsJEC[var]] = 0.
            self.ret["mTL_3l_gen"  + self.systsJEC[var]] = 0.
            self.ret["mTT_3l_gen"  + self.systsJEC[var]] = 0.
            self.ret["mT2L_3l_gen" + self.systsJEC[var]] = 0.  
            self.ret["mT2T_3l_gen" + self.systsJEC[var]] = 0. 
            self.ret["mT_4l_gen"   + self.systsJEC[var]] = 0.
            self.ret["mTL_4l_gen"  + self.systsJEC[var]] = 0.
            self.ret["mTT_4l_gen"  + self.systsJEC[var]] = 0.
            self.ret["mT2L_4l_gen" + self.systsJEC[var]] = 0.  
            self.ret["mT2T_4l_gen" + self.systsJEC[var]] = 0. 


    ## setAttributes 
    ## _______________________________________________________________
    def setAttributes(self, event, lepSel, isData = False):

        for i, l in enumerate(lepSel): 
            if l in self.tausFO:
                tau = self.findTau(event, l)
                setattr(l, "pdgId"        , -1*15*tau.charge                      )
                setattr(l, "isTight"      , (l.reclTauId == 2)                    )
                setattr(l, "mcMatchId"    , 1                                     )
                setattr(l, "mcMatchAny"   , 0                                     )
                setattr(l, "mcPromptGamma", 0                                     )
                setattr(l, "mcUCSX"       , tau.mcUCSXMatchId if not isData else 0)
                setattr(l, "trIdx"        , self.taus.index(l)                    )
                setattr(l, "dxy"          , tau.dxy if not tau is None else 0   )
                setattr(l, "dz"           , tau.dz  if not tau is None else 0   )
                setattr(l, "sip3d"        , 0                                   )
                setattr(l, "miniRelIso"   , 0                                   )
                setattr(l, "relIso"       , 0                                   )
                setattr(l, "ptratio"      , 0                                   )
                setattr(l, "ptrel"        , 0                                   )
                setattr(l, "mva"          , tau.idMVAOldDMRun2 if not tau is None else 0 )
            else:
                setattr(l, "isTight"      , (l in self.lepsT  )                 )
                setattr(l, "mcMatchId"    , l.mcMatchId     if not isData else 1)
                setattr(l, "mcMatchAny"   , l.mcMatchAny    if not isData else 0)
                setattr(l, "mcPromptGamma", l.mcPromptGamma if not isData else 0)
                setattr(l, "mcUCSX"       , l.mcUCSXMatchId if not isData else 0)
                setattr(l, "trIdx"        , self.leps.index(l)                  )
                setattr(l, "dxy"          , l.dxy                               )
                setattr(l, "dz"           , l.dz                                )
                setattr(l, "sip3d"        , l.sip3d                             )
                setattr(l, "miniRelIso"   , l.miniRelIso                        )
                setattr(l, "relIso"       , l.relIso03                          )
                setattr(l, "ptratio"      , l.jetPtRatiov2                      )
                setattr(l, "ptrel"        , l.jetPtRelv2                        )
                setattr(l, "mva"          , l.mvaSUSY                           )


    ## writeLepSel
    ## _______________________________________________________________
    def writeLepSel(self):

        self.ret["nLepSel"] = len(self.lepSelFO)
        for i, l in enumerate(self.lepSelFO):
            if i == 4: break # only keep the first 4 entries
            for var in ["pt", "eta", "phi", "mass", "conePt", "dxy", "dz", "sip3d", "miniRelIso", "relIso", "ptratio", "ptrel", "mva"]:
                self.ret["LepSel_" + var][i] = getattr(l, var, 0)
            for var in ["pdgId", "isTight", "mcMatchId", "mcMatchAny", "mcPromptGamma", "mcUCSX", "trIdx"]:
                self.ret["LepSel_" + var][i] = int(getattr(l, var, 0))

        all = []
        for os in self.OS:
            all.append((0 if os.isSF else 1, 1 if os.wTau else 0, os.diff, os)) # priority to SF, then light, then difference to target
        if all:
            all.sort()
            self.ret["nOS"] = len(all)
            for i,os in enumerate(all):
                self.ret["mll"   ][i] = os[3].mll
                self.ret["mll_fl"][i] = abs(os[3].l1.pdgId)+abs(os[3].l2.pdgId)
                self.ret["mll_i1"][i] = self.lepSelFO.index(os[3].l1)
                self.ret["mll_i2"][i] = self.lepSelFO.index(os[3].l2)



## _susyEWK_tauId_CBloose
## _______________________________________________________________
def _susyEWK_tauId_CBloose(tau):
    return (tau.pt > 20 and abs(tau.eta)<2.3 and abs(tau.dxy)<1000 and abs(tau.dz)<0.2 and tau.idMVAOldDMRun2 >= 1 and tau.idDecayMode and tau.idAntiE >= 2)


## _susyEWK_tauId_CBtight
## _______________________________________________________________
def _susyEWK_tauId_CBtight(tau):
    if not _susyEWK_tauId_CBloose(tau): return False
    return (tau.idMVAOldDMRun2 >= 4)


## _susyEWK_lepId_CBloose
## _______________________________________________________________
def _susyEWK_lepId_CBloose(lep):
        if abs(lep.pdgId) == 13:
            if lep.pt <= 5: return False
            return True
        elif abs(lep.pdgId) == 11:
            if lep.pt <= 7: return False
            if not (lep.convVeto and lep.lostHits == 0): 
                return False
            if not lep.mvaIdSpring15 > -0.70+(-0.83+0.70)*(abs(lep.etaSc)>0.8)+(-0.92+0.83)*(abs(lep.etaSc)>1.479):
                return False
            if not _susyEWK_idEmu_cuts(lep): return False
            return True
        return False


## _susyEWK_idEmu_cuts
## _______________________________________________________________
def _susyEWK_idEmu_cuts(lep):
    if (abs(lep.pdgId)!=11): return True
    if (lep.hadronicOverEm>=(0.10-0.03*(abs(lep.etaSc)>1.479))): return False
    if (abs(lep.dEtaScTrkIn)>=(0.01-0.002*(abs(lep.etaSc)>1.479))): return False
    if (abs(lep.dPhiScTrkIn)>=(0.04+0.03*(abs(lep.etaSc)>1.479))): return False
    if (lep.eInvMinusPInv<=-0.05): return False
    if (lep.eInvMinusPInv>=(0.01-0.005*(abs(lep.etaSc)>1.479))): return False
    if (lep.sigmaIEtaIEta>=(0.011+0.019*(abs(lep.etaSc)>1.479))): return False
    return True


## _susyEWK_lepId_IPcuts
## _______________________________________________________________
def _susyEWK_lepId_IPcuts(lep):
    if not (lep.sip3d<8): return False
    if not (abs(lep.dxy)<0.05): return False
    if not (abs(lep.dz)<0.1): return False
    return True


## _susyEWK_lepId_MVAFO
## _______________________________________________________________
def _susyEWK_lepId_MVAFO(lep):
    if not _susyEWK_lepId_CBloose(lep): return False
    if not _susyEWK_lepId_IPcuts(lep): return False
    if not (lep.pt > 10 and (abs(lep.pdgId) == 11 or lep.mediumMuonID2016 > 0)): return False
    if _susyEWK_lepId_MVAmedium(lep): return True
    if not (lep.jetPtRatiov2 > 0.3 and lep.jetBTagCSV < 0.3 and (abs(lep.pdgId)!=11 or (abs(lep.eta)<1.479 and lep.mvaIdSpring15>0.0) or (abs(lep.eta)>1.479 and lep.mvaIdSpring15>0.3))): return False
    return True


## _susyEWK_lepId_MVAmedium
## _______________________________________________________________
def _susyEWK_lepId_MVAmedium(lep):
    if not _susyEWK_lepId_CBloose(lep): return False
    if not _susyEWK_lepId_IPcuts(lep): return False
    if lep.pt <= 10: return False
    if abs(lep.pdgId) == 13:
        return (lep.mvaSUSY>-0.20 and lep.mediumMuonID2016>0)
    elif abs(lep.pdgId)==11:
        return lep.mvaSUSY>0.5
    return False


## passPtCutTriple
## _______________________________________________________________
def passPtCutTriple(l1, l2, l3):

    leps = [l1, l2, l3]
    light = [l for l in leps if abs(l.pdgId) == 11 or abs(l.pdgId) == 13]
    tau   = [l for l in leps if abs(l.pdgId) == 15                      ]

    for t in tau:
        if t.conePt < 20: return False

    for i,l in enumerate(light):
        if l.conePt < 10: return False
        if i == 0:
            if abs(l.pdgId) == 11 and l.conePt < 25: return False
            if abs(l.pdgId) == 13 and l.conePt < 20: return False
            continue
        if i == 1:
            if abs(l.pdgId) == 11 and l.conePt < 15: return False
            continue
    return True




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

