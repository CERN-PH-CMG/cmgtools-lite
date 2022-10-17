from CMGTools.TTHAnalysis.treeReAnalyzer import Collection, deltaR
from CMGTools.TTHAnalysis.tools.collectionSkimmer import CollectionSkimmer
import ROOT, os


class SOSLepCleaner:
    def __init__(self,label=""):
        self.label = label
        self.branches =  [ ("nLepSel"+self.label, "I") ]
        self.branches += [ ("iLepSel"+self.label, "I", 20, "nLepSel"+self.label) ]
        self.branches += [ ("m2lSel"+self.label, "F") ]
        if "/functions_cc.so" not in ROOT.gSystem.GetLibraries(): 
            ROOT.gROOT.ProcessLine(".L %s/src/CMGTools/TTHAnalysis/python/plotter/functions.cc+" % os.environ['CMSSW_BASE']);
        self.m2l = ROOT.mass_2
    def listBranches(self):
        return self.branches
    def init(self,tree):
        self._ttreereaderversion = tree._ttreereaderversion
        for B in "nLepGood",: setattr(self, B, tree.valueReader(B))
        for B in "pt", "eta", "phi", "mass", "RelIsoMIV04", "sip3d" : setattr(self,"LepGood_"+B, tree.arrayReader("LepGood_"+B))
    def __call__(self,event):
        ## Init
        if event._tree._ttreereaderversion > self._ttreereaderversion: 
            self.init(event._tree)
        LepSel = []; 
        pt = self.LepGood_pt.At
        eta = self.LepGood_eta.At
        phi = self.LepGood_phi.At
        mass = self.LepGood_mass.At
        riso = self.LepGood_RelIsoMIV04.At
        sip = self.LepGood_sip3d.At
        for iL in xrange(self.nLepGood.Get()[0]):
            if pt(iL)*riso(iL) < 10 and sip(iL) < 8:
                LepSel.append(iL)
        ret = { 'nLepSel'+self.label : len(LepSel),
                'iLepSel'+self.label : LepSel }
        if len(LepSel) >= 2:
            ret['m2lSel'] = self.m2l(pt(LepSel[0]),eta(LepSel[0]),phi(LepSel[0]),mass(LepSel[0]),
                                     pt(LepSel[1]),eta(LepSel[1]),phi(LepSel[1]),mass(LepSel[1]))
        return ret

class SOSLepCleanerIP3D:
    def __init__(self,mu_ip3d=9e9,el_ip3d=9e9,mu_sip3d=9e9,el_sip3d=9e9,label=""):
        self.label = label
        self.branches =  [ ("nLepSel"+self.label, "I") ]
        self.branches += [ ("iLepSel"+self.label, "I", 20, "nLepSel"+self.label) ]
        self.branches += [ ("m2lSel"+self.label, "F") ]
        self.branches += [ ("m3lSel"+self.label, "F") ]
        self.branches += [ ("mZ1Sel"+self.label, "F") ]
        self.branches += [ ("minMllSFOSSel"+self.label, "F") ]
        
        if "/functions_cc.so" not in ROOT.gSystem.GetLibraries(): 
            ROOT.gROOT.ProcessLine(".L %s/src/CMGTools/TTHAnalysis/python/plotter/functions.cc+" % os.environ['CMSSW_BASE']);
        self.m2l = ROOT.mass_2
        self.m3l = ROOT.mass_3
        self.mu_sip3d = mu_sip3d
        self.el_sip3d = el_sip3d
        self.mu_ip3d = mu_ip3d
        self.el_ip3d = el_ip3d
    def listBranches(self):
        return self.branches
    def init(self,tree):
        self._ttreereaderversion = tree._ttreereaderversion
        for B in "nLepGood",: setattr(self, B, tree.valueReader(B))
        for B in "pt", "eta", "phi", "mass", "ip3d", "sip3d", "jetBTagCSV", "pdgId" : setattr(self,"LepGood_"+B, tree.arrayReader("LepGood_"+B))
    def __call__(self,event):
        ## Init
        if event._tree._ttreereaderversion > self._ttreereaderversion: 
            self.init(event._tree)
        LepSel = []; 
        leps = [l for l in Collection(event,"LepGood","nLepGood")]
        lepsSel = [];
        pt = self.LepGood_pt.At
        eta = self.LepGood_eta.At
        phi = self.LepGood_phi.At
        mass = self.LepGood_mass.At
        pdgId = self.LepGood_pdgId.At
        ip = self.LepGood_ip3d.At
        sip = self.LepGood_sip3d.At
        csv = self.LepGood_jetBTagCSV.At
        for iL in xrange(self.nLepGood.Get()[0]):
            if not( sip(iL) < 8 and csv(iL) < 0.46 ): continue
            if not( sip(iL) < (self.mu_sip3d if abs(pdgId(iL)) == 13 else self.el_sip3d) ): continue
            if not( abs(ip(iL)) < (self.mu_ip3d  if abs(pdgId(iL)) == 13 else self.el_ip3d)  ): continue
            LepSel.append(iL)
            lepsSel.append(leps[iL])
            if len(LepSel) == 3: break
        ret = { 'nLepSel'+self.label : len(LepSel),
                'iLepSel'+self.label : LepSel }
        if len(LepSel) >= 2:
            ret['m2lSel'] = self.m2l(pt(LepSel[0]),eta(LepSel[0]),phi(LepSel[0]),mass(LepSel[0]),
                                     pt(LepSel[1]),eta(LepSel[1]),phi(LepSel[1]),mass(LepSel[1]))
        if len(LepSel) >= 3:
            ret['m3lSel'] = self.m3l(pt(LepSel[0]),eta(LepSel[0]),phi(LepSel[0]),mass(LepSel[0]),
                                     pt(LepSel[1]),eta(LepSel[1]),phi(LepSel[1]),mass(LepSel[1]),
                                     pt(LepSel[2]),eta(LepSel[2]),phi(LepSel[2]),mass(LepSel[2]))            
        ret['mZ1Sel'] = bestZ1TL(lepsSel, lepsSel)
        ret['minMllSFOSSel'] = minMllTL(lepsSel, lepsSel, paircut = lambda l1,l2 : l1.pdgId == -l2.pdgId)     
        return ret


