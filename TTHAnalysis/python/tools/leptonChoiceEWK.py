from CMGTools.TTHAnalysis.treeReAnalyzer import *
from CMGTools.TTHAnalysis.tools.leptonJetReCleaner import passTripleMllVeto,passMllTLVeto
from ROOT import TFile,TH1F
import copy, os
import array

ROOT.gROOT.LoadMacro(os.environ["CMSSW_BASE"]+"/src/PhysicsTools/Heppy/src/mt2_bisect.cc")
from ROOT import mt2_bisect


## FakeHisto
## ___________________________________________________________________
class FakeHisto:


    ## __init__
    ## _______________________________________________________________
    def __init__(self, accesspath):

        self.histo = Histo(accesspath)


    ## getFakeRate
    ## _______________________________________________________________
    def getFakeRate(self, lep, var = 0): 
        idx = 0 if abs(lep.pdgId) == 13 else 1
        return self.histo.readHisto(idx, var, lep.conePt, abs(lep.eta))


    ## getFakeTransfer
    ## _______________________________________________________________
    def getFakeTransfer(self, lep, var = 0):
        prob = self.getFakeRate(lep, var)
        return prob/(1 - prob)

## Histo
## ___________________________________________________________________
class Histo:

    ## __init__
    ## _______________________________________________________________
    def __init__(self, accessline):
        # format: [muonFilePath::histo[::upvar::downvar], electronFilePath::histo[::upvar::downvar]]
        # self.list[i][var] where list = mus or els, i = number of the histogram, var = 0 (central), +1 (up), -1 (down)

        self.accessHistos(accessline)


    ## accessHisto
    ## _______________________________________________________________
    def accessHisto(self, fullLine):
        e = {}
        s = fullLine.split("::")
        f = ROOT.TFile.Open(s[0], "read")
        e[0] = copy.deepcopy(f.Get(s[1]))
        if len(s) >= 3: e[1]  = copy.deepcopy(f.Get(s[2]))
        if len(s) >= 4: e[-1] = copy.deepcopy(f.Get(s[3]))
        f.Close()

        return e


    ## accessHistos
    ## _______________________________________________________________
    def accessHistos(self, fullList):
        self.mus = []
        self.els = []

        for i, entry in enumerate(fullList):
            for item in entry:
                if not item: continue
                e = self.accessHisto(item)

                if i == 0: self.mus.append(e)
                else     : self.els.append(e)


    ## readHisto
    ## _______________________________________________________________
    def readHisto(self, mu, idx, var, valx, valy, valz = 0):
        hist = self.mus[idx][var] if mu else self.els[idx][var]
        if hist.GetDimension() == 3:
            return hist.GetBinContent(max(1, min(hist.GetNbinsX(), hist.GetXaxis().FindBin(valx))),\
                                      max(1, min(hist.GetNbinsY(), hist.GetYaxis().FindBin(valy))),\
                                      max(1, min(hist.GetNbinsZ(), hist.GetZaxis().FindBin(valz))))
        return hist.GetBinContent(max(1, min(hist.GetNbinsX(), hist.GetXaxis().FindBin(valx))),\
                                  max(1, min(hist.GetNbinsY(), hist.GetYaxis().FindBin(valy)))) 


    ## readHistos
    ## _______________________________________________________________
    def readHistos(self, mu, var, valx, valy, valz = 0):
        value = 1.
        hists = self.mus if mu else self.els
        for idx in range(len(hists)): 
            value *= self.readHisto(mu, idx, var, valx, valy, valz)
        return value


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

        if   self.isSF                                           : self.target = 91.2
        elif abs(self.l1.pdgId) == 15 or abs(self.l2.pdgId) == 15: self.target = 60
        else                                                     : self.target = 50

        self.mll  = (self.l1.p4() + self.l2.p4()).M()
        self.diff = abs(self.target - self.mll)


## LeptonTriple
## ___________________________________________________________________
class LeptonTriple:


    ## __init__
    ## _______________________________________________________________
    def __init__(self, l1, l2, l3, FakeHisto = None, listOfFakes = [], systs = {}):
        self.l1 = l1
        self.l2 = l2
        self.l3 = l3

        self.collectOSpairs()
        self.OSLF  = [p for p in self.OS if not p.wTau]
        self.OSTF  = [p for p in self.OS if     p.wTau]
        self.OSSF  = [p for p in self.OS if     p.isSF]

        self.nOSLF = len(self.OSLF)
        self.nOSTF = len(self.OSTF)
        self.nOSSF = len(self.OSSF)

        self.setFakes()
        self.setBestPair()
        self.setAppWeight()


    ## collectOSpairs
    ## _______________________________________________________________
    def collectOSpairs(self, useTaus = False, needSF = True):
        leps    = [self.l1, self.l2, self.l3]
        self.OS = []       

        if self.l1.pdgId * self.l2.pdgId < 0: self.OS.append(OSpair(self.l1, self.l2))
        if self.l1.pdgId * self.l3.pdgId < 0: self.OS.append(OSpair(self.l1, self.l3))
        if self.l2.pdgId * self.l3.pdgId < 0: self.OS.append(OSpair(self.l2, self.l3))


    ## debug
    ## _______________________________________________________________
    def debug(self):
        oslist = [os.debug() for os in self.OS]
        return "LeptonTriple made up of (%3.1f, %d), (%3.1f, %d) and (%3.1f, %d)\nwith OSpairs:\n" % (self.l1.pt, self.l1.pdgId, self.l2.pt, self.l2.pdgId, self.l3.pt, self.l3.pdgId) + "\n".join(oslist)


    ## getL
    ## _______________________________________________________________
    def getL(self):
        buffer = []
        if abs(self.l1.pdgId) != 15: buffer.append(self.l1)
        if abs(self.l2.pdgId) != 15: buffer.append(self.l2)
        if abs(self.l3.pdgId) != 15: buffer.append(self.l3)
        return buffer


    ## getLeps
    ## _______________________________________________________________
    def getLeps(self):
        return [self.l1, self.l2, self.l3]


    ## getOSLF
    ## _______________________________________________________________
    def getOSLF(self):
        return [(p, p.l1, p.l2) for p in self.OSLF]


    ## getOSSF
    ## _______________________________________________________________
    def getOSSF(self):
        return [(p, p.l1, p.l2) for p in self.OSSF]


    ## getOSTF
    ## _______________________________________________________________
    def getOSTF(self):
        return [(p, p.l1, p.l2) for p in self.OSTF]


    ## getT
    ## _______________________________________________________________
    def getT(self):
        buffer = []
        if abs(self.l1.pdgId) == 15: buffer.append(self.l1)
        if abs(self.l2.pdgId) == 15: buffer.append(self.l2)
        if abs(self.l3.pdgId) == 15: buffer.append(self.l3)
        return buffer


    ## setAppWeight
    ## _______________________________________________________________
    def setAppWeight(self):
        self.appWeight = {}
        if self.nFakes == 1:
            for var in self.systs:
                self.appWeight[var] =   FakeHisto.read(self.fakes[0], var)
        elif self.nFakes == 2:
            for var in self.systs:
                self.appWeight[var] = - FakeHisto.read(self.fakes[0], var) \
                                      * FakeHisto.read(self.fakes[1], var)
        elif self.nFakes == 3:
            for var in self.systs:
                self.appWeight[var] =   FakeHisto.read(self.fakes[0], var) \
                                      * FakeHisto.read(self.fakes[1], var) \
                                      * FakeHisto.read(self.fakes[2], var) 


    ## setBestPair
    ## _______________________________________________________________
    def setBestPair(self):

        self.bestPair = None
        buffer = []
        if   self.nOSSF > 0: buffer = [(p.diff, p) for p in self.OSSF]
        elif self.nOSLF > 0: buffer = [(p.diff, p) for p in self.OSLF]
        else               : buffer = [(p.diff, p) for p in self.OSTF]

        if buffer:
            buffer.sort()
            self.bestPair = buffer[0][0]


    ## setFakes
    ## _______________________________________________________________
    def setFakes(self, listOfFakes = []):
        self.fakes  = filter(None, listOfFakes)
        self.nFakes = len(self.fakes)


    ## test
    ## _______________________________________________________________
    def test(self, leps):
        if len(leps) > 3: return False
        ll = [self.l1, self.l2, self.l3]
        return all([l in ll for l in leps])
            


