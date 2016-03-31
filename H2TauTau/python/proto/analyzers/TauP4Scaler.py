import os
import ROOT
import array
from collections import OrderedDict

from PhysicsTools.Heppy.analyzers.core.Analyzer       import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle     import AutoHandle
from PhysicsTools.Heppy.physicsobjects.PhysicsObjects import Tau, Jet
from PhysicsTools.HeppyCore.utils.deltar              import cleanObjectCollection, matchObjectCollection

class TauP4Scaler(Analyzer):

    '''Calibrates tau four momentum'''

    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(TauP4Scaler, self).__init__(cfg_ana, cfg_comp, looperName)

        weights = '/'.join( [os.environ['CMSSW_BASE'], 
                             'src', 
                             'CMGTools', 
                             'H2TauTau', 
                             'data', 
                             'tau_energy_scale_calibration_weights.xml'] )

        self.reader = ROOT.TMVA.Reader('Color:Silent')
        
        self.variables = OrderedDict()
        
        self.variables['tau_pt'                     ] = array.array('f',[0])
        self.variables['tau_eta'                    ] = array.array('f',[0])
        self.variables['tau_mass'                   ] = array.array('f',[0])
        self.variables['tau_decayMode'              ] = array.array('f',[0])

        self.variables['tau_charged_iso'            ] = array.array('f',[0])
        self.variables['tau_gamma_iso'              ] = array.array('f',[0])
        self.variables['tau_charged_sig'            ] = array.array('f',[0])
        self.variables['tau_gamma_sig'              ] = array.array('f',[0])

        self.variables['tau_jet_pt'                 ] = array.array('f',[0])
        self.variables['tau_jet_mass'               ] = array.array('f',[0])
        self.variables['tau_jet_nConstituents'      ] = array.array('f',[0])
        self.variables['tau_jet_rawFactor'          ] = array.array('f',[0])
        self.variables['tau_jet_chargedHadronEnergy'] = array.array('f',[0])
        self.variables['tau_jet_neutralHadronEnergy'] = array.array('f',[0])
        self.variables['tau_jet_neutralEmEnergy'    ] = array.array('f',[0])
        self.variables['tau_jet_chargedEmEnergy'    ] = array.array('f',[0])
        
        for k, v in self.variables.items():
            self.reader.AddVariable(k, v)    
        
        self.reader.BookMVA('BDTG', weights)

    def declareHandles(self):
        super(TauP4Scaler, self).declareHandles()

        self.handles['taus'] = AutoHandle(
            'slimmedTaus', 
            'std::vector<pat::Tau>'
        )

        self.handles['jets'] = AutoHandle(
            'slimmedJets',
            'std::vector<pat::Jet>'
        )

        self.handles['puppiMET'] = AutoHandle(
            'slimmedMETsPuppi',
            'std::vector<pat::MET>'
        )

        self.handles['pfMET'] = AutoHandle(
            'slimmedMETs',
            'std::vector<pat::MET>'
        )
        
    def process(self, event):
        '''
        '''

        self.readCollections(event.input)

        taus     = [Tau(tau) for tau in self.handles['taus'].product()]
        jets     = [Jet(jet) for jet in self.handles['jets'].product()]
        pfmet    = self.handles['pfMET'   ].product()[0]
        puppimet = self.handles['puppiMET'].product()[0]
        
        pairs = matchObjectCollection(taus, jets, 0.5 * 0.5)
        
#         import pdb ; pdb.set_trace()
        
        # associating a jet to each lepton
        for tau in taus:
            jet = pairs[tau]
            if jet is None:
                pass
            else:
                tau.jet = jet

        event.calibratedTaus = []
        
        for tau in taus:

            tau.associatedVertex = event.goodVertices[0]

            tau_p4_scale = 1.
            
            if tau.decayMode() in (0, 1, 10) and hasattr(tau, 'jet'):

                self.tauIsoBreakdown(tau)

                self.variables['tau_pt'                     ][0] = tau.pt()               
                self.variables['tau_eta'                    ][0] = tau.eta()              
                self.variables['tau_mass'                   ][0] = tau.mass()             
                self.variables['tau_decayMode'              ][0] = tau.decayMode()        

                self.variables['tau_charged_iso'            ][0] = tau.chargedPtSumIso    
                self.variables['tau_gamma_iso'              ][0] = tau.gammaPtSumIso      
                self.variables['tau_charged_sig'            ][0] = tau.chargedPtSumSignal 
                self.variables['tau_gamma_sig'              ][0] = tau.gammaPtSumSignal   

                self.variables['tau_jet_pt'                 ][0] = tau.jet.pt()           
                self.variables['tau_jet_mass'               ][0] = tau.jet.mass()         
                self.variables['tau_jet_nConstituents'      ][0] = tau.jet.nConstituents()
                self.variables['tau_jet_rawFactor'          ][0] = tau.jet.rawFactor()
                self.variables['tau_jet_chargedHadronEnergy'][0] = tau.jet.chargedHadronEnergy()      
                self.variables['tau_jet_neutralHadronEnergy'][0] = tau.jet.neutralHadronEnergy()      
                self.variables['tau_jet_neutralEmEnergy'    ][0] = tau.jet.neutralEmEnergy()    
                self.variables['tau_jet_chargedEmEnergy'    ][0] = tau.jet.chargedEmEnergy()          

                calibrated_tau_pt = self.reader.EvaluateRegression('BDTG')[0]
                tau_p4_scale = calibrated_tau_pt / tau.pt()

                pfmetP4    = pfmet   .p4()
                puppimetP4 = puppimet.p4()

                # remove pre-calibrated tau from met computation
                pfmetP4    += tau.p4()
                puppimetP4 += tau.p4()
                
                self.scaleP4(tau, tau_p4_scale)
                tau.ptScale = tau_p4_scale

                # include calibrated tau into the met computation
                pfmetP4    -= tau.p4()
                puppimetP4 -= tau.p4()
            
                pfmet   .setP4(pfmetP4   )
                puppimet.setP4(puppimetP4)
            
            event.calibratedTaus.append(tau)
        
        event.calibratedPfMet    = pfmet
        event.calibratedPuppiMet = puppimet

        return True

    def tauIsoBreakdown(self, tau):

        variables = {
            'ptSumIso'           : tau.isolationCands()           ,
            'chargedPtSumIso'    : tau.isolationChargedHadrCands(),
            'gammaPtSumIso'      : tau.isolationGammaCands()      ,
            'neutralPtSumIso'    : tau.isolationNeutrHadrCands()  ,
            'ptSumSignal'        : tau.signalCands()              ,
            'chargedPtSumSignal' : tau.signalChargedHadrCands()   ,
            'gammaPtSumSignal'   : tau.signalGammaCands()         ,
            'neutralPtSumSignal' : tau.signalNeutrHadrCands()     ,
        }

        for k, v in variables.items():
            ptsum = 0.
            for i in v:
                ptsum += i.pt()
            setattr(tau, k, ptsum)

    def scaleP4(self, tau, scale):
       
        modifiedP4 = ROOT.TLorentzVector()
        modifiedP4.SetPtEtaPhiM(
            tau.pt() * scale,
            tau.eta(),
            tau.phi(),
            tau.mass() # do not scale mass
        )
        
        # I love ROOT
        modifiedP4LV = ROOT.LorentzVector(
            modifiedP4.Px(),
            modifiedP4.Py(),
            modifiedP4.Pz(),
            modifiedP4.E(),
        )
        
        tau.setP4(modifiedP4LV)
