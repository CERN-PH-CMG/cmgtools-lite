from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle

from CMGTools.H2TauTau.proto.analyzers.H2TauTauTreeProducerBase import H2TauTauTreeProducerBase
from CMGTools.H2TauTau.proto.analyzers.TreeVariables            import Variable

class H2TauTauTreeProducerRate(H2TauTauTreeProducerBase):

    '''
    '''

    def __init__(self, *args):
        super(H2TauTauTreeProducerRate, self).__init__(*args)

    def declareHandles(self):
        super(H2TauTauTreeProducerRate, self).declareHandles()

    def declareVariables(self, setup):
        self.bookEvent(self.tree)
        self.var(self.tree, 'tag')
        self.var(self.tree, 'probe')

        # HLT trigger object
        self.bookParticle(self.tree, 'l2_trig_obj')
        
        # L1 particle
        self.bookParticle(self.tree, 'l2_L1')
        self.var(self.tree, 'l1_L1_type')

        # L2 jet matched to HLT objects
        self.bookJet(self.tree, 'l2_L2')
        self.var(self.tree, 'l2_L2_dR')

        # leading L2 jet
        self.bookJet(self.tree, 'lead_L2')

    def process(self, event):

        # needed when doing handle.product(), goes back to
        # PhysicsTools.Heppy.analyzers.core.Analyzer
        self.readCollections(event.input)

        self.tree.reset()

        if not eval(self.skimFunction):
            return False
        
        self.fillEvent(self.tree, event)
        self.fill(self.tree, 'tag', event.tag)
        self.fill(self.tree, 'probe', event.probe)

        for i, jet in enumerate(event.L2jets):
            if i > 0: break
            self.fillJet(self.tree, 'lead_L2', jet)
            

        # consider only events that fired mu + tau
        tis  = [ti for ti in event.trigger_infos if 'HLT_IsoMu17_eta2p1_MediumIsoPFTau35_Trk1_eta2p1_Reg' in ti.name][0]
        if tis.fired:
            # clean trigger objects by muons
            tos = [to for to in ti.objects if abs(to.pdgId()) != 13]
            # sort by most isolated
            try:
                tos.sort(key = lambda to: to.L2iso)
                myto = tos[0] 
                self.fillParticle(self.tree, 'l2_trig_obj', myto)
                self.fillJet(self.tree, 'l2_L2', myto.L2)
                self.fill(self.tree, 'l2_L2_dR', myto.L2dR)
            except:
                print 'WARNING: no L2 match'
                pass
                
        if type(self) is H2TauTauTreeProducerRate:
            self.fillTree(event)

    # event
    def bookEvent(self, tree):
        self.bookGeneric(tree, event_vars)

    def fillEvent(self, tree, event):
        self.fillGeneric(tree, event_vars, event)

    # jet
    def bookJet(self, tree, p_name):
        self.bookParticle(tree, p_name)
        self.bookGeneric(tree, jet_vars, p_name)
        
    def fillJet(self, tree, p_name, jet):
        self.fillParticle(tree, p_name, jet)
        self.fillGeneric(tree, jet_vars, jet, p_name)


global event_vars

event_vars = [
    Variable('run', type=int),
    Variable('lumi', type=int),
    Variable('event', lambda ev : ev.eventId, type=int),
    Variable('bx', lambda ev : (ev.input.eventAuxiliary().bunchCrossing() * ev.input.eventAuxiliary().isRealData()), type=int),
    Variable('orbit_number', lambda ev : (ev.input.eventAuxiliary().orbitNumber() * ev.input.eventAuxiliary().isRealData()), type=int),
    Variable('nPU', lambda ev : ev.nPU if hasattr(ev, 'nPU') else -1, type=int),
    Variable('n_vertices', lambda ev : len(ev.vertices), type=int),
    Variable('rho', lambda ev : ev.rho),
]


global jet_vars

jet_vars = [
    Variable('maxEInEmTowers'        , lambda jet : jet.maxEInEmTowers()        ),
    Variable('maxEInHadTowers'       , lambda jet : jet.maxEInHadTowers()       ),
    Variable('hadEnergyInHO'         , lambda jet : jet.hadEnergyInHO()         ),
    Variable('hadEnergyInHB'         , lambda jet : jet.hadEnergyInHB()         ),
    Variable('hadEnergyInHF'         , lambda jet : jet.hadEnergyInHF()         ),
    Variable('hadEnergyInHE'         , lambda jet : jet.hadEnergyInHE()         ),
    Variable('emEnergyInEB'          , lambda jet : jet.emEnergyInEB()          ),
    Variable('emEnergyInEE'          , lambda jet : jet.emEnergyInEE()          ),
    Variable('emEnergyInHF'          , lambda jet : jet.emEnergyInHF()          ),
    Variable('energyFractionHadronic', lambda jet : jet.energyFractionHadronic()),
    Variable('towersArea'            , lambda jet : jet.towersArea()            ),
    Variable('emEnergyFraction'      , lambda jet : jet.emEnergyFraction()      ),
    Variable('n90'                   , lambda jet : jet.n90()                   ),
    Variable('n60'                   , lambda jet : jet.n60()                   ),
    Variable('etInAnnulus_0p2_0p4'   , lambda jet : jet.etInAnnulus(0.2, 0.4)   ),
    Variable('nCarrying_0p9'         , lambda jet : jet.nCarrying(0.90)         ),
    Variable('nConstituents'         , lambda jet : jet.nConstituents()         ),
    Variable('area'                  , lambda jet : jet.jetArea()               ),
    Variable('L2_iso'                , lambda jet : jet.L2iso                   ),
    Variable('L2_iso_legacy'         , lambda jet : jet.L2isolegacy             ),
]
