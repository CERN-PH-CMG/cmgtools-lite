from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection as Collection

class SynchTuples(Module):
    def __init__(self):
        self.generalVars = [
            'nEvent','ls','run',
            'n_presel_mu','n_fakeablesel_mu','n_mvasel_mu',
            'n_presel_ele','n_fakeablesel_ele','n_mvasel_ele',
            'n_presel_tau','n_presel_jet','n_presel_jetFwd',
            'n_presel_jetAK8',
        ]
        self.floatGeneralVars = [
            'PFMET','PFMETphi','MHT','metLD'
        ]
        self.lepVars = [ 'E','pt','eta','phi', 'conept','charge', 'miniRelIso','miniIsoCharged',
                        'miniIsoNeutral', 'jetPtRel', 'jetRelIso', 'jetDeepJet', 'sip3d',
                        'dxy', 'dz', 'leptonMVA', 'isfakeablesel', 'ismvasel', 'isGenMatched', 'tightCharge' ]

        self.muVars = [ 'segmentCompatibility', 'mediumID'
                        ]
       
        self.elVars = [ 'ntMVAeleID', 'passesConversionVeto','nMissingHits','sigmaEtaEta','HoE','OoEminusOoP',
                        'deltaEta'
        ]
        
        self.tauVars = [ 'pt','eta','phi', 'E','charge','dxy', 'dz','idMVAoldDMdR032017v2','decayModeFindingNewDMs']
        self.jetVars = [ 'pt','eta','phi','E','deepJet','QGdiscr']
        self.fwdJetVars = [ 'pt','eta']
        self.vars_2lss = {'avg_dr_jet'          : lambda ev : ev.avg_dr_jet,
                          #'ptmiss'              : lambda ev : ev.MET_pt, 
                          'mbb'                 : lambda ev : ev.mbb,
                          #'jet1_pt'             : lambda ev : ev.JetSel_Recl_pt[0] if ev.nJetSel_Recl > 0 else 0,
                          #'jet2_pt'             : lambda ev : ev.JetSel_Recl_pt[1] if ev.nJetSel_Recl > 1 else 0,
                          #'jet3_pt'             : lambda ev : ev.JetSel_Recl_pt[2] if ev.nJetSel_Recl > 2 else 0,
                          #'jet4_pt'             : lambda ev : ev.JetSel_Recl_pt[3] if ev.nJetSel_Recl > 3 else 0,
                          'max_lep_eta'         : lambda ev : max(abs(ev.LepGood_eta[int(ev.iLepFO_Recl[0])]),abs(ev.LepGood_eta[int(ev.iLepFO_Recl[1])])) if ev.nLepFO_Recl > 1 else 0,
                          'mT_lep1'             : lambda ev : ev.MT_met_lep1,
                          #'lep1_conept'         : lambda ev : ev.LepGood_conePt[int(ev.iLepFO_Recl[0])], 
                          'mindr_lep1_jet'     : lambda ev : ev.mindr_lep1_jet,
                          'mT_lep2'             : lambda ev : ev.MT_met_lep2,
                          #'lep2_conept'         : lambda ev : ev.LepGood_conePt[int(ev.iLepFO_Recl[1])],
                          'mindr_lep2_jet'     : lambda ev : ev.mindr_lep2_jet,
                          #'nJetForward'         : lambda ev : ev.nFwdJet_Recl,
                          #'jetForward1_pt'      : lambda ev : ev.FwdJet1_pt_Recl,
                          #'jetForward1_eta_abs' : lambda ev : abs(ev.FwdJet1_eta_Recl),
                          'HTT'  : lambda ev : ev.BDThttTT_eventReco_mvaValue,
                          'HadTop_pt': lambda ev : ev.BDThttTT_eventReco_HadTop_pt,
                          'nJet'                : lambda ev : ev.nJet25_Recl,
                          'nBJetLoose'          : lambda ev : ev.nBJetLoose25_Recl,
                          'nBJetMedium'         : lambda ev : ev.nBJetMedium25_Recl,
                          'nElectron'           : lambda ev : abs(ev.LepGood_pdgId[int(ev.iLepFO_Recl[0])]) == 11 + abs(ev.LepGood_pdgId[int(ev.iLepFO_Recl[1])]) == 11 if ev.nLepFO_Recl > 1 else 0,
                          'sum_lep_charge'      : lambda ev : ev.LepGood_charge[int(ev.iLepFO_Recl[0])] + ev.LepGood_charge[int(ev.iLepFO_Recl[1])] if ev.nLepFO_Recl > 1 else 0,
                          'mvaOutput_Hj_tagger' : lambda ev : ev.BDThttTT_eventReco_Hj_score, 
                          'mvaOutput_2lss_ttH_tH_4cat_onlyTHQ_v4_ttH' : lambda ev : ev.DNN_2lss_predictions_ttH,
                          'mvaOutput_2lss_ttH_tH_4cat_onlyTHQ_v4_ttW' : lambda ev : ev.DNN_2lss_predictions_ttW,
                          'mvaOutput_2lss_ttH_tH_4cat_onlyTHQ_v4_rest' : lambda ev : ev.DNN_2lss_predictions_rest,
                          'mvaOutput_2lss_ttH_tH_4cat_onlyTHQ_v4_tH' : lambda ev : ev.DNN_2lss_predictions_tH,
                      }

        
        
        self.vars = ['mu%d_%s'%(i,x) for i in range(1,5) for x in (self.muVars+self.lepVars)] + ['ele%d_%s'%(i,x) for i in range(1,5) for x in (self.elVars+self.lepVars)] 
        self.vars.extend( [ 'tau%d_%s'%(i,x) for i in range(1,3) for x in self.tauVars] + ['jet%d_%s'%(i,x) for i in range(1,5) for x in self.jetVars] + ['jetFwd1_%s'%(x) for x in self.fwdJetVars] )
        self.vars.extend( self.generalVars  + self.floatGeneralVars)  
        self.vars.extend( [ x for x in self.vars_2lss])


    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        for var in self.vars:
            self.out.branch( var, 'I' if var in self.generalVars else 'F')

    def analyze(self, event):
        
        self.out.fillBranch('nEvent', event.event)
        self.out.fillBranch('ls',event.luminosityBlock)
        self.out.fillBranch('run', event.run)
        self.out.fillBranch('PFMET', event.MET_pt if event.year != 2017 else event.METFixEE2017_pt)
        self.out.fillBranch('PFMETphi',event.MET_phi if event.year != 2017 else event.METFixEE2017_phi)
        self.out.fillBranch('MHT',event.mhtJet25_Recl)
        self.out.fillBranch('metLD', event.MET_pt if event.year != 2017 else event.METFixEE2017_pt + event.mhtJet25_Recl*0.4)

        
        all_leps = [l for l in Collection(event,"LepGood")]
        nFO = getattr(event,"nLepFO_Recl")
        chosen = getattr(event,"iLepFO_Recl")
        leps = [all_leps[chosen[i]] for i in xrange(nFO)]

        n_presel_mu = 0
        n_presel_ele = 0
        n_fakeablesel_mu = 0
        n_mvasel_mu = 0
        n_fakeablesel_ele = 0
        n_mvasel_ele = 0
        for lep in all_leps:
            if abs(lep.pdgId) == 11: 
                flav = 'ele'
                n_presel_ele = n_presel_ele + 1 
                if (lep in leps): n_fakeablesel_ele = n_fakeablesel_ele + 1 
                if lep.isLepTight_Recl: n_mvasel_ele = n_mvasel_ele + 1 
                if n_presel_ele > 2: continue
                self.out.fillBranch('%s%d_ntMVAeleID'          %(flav,n_presel_ele), lep.mvaFall17V2noIso)
                self.out.fillBranch('%s%d_passesConversionVeto'%(flav,n_presel_ele), lep.convVeto)
                self.out.fillBranch('%s%d_nMissingHits'        %(flav,n_presel_ele), lep.lostHits)
                self.out.fillBranch('%s%d_sigmaEtaEta'         %(flav,n_presel_ele), lep.sieie)
                self.out.fillBranch('%s%d_HoE'                 %(flav,n_presel_ele), lep.sieie)
                self.out.fillBranch('%s%d_OoEminusOoP'         %(flav,n_presel_ele), lep.eInvMinusPInv)
                self.out.fillBranch('%s%d_deltaEta'            %(flav,n_presel_ele), lep.deltaEtaSC)


            if abs(lep.pdgId) == 13: 
                flav = 'mu'
                n_presel_mu = n_presel_mu + 1 
                if (lep in leps): n_fakeablesel_mu = n_fakeablesel_mu + 1 
                if lep.isLepTight_Recl: n_mvasel_mu = n_mvasel_mu + 1 
                if n_presel_mu > 2: continue
                self.out.fillBranch('%s%d_segmentCompatibility'%(flav,n_presel_mu), lep.segmentComp)
                self.out.fillBranch('%s%d_mediumID'            %(flav,n_presel_mu), lep.mediumId)
                

            self.out.fillBranch('%s%d_pt'%(flav, eval('n_presel_%s'%flav)), lep.pt)
            self.out.fillBranch('%s%d_eta'%(flav, eval('n_presel_%s'%flav)), lep.eta)
            self.out.fillBranch('%s%d_phi'%(flav, eval('n_presel_%s'%flav)), lep.phi)            
            self.out.fillBranch('%s%d_conept'%(flav, eval('n_presel_%s'%flav)), lep.conePt)            
            self.out.fillBranch('%s%d_charge'%(flav, eval('n_presel_%s'%flav)), lep.charge)
            self.out.fillBranch('%s%d_miniRelIso'%(flav, eval('n_presel_%s'%flav)), lep.miniPFRelIso_all)
            self.out.fillBranch('%s%d_miniIsoCharged'%(flav, eval('n_presel_%s'%flav)), lep.miniPFRelIso_chg)
            self.out.fillBranch('%s%d_miniIsoNeutral'%(flav, eval('n_presel_%s'%flav)), lep.miniPFRelIso_all-lep.miniPFRelIso_chg)
            self.out.fillBranch('%s%d_jetPtRel'%(flav, eval('n_presel_%s'%flav)), lep.jetPtRelv2)
            self.out.fillBranch('%s%d_jetRelIso'%(flav, eval('n_presel_%s'%flav)), lep.jetRelIso)
            self.out.fillBranch('%s%d_jetDeepJet'%(flav, eval('n_presel_%s'%flav)), lep.jetBTagDeepFlav)
            self.out.fillBranch('%s%d_sip3d'%(flav, eval('n_presel_%s'%flav)), lep.sip3d)
            self.out.fillBranch('%s%d_dxy'%(flav, eval('n_presel_%s'%flav)), lep.dxy)
            self.out.fillBranch('%s%d_dz'%(flav, eval('n_presel_%s'%flav)), lep.dz)
            self.out.fillBranch('%s%d_leptonMVA'%(flav, eval('n_presel_%s'%flav)), lep.mvaTTH)
            self.out.fillBranch('%s%d_isfakeablesel'%(flav, eval('n_presel_%s'%flav)), lep in leps)
            self.out.fillBranch('%s%d_ismvasel'%(flav, eval('n_presel_%s'%flav)), lep.isLepTight_Recl)
            self.out.fillBranch('%s%d_isGenMatched'%(flav, eval('n_presel_%s'%flav)), lep.genPartFlav == 1 or lep.genPartFlav == 15)
            self.out.fillBranch('%s%d_tightCharge'%(flav, eval('n_presel_%s'%flav)), lep.tightCharge >= 2 )
            self.out.fillBranch('%s%d_E'%(flav, eval('n_presel_%s'%flav)), lep.p4().E())
            
            
        if n_presel_mu < 2: 
            for mu in range(n_presel_mu+1,3):
                for var in self.lepVars + self.muVars:
                    self.out.fillBranch('mu%d_%s'%(mu,var),-9999)
        if n_presel_ele < 2: 
            for el in range(n_presel_ele+1,3):
                for var in self.lepVars + self.elVars:
                    self.out.fillBranch('ele%d_%s'%(el,var),-9999)
        

            
        self.out.fillBranch( 'n_presel_mu', n_presel_mu)
        self.out.fillBranch( 'n_fakeablesel_mu', n_fakeablesel_mu)
        self.out.fillBranch( 'n_mvasel_mu', n_mvasel_mu)
        self.out.fillBranch( 'n_presel_ele', n_presel_ele)
        self.out.fillBranch( 'n_fakeablesel_ele', n_fakeablesel_ele)
        self.out.fillBranch( 'n_mvasel_ele', n_mvasel_ele)

        n_presel_jet = 0
        jets = [j for j in Collection(event,"JetSel_Recl")]
        for jet in jets: 
            if jet.pt < 25: continue
            n_presel_jet = n_presel_jet + 1 
            if n_presel_jet> 4: continue
            self.out.fillBranch('jet%d_pt'%(n_presel_jet), jet.pt)
            self.out.fillBranch('jet%d_eta'%(n_presel_jet), jet.eta)
            self.out.fillBranch('jet%d_phi'%(n_presel_jet), jet.phi)
            self.out.fillBranch('jet%d_E'%(n_presel_jet), jet.p4().E())
            self.out.fillBranch('jet%d_deepJet'%(n_presel_jet), jet.btagDeepFlavB)
            self.out.fillBranch('jet%d_QGdiscr'%(n_presel_jet), jet.qgl)

        if n_presel_jet < 4: 
            for el in range(n_presel_jet+1,5):
                for var in self.jetVars:
                    self.out.fillBranch('jet%d_%s'%(el,var),-9999)

        
        self.out.fillBranch('n_presel_jet',n_presel_jet)
        self.out.fillBranch('n_presel_jetFwd', event.nFwdJet_Recl)
        if event.nFwdJet_Recl: 
            self.out.fillBranch('jetFwd1_pt' , event.FwdJet1_pt_Recl)
            self.out.fillBranch('jetFwd1_eta', event.FwdJet1_eta_Recl)
        else:
            self.out.fillBranch('jetFwd1_pt' , -9999)
            self.out.fillBranch('jetFwd1_eta', -9999)

        for var in self.vars_2lss:
            self.out.fillBranch(var, self.vars_2lss[var](event))
        

        return True
