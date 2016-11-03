import math
import re

from ROOT import gSystem
from ROOT import LorentzVector
from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer

gSystem.Load("libCMGToolsH2TauTau")

from ROOT import HTTRecoilCorrector as RC

class RecoilCorrector(Analyzer):
    '''Corrects MVA MET recoil.
    '''

    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(RecoilCorrector, self).__init__(cfg_ana, cfg_comp, looperName)

        self.rcMVAMET = RC('CMGTools/H2TauTau/data/recoilMvaMEt_76X_newTraining_MG5.root')
        self.rcPFMET = RC('CMGTools/H2TauTau/data/recoilPFMEt_76X_MG5.root')

        wpat = re.compile('W\d?Jet.*')
        match = wpat.match(self.cfg_comp.name)
        self.isWJets = not (match is None)

        # Apply to signal, DY, and W+jets samples
        self.apply = 'Higgs' in self.cfg_comp.name or 'DY' in self.cfg_comp.name or self.isWJets


    def getGenP4(self, event):
        leptons_prompt = [p for p in event.genParticles if abs(p.pdgId()) in [11, 12, 13, 14] and p.fromHardProcessFinalState()]
        leptons_prompt_vis = [p for p in leptons_prompt if abs(p.pdgId()) not in [12, 14]]

        taus_prompt = [p for p in event.genParticles if p.statusFlags().isDirectHardProcessTauDecayProduct()]

        taus_prompt_vis = [p for p in taus_prompt if abs(p.pdgId()) not in [12, 14, 16]]

        if 'DY' in self.cfg_comp.name or 'Higgs' in self.cfg_comp.name or 'WJ' in self.cfg_comp.name:
            if len(leptons_prompt) != 2 and len(taus_prompt) < 2:
                print 'ERROR: No 2 prompt leptons found'
                # import pdb; pdb.set_trace()

        vis = leptons_prompt_vis + taus_prompt_vis
        all = leptons_prompt + taus_prompt

        if len(vis) == 0 or len(all) == 0:
            return 0., 0., 0., 0.

        def p4sum(ps):
            if not ps:
                return None
            p4 = ps[0].p4()
            for i in xrange(len(ps) - 1):
                p4 += ps[i + 1].p4()
            return p4

        taus = []
        for t in taus_prompt:
            if t.mother().pdgId() == 15:
                taus.append(t.mother())
                break

        for t in taus_prompt:
            if t.mother().pdgId() == -15:
                taus.append(t.mother())
                break

        p4 = p4sum(all)
        p4_vis = p4sum(vis)

        event.parentBoson = p4
        event.parentBoson.detFlavour = 0

        return p4.px(), p4.py(), p4_vis.px(), p4_vis.py()


    def process(self, event):
        if not self.cfg_comp.isMC:
            return

        # Calculate generator four-momenta even if not applying corrections
        # to save them in final trees
        gen_z_px, gen_z_py, gen_vis_z_px, gen_vis_z_py = self.getGenP4(event)

        if not self.apply:
            return

        dil = event.diLepton

        n_jets_30 = len(event.cleanJets30)
        
        if self.isWJets:
            n_jets_30 += 1


        # Correct MVA MET
        px_old = dil.met().px()
        py_old = dil.met().py()

        # Correct by mean and resolution as default (otherwise use .Correct(..))
        new = self.rcMVAMET.CorrectByMeanResolution(
            px_old, 
            py_old, 
            gen_z_px,    
            gen_z_py,    
            gen_vis_z_px,    
            gen_vis_z_py,    
            n_jets_30,   
        )

        px_new, py_new = new.first, new.second

        dil.met().setP4(LorentzVector(px_new, py_new, 0., math.sqrt(px_new*px_new + py_new*py_new)))

        # print 'px old - new', px_old, dil.met().px()
        # print 'py old - new', py_old, dil.met().py()

        # Correct PF MET
        pfmet_px_old = event.pfmet.px()
        pfmet_py_old = event.pfmet.py()

        # Correct by mean and resolution as default (otherwise use .Correct(..))
        new = self.rcPFMET.CorrectByMeanResolution(
            pfmet_px_old, 
            pfmet_py_old, 
            gen_z_px,    
            gen_z_py,    
            gen_vis_z_px,    
            gen_vis_z_py,    
            n_jets_30,   
        )

        px_new, py_new = new.first, new.second

        event.pfmet.setP4(LorentzVector(px_new, py_new, 0., math.sqrt(px_new*px_new + py_new*py_new)))

