import ROOT

from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.HeppyCore.statistics.counter import Counter, Counters
from PhysicsTools.HeppyCore.utils.deltar import *
import PhysicsTools.HeppyCore.framework.config as cfg

class badMuonAnalyzerMoriond2017( Analyzer ):

    def __init__(self, cfg_ana, cfg_comp, looperName ):
        super(badMuonAnalyzerMoriond2017,self).__init__(cfg_ana,cfg_comp,looperName)
        self.minMuPt = cfg_ana.minMuPt
        self.selectClones = cfg_ana.selectClones
        self.muons = cfg_ana.muons
        self.vertices = cfg_ana.vertices
        self.flagName = self.name+'_'+cfg_ana.postFix if cfg_ana.postFix!='' else self.name

    def declareHandles(self):
        super(badMuonAnalyzerMoriond2017, self).declareHandles()
        self.handles['muons'] = AutoHandle(self.cfg_ana.muons,"std::vector<pat::Muon>")
        self.handles['vertices']         = AutoHandle( self.vertices, 'std::vector<reco::Vertex>')

    def outInOnly(self,mu):
        tk = mu.innerTrack().get();
        return tk.algoMask().count() == 1 and tk.isAlgoInMask(tk.muonSeededStepOutIn);
    def preselection(self, mu): 
        return (not(self.selectClones) or self.outInOnly(mu));
    def tighterId(self, mu): 
        return mu.isMediumMuon() and mu.numberOfMatchedStations() >= 2; 
    def tightGlobal(self, mu):
        return mu.isGlobalMuon() and (mu.globalTrack().hitPattern().muonStationsWithValidHits() >= 3 and mu.globalTrack().normalizedChi2() <= 20);
    def safeId(self, mu): 
        if (mu.muonBestTrack().ptError() > 0.2 * mu.muonBestTrack().pt()): return False;
        return mu.numberOfMatchedStations() >= 1 or self.tightGlobal(mu);
    def partnerId(self, mu):
        return mu.pt() >= 10 and mu.numberOfMatchedStations() >= 1;


    def beginLoop(self, setup):
        super(badMuonAnalyzerMoriond2017,self).beginLoop( setup )

    def process(self, event):
        self.readCollections( event.input )

        muons       = self.handles['muons'].product() 
        allvertices = self.handles['vertices'].product() 

        goodMuon = []

        if len(allvertices) < 1: raise RuntimeError
        PV = allvertices[0].position()
    
        bad_muons = [] 
        clone_muons = [] 
        for mu in muons:
            if (not(mu.isPFMuon()) or mu.innerTrack().isNull()):
                goodMuon.append(-1); # bad but we don't care
                continue;
            if (self.preselection(mu)):
                dxypv = abs(mu.innerTrack().dxy(PV));
                dzpv  = abs(mu.innerTrack().dz(PV));
                if (self.tighterId(mu)):
                    ipLoose = ((dxypv < 0.5 and dzpv < 2.0) or mu.innerTrack().hitPattern().pixelLayersWithMeasurement() >= 2);
                    goodMuon.append(ipLoose or (not(self.selectClones) and self.tightGlobal(mu)));
                elif (self.safeId(mu)):
                    ipTight = (dxypv < 0.2 and dzpv < 0.5);
                    goodMuon.append(ipTight);
                else:
                    goodMuon.append(0);
            else:
                goodMuon.append(3); # maybe good, maybe bad, but we don't care

        out = []
        n = len(muons)
        for i in xrange(n):
            if (muons[i].pt() < self.minMuPt or goodMuon[i] != 0): continue;
            bad_muons.append( muons[i] )
            bad = True;
            if (self.selectClones):
                bad = False; # unless proven otherwise
                n1 = muons[i].numberOfMatches(ROOT.reco.Muon.SegmentArbitration);
                for j in xrange(n):
                    if (j == i or goodMuon[j] <= 0 or not(self.partnerId(muons[j]))): continue
                    n2 = muons[j].numberOfMatches(ROOT.reco.Muon.SegmentArbitration);
                    if (deltaR(muons[i],muons[j]) < 0.4 or (n1 > 0 and n2 > 0 and ROOT.muon.sharedSegments(muons[i],muons[j]) >= 0.5*min(n1,n2))):
                        clone_muons.append( muons[i] )
                        bad = True;
                        break;
            if (bad):
                out.append(muons[i]);
                
        setattr( event, self.flagName,              len(bad_muons)==0 )
        setattr( event, self.flagName+"_badMuons",  bad_muons )
        return True

setattr(badMuonAnalyzerMoriond2017,"defaultConfig", cfg.Analyzer(
        class_object = badMuonAnalyzerMoriond2017,
        muons = 'slimmedMuons',
        vertices         = 'offlineSlimmedPrimaryVertices',
        minMuPt = 20,
        selectClones = True,
        postFix = '',
        )
)