## LeptonChoiceEWK
## ___________________________________________________________________
class LeptonChoiceEWK:


    ## __init__
    ## _______________________________________________________________
    def __init__(self, label, inputlabel, isFastSim=False, filePathFakeRate=None, filePathLeptonSFfull=None, filePathLeptonSFfast=None):

        self.mt2maker = mt2_bisect.mt2()

        self.label      = "" if (label in ["", None]) else ("_" + label)
        self.inputlabel = '_' + inputlabel
        self.isFastSim = isFastSim

        self.collectSysts()
        self.loadFakeRateHistos(filePathFakeRate)
        self.loadLeptonScaleFactorHistos(filePathLeptonSFfull, filePathLeptonSFfast)


    ## __call__
    ## _______________________________________________________________
    def __call__(self, event):

        self.resetMemory()
        self.checkEvent(event)
        self.collectObjects(event)
        self.collectTriples()
        self.countTriples()
        self.firstCategorization()
        self.categorizeEvent(event)
        return self.attachLabels()


    ## attachLabels
    ## _______________________________________________________________
    def attachLabels(self):
        ## attach labels and return branch variables

        fullret = {}
        for k,v in self.ret.iteritems(): 
            fullret[k + self.label] = v
        return fullret


    ## categorizeEvent
    ## _______________________________________________________________
    def categorizeEvent(self, event):

        if not self.triples: return

        self.findBestOSpair()
        self.findMtMin()

        for var in self.systs["JEC"]:
           self.fillMllMt(var)
           self.fillBR(event, var)
           self.fillSR(var)

        #self.fillTriggerSF(event) # flat uncertainty for now

        #for var in self.systs["LEPSF"]:
        #    self.fillLeptonSF(event)


    ## checkEvent
    ## _______________________________________________________________
    def checkEvent(self, event):

        if not hasattr(self, "checked_fastsim_data"):
            if self.isFastSim and event.isData: raise RuntimeError,'Running with isFastSim on data!'
            self.checked_fastsim_data = True


    ## collectObjects
    ## _______________________________________________________________
    def collectObjects(self, event):

        self.leps       = [l             for l  in Collection(event, "LepGood", "nLepGood")  ]
        for i, l in enumerate(self.leps): setattr(l, "trIdx", i)

        self.lepsl      = [self.leps[il] for il in list(getattr   (event, "iL"  + self.inputlabel))[0:int(getattr(event,"nLepLoose"+self.inputlabel))]]
        self.lepst      = [self.leps[il] for il in list(getattr   (event, "iT"  + self.inputlabel))[0:int(getattr(event,"nLepTight"+self.inputlabel))]]
        self.lepsfv     = [self.leps[il] for il in list(getattr   (event, "iFV" + self.inputlabel))[0:int(getattr(event,"nLepFOVeto"+self.inputlabel))] \
                                      if not il in list(getattr   (event, "iTV" + self.inputlabel))[0:int(getattr(event,"nLepTightVeto"+self.inputlabel))]]
        self.lepstv     = [self.leps[il] for il in list(getattr   (event, "iTV" + self.inputlabel))[0:int(getattr(event,"nLepTightVeto"+self.inputlabel))]]

        self.tausl      = [t             for t  in Collection(event, "TauSel" + self.inputlabel , "nTauSel" + self.inputlabel )]
        for i, l in enumerate(self.tausl): setattr(l, "trIdx", i)
        self.taust      = [t             for t in self.tausl if t.ewkId == 2]
        self.tausf      = self.taust # THESE ARE THE TAU FAKES, NEED TO BE CHANGED!

        self.alltight   = self.lepstv + self.taust

        self.lepsFO     = [self.leps[il] for il in list(getattr   (event, "iFV" + self.inputlabel))[0:int(getattr(event,"nLepFOVeto"+self.inputlabel))]]
        self.tausFO     = [t             for t in self.tausl if t.ewkId >= 1]
        self.lepSelFO   = self.lepsFO  + self.tausFO

        self.setAttributes(self.lepSelFO)
        self.lepSelFO   = sorted(self.lepSelFO , key = lambda x: x.conePt, reverse=True)

        self.ret["nLepSel"] = len(self.lepSelFO)
        for i, l in enumerate(self.lepSelFO):
            for var in ["pt", "eta", "phi", "mass", "conePt", "pdgId", "isTight", "mcMatchId", "mcPromptGamma"]:
                self.ret["LepSel_" + var][i] = getattr(l, var)
        
        for i, l in enumerate(self.leps ): setattr(l, "selIdx", self.lepSelFO.index(l) if l in self.lepSelFO else -1)
        for i, l in enumerate(self.tausl): setattr(l, "selIdx", self.lepSelFO.index(l) if l in self.lepSelFO else -1)

        self.met        = {}
        self.met[0]     = event.met_pt
        self.met[1]     = getattr(event, "met_jecUp_pt"  , event.met_pt)
        self.met[-1]    = getattr(event, "met_jecDown_pt", event.met_pt)

        self.metphi     = {}
        self.metphi[0]  = event.met_phi
        self.metphi[1]  = getattr(event, "met_jecUp_phi"  , event.met_phi)
        self.metphi[-1] = getattr(event, "met_jecDown_phi", event.met_phi)


    ## collectSysts
    ## _______________________________________________________________
    def collectSysts(self): 
        self.systs = {}       
        self.systs["FR"    ] = {0: "", 1: "_ewkUp"   , -1: "_ewkDown"  }
        self.systs["JEC"   ] = {0: "", 1: "_jecUp"   , -1: "_jecDown"  }
        self.systs["LEPSF" ] = {0: "", 1: "_lepSFUp" , -1: "_lepSFDown" , 2: "_lepSF_FS_Up" , -2: "_lepSF_FS_Down" }
        self.systs["TRIGSF"] = {0: "", 1: "_trigSFUp", -1: "_trigSFDown", 2: "_trigSF_FS_Up", -2: "_trigSF_FS_Down"}


    ## collectTriples
    ## _______________________________________________________________
    def collectTriples(self):
        ## encodes the logic of finding the three leptons in the event
        ## if we have TTT -> event only goes into SR
        ## if not, we look for all possible triples (c.f. findTriples())
        ## priority is given to the light flavor leptons, if less than 
        ## 3 are present (tight or fake), fill up with taus

        self.ret["nLep" ] = len(self.lepstv) + len(self.taust)
        self.ret["nL"   ] = len(self.lepstv)
        self.ret["nT"   ] = len(self.taust)

        ## for testing
        ## 3 light leptons tight
        self.triples     = []
        self.trueTriples = []
        self.triples = self.findTriples([], self.lepstv, self.lepstv, self.lepstv, bypassMV=False)

        if self.triples:
            self.ret["isTight"] = True
            self.trueTriples    = self.triples
            return

        ## 2 light leptons tight + 1 tau tight
        self.triples = self.findTriples([], self.lepstv, self.lepstv, self.taust, bypassMV=False)

        if self.triples:
            self.ret["isTight"] = True
            self.trueTriples   = self.triples
            return

        ## 1 light leptons tight + 2 tau tight
        self.triples = self.findTriples([], self.lepstv, self.taust, self.taust, bypassMV=False)

        if self.triples:
            self.ret["isTight"] = True
            self.trueTriples   = self.triples
            return



        return


        nLep = self.ret["nLep" ]
        nL   = self.ret["nL"   ]
        nT   = self.ret["nT"   ]
       
        if nL < 3: return

        return

        ## light flavor
        if categ < 2: 

            ## 3 light leptons tight
            self.triples     = []
            self.trueTriples = []
            self.triples = self.findTriples([], self.lepstv, self.lepstv, self.lepstv, bypassMV=False)

            if self.triples:
                self.ret["isTight"] = True
                self.trueTriples    = self.triples
                return

            ## 3 light leptons tight and fake
            tr1f = self.findTriples(self.triples, self.lepstv, self.lepstv, self.lepsfv, bypassMV=False, nF=1)
            tr2f = self.findTriples(self.triples, self.lepstv, self.lepsfv, self.lepsfv, bypassMV=False, nF=2)
            tr3f = self.findTriples(self.triples, self.lepsfv, self.lepsfv, self.lepsfv, bypassMV=False, nF=3)

            self.triples = tr1f + tr2f + tr3f

            if self.triples:
                self.ret["isFake" ] = True
                return

        ## 1 tau
        if categ < 5: 

            ## 2 light leptons tight + 1 tau tight
            self.triples = self.findTriples([], self.lepstv, self.lepstv, self.taust, bypassMV=False)

            if self.triples:
                self.ret["isTight"] = True
                self.trueTriples   = self.triples
                return


        ## 2 tau
        if categ >= 5:

            ## 1 light leptons tight + 2 tau tight
            self.triples = self.findTriples([], self.lepstv, self.taust, self.taust, bypassMV=False)

            if self.triples:
                self.ret["isTight"] = True
                self.trueTriples   = self.triples
                return


    ## countOSLF
    ## _______________________________________________________________
    def countOSLF(self):

        all = []; leps = []
        for t in self.triples:
            for p in t.getOSLF():
                if (p[1], p[2]) not in leps:
                    all.append(p[0]); leps.append((p[1], p[2]))
        return len(all)


    ## countOSSF
    ## _______________________________________________________________
    def countOSSF(self):

        all = []; leps = []
        for t in self.triples:
            for p in t.getOSSF():
                if not (p[1], p[2]) in leps:
                    all.append(p[0]); leps.append((p[1], p[2]))
        return len(all)


    ## countOSTF
    ## _______________________________________________________________
    def countOSTF(self):

        all = []; leps = []
        for t in self.triples:
            for p in t.getOSTF():
                if (p[1], p[2]) not in leps:
                    all.append(p[0]); leps.append((p[1], p[2]))
        return len(all)


    ## countTriples
    ## _______________________________________________________________
    def countTriples(self):

        self.ret["nTriples"] = len(self.triples)
        if self.ret["nTriples"] > 40: raise RuntimeError,'Too many lepton pairs'

        for i, t in enumerate(self.triples):
            for j, lep   in enumerate(t.getLeps()):
                self.ret["t" + str(j+1)][i] = (abs(lep.pdgId) == 15)
                self.ret["i" + str(j+1)][i] = lep.selIdx
            ## FIXME: add hasOSSF, hasOSLF, bestMll, nOSSF


    ## fillBR
    ## _______________________________________________________________
    def fillBR(self, event, var = 0):

        BR = 0
        if   self.met[var] >= 50 and getattr(event, "nBJetMedium25_Mini" + self.systs["JEC"][var], "nBJetMedium25_Mini") <= 0: BR = 1
        elif                         getattr(event, "nBJetMedium25_Mini" + self.systs["JEC"][var], "nBJetMedium25_Mini") <= 0: BR = 2
        self.ret["BR" + self.systs["JEC"][var]] = BR


    ## fillLeptonSF
    ## _______________________________________________________________
    def fillLeptonSF(self, event, t, i1, i2, i3, t1, t2, t3, var = 0):

        print "fixme"
        ## FIXME
        ##self.ret["leptonSF" + self.systs["LEPSF"][var]][t] = 1.;
        ##if event.isData: return

        ##lepsf = [1]*3
        ##for i, (idx, ist) in enumerate([(i1, t1), (i2, t2), (i3, t3)]):
        ##    if ist == 1: continue
        ##    idxs = 0 if abs(self.leps[idx].pdgId) == 13 else 1
        ##    lepsf[i] *= self.readHistos(self.leptonScaleFactorHistosFull[idxs], var, self.leps[idx].pt, abs(self.leps[idx].eta))

        ##    #FIXME: fast sim lepton SF not yet included
        ##    #if self.isFastSim:
        ##    #    sf    = self.readHistos(self.leptonScaleFactorHistosFast[idxs], var, self.leps[idx].pt,  abs(self.leps[idx].eta), event.nVert)
        ##    #    sferr = 0 # error ignored for now
        ##    #    err = sferr / sf
        ##    #    lepsf[i] *= sf
        ##    #    if   var ==  2: lepsf[i] *= (1+err)
        ##    #    elif var == -2: lepsf[i] *= (1-err)
        ##self.ret["leptonSF" + self.systs["LEPSF"][var]][t] = lepsf[0] * lepsf[1] * lepsf[2]


    ## fillMllMt
    ## _______________________________________________________________
    def fillMllMt(self, var = 0):

        self.ret["bestMll"] = self.bestOSPair.mll if self.bestOSPair else -1
        for var in self.systs["JEC"]:
            self.ret["bestMt" + self.systs["JEC"][var]] = self.mTmin[var]


    ## fillSR
    ## _______________________________________________________________
    def fillSR(self, var = 0):

        categ = self.ret["categ"]
        mll   = self.bestOSPair.mll if self.bestOSPair else -1
        mt    = self.mTmin[var]
        met   = self.met[var]

        SR = -1
        if   categ ==  1: SR = self.findSRcategA(mll, mt, met,   0) # category A
        elif categ ==  2: SR = self.findSRcategB(mll, mt, met,  36) # category B
        elif categ ==  3: SR = self.findSRcategA(mll, mt, met,  60) # category C
        elif categ ==  4: SR = self.findSRcategB(mll, mt, met,  96) # category D
        elif categ ==  5: SR = self.findSRcategB(mll, mt, met, 120) # category E
        elif categ ==  6: SR = 145                                  # category F
        elif categ ==  7: SR = self.findSRcategG(mll, mt, met, 145) # category G
        elif categ ==  8: SR = self.findSRcategG(mll, mt, met, 149) # category H
        elif categ ==  9: SR = self.findSRcategG(mll, mt, met, 153) # category I
        elif categ == 10: SR = self.findSRcategG(mll, mt, met, 157) # category J
        elif categ == 11: SR = self.findSRcategG(mll, mt, met, 161) # category K

        self.ret["SR" + self.systs["JEC"][var]] = SR


    ## fillTriggerSF
    ## _______________________________________________________________
    def fillTriggerSF(self, event, t, i1, i2, i3):

        print "fixme"
        ## FIXME
        ##self.ret["triggerSF"][t] = 1.
        ##if event.isData: return
        ##self.ret["triggerSF"][t] = triggerScaleFactorFullSim(self.leps[i1].pdgId, self.leps[i2].pdgId, \
        ##                                                     self.leps[i1].pt   , self.leps[i2].pt   , self.ht)
        ##if self.isFastSim:
        ##    self.ret["triggerSF"][t] *= FastSimTriggerEfficiency( self.ht, self.leps[i1].pt, self.leps[i1].pdgId, \
        ##                                                                   self.leps[i2].pt, self.leps[i2].pdgId)


    ## findBestOSpair
    ## _______________________________________________________________
    def findBestOSpair(self):

        self.bestOSPair = None
        all = []; leps = []

        # priority to SF
        for t in self.triples:
            for p in t.getOSSF():
                if (p[1], p[2]) not in leps:
                    all.append((p[0].diff, p[0])); leps.append((p[1], p[2]))
        if all:
            all.sort()
            self.bestOSPair = all[0][1]
            return # priority to SF!

        # light flavor OSOF
        for t in self.triples:
            for p in t.getOSLF():
                if (p[1], p[2]) not in leps:
                    all.append((p[0].diff, p[0])); leps.append((p[1], p[2]))
        if all:
            all.sort()
            self.bestOSPair = all[0][1]
            return # priority to LF!

        # tau flavor OSOF
        for t in self.triples:
            for p in t.getOSTF():
                if (p[1], p[2]) not in leps:
                    all.append((p[0].diff, p[0])); leps.append((p[1], p[2]))
        if all:
            all.sort()
            self.bestOSPair = all[0][1]


    ## findCateg
    ## _______________________________________________________________
    def findCateg(self):

        nLep  = self.ret["nLep"]
        nL    = self.ret["nL"] 
        nT    = self.ret["nT"] 

        nOSSF = self.ret["nOSSF"]
        nOSLF = self.ret["nOSLF"]
        nOSTF = self.ret["nOSTF"]

        categ = 0

        ## at least three leptons
        if nLep < 3: return categ

        ## TTW sync
        if   nL == 3: categ = 1
        elif nL == 2: categ = 2
        elif nL == 1: categ = 3
        return categ

        ## WZ sync
        if   nL == 3 and nOSSF >= 1: categ = 1
        else: categ = 2
        return categ

        ## final
        if   nLep == 3 and nT == 0 and nOSSF >= 1               : categ =  1 # A
        elif nLep == 3 and nT == 0 and nOSSF == 0               : categ =  2 # B
        elif nLep == 3 and nT == 1 and nOSSF >= 1               : categ =  3 # C
        elif nLep == 3 and nT == 1 and nOSSF == 0 and nOSLF == 1: categ =  4 # D
        elif nLep == 3 and nT == 1 and nOSLF == 0               : categ =  5 # E
        elif nLep == 3 and nT == 2                              : categ =  6 # F
        elif nLep >  3 and nT == 0 and nOSSF >= 2               : categ =  7 # G
        elif nLep >  3 and nT == 0 and nOSSF == 1               : categ =  8 # H
        elif nLep >  3 and nT == 0 and nOSSF == 0               : categ =  9 # I
        elif nLep >  3 and nT == 1 and nOSSF >= 1               : categ = 10 # J
        elif nLep >  3 and nT == 1 and nOSSF == 0               : categ = 11 # K

        return categ


    ## findMtMin
    ## _______________________________________________________________
    def findMtMin(self):

        self.mTmin = {}
        used = [self.bestOSPair.l1, self.bestOSPair.l2] if self.bestOSPair else []
        leps = []

        if len(used) == 2: 
            for t in self.triples:
                if not pairInTriple(self.bestOSPair, t): continue
                list = t.getLeps()
                list.remove(used[0]); list.remove(used[1])
                if len(list) == 1: leps.append(list[0])
        else:
            for l in self.alltight:
                if not l in used: leps.append(l) 

        for var in self.systs["JEC"]:
            buffer = [] 
            self.mTmin[var] = -1
            for l in leps:
                buffer.append(self.mtW(l, var))
            if len(buffer):
                buffer.sort()
                self.mTmin[var] = buffer[0]


    ## firstCategorization
    ## _______________________________________________________________
    def firstCategorization(self):

        self.ret["nOSSF"] = self.countOSSF()
        self.ret["nOSTF"] = self.countOSTF()
        self.ret["nOSLF"] = self.countOSLF()

        self.ret["categ"] = self.findCateg()


    ## findSRcategA
    ## _______________________________________________________________
    def findSRcategA(self, mll, mT, met, offset = 0): 
        ## category A: trilepton-0taus-1ossf

        SR = 0

        if 0 <= mll < 75:
            if     0 <= mT < 120 and  50 <= met < 100: SR =  1
            elif   0 <= mT < 120 and 100 <= met < 150: SR =  2
            elif   0 <= mT < 120 and 150 <= met < 200: SR =  3
            elif   0 <= mT < 120 and 200 <= met      : SR =  4
            elif 120 <= mT < 160 and  50 <= met < 100: SR =  5
            elif 120 <= mT < 160 and 100 <= met < 150: SR =  6
            elif 120 <= mT < 160 and 150 <= met < 200: SR =  7
            elif 120 <= mT < 160 and 200 <= met      : SR =  8
            elif 160 <= mT       and  50 <= met < 100: SR =  9
            elif 160 <= mT       and 100 <= met < 150: SR = 10
            elif 160 <= mT       and 150 <= met < 200: SR = 11
            elif 160 <= mT       and 200 <= met      : SR = 12
        elif 75 <= mll < 105:
            if     0 <= mT < 120 and  50 <= met < 100: SR = 13
            elif   0 <= mT < 120 and 100 <= met < 150: SR = 14
            elif   0 <= mT < 120 and 150 <= met < 200: SR = 15
            elif   0 <= mT < 120 and 200 <= met      : SR = 16
            elif 120 <= mT < 160 and  50 <= met < 100: SR = 17
            elif 120 <= mT < 160 and 100 <= met < 150: SR = 18
            elif 120 <= mT < 160 and 150 <= met < 200: SR = 19
            elif 120 <= mT < 160 and 200 <= met      : SR = 20
            elif 160 <= mT       and  50 <= met < 100: SR = 21
            elif 160 <= mT       and 100 <= met < 150: SR = 22
            elif 160 <= mT       and 150 <= met < 200: SR = 23
            elif 160 <= mT       and 200 <= met      : SR = 24
        elif 105 <= mll:
            if     0 <= mT < 120 and  50 <= met < 100: SR = 25
            elif   0 <= mT < 120 and 100 <= met < 150: SR = 26
            elif   0 <= mT < 120 and 150 <= met < 200: SR = 27
            elif   0 <= mT < 120 and 200 <= met      : SR = 28
            elif 120 <= mT < 160 and  50 <= met < 100: SR = 29
            elif 120 <= mT < 160 and 100 <= met < 150: SR = 30
            elif 120 <= mT < 160 and 150 <= met < 200: SR = 31
            elif 120 <= mT < 160 and 200 <= met      : SR = 32
            elif 160 <= mT       and  50 <= met < 100: SR = 33
            elif 160 <= mT       and 100 <= met < 150: SR = 34
            elif 160 <= mT       and 150 <= met < 200: SR = 35
            elif 160 <= mT       and 200 <= met      : SR = 36

        return SR + offset


    ## findSRcategB
    ## _______________________________________________________________
    def findSRcategB(self, mll, mT, met, offset = 0): 
        ## category B: trilepton-0taus-0ossf

        SR = 0

        if 0 <= mll < 100:
            if          mT < 120 and  50 <= met < 100: SR =  1
            elif        mT < 120 and 100 <= met < 150: SR =  2
            elif        mT < 120 and 150 <= met < 200: SR =  3
            elif        mT < 120 and 200 <= met      : SR =  4
            elif 120 <= mT < 160 and  50 <= met < 100: SR =  5
            elif 120 <= mT < 160 and 100 <= met < 150: SR =  6
            elif 120 <= mT < 160 and 150 <= met < 200: SR =  7
            elif 120 <= mT < 160 and 200 <= met      : SR =  8
            elif 160 <= mT       and  50 <= met < 100: SR =  9
            elif 160 <= mT       and 100 <= met < 150: SR = 10
            elif 160 <= mT       and 150 <= met < 200: SR = 11
            elif 160 <= mT       and 200 <= met      : SR = 12
        elif 100 <= mll:
            if          mT < 120 and  50 <= met < 100: SR = 13
            elif        mT < 120 and 100 <= met < 150: SR = 14 
            elif        mT < 120 and 150 <= met < 200: SR = 15
            elif        mT < 120 and 200 <= met      : SR = 16
            elif 120 <= mT < 160 and  50 <= met < 100: SR = 17
            elif 120 <= mT < 160 and 100 <= met < 150: SR = 18
            elif 120 <= mT < 160 and 150 <= met < 200: SR = 19
            elif 120 <= mT < 160 and 200 <= met      : SR = 20
            elif 160 <= mT       and  50 <= met < 100: SR = 21
            elif 160 <= mT       and 100 <= met < 150: SR = 22
            elif 160 <= mT       and 150 <= met < 200: SR = 23
            elif 160 <= mT       and 200 <= met      : SR = 24

            ## new
            #if          m < 100 and        mT < 120 and  50 <= met < 100: SR = 38
            #elif        m < 100 and        mT < 120 and 100 <= met      : SR = 39
            #elif        m < 100 and 120 <= mT       and  50 <= met      : SR = 40
            #elif 100 <= m       and        mT < 120 and  50 <= met < 100: SR = 41
            #elif 100 <= m       and        mT < 120 and 100 <= met      : SR = 42
            #elif 100 <= m       and 120 <= mT       and  50 <= met      : SR = 43

        return SR + offset


    ## findSRcategG
    ## _______________________________________________________________
    def findSRcategG(self, mll, mT, met, offset = 0): 
        ## category G: four lepton

        SR = 0

        if     0 <= met <  30: SR = 1
        elif  30 <= met <  50: SR = 2
        elif  50 <= met < 100: SR = 3
        elif 100 <= met      : SR = 4

        return SR + offset


    ## findTriples
    ## _______________________________________________________________
    def findTriples(self, already, leps1, leps2, leps3, bypassMV, nF = 0):
        ## produces a list of all valid 3lepton combinations in the event,
        ## ordered by pt (first one hardest), and also returns the list of
        ## fakes in the triple

        triples   = []
        tr_raw    = []
        tr_sorted = []
        fk_raw    = []
        fk_sorted = []
        pt_raw    = []
        pt_sorted = []

        ## collect all three lepton combinations
        for p in [(l1,l2,l3) for l1 in leps1 for l2 in leps2 for l3 in leps3 if l1!=l2 and l1!=l3 and l2!=l3]:
            if (p[0], p[1], p[2]) in tr_raw: continue
            tr_raw.append(p)
            if   nF == 1: fk_raw.append((None, None, p[2])); pt_raw.append((p[0].pt    , p[1].pt    , p[2].conePt))
            elif nF == 2: fk_raw.append((None, p[1], p[2])); pt_raw.append((p[0].pt    , p[1].conePt, p[2].conePt))
            elif nF == 3: fk_raw.append((p[0], p[1], p[2])); pt_raw.append((p[0].conePt, p[1].conePt, p[2].conePt))
            else        : fk_raw.append((None, None, None)); pt_raw.append((p[0].pt    , p[1].pt    , p[2].pt    ))

        ## sort them by pT (first one always the hardest)
        for i, l in enumerate(tr_raw):
            p = pt_raw[i]
            ls = sorted([[p[0], 0], [p[1], 1], [p[2], 2]], key = lambda x: x[0], reverse=True)
            np = (l[ls[0][1]], l[ls[1][1]], l[ls[2][1]])
            if np not in tr_sorted:
                tr_sorted.append((l        [ls[0][1]], l        [ls[1][1]], l        [ls[2][1]]))
                fk_sorted.append((fk_raw[i][ls[0][1]], fk_raw[i][ls[1][1]], fk_raw[i][ls[2][1]]))
                pt_sorted.append((p        [ls[0][1]], p        [ls[1][1]], p        [ls[2][1]]))

        ## selection: only keep the good ones
        for i,(l1, l2, l3) in enumerate(tr_sorted):
            if any([t.test([l1, l2, l3]) for t in already]): continue
            if any([t.test([l1, l2, l3]) for t in triples]): continue
            if not bypassMV and not passTripleMllVeto(l1, l2, l3, 0, 12, True): continue
            if passPtCutTriple(tr_sorted[i][0], tr_sorted[i][1], tr_sorted[i][2]):
                triples.append(LeptonTriple(l1, l2, l3, self.fakeHisto, fk_sorted[i], self.systs["FR"]))

        return triples


    ## listBranches
    ## _______________________________________________________________
    def listBranches(self):

        biglist = [
            ("nLep"      + self.label, "I"),
            ("nL"        + self.label, "I"),
            ("nT"        + self.label, "I"),
            ("nOSSF"     + self.label, "I"),
            ("nOSLF"     + self.label, "I"),
            ("nOSTF"     + self.label, "I"),
            ("categ"     + self.label, "I"),
            ("bestMll"   + self.label, "F"),
            ("isTight"   + self.label, "I"),
            ("isFake"    + self.label, "I"),

            ("nTriples"  + self.label, "I"),
            ("i1"        + self.label, "I", 40, "nTriples" + self.label),
            ("i2"        + self.label, "I", 40, "nTriples" + self.label),
            ("i3"        + self.label, "I", 40, "nTriples" + self.label),
            ("t1"        + self.label, "I", 40, "nTriples" + self.label),
            ("t2"        + self.label, "I", 40, "nTriples" + self.label),
            ("t3"        + self.label, "I", 40, "nTriples" + self.label),
            ("mll"       + self.label, "F", 40, "nTriples" + self.label),
            ("hasFake"   + self.label, "I", 40, "nTriples" + self.label),
            ("hasOSSF"   + self.label, "I", 40, "nTriples" + self.label),
            ("hasOSLF"   + self.label, "I", 40, "nTriples" + self.label)]
 
        biglist.append(("nLepSel"   + self.label, "I"))
        for var in ["pt", "eta", "phi", "mass", "conePt"]:
            biglist.append(("LepSel_" + var + self.label, "F", 20, "nLepSel" + self.label))
        for var in ["pdgId", "isTight", "mcMatchId", "mcPromptGamma", "trIdx"]:
            biglist.append(("LepSel_" + var + self.label, "I", 20, "nLepSel" + self.label))
 
        for var in self.systs["FR"]:
            biglist.append(("appWeight" + self.systs["FR"    ][var] + self.label, "F", 40, "nTriples" + self.label))
        for var in self.systs["LEPSF"]: 
            biglist.append(("leptonSF"  + self.systs["LEPSF" ][var] + self.label, "F", 40, "nTriples" + self.label))
        for var in self.systs["TRIGSF"]: 
            biglist.append(("triggerSF" + self.systs["TRIGSF"][var] + self.label, "F", 40, "nTriples" + self.label))
        for var in self.systs["JEC"]:
            biglist.append(("BR"      + self.systs["JEC"][var] + self.label, "I"))
            biglist.append(("SR"      + self.systs["JEC"][var] + self.label, "I"))
            biglist.append(("bestMt"  + self.systs["JEC"][var] + self.label, "F"))
            biglist.append(("mT"      + self.systs["JEC"][var] + self.label, "F", 40, "nTriples" + self.label))
            biglist.append(("mT2L"    + self.systs["JEC"][var] + self.label, "F"))
            biglist.append(("mT2T"    + self.systs["JEC"][var] + self.label, "F"))

        return biglist


    ## loadFakeRateHistos
    ## _______________________________________________________________
    def loadFakeRateHistos(self, accessLine):
        if not accessLine: return
        self.fakeHisto = FakeHisto(accessLine)


    ## loadLeptonScaleFactorHistos
    ## _______________________________________________________________
    def loadLeptonScaleFactorHistos(self, filePathsFull, filePathsFast):
        if not filePathsFull: return
        self.leptonScaleFactorHistosFull = Histo(filePathsFull)
        if not filePathsFast: return
        self.leptonScaleFactorHistosFast = Histo(filePathsFast)


    ## makeMt2
    ## _______________________________________________________________
    def makeMt2(self):

        if not self.mt2maker: return False

        for var in self.systs["JEC"]:
            for os in self.OS:
                if os.wTau: self.ret["mT2T" + self.systs["JEC"][var]] = self.mt2(os.l1, os.l2, var)
                else      : self.ret["mT2L" + self.systs["JEC"][var]] = self.mt2(os.l1, os.l2, var)


    ## mt  
    ## _______________________________________________________________
    def mt(self, pt1, pt2, phi1, phi2):
        return sqrt(2*pt1*pt2*(1-cos(phi1-phi2)))


    ## mt2
    ## _______________________________________________________________
    def mt2(self, obj1, obj2, var):

        vector_met  = array.array('d', [0, self.met[var]*cos(self.metphi[var]), self.met[var]*sin(self.metphi[var])])
        vector_obj1 = array.array('d', [obj1.mass, obj1.p4().Px(), obj1.p4().Py()])
        vector_obj2 = array.array('d', [obj2.mass, obj2.p4().Px(), obj2.p4().Py()])

        self.mt2maker.set_momenta(vector_obj1, vector_obj2, vector_met)
        self.mt2maker.set_mn(0)

        return self.mt2maker.get_mt2()
    
    
    ## mtW
    ## _______________________________________________________________
    def mtW(self, lep, var):
        return self.mt(lep.pt, self.met[var], lep.phi, self.metphi[var])


    ## resetMemory
    ## _______________________________________________________________
    def resetMemory(self):

        self.ret = {};

        self.ret["nLep"              ] = 0
        self.ret["nL"                ] = 0
        self.ret["nT"                ] = 0
        self.ret["nOSSF"             ] = 0
        self.ret["nOSLF"             ] = 0
        self.ret["nOSTF"             ] = 0
        self.ret["categ"             ] = 0
        self.ret["bestMll"           ] = 0
        self.ret["isTight"           ] = 0
        self.ret["isFake"            ] = 0

        self.ret["nTriples"          ] = 0
        self.ret["i1"                ] = [-1]*40
        self.ret["i2"                ] = [-1]*40
        self.ret["i3"                ] = [-1]*40
        self.ret["t1"                ] = [0]*40
        self.ret["t2"                ] = [0]*40
        self.ret["t3"                ] = [0]*40
        self.ret["mll"               ] = [0]*40
        self.ret["hasFake"           ] = [0]*40
        self.ret["hasOSSF"           ] = [0]*40
        self.ret["hasOSLF"           ] = [0]*40
 
        self.ret["nLepSel"] = 0
        for var in ["pt", "eta", "phi", "mass", "conePt"]:
            self.ret["LepSel_" + var] = [0.]*20
        for var in ["pdgId", "isTight", "mcMatchId", "mcPromptGamma", "trIdx"]:
            self.ret["LepSel_" + var] = [0]*20
 
        for var in self.systs["FR"]: 
            self.ret["appWeight" + self.systs["FR"    ][var]] = [0.]*40
        for var in self.systs["LEPSF"]: 
            self.ret["leptonSF"  + self.systs["LEPSF" ][var]] = [1.]*40
        for var in self.systs["TRIGSF"]: 
            self.ret["triggerSF" + self.systs["TRIGSF"][var]] = [1.]*40
        for var in self.systs["JEC"]:
            self.ret["BR"        + self.systs["JEC"   ][var]] = 0
            self.ret["SR"        + self.systs["JEC"   ][var]] = 0
            self.ret["bestMt"    + self.systs["JEC"   ][var]] = 0.
            self.ret["mT"        + self.systs["JEC"   ][var]] = [0.]*40
            self.ret["mT2L"      + self.systs["JEC"   ][var]] = 0.
            self.ret["mT2T"      + self.systs["JEC"   ][var]] = 0.


    ## setAttributes 
    ## _______________________________________________________________
    def setAttributes(self, lepSel):

        for i, l in enumerate(lepSel):
            if abs(l.pdgId) == 15:
                setattr(l, "conePt"       , l.pt               ) # FIXME: to be moved to recleaner once settled
                setattr(l, "isTight"      , (l.ewkId == 2)     )
                setattr(l, "mcMatchId"    , 1                  )
                setattr(l, "mcPromptGamma", 0                  )
                setattr(l, "trIdx"        , self.tausl.index(l))
            else:
                setattr(l, "isTight"      , (l in self.lepstv) )
                setattr(l, "mcMatchId"    , l.mcMatchId        )
                setattr(l, "mcPromptGamma", l.mcPromptGamma    )
                setattr(l, "trIdx"        , self.leps.index(l) )


    ### storeIdx
    ### _______________________________________________________________
    #def storeIdx(self, t, num):
    #    nL=sum([1 for i,l in enumerate(self.triples[t]) if not l.isTau and i < num])
    #    nT=sum([1 for i,l in enumerate(self.triples[t]) if     l.isTau and i < num])

    #    label = "li" + str(nL+1)
    #    if self.triples[t][num].isTau: label = "ti" + str(nT+1)
    #    self.ret[label][t] = self.triples[t][num].trIdx
    #    self.ret["t"+str(num+1)][t] = self.triples[t][num].isTau


    ## for debugging only
    ## _______________________________________________________________
    def testMt(self, min, max):
        mt = []
        for l in self.lepst:
            mt.append(self.mtW(l.pt, l.phi, 0))
        return any([min <= m < max for m in mt])

    def passTrigger(self):
        if self.ev.HLT_BIT_HLT_DoubleEle8_CaloIdM_TrackIdM_Mass8_PFHT300_v   == 1: return True
        if self.ev.HLT_BIT_HLT_Mu8_Ele8_CaloIdM_TrackIdM_Mass8_PFHT300_v     == 1: return True
        if self.ev.HLT_BIT_HLT_DoubleMu8_Mass8_PFHT300_v                     == 1: return True
        if self.ev.HLT_BIT_HLT_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v       == 1: return True
        if self.ev.HLT_BIT_HLT_Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL_v  == 1: return True
        if self.ev.HLT_BIT_HLT_Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v == 1: return True
        if self.ev.HLT_BIT_HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v             == 1: return True
        if self.ev.HLT_BIT_HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v           == 1: return True
        return False


