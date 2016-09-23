from CMGTools.TTHAnalysis.treeReAnalyzer import *
from CMGTools.TTHAnalysis.tools.leptonJetReCleaner import passMllTLVeto, passTripleMllVeto
from ROOT import TFile,TH1F
import copy, os

for extlib in ["triggerSF/triggerSF_fullsim_UCSx_v5_01.cc","leptonSF/lepton_SF_UCSx_v5_03.cc","triggerSF/FastSimTriggerEff.cc"]:
    if not extlib.endswith(".cc"): raise RuntimeError
    if "/%s"%extlib.replace(".cc","_cc.so") not in ROOT.gSystem.GetLibraries():
        ROOT.gROOT.LoadMacro(os.environ["CMSSW_BASE"]+"/src/CMGTools/TTHAnalysis/data/%s+"%extlib)
from ROOT import triggerScaleFactorFullSim
from ROOT import FastSimTriggerEfficiency

class LeptonChoiceRA7:

    # enum
    appl_Fakes = 0
    appl_Flips = 1
    appl_WZ    = 2


    ## __init__
    ## _______________________________________________________________
    def __init__(self, label, inputlabel, whichApplication, isFastSim=False, filePathFakeRate=None, filePathLeptonSFfull=None, filePathLeptonSFfast=None, filePathPileUp=None):

        self.counter = 0

        self.label      = "" if (label in ["", None]) else ("_" + label)
        self.inputlabel = '_' + inputlabel
        self.isFastSim = isFastSim

        if self.isFastSim:
            print '-'*15
            print 'WARNING: will apply trigger efficiency for FastSim'
            print '-'*15

        self.collectSysts()
        self.setApplication(whichApplication, filePathFakeRate)
        self.loadLeptonScaleFactorHistos(filePathLeptonSFfull, filePathLeptonSFfast)
        self.loadPileUpHisto(filePathPileUp)



    ## __call__
    ## _______________________________________________________________
    def __call__(self, event):

        self.ev = event
        self.checkEvent(event)
        self.collectObjects(event)
        self.resetMemory()
        self.collectTriples()
        self.categorizeEvent(event)
        return self.attachLabels()


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
        # format: [muonFilePath::histo[::upvar::downvar], electronFilePath::histo[::upvar::downvar]]
        # returns list[idx][i][var] where idx = 0 (mu) or 1 (el), i = number of the histogram, var = 0 (central), +1 (up), -1 (down)

        mus, els = [], []

        for i, entry in enumerate(fullList):
            for item in entry:
                if not item: continue
                e = self.accessHisto(item)

                if i == 0: mus.append(e)
                else     : els.append(e)

        return mus, els


    ## attachLabels
    ## _______________________________________________________________
    def attachLabels(self):
        ## attach labels and return branch variables

        fullret = {}
        for k,v in self.ret.iteritems(): 
            fullret[k + self.label] = v
        return fullret


    ## bestZ1TL
    ## _______________________________________________________________
    def bestZ1TL(self, lepsl, lepst, cut=lambda lep:True):
          ## returns the Mll, i1 and i2 of the lepton pair whose Mll is closest to mZ

          pairs = []
          for i1, l1 in enumerate(lepst):
            if not cut(l1): continue
            for i2, l2 in enumerate(lepsl):
                if not cut(l2): continue
                if l1 == l2: continue
                if l1.pdgId == -l2.pdgId:
                   mz = (l1.p4() + l2.p4()).M()
                   diff = abs(mz-91)
                   pairs.append( (diff,mz,i1,i2) )
          if len(pairs):
              pairs.sort()
              return (pairs[0][1], pairs[0][2], pairs[0][3])
          return (0., -1, -1)


    ## categorizeEvent
    ## _______________________________________________________________
    def categorizeEvent(self, event):

        self.fillVtxWeight(event, 0)

        if not self.triples: return

        #if len(self.trueTriples) < 1: return

        #printed = False
        for t in xrange(len(self.triples)):

            i1 = self.leps.index(self.triples[t][0])
            i2 = self.leps.index(self.triples[t][1])
            i3 = self.leps.index(self.triples[t][2])

            #self.fillTriggerSF(event, t, i1, i2, i3) # flat uncertainty for now

            for var in self.systs["LEPSF"]:
                self.fillLeptonSF(event, t, i1, i2, i3, var)

            for var in self.systs["JEC"]:
                self.fillOnZ(t, var)
                self.fillSR(t, var)

            self.fillJetQuantities(t, i1, i2, i3)
            self.fillAppWeights(t, i1, i2, i3)  

            # debugging and synching
            #if not printed and len(self.trueTriples) >=1 and self.passTrigger() and \
            #if not printed and self.passTrigger() and \
            #    (len(self.jets30) >= 2 and len(self.bJets30) >= 0 and  50 <= self.met[0] and  60 <= self.ht): 
            #    #vtxWeight*btagMediumSF_Mini*triggerSF_Loop*leptonSF_Loop
            #    #weight = self.ev.vtxWeight*self.ev.btagMediumSF_Mini*self.ret["leptonSF"][t]
            #    ll = []
            #    for i in range(len(self.trueTriples)):
            #        for l in self.trueTriples[i]:
            #            if not l in ll: ll.append(l)
            #    nels = sum([1 if abs(l.pdgId) == 11 else 0 for l in ll])
            #    nmus = sum([1 if abs(l.pdgId) == 13 else 0 for l in ll])
            #    appWeight = 0.
            #    for t in xrange(len(self.triples)): 
            #        appWeight += self.ret["appWeight"][t]
            #    lepsf = 1.
            #    for l in ll: 
            #        idx = 0 if abs(l.pdgId) == 13 else 1
            #        lepsf *= self.readHistos(self.leptonScaleFactorHistosFull[idx], var, l.pt, abs(l.eta))
            #    #print "%d %d %d %d %d %d %d %d %3.3f %3.3f %d" % (self.ev.run, self.ev.lumi, self.ev.evt, nmus, nels, 0, len(self.jets30), len(self.bJets30), self.met[0], self.ht, self.ret["isOnZ"])
            #    #print "%d %d %d %d %d %d %d %d %3.3f %3.3f %1.5f %1.5f %d %d %1.5f" % (self.ev.run, self.ev.lumi, self.ev.evt, nmus, nels, 0, len(self.jets30), len(self.bJets30), self.met[0], self.ht, self.ev.btagMediumSF_Mini, lepsf, self.ret["isOnZ"], (not self.ret["hasTTT"]), appWeight)
            #    print "%d %d %d %d %d %d %d %d %3.3f %3.3f %1.5f %1.5f %1.5f %1.5f %d %d %1.5f" % (self.ev.run, self.ev.lumi, self.ev.evt, nmus, nels, 0, len(self.jets30), len(self.bJets30), self.met[0], self.ht, self.ev.genWeight, self.ret["vtxWeight"], self.ev.btagMediumSF_Mini, lepsf, self.ret["isOnZ"], (len(self.trueTriples) < len(self.triples)), appWeight)
            #    #print "%d %d %d %d %d %d %d %d %3.3f %3.3f %1.5f %1.5f %1.5f %1.5f %d" % (self.ev.run, self.ev.lumi, self.ev.evt, nmus, nels, 0, len(self.jets30), len(self.bJets30), self.met[0], self.ht, self.ev.genWeight, self.ev.vtxWeight, self.ev.btagMediumSF_Mini, self.ret["leptonSF"][t], self.ret["isOnZ"])
            #    printed = True


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
        self.lepsl      = [self.leps[il] for il in getattr   (event, "iL"  + self.inputlabel)][0:getattr(event,"nLepLoose"+self.inputlabel)]
        self.lepst      = [self.leps[il] for il in getattr   (event, "iT"  + self.inputlabel)][0:getattr(event,"nLepTight"+self.inputlabel)]
        self.lepsfv     = [self.leps[il] for il in getattr   (event, "iFV" + self.inputlabel)][0:getattr(event,"nLepFOVeto"+self.inputlabel)]
        self.lepstv     = [self.leps[il] for il in getattr   (event, "iTV" + self.inputlabel)][0:getattr(event,"nLepTightVeto"+self.inputlabel)]
        self.lepsfv     = [x for x in self.lepsfv if x not in self.lepstv]

        jetcollcleaned  = [j for j in Collection(event,"Jet","nJet")]
        jetcolldiscarded = [j for j in Collection(event,"DiscJet","nDiscJet")]
        self.jets30     = filter(lambda x: x.pt > 30., [ (jetcollcleaned[idx] if idx>=0 else jetcolldiscarded[-1-idx]) for idx in getattr(event,"iJSel"+self.inputlabel) ])
        self.bJets30    = filter(lambda j: j.btagCSV >  0.89, self.jets30)
        self.ht         = sum([j.pt for j in self.jets30])

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
        self.systs["FR"   ] = {0: "", 1: "_ewkUp"  , -1: "_ewkDown"  }
        self.systs["JEC"  ] = {0: "", 1: "_jecUp"  , -1: "_jecDown"  }
        self.systs["LEPSF"] = {0: "", 1: "_lepSFUp", -1: "_lepSFDown", 2: "_lepSF_FS_Up", -2: "_lepSF_FS_Down"}


    ## collectTriples
    ## _______________________________________________________________
    def collectTriples(self):
        ## searches for the three leptons in the event

        self.triples = []

        if self.whichApplication == self.appl_Fakes:
            self.collectTriplesFakes(byflav = True, bypassMV = False)
        elif self.whichApplication == self.appl_Flips:
            self.collectTriplesFlips(byflav = True, bypassMV = False)
        elif self.whichApplication == self.appl_WZ:
            self.collectTriplesWZ(byflav = True, bypassMV = False)

        self.ret["nTriples"] = len(self.triples)
        if self.ret["nTriples"] > 20: raise RuntimeError,'Too many lepton pairs'



    ## collectTriplesFakes
    ## _______________________________________________________________
    def collectTriplesFakes(self, byflav, bypassMV):
        ## encodes the logic of finding the three leptons in the event
        ## if we have TTT -> event only goes into SR
        ## if not, we look for all possible triples (c.f. findTriples())
        ## made of tight leptons and fakes

        self.trueTriples = []
        self.triples, self.fakes = self.findTriples([], self.lepstv, self.lepstv, self.lepstv, bypassMV=False)

        if self.triples:
            self.ret["hasTTT"] = True
            self.trueTriples   = self.triples
        else:
            tr1f, f1 = self.findTriples(self.triples, self.lepstv, self.lepstv, self.lepsfv, bypassMV=False, nF=1)
            tr2f, f2 = self.findTriples(self.triples, self.lepstv, self.lepsfv, self.lepsfv, bypassMV=False, nF=2)
            tr3f, f3 = self.findTriples(self.triples, self.lepsfv, self.lepsfv, self.lepsfv, bypassMV=False, nF=3)

            if tr1f: self.ret["hasTTF"] = True
            if tr2f: self.ret["hasTFF"] = True
            if tr3f: self.ret["hasFFF"] = True

            self.triples = tr1f + tr2f + tr3f
            self.fakes   = f1   + f2   + f3


    ## collectTriplesFlips
    ## _______________________________________________________________
    def collectTriplesFlips(self, byflav, bypassMV):

        print "do stuff"
        #FIXME
        #    choice = self.findPairs(lepstv,lepstv,byflav=True,bypassMV=False,choose_SS_else_OS=True)
        #    if choice:
        #        ret["hasTT"]=True
        #        choice=choice[:1]
        #    else:
        #        choice = self.findPairs(lepst,lepst,byflav=True,bypassMV=False,choose_SS_else_OS=False)
        #        if choice:
        #            ret["hasTF"]=True
        #            choice=choice[:1]


    ## collectTriplesWZ
    ## _______________________________________________________________
    def collectTriplesWZ(self, byflav, bypassMV):

        print "do more stuff"
        #FIXME
        #    choice = self.findPairs(lepst,lepst,byflav=True,bypassMV=True,choose_SS_else_OS=True)
        #    if choice:
        #        ret["hasTT"]=True
        #    else:
        #        choice = self.findPairs(lepst,lepst,byflav=True,bypassMV=True,choose_SS_else_OS=False)
        #        if choice:
        #            ret["hasTF"]=True
        #            choice=choice[:1]
         

    ## fillAppWeights
    ## _______________________________________________________________
    def fillAppWeights(self, t, i1, i2, i3):

        if not self.apply: return

        if   self.whichApplication == self.appl_Fakes: self.fillAppWeightsFakes(t)
        elif self.whichApplication == self.appl_Flips: self.fillAppWeightsFlips(t, i1, i2, i3)
        elif self.whichApplication == self.appl_WZ   : self.fillAppWeightsWZ   (t, i1, i2, i3)


    ## fillAppWeightsFakes
    ## _______________________________________________________________
    def fillAppWeightsFakes(self, t):

        if self.ret["hasTTT"]: 
            for var in self.systs["FR"]:
                self.ret["appWeight" + self.systs["FR"][var]][t] = 0.0
        else:
            for var in self.systs["FR"]:
                fk = filter(None, self.fakes[t])
                nF = len(fk)

                if nF == 1:
                    self.ret["appWeight" + self.systs["FR"][var]][t] =   self.getFakeTransfer(fk[0], var)

                elif nF == 2:
                    self.ret["appWeight" + self.systs["FR"][var]][t] = - self.getFakeTransfer(fk[0], var) \
                                                                       * self.getFakeTransfer(fk[1], var)
                elif nF == 3:
                    self.ret["appWeight" + self.systs["FR"][var]][t] =   self.getFakeTransfer(fk[0], var) \
                                                                       * self.getFakeTransfer(fk[1], var) \
                                                                       * self.getFakeTransfer(fk[2], var)


    ## fillAppWeightsFlips
    ## _______________________________________________________________
    def fillAppWeightsFlips(self, t):
        print "do stuff"
        #FIXME
        #ret["appWeight"][npair] = self.flipRate(leps[i1])+self.flipRate(leps[i2])


    ## fillAppWeightsWZ
    ## _______________________________________________________________
    def fillAppWeightsWZ(self, t):
        print "do stuff"
        #FIXME


    ## fillJetQuantities
    ## _______________________________________________________________
    def fillJetQuantities(self, t, i1, i2, i3):

        lepcoll = [self.leps[i1], self.leps[i2], self.leps[i3]]
        self.ret["maxDeltaPhiLepJet" ][t] = max([ abs(deltaPhi(l.phi, j.phi)) for l in lepcoll for j in self.jets30 ]+[-999])
        self.ret["maxDeltaPhiLepBJet"][t] = max([ abs(deltaPhi(l.phi, j.phi)) for l in lepcoll for j in self.bJets30]+[-999])
        self.ret["maxDeltaPhiJetJet" ][t] = max([(abs(deltaPhi(j1.phi, j2.phi)) if j1!=j2 else -999) for j1 in self.jets30 for j2 in self.jets30]+[-999])
        self.ret["minDeltaRLepJet"   ][t] = min([ abs(deltaR(l, j)) for l in lepcoll for j in self.jets30]+[999])
        self.ret["minDeltaRLepBJet"  ][t] = min([ abs(deltaR(l, j)) for l in lepcoll for j in self.bJets30]+[999])


    ## fillLeptonSF
    ## _______________________________________________________________
    def fillLeptonSF(self, event, t, i1, i2, i3, var = 0):

        self.ret["leptonSF" + self.systs["LEPSF"][var]][t] = 1.;
        if event.isData: return

        lepsf = [1]*3
        for i, idx in enumerate([i1, i2, i3]):
            idxs = 0 if abs(self.leps[idx].pdgId) == 13 else 1
            lepsf[i] *= self.readHistos(self.leptonScaleFactorHistosFull[idxs], var, self.leps[idx].pt, abs(self.leps[idx].eta))

            #FIXME: fast sim lepton SF not yet included
            #if self.isFastSim:
            #    sf    = self.readHistos(self.leptonScaleFactorHistosFast[idxs], var, self.leps[idx].pt,  abs(self.leps[idx].eta), event.nVert)
            #    sferr = 0 # error ignored for now
            #    err = sferr / sf
            #    lepsf[i] *= sf
            #    if   var ==  2: lepsf[i] *= (1+err)
            #    elif var == -2: lepsf[i] *= (1-err)
        self.ret["leptonSF" + self.systs["LEPSF"][var]][t] = lepsf[0] * lepsf[1] * lepsf[2]


    ## fillOnZ
    ## _______________________________________________________________
    def fillOnZ(self, t, var = 0):
        self.ret["isOnZ" + self.systs["JEC"][var]] = 1 if self.isOnZ(self.lepstv, var) else 0


    ## fillSR
    ## _______________________________________________________________
    def fillSR(self, t, var = ""):

        BR  = -1
        SR  = -1

        if self.ret["isOnZ" + self.systs["JEC"][var]]: 
            BR = self.findBR(var, 0 )
            SR = self.findSR(var, 0 )
        else: 
            BR = self.findBR(var, 15)
            SR = self.findSR(var, 15)

        self.ret["BR" + self.systs["JEC"][var]][t] = BR
        self.ret["SR" + self.systs["JEC"][var]][t] = SR


    ## fillTriggerSF
    ## _______________________________________________________________
    def fillTriggerSF(self, event, t, i1, i2, i3):

        self.ret["triggerSF"][t] = 1.
        if event.isData: return
        self.ret["triggerSF"][t] = triggerScaleFactorFullSim(self.leps[i1].pdgId, self.leps[i2].pdgId, \
                                                             self.leps[i1].pt   , self.leps[i2].pt   , self.ht)
        if self.isFastSim:
            self.ret["triggerSF"][t] *= FastSimTriggerEfficiency( self.ht, self.leps[i1].pt, self.leps[i1].pdgId, \
                                                                              self.leps[i2].pt, self.leps[i2].pdgId)


    ## fillVtxWeight
    ## _______________________________________________________________
    def fillVtxWeight(self, event, var = 0):
        if event.isData: return
        nvtx = int(getattr(event,"nTrueInt"))
        self.ret["vtxWeight"] = self.puWeights[var][nvtx] if nvtx < len(self.puWeights[var]) else 1
        


    ## findBR
    ## _______________________________________________________________
    def findBR(self, var, offset = 0):

        BR = -1
        if   len(self.jets30) >= 2 and len(self.bJets30) == 0 and  50 <= self.met[var] and  60 <= self.ht:   BR =  1 

        return BR + offset


    ## findSR
    ## _______________________________________________________________
    def findSR(self, var, offset = 0):

        SR = -1
        if   len(self.jets30) >= 2 and len(self.bJets30) == 0 and  50 <= self.met[var] < 150 and  60 <= self.ht < 400:   SR =  1 
        elif len(self.jets30) >= 2 and len(self.bJets30) == 0 and 150 <= self.met[var] < 300 and  60 <= self.ht < 400:   SR =  2 
        elif len(self.jets30) >= 2 and len(self.bJets30) == 0 and  50 <= self.met[var] < 150 and 400 <= self.ht < 600:   SR =  3 
        elif len(self.jets30) >= 2 and len(self.bJets30) == 0 and 150 <= self.met[var] < 300 and 400 <= self.ht < 600:   SR =  4 
        elif len(self.jets30) >= 2 and len(self.bJets30) == 1 and  50 <= self.met[var] < 150 and  60 <= self.ht < 400:   SR =  5 
        elif len(self.jets30) >= 2 and len(self.bJets30) == 1 and 150 <= self.met[var] < 300 and  60 <= self.ht < 400:   SR =  6 
        elif len(self.jets30) >= 2 and len(self.bJets30) == 1 and  50 <= self.met[var] < 150 and 400 <= self.ht < 600:   SR =  7 
        elif len(self.jets30) >= 2 and len(self.bJets30) == 1 and 150 <= self.met[var] < 300 and 400 <= self.ht < 600:   SR =  8 
        elif len(self.jets30) >= 2 and len(self.bJets30) == 2 and  50 <= self.met[var] < 150 and  60 <= self.ht < 400:   SR =  9 
        elif len(self.jets30) >= 2 and len(self.bJets30) == 2 and 150 <= self.met[var] < 300 and  60 <= self.ht < 400:   SR = 10
        elif len(self.jets30) >= 2 and len(self.bJets30) == 2 and  50 <= self.met[var] < 150 and 400 <= self.ht < 600:   SR = 11
        elif len(self.jets30) >= 2 and len(self.bJets30) == 2 and 150 <= self.met[var] < 300 and 400 <= self.ht < 600:   SR = 12
        elif len(self.jets30) >= 2 and len(self.bJets30) >= 3 and  50 <= self.met[var] < 300 and  60 <= self.ht < 600:   SR = 13
        elif len(self.jets30) >= 2 and len(self.bJets30) >= 0 and  50 <= self.met[var] < 300 and 600 <= self.ht      :   SR = 14
        elif len(self.jets30) >= 2 and len(self.bJets30) >= 0 and 300 <= self.met[var]       and  60 <= self.ht      :   SR = 15

        return SR + offset


    ## findTriples
    ## _______________________________________________________________
    def findTriples(self, already, leps1, leps2, leps3, bypassMV, nF = 0):
        ## produces a list of all valid 3lepton combinations in the event,
        ## ordered by pt (first one hardest), and also returns the list of
        ## fakes in the triple

        triples   = []
        fakes     = []
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
            if (l1, l2, l3) in already: continue # fake-not-tight!
            if not bypassMV and not passTripleMllVeto(l1, l2, l3, 0, 12, True): continue
            if pt_sorted[i][0] > 20 and pt_sorted[i][1] > 15 and pt_sorted[i][2] > 10:
                triples.append((l1, l2, l3))
                fakes  .append(fk_sorted[i])

        if len(triples):
             return triples, fakes
        return [], []


    ## getFakeRate
    ## _______________________________________________________________
    def getFakeRate(self, lep, var = 0): 
        idx = 0 if abs(lep.pdgId) == 13 else 1
        return self.readHistos(self.fakeRatioMap[idx], var, lep.conePt, abs(lep.eta))


    ## getFakeTransfer
    ## _______________________________________________________________
    def getFakeTransfer(self, lep, var = 0):
        prob = self.getFakeRate(lep, var)
        return prob/(1 - prob)


    ## getFlipRate
    ## _______________________________________________________________
    def getFlipRate(self, lep, var = 0):
        if abs(lep.pdgId) != 11: return 0.
        idx = 0 if abs(lep.pdgId) == 13 else 1
        sf = 3.6 if (lep.eta < -1.5 and lep.eta > -2) else 1.15
        return sf * self.readHistos(self.flipRatioMap[idx], var, lep.conePt, abs(lep.eta))


    ## isOnZ
    ## _______________________________________________________________
    def isOnZ(self, leps, var = 0):
        passMll = False
        for lep in leps:
            if not passMllTLVeto(lep, leps, 76, 106, True): 
                passMll = True
                break
        mll, ii1, ii2 = self.bestZ1TL(leps, leps)
        if abs(mll - 91) < 15:
            return True
        return False


    ## listBranches
    ## _______________________________________________________________
    def listBranches(self):
        biglist = [ 
            ("vtxWeight"          + self.label, "F"),
            ("nTriples"           + self.label, "I"),
            ("i1"                 + self.label, "I", 20, "nTriples" + self.label),
            ("i2"                 + self.label, "I", 20, "nTriples" + self.label),
            ("i3"                 + self.label, "I", 20, "nTriples" + self.label),
            ("hasTTT"             + self.label, "I"), 
            ("hasTTF"             + self.label, "I"), 
            ("hasTFF"             + self.label, "I"), 
            ("hasFFF"             + self.label, "I"), 
            ("triggerSF"          + self.label, "F", 20, "nTriples" + self.label),
            ("maxDeltaPhiLepJet"  + self.label, "F", 20, "nTriples" + self.label),
            ("maxDeltaPhiLepBJet" + self.label, "F", 20, "nTriples" + self.label),
            ("maxDeltaPhiJetJet"  + self.label, "F", 20, "nTriples" + self.label),
            ("minDeltaRLepJet"    + self.label, "F", 20, "nTriples" + self.label),
            ("minDeltaRLepBJet"   + self.label, "F", 20, "nTriples" + self.label),
            ]
        for var in self.systs["FR"]:
            biglist.append(("appWeight" + self.systs["FR"   ][var] + self.label, "F", 20, "nTriples" + self.label))
        for var in self.systs["JEC"]:
            biglist.append(("isOnZ"     + self.systs["JEC"  ][var] + self.label, "I"))
            biglist.append(("BR"        + self.systs["JEC"  ][var] + self.label, "I", 20, "nTriples" + self.label))
            biglist.append(("SR"        + self.systs["JEC"  ][var] + self.label, "I", 20, "nTriples" + self.label))
        for var in self.systs["LEPSF"]: 
            biglist.append(("leptonSF"  + self.systs["LEPSF"][var] + self.label, "F", 20, "nTriples" + self.label))
        return biglist


    ## loadFakeRateHistos
    ## _______________________________________________________________
    def loadFakeRateHistos(self, filePath):
        if not filePath: return
        mu, el = self.accessHistos(filePath)
        self.fakeRatioMap = [mu, el]
        return (mu and el)


    ## loadFlipRateHistos
    ## _______________________________________________________________
    def loadFlipRateHistos(self, filePath):
        if not filePath: return
        mu, el = self.accessHistos(filePath)
        self.flipRatioMap = [mu, el]
        return (mu and el)


    ## loadLeptonScaleFactorHistos
    ## _______________________________________________________________
    def loadLeptonScaleFactorHistos(self, filePathsFull, filePathsFast):
        if not filePathsFull: return
        mu, el = self.accessHistos(filePathsFull)
        self.leptonScaleFactorHistosFull = [mu, el]
        if not filePathsFast: return
        mu, el = self.accessHistos(filePathsFast)
        self.leptonScaleFactorHistosFast = [mu, el]


    ## loadPileUpHisto
    ## _______________________________________________________________
    def loadPileUpHisto(self, filePath):
        if not filePath: return
        self.pileupHisto = self.accessHisto(filePath)
        self.puWeights = {}
        for key, val in self.pileupHisto.iteritems():
            self.puWeights[key] = [val.GetBinContent(i) for i in xrange(1, val.GetNbinsX()+1)]


    ## mt  
    ## _______________________________________________________________
    def mt(self, pt1, pt2, phi1, phi2):
        return sqrt(2*pt1*pt2*(1-cos(phi1-phi2)))


    ## mtW
    ## _______________________________________________________________
    def mtW(self, pt, phi, var):
        return self.mt(pt, self.met[var], phi, self.metphi[var])


    ## readHisto
    ## _______________________________________________________________
    def readHisto(self, hist, valx, valy, valz = 0):
        if hist.GetDimension() == 3:
            return hist.GetBinContent(max(1, min(hist.GetNbinsX(), hist.GetXaxis().FindBin(valx))),\
                                      max(1, min(hist.GetNbinsY(), hist.GetYaxis().FindBin(valy))),\
                                      max(1, min(hist.GetNbinsZ(), hist.GetZaxis().FindBin(valz))))
        return hist.GetBinContent(max(1, min(hist.GetNbinsX(), hist.GetXaxis().FindBin(valx))),\
                                  max(1, min(hist.GetNbinsY(), hist.GetYaxis().FindBin(valy)))) 


    ## readHistos
    ## _______________________________________________________________
    def readHistos(self, hists, var, valx, valy, valz = 0):
        value = 1.
        for hist in hists: 
            if not var in hist.keys(): var = 0
            value *= self.readHisto(hist[var], valx, valy, valz)
        return value


    ## resetMemory
    ## _______________________________________________________________
    def resetMemory(self):
        self.ret = {};
        self.ret["vtxWeight"         ] = 1.
        self.ret["nTriples"          ] = 0
        self.ret["i1"                ] = [0]*20
        self.ret["i2"                ] = [0]*20
        self.ret["i3"                ] = [0]*20
        self.ret["hasTTT"            ] = False
        self.ret["hasTTF"            ] = False
        self.ret["hasTFF"            ] = False
        self.ret["hasFFF"            ] = False
        self.ret["triggerSF"         ] = [0]*20
        self.ret["maxDeltaPhiLepJet" ] = [0]*20
        self.ret["maxDeltaPhiLepBJet"] = [0]*20
        self.ret["maxDeltaPhiJetJet" ] = [0]*20
        self.ret["minDeltaRLepJet"   ] = [0]*20
        self.ret["minDeltaRLepBJet"  ] = [0]*20

        for var in self.systs["FR"]: 
            self.ret["appWeight" + self.systs["FR"   ][var]] = [0]*20
        for var in self.systs["JEC"]: 
            self.ret["isOnZ"     + self.systs["JEC"  ][var]] = 0
            self.ret["BR"        + self.systs["JEC"  ][var]] = [0]*20
            self.ret["SR"        + self.systs["JEC"  ][var]] = [0]*20
        for var in self.systs["LEPSF"]: 
            self.ret["leptonSF"  + self.systs["LEPSF"][var]] = [0]*20


    ## setApplication
    ## _______________________________________________________________
    def setApplication(self, whichApplication, filePathFakeRate):

        self.apply            = False
        self.whichApplication = -1

        if   whichApplication == "Fakes": self.whichApplication = self.appl_Fakes
        elif whichApplication == "Flips": self.whichApplication = self.appl_Flips
        elif whichApplication == "WZ"   : self.whichApplication = self.appl_WZ
        else                            : raise RuntimeError, 'Unknown whichApplication'

        if self.whichApplication == self.appl_Fakes:
            if filePathFakeRate and self.loadFakeRateHistos(filePathFakeRate):
                self.apply = True
        elif self.whichApplication == self.appl_Flips:
            if filePathFakeRate and self.loadFlipRateHistos(filePathFakeRate):
                self.apply = True
        if not self.apply:
            print 'WARNING: running leptonChoiceRA7 in pure tagging mode (no weights applied)'


    ## for debugging only
    ## _______________________________________________________________
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

