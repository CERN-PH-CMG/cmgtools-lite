import math

from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.HeppyCore.statistics.average import Average

from CMGTools.RootTools.statistics.TreeNumpy import TreeNumpy

from ROOT import TFile, TH1F, TLorentzVector


class NJetsAnalyzer(Analyzer):

    '''Saves the number of partons and gen HT from the LHEEventProduct 
    information, and reweights the events if according information present
    in the sample configuration.

    Note that unlike before, the number of partons is calculated directly
    and not taken from the NUP variable inside the LHEEventProduct since the
    latter doesn't account for off-shell Z/W bosons anymore.
    '''

    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(NJetsAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)

        # wpat = re.compile('(DY|W)\d?Jet.*') # match DY1Jet, DYJet, W1Jet, WJet, etc.
        # match = wpat.match(self.cfg_comp.name)
        # self.isWJets = not (match is None)

        # if self.isWJets:
        self.applyWeight = False
        if hasattr(self.cfg_comp, 'nevents') and hasattr(self.cfg_comp, 'fractions'):
            assert(len(self.cfg_comp.nevents) == len(self.cfg_comp.fractions))
            self.ninc = self.cfg_comp.nevents[0]
            self.cfg_comp.nevents[0] = 0.
            self.ni = [frac * self.ninc for frac in self.cfg_comp.fractions]
            self.weighti = []
            for ninc, nexc in zip(self.ni, self.cfg_comp.nevents):
                self.weighti.append(ninc / (ninc + nexc))
            self.applyWeight = True

        self.applyWeightFunc = False

        if hasattr(self.cfg_comp, 'weight_func'):
            self.weight_func = self.cfg_comp.weight_func
            self.applyWeightFunc = True

        self.hasMCProduct = True

    def beginLoop(self, setup):
        super(NJetsAnalyzer, self).beginLoop(setup)
        self.averages.add('NUP', Average('NUP'))
        self.averages.add('NJets', Average('NJets'))
        self.averages.add('NJetWeight', Average('NJetWeight'))
        if self.cfg_comp.isMC:
            self.rootfile = TFile('/'.join([self.dirName,
                                            'NUP.root']),
                                  'recreate')
            self.nup = TH1F('nup', 'nup', 20, 0, 20)
            self.njets = TH1F('njets', 'njets', 10, 0, 10)
            self.tree = TreeNumpy('tree', 'test tree for NJetsAnalyzer')
            if self.cfg_ana.fillTree:
                self.tree.var('njets', int)
                self.tree.var('nup', int)
                self.tree.var('weight')

    def process(self, event):
        event.NUP = -1
        event.genPartonHT = 0.
        event.NJetWeight = 1
        event.geninvmass = -999.

        if not self.cfg_comp.isMC:
            return True

        if not self.hasMCProduct:
            return True

        self.readCollections(event.input)

        self.mchandles['source'].ReallyLoad(event.input)
        if not self.mchandles['source'].isValid():
            self.hasMCProduct = False
            print 'WARNING: No LHEEventProduct from externalLHEProducer present in event'
            print '  (fine for sample directly produced in Pythia)'
            return True

        hep = self.mchandles['source'].product().hepeup()

        # For reference: The following worked in run 1, but for run 2 MC,
        # the intermediate boson is not saved if it's too far off shell...
        # removing the 2 incoming partons, a boson,
        # and the 2 partons resulting from the decay of a boson
        # njets = event.NUP - 5

        event.NJetWeight = 1.

        sumpt = 0.
        outgoing = []
        leptons = []

        # print [(a, b) for a, b in zip(hep.ISTUP, hep.IDUP)]

        for status, pdg, moth, mom in zip(hep.ISTUP, hep.IDUP, hep.MOTHUP, hep.PUP):

            if status == 1 and abs(pdg) in [21, 1, 2, 3, 4, 5]:
                sumpt += math.sqrt(mom.x[0]**2 + mom.x[1]**2)
                outgoing.append(pdg)

            if status == 1 and abs(pdg) in [11, 12, 13, 14, 15, 16]:
                l = TLorentzVector(mom.x[0], mom.x[1], mom.x[2], mom.x[3])
                leptons.append(l)

        njets = len(outgoing)
        event.NUP = njets

        if len(leptons) == 2:
            event.geninvmass = (leptons[0] + leptons[1]).M()
            event.genbosonpt = (leptons[0] + leptons[1]).Pt()

        event.genPartonHT = sumpt

        if self.applyWeight:
            event.NJetWeight = self.weighti[njets]
            event.eventWeight *= event.NJetWeight

            self.averages['NJetWeight'].add(event.NJetWeight)

            if self.cfg_ana.verbose:
                print 'NUP, njets, weight', event.NUP, njets, event.NJetWeight

        if self.applyWeightFunc:
            event.NJetWeight = self.weight_func(njets)

        if self.cfg_ana.fillTree:
            self.tree.reset()
            self.tree.fill('njets', njets)
            self.tree.fill('nup', event.NUP)
            self.tree.fill('weight', event.NJetWeight)
            self.tree.tree.Fill()

        self.averages['NUP'].add(event.NUP)
        self.averages['NJets'].add(njets)

        self.nup.Fill(event.NUP)
        self.njets.Fill(njets)

        return True

    def declareHandles(self):
        '''Reads LHEEventsProduct.'''
        super(NJetsAnalyzer, self).declareHandles()
        self.mchandles['source'] = AutoHandle(
            'externalLHEProducer',
            'LHEEventProduct',
            mayFail=True
        )

    def write(self, setup):
        super(NJetsAnalyzer, self).write(setup)
        if self.cfg_comp.isMC:
            self.rootfile.Write()
            self.rootfile.Close()
