from CMGTools.H2TauTau.proto.analyzers.H2TauTauTreeProducer import H2TauTauTreeProducer
from PhysicsTools.Heppy.physicsutils.TauDecayModes import tauDecayModes

class H2TauTauTreeProducerTauTau( H2TauTauTreeProducer ):
  '''Tree producer for the H->tau tau analysis'''
  
  def declareVariables(self, setup):
    
    super(H2TauTauTreeProducerTauTau, self).declareVariables(setup)
    
    self.bookTau(self.tree, 'l1')
    self.bookTau(self.tree, 'l2')
    
    self.bookGenParticle(self.tree, 'l1_gen')
    self.bookGenParticle(self.tree, 'l2_gen')

    self.bookParticle(self.tree, 'l1_gen_vis')
    self.bookParticle(self.tree, 'l2_gen_vis')

    self.var(self.tree, 'l1_gen_decaymode', int)
    self.var(self.tree, 'l2_gen_decaymode', int)
    
  def process(self, event):
             
    super(H2TauTauTreeProducerTauTau, self).process(event)
    
    tau1 = event.diLepton.leg1()
    tau2 = event.diLepton.leg2()
        
    self.fillTau(self.tree, 'l1', tau1 )
    self.fillTau(self.tree, 'l2', tau2 )

    if hasattr(tau1, 'genp') : 
        if tau1.genp: self.fillGenParticle(self.tree, 'l1_gen', tau1.genp )
    if hasattr(tau2, 'genp') : 
        if tau2.genp: self.fillGenParticle(self.tree, 'l2_gen', tau2.genp )

    # save the p4 of the visible tau products at the generator level
    # make sure that the reco tau matches with a gen tau that decays into hadrons

    if tau1.genJet() and hasattr(tau1, 'genp') and tau1.genp and abs(tau1.genp.pdgId()) == 15:
        self.fillParticle(self.tree, 'l1_gen_vis', tau1.physObj.genJet() )
        tau_gen_dm = tauDecayModes.translateGenModeToInt(tauDecayModes.genDecayModeFromGenJet(tau1.physObj.genJet()))
        self.fill(self.tree, 'l1_gen_decaymode', tau_gen_dm)


    if tau2.genJet() and hasattr(tau2, 'genp') and tau2.genp and abs(tau2.genp.pdgId()) == 15:
        self.fillParticle(self.tree, 'l2_gen_vis', tau2.physObj.genJet() )
        tau_gen_dm = tauDecayModes.translateGenModeToInt(tauDecayModes.genDecayModeFromGenJet(tau2.physObj.genJet()))
        self.fill(self.tree, 'l2_gen_decaymode', tau_gen_dm)
      
    self.fillTree(event)
