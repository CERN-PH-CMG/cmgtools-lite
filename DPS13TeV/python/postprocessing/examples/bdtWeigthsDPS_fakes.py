## from CMGTools.TTHAnalysis.treeReAnalyzer import *
## from CMGTools.TTHAnalysis.tools.mvaTool import *
from mvaTool import *

from CMGTools.DPS13TeV.postprocessing.framework.datamodel import Collection 
from CMGTools.DPS13TeV.postprocessing.framework.eventloop import Module
from PhysicsTools.HeppyCore.utils.deltar import deltaPhi

ROOT.gROOT.ProcessLine('.L %s/src/CMGTools/DPS13TeV/python/plotter/functions.cc+' % os.environ['CMSSW_BASE']);

class BDT_DPS_fakes(Module):
    def __init__(self):
        self._MVAs = {}
        self._vars= [
            ## order 2018:
            MVAVar('v1 := LepGood_pt[0]'),
            MVAVar('v2 := LepGood_pt[1]'),
            MVAVar('v3 := met_pt'),
            MVAVar('v4 := mt2davis(LepGood_pt[0],LepGood_eta[0],LepGood_phi[0],LepGood_pt[1],LepGood_eta[1],LepGood_phi[1],met_pt,met_phi)'),
            MVAVar('v5 := mt_2(LepGood_pt[0],LepGood_phi[0],LepGood_pt[1],LepGood_phi[1])'),
            MVAVar('v6 := mt_2(LepGood_pt[0],LepGood_phi[0],met_pt,met_phi)'),
            MVAVar('v7 := abs(deltaPhi(LepGood_phi[0],LepGood_phi[1]))'),
            MVAVar('v8 := abs(deltaPhi(LepGood_phi[1],met_phi))'),
            MVAVar('v9 := abs(deltaPhi(phi_2(LepGood_pt[0],LepGood_eta[0],LepGood_phi[0],LepGood_mass[0],LepGood_pt[1],LepGood_eta[1],LepGood_phi[1],LepGood_mass[1]),LepGood_phi[1]))'),
            MVAVar('v10:= LepGood_eta[0]*LepGood_eta[1]'),
            MVAVar('v11:= abs(LepGood_eta[0]+LepGood_eta[1])'),
            ## order 2016:
            ## MVAVar('v1 := LepGood_eta[0]*LepGood_eta[1]'),
            ## MVAVar('v2 := mt2davis(LepGood_pt[0],LepGood_eta[0],LepGood_phi[0],LepGood_pt[1],LepGood_eta[1],LepGood_phi[1],met_pt,met_phi)'),
            ## MVAVar('v3 := LepGood_pt[0]'),
            ## MVAVar('v4 := LepGood_pt[1]'),
            ## MVAVar('v5 := met_pt'),
            ## MVAVar('v6 := abs(LepGood_eta[0]+LepGood_eta[1])'),
            ## MVAVar('v7 := mt_2(LepGood_pt[0],LepGood_phi[0],LepGood_pt[1],LepGood_phi[1])'),
            ## MVAVar('v8 := mt_2(LepGood_pt[0],LepGood_phi[0],met_pt,met_phi)'),
            ## MVAVar('v9 := abs(deltaPhi(LepGood_phi[1],met_phi))'),
            ## MVAVar('v10:= abs(deltaPhi(LepGood_phi[0],LepGood_phi[1]))'),
            ## MVAVar('v11:= abs(dphi_2(LepGood_pt[0],LepGood_eta[0],LepGood_phi[0],LepGood_pt[1],LepGood_eta[1],LepGood_phi[1],2))'),
        ]
        P='/afs/cern.ch/user/a/anmehta/public/'
        self._MVAs['BDT_DPS_fakes'] = MVATool('BDT', P+'TMVAClassification_BDT.weights.xml', self._vars, rarity=True) 

    ## new stuff
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        #self.initReaders(inputTree) # initReaders must be called in beginFile
        self.out = wrappedOutputTree
        self.out.branch('BDT_DPS_fakes', "F")
        pass
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        mvadict = dict([ (name, mva(event)) for name, mva in self._MVAs.iteritems()])
        self.out.fillBranch('BDT_DPS_fakes', mvadict['BDT_DPS_fakes'])
        return True

BDT_fakes = lambda : BDT_DPS_fakes()
        
##     def listBranches(self):
##         return self._MVAs.keys()
##     def __call__(self,event):
##         return dict([ (name, mva(event)) for name, mva in self._MVAs.iteritems()])
## 
## if __name__ == '__main__':
##     from sys import argv
##     file = ROOT.TFile(argv[1])
##     tree = file.Get('tree')
##     tree.vectorTree = True
##     #tree.AddFriend('sf/t', argv[2])
##     class Tester(Module):
##         def __init__(self, name):
##             Module.__init__(self,name,None)
##             self.sf = BDT_DPS_fakes()
##         def analyze(self,ev):
##             print '\nrun %6d lumi %4d event %d: leps %d' % (ev.run, ev.lumi, ev.evt, ev.nLepGood)
##             print self.sf(ev)
##     el = EventLoop([ Tester('tester') ])
##     el.loop([tree], maxEvents = 50)

