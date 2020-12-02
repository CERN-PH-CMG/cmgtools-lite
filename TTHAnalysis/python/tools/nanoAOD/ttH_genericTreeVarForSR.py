from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
import ROOT as r 

from math import sqrt, cos
from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR, deltaPhi
from PhysicsTools.Heppy.physicsobjects.Jet import _btagWPs

from copy import deepcopy

class ttH_genericTreeVarForSR(Module):
    def __init__(self, lepMultiplicity, selection, execute=[],extraVars=[], is2lss1tau=False):
        self.lepMultiplicity=lepMultiplicity
        self.selection=selection
        self.execute=execute
        self.extraVars=extraVars
        self.is2lss1tau=is2lss1tau

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        for var in 'pt,eta,phi'.split(','):
            for l in range(self.lepMultiplicity):
                self.out.branch('Lep%d_%s'%(l+1,var),'F')
        
        self.out.branch('nSelJets'  ,'I')
        for var in 'pt,eta,phi,mass,isBtag,isFromHadTop,btagDeepFlavB'.split(','):
            self.out.branch('SelJet_%s'%var, 'F', 20, 'nSelJets')

        self.out.branch('event', 'I')


        self.out.branch('met'       ,'F')
        self.out.branch('met_phi'   ,'F')
        self.out.branch('Higgs_y'   ,'F')
        self.out.branch('Higgs_pt'  ,'F')

        self.out.branch('weight_SM'       ,'F')
        self.out.branch('weight_CP_odd'       ,'F')
        self.out.branch('weight_CP_mixed', 'F')
        self.out.branch('weight_CP_mixed_neg', 'F')

        self.out.branch('HTT_score','F')

        self.out.branch('mT_lep2',"F")
        self.out.branch('mT_lep1',"F")
        self.out.branch("Hj_tagger_hadTop","F")
        self.out.branch("mindr_lep2_jet","F")
        self.out.branch("mindr_lep1_jet","F")
        self.out.branch("avg_dr_jet","F")

        self.out.branch("dPhiLL_BBframe_2lss", 'F' ) 
        self.out.branch("dEtaLL_BBframe_2lss", 'F' ) 
        self.out.branch("dPhiBB_LLframe_2lss", 'F' ) 
        self.out.branch("dEtaBB_LLframe_2lss", 'F' ) 
        self.out.branch("dEtaBB_2lss"        , 'F' ) 


        self.out.branch("dEtaL1L2_BBframe_3l", 'F' ) 
        self.out.branch("dEtaL1L3_BBframe_3l", 'F' ) 
        self.out.branch("dEtaBB_L1L2frame_3l", 'F' ) 
        self.out.branch("dEtaBB_L1L3frame_3l", 'F' ) 

        self.out.branch("mTTH_2lss"        , 'F' ) 
        self.out.branch("mTTH_3l"        , 'F' ) 


        self.out.branch('mTTH_2lss1tau','F')
        self.out.branch('theta_higgs_ttbar_TTHsystem_2lss1tau','F')
        self.out.branch('thetaTopTop_ttbarframe_2lss1tau','F')


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

        for var in 'pt,eta,phi,mass,isBtag,isFromHadTop,btagDeepFlavB'.split(','):
            jetVar=[]
            for j in jets:
                if j.pt < 25: continue
                jetVar.append(getattr(j,var))

            self.out.fillBranch('SelJet_%s'%var, jetVar)

        ## b-jet related vars
        goodJetsByBtag = [j for j in jets if j.pt >= 25]
        if len(goodJetsByBtag)>=2:
            goodJetsByBtag.sort( key = lambda x : x.btagDeepFlavB, reverse=True)

            bbBost=goodJetsByBtag[0].p4()+goodJetsByBtag[1].p4()
            llBost=leps[0].p4()+leps[1].p4()
            
            l1_BBframe = deepcopy(leps[0].p4())
            l2_BBframe = deepcopy(leps[1].p4())
            l1_BBframe.Boost( -bbBost.BoostVector())
            l2_BBframe.Boost( -bbBost.BoostVector())
            
            b1_LLframe = deepcopy(goodJetsByBtag[0].p4())
            b2_LLframe = deepcopy(goodJetsByBtag[1].p4())
            b1_LLframe.Boost( -llBost.BoostVector())
            b2_LLframe.Boost( -llBost.BoostVector())
            
            dPhiLL_BBframe = l1_BBframe.DeltaPhi(l2_BBframe)
            dEtaLL_BBframe = abs(l1_BBframe.Eta() - l2_BBframe.Eta())
            dPhiBB_LLframe = b1_LLframe.DeltaPhi(b2_LLframe)
            dEtaBB_LLframe = abs(b1_LLframe.Eta() - b2_LLframe.Eta())
            dEtaBB         = abs(goodJetsByBtag[0].eta-goodJetsByBtag[1].eta)
        else:
            dPhiLL_BBframe = 0
            dEtaLL_BBframe = 0
            dPhiBB_LLframe = 0        
            dEtaBB_LLframe = 0
            dEtaBB         = 0

        jetsForMass= [j for j in jets if j.pt >= 25][:6]
        ttHsystem=leps[0].p4()+leps[1].p4()
        met=r.TLorentzVector()
        met.SetPtEtaPhiM( event.MET_pt, 0,event.MET_phi,0)
        ttHsystem = met + ttHsystem
        for j in jetsForMass:
            ttHsystem = ttHsystem  + j.p4()


        dEtaL1L2_BBframe_3l = 0
        dEtaL1L3_BBframe_3l = 0
        dEtaBB_L1L2frame_3l = 0
        dEtaBB_L1L3frame_3l = 0

        ttH_system3l=None

        if len(leps) > 2 and len(goodJetsByBtag)>1: 
            bbBost=goodJetsByBtag[0].p4()+goodJetsByBtag[1].p4()
            l1_BBframe = deepcopy(leps[0].p4()); l1_BBframe.Boost( -bbBost.BoostVector() ) 
            l2_BBframe = deepcopy(leps[1].p4()); l1_BBframe.Boost( -bbBost.BoostVector() ) 
            l3_BBframe = deepcopy(leps[2].p4()); l1_BBframe.Boost( -bbBost.BoostVector() ) 

            dEtaL1L2_BBframe_3l = abs(l1_BBframe.Eta()-l2_BBframe.Eta())
            dEtaL1L3_BBframe_3l = abs(l1_BBframe.Eta()-l3_BBframe.Eta())

            l1l2frame = (leps[0].p4()+leps[1].p4()).BoostVector()
            l1l3frame = (leps[0].p4()+leps[2].p4()).BoostVector()

            b1_L1L2frame = deepcopy(goodJetsByBtag[0].p4()) ; b1_L1L2frame.Boost(-l1l2frame)
            b2_L1L2frame = deepcopy(goodJetsByBtag[1].p4()) ; b2_L1L2frame.Boost(-l1l2frame)
            b1_L1L3frame = deepcopy(goodJetsByBtag[0].p4()) ; b1_L1L3frame.Boost(-l1l3frame)
            b2_L1L3frame = deepcopy(goodJetsByBtag[1].p4()) ; b2_L1L3frame.Boost(-l1l3frame)
            

            dEtaBB_L1L2frame_3l = abs( b1_L1L2frame.Eta() - b2_L1L2frame.Eta())
            dEtaBB_L1L3frame_3l = abs( b1_L1L3frame.Eta() - b2_L1L3frame.Eta())

            ttH_system3l = leps[0].p4()+leps[1].p4()+leps[2].p4()
            ttH_system3l = ttH_system3l + met
            jetsFor3LMass= [j for j in jets if j.pt >= 25][:4]
            for j in jetsFor3LMass:
                ttH_system3l = ttH_system3l + j.p4()

        mTTH_2lss1tau=0
        theta_higgs_ttbar_TTHsystem_2lss1tau=0
        thetaTopTop_ttbarframe_2lss1tau=0

        if self.is2lss1tau: 
            TTHsystem_2lss1tau=thetau.p4()+leps[0].p4()+leps[1].p4()
            jetsFor2Lss1tauMass=[j for j in jets if j.pt>=25][:4]
            for j in jetsFor2Lss1tauMass:
                TTHsystem_2lss1tau = TTHsystem_2lss1tau + j.p4()
            mTTH_2lss1tau=TTHsystem_2lss1tau.M()

            higgsLeptonIdx = 0 if deltaR(leps[0], thetau) < deltaR(leps[1], thetau) else 1 
            higgsLepton = leps[higgsLeptonIdx]
            otherLepton = leps[1-higgsLeptonIdx]
            ttbarjets=[]
            maxCSV=-2; lepTbjet=None


            for j in jetsFor2Lss1tauMass: 
                if j.isFromHadTop: 
                    ttbarjets.append(j)
                else:
                    if j.btagDeepFlavB  > maxCSV:
                        lepTbjet=j; maxCSV=j.btagDeepFlavB
            if lepTbjet:
                ttbarjets.append(lepTbjet)
            ttbarSystem=otherLepton.p4()
            hadTop=r.TLorentzVector()

            for j in ttbarjets:
                ttbarSystem = ttbarSystem + j.p4()
                hadTop = hadTop + j.p4()            

            visHiggsSystem = higgsLepton.p4() + thetau.p4()
            ttbarSystem.Boost( -TTHsystem_2lss1tau.BoostVector())
            visHiggsSystem.Boost( -TTHsystem_2lss1tau.BoostVector())
            theta_higgs_ttbar_TTHsystem_2lss1tau=ttbarSystem.Angle( visHiggsSystem.BoostVector() ) 
            
            otherLeptonTTbarFrame=otherLepton.p4()
            hadTop.Boost( -ttbarSystem.BoostVector())
            otherLeptonTTbarFrame.Boost(-ttbarSystem.BoostVector())
            thetaTopTop_ttbarframe_2lss1tau = hadTop.Angle(otherLeptonTTbarFrame.BoostVector())
            
            

        self.out.fillBranch('mTTH_2lss1tau',mTTH_2lss1tau)
        self.out.fillBranch('theta_higgs_ttbar_TTHsystem_2lss1tau',theta_higgs_ttbar_TTHsystem_2lss1tau)
        self.out.fillBranch('thetaTopTop_ttbarframe_2lss1tau',thetaTopTop_ttbarframe_2lss1tau)

        self.out.fillBranch('met',event.MET_pt)
        self.out.fillBranch('met_phi',event.MET_phi)
        self.out.fillBranch('HTT_score',  event.BDThttTT_eventReco_mvaValue)
        self.out.fillBranch('Higgs_pt',event.HTXS_Higgs_pt)
        self.out.fillBranch('Higgs_y',event.HTXS_Higgs_y)
        self.out.fillBranch('nSelJets', len(jetVar))   # outside the loop but on purpose
        self.out.fillBranch('mTTH_2lss',ttHsystem.M())
        self.out.fillBranch('mTTH_3l', ttH_system3l.M() if ttH_system3l else 0 )

        self.out.fillBranch('mT_lep2', event.MT_met_lep2)
        self.out.fillBranch('mT_lep1', event.MT_met_lep1)
        self.out.fillBranch("Hj_tagger_hadTop", event.BDThttTT_eventReco_Hj_score)
        self.out.fillBranch("mindr_lep2_jet", event.mindr_lep2_jet)
        self.out.fillBranch("mindr_lep1_jet", event.mindr_lep1_jet)
        self.out.fillBranch("avg_dr_jet", event.avg_dr_jet)

        self.out.fillBranch("dPhiLL_BBframe_2lss", dPhiLL_BBframe)         
        self.out.fillBranch("dEtaLL_BBframe_2lss", dEtaLL_BBframe)
        self.out.fillBranch("dPhiBB_LLframe_2lss", dPhiBB_LLframe)
        self.out.fillBranch("dEtaBB_LLframe_2lss", dEtaBB_LLframe)
        self.out.fillBranch("dEtaBB_2lss"        , dEtaBB        )     


        self.out.fillBranch("dEtaL1L2_BBframe_3l", dEtaL1L2_BBframe_3l)
        self.out.fillBranch("dEtaL1L3_BBframe_3l", dEtaL1L3_BBframe_3l)
        self.out.fillBranch("dEtaBB_L1L2frame_3l", dEtaBB_L1L2frame_3l)
        self.out.fillBranch("dEtaBB_L1L3frame_3l", dEtaBB_L1L3frame_3l)

        self.out.fillBranch('weight_SM'    , event.LHEReweightingWeight[11])
        self.out.fillBranch('weight_CP_odd', event.LHEReweightingWeight[59])
        self.out.fillBranch('weight_CP_mixed', event.LHEReweightingWeight[66])
        self.out.fillBranch('weight_CP_mixed_neg', event.LHEReweightingWeight[52])

        for br in self.extraVars:
            self.out.fillBranch(br[0],eval(br[1]))

        return True
