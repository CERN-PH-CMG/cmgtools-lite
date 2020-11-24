from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from CMGTools.TTHAnalysis.tools.nanoAOD.friendVariableProducerTools import writeOutput
from collections import defaultdict
import math

import CMGTools.TTHAnalysis.tools.nanoAOD.tHq.allmatrix2py as allmatrix2py
#import CMGTools.TTHAnalysis.tools.nanoAOD.ttH.allmatrix2py as allmatrix2py

def invert_momenta(p):
    #fortran/C-python do not order table in the same order
    new_p = []
    for i in range(len(p[0])):  
        new_p.append([0]*len(p))
    for i, onep in enumerate(p):
        for j, x in enumerate(onep):
            new_p[j][i] = x
    return new_p

def SortPDGs(pdgs):
    return sorted(pdgs[:2]) + sorted(pdgs[2:])


def zboost(part, pboost=[]):
    """Both momenta should be in the same frame.
The boost perform correspond to the boost required to set pboost at
    rest (only z boost applied).
    """
    E = pboost[0]
    pz = pboost[3]
    #beta = pz/E
    gamma = E / math.sqrt(E**2-pz**2)
    gammabeta = pz  / math.sqrt(E**2-pz**2)
        
    out =  [gamma * part[0] - gammabeta * part[3],
            part[1],
            part[2],
            gamma * part[3] - gammabeta * part[0]]
    
    if abs(out[3]) < 1e-6 * out[0]:
        out[3] = 0
    return out

        
class THQ_weights( Module ):
    def __init__(self):
        allmatrix2py.initialise('param_card.dat')
        
        self.pdgOrderSorted = [SortPDGs(x.tolist()) for x in allmatrix2py.get_pdg_order()]
        self.pdgOrder = [x.tolist() for x in allmatrix2py.get_pdg_order()]
                
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.wrappedOutputTree = wrappedOutputTree
        self.wrappedOutputTree.branch('weight','F')

    def analyze(self, event):

        lheParts = [l for l in Collection(event, 'LHEPart')]
        pdgs = [x.pdgId for x in lheParts]
        hel  = [x.spin  for x in lheParts]


        p = [ ]
        for part in lheParts:
            if part.status < 0: 
                energy = math.sqrt(part.incomingpz*part.incomingpz+part.mass*part.mass)
                p.append([energy,0.,0.,part.incomingpz])
            else:
                p.append([part.p4().E(), part.p4().Px(), part.p4().Py(), part.p4().Pz()])
        evt_sorted_pdgs = SortPDGs(pdgs)

        try:
            idx = self.pdgOrderSorted.index(evt_sorted_pdgs)
        except ValueError:
            print '>> Event with PDGs %s does not match any known process' % pdgs
            return res

        target_pdgs=self.pdgOrder[idx]
        pdgs_withIndices = [(y,x) for x,y in enumerate(pdgs)]
        mapping=[]

        for p1 in target_pdgs:
            toremove=None
            for p2 in pdgs_withIndices:
                if p2[0]==p1:
                    mapping.append( p2[1])
                    toremove=p2
                    break
            if toremove:
                pdgs_withIndices.remove(toremove)
            else:
                raise RuntimeError("It shouldn't be here")

        final_pdgs = []
        final_parts = []
        final_hels = []
        for in_Indx in mapping:
            final_parts.append(p[in_Indx])
            final_pdgs.append(pdgs[in_Indx])
            final_hels.append(hel[in_Indx])

        if target_pdgs != final_pdgs:
            raise RuntimeError("Wrong pdgid")
            
        com_final_parts = []



        pboost = [final_parts[0][i] + final_parts[1][i] for i in xrange(4)]

        for part in final_parts:
            com_final_parts.append(zboost(part, pboost))
            

        final_parts_i = invert_momenta(com_final_parts)
        scale2=0
        weight=allmatrix2py.smatrixhel( final_pdgs, final_parts_i, event.LHE_AlphaS, scale2, final_hels)
        self.wrappedOutputTree.fillBranch('weight', weight)
        print 'weight ->', weight
        if not weight:
            print final_pdgs, final_hels

        return True

ttH_reweigther = lambda : THQ_weights()
