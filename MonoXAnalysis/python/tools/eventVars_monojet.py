from CMGTools.TTHAnalysis.treeReAnalyzer import *
from CMGTools.MonoXAnalysis.tools.PileUpReWeighter import PileUpReWeighter
from CMGTools.MonoXAnalysis.tools.BTagWeightCalculator import BTagWeightCalculator
from PhysicsTools.Heppy.physicsutils.PuJetIDWP import PuJetIDWP
import types

BTagReweight74X = lambda : BTagWeightCalculator("/afs/cern.ch/work/e/emanuele/public/monox/leptonsf/csv_rwt_fit_hf_2015_11_20.root",
                                                "/afs/cern.ch/work/e/emanuele/public/monox/leptonsf/csv_rwt_fit_lf_2015_11_20.root")

class EventVarsMonojet:
    def __init__(self):
        self.branches = [ "nMu10V", "nMu20T", "nEle10V", "nEle40T", "nTau18V", "nGamma15V", "nGamma175T", "nBTag15",
                          "dphijj", "dphijm", "weight", "events_ntot", "recoil_pt", "recoil_phi","SF_BTag"
                          ]
        vbfHiggsToInvVars = [ "dphijmAllJets", "vbfTaggedJet_deltaEta", "vbfTaggedJet_invMass", 
                              "vbfTaggedJet_leadJetPt", "vbfTaggedJet_trailJetPt", "vbfTaggedJet_leadJetEta", "vbfTaggedJet_trailJetEta" 
                              ]  
        # number of VBF tagged jets, pt > 30, |eta| < 4.7; 
        # dPhi(jet,MET) using all jets, not just the leading 4
        self.branches = self.branches + vbfHiggsToInvVars
        btagreweight = BTagReweight74X()
        self._btagreweight = (btagreweight() if type(btagreweight) == types.FunctionType else btagreweight)
        self._btagreweight.btag = "btagCSV"
    def initSample(self,region,sample_nevt):
        self.region = region
        self.sample_nevt = sample_nevt        
    def listBranches(self):
        biglist = [ ("nJetClean", "I"), ("nFatJetClean","I"), ("nTauClean", "I"), ("nLepSel", "I"),
                    ("iL","I",10,"nLepSel"), ("iJ","I",10,"nJetClean"), ("iT","I",3,"nTauClean"),
                    ("iFJ","I",10,"nFatJetClean"), ("nJetCleanCentral", "I"), ("nTauClean18V", "I") ] 
        for jfloat in "pt eta phi mass btagCSV rawPt leadClean".split():
            biglist.append( ("JetClean"+"_"+jfloat,"F",10,"nJetClean") )
        for fjfloat in "pt eta phi prunedMass tau2 tau1".split():
            biglist.append( ("FatJetClean"+"_"+fjfloat,"F",10,"nFatJetClean") )
        for tfloat in "pt eta phi".split():
            biglist.append( ("TauClean"+"_"+tfloat,"F",3,"nTauClean") )
        self.branches = self.branches + biglist
        return self.branches[:]
    # physics object multiplicity with the monojet analysis specific selections
    def lepIdVeto(self,lep):
        if lep.pt <= 10: return False
        if abs(lep.pdgId) == 13:
            if abs(lep.eta) > 2.4: return False
            return lep.relIso04 < 0.25
        elif abs(lep.pdgId) == 11:
            if abs(lep.etaSc) > 2.5: return False
            return lep.relIso03 < (0.126 if abs(lep.etaSc)<1.479 else 0.144)
    def lepIdTight(self,lep):
        if abs(lep.pdgId) == 13:
            if lep.pt <= 20: return False
            return abs(lep.eta) < 2.4 and lep.tightId >=1  and lep.relIso04 < 0.15
        elif abs(lep.pdgId) == 11:
            if lep.relIso03 > (0.0354 if abs(lep.etaSc)<1.479 else 0.0646): return False
            return lep.pt > 40 and abs(lep.etaSc) < 2.5 and lep.tightId >=3
    def tauIdVeto(self,tau):
        if tau.pt <= 18 or abs(tau.eta) > 2.3: return False
        return tau.idDecayMode > 0.5 and tau.isoCI3hit < 5.0
    def gammaIdVeto(self,gamma):
        return gamma.pt > 15 and abs(gamma.etaSc) < 2.5
    def gammaIdTight(self,gamma):
        return gamma.pt > 175 and abs(gamma.etaSc) < 1.4442 and gamma.idCutBased>=2
    def leadJetCleaning(self,jet):
        return jet.chHEF > 0.1 and jet.neHEF < 0.8
    def metNoPh(self,met,photons):
        px = met.Px() + sum([p.p4().Px() for p in photons])
        py = met.Py() + sum([p.p4().Py() for p in photons])
        ret = ROOT.TVector3()
        ret.SetXYZ(px,py,0.)
        return ret
    def BTagEventReweight(self,jets,rwtKind='final',rwtSyst='nominal',mcOnly=True):
        # for j in jets:
        #     print "    single wgt for jpt=%.3f jeta=%.3f, mcFlav=%d, btag=%.3f, SF=%.3f" % (j.pt, j.eta, j.mcFlavour, j.btagCSV, self._btagreweight.calcJetWeight(j,rwtKind,rwtSyst) )
        return self._btagreweight.calcEventWeight(jets, rwtKind, rwtSyst)
    def PtEtaPhi3V(self,pt,eta,phi):
        return ROOT.TVector3(pt*cos(phi),pt*sin(phi),pt*sinh(eta))
    def __call__(self,event):
        # prepare output
        ret = {}; jetret = {}; fatjetret = {}; tauret = {}
        ret['weight'] = event.xsec * 1000 * event.genWeight / self.sample_nevt if event.run == 1 else 1.0
        ret['events_ntot'] = self.sample_nevt
        leps = [l for l in Collection(event,"LepGood","nLepGood")]
        ret['nMu10V'] = sum([(abs(l.pdgId)==13 and int(self.lepIdVeto(l))) for l in leps ])
        ret['nMu20T'] = sum([(abs(l.pdgId)==13 and int(self.lepIdTight(l))) for l in leps ])
        ret['nEle10V'] = sum([(abs(l.pdgId)==11 and int(self.lepIdVeto(l))) for l in leps ])
        ret['nEle40T'] = sum([(abs(l.pdgId)==11 and int(self.lepIdTight(l))) for l in leps ])
        taus = [t for t in Collection(event,"TauGood","nTauGood")]
        ret['nTau18V'] = sum([(int(self.tauIdVeto(t))) for t in taus ])
        photons = [p for p in Collection(event,"GammaGood","nGammaGood")]
        ret['nGamma15V'] = sum([(int(self.gammaIdVeto(p))) for p in photons ])
        ret['nGamma175T'] = sum([(int(self.gammaIdTight(p))) for p in photons ])
        # event variables for the monojet analysis
        jets = [j for j in Collection(event,"Jet","nJet")]
        jetsFwd = [j for j in Collection(event,"JetFwd","nJetFwd")]
        alljets = jets + jetsFwd
        njet = len(jets)
        fatjets = [f for f in Collection(event,"FatJet","nFatJet")]
        photonsT = [p for p in photons if self.gammaIdTight(p)]
        #print "check photonsT size is ", len(photonsT), " and nGamma175T = ",ret['nGamma175T']
        electrons3V=[self.PtEtaPhi3V(l.pt,l.eta,l.phi) for l in leps if (abs(l.pdgId)==11 and self.lepIdVeto(l)) ] 
        pfmet = self.PtEtaPhi3V(event.met_pt,0.,event.met_phi)
        if self.region == 'VE' and len(electrons3V)>1: # if there are >1 loose electrons, the event is vetoed for W->enu, can only belong to Z->ee
            recoil = electrons3V[0] + electrons3V[1] + pfmet
            (met,metphi) = (recoil.Pt(),recoil.Phi())
        elif self.region == 'VE' and len(electrons3V)>0:
            recoil = electrons3V[0] + pfmet
            (met,metphi) = (recoil.Pt(),recoil.Phi())
        elif self.region == 'GJ' and len(photonsT)>0:
            photon1 = self.PtEtaPhi3V(photonsT[0].pt,photonsT[0].eta,photonsT[0].phi)
            recoil = photon1 + pfmet
            (met,metphi) = (recoil.Pt(),recoil.Phi())
        else:
            recoil = self.PtEtaPhi3V(event.metNoMu_pt,0.,event.metNoMu_phi)

        (met,metphi) = (recoil.Pt(), recoil.Phi())
        ret['recoil_pt'] = met
        ret['recoil_phi'] = metphi

        ### lepton-jet cleaning
        # Define the loose leptons to be cleaned
        ret["iL"] = []
        for il,lep in enumerate(leps):
            if self.lepIdVeto(lep):
                ret["iL"].append(il)
        ret["nLepSel"] = len(ret["iL"])
        # Define cleaned jets 
        ret["iJ"] = []; 
        # 0. mark each identified jet as clean
        puId76X = PuJetIDWP()
        for j in alljets: 
            # remove PU jet ID for the time being
            # j._clean = True if (puId76X.passWP(j,"loose") and j.id > 0.5) else False
            j._clean = True if j.id > 0.5 else False
            j._central = True if (abs(j.eta) < 2.5) else False
        # 1. associate to each loose lepton its nearest jet 
        for il in ret["iL"]:
            lep = leps[il]
            best = None; bestdr = 0.4
            for j in alljets:
                dr = deltaR(lep,j)
                if dr < bestdr:
                    best = j; bestdr = dr
            if best is not None: best._clean = False
        # 2. compute the jet list
        nJetCleanCentral=0
        nJetCleanFwd=0
        for ij,j in enumerate(alljets):
            if not j._clean: continue
            ret["iJ"].append(ij)
        # 3. sort the jets by pt
        ret["iJ"].sort(key = lambda idx : alljets[idx].pt, reverse = True)
        # 4. compute the variables
        for jfloat in "pt eta phi mass btagCSV rawPt leadClean".split():
            jetret[jfloat] = []
        dphijj = 999
        dphijm = 999
        dphijmAllJets = 999
        ijc = 0
        nAllJets30 = 0
        for idx in ret["iJ"]:
            jet = alljets[idx]
            # only save in the jetClean collection the jets with pt > 30 GeV
            if jet.pt < 30: continue
            nAllJets30 += 1
            if jet._central: nJetCleanCentral += 1
            else: nJetCleanFwd += 1
            for jfloat in "pt eta phi mass btagCSV rawPt".split():
                jetret[jfloat].append( getattr(jet,jfloat) )
            jetret["leadClean"].append( self.leadJetCleaning(jet) )
            if ijc==1 and jet._central: dphijj = deltaPhi(alljets[ret["iJ"][0]].phi,jet.phi)
            ijc += 1
            # use both central and fwd jets to compute deltaphi(jet,met)_min
            dphijmAllJets = min(dphijmAllJets,abs(deltaPhi(jet.phi,metphi))) 
            if nAllJets30 < 5: dphijm = min(dphijm,abs(deltaPhi(jet.phi,metphi)))
        ret["nJetClean"] = nJetCleanCentral+nJetCleanFwd
        ret['dphijj'] = dphijj
        ret['dphijm'] = dphijm
        ret['dphijmAllJets'] = dphijmAllJets 
        # 5. compute the sums 
        ret["nJetCleanCentral"] = 0
        ret["nBTag15"] = 0
        lowptjets = []
        for j in jets: # these are all central
            if not j._clean: continue
            if j.pt > 30:
                ret["nJetCleanCentral"] += 1
            if j.pt > 15:
                lowptjets.append(j)
                if j.btagCSV > 0.800:
                    ret["nBTag15"] += 1

        ret["vbfTaggedJet_deltaEta"] = -1
        ret["vbfTaggedJet_invMass"] = -1
        ret["vbfTaggedJet_leadJetPt"] = -1
        ret["vbfTaggedJet_trailJetPt"] = -1
        ret["vbfTaggedJet_leadJetEta"] = 999
        ret["vbfTaggedJet_trailJetEta"] = 999
        DeltaEtaMax = -1 
        for i in alljets:
            for j in alljets:
                if i.pt < j.pt: continue   # this way we sort by pt and avoid self or double counting
                if not i._clean or not j._clean: continue
                if i.pt < 70 or j.pt < 50: continue
                if i.eta*j.eta > 0: continue
                DeltaEta = abs(i.eta - j.eta)
                if DeltaEta > DeltaEtaMax:
                    DeltaEtaMax = DeltaEta
                    jet1 = ROOT.TLorentzVector()
                    jet1.SetPtEtaPhiM(i.pt,i.eta,i.phi,0)
                    jet2 = ROOT.TLorentzVector()
                    jet2.SetPtEtaPhiM(j.pt,j.eta,j.phi,0)
                    jet1plus2 = jet1 + jet2
                    ret["vbfTaggedJet_invMass"] = jet1plus2.Mag()
                    ret["vbfTaggedJet_leadJetPt"] = jet1.Pt()
                    ret["vbfTaggedJet_trailJetPt"] = jet2.Pt()
                    ret["vbfTaggedJet_leadJetEta"] = jet1.Eta()
                    ret["vbfTaggedJet_trailJetEta"] =jet2.Eta()
                    ret["vbfTaggedJet_deltaEta"] = DeltaEtaMax
                
        ret["SF_BTag"] = self.BTagEventReweight(lowptjets) if event.run == 1 else 1.0

        ### fat-jet cleaning
        ret['iFJ'] = []
        # 1. clean the fatjets from close leptons
        for ij,j in enumerate(fatjets):
            j._clean = True if j.id > 0.5 else False
            for il in ret["iL"]:
                lep = leps[il]
                if deltaR(lep,j) < 0.8: j._clean = False
            if j._clean: ret['iFJ'].append(ij)
        # 2. sort the fatjets by pt 
        ret['iFJ'].sort(key = lambda idx : fatjets[idx].pt, reverse = True)
        # 3. compute the cleaned fatjet variables
        for jfloat in "pt eta phi prunedMass tau2 tau1".split():
            fatjetret[jfloat] = []
        for idx in ret['iFJ']:
            jet = fatjets[idx]
            for jfloat in "pt eta phi prunedMass tau2 tau1".split():
                fatjetret[jfloat].append( getattr(jet,jfloat) )
        # 4. compute the sums
        ret["nFatJetClean"] = len(ret['iFJ'])

        ### muon-tau cleaning
        # Define cleaned taus
        ret["iT"] = []; 
        # 0. mark each tau as clean
        for t in taus: t._clean = True
        # 1. associate to each loose lepton its nearest tau 
        for il in ret["iL"]:
            lep = leps[il]
            best = None; bestdr = 0.4
            for t in taus:
                dr = deltaR(lep,t)
                if dr < bestdr:
                    best = t; bestdr = dr
            if best is not None: best._clean = False
        # 2. compute the tau list
        for it,t in enumerate(taus):
            if not t._clean: continue
            ret["iT"].append(it)
        # 3. sort the taus by pt
        ret["iT"].sort(key = lambda idx : taus[idx].pt, reverse = True)
        # 4. compute the variables
        for tfloat in "pt eta phi".split():
            tauret[tfloat] = []
        for idx in ret["iT"]:
            tau = taus[idx]
            for tfloat in "pt eta phi".split():
                tauret[tfloat].append( getattr(tau,tfloat) )
        ret["nTauClean"] = len(ret['iT'])
        # 5. compute the sums 
        ret["nTauClean18V"] = 0
        for t in taus:
            if not t._clean: continue
            if not self.tauIdVeto(t): continue
            ret["nTauClean18V"] += 1

        ### return
        fullret = {}
        for k,v in ret.iteritems():
            fullret[k] = v
        for k,v in jetret.iteritems():
            fullret["JetClean_%s" % k] = v
        for k,v in fatjetret.iteritems():
            fullret["FatJetClean_%s" % k] = v
        for k,v in tauret.iteritems():
            fullret["TauClean_%s" % k] = v
        return fullret

if __name__ == '__main__':
    from sys import argv
    file = ROOT.TFile(argv[1])
    tree = file.Get("tree")
    tree.vectorTree = True
    class Tester(Module):
        def __init__(self, name):
            Module.__init__(self,name,None)
            self.sf = EventVarsMonojet()
        def analyze(self,ev):
            if ev.metNoMu_pt < 200: return True
            print "\nrun %6d lumi %4d event %d: metNoMu %d" % (ev.run, ev.lumi, ev.evt, ev.metNoMu_pt)
            print self.sf(ev)
    el = EventLoop([ Tester("tester") ])
    el.loop([tree], maxEvents = 50)

        
