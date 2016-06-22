from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer

class monoJetCtrlFatJetSkimmer( Analyzer ):
    def __init__(self, cfg_ana, cfg_comp, looperName ):
        super(monoJetCtrlFatJetSkimmer,self).__init__(cfg_ana,cfg_comp,looperName)
        self.ptCuts = cfg_ana.ptCuts if hasattr(cfg_ana, 'ptCuts') else []
        self.ptCuts += 10*[-1.]

        #self.idCut = cfg_ana.idCut if (getattr(cfg_ana, 'idCut', '') != '') else "True"
        #self.idFunc = eval("lambda lepton : "+self.idCut);

    def declareHandles(self):
        super(monoJetCtrlFatJetSkimmer, self).declareHandles()

    def beginLoop(self, setup):
        super(monoJetCtrlFatJetSkimmer,self).beginLoop(setup)
        self.counters.addCounter('events')
        count = self.counters.counter('events')
        count.register('all events')
        count.register('vetoed events')
        count.register('accepted events')


    def process(self, event):
        self.readCollections( event.input )
        self.counters.counter('events').inc('all events')

        fatJets = []
        for jet, ptCut in zip(event.fatJets, self.ptCuts):
            #if not self.idFunc(lep):
            #    continue
            if jet.pt() > ptCut: 
                fatJets.append(jet)

        ret = False 
        if len(fatJets) >= self.cfg_ana.minFatJets:
            ret = True
        if len(fatJets) > self.cfg_ana.maxFatJets:
            if ret: self.counters.counter('events').inc('vetoed events')
            ret = False

        if ret: self.counters.counter('events').inc('accepted events')
        return ret
