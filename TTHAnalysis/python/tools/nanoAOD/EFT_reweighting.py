from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from CMGTools.TTHAnalysis.tools.nanoAOD.friendVariableProducerTools import writeOutput
import os, sys
import math
import numpy as np 
import imp
import tempfile, shutil
import numpy

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


def numToString(num):
    return ("%4.2f"%num).replace('.','p').replace('-','m')
        
class EFTreweighting( Module ):
    def __init__(self, process, subprocess=['']):

        self.mods=[]
        self.tmpdirs=[]
        self.process=process
        self.subprocesses=subprocess
        if 'psi.ch' in os.environ['HOSTNAME']:
            self.tmpdir='/scratch/'
        else:
            self.tmpdir='/tmp/'

        path=os.environ['CMSSW_BASE'] + '/src/CMGTools/TTHAnalysis/data/eft/reweighting//'
        

        # reweighting points (first should be reference) 
        self.param_cards=[path + '/cardsForEFT/param_card_sm.dat']
        for car in os.listdir(path + '/cardsForEFT/'):
            if not car.endswith('.dat'): continue
            if 'template' in car: continue
            self.param_cards.append(path + '/cardsForEFT/' + car)
        self.pdgOrderSorted =[]
        self.pdgOrder = []
        self.all_prefix = []
        self.hel_dict = []

        for subprocess in self.subprocesses:
            self.mods.append([])
            for card in self.param_cards:
                dirpath = tempfile.mkdtemp(dir=self.tmpdir)
                self.tmpdirs.append(dirpath)
                shutil.copyfile( path + self.process + subprocess + '/allmatrix2py.so', self.tmpdirs[-1] + '/allmatrix2py.so')
                sys.path[-1] =self.tmpdirs[-1]
                self.mods[-1].append(imp.load_module('allmatrix2py',*imp.find_module('allmatrix2py')))
                del sys.modules['allmatrix2py']
                print 'initializing', card
                self.mods[-1][-1].initialise(card)
            print len(self.pdgOrderSorted)
            self.pdgOrderSorted.append( [SortPDGs(x.tolist()) for x in self.mods[-1][-1].get_pdg_order()] )
            self.pdgOrder.append( [x.tolist() for x in self.mods[-1][-1].get_pdg_order()])
            self.all_prefix.append( [''.join(j).strip().lower() for j in self.mods[-1][-1].get_prefix()])
            self.hel_dict.append( {} ); prefix_set = set(self.all_prefix[-1])
            for prefix in prefix_set:
                if hasattr(self.mods[-1][-1], '%sprocess_nhel' % prefix):
                    nhel = getattr(self.mods[-1][-1], '%sprocess_nhel' % prefix).nhel
                    self.hel_dict[-1][prefix] = {}
                    for i, onehel in enumerate(zip(*nhel)):
                        self.hel_dict[-1][prefix][tuple(onehel)] = i + 1

        

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.wrappedOutputTree = wrappedOutputTree
        for card in self.param_cards:
            self.wrappedOutputTree.branch('weight_%s'%(card.split('/')[-1].replace('param_card_','')),'F')

    def endJob(self):
        for dr in self.tmpdirs:
            shutil.rmtree(dr)

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
        
        sub_idx=-1
        for subproc in range(len(self.subprocesses)):
            if evt_sorted_pdgs not in self.pdgOrderSorted[subproc]:
                continue
            idx = self.pdgOrderSorted[subproc].index(evt_sorted_pdgs)
            sub_idx=subproc
            break

        if sub_idx < 0:
            print '>> Event with PDGs %s does not match any known process' % evt_sorted_pdgs
            print 'Available processes are'
            print self.pdgOrderSorted
            

        target_pdgs=self.pdgOrder[sub_idx][idx]
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

        hel_dict = self.hel_dict[sub_idx][self.all_prefix[sub_idx][idx]]
        t_final_hels = tuple(final_hels)
        if t_final_hels in hel_dict:
            nhel = hel_dict[t_final_hels]
        else:
            print "Available helicities are"
            print hel_dict
            print "tried", t_final_hels
            raise RuntimeError("Helicity configuration not found")
        
        com_final_parts = []


        pboost = [final_parts[0][i] + final_parts[1][i] for i in xrange(4)]

        for part in final_parts:
            com_final_parts.append(zboost(part, pboost))
            

        final_parts_i = invert_momenta(com_final_parts)
        scale2=0
        weights=[]
        
        for mod in self.mods[sub_idx]:
            weights.append( mod.smatrixhel( final_pdgs, final_parts_i, event.LHE_AlphaS, scale2, nhel) ) 
        for i, card in enumerate(self.param_cards):
            if not weights[0]: 
                print 'Warning, zero weight!!'
                weights[0]=1
                weights[i]=1
            self.wrappedOutputTree.fillBranch('weight_%s'%(card.split('/')[-1].replace('param_card_','')), weights[i]/weights[0])


        return True

TTH_reweighting = lambda : EFTreweighting('ttH')
TTZ_reweighting = lambda : EFTreweighting('ttZ',['_0j_0','_1j_0', '_0j_1','_1j_1', '_0j_2','_1j_2'])
TTW_reweighting = lambda : EFTreweighting('ttW',['_0j','_1j','_2j'])