## passPtCutTriple
## _______________________________________________________________
def passPtCutTriple(l1, l2, l3):

    leps = [l1, l2, l3]
    light = [l for l in leps if abs(l.pdgId) == 11 or abs(l.pdgId) == 13]
    tau   = [l for l in leps if abs(l.pdgId) == 15                      ]

    for t in tau:
        if t.pt < 20: return False

    for i,l in enumerate(light):
        if l.pt < 10: return False
        if i == 0:
            if l.pt < 20: return False
            continue
        if i == 1:
            if abs(l.pdgId) == 11 and l.pt < 15: return False
            continue
    return True 


## _susy3l_lepId_CBlooseMVA
## _______________________________________________________________
def _susy3l_lepId_CBlooseMVA(lep):
        if abs(lep.pdgId) == 13:
            if lep.pt <= 5: return False
            return True
        elif abs(lep.pdgId) == 11:
            if lep.pt <= 7: return False
            if not (lep.convVeto and lep.lostHits == 0): 
                return False
            if not lep.mvaIdSpring15 > -0.70+(-0.83+0.70)*(abs(lep.etaSc)>0.8)+(-0.92+0.83)*(abs(lep.etaSc)>1.479):
                return False
            if not _susy3l_idEmu_cuts(lep): return False
            return True
        return False


