from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer

from CMGTools.H2TauTau.proto.analyzers.HTTGenAnalyzer import HTTGenAnalyzer

class HTTGenMatcher(Analyzer):

    '''Add generator information to hard leptons.
    '''
    def declareHandles(self):
        super(HTTGenMatcher, self).declareHandles()

    def process(self, event):

        self.l1 = event.diLepton.leg1()
        self.l2 = event.diLepton.leg2()

        HTTGenAnalyzer.genMatch(event, self.l1, event.ptSelGentauleps, event.ptSelGenleps, event.ptSelGenSummary)
        HTTGenAnalyzer.genMatch(event, self.l2, event.ptSelGentauleps, event.ptSelGenleps, event.ptSelGenSummary)

        HTTGenAnalyzer.attachGenStatusFlag(self.l1)
        HTTGenAnalyzer.attachGenStatusFlag(self.l2)

        if hasattr(event, 'selectedTaus'):
            for tau in event.selectedTaus:
                HTTGenAnalyzer.genMatch(event, tau, event.ptSelGentauleps, event.ptSelGenleps, event.ptSelGenSummary)
