from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from CMGTools.TTHAnalysis.tools.nanoAOD.friendVariableProducerTools import declareOutput, writeOutput

from math import sqrt, cos
from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR
from PhysicsTools.Heppy.physicsobjects.Jet import _btagWPs
from CMGTools.TTHAnalysis.tools.mvaTool import *

class emptyclass: 
    pass

class HjDummyCalc(Module):
    def __init__(self, variations=[], doSystJEC=True): 
        self.inputlabel = "_Recl"
        self._vars = [
            MVAVar("Jet25_bDiscriminator", func = lambda ev : ev.v2),
            MVAVar("Jet25_pt", func = lambda ev : ev.v5),
            MVAVar("Jet25_lepdrmin", func = lambda ev : ev.v1),
            MVAVar("Jet25_lepdrmax", func = lambda ev : ev.v4),
            MVAVar("Jet25_qg", func = lambda ev : ev.v3),
        ]
        P = os.environ["CMSSW_BASE"] + '/src/CMGTools/TTHAnalysis/data/kinMVA/tth/Hjtagger_legacy_xgboost_v1.weights.xml' 
        self._MVA = MVATool("BDTG", P, self._vars) 
        self.systsJEC = {0:"",\
                         1:"_jesTotalCorrUp"  , -1:"_jesTotalCorrDown",\
                        2:"_jesTotalUnCorrUp", -2: "_jesTotalUnCorrDown",\
                         3:"_jerUp", -3: "_jerDown",\
                     } if doSystJEC else {0:""}

        if len(variations):  
            self.systsJEC = {0:""}
            for i,var in enumerate(variations):
                self.systsJEC[i+1]   ="_%sUp"%var
                self.systsJEC[-(i+1)]="_%sDown"%var
        self.branches = []
        for var in self.systsJEC: 
            self.branches.append( 'highestHjTagger' + self.systsJEC[var]) 
        

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        declareOutput(self, wrappedOutputTree, self.branches)
    def analyze(self, event):
        all_leps = [l for l in Collection(event,"LepGood")]
        nFO = getattr(event,"nLepFO"+self.inputlabel)
        chosen = getattr(event,"iLepFO"+self.inputlabel)
        leps = [all_leps[chosen[i]] for i in xrange(nFO)]
        if len(leps) < 2: return True
        ret = {} 
        for var in self.systsJEC:
            ret['highestHjTagger%s'%self.systsJEC[var]] = -99
            _var = var
            if not hasattr(event,"nJet25"+self.systsJEC[var]+self.inputlabel): 
                _var = 0; 
            jets = [j for j in Collection(event,"JetSel"+self.inputlabel)]
            jetptcut = 25
            jets = filter(lambda x : getattr(x,'pt%s'%self.systsJEC[_var]) > jetptcut, jets)


            allVars = [] 
            for j in jets:
                pseudoevent = emptyclass()
                setattr(pseudoevent, 'v1', min( deltaR(j, leps[0]), deltaR(j, leps[1])))
                setattr(pseudoevent, 'v2', max( 0, j.btagDeepFlavB))
                setattr(pseudoevent, 'v3', max( 0, j.qgl ))
                setattr(pseudoevent, 'v4', max( deltaR(j, leps[0]), deltaR(j, leps[1]) ))
                setattr(pseudoevent, 'v5', getattr(j,'pt%s'%self.systsJEC[_var]))
                allVars.append( self._MVA( pseudoevent )  )
                del pseudoevent
            if len(allVars):
                ret['highestHjTagger%s'%self.systsJEC[var]] = max(allVars) 
                
        

        writeOutput(self, ret)
        return True
