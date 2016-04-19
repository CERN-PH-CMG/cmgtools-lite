from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer

from PhysicsTools.HeppyCore.utils.deltar import deltaR

class TauIsolationCalculator(Analyzer):

    '''Gets tau decay mode efficiency weight and puts it in the event'''

    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(TauIsolationCalculator, self).__init__(cfg_ana, cfg_comp, looperName)
    def declareHandles(self):

        super(TauIsolationCalculator, self).declareHandles()

        self.getter = self.cfg_ana.getter if hasattr(self.cfg_ana, 'getter') else lambda event: event.selectedTaus
        
    def beginLoop(self, setup):
        print self, self.__class__
        super(TauIsolationCalculator, self).beginLoop(setup)

    def process(self, event):
        self.readCollections(event.input)

        for tau in self.getter(event):
            puppi_iso_cands = []
            puppi_iso_cands_04 = []
            puppi_iso_cands_03 = []
            isoPtSumOld = 0.
            tau_eta = tau.eta()
            tau_phi = tau.phi()
            # Normal loop crashes for some reason...
            for i_iso in range(len(tau.isolationCands())):
                iso_cand = tau.isolationCands()[i_iso].get()
                isoPtSumOld += tau.isolationCands()[i_iso].pt()

                pdgId = iso_cand.pdgId()
                if abs(pdgId) not in [22, 211]:
                    # print 'Found puppi particle with pdgID', pdgId, 'ignoring...'
                    continue
                    
                puppi_iso_cands.append(iso_cand)
                dr = deltaR(iso_cand.eta(), iso_cand.phi(), tau_eta, tau_phi)
                if dr < 0.4:
                    puppi_iso_cands_04.append(iso_cand)
                if dr < 0.3:
                    puppi_iso_cands_03.append(iso_cand)

            tau.puppi_iso_pt = sum(c_p.pt()*c_p.puppiWeight() for c_p in puppi_iso_cands)
            tau.puppi_iso04_pt = sum(c_p.pt()*c_p.puppiWeight() for c_p in puppi_iso_cands_04)
            tau.puppi_iso03_pt = sum(c_p.pt()*c_p.puppiWeight() for c_p in puppi_iso_cands_03)
            # Add puppi isolation

            self.tauIsoBreakdown(tau)
            
            tau.trigger_iso = (tau.chargedPtSumIso + tau.gammaPtSumIso) < max(2., 0.06 * tau.pt() * (tau.pt() > 40.) ) 
            
            #import pdb ; pdb.set_trace()
            
        return True

    @staticmethod
    def tauIsoBreakdown(tau):

        variables = {
            'ptSumIso'                : tau.isolationCands()           ,
            'chargedPtSumIso'         : tau.isolationChargedHadrCands(),
            'gammaPtSumIso'           : tau.isolationGammaCands()      ,
            'neutralPtSumIso'         : tau.isolationNeutrHadrCands()  ,
            'ptSumSignal'             : tau.signalCands()              ,
            'chargedCandsPtSumSignal' : tau.signalChargedHadrCands()   ,
            'gammaCandsPtSumSignal'   : tau.signalGammaCands()         ,
            'neutralCandsPtSumSignal' : tau.signalNeutrHadrCands()     ,
        }

        for k, v in variables.items():
            ptsum = 0.
            for i in v:
                ptsum += i.pt()
            setattr(tau, k, ptsum)
