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
        
class TH_weights( Module ):
    def __init__(self, process):

        self.mods=[]
        self.tmpdirs=[]

        path=os.environ['CMSSW_BASE'] + '/src/CMGTools/TTHAnalysis/data/mc_rw/%s/'%process
        

        # reweighting points (first should be reference) 
        self.param_cards=[path + '/param_card_itc.dat', path+'/param_card_sm.dat']

        # generate scan
        cosa = np.array([-0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, -0.0001, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
        q = np.linspace(-3,3,10).transpose()

        cosacosa,qq = np.meshgrid( cosa, q )


        # for plotting
        #kt = cosa
        #sina= np.sin(np.arccos(cosa))
        # kt_tilde = 2./3*sina
        #kt_tildekt_tilde,qq = np.meshgrid( kt_tilde, q)
        #cosacosa,qq=np.meshgrid(cosa,q)

        # ktkt=np.multiply(ktkt,qq)
        # kt_tildekt_tilde = np.multiply(kt_tildekt_tilde,qq)

        # ktkt=ktkt.flatten()
        # kt_tildekt_tilde=kt_tildekt_tilde.flatten()
        qq = qq.flatten()
        cosacosa = cosacosa.flatten()



        template=open("%s/param_card_sm_template.dat"%path).read()
        for cosa, q in zip(cosacosa, qq):
            outn="param_card_cosa_%s_q_%s.dat"%(numToString(cosa), numToString(q))
            out=template.format(khtt=q,katt=2.*q/3,cosa=cosa,kSM=1/cosa)
            outf=open('/scratch/%s'%outn,'w')
            outf.write(out)
            outf.close()
            self.param_cards.append('/scratch/%s'%outn)

        for card in self.param_cards:
            dirpath = tempfile.mkdtemp(dir='/scratch/')
            self.tmpdirs.append(dirpath)
            shutil.copyfile( path + '/allmatrix2py.so', self.tmpdirs[-1] + '/allmatrix2py.so')
            sys.path[-1] =self.tmpdirs[-1]
            self.mods.append(imp.load_module('allmatrix2py',*imp.find_module('allmatrix2py')))
            del sys.modules['allmatrix2py']
            print 'initializing', card
            self.mods[-1].initialise(card)
        print self.mods
        
        self.pdgOrderSorted = [SortPDGs(x.tolist()) for x in self.mods[-1].get_pdg_order()]
        self.pdgOrder = [x.tolist() for x in self.mods[-1].get_pdg_order()]
        self.all_prefix = [''.join(j).strip().lower() for j in self.mods[-1].get_prefix()]
        self.hel_dict = {}; prefix_set = set(self.all_prefix)
        for prefix in prefix_set:
            if hasattr(self.mods[-1], '%sprocess_nhel' % prefix):
                nhel = getattr(self.mods[-1], '%sprocess_nhel' % prefix).nhel
                self.hel_dict[prefix] = {}
                for i, onehel in enumerate(zip(*nhel)):
                    self.hel_dict[prefix][tuple(onehel)] = i + 1

        

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

        hel_dict = self.hel_dict[self.all_prefix[idx]]
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
        for mod in self.mods:
            weights.append( mod.smatrixhel( final_pdgs, final_parts_i, event.LHE_AlphaS, scale2, nhel) ) 

        for i, card in enumerate(self.param_cards):
            self.wrappedOutputTree.fillBranch('weight_%s'%(card.split('/')[-1].replace('param_card_','')), weights[i]/weights[0])


        return True

tHq_reweigther = lambda : TH_weights('thq')
tHW_reweigther = lambda : TH_weights('thw')
ttH_reweigther = lambda : TH_weights('tth')