from CMGTools.TTHAnalysis.tools.leptonChoiceRA5 import _susy2lss_lepId_IPcuts


def _susyEWK_idEmu_cuts(lep):
    if (abs(lep.pdgId)!=11): return True
    if (lep.hadronicOverEm>=(0.10-0.03*(abs(lep.etaSc)>1.479))): return False
    if (abs(lep.dEtaScTrkIn)>=(0.01-0.002*(abs(lep.etaSc)>1.479))): return False
    if (abs(lep.dPhiScTrkIn)>=(0.04+0.03*(abs(lep.etaSc)>1.479))): return False
    if (lep.eInvMinusPInv<=-0.05): return False
    if (lep.eInvMinusPInv>=(0.01-0.005*(abs(lep.etaSc)>1.479))): return False
    if (lep.sigmaIEtaIEta>=(0.011+0.019*(abs(lep.etaSc)>1.479))): return False
    return True

def _susy3l_multiIso(lep):
    # CH: looser WP than for RA5 (electrons -> medium, muons -> loose)
    if abs(lep.pdgId) == 13: A,B,C = (0.20,0.69,6.0)
    else:                    A,B,C = (0.16,0.76,7.2)
    return lep.miniRelIso < A and (lep.jetPtRatiov2 > B or lep.jetPtRelv2 > C)

