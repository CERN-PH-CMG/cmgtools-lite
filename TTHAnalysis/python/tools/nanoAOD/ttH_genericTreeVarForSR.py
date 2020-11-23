from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 


from math import sqrt, cos
from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR
from PhysicsTools.Heppy.physicsobjects.Jet import _btagWPs

class ttH_genericTreeVarForSR(Module):
    def __init__(self, lepMultiplicity, selection, execute=[],extraVars=[]):
        self.lepMultiplicity=lepMultiplicity
        self.selection=selection
        self.execute=execute
        self.extraVars=extraVars

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        for var in 'pt,eta,phi'.split(','):
            for l in range(self.lepMultiplicity):
                self.out.branch('Lep%d_%s'%(l+1,var),'F')
        
        self.out.branch('nSelJets'  ,'I')
        for var in 'pt,eta,phi,mass,isBtag,isFromHadTop'.split(','):
            self.out.branch('SelJet_%s'%var, 'F', 20, 'nSelJets')

        self.out.branch('event', 'I')


        self.out.branch('met'       ,'F')
        self.out.branch('met_phi'   ,'F')
        self.out.branch('Higgs_y'   ,'F')
        self.out.branch('Higgs_pt'  ,'F')

        self.out.branch('weight_SM'       ,'F')
        self.out.branch('weight_CP_odd'       ,'F')

        self.out.branch('HTT_score','F')

        for br in self.extraVars:
            self.out.branch(br[0],'F')


    def analyze(self, event):
        self.out.fillBranch('event',event.event)
        all_leps = [l for l in Collection(event,"LepGood")]
        nFO = getattr(event,"nLepFO_Recl")
        chosen = getattr(event,"iLepFO_Recl")
        leps = [all_leps[chosen[i]] for i in xrange(nFO)]
        jets = [j for j in Collection(event,"JetSel_Recl")]
        gen  = [g for g in Collection(event,"GenPart")]

        if len(leps) < self.lepMultiplicity: return False
        for ex in self.execute:
            exec(ex)
        

        for sel in self.selection: 
            if eval(sel): return False

        for j in jets: 
            setattr(j, 'isFromHadTop', jets.index(j) in [int(event.BDThttTT_eventReco_iJetSel1), int(event.BDThttTT_eventReco_iJetSel2), int(event.BDThttTT_eventReco_iJetSel3)])
            setattr(j, 'isBtag', j.btagDeepFlavB > (0.3093, 0.3033, 0.2770)[event.year-2016])            
        
        for lep in range(self.lepMultiplicity):
            for var in 'pt,eta,phi'.split(','):
                self.out.fillBranch('Lep%d_%s'%(lep+1,var), getattr(leps[lep],var))

        for var in 'pt,eta,phi,mass,isBtag,isFromHadTop'.split(','):
            jetVar=[]
            for j in jets:
                if j.pt < 25: continue
                jetVar.append(getattr(j,var))

            self.out.fillBranch('SelJet_%s'%var, jetVar)


        self.out.fillBranch('met',event.MET_pt)
        self.out.fillBranch('met_phi',event.MET_phi)
        self.out.fillBranch('HTT_score',  event.BDThttTT_eventReco_mvaValue)
        self.out.fillBranch('Higgs_pt',event.HTXS_Higgs_pt)
        self.out.fillBranch('Higgs_y',event.HTXS_Higgs_y)
        self.out.fillBranch('nSelJets', len(jetVar))   # outside the loop but on purpose

        self.out.fillBranch('weight_SM'    , event.LHEReweightingWeight[11])
        self.out.fillBranch('weight_CP_odd', event.LHEReweightingWeight[59])

        for br in self.extraVars:
            self.out.fillBranch(br[0],eval(br[1]))

        return True
