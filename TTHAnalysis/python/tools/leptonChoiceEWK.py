from CMGTools.TTHAnalysis.treeReAnalyzer import *
from CMGTools.TTHAnalysis.tools.leptonJetReCleaner import passTripleMllVeto,passMllTLVeto
from ROOT import TFile,TH1F
import copy, os

for extlib in ["triggerSF/triggerSF_fullsim_UCSx_v5_01.cc","leptonSF/lepton_SF_UCSx_v5_03.cc","triggerSF/FastSimTriggerEff.cc"]:
    if not extlib.endswith(".cc"): raise RuntimeError
    if "/%s"%extlib.replace(".cc","_cc.so") not in ROOT.gSystem.GetLibraries():
        ROOT.gROOT.LoadMacro(os.environ["CMSSW_BASE"]+"/src/CMGTools/TTHAnalysis/data/%s+"%extlib)
from ROOT import triggerScaleFactorFullSim
from ROOT import FastSimTriggerEfficiency

class LeptonChoiceEWK:

    # enum
    appl_Fakes = 0
    appl_Flips = 1
    appl_Taus  = 2
    appl_WZ    = 3


    ## __init__
    ## _______________________________________________________________
    def __init__(self, label, inputlabel, whichApplication, isFastSim=False, filePathFakeRate=None, filePathLeptonSFfull=None, filePathLeptonSFfast=None, filePathPileUp=None, noTausOS=True):

        self.label      = "" if (label in ["", None]) else ("_" + label)
        self.inputlabel = '_' + inputlabel
        self.isFastSim = isFastSim
        self.noTausOS  = noTausOS # set to true if you do NOT want to use taus in the OSSF/OSOF pairing for mll

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
          ## returns the Mll, i1 and i2 of the OSSF lepton pair whose Mll is closest to mZ

          pairs = []
          for i1, l1 in enumerate(lepst):
            if not cut(l1): continue
            for i2, l2 in enumerate(lepsl):
                if not cut(l2): continue
                if self.noTausOS and (l1.isTau or l2.isTau): continue
                if l1 == l2: continue
                if l1.pdgId == -l2.pdgId:
                   mz = (l1.p4() + l2.p4()).M()
                   diff = abs(mz-91)
                   pairs.append( (diff, mz, l1.trIdx, l2.trIdx, l1.isTau, l2.isTau) )
          if len(pairs):
              pairs.sort()
              return pairs[0]
          return (0., -1,  -1, -1, 0, 0)


    ## bestZtauTL
    ## _______________________________________________________________
    def bestZtauTL(self, lepsl, lepst, cut=lambda lep:True):
          ## returns the Mll, i1 and i2 of the OS lepton pair whose Mll is closest to corresponding
          ## dilepton mass (50 for emu)

          pairs = []
          for i1, l1 in enumerate(lepst):
            if not cut(l1): continue
            for i2, l2 in enumerate(lepsl):
                if not cut(l2): continue
                if self.noTausOS and (l1.isTau or l2.isTau): continue
                if l1 == l2: continue
                if l1.charge == -l2.charge and l1.pdgId != -l2.pdgId:
                   mz = (l1.p4() + l2.p4()).M()
                   dm = 50. #if abs(l1.pdgId) + abs(l1.pdgId)
                   if abs(l1.pdgId) == 15 or abs(l2.pdgId) == 15: dm = 60.
                   diff = abs(mz-dm)
                   pairs.append( (diff, mz, l1.trIdx, l2.trIdx, l1.isTau, l2.isTau) )
          if len(pairs):
              pairs.sort()
              return pairs[0]
          return (0., -1, -1, -1, 0, 0)
          

    ## categorizeEvent
    ## _______________________________________________________________
    def categorizeEvent(self, event):

        self.fillVtxWeight(event, 0)

        if not self.triples: return

        for var in self.systs["JEC"]:
            self.fillMllMtMinOnZ(var)
            self.fillSR(var)

        #if len(self.trueTriples) < 1: return

        #printed = False
        for t in xrange(len(self.triples)):

            i1 = self.triples[t][0].trIdx
            i2 = self.triples[t][1].trIdx
            i3 = self.triples[t][2].trIdx
            t1 = self.triples[t][0].isTau
            t2 = self.triples[t][1].isTau
            t3 = self.triples[t][2].isTau

            #self.fillTriggerSF(event, t, i1, i2, i3) # flat uncertainty for now

            for var in self.systs["LEPSF"]:
                self.fillLeptonSF(event, t, i1, i2, i3, t1, t2, t3, var)

            self.fillJetQuantities(t, i1, i2, i3, t1, t2, t3)
            self.fillAppWeights(t, i1, i2, i3, t1, t2, t3)  

            ## debugging and synching
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
        self.setAttributes(self.leps, False)

        self.lepsl      = [self.leps[il] for il in getattr   (event, "iL"  + self.inputlabel)][0:getattr(event,"nLepLoose"+self.inputlabel)]
        self.lepst      = [self.leps[il] for il in getattr   (event, "iT"  + self.inputlabel)][0:getattr(event,"nLepTight"+self.inputlabel)]
        self.lepsfv     = [self.leps[il] for il in getattr   (event, "iFV" + self.inputlabel)][0:getattr(event,"nLepFOVeto"+self.inputlabel)]
        self.lepstv     = [self.leps[il] for il in getattr   (event, "iTV" + self.inputlabel)][0:getattr(event,"nLepTightVeto"+self.inputlabel)]
        self.lepsfv     = [x for x in self.lepsfv if x not in self.lepstv]

        self.taus       = [t             for t  in Collection(event, "TauGood", "nTauGood") if t.pt > 20]
        self.setAttributes(self.taus, True)
        self.taust      = self.taus
        self.tausf      = self.taust # THESE ARE THE TAU FAKES, NEED TO BE CHANGED!

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
        elif self.whichApplication == self.appl_Taus:
            self.collectTriplesTaus(byflav = True, bypassMV = False)
        elif self.whichApplication == self.appl_WZ:
            self.collectTriplesWZ(byflav = True, bypassMV = False)

        self.ret["nTriples"] = len(self.triples)
        if self.ret["nTriples"] > 20: raise RuntimeError,'Too many lepton pairs'

        for i in range(len(self.triples)):
            self.ret["i1"][i] = self.triples[i][0].trIdx; self.ret["t1"][i] = self.triples[i][0].isTau
            self.ret["i2"][i] = self.triples[i][1].trIdx; self.ret["t2"][i] = self.triples[i][1].isTau
            self.ret["i3"][i] = self.triples[i][2].trIdx; self.ret["t3"][i] = self.triples[i][2].isTau


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
            self.triples += tr1f
            tr2f, f2 = self.findTriples(self.triples, self.lepstv, self.lepsfv, self.lepsfv, bypassMV=False, nF=2)
            self.triples += tr2f
            tr3f, f3 = self.findTriples(self.triples, self.lepsfv, self.lepsfv, self.lepsfv, bypassMV=False, nF=3)
            self.triples += tr3f

            if tr1f: self.ret["hasTTF"] = True
            if tr2f: self.ret["hasTFF"] = True
            if tr3f: self.ret["hasFFF"] = True

            self.fakes       = f1 + f2 + f3


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


    ## collectTriplesTaus 
    ## _______________________________________________________________
    def collectTriplesTaus(self, byflav, bypassMV):
        ## encodes the logic of finding the three leptons in the event
        ## if we have TTT -> event only goes into SR
        ## if not, we look for all possible triples (c.f. findTriples())
        ## made of tight leptons and fakes
        ## hadronic taus included

        self.trueTriples = []
        self.triples, self.fakes = self.findTriples([], self.lepstv, self.lepstv, self.taust, bypassMV=False, nF=0)

        if self.triples:
            self.ret["hasTTT"] = True
            self.trueTriples   = self.triples

        #FIXME: fake taus not included yet
        #else:
        #    #tr1f, f1 = self.findTriples(self.triples, self.lepstv, self.lepstv, self.tausf, bypassMV=False, nF=1)
        #    #tr2f, f2 = self.findTriples(self.triples, self.lepstv, self.lepsfv, self.tausf, bypassMV=False, nF=2)
        #    #tr3f, f3 = self.findTriples(self.triples, self.lepsfv, self.lepsfv, self.tausf, bypassMV=False, nF=3)

        #    #if tr1f: self.ret["hasTTF"] = True
        #    #if tr2f: self.ret["hasTFF"] = True
        #    #if tr3f: self.ret["hasFFF"] = True

        #    #self.triples     = tr1f + tr2f + tr3f
        #    #self.fakes       = f1 + f2 + f3


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
    def fillAppWeights(self, t, i1, i2, i3, t1, t2, t3):

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
    def fillJetQuantities(self, t, i1, i2, i3, t1, t2, t3):

        lepcoll = [self.findObj(i1, t1), self.findObj(i2, t2), self.findObj(i3, t3)]
        self.ret["maxDeltaPhiLepJet" ][t] = max([ abs(deltaPhi(l.phi, j.phi)) for l in lepcoll for j in self.jets30 ]+[-999])
        self.ret["maxDeltaPhiLepBJet"][t] = max([ abs(deltaPhi(l.phi, j.phi)) for l in lepcoll for j in self.bJets30]+[-999])
        self.ret["maxDeltaPhiJetJet" ][t] = max([(abs(deltaPhi(j1.phi, j2.phi)) if j1!=j2 else -999) for j1 in self.jets30 for j2 in self.jets30]+[-999])
        self.ret["minDeltaRLepJet"   ][t] = min([ abs(deltaR(l, j)) for l in lepcoll for j in self.jets30]+[999])
        self.ret["minDeltaRLepBJet"  ][t] = min([ abs(deltaR(l, j)) for l in lepcoll for j in self.bJets30]+[999])


    ## fillLeptonSF
    ## _______________________________________________________________
    def fillLeptonSF(self, event, t, i1, i2, i3, t1, t2, t3, var = 0):

        self.ret["leptonSF" + self.systs["LEPSF"][var]][t] = 1.;
        if event.isData: return

        lepsf = [1]*3
        for i, (idx, ist) in enumerate([(i1, t1), (i2, t2), (i3, t3)]):
            if ist == 1: continue
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


    ## fillMllMtMinOnZ
    ## _______________________________________________________________
    def fillMllMtMinOnZ(self, var = 0):

        m , i1_mll , i2_mll, t1_mll, t2_mll, os = self.mll   (var)
        mT, i_mTmin, t_mTmin                    = self.findmt(i1_mll, i2_mll, t1_mll, t2_mll, var)

        self.ret["mll"     + self.systs["JEC"][var]] = m
        self.ret["i1_mll"  + self.systs["JEC"][var]] = i1_mll
        self.ret["i2_mll"  + self.systs["JEC"][var]] = i2_mll
        self.ret["t1_mll"  + self.systs["JEC"][var]] = t1_mll
        self.ret["t2_mll"  + self.systs["JEC"][var]] = t2_mll
        self.ret["mTmin"   + self.systs["JEC"][var]] = mT
        self.ret["i_mTmin" + self.systs["JEC"][var]] = i_mTmin
        self.ret["t_mTmin" + self.systs["JEC"][var]] = t_mTmin
        self.ret["isOnZ"   + self.systs["JEC"][var]] = 0

        if   os == 1: self.ret["hasOSSF" + self.systs["JEC"][var]] = 1
        elif os == 0: self.ret["hasOSOF" + self.systs["JEC"][var]] = 1
        elif os == 2: self.ret["hasSS"   + self.systs["JEC"][var]] = 1

        if abs(m - 91) < 15:
            self.ret["isOnZ" + self.systs["JEC"][var]] = 1


    ## fillSR
    ## _______________________________________________________________
    def fillSR(self, var = ""):

        BR = self.findBR(var)
        SR = self.findSR(var, BR)

        self.ret["BR" + self.systs["JEC"][var]] = BR
        self.ret["SR" + self.systs["JEC"][var]] = SR


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
    def findBR(self, var):
        # BR number = 0, 1, 2 = not in BR, with OSOF pair, with OSSF pair

        ossf = self.ret["hasOSSF" + self.systs["JEC"][var]]
        osof = self.ret["hasOSOF" + self.systs["JEC"][var]]
        met  = self.met[var]

        if met < 50        : return 0
        if ossf + osof == 0: return 0
        if osof            : return 1
        if ossf            : return 2

        return 0


    ## findmt
    ## _______________________________________________________________
    def findmt(self, i1, i2, t1, t2, var = 0):
        ## compute the MT of the third lepton of that triple, that was
        ## used to compute the mll

        buffer = []
        for (l1, l2, l3) in self.triples:
            idxs = [(l1.trIdx, l1.isTau), (l2.trIdx, l2.isTau), (l3.trIdx, l3.isTau)]
            if (i1, t1) in idxs and (i2, t2) in idxs:
                idxs.remove((i1, t1))
                idxs.remove((i2, t2))
                buffer.append((self.mtW(self.findObj(idxs[0][0], idxs[0][1]).pt, self.findObj(idxs[0][0], idxs[0][1]).phi, var), idxs[0][0], idxs[0][1]))
        if len(buffer):
            buffer.sort()
            return buffer[0]
        return (0., -1, 0)


    ## findObj
    ## _______________________________________________________________
    def findObj(self, idx, isTau = 0):
        if isTau == 1: return self.taus[idx]
        return self.leps[idx]


    ## findSR
    ## _______________________________________________________________
    def findSR(self, var, BR):

        SR = 0

        ossf = self.ret["hasOSSF" + self.systs["JEC"][var]]
        osof = self.ret["hasOSOF" + self.systs["JEC"][var]]
        ss   = self.ret["hasSS"   + self.systs["JEC"][var]]
        m    = self.ret["mll"     + self.systs["JEC"][var]]
        mT   = self.ret["mTmin"   + self.systs["JEC"][var]]
        met  = self.met[var]

        if BR == 0: return 0

        # OSSF category
        if   ossf and        m <  75 and        mT < 120 and  50 <= met < 100: SR =  1
        elif ossf and        m <  75 and        mT < 120 and 100 <= met < 150: SR =  2
        elif ossf and        m <  75 and        mT < 120 and 150 <= met < 200: SR =  3
        elif ossf and        m <  75 and        mT < 120 and 200 <= met      : SR =  4
        elif ossf and        m <  75 and 120 <= mT < 160 and  50 <= met < 100: SR =  5
        elif ossf and        m <  75 and 120 <= mT < 160 and 100 <= met < 150: SR =  6
        elif ossf and        m <  75 and 120 <= mT < 160 and 150 <= met < 200: SR =  7
        elif ossf and        m <  75 and 120 <= mT < 160 and 200 <= met      : SR =  8
        elif ossf and        m <  75 and 160 <= mT       and  50 <= met < 100: SR =  9
        elif ossf and        m <  75 and 160 <= mT       and 100 <= met < 150: SR = 10
        elif ossf and        m <  75 and 160 <= mT       and 150 <= met < 200: SR = 11
        elif ossf and        m <  75 and 160 <= mT       and 200 <= met      : SR = 12
        elif ossf and  75 <= m < 105 and        mT < 120 and  50 <= met < 100: SR = 13
        elif ossf and  75 <= m < 105 and        mT < 120 and 100 <= met < 150: SR = 14
        elif ossf and  75 <= m < 105 and        mT < 120 and 150 <= met < 200: SR = 15
        elif ossf and  75 <= m < 105 and        mT < 120 and 200 <= met      : SR = 16
        elif ossf and  75 <= m < 105 and 120 <= mT < 160 and  50 <= met < 100: SR = 17
        elif ossf and  75 <= m < 105 and 120 <= mT < 160 and 100 <= met < 150: SR = 18
        elif ossf and  75 <= m < 105 and 120 <= mT < 160 and 150 <= met < 200: SR = 19
        elif ossf and  75 <= m < 105 and 120 <= mT < 160 and 200 <= met      : SR = 20
        elif ossf and  75 <= m < 105 and 160 <= mT       and  50 <= met < 100: SR = 21
        elif ossf and  75 <= m < 105 and 160 <= mT       and 100 <= met < 150: SR = 22
        elif ossf and  75 <= m < 105 and 160 <= mT       and 150 <= met < 200: SR = 23
        elif ossf and  75 <= m < 105 and 160 <= mT       and 200 <= met      : SR = 24
        elif ossf and 105 <= m       and        mT < 120 and  50 <= met < 100: SR = 25
        elif ossf and 105 <= m       and        mT < 120 and 100 <= met < 150: SR = 26
        elif ossf and 105 <= m       and        mT < 120 and 150 <= met < 200: SR = 27
        elif ossf and 105 <= m       and        mT < 120 and 200 <= met      : SR = 28
        elif ossf and 105 <= m       and 120 <= mT < 160 and  50 <= met < 100: SR = 29
        elif ossf and 105 <= m       and 120 <= mT < 160 and 100 <= met < 150: SR = 30
        elif ossf and 105 <= m       and 120 <= mT < 160 and 150 <= met < 200: SR = 31
        elif ossf and 105 <= m       and 120 <= mT < 160 and 200 <= met      : SR = 32
        elif ossf and 105 <= m       and 160 <= mT       and  50 <= met < 100: SR = 33
        elif ossf and 105 <= m       and 160 <= mT       and 100 <= met < 150: SR = 34
        elif ossf and 105 <= m       and 160 <= mT       and 150 <= met < 200: SR = 35
        elif ossf and 105 <= m       and 160 <= mT       and 200 <= met      : SR = 36

        # OSOF category
        elif osof and        m < 100 and        mT < 120 and  50 <= met < 100: SR = 37
        elif osof and        m < 100 and        mT < 120 and 100 <= met < 150: SR = 38
        elif osof and        m < 100 and        mT < 120 and 150 <= met < 200: SR = 39
        elif osof and        m < 100 and        mT < 120 and 200 <= met      : SR = 40
        elif osof and        m < 100 and 120 <= mT < 160 and  50 <= met < 100: SR = 41
        elif osof and        m < 100 and 120 <= mT < 160 and 100 <= met < 150: SR = 42
        elif osof and        m < 100 and 120 <= mT < 160 and 150 <= met < 200: SR = 43
        elif osof and        m < 100 and 120 <= mT < 160 and 200 <= met      : SR = 44
        elif osof and        m < 100 and 160 <= mT       and  50 <= met < 100: SR = 45
        elif osof and        m < 100 and 160 <= mT       and 100 <= met < 150: SR = 46
        elif osof and        m < 100 and 160 <= mT       and 150 <= met < 200: SR = 47
        elif osof and        m < 100 and 160 <= mT       and 200 <= met      : SR = 48
        elif osof and 100 <= m       and        mT < 120 and  50 <= met < 100: SR = 49
        elif osof and 100 <= m       and        mT < 120 and 100 <= met < 150: SR = 50
        elif osof and 100 <= m       and        mT < 120 and 150 <= met < 200: SR = 51
        elif osof and 100 <= m       and        mT < 120 and 200 <= met      : SR = 52
        elif osof and 100 <= m       and 120 <= mT < 160 and  50 <= met < 100: SR = 53
        elif osof and 100 <= m       and 120 <= mT < 160 and 100 <= met < 150: SR = 54
        elif osof and 100 <= m       and 120 <= mT < 160 and 150 <= met < 200: SR = 55
        elif osof and 100 <= m       and 120 <= mT < 160 and 200 <= met      : SR = 56
        elif osof and 100 <= m       and 160 <= mT       and  50 <= met < 100: SR = 57
        elif osof and 100 <= m       and 160 <= mT       and 100 <= met < 150: SR = 58
        elif osof and 100 <= m       and 160 <= mT       and 150 <= met < 200: SR = 59
        elif osof and 100 <= m       and 160 <= mT       and 200 <= met      : SR = 60

        # SS category
        elif ss   and        m < 100 and        mT < 120 and  50 <= met < 100: SR = 61
        elif ss   and        m < 100 and        mT < 120 and 100 <= met < 150: SR = 62
        elif ss   and        m < 100 and        mT < 120 and 150 <= met < 200: SR = 63
        elif ss   and        m < 100 and        mT < 120 and 200 <= met      : SR = 64
        elif ss   and        m < 100 and 120 <= mT < 160 and  50 <= met < 100: SR = 65
        elif ss   and        m < 100 and 120 <= mT < 160 and 100 <= met < 150: SR = 66
        elif ss   and        m < 100 and 120 <= mT < 160 and 150 <= met < 200: SR = 67
        elif ss   and        m < 100 and 120 <= mT < 160 and 200 <= met      : SR = 68
        elif ss   and        m < 100 and 160 <= mT       and  50 <= met < 100: SR = 69
        elif ss   and        m < 100 and 160 <= mT       and 100 <= met < 150: SR = 70
        elif ss   and        m < 100 and 160 <= mT       and 150 <= met < 200: SR = 71
        elif ss   and        m < 100 and 160 <= mT       and 200 <= met      : SR = 72
        elif ss   and 100 <= m       and        mT < 120 and  50 <= met < 100: SR = 73
        elif ss   and 100 <= m       and        mT < 120 and 100 <= met < 150: SR = 74
        elif ss   and 100 <= m       and        mT < 120 and 150 <= met < 200: SR = 75
        elif ss   and 100 <= m       and        mT < 120 and 200 <= met      : SR = 76
        elif ss   and 100 <= m       and 120 <= mT < 160 and  50 <= met < 100: SR = 77
        elif ss   and 100 <= m       and 120 <= mT < 160 and 100 <= met < 150: SR = 78
        elif ss   and 100 <= m       and 120 <= mT < 160 and 150 <= met < 200: SR = 79
        elif ss   and 100 <= m       and 120 <= mT < 160 and 200 <= met      : SR = 80
        elif ss   and 100 <= m       and 160 <= mT       and  50 <= met < 100: SR = 81
        elif ss   and 100 <= m       and 160 <= mT       and 100 <= met < 150: SR = 82
        elif ss   and 100 <= m       and 160 <= mT       and 150 <= met < 200: SR = 83
        elif ss   and 100 <= m       and 160 <= mT       and 200 <= met      : SR = 84

        return SR        


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
            #if pt_sorted[i][0] > 20 and pt_sorted[i][2] > 5 and \
            #   ((abs(tr_sorted[i][1].pdgId)==11 and pt_sorted[i][1] > 15) or \
            #    (abs(tr_sorted[i][1].pdgId)==13 and pt_sorted[i][1] > 10)):
            #if pt_sorted[i][0] > 10 and pt_sorted[i][1] > 10 and pt_sorted[i][2] > 10:
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


    ## listBranches
    ## _______________________________________________________________
    def listBranches(self):
        biglist = [ 
            ("vtxWeight"          + self.label, "F"),
            ("nTriples"           + self.label, "I"),
            ("i1"                 + self.label, "I", 20, "nTriples" + self.label),
            ("i2"                 + self.label, "I", 20, "nTriples" + self.label),
            ("i3"                 + self.label, "I", 20, "nTriples" + self.label),
            ("t1"                 + self.label, "I", 20, "nTriples" + self.label),
            ("t2"                 + self.label, "I", 20, "nTriples" + self.label),
            ("t3"                 + self.label, "I", 20, "nTriples" + self.label),
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
            biglist.append(("mTmin"     + self.systs["JEC"  ][var] + self.label, "F")) 
            biglist.append(("i_mTmin"   + self.systs["JEC"  ][var] + self.label, "I")) 
            biglist.append(("t_mTmin"   + self.systs["JEC"  ][var] + self.label, "I")) 
            biglist.append(("mll"       + self.systs["JEC"  ][var] + self.label, "F")) 
            biglist.append(("i1_mll"    + self.systs["JEC"  ][var] + self.label, "I")) 
            biglist.append(("i2_mll"    + self.systs["JEC"  ][var] + self.label, "I")) 
            biglist.append(("t1_mll"    + self.systs["JEC"  ][var] + self.label, "I")) 
            biglist.append(("t2_mll"    + self.systs["JEC"  ][var] + self.label, "I")) 
            biglist.append(("isOnZ"     + self.systs["JEC"  ][var] + self.label, "I"))
            biglist.append(("hasOSSF"   + self.systs["JEC"  ][var] + self.label, "I"))
            biglist.append(("hasOSOF"   + self.systs["JEC"  ][var] + self.label, "I"))
            biglist.append(("hasSS"     + self.systs["JEC"  ][var] + self.label, "I"))
            biglist.append(("BR"        + self.systs["JEC"  ][var] + self.label, "I"))
            biglist.append(("SR"        + self.systs["JEC"  ][var] + self.label, "I"))
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


    ## mTmin
    ## _______________________________________________________________
    #def mTmin(self, lepst, lepsf, var = 0, excl = []):
    #      list = []
    #      ll = lepst if len(self.trueTriples) > 0 else lepst + lepsf
    #      for i, l in enumerate(ll):
    #          if len(excl) > 0 and l.trIdx in excl: continue
    #          list.append((self.mtW(l.pt, l.phi, var), l.trIdx))
    #      if len(list):
    #          list.sort()
    #          return (list[0][0], list[0][1])
    #      return (0., -1)


    ## mll
    ## _______________________________________________________________
    def mll(self, var = 0):

        ## search for OSSF pair first
        buffer = []
        for (l1, l2, l3) in self.triples:
            leps = [l1, l2, l3]
            buffer.append(self.bestZ1TL(leps, leps))
        
        if len(buffer) and buffer[0][1] != -1:
            buffer.sort()
            return (buffer[0][1], buffer[0][2], buffer[0][3], buffer[0][4], buffer[0][5], 1)

        ## search for OSOF pair second
        buffer = []
        for (l1, l2, l3) in self.triples:
            leps = [l1, l2, l3]
            buffer.append(self.bestZtauTL(leps, leps))
        
        if len(buffer) and buffer[0][1] != -1:
            buffer.sort()
            return (buffer[0][1], buffer[0][2], buffer[0][3], buffer[0][4], buffer[0][5], 0)

        ## no OS pair, take any SS pair from light-flavor leptons
        for (l1, l2, l3) in self.triples:
            if l1.isTau + l2.isTau + l3.isTau > 1: continue
            lep1 = l1; lep2 = l2
            if l1.isTau: lep1 = l2; lep2 = l3
            if l2.isTau: lep2 = l3
            mz = (lep1.p4() + lep2.p4()).M()
            return (mz, lep1.trIdx, lep2.trIdx, lep1.isTau, lep2.isTau, 2)

        ## nothing useful found
        return (-1, -1, -1, 0, 0, -1)



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
        self.ret["t1"                ] = [0]*20
        self.ret["t2"                ] = [0]*20
        self.ret["t3"                ] = [0]*20
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
            self.ret["mTmin"     + self.systs["JEC"  ][var]] = -1.
            self.ret["mll"       + self.systs["JEC"  ][var]] = -1.
            self.ret["i_mTmin"   + self.systs["JEC"  ][var]] = 0
            self.ret["t_mTmin"   + self.systs["JEC"  ][var]] = 0
            self.ret["i1_mll"    + self.systs["JEC"  ][var]] = 0
            self.ret["i2_mll"    + self.systs["JEC"  ][var]] = 0
            self.ret["t1_mll"    + self.systs["JEC"  ][var]] = 0
            self.ret["t2_mll"    + self.systs["JEC"  ][var]] = 0
            self.ret["isOnZ"     + self.systs["JEC"  ][var]] = 0
            self.ret["hasOSSF"   + self.systs["JEC"  ][var]] = 0
            self.ret["hasOSOF"   + self.systs["JEC"  ][var]] = 0
            self.ret["hasSS"     + self.systs["JEC"  ][var]] = 0
            self.ret["BR"        + self.systs["JEC"  ][var]] = 0 
            self.ret["SR"        + self.systs["JEC"  ][var]] = 0 
        for var in self.systs["LEPSF"]: 
            self.ret["leptonSF"  + self.systs["LEPSF"][var]] = [0]*20


    ## setApplication
    ## _______________________________________________________________
    def setApplication(self, whichApplication, filePathFakeRate):

        self.apply            = False
        self.whichApplication = -1

        if   whichApplication == "Fakes": self.whichApplication = self.appl_Fakes
        elif whichApplication == "Flips": self.whichApplication = self.appl_Flips
        elif whichApplication == "Taus" : self.whichApplication = self.appl_Taus
        elif whichApplication == "WZ"   : self.whichApplication = self.appl_WZ
        else                            : raise RuntimeError, 'Unknown whichApplication'

        if self.whichApplication == self.appl_Fakes:
            if filePathFakeRate and self.loadFakeRateHistos(filePathFakeRate):
                self.apply = True
        elif self.whichApplication == self.appl_Flips:
            if filePathFakeRate and self.loadFlipRateHistos(filePathFakeRate):
                self.apply = True
        if not self.apply:
            print 'WARNING: running leptonChoiceEWK in pure tagging mode (no weights applied)'


    ## setAttributes 
    ## _______________________________________________________________
    def setAttributes(self, leps, isTau = False):
        
        for i, l in enumerate(leps): 
            setattr(l, "trIdx", i)
            setattr(l, "isTau", 1 if isTau else 0)



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

        
