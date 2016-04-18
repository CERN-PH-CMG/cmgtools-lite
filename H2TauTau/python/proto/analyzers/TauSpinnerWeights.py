import math
import numpy
from DataFormats.FWLite import Handle, Runs
from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle


class TauSpinnerWeights( Analyzer ):
    '''Retrieves the weights that have been produced by running TauSpinner and puts them in the event'''

    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(TauSpinnerWeights,self).__init__(cfg_ana, cfg_comp, looperName)

        self.TauSpinnerWTisValid = -999
        self.TauSpinnerWT = -999
        self.TauSpinnerWThminus = -999
        self.TauSpinnerWThplus = -999
        self.TauSpinnerTauPolFromZ = -999
        self.TauSpinnerWRight = -999
        self.TauSpinnerWLeft = -999
        self.TauSpinnerIsRightLeft = -999


    def beginLoop(self, setup):
        print self, self.__class__
        super(TauSpinnerWeights, self).beginLoop(setup)
        self.counters.addCounter('TauSpinnerWeights')
        count = self.counters.counter('TauSpinnerWeights')
        count.register('all events')
        count.register('events with TauSpinner weights')
        
                
    def declareHandles(self):
        super(TauSpinnerWeights,self).declareHandles()
        self.handles['TauSpinnerWTisValid'] = AutoHandle(
                ('TauSpinnerReco', 'TauSpinnerWTisValid'), 'bool' )
        self.handles['TauSpinnerWT'] = AutoHandle(
		('TauSpinnerReco', 'TauSpinnerWT'), 'double' )
        self.handles['TauSpinnerWThminus'] = AutoHandle(
		('TauSpinnerReco','TauSpinnerWThminus'), 'double' )
        self.handles['TauSpinnerWThplus'] = AutoHandle(
                ('TauSpinnerReco','TauSpinnerWThplus'), 'double' )
        self.handles['TauSpinnerTauPolFromZ'] = AutoHandle(
		('TauSpinnerReco','TauSpinnerTauPolFromZ'), 'double' )
        self.handles['TauSpinnerWRight'] = AutoHandle(
		('TauSpinnerReco','TauSpinnerWRight'), 'double' )
        self.handles['TauSpinnerWLeft'] = AutoHandle(
		('TauSpinnerReco','TauSpinnerWLeft'), 'double' )
        self.handles['TauSpinnerIsRightLeft'] = AutoHandle(
		('TauSpinnerReco','TauSpinnerIsRightLeft'), 'double' )


    def process(self, event):

        event.TauSpinnerWTisValid = -999
        event.TauSpinnerWT = -999
        event.TauSpinnerWThminus = -999
        event.TauSpinnerWThplus = -999
        event.TauSpinnerTauPolFromZ = -999
        event.TauSpinnerWRight = -999
        event.TauSpinnerWLeft = -999
        event.TauSpinnerIsRightLeft = -999

        self.readCollections( event.input )

        self.counters.counter('TauSpinnerWeights').inc('all events')
        try:
            valid = self.handles['TauSpinnerWTisValid'].product()
            WT = self.handles['TauSpinnerWT'].product()
            WThminus = self.handles['TauSpinnerWThminus'].product()
            WThplus = self.handles['TauSpinnerWThplus'].product()
            TauPolFromZ = self.handles['TauSpinnerTauPolFromZ'].product()
            WRight = self.handles['TauSpinnerWRight'].product()
            WLeft = self.handles['TauSpinnerWLeft'].product()
            IsRightLeft = self.handles['TauSpinnerIsRightLeft'].product()
        except RuntimeError:
            print 'WARNING TauSpinnerWeights, cannot find the weights in the event'
            return False

        event.TauSpinnerWTisValid = valid[0]
        event.TauSpinnerWT =  WT[0] 
        event.TauSpinnerWThminus = WThminus[0] 
        event.TauSpinnerWThplus = WThplus[0] 
        event.TauSpinnerTauPolFromZ = TauPolFromZ[0] 
        event.TauSpinnerWRight = WRight[0] 
        event.TauSpinnerWLeft = WLeft[0] 
        event.TauSpinnerIsRightLeft = IsRightLeft[0] 
	
	#print "MANU : valid " , event.TauSpinnerWTisValid, " WT = ", event.TauSpinnerWT, " IsRightLeft = " ,event.TauSpinnerIsRightLeft

        self.counters.counter('TauSpinnerWeights').inc('events with TauSpinner weights')

        return True

	    
