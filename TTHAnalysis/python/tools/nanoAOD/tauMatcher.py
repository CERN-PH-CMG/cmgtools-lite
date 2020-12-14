from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection as Collection 
from CMGTools.TTHAnalysis.tools.nanoAOD.friendVariableProducerTools import writeOutput
from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR

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


class tauMatcher(Module):
    def __init__(self, recllabel='Recl'):
        self.inputlabel = '_'+recllabel
    
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.wrappedOutputTree = wrappedOutputTree
        self.wrappedOutputTree.branch('TauSel_Recl_isMatch','I',lenVar='nTauSel_Recl')

    def analyze(self,event):
        taus = [ t for t in Collection(event, 'TauSel'+self.inputlabel)]
        if not hasattr(event, 'nGenVisTau'):
            self.wrappedOutputTree.fillBranch( 'TauSel_Recl_isMatch', len(taus)*[0])
            return True


        genvistau = [ t for t in Collection(event, 'GenVisTau')]
        results=[]
        match=matchObjectCollection( taus, genvistau, filter = lambda x,y : deltaR(x,y)<0.3 and (abs(x.pt-y.pt)/y.pt ) < 0.5 )

        for tau in taus: 
            results.append( bool(match[tau] ) )
        self.wrappedOutputTree.fillBranch( 'TauSel_Recl_isMatch', results)
        
        return True
taumatcher = lambda : tauMatcher()
