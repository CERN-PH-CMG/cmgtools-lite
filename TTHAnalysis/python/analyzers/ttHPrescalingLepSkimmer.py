from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer

import itertools

class ttHPrescalingLepSkimmer( Analyzer ):
    def __init__(self, cfg_ana, cfg_comp, looperName ):
        super(ttHPrescalingLepSkimmer,self).__init__(cfg_ana,cfg_comp,looperName)
        self.prescaleFactor = cfg_ana.prescaleFactor
        self.useEventNumber = getattr(cfg_ana,'useEventNumber',True)
        self.leptons    = getattr(cfg_ana, 'leptons', "selectedLeptons")
        self.leptonSel  = getattr(cfg_ana, 'leptonSelection', None)
        self.minLeptons = getattr(cfg_ana, 'minLeptons', 0)
        self.requireSameSignPair = getattr(cfg_ana,"requireSameSignPair",False)
        self.jets    = getattr(cfg_ana, 'jets', "cleanJets")
        self.jetSel  = getattr(cfg_ana, 'jetSelection', None)
        self.minJets = getattr(cfg_ana, 'minJets', 0)
        self.met    = getattr(cfg_ana, 'met', "met")
        self.minMET = getattr(cfg_ana, 'minMET', 0)
        self.label  = getattr(cfg_ana, 'label', "prescaleFromSkim")
        self.events = 0

    def declareHandles(self):
        super(ttHPrescalingLepSkimmer, self).declareHandles()

    def beginLoop(self, setup):
        super(ttHPrescalingLepSkimmer,self).beginLoop(setup)
        self.counters.addCounter('events')
        count = self.counters.counter('events')
        count.register('all events')
        count.register('accepted (unity / leptons)')
        count.register('accepted (unity / same-sign leps)')
        count.register('accepted (unity / jets)')
        count.register('accepted (unity / met)')
        count.register('accepted (unity)')
        count.register('tested   (prescaled)')
        count.register('accepted (prescaled)')


    def process(self, event):
        counters = self.counters.counter('events')
        counters.inc('all events')
        toBePrescaled = True
        if self.minLeptons > 0:
            leps = getattr(event, self.leptons)
            if self.leptonSel: leps = filter(self.leptonSel, leps)
            if len(leps) >= self.minLeptons:
                if self.requireSameSignPair:
                    if any([(l1.charge() * l2.charge() > 0) for l1,l2 in itertools.combinations(leps,2)]):
                        toBePrescaled = False
                        counters.inc('accepted (unity / same-sign leps)')
                else:
                    toBePrescaled = False
                    counters.inc('accepted (unity / leptons)')
        if self.minJets > 0:
            jets = getattr(event, self.jets)
            if self.jetSel: jets = filter(self.jetSel, jets)
            if len(jets) >= self.minJets:
                toBePrescaled = False
                counters.inc('accepted (unity / jets)')
        if self.minMET > 0:
            met = getattr(event, self.met)
            if met.pt() > self.minMET:
                toBePrescaled = False
                counters.inc('accepted (unity / met)')
        if not toBePrescaled:
            counters.inc('accepted (unity)')
            setattr(event, self.label, 1)
            return True
        counters.inc('tested   (prescaled)')
        self.events += 1
        evno = self.events
        if self.useEventNumber: # use run and LS number multiplied by some prime numbers
            evno = event.input.eventAuxiliary().id().event()*223 + event.input.eventAuxiliary().id().luminosityBlock()*997
        if (evno % self.prescaleFactor == 1):
            counters.inc('accepted (prescaled)')
            setattr(event, self.label, self.prescaleFactor)
            return True
        else:
            return False