class SOSLepCleanerIP:
    def __init__(self,label=""):
        self.label = label
        self.branches =  [ ("nLepSel"+self.label, "I") ]
        self.branches += [ ("iLepSel"+self.label, "I", 20, "nLepSel"+self.label) ]
        self.branches += [ ("m2lSel"+self.label, "F") ]
        if "/functions_cc.so" not in ROOT.gSystem.GetLibraries(): 
            ROOT.gROOT.ProcessLine(".L %s/src/CMGTools/TTHAnalysis/python/plotter/functions.cc+" % os.environ['CMSSW_BASE']);
        self.m2l = ROOT.mass_2
    def listBranches(self):
        return self.branches
    def init(self,tree):
        self._ttreereaderversion = tree._ttreereaderversion
        for B in "nLepGood",: setattr(self, B, tree.valueReader(B))
        for B in "pt", "eta", "phi", "mass", "dxy", "dz", "sip3d", "jetBTagCSV" : setattr(self,"LepGood_"+B, tree.arrayReader("LepGood_"+B))
    def __call__(self,event):
        ## Init
        if event._tree._ttreereaderversion > self._ttreereaderversion: 
            self.init(event._tree)
        LepSel = []; 
        pt = self.LepGood_pt.At
        eta = self.LepGood_eta.At
        phi = self.LepGood_phi.At
        mass = self.LepGood_mass.At
        dxy = self.LepGood_dxy.At
        dz = self.LepGood_dz.At
        sip = self.LepGood_sip3d.At
        csv = self.LepGood_jetBTagCSV.At
        for iL in xrange(self.nLepGood.Get()[0]):
            if abs(dxy(iL)) < 0.01 and abs(dz(iL)) < 0.01 and sip(iL) < 8 and csv(iL) < 0.46:
                LepSel.append(iL)
                if len(LepSel) == 2: break
        ret = { 'nLepSel'+self.label : len(LepSel),
                'iLepSel'+self.label : LepSel }
        if len(LepSel) >= 2:
            ret['m2lSel'] = self.m2l(pt(LepSel[0]),eta(LepSel[0]),phi(LepSel[0]),mass(LepSel[0]),
                                     pt(LepSel[1]),eta(LepSel[1]),phi(LepSel[1]),mass(LepSel[1]))
        return ret

