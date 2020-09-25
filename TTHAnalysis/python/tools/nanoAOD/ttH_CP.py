from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 


from math import sqrt, cos
from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR
from PhysicsTools.Heppy.physicsobjects.Jet import _btagWPs

class TTH_CP(Module):
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

        self.out.branch('nSelJets'  ,'I')
        self.out.branch('SelJet_pt', 'F', 20, 'nSelJets')
        self.out.branch('SelJet_eta', 'F', 20, 'nSelJets')
        self.out.branch('SelJet_phi', 'F', 20, 'nSelJets')
        self.out.branch('SelJet_mass', 'F', 20, 'nSelJets')
        self.out.branch('SelJet_isBtag', 'I', 20, 'nSelJets')
        self.out.branch('SelJet_isFromHadTop', 'I', 20, 'nSelJets')


        self.out.branch('met'       ,'F')
        self.out.branch('met_phi'   ,'F')
        self.out.branch('Higgs_y'   ,'F')
        self.out.branch('Higgs_pt'  ,'F')

        self.out.branch('weight_SM'       ,'F')
        self.out.branch('weight_CP_odd'       ,'F')

        
    def analyze(self, event):
        all_leps = [l for l in Collection(event,"LepGood")]
        nFO = getattr(event,"nLepFO_Recl")
        chosen = getattr(event,"iLepFO_Recl")
        leps = [all_leps[chosen[i]] for i in xrange(nFO)]
        jets = [j for j in Collection(event,"JetSel_Recl")]
        gen  = [g for g in Collection(event,"GenPart")]

        if len(leps) < 2                                          : return False
        if leps[0].pt < 25 or leps[1].pt < 15                     : return False # pt2515
        if event.nLepTight_Recl > 2                              : return False # exclusive
        if leps[0].pdgId*leps[1].pdgId < 0                        : return False # same-sign
        if abs(event.mZ1_Recl-91.2)<10                                 : return False # Z_veto
        
        if leps[0].genPartFlav != 1 and leps[0].genPartFlav != 15 : return False
        if leps[1].genPartFlav != 1 and leps[1].genPartFlav != 15 : return False
        if event.nTauSel_Recl_Tight > 0                           : return False
        if not ((event.nJet25_Recl>=3 and (event.nBJetLoose25_Recl >= 2 or event.nBJetMedium25_Recl >= 1)) or (event.nBJetMedium25_Recl >= 1 and (event.nJet25_Recl+event.nFwdJet_Recl-event.nBJetLoose25_Recl) > 0)) : return False

        self.out.fillBranch('Lep1_pt'   ,leps[0].pt)
        self.out.fillBranch('Lep1_eta'  ,leps[0].eta)
        self.out.fillBranch('Lep1_phi'  ,leps[0].phi)
        self.out.fillBranch('Lep2_pt'   ,leps[1].pt)
        self.out.fillBranch('Lep2_eta'  ,leps[1].eta)
        self.out.fillBranch('Lep2_phi'  ,leps[1].phi)
        
        pts=[]; etas=[]; phis=[]; masses=[]; btags=[]; fromTop=[]
        for j in jets: 
            if jets.index(j) in [int(event.BDThttTT_eventReco_iJetSel1), int(event.BDThttTT_eventReco_iJetSel2), int(event.BDThttTT_eventReco_iJetSel3)]:
                setattr(j, 'fromHadTop', True)
            else:
                setattr(j, 'fromHadTop', False)
            if j.pt < 25: continue
            
            pts.append(j.pt)
            etas.append(j.eta)
            phis.append(j.phi)
            masses.append(j.mass)
            btags.append( j.btagDeepFlavB < _btagWPs["DeepFlav_%d_M"%event.year] ) 
            fromTop.append(j.fromHadTop)
            

        self.out.fillBranch('met',event.MET_pt)
        self.out.fillBranch('met_phi',event.MET_phi)

        self.out.fillBranch('Higgs_pt',event.HTXS_Higgs_pt)
        self.out.fillBranch('Higgs_y',event.HTXS_Higgs_y)
        self.out.fillBranch('nSelJets', len(pts))  
        self.out.fillBranch('SelJet_pt', pts)
        self.out.fillBranch('SelJet_eta', etas)
        self.out.fillBranch('SelJet_phi', phis)
        self.out.fillBranch('SelJet_mass', masses)
        self.out.fillBranch('SelJet_isBtag',btags)
        self.out.fillBranch('SelJet_isFromHadTop',fromTop)
 
        self.out.fillBranch('weight_SM'    , event.LHEReweightingWeight[11])
        self.out.fillBranch('weight_CP_odd', event.LHEReweightingWeight[59])

        
        return True

    
ttH_CP = lambda : TTH_CP()