## _susy3l_lepId_CBloose
## _______________________________________________________________
def _susy3l_lepId_CBloose(lep):
        if abs(lep.pdgId) == 13:
            if lep.pt <= 5: return False
            return True
        elif abs(lep.pdgId) == 11:
            if lep.pt <= 7: return False
            if not (lep.convVeto and lep.lostHits <= 1): 
                return False
            if not lep.mvaIdSpring15 > -0.70+(-0.83+0.70)*(abs(lep.etaSc)>0.8)+(-0.92+0.83)*(abs(lep.etaSc)>1.479):
                return False
            if not _susy3l_idEmu_cuts(lep): return False
            return True
        return False


## _susy3l_idEmu_cuts
## _______________________________________________________________
def _susy3l_idEmu_cuts(lep):
    if (abs(lep.pdgId)!=11): return True
    if (lep.hadronicOverEm>=(0.10-0.03*(abs(lep.etaSc)>1.479))): return False
    if (abs(lep.dEtaScTrkIn)>=(0.01-0.002*(abs(lep.etaSc)>1.479))): return False
    if (abs(lep.dPhiScTrkIn)>=(0.04+0.03*(abs(lep.etaSc)>1.479))): return False
    if (lep.eInvMinusPInv<=-0.05): return False
    if (lep.eInvMinusPInv>=(0.01-0.005*(abs(lep.etaSc)>1.479))): return False
    if (lep.sigmaIEtaIEta>=(0.011+0.019*(abs(lep.etaSc)>1.479))): return False
    return True


