import array
import ROOT

from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.HeppyCore.utils.deltar import deltaPhi

import PhysicsTools.HeppyCore.framework.config as cfg

from ROOT.heppy import Davismt2
davismt2 = Davismt2()


class MT2Analyzer(Analyzer):

    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(MT2Analyzer, self).__init__(cfg_ana, cfg_comp, looperName)
        self.jetPt = cfg_ana.jetPt

    def declareHandles(self):
        super(MT2Analyzer, self).declareHandles()
       # genJets
        self.handles['genJets'] = AutoHandle('slimmedGenJets', 'std::vector<reco::GenJet>')
        self.handles['met'] = AutoHandle(self.cfg_ana.metCollection, 'std::vector<pat::MET>')

    def beginLoop(self, setup):
        super(MT2Analyzer, self).beginLoop(setup)
        self.counters.addCounter('pairs')
        count = self.counters.counter('pairs')
        count.register('all events')

    def computeMT2(self, visaVec, visbVec, metVec):

        metVector = array.array('d', [0., metVec.px(), metVec.py()])
        visaVector = array.array('d', [0., visaVec.px(), visaVec.py()])
        visbVector = array.array('d', [0., visbVec.px(), visbVec.py()])

        davismt2.set_momenta(visaVector, visbVector, metVector)
        davismt2.set_mn(0)

        return davismt2.get_mt2()


    def computeVisMT2(self, visaVec, visbVec):
        metVector = array.array('d', [0., -(visaVec.px()+visbVec.px()), -(visaVec.py()+visbVec.py())])
        visaVector = array.array('d', [0., visaVec.px(), visaVec.py()])
        visbVector = array.array('d', [0., visbVec.px(), visbVec.py()])

        davismt2.set_momenta(visaVector, visbVector, metVector)
        davismt2.set_mn(0)

        return davismt2.get_mt2()

 
    def makeMT2(self, event):
        rawmet = ROOT.pat.MET(self.handles['met'].product()[0])

        mt2 = self.computeMT2(event.leg1, event.leg2, rawmet)
        setattr(event, "mt2"+self.cfg_ana.collectionPostFix+'_rawpfmet', mt2)

        pfmet = event.pfmet
        mt2 = self.computeMT2(event.leg1, event.leg2, pfmet)
        setattr(event, "mt2"+self.cfg_ana.collectionPostFix, mt2)

        mt2_lep = self.computeVisMT2(event.leg1, event.leg2)
        setattr(event, "mt2"+self.cfg_ana.collectionPostFix+"_lep", mt2_lep)


        mva_met = event.diLepton.met()
        mt2_mvamet = self.computeMT2(event.leg1, event.leg2, mva_met)
        setattr(event, "mt2"+self.cfg_ana.collectionPostFix+"_mvamet", mt2_mvamet)

    def calculateSUSYVars(self, event):
        met = ROOT.pat.MET(self.handles['met'].product()[0])
        mva_met = event.diLepton.met()

        event.minDphiMETJets = min(deltaPhi(met.phi(), jet.phi()) for jet in event.cleanJets30) if event.cleanJets30 else -999.
        event.minDphiMVAMETJets = min(deltaPhi(mva_met.phi(), jet.phi()) for jet in event.cleanJets30)if event.cleanJets30 else -999.

    def process(self, event):
        self.readCollections(event.input)

        self.makeMT2(event)
        self.calculateSUSYVars(event)

        return True


setattr(MT2Analyzer, "defaultConfig", cfg.Analyzer(
    class_object=MT2Analyzer,
    metCollection="slimmedMETs",
    collectionPostFix="",
    doOnlyDefault=True,
)
)
