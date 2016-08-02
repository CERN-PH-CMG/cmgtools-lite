from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.HeppyCore.utils.deltar import deltaR2
import math

##__________________________________________________________________||
class NIsrAnalyzer(Analyzer):

    def process(self, event):

        #Can only be performed on MC
        if not self.cfg_comp.isMC: return True

        event.nIsr = 0

        for jet in event.cleanJetsAll:

            if jet.pt()<30.0: continue
            if abs(jet.eta())>2.4: continue
            matched = False
            for mc in event.genParticles:
                if matched: break
                if (mc.status()!=23 or abs(mc.pdgId())>5): continue
                momid = abs(mc.mother().pdgId())
                if not (momid==6 or momid==23 or momid==24 or momid==25 or momid>1e6): continue
                    #check against daughter in case of hard initial splitting
                for idau in range(mc.numberOfDaughters()):
                    dR = math.sqrt(deltaR2(jet.eta(),jet.phi(), mc.daughter(idau).p4().eta(),mc.daughter(idau).p4().phi()))
                    if dR<0.3:
                        matched = True
                        break
            if not matched:
                event.nIsr+=1
        pass

        return True
 

##__________________________________________________________________||
