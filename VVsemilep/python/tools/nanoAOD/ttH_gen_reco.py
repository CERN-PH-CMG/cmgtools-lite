from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 


from math import sqrt, cos
from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR
from PhysicsTools.Heppy.physicsobjects.Jet import _btagWPs

class TTH_gen_reco(Module):
    def __init__(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch('Lep1_pt'   ,'F')
        self.out.branch('Lep1_eta'  ,'F')
        self.out.branch('Lep1_phi'  ,'F')
        self.out.branch('Lep2_pt'   ,'F')
        self.out.branch('Lep2_eta'  ,'F')
        self.out.branch('Lep2_phi'  ,'F')
        self.out.branch('Jet1_pt'   ,'F')
        self.out.branch('Jet1_eta'  ,'F')
        self.out.branch('Jet1_phi'  ,'F')
        self.out.branch('Jet1_mass' ,'F')
        self.out.branch('Jet2_pt'   ,'F')
        self.out.branch('Jet2_eta'  ,'F')
        self.out.branch('Jet2_phi'  ,'F')
        self.out.branch('Jet2_mass' ,'F')
        self.out.branch('HadTop_pt' ,'F')
        self.out.branch('HadTop_eta','F')
        self.out.branch('HadTop_phi','F')
        self.out.branch('met'       ,'F')
        self.out.branch('met_phi'   ,'F')
        self.out.branch('Higgs_y'   ,'F')
        self.out.branch('Higgs_pt'  ,'F')
        self.out.branch('GenHiggsDecayMode'   ,'I')

        
    def analyze(self, event):
        all_leps = [l for l in Collection(event,"LepGood")]
        nFO = getattr(event,"nLepFO_Recl")
        chosen = getattr(event,"iLepFO_Recl")
        leps = [all_leps[chosen[i]] for i in xrange(nFO)]
        jets = [j for j in Collection(event,"JetSel_Recl")]
        gen  = [g for g in Collection(event,"GenPart")]

        if len(leps) < 2:                                          return False
        if leps[0].pdgId*leps[1].pdgId > 0:                        return False
        if leps[0].genPartFlav != 1 and leps[0].genPartFlav != 15: return False
        if leps[1].genPartFlav != 1 and leps[1].genPartFlav != 15: return False
        if len(jets) < 4                                         : return False


        self.out.fillBranch('GenHiggsDecayMode'   ,event.GenHiggsDecayMode)
        self.out.fillBranch('Lep1_pt'   ,leps[0].pt)
        self.out.fillBranch('Lep1_eta'  ,leps[0].eta)
        self.out.fillBranch('Lep1_phi'  ,leps[0].phi)
        self.out.fillBranch('Lep2_pt'   ,leps[1].pt)
        self.out.fillBranch('Lep2_eta'  ,leps[1].eta)
        self.out.fillBranch('Lep2_phi'  ,leps[1].phi)

        toremove = []
        if event.BDThttTT_eventReco_iJetSel1 > -1: 
            top = jets[int(event.BDThttTT_eventReco_iJetSel1)].p4()+jets[int(event.BDThttTT_eventReco_iJetSel2)].p4()+jets[int(event.BDThttTT_eventReco_iJetSel3)].p4()
            self.out.fillBranch('HadTop_pt'   , top.Pt())
            self.out.fillBranch('HadTop_eta'  , top.Eta())
            self.out.fillBranch('HadTop_phi'  , top.Phi())

            toremove.append(jets[int(event.BDThttTT_eventReco_iJetSel1)])
            toremove.append(jets[int(event.BDThttTT_eventReco_iJetSel2)])
            toremove.append(jets[int(event.BDThttTT_eventReco_iJetSel3)])
            

        else: 
            self.out.fillBranch('HadTop_pt'   , 0)
            self.out.fillBranch('HadTop_eta'  , 0)
            self.out.fillBranch('HadTop_phi'  , 0)

        for jet in jets:
            if jet.btagDeepFlavB < _btagWPs["DeepFlav_%d_M"%event.year]: toremove.append(jet)

        for jet in jets:
            jets.remove(jet)

        self.out.fillBranch('met',event.MET_pt)
        self.out.fillBranch('met_phi',event.MET_phi)

        self.out.fillBranch('Higgs_pt',event.HTXS_Higgs_pt)
        self.out.fillBranch('Higgs_y',event.HTXS_Higgs_y)
        
        self.out.fillBranch('Jet1_pt'   ,jets[0].pt   if len(jets) > 0  else 0)
        self.out.fillBranch('Jet1_eta'  ,jets[0].eta  if len(jets) > 0  else 0)
        self.out.fillBranch('Jet1_phi'  ,jets[0].phi  if len(jets) > 0  else 0)
        self.out.fillBranch('Jet1_mass' ,jets[0].mass if len(jets) > 0  else 0)
        self.out.fillBranch('Jet2_pt'   ,jets[1].pt   if len(jets) > 1  else 0)
        self.out.fillBranch('Jet2_eta'  ,jets[1].eta  if len(jets) > 1  else 0)
        self.out.fillBranch('Jet2_phi'  ,jets[1].phi  if len(jets) > 1  else 0)
        self.out.fillBranch('Jet2_mass' ,jets[1].mass if len(jets) > 1  else 0)

        
        return True

    
ttH_gen_reco = lambda : TTH_gen_reco()