def _susy3l_lepId_CBloose(lep):
        if abs(lep.pdgId) == 13:
            if lep.pt <= 5: return False
            return True #lep.mediumMuonId > 0
        elif abs(lep.pdgId) == 11:
            if lep.pt <= 7: return False
            if not (lep.convVeto and lep.lostHits <= 1): 
                return False
            if not lep.mvaIdSpring15 > -0.70+(-0.83+0.70)*(abs(lep.etaSc)>0.8)+(-0.92+0.83)*(abs(lep.etaSc)>1.479):
                return False
            if not _susy3l_idEmu_cuts(lep): return False
            return True
        return False

def _susy3l_lepId_loosestFO(lep):
    # CH: the same as the 2lss one but without tightCharge
    if not _susy3l_lepId_CBloose(lep): return False
    if abs(lep.pdgId) == 13:
        return lep.mediumMuonID2016 > 0
    elif abs(lep.pdgId) == 11:
        return (lep.convVeto and lep.lostHits == 0)
    return False

def _susy3l_lepId_CB(lep):
    # CH: the same as the 2lss one but without tightCharge
    if not _susy3l_lepId_CBloose(lep): return False
    if not _susy2lss_lepId_IPcuts(lep): return False
    if abs(lep.pdgId) == 13:
        return lep.mediumMuonID2016 > 0
    elif abs(lep.pdgId) == 11:
        if not (lep.convVeto and lep.lostHits == 0): 
            return False
        return lep.mvaIdSpring15 > 0.87+(0.60-0.87)*(abs(lep.eta)>0.8)+(0.17-0.60)*(abs(lep.eta)>1.479)
    return False



