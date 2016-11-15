from CMGTools.TTHAnalysis.treeReAnalyzer import *
from ROOT import TLorentzVector, TVector2, std
import ROOT
import time
import itertools
import PhysicsTools.Heppy.loadlibs
import array
import operator

class EventVars1L_triggers:
    def __init__(self):
        self.branches = [
            'HLT_HT350', 'HLT_HT600', 'HLT_HT800', 'HLT_HT900',
            'HLT_PFJet450',
            'HLT_MET170',
            'HLT_HT350MET120','HLT_HT350MET100','HLT_HTMET',
            'HLT_IsoMu27','HLT_IsoMu20','HLT_IsoMu24','HLT_Mu50', # single mu
            'HLT_MuHT400MET70','HLT_MuHT350MET70','HLT_MuHT350MET50', 'HLT_MuHTMET','HLT_MuHT350',# for analysis
            #'HLT_MuHT600', 'HLT_MuMET120', 'HLT_MuHT400B', #aux
            'HLT_IsoEle32','HLT_IsoEle22','HLT_IsoEle23','HLT_IsoEle27T','HLT_Ele105','HLT_Ele115', # single ele
            'HLT_EleHT400MET70','HLT_EleHT350MET70','HLT_EleHT350MET50','HLT_EleHTMET','HLT_EleHT350', # for analysis
            'HLT_EleHT400', 'HLT_MuHT400', 'HLT_Ele50HT400', 'HLT_Mu50HT400', #latest additions 
            #'HLT_EleHT600','HLT_EleHT200', 'HLT_EleHT400B', # aux
            ## custom names
            #'HLT_EleOR', 'HLT_MuOR','HLT_LepOR'
            #'HLT_IsoMu27','HLT_IsoEle32',
            #'HLT_Mu50','HLT_Ele105'
            ## Trigger efficiencies
            'TrigEff'
            ]

    def listBranches(self):
        return self.branches[:]

    def __call__(self,event,base):

        # output dict:
        ret = {}

        ## loop over all HLT names and set them in tree
        for var in self.branches:
            #print var, getattr(event,var)
            if 'HLT_' in var and hasattr(event,var):
                ret[var] = getattr(event,var)
            else:
                ret[var] = 0

        # Trigger efficiencies:
        if hasattr(self,'sample'):
#            print self.sample
            if 'Ele' in self.sample or 'Mu' in self.sample:
                ret['TrigEff'] = 1.0
            elif base['nEl']>=1: ret['TrigEff'] = 0.963 # ele efficieny (for 2016 4/fb)
            elif base['nMu']>=1: ret['TrigEff'] = 0.926 # mu efficieny (for 2016 4/fb)
            else: ret['TrigEff'] = 1.0
#old logic
#            if 'Ele' in self.sample: ret['TrigEff'] = 0.963 # ele efficieny (for 2016 4/fb)
#            elif 'Mu' in self.sample: ret['TrigEff'] = 0.926 # mu efficieny (for 2016 4/fb)
#            else: ret['TrigEff'] = 1.0
        else:
            ret['TrigEff'] = 1.00 # to make clear that this is not the accurate value

        ## print out all HLT names
        #for line in vars(event)['_tree'].GetListOfBranches():
        #    if 'HLT_' in line.GetName():
        #        print line.GetName()

        # custom names for triggers
        '''
        if hasattr(event,'HLT_Ele105'):
            ret['HLT_EleOR'] = event.HLT_Ele105 or event.HLT_EleHTMET
        if hasattr(event,'HLT_Mu50'):
            ret['HLT_MuOR'] = event.HLT_Mu50 or event.HLT_MuHTMET
        if hasattr(event,'HLT_Ele105'):
            ret['HLT_LepOR'] = event.HLT_Mu50 or event.HLT_MuHTMET or event.HLT_Ele105 or event.HLT_EleHTMET
        '''

        # return branches
        return ret

if __name__ == '__main__':
    from sys import argv
    file = ROOT.TFile(argv[1])
    tree = file.Get("tree")
    class Tester(Module):
        def __init__(self, name):
            Module.__init__(self,name,None)
            self.sf = EventVars1L()
        def analyze(self,ev):
            print "\nrun %6d lumi %4d event %d: leps %d" % (ev.run, ev.lumi, ev.evt, ev.nLepGood)
            print self.sf(ev)
    el = EventLoop([ Tester("tester") ])
    el.loop([tree], maxEvents = 50)
