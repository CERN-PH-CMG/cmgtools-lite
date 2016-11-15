from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
#from CMGTools.RootTools.fwlite.AutoHandle import AutoHandle
from PhysicsTools.HeppyCore.utils.deltar import *
from PhysicsTools.Heppy.physicsutils.genutils import *

class susyLeptonMatchAnalyzer( Analyzer ):
    def __init__(self, cfg_ana, cfg_comp, looperName ):
        super(susyLeptonMatchAnalyzer,self).__init__(cfg_ana,cfg_comp,looperName)
        self.bottoms=[5,511,521,531,533,535,551,553 ]
        self.charms=[4,411,421,441,443,431,433 ]
        self.lights=[1,2,3,111,211,130,210,321 ]
        self.promptMothers=[23,24,-24,1000024,-1000024]
        self.collection = self.cfg_ana.collection
        self.deltaR     = float(self.cfg_ana.deltaR)
        self.statusOne  = self.cfg_ana.statusOne

    def declareHandles(self):
        super(susyLeptonMatchAnalyzer, self).declareHandles()
      
    def beginLoop(self, setup):
        super(susyLeptonMatchAnalyzer,self).beginLoop(setup)

    def isFromGamma(self,particle,gid=22, done={}):
        for i in xrange( particle.numberOfMothers() ): 
            mom  = particle.mother(i)
            momid = abs(mom.pdgId())
            if momid == gid: 
                return True
        return False

    def SUSYMatchLeptons(self, event):
        
        leps = getattr(event, self.collection, event.inclusiveLeptons)
        genPs=[]
        genPsIdxs={}
        for idx,x in enumerate(event.genParticles):
            if x.status() == 1 or x.status() == 2 or x.status() == 71:
                genPs.append(x)
                genPsIdxs[idx]=len(genPsIdxs)

        def lepMatch(rec, gen):
            if self.statusOne and gen.status() !=1: return False
            if abs(rec.pdgId()) != abs(gen.pdgId()): return False
            return True
        matchLep = matchObjectCollection3(leps,genPs, 
                                          deltaRMax = self.deltaR, filter = lepMatch)
        
        def generalMatch(rec, gen):
            if gen.status() !=1 and gen.status() !=71: return False
            return True
        matchPart = matchObjectCollection3(leps,genPs, 
                                           deltaRMax = self.deltaR, filter = generalMatch)
        
        for il, lep in  enumerate(leps):
            gen = matchLep[lep] if matchLep[lep] else matchPart[lep]
            code=-1
            if not gen: 
                lep.mcUCSXMatchId = -1
                continue
            
            prompt = gen.isPromptFinalState() or gen.isDirectPromptTauDecayProductFinalState() or gen.isHardProcess() 
            motherId=-9999
            grandMotherId=-9999
            moms=realGenMothers(gen)
            if len(moms)==1:
                motherId = abs(moms[0].pdgId())
                gmoms = realGenMothers(moms[0])
                if len(gmoms)==1:
                    grandMotherId = abs(gmoms[0].pdgId())
            if gen.pdgId()==22 or (motherId==22 and gen.pdgId()==lep.pdgId() ):
                if prompt: code= 4
                else: code= -1

            if prompt or ((abs(gen.pdgId())==abs(lep.pdgId()) or abs(gen.pdgId())==15 ) and ((motherId in self.promptMothers) or (abs(motherId)==15 and (grandMotherId in self.promptMothers)) ) ) :
                if gen.pdgId()*lep.pdgId()>0: code= 0
                else : code= 1
            
            if (abs(gen.pdgId()) in self.bottoms) or (motherId in self.bottoms) : code= 3
            if (abs(gen.pdgId()) in self.charms) or (motherId in self.charms) : code= 3
            if (abs(gen.pdgId()) in self.lights) or (motherId in self.lights) : code= 2
            lep.mcUCSXMatchId = code
            
    def process(self, event):
        self.readCollections(event.input)

        if not self.cfg_comp.isMC: return True

        self.SUSYMatchLeptons(event)

        return True