## _susy3l_lepId_IPcuts
## _______________________________________________________________
def _susy3l_lepId_IPcuts(lep):
    if not (lep.sip3d<4): return False
    if not (abs(lep.dxy)<0.05): return False
    if not (abs(lep.dz)<0.1): return False
    return True


## _susy3l_lepIdx_IPcutsMVA
## _______________________________________________________________
def _susy3l_lepId_IPcutsMVA(lep):
    if not (lep.sip3d<8): return False
    if not (abs(lep.dxy)<0.05): return False
    if not (abs(lep.dz)<0.1): return False
    return True


## equalPairs
## _______________________________________________________________
def equalPairs(pair1, pair2):
    if pair1.l1 == pair2.l1 and pair1.l2 == pair2.l2: return True
    if pair1.l1 == pair2.l2 and pair1.l2 == pair2.l1: return True
    return False


## equalTriples
## _______________________________________________________________
def equalTriples(triple1, triple2):
    if triple1.l1 == triple2.l1 and triple1.l2 == triple2.l2 and triple1.l3 == triple2.l3: return True
    if triple1.l1 == triple2.l1 and triple1.l2 == triple2.l3 and triple1.l3 == triple2.l2: return True
    if triple1.l1 == triple2.l2 and triple1.l2 == triple2.l1 and triple1.l3 == triple2.l3: return True
    if triple1.l1 == triple2.l2 and triple1.l2 == triple2.l3 and triple1.l3 == triple2.l1: return True
    if triple1.l1 == triple2.l3 and triple1.l2 == triple2.l1 and triple1.l3 == triple2.l2: return True
    if triple1.l1 == triple2.l3 and triple1.l2 == triple2.l2 and triple1.l3 == triple2.l1: return True
    return False


## pairInTriple
## _______________________________________________________________
def pairInTriple(pair, triple):
    for pairs in triple.OS:
        if equalPairs(pair, pairs): return True
    return False



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

        
