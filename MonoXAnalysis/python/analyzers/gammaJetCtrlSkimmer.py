from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer

class gammaJetCtrlSkimmer( Analyzer ):
    def __init__(self, cfg_ana, cfg_comp, looperName ):
        super(gammaJetCtrlSkimmer,self).__init__(cfg_ana,cfg_comp,looperName)
        self.photonPtCut = cfg_ana.photonPtCut if hasattr(cfg_ana, 'photonPtCut') else []
        self.jetPtCut = cfg_ana.jetPtCut if hasattr(cfg_ana, 'jetPtCut') else []

        self.photonIdCut = cfg_ana.photonIdCut if (getattr(cfg_ana, 'photonIdCut', '') != '') else "True"
        self.idFunc = eval("lambda photon : "+self.photonIdCut);

    def declareHandles(self):
        super(gammaJetCtrlSkimmer, self).declareHandles()

    def beginLoop(self, setup):
        super(gammaJetCtrlSkimmer,self).beginLoop(setup)
        self.counters.addCounter('events')
        count = self.counters.counter('events')
        count.register('all events')
        count.register('accepted events')


    def process(self, event):
        self.readCollections( event.input )
        self.counters.counter('events').inc('all events')

        
        photons = []
        for pho in event.selectedPhotons:
            if not self.idFunc(pho):
                continue
            if pho.pt() > self.photonPtCut: 
                photons.append(pho)

        jets = []
        allJets = event.cleanJets + event.cleanJetsFwd + event.fatJets
        for jet in allJets:
            if jet.pt() > self.jetPtCut:
                jets.append(jet)

        ret = False 
        if len(photons) >= self.cfg_ana.minPhotons and len(jets) >= self.cfg_ana.minJets:
            ret = True

        if ret: self.counters.counter('events').inc('accepted events')
        return ret
