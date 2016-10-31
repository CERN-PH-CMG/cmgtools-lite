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


    ## __call__
    ## _______________________________________________________________
    def __call__(self, event):

        self.resetMemory()
        self.collectObjects(event)
        self.writeTauSel()
        return self.ret



    ## collectObjects
    ## _______________________________________________________________
    def collectObjects(self, event):

        ## light leptons
        self.leps       = [l             for l  in Collection(event, "LepGood", "nLepGood")  ]
        self.lepsFO     = [self.leps[il] for il in list(getattr   (event, "iF" + self.inputlabel))[0:int(getattr(event,"nLepFO"+self.inputlabel))]]
        self.lepsT      = [self.leps[il] for il in list(getattr   (event, "iT" + self.inputlabel))[0:int(getattr(event,"nLepTight"+self.inputlabel))]]

        ## taus
        self.inclusivetaus       = [t          for t  in Collection(event, "TauGood" , "nTauGood"  )]
        self.inclusivetaus.append( [t          for t  in Collection(event, "TauOther", "nTauOther" )] )
        self.tausFO = self.inclusiveTaus
        # not sure I really need to define tausFO

        ## Non-tau-cleaned jets
        self.uncleanJets = [t            for t  in Collection(event, "leptonJetReCleanerSusyEWK3LnoTauCleaning", "nJet")]
        # jetsc[var] = [j for j in Collection(event,"Jet"+self.systsJEC[_var],"nJet"+self.systsJEC[_var])]
        # jetsd[var] = [j for j in Collection(event,"DiscJet"+self.systsJEC[_var],"nDiscJet"+self.systsJEC[_var])]


        ## FO, both flavors
        self.setAttributes(event, self.tausFO, event.isData)
        self.tausFO.sort(key = lambda x: x.conePt, reverse=True)



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
        for i in range(len(collection)):
            it = collection[i]
            if abs(it.pt-object.pt) < delta and abs(it.eta-object.eta)<delta and abs(it.phi-object.phi)<delta and abs(it.mass-object.mass)<delta: return i
        return -1


    ## listBranches
    ## _______________________________________________________________
    def listBranches(self):

        biglist = [
            ("nTauSel"     , "I")]

        for var in ["pt", "eta", "phi", "mass", "conePt", "dxy", "dz", "sip3d", "miniRelIso", "relIso", "ptratio", "ptrel", "mva"]:
            biglist.append(("TauSel_" + var, "F", 4))
        for var in ["pdgId", "isTight", "mcMatchId", "mcMatchAny", "mcPromptGamma", "mcUCSX", "trIdx"]:
            biglist.append(("TauSel_" + var, "I", 4))
  
        #for var in self.systsJEC:
        #    biglist.append(("mT_3l"       + self.systsJEC[var], "F"))

        return biglist


    ## resetMemory
    ## _______________________________________________________________
    def resetMemory(self):

        self.ret = {};

        self.ret["is_3l"                ] = 0
        self.ret["nOSSF_3l"             ] = 0
        self.ret["nOSLF_3l"             ] = 0
        self.ret["nOSTF_3l"             ] = 0
        self.ret["mll_3l"               ] = 0
        self.ret["m3L"                  ] = 0
        self.ret["is_4l"                ] = 0
        self.ret["nOSSF_4l"             ] = 0
        self.ret["nOSLF_4l"             ] = 0
        self.ret["nOSTF_4l"             ] = 0
        self.ret["mll_4l"               ] = 0
        self.ret["m4L"                  ] = 0


        self.ret["idMVA"              ] = 0 
        self.ret["idMVANewDM"         ] = 0
        self.ret["idCI3hit"           ] = 0
        self.ret["idMVAOldDMRun2"     ] = 0
        self.ret["idMVAOldDMRun2dR03" ] = 0
        self.ret["idAntiMu"           ] = 0
        self.ret["idAntiE"            ] = 0


        self.ret["nOS"   ] = 0
        self.ret["mll"   ] = [0]*20
        self.ret["mll_i1"] = [-1]*20
        self.ret["mll_i2"] = [-1]*20

        self.ret["nLepSel"] = 0
        # MVA is duplicate for var in ["pt", "eta", "phi", "mass", "conePt", "dxy", "dz", "sip3d", "miniRelIso", "relIso", "ptratio", "ptrel", "mva"]:
        for var in ["pt", "eta", "phi", "mass", "conePt", "dxy", "dz", "sip3d", "miniRelIso", "relIso", "ptratio", "ptrel"]:
            self.ret["LepSel_" + var] = [0.]*20
        for var in ["pdgId", "isTight", "mcMatchId", "mcMatchAny", "mcPromptGamma", "mcUCSX", "trIdx"]:
            self.ret["LepSel_" + var] = [0 ]*20

        for var in self.systsJEC:
            self.ret["mT_3l"       + self.systsJEC[var]] = 0.
            self.ret["mT2L_3l"     + self.systsJEC[var]] = 0.  
            self.ret["mT2T_3l"     + self.systsJEC[var]] = 0. 
            self.ret["mT_4l"       + self.systsJEC[var]] = 0.
            self.ret["mT2L_4l"     + self.systsJEC[var]] = 0.  
            self.ret["mT2T_4l"     + self.systsJEC[var]] = 0. 
            self.ret["mT_3l_gen"   + self.systsJEC[var]] = 0.
            self.ret["mT2L_3l_gen" + self.systsJEC[var]] = 0.  
            self.ret["mT2T_3l_gen" + self.systsJEC[var]] = 0. 
            self.ret["mT_4l_gen"   + self.systsJEC[var]] = 0.
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
                # Duplicate setattr(l, "mva"          , tau.idMVAOldDMRun2 if not tau is None else 0 )
                setattr(l, "idMVA"             , tau.idMVA              if not tau is None else 0 ) 
                setattr(l, "idMVANewDM"        , tau.idMVANewDM         if not tau is None else 0 )
                setattr(l, "idCI3hit"          , tau.idCI3hit           if not tau is None else 0 )
                setattr(l, "idMVAOldDMRun2"    , tau.idMVAOldDMRun2     if not tau is None else 0 )
                setattr(l, "idMVAOldDMRun2dR03", tau.idMVAOldDMRun2dR03 if not tau is None else 0 )
                setattr(l, "idAntiMu"          , tau.idAntiMu           if not tau is None else 0 )
                setattr(l, "idAntiE"           , tau.idAntiE            if not tau is None else 0 )


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


    ## writeTauSel
    ## _______________________________________________________________
    def writeTauSel(self):

        self.ret["nTauSel"] = len(self.tauSelFO)
        for i, l in enumerate(self.tauSelFO):
            if i == 8: break # only keep the first 8 entries
            # MVA is duplicatefor var in ["pt", "eta", "phi", "mass", "conePt", "dxy", "dz", "sip3d", "miniRelIso", "relIso", "ptratio", "ptrel", "mva"]:
            for var in ["pt", "eta", "phi", "mass", "conePt", "dxy", "dz", "sip3d", "miniRelIso", "relIso", "ptratio", "ptrel", "idMVA", "idMVANewDM", "idCI3hit", "idMVAOldDMRun2", "idMVAOldDMRun2dR03", "idAntiMu", "idAntiE"]:
                self.ret["TauSel_" + var][i] = getattr(l, var, 0)
            for var in ["pdgId", "isTight", "mcMatchId", "mcMatchAny", "mcPromptGamma", "mcUCSX", "trIdx"]:
                self.ret["TauSel_" + var][i] = int(getattr(l, var, 0))


        #all = []
        #for os in self.OS:
        #    all.append((0 if os.isSF else 1, 1 if os.wTau else 0, os.diff, os)) # priority to SF, then light, then difference to target
        #if all:
        #    all.sort()
        #    self.ret["nOS"] = len(all)
        #    for i,os in enumerate(all):
        #        self.ret["mll"][i] = os[3].mll
        #        self.ret["mll_i1"][i] = self.lepSelFO.index(os[3].l1)
        #        self.ret["mll_i2"][i] = self.lepSelFO.index(os[3].l2)



## _susyEWK_tauId_CBloose
## _______________________________________________________________
def _susyEWK_tauId_CBloose(tau):
    return (tau.pt > 20 and abs(tau.eta)<2.3 and abs(tau.dxy)<1000 and abs(tau.dz)<0.2 and tau.idMVAOldDMRun2 >= 1 and tau.idDecayMode and tau.idAntiE >= 2 and tau.idAntiMu >= 1)


## _susyEWK_tauId_CBtight
## _______________________________________________________________
def _susyEWK_tauId_CBtight(tau):
    if not _susyEWK_tauId_CBloose(tau): return False
    return (tau.idMVAOldDMRun2 >= 4)




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

