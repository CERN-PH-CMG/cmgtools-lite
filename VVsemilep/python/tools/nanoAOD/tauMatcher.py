from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection as Collection 
from CMGTools.TTHAnalysis.tools.nanoAOD.friendVariableProducerTools import writeOutput
from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR

import os
import ROOT as r 

def matchObjectCollection( objects, matchCollection, deltaRMax = 0.3, filter = lambda x,y: True):
    pairs={}

    if len(objects)==0:
        return pairs
    if len(matchCollection)==0:
        return dict( list(zip(objects, [None]*len(objects))) )

    objectCoords = [ (o.eta,o.phi,o) for o in objects ]
    matchdCoords = [ (o.eta,o.phi,o) for o in matchCollection ]

    allPairs = sorted([(deltaR (oeta, ophi, meta, mphi), (object, match)) for (oeta,ophi,object) in objectCoords for (meta,mphi,match) in matchdCoords if abs(oeta-meta)<=deltaRMax and filter(object,match) ])

    for object in objects:
        object.matched = False
    for match in matchCollection:
        match.matched = False

    for dR, (object, match) in allPairs:
        if dR > deltaRMax:
            break
        if dR < deltaRMax and object.matched == False and match.matched == False:
            object.matched = True
            match.matched = True
            pairs[object] = match

    for object in objects:
        if object.matched == False:
            pairs[object] = None


    return pairs


class tauSFs(Module):
    def __init__(self, recllabel='Recl'):
        self.inputlabel = '_'+recllabel
        r.gROOT.LoadMacro(os.environ['CMSSW_BASE'] + '/src/CMGTools/TTHAnalysis/python/plotter/ttH-multilepton/functionsTTH.cc+')
    
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.wrappedOutputTree = wrappedOutputTree
        self.wrappedOutputTree.branch('TauSel_2lss1tau_SF','F')
        self.wrappedOutputTree.branch('TauSel_2lss1tau_SF_effUp','F')
        self.wrappedOutputTree.branch('TauSel_2lss1tau_SF_effDown','F')
        self.wrappedOutputTree.branch('TauSel_2lss1tau_SF_frNormUp','F')
        self.wrappedOutputTree.branch('TauSel_2lss1tau_SF_frNormDown','F')
        self.wrappedOutputTree.branch('TauSel_2lss1tau_SF_frShapeUp','F')
        self.wrappedOutputTree.branch('TauSel_2lss1tau_SF_frShapeDown','F')
        

    def analyze(self,event):
        taus = [ t for t in Collection(event, 'TauSel'+self.inputlabel)]
        if not hasattr(event, 'nGenVisTau') or event.Tau_tight2lss1tau_idx < 0:
            self.wrappedOutputTree.fillBranch('TauSel_2lss1tau_SF',0.)
            self.wrappedOutputTree.fillBranch('TauSel_2lss1tau_SF_effUp',0.)
            self.wrappedOutputTree.fillBranch('TauSel_2lss1tau_SF_effDown',0.)
            self.wrappedOutputTree.fillBranch('TauSel_2lss1tau_SF_frNormUp',0.)
            self.wrappedOutputTree.fillBranch('TauSel_2lss1tau_SF_frNormDown',0.)
            self.wrappedOutputTree.fillBranch('TauSel_2lss1tau_SF_frShapeUp',0.)
            self.wrappedOutputTree.fillBranch('TauSel_2lss1tau_SF_frShapeDown',0.)
            
            return True

        genvistau = [ t for t in Collection(event, 'GenVisTau')]
        results=[]
        match=matchObjectCollection( taus, genvistau, filter = lambda x,y : deltaR(x,y)<0.3 and (abs(x.pt-y.pt)/y.pt ) < 0.5 )
        thetau = taus[int(event.Tau_tight2lss1tau_idx)]

        self.wrappedOutputTree.fillBranch('TauSel_2lss1tau_SF', r.tauSF( thetau.pt, thetau.eta, event.year, bool(match[thetau])))
        self.wrappedOutputTree.fillBranch('TauSel_2lss1tau_SF_effUp', r.tauSF( thetau.pt, thetau.eta, event.year, bool(match[thetau]), 1))
        self.wrappedOutputTree.fillBranch('TauSel_2lss1tau_SF_effDown', r.tauSF( thetau.pt, thetau.eta, event.year, bool(match[thetau]), -1))
        self.wrappedOutputTree.fillBranch('TauSel_2lss1tau_SF_frNormUp', r.tauSF( thetau.pt, thetau.eta, event.year, bool(match[thetau]), 0,1))
        self.wrappedOutputTree.fillBranch('TauSel_2lss1tau_SF_frNormDown', r.tauSF( thetau.pt, thetau.eta, event.year, bool(match[thetau]), 0,-1))
        self.wrappedOutputTree.fillBranch('TauSel_2lss1tau_SF_frShapeUp', r.tauSF( thetau.pt, thetau.eta, event.year, bool(match[thetau]), 0,0,1))
        self.wrappedOutputTree.fillBranch('TauSel_2lss1tau_SF_frShapeDown', r.tauSF( thetau.pt, thetau.eta, event.year, bool(match[thetau]), 0,0,-1))
    
        
        return True
tauScaleFactors = lambda : tauSFs()