if __name__ == '__main__':
    from sys import argv
    file = ROOT.TFile(argv[1])
    tree = file.Get("tree")
    tree.vectorTree = True
    class Tester(Module):
        def __init__(self, name):
            Module.__init__(self,name,None)
            self.sf1 = LeptonChoiceRA7("Old", 
                lambda lep : lep.relIso03 < 0.5, 
                lambda lep : lep.relIso03 < 0.1 and lep.sip3d < 4 and _susy2lss_lepId_CB(lep),
                cleanJet = lambda lep,jet,dr : (lep.pt > 10 and dr < 0.4))
            self.sf2 = LeptonChoiceRA7("PtRel", 
                lambda lep : lep.relIso03 < 0.4 or lep.jetPtRel > 5, 
                lambda lep : (lep.relIso03 < 0.1 or lep.jetPtRel > 14) and lep.sip3d < 4 and _susy2lss_lepId_CB(lep),
                cleanJet = lambda lep,jet,dr : (lep.pt > 10 and dr < 0.4))
            self.sf3 = LeptonChoiceRA7("MiniIso", 
                lambda lep : lep.miniRelIso < 0.4, 
                lambda lep : lep.miniRelIso < 0.05 and lep.sip3d < 4 and _susy2lss_lepId_CB(lep),
                cleanJet = lambda lep,jet,dr : (lep.pt > 10 and dr < 0.4))
            self.sf4 = LeptonChoiceRA7("PtRelJC", 
                lambda lep : lep.relIso03 < 0.4 or lep.jetPtRel > 5, 
                lambda lep : (lep.relIso03 < 0.1 or lep.jetPtRel > 14) and lep.sip3d < 4 and _susy2lss_lepId_CB(lep),
                cleanJet = lambda lep,jet,dr : (lep.pt > 10 and dr < 0.4 and not (lep.jetPtRel > 5 and lep.pt*(1/lep.jetPtRatio-1) > 25)))
            self.sf5 = LeptonChoiceRA7("MiniIsoJC", 
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

        