class SOSJetCleaner:
    def __init__(self,label="",leptons="LepSel",lepPtCut=20):
        self.label = label
        self.floats = [ ]
        self.ints = [ ]
        self.branches =  [ ("nJetSel"+self.label, "I") ]
        self.branches += [ ("JetSel"+self.label+"_"+V, "F", 20, "nJetSel"+self.label) for V in ["pt"]+self.floats]
        self.branches += [ ("JetSel"+self.label+"_"+V, "I", 20, "nJetSel"+self.label) for V in ["id"]+self.ints]
        self.branches += [ ("htJet25Sel"+self.label, "F") ]
        self.branches += [ (("nBJet%s%dSel"%(W,P))+self.label, "I") for W in ("Loose","Medium") for P in (25,40)]
        self.leptons = leptons
        self.lepPtCut = lepPtCut
    def listBranches(self):
        return self.branches
    def init(self,tree):
        self._ttreereaderversion = tree._ttreereaderversion
        for B in "nLepGood",: setattr(self, B, tree.valueReader(B))
        for B in "pt", "eta", "phi": setattr(self,"LepGood_"+B, tree.arrayReader("LepGood_"+B))
        for J in "Jet", "DiscJet":
            for B in "n"+J,: setattr(self, B, tree.valueReader(B))
            for B in "pt", "eta", "phi","btagCSV","id": setattr(self,J+"_"+B, tree.arrayReader(J+"_"+B))
    def __call__(self,event):
        ## Init
        if event._tree._ttreereaderversion > self._ttreereaderversion: 
            self.init(event._tree)
        iLepSel = getattr(event, "i"+self.leptons)
        leps = [ (self.LepGood_pt.At(i),self.LepGood_eta.At(i),self.LepGood_phi.At(i)) for i in iLepSel ]
        jets = []; 
        for J in "Jet","DiscJet":
            nJ = getattr(self, "n"+J).Get()[0]
            if nJ == 0: continue
            pt = getattr(self, J+"_pt").At
            eta = getattr(self, J+"_eta").At
            phi = getattr(self, J+"_phi").At
            jid = getattr(self, J+"_id").At
            btag = getattr(self, J+"_btagCSV").At
            copys = [ getattr(self, J+"_"+V).At for V in self.ints + self.floats ]
            for iJ in xrange(nJ):
                jets.append( (pt(iJ),eta(iJ),phi(iJ),jid(iJ),btag(iJ), [c(iJ) for c in copys]) )
        badjets = []
        for (lpt,leta,lphi) in leps:
            if lpt <= self.lepPtCut: continue
            imin, drmin = -1, 0.4
            for (iJ,J) in enumerate(jets):
                dr = deltaR(leta,lphi,J[1],J[2])
                if dr < drmin: (imin,drmin) = (iJ,dr)
            if imin >= 0: badjets.append(imin)
        jets = [J for (i,J) in enumerate(jets) if i not in badjets and J[0] > 25 and abs(J[1]) < 2.4 and J[3] > 0 ]

        ret = { "nJetSel"+self.label : len(jets) }
        ret["htJet25Sel"+self.label] = sum(l[0] for l in leps) + sum(J[0] for J in jets)

        ret["nBJetLoose25Sel"+self.label]  =  sum((J[4]>0.46) for J in jets)
        ret["nBJetMedium25Sel"+self.label] =  sum((J[4]>0.80) for J in jets)
        ret["nBJetLoose40Sel"+self.label]  =  sum((J[4]>0.46 and J[0]>40) for J in jets)
        ret["nBJetMedium40Sel"+self.label] =  sum((J[4]>0.80 and J[0]>40) for J in jets)
        
        ret["JetSel"+self.label+"_pt"] = [ J[0] for J in jets ]
        ret["JetSel"+self.label+"_id"] = [ J[3] for J in jets ]
        for i,V in enumerate(self.ints+self.floats):
            ret["JetSel"+self.label+"_"+V] = [ J[5][i] for J in jets ]

        return ret

MODULES = [
    ('leps', lambda : SOSLepCleaner()),
    ('jets', lambda : SOSJetCleaner()),
    ('ipleps', lambda : SOSLepCleanerIP()),
    ('ip3dleps', lambda : SOSLepCleanerIP3D(mu_ip3d=0.006,el_ip3d=0.008)),
    ('sip3dleps', lambda : SOSLepCleanerIP3D(mu_sip3d=1.8,el_sip3d=1.8)),
    ('both3dleps', lambda : SOSLepCleanerIP3D(mu_ip3d=0.01,el_ip3d=0.01,mu_sip3d=2.0,el_sip3d=2.0)),
    ('both3dloose', lambda : SOSLepCleanerIP3D(mu_ip3d=0.0175,el_ip3d=0.0175,mu_sip3d=2.5,el_sip3d=2.5)),
    ('ipjets', lambda : SOSJetCleaner(lepPtCut=0)),
]



def bestZ1TL(lepsl,lepst,cut=lambda lep:True):
      pairs = []
      for l1 in lepst:
        if not cut(l1): continue
        for l2 in lepsl:
            if not cut(l2): continue
            if l1.pdgId == -l2.pdgId:
               mz = (l1.p4() + l2.p4()).M()
               diff = abs(mz-91.188)
               pairs.append( (diff,mz) )
      if len(pairs):
          pairs.sort()
          return pairs[0][1]
      return 0.

def minMllTL(lepsl, lepst, bothcut=lambda lep:True, onecut=lambda lep:True, paircut=lambda lep1,lep2:True):
        pairs = []
        for l1 in lepst:
            if not bothcut(l1): continue
            for l2 in lepsl:
                if l2 == l1 or not bothcut(l2): continue
                if not onecut(l1) and not onecut(l2): continue
                if not paircut(l1,l2): continue
                mll = (l1.p4() + l2.p4()).M()
                pairs.append(mll)
        if len(pairs):
            return min(pairs)
        return -1
