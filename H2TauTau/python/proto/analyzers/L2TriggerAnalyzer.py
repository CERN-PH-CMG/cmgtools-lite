import ROOT
from itertools import product

from PhysicsTools.Heppy.analyzers.core.Analyzer       import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle     import AutoHandle
from PhysicsTools.Heppy.physicsobjects.PhysicsObjects import Jet
from PhysicsTools.HeppyCore.utils.deltar              import deltaR

class L2TriggerAnalyzer(Analyzer):

    def declareHandles(self):
        super(L2TriggerAnalyzer, self).declareHandles()

        self.handles['hltL2TauPixelIsoTagProducer'] = AutoHandle(
            'hltL2TauPixelIsoTagProducer',
            'edm::AssociationVector<edm::RefToBaseProd<reco::Jet>,vector<float>,edm::RefToBase<reco::Jet>,unsigned int,edm::helper::AssociationIdenticalKeyReference>',
            mayFail            = True,
            disableAtFirstFail = False,
            lazy               = False
        )

        self.handles['hltL2TauPixelIsoTagProducerLegacy'] = AutoHandle(
            ('hltL2TauPixelIsoTagProducer', 'legacy'),
            'edm::AssociationVector<edm::RefToBaseProd<reco::Jet>,vector<float>,edm::RefToBase<reco::Jet>,unsigned int,edm::helper::AssociationIdenticalKeyReference>',
            mayFail            = True,
            disableAtFirstFail = False,
            lazy               = False
        )

        self.handles['hltL2TauJetsIso'] = AutoHandle(
            'hltL2TauJetsIso',
            'std::vector<reco::CaloJet>',
            mayFail            = True,
            disableAtFirstFail = False,
            lazy               = False
        )

        self.handles['hltL2TauIsoFilter'] = AutoHandle(
            'hltL2TauIsoFilter',
            'trigger::TriggerFilterObjectWithRefs',
            mayFail            = True,
            disableAtFirstFail = False,
            lazy               = False
        )

        self.handles['hltL2TausForPixelIsolation'] = AutoHandle(
            'hltL2TausForPixelIsolation',
            'std::vector<reco::CaloJet>',
            mayFail            = True,
            disableAtFirstFail = False,
            lazy               = False
        )

    def process(self, event):

        self.readCollections(event.input)

        try:
            event.hltL2TauPixelIsoTagProducerLegacy = self.handles['hltL2TauPixelIsoTagProducerLegacy'].product()
            event.hltL2TauPixelIsoTagProducer       = self.handles['hltL2TauPixelIsoTagProducer'      ].product()
            event.hltL2TauJetsIso                   = self.handles['hltL2TauJetsIso'                  ].product()
            event.hltL2TauIsoFilter                 = self.handles['hltL2TauIsoFilter'                ].product()
            event.hltL2TausForPixelIsolation        = self.handles['hltL2TausForPixelIsolation'       ].product()
        except:
            pass
        
        if self.cfg_ana.verbose:
        
            if hasattr(event, 'hltL2TauPixelIsoTagProducer'      ) or \
               hasattr(event, 'hltL2TauPixelIsoTagProducerLegacy') or \
               hasattr(event, 'hltL2TauJetsIso'                  ) or \
               hasattr(event, 'hltL2TauIsoFilter'                ) or \
               hasattr(event, 'hltL2TausForPixelIsolation'       ):
                
                print '\n\n===================== event', event.eventId
                
                for jet in event.hltL2TausForPixelIsolation:
                    print '\t====>\thltL2TausForPixelIsolation      pt, eta, phi     ', jet.pt(), jet.eta(), jet.phi() 
                
                for j in range(event.hltL2TauPixelIsoTagProducer.size()):
                    jet = event.hltL2TauPixelIsoTagProducer.keyProduct().product().at(j)
                    iso = event.hltL2TauPixelIsoTagProducer.value(j)
                    print '\t====>\thltL2TauPixelIsoTagProducer     pt, eta, phi, iso', jet.pt(), jet.eta(), jet.phi(), iso 
                            
                for jet in event.hltL2TauIsoFilter.jetRefs():
                    print '\t====>\thltL2TauIsoFilter               pt, eta, phi     ', jet.pt(), jet.eta(), jet.phi() 

        self.dRmax = 0.5
        if hasattr(self.cfg_ana, 'dR'):
            self.dRmax = self.cfg_ana.dR

        event.L2jets = []
        
        # stop here if there are no L2 jets
        if not hasattr(event, 'hltL2TauPixelIsoTagProducer'):
            return True

        nL2jets = event.hltL2TauPixelIsoTagProducer.size()        
        
        for l2jIndex in range(nL2jets):
            jet       = event.hltL2TauPixelIsoTagProducer.keyProduct().product().at(l2jIndex)
            iso       = event.hltL2TauPixelIsoTagProducer.value(l2jIndex)
            isolegacy = event.hltL2TauPixelIsoTagProducerLegacy.value(l2jIndex)
            
            l2jet             = Jet(jet)
            l2jet.L2iso       = iso
            l2jet.L2isolegacy = isolegacy
            
            event.L2jets.append(l2jet)
        
        for ti in event.trigger_infos:
            for to, jet in product(ti.objects, event.L2jets):

                dR = deltaR(jet.eta(), jet.phi(), to.eta(), to.phi())
                
                if hasattr(to, 'L2dR'):
                    dRmax = to.L2dR
                else:
                    dRmax = self.dRmax 
                
                if dR < dRmax:
                    to.L2          = jet            
                    to.L2iso       = jet.L2iso      
                    to.L2isolegacy = jet.L2isolegacy
                    to.L2dR        = dR
                
        # stop here if there's no diLepton. Useful for rate studies
        if not hasattr(event, 'diLepton'):
            return True
        
        legs = {event.diLepton.leg1():self.dRmax,
                event.diLepton.leg2():self.dRmax}    
                    
        event.diLepton.leg1().L2          = None
        event.diLepton.leg1().L2iso       = None
        event.diLepton.leg1().L2isolegacy = None

        event.diLepton.leg2().L2          = None
        event.diLepton.leg2().L2iso       = None
        event.diLepton.leg2().L2isolegacy = None
             
        for leg, l2jIndex in product(legs.keys(), range(nL2jets)):               
            dR = deltaR(jet.eta(), jet.phi(), leg.eta(), leg.phi())
            if dR < legs[leg]:
                leg.L2          = jet            
                leg.L2iso       = jet.L2iso      
                leg.L2isolegacy = jet.L2isolegacy
                leg.L2dR        = dR
                legs[leg]       = dR  

        if self.cfg_ana.verbose:
            
            if event.diLepton.leg1().L2:
                print 'leg1 L2 jet pt, eta, phi, iso, dR', event.diLepton.leg1().L2.pt(), event.diLepton.leg1().L2.eta(), event.diLepton.leg1().L2.phi(), event.diLepton.leg1().L2iso, event.diLepton.leg1().L2dR 
            if event.diLepton.leg2().L2:
                print 'leg2 L2 jet pt, eta, phi, iso, dR', event.diLepton.leg2().L2.pt(), event.diLepton.leg2().L2.eta(), event.diLepton.leg2().L2.phi(), event.diLepton.leg2().L2iso, event.diLepton.leg2().L2dR

        return True
