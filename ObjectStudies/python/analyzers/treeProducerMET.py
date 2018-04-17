from PhysicsTools.Heppy.analyzers.core.AutoFillTreeProducer  import * 

met_globalVariables = [
    NTupleVariable("rho",  lambda ev: ev.rho, float, help="kt6PFJets rho"),
    NTupleVariable("nVert",  lambda ev: len(ev.goodVertices), int, help="Number of good vertices"),
##    NTupleVariable("nPU",  lambda ev: ev.nPU, long, help="getPU_NumInteractions"),

##    NTupleVariable("ntracksPV",  lambda ev: ev.goodVertices[0].tracksSize() , int, help="Number of tracks (with weight > 0.5)"),
##    NTupleVariable("ndofPV",  lambda ev: ev.goodVertices[0].ndof() , int, help="Degrees of freedom of the fit"),

   # ----------------------- lepton info -------------------------------------------------------------------- #     
    NTupleVariable("nLeptons",   lambda x : len(x.leptons) if  hasattr(x,'leptons') else  0 , float, mcOnly=False,help="Number of associated leptons"),
    NTupleVariable("nLepGood20", lambda ev: sum([l.pt() > 20 for l in ev.selectedLeptons]), int, help="Number of leptons with pt > 20"),
    NTupleVariable("nLepGood15", lambda ev: sum([l.pt() > 15 for l in ev.selectedLeptons]), int, help="Number of leptons with pt > 15"),
    NTupleVariable("nLepGood10", lambda ev: sum([l.pt() > 10 for l in ev.selectedLeptons]), int, help="Number of leptons with pt > 10"),


    NTupleVariable("zll_pt", lambda ev : ev.zll_p4.Pt() if  hasattr(ev,'zll_p4') else  0 , help="Pt of di-lepton system"),
    NTupleVariable("zll_eta", lambda ev : ev.zll_p4.Eta() if  hasattr(ev,'zll_p4') else  0, help="Eta of di-lepton system"),
    NTupleVariable("zll_phi", lambda ev : ev.zll_p4.Phi() if  hasattr(ev,'zll_p4') else  0, help="Phi of di-lepton system"),
    NTupleVariable("zll_mass", lambda ev : ev.zll_p4.M() if  hasattr(ev,'zll_p4') else  0, help="Invariant mass of di-lepton system"),

   # ----------------------- MET filter information (temporary)  -------------------------------------------------------------------- #

    # comment to use the official as stored in miniAOD 76
#    NTupleVariable("Flag_HBHENoiseFilter", lambda ev: ev.hbheFilterNew, help="HBEHE temporary filter decision"),
#    NTupleVariable("Flag_HBHEIsoNoiseFilter", lambda ev: ev.hbheFilterIso, help="HBEHE isolation temporary filter decision"),
    NTupleVariable("Flag_badChargedHadronFilter", lambda ev: ev.badChargedHadron, help="bad charged hadron filter decision"),

    NTupleVariable("Flag_badMuonMoriond2017",  lambda ev: ev.badMuonMoriond2017, int, help="bad muon found in event (Moriond 2017 filter)?"),
    NTupleVariable("Flag_badCloneMuonMoriond2017",  lambda ev: ev.badCloneMuonMoriond2017, int, help="clone muon found in event (Moriond 2017 filter)?"),
    NTupleVariable("badCloneMuonMoriond2017_maxPt",  lambda ev: max(mu.pt() for mu in ev.badCloneMuonMoriond2017_badMuons) if not ev.badCloneMuonMoriond2017 else 0, help="max pt of any clone muon found in event (Moriond 2017 filter)"),
    NTupleVariable("badNotCloneMuonMoriond2017_maxPt",  lambda ev: max((mu.pt() if mu not in ev.badCloneMuonMoriond2017_badMuons else 0) for mu in ev.badMuonMoriond2017_badMuons) if not ev.badMuonMoriond2017 else 0, help="max pt of any bad non-clone muon found in event (Moriond 2017 filter)"),

    NTupleVariable("metPuppi_EGCorX", lambda ev : ev.met_EGCorXPuppi if  hasattr(ev,'met_EGCorXPuppi') else  0 , help="Puppi EGCorX"),
    NTupleVariable("metPuppi_EGCorY", lambda ev : ev.met_EGCorYPuppi if  hasattr(ev,'met_EGCorYPuppi') else  0 , help="Puppi EGCorY"),

   # ----------------------- jet info  --------------------------------------------------------------------- #

    NTupleVariable("jet1_pt", lambda ev : ev.cleanJets[0].pt() if len(ev.cleanJets)>0 else -99, help="pt of leading central jet"),
    NTupleVariable("jet2_pt", lambda ev : ev.cleanJets[1].pt() if len(ev.cleanJets)>1 else -99, help="pt of second central jet"),
    NTupleVariable("nJet40", lambda ev: sum([j.pt() > 40 for j in ev.cleanJets]), int, help="Number of jets with pt > 40, |eta|<2.4"),

    NTupleVariable("jetPuppi1_pt", lambda ev : ev.cleanJetsPuppi[0].pt() if len(ev.cleanJetsPuppi)>0 else -99, help="pt of leading central jet"),
    NTupleVariable("jetPuppi2_pt", lambda ev : ev.cleanJetsPuppi[1].pt() if len(ev.cleanJetsPuppi)>1 else -99, help="pt of second central jet"),
    NTupleVariable("nJetPuppi40", lambda ev: sum([j.pt() > 40 for j in ev.cleanJetsPuppi]), int, help="Number of jets with pt > 40, |eta|<2.4"),

   # ----------------------- dedicated met info -------------------------------------------------------------------- #

    NTupleVariable("met_uPara_zll", lambda ev : ev.met.upara_zll if  hasattr(ev,'zll_p4') else -999 , help="recoil MET"),
    NTupleVariable("met_uPerp_zll", lambda ev : ev.met.uperp_zll if  hasattr(ev,'zll_p4') else -999 , help="recoil MET"),

    NTupleVariable("met_jecDown_uPara_zll", lambda ev : ev.met_jecDown.upara_zll if  hasattr(ev,'zll_p4') else -999 , help="recoil MET jecDown"),
    NTupleVariable("met_jecDown_uPerp_zll", lambda ev : ev.met_jecDown.uperp_zll if  hasattr(ev,'zll_p4') else -999 , help="recoil MET jecDown"),

    NTupleVariable("met_jecUp_uPara_zll", lambda ev : ev.met_jecUp.upara_zll if  hasattr(ev,'zll_p4') else -999 , help="recoil MET jecUp"),
    NTupleVariable("met_jecUp_uPerp_zll", lambda ev : ev.met_jecUp.uperp_zll if  hasattr(ev,'zll_p4') else -999 , help="recoil MET jecUp"),

    NTupleVariable("met_sig", lambda ev : ev.met_sig, help="met significance, filled when running preprocessor"),

#    NTupleVariable("metNoHF_uPara_zll", lambda ev : ev.metNoHF.upara_zll if hasattr(ev,'metNoHF') and hasattr(ev,'zll_p4') else -999 , help="recoil MET"),
#    NTupleVariable("metNoHF_uPerp_zll", lambda ev : ev.metNoHF.uperp_zll if hasattr(ev,'metNoHF') and hasattr(ev,'zll_p4') else -999 , help="recoil MET"),

    NTupleVariable("metPuppi_uPara_zll", lambda ev : ev.metPuppi.upara_zll if hasattr(ev,'metPuppi') and hasattr(ev,'zll_p4') else -999 , help="recoil MET puppi"),
    NTupleVariable("metPuppi_uPerp_zll", lambda ev : ev.metPuppi.uperp_zll if hasattr(ev,'metPuppi') and hasattr(ev,'zll_p4') else -999 , help="recoil MET puppi"),

    NTupleVariable("metPuppi_sig", lambda ev : ev.met_sigPuppi, help="met significance, filled when running preprocessor"),

    NTupleVariable("met_raw_uPara_zll", lambda ev : ev.met_raw.upara_zll if  hasattr(ev,'zll_p4') else -999 , help="recoil MET raw"),
    NTupleVariable("met_raw_uPerp_zll", lambda ev : ev.met_raw.uperp_zll if  hasattr(ev,'zll_p4') else -999 , help="recoil MET raw"),

    NTupleVariable("met_caloPt", lambda ev : ev.met.caloMETPt(), help="calo met p_{T}"),
    NTupleVariable("met_caloPhi", lambda ev : ev.met.caloMETPhi(), help="calo met phi"),
    NTupleVariable("met_caloSumEt", lambda ev : ev.met.caloMETSumEt(), help="calo met sumEt"),

   # ----------------------- type1met studies info -------------------------------------------------------------------- #     

#    NTupleVariable("met_JetEnUp_Pt", lambda ev : ev.met.shiftedPt(ev.met.JetEnUp, ev.met.Raw), help="type1, JetEnUp, pt"),
#    NTupleVariable("met_JetEnUp_Phi", lambda ev : ev.met.shiftedPhi(ev.met.JetEnUp, ev.met.Raw), help="type1, JetEnUp, phi"),

#    NTupleVariable("met_JetEnDown_Pt", lambda ev : ev.met.shiftedPt(ev.met.JetEnDown, ev.met.Raw), help="type1, JetEnDown, pt"),
#    NTupleVariable("met_JetEnDown_Phi", lambda ev : ev.met.shiftedPhi(ev.met.JetEnDown, ev.met.Raw), help="type1, JetEnDown, phi"),

#    NTupleVariable("metNoHF_JetEnUp_Pt", lambda ev : ev.metNoHF.shiftedPt(ev.met.JetEnUp, ev.met.Raw) if hasattr(ev,'metNoHF') else -999, help="type1 noHF , JetEnUp, pt"),
#    NTupleVariable("metNoHF_JetEnUp_Phi", lambda ev : ev.metNoHF.shiftedPhi(ev.met.JetEnUp, ev.met.Raw) if hasattr(ev,'metNoHF') else -999, help="type1 noHF , JetEnUp, phi"),

#    NTupleVariable("metNoHF_JetEnDown_Pt", lambda ev : ev.metNoHF.shiftedPt(ev.met.JetEnDown, ev.met.Raw) if hasattr(ev,'metNoHF') else -999, help="type1 noHF , JetEnDown, pt"),
#    NTupleVariable("metNoHF_JetEnDown_Phi", lambda ev : ev.metNoHF.shiftedPhi(ev.met.JetEnDown, ev.met.Raw) if hasattr(ev,'metNoHF') else -999, help="type1 noHF , JetEnDown, phi"),

   # --------------------------------------------------------

#    NTupleVariable("ak4MET_Pt", lambda ev : ev.ak4MET.pt() if  hasattr(ev,'ak4MET') else  0 , help="type1, V4, pt"),
#    NTupleVariable("ak4MET_Phi", lambda ev : ev.ak4MET.phi() if  hasattr(ev,'ak4MET') else  0 , help="type1, V4, phi"),

#    NTupleVariable("ak4chsMET_Pt", lambda ev : ev.ak4chsMET.pt() if  hasattr(ev,'ak4chsMET') else  0 , help="type1, V4, pt"),
#    NTupleVariable("ak4chsMET_Phi", lambda ev : ev.ak4chsMET.phi() if  hasattr(ev,'ak4chsMET') else  0 , help="type1, V4, phi"),

#    NTupleVariable("ak420MET_Pt", lambda ev : ev.ak4pt20MET.pt() if  hasattr(ev,'ak4pt20MET') else  0 , help="type1, V4, pt20, pt"),
#    NTupleVariable("ak420MET_Phi", lambda ev : ev.ak4pt20MET.phi() if  hasattr(ev,'ak4pt20MET') else  0 , help="type1, V4, pt20, phi"),

#    NTupleVariable("ak4chs20MET_Pt", lambda ev : ev.ak4chspt20MET.pt() if  hasattr(ev,'ak4chspt20MET') else  0 , help="type1, V4, pt20, pt"),
#    NTupleVariable("ak4chs20MET_Phi", lambda ev : ev.ak4chspt20MET.phi() if  hasattr(ev,'ak4chspt20MET') else  0 , help="type1, V4, pt>20, phi"),

#    NTupleVariable("ak4Mix_Pt", lambda ev : ev.ak4Mix.pt() if  hasattr(ev,'ak4Mix') else  0 , help="type1, V4, pt20, Mix, pt"),
#    NTupleVariable("ak4Mix_Phi", lambda ev : ev.ak4Mix.phi() if  hasattr(ev,'ak4Mix') else  0 , help="type1, V4, pt>20, Mix, phi"),

   # ----------------------- tkMet info -------------------------------------------------------------------- #     

    NTupleVariable("tkmet_genPt", lambda ev : ev.tkGenMet.pt() if  hasattr(ev,'tkGenMet') else  0 , help="TK E_{T}^{miss} dz<0.1 pt"),
    NTupleVariable("tkmet_genPhi", lambda ev : ev.tkGenMet.phi() if  hasattr(ev,'tkGenMet') else  0 , help="TK E_{T}^{miss} dz<0.1 phi"),

    ##
    NTupleVariable("tkmet_pt", lambda ev : ev.tkMet.pt() if  hasattr(ev,'tkMet') else  0, help="TK E_{T}^{miss} dz<0.1 pt"),
    NTupleVariable("tkmet_phi", lambda ev : ev.tkMet.phi() if  hasattr(ev,'tkMet') else  0 , help="TK E_{T}^{miss} dz<0.1 phi"),
    NTupleVariable("tkmet_sumEt", lambda ev : ev.tkMet.sumEt if  hasattr(ev,'tkMet') else  0 , help="TK sumEt charged dz<0.1 pt"),

    NTupleVariable("tkmet_uPara_zll", lambda ev : ev.tkMet.upara_zll if  hasattr(ev,'tkMet') and hasattr(ev,'zll_p4') else -999 , help="TK sumEt charged dz<0.1 pt"),
    NTupleVariable("tkmet_uPerp_zll", lambda ev : ev.tkMet.uperp_zll if  hasattr(ev,'tkMet') and hasattr(ev,'zll_p4') else -999 , help="TK sumEt charged dz<0.1 pt"),

    ##
    NTupleVariable("tkmetchs_pt", lambda ev : ev.tkMetPVchs.pt() if  hasattr(ev,'tkMetPVchs') else  0, help="TK E_{T}^{miss} fromPV>0 pt"),
    NTupleVariable("tkmetchs_phi", lambda ev : ev.tkMetPVchs.phi() if  hasattr(ev,'tkMetPVchs') else  0, help="TK E_{T}^{miss} fromPV>0 phi"),
    NTupleVariable("tkmetchs_sumEt", lambda ev : ev.tkMetPVchs.sumEt if  hasattr(ev,'tkMetPVchs') else  0, help="TK sumEt charged fromPV>0"),

    NTupleVariable("tkmetchs_uPara_zll", lambda ev : ev.tkMetPVchs.upara_zll if  hasattr(ev,'tkMetPVchs') and hasattr(ev,'zll_p4') else -999 , help="TK sumEt charged fromPV>0 pt"),
    NTupleVariable("tkmetchs_uPerp_zll", lambda ev : ev.tkMetPVchs.uperp_zll if  hasattr(ev,'tkMetPVchs') and hasattr(ev,'zll_p4') else -999 , help="TK sumEt charged fromPV>0 pt"),

#    NTupleVariable("tkmetPVLoose_pt", lambda ev : ev.tkMetPVLoose.pt(), help="TK E_{T}^{miss} fromPV>0 pt"),
#    NTupleVariable("tkmetPVLoose_phi", lambda ev : ev.tkMetPVLoose.phi(), help="TK E_{T}^{miss} fromPV>0 phi"),
#    NTupleVariable("tkmetPVLoose_sumEt", lambda ev : ev.tkMetPVLoose.sumEt, help="TK sumEt charged fromPV>0"),

    NTupleVariable("tkmetPVTight_pt", lambda ev : ev.tkMetPVTight.pt(), help="TK E_{T}^{miss} fromPV>1 pt"),
    NTupleVariable("tkmetPVTight_phi", lambda ev : ev.tkMetPVTight.phi(), help="TK E_{T}^{miss} fromPV>1 phi"),
    NTupleVariable("tkmetPVTight_sumEt", lambda ev : ev.tkMetPVTight.sumEt, help="TK sumEt charged fromPV>1"),

    NTupleVariable("tkmetNoPV_pt", lambda ev : ev.tkMetNoPV.pt() if  hasattr(ev,'tkMetNoPV') else  0, help="TK E_{T}^{miss} fromPV>0 pt"),
    NTupleVariable("tkmetNoPV_phi", lambda ev : ev.tkMetNoPV.phi() if  hasattr(ev,'tkMetNoPV') else  0, help="TK E_{T}^{miss} fromPV>0 phi"),
    NTupleVariable("tkmetNoPV_sumEt", lambda ev : ev.tkMetNoPV.sumEt if  hasattr(ev,'tkMetNoPV') else  0, help="TK sumEt charged fromPV>0"),


    NTupleVariable("tkmetPVUsedInFit_pt", lambda ev : ev.tkMetPVUsedInFit.pt() if  hasattr(ev,'tkMetPVUsedInFit') else  0, help="TK E_{T}^{miss} fromPV>0 pt"),
    NTupleVariable("tkmetPVUsedInFit_phi", lambda ev : ev.tkMetPVUsedInFit.phi() if  hasattr(ev,'tkMetPVUsedInFit') else  0, help="TK E_{T}^{miss} fromPV>0 phi"),
#    NTupleVariable("tkmetPVUsedInFit_sumEt", lambda ev : ev.tkMetPVUsedInFit.sumEt if  hasattr(ev,'tkMetPVUsedInFit') else  0, help="TK sumEt charged fromPV>0 sumEt"),
    NTupleVariable("tkmetUsedInFitTight_pt", lambda ev : ev.tkMetUsedInFitTight.pt() if  hasattr(ev,'tkMetUsedInFitTight') else  0, help="TK E_{T}^{miss} fromPV>0 pt"),
    NTupleVariable("tkmetUsedInFitTight_phi", lambda ev : ev.tkMetUsedInFitTight.phi() if  hasattr(ev,'tkMetUsedInFitTight') else  0, help="TK E_{T}^{miss} fromPV>0 phi"),
#    NTupleVariable("tkmetUsedInFitTight_sumEt", lambda ev : ev.tkMetUsedInFitTight.sumEt if  hasattr(ev,'tkMetUsedInFitTight') else  0, help="TK sumEt charged fromPV>0 sumEt"),
    NTupleVariable("tkmetUsedInFitLoose_pt", lambda ev : ev.tkMetUsedInFitLoose.pt() if  hasattr(ev,'tkMetUsedInFitLoose') else  0, help="TK E_{T}^{miss} fromPV>0 pt"),
    NTupleVariable("tkmetUsedInFitLoose_phi", lambda ev : ev.tkMetUsedInFitLoose.phi() if  hasattr(ev,'tkMetUsedInFitLoose') else  0, help="TK E_{T}^{miss} fromPV>0 phi"),
#    NTupleVariable("tkmetUsedInFitLoose_sumEt", lambda ev : ev.tkMetUsedInFitLoose.sumEt if  hasattr(ev,'tkMetUsedInFitLoose') else  0, help="TK sumEt charged fromPV>0 sumEt"),
    NTupleVariable("tkmetCompatibilityDz_pt", lambda ev : ev.tkMetCompatibilityDz.pt() if  hasattr(ev,'tkMetCompatibilityDz') else  0, help="TK E_{T}^{miss} fromPV>0 pt"),
    NTupleVariable("tkmetCompatibilityDz_phi", lambda ev : ev.tkMetCompatibilityDz.phi() if  hasattr(ev,'tkMetCompatibilityDz') else  0, help="TK E_{T}^{miss} fromPV>0 phi"),
#    NTupleVariable("tkmetCompatibilityDz_sumEt", lambda ev : ev.tkMetCompatibilityDz.sumEt if  hasattr(ev,'tkMetCompatibilityDz') else  0, help="TK sumEt charged fromPV>0 sumEt"),
    NTupleVariable("tkmetCompatibilityBTag_pt", lambda ev : ev.tkMetCompatibilityBTag.pt() if  hasattr(ev,'tkMetCompatibilityBTag') else  0, help="TK E_{T}^{miss} fromPV>0 pt"),
    NTupleVariable("tkmetCompatibilityBTag_phi", lambda ev : ev.tkMetCompatibilityBTag.phi() if  hasattr(ev,'tkMetCompatibilityBTag') else  0, help="TK E_{T}^{miss} fromPV>0 phi"),
#    NTupleVariable("tkmetCompatibilityBTag_sumEt", lambda ev : ev.tkMetCompatibilityBTag.sumEt if  hasattr(ev,'tkMetCompatibilityBTag') else  0, help="TK E_{T}^{miss} fromPV>0 sumEt"),
    NTupleVariable("tkmetNotReconstructedPrimary_pt", lambda ev : ev.tkMetNotReconstructedPrimary.pt() if  hasattr(ev,'tkMetNotReconstructedPrimary') else  0, help="TK E_{T}^{miss} fromPV>0 pt"),
    NTupleVariable("tkmetNotReconstructedPrimary_phi", lambda ev : ev.tkMetNotReconstructedPrimary.phi() if  hasattr(ev,'tkMetNotReconstructedPrimary') else  0, help="TK E_{T}^{miss} fromPV>0 phi"),
#    NTupleVariable("tkmetNotReconstructedPrimary_sumEt", lambda ev : ev.tkMetNotReconstructedPrimary.sumEt if  hasattr(ev,'tkMetNotReconstructedPrimary') else  0, help="TK E_{T}^{miss} fromPV>0 sumEt"),
    NTupleVariable("tkmetOtherDeltaZ_pt", lambda ev : ev.tkMetOtherDeltaZ.pt() if  hasattr(ev,'tkMetOtherDeltaZ') else  0, help="TK E_{T}^{miss} fromPV>0 pt"),
    NTupleVariable("tkmetOtherDeltaZ_phi", lambda ev : ev.tkMetOtherDeltaZ.phi() if  hasattr(ev,'tkMetOtherDeltaZ') else  0, help="TK E_{T}^{miss} fromPV>0 phi"),
#    NTupleVariable("tkmetOtherDeltaZ_sumEt", lambda ev : ev.tkMetOtherDeltaZ.sumEt if  hasattr(ev,'tkMetOtherDeltaZ') else  0, help="TK E_{T}^{miss} fromPV>0 sumEt"),

#    NTupleVariable("tkmetPuppichs_pt", lambda ev : ev.tkMetPuppiPVchs.pt() if  hasattr(ev,'tkMetPuppiPVchs') else  0, help="TK Puppi E_{T}^{miss} fromPV>0 pt"),
#    NTupleVariable("tkmetPuppichs_phi", lambda ev : ev.tkMetPuppiPVchs.phi() if  hasattr(ev,'tkMetPuppiPVchs') else  0, help="TK PuppiE_{T}^{miss} fromPV>0 phi"),
#    NTupleVariable("tkmetPuppichs_sumEt", lambda ev : ev.tkMetPuppiPVchs.sumEt if  hasattr(ev,'tkMetPuppiPVchs') else  0, help="TK PuppisumEt charged fromPV>0"),
#    NTupleVariable("tkmetPuppiPVLoose_pt", lambda ev : ev.tkMetPuppiPVLoose.pt() if  hasattr(ev,'tkMetPuppiPVLoose') else  0, help="TK PuppiE_{T}^{miss} fromPV>0 pt"),
#    NTupleVariable("tkmetPuppiPVLoose_phi", lambda ev : ev.tkMetPuppiPVLoose.phi() if  hasattr(ev,'tkMetPuppiPVLoose') else  0, help="TK PuppiE_{T}^{miss} fromPV>0 phi"),
#    NTupleVariable("tkmetPuppiPVLoose_sumEt", lambda ev : ev.tkMetPuppiPVLoose.sumEt if  hasattr(ev,'tkMetPuppiPVLoose') else  0, help="TK PuppisumEt charged fromPV>0"),
#    NTupleVariable("tkmetPuppiPVTight_pt", lambda ev : ev.tkMetPuppiPVTight.pt() if  hasattr(ev,'tkMetPuppiPVTight') else  0, help="TK PuppiE_{T}^{miss} fromPV>0 pt"),
#    NTupleVariable("tkmetPuppiPVTight_phi", lambda ev : ev.tkMetPuppiPVTight.phi() if  hasattr(ev,'tkMetPuppiPVTight') else  0, help="TK PuppiE_{T}^{miss} fromPV>0 phi"),
#    NTupleVariable("tkmetPuppiPVTight_sumEt", lambda ev : ev.tkMetPuppiPVTight.sumEt if  hasattr(ev,'tkMetPuppiPVTight') else  0, help="TK PuppisumEt charged fromPV>0"),
#    NTupleVariable("tkmetPuppiNoPV_pt", lambda ev : ev.tkMetPuppiNoPV.pt() if  hasattr(ev,'tkMetPuppiNoPV') else  0, help="TK PuppiE_{T}^{miss} fromPV>0 pt"),
#    NTupleVariable("tkmetPuppiNoPV_phi", lambda ev : ev.tkMetPuppiNoPV.phi() if  hasattr(ev,'tkMetPuppiNoPV') else  0, help="TK PuppiE_{T}^{miss} fromPV>0 phi"),
#    NTupleVariable("tkmetPuppiNoPV_sumEt", lambda ev : ev.tkMetPuppiNoPV.sumEt if  hasattr(ev,'tkMetPuppiNoPV') else  0, help="TK PuppisumEt charged fromPV>0"),
#    NTupleVariable("tkmetPuppiPVUsedInFit_pt", lambda ev : ev.tkMetPuppiPVUsedInFit.pt() if  hasattr(ev,'tkMetPuppiPVUsedInFit') else  0, help="TK PuppiE_{T}^{miss} fromPV>0 pt"),
#    NTupleVariable("tkmetPuppiPVUsedInFit_phi", lambda ev : ev.tkMetPuppiPVUsedInFit.phi() if  hasattr(ev,'tkMetPuppiPVUsedInFit') else  0, help="TK PuppiE_{T}^{miss} fromPV>0 phi"),
#    NTupleVariable("tkmetPuppiPVUsedInFit_sumEt", lambda ev : ev.tkMetPuppiPVUsedInFit.sumEt if  hasattr(ev,'tkMetPuppiPVUsedInFit') else  0, help="TK PuppisumEt charged fromPV>0"),
#    NTupleVariable("tkmetPuppiUsedInFitTight_pt", lambda ev : ev.tkMetPuppiUsedInFitTight.pt() if  hasattr(ev,'tkMetPuppiUsedInFitTight') else  0, help="TK PuppiE_{T}^{miss} fromPV>0 pt"),
#    NTupleVariable("tkmetPuppiUsedInFitTight_phi", lambda ev : ev.tkMetPuppiUsedInFitTight.phi() if  hasattr(ev,'tkMetPuppiUsedInFitTight') else  0, help="TK PuppiE_{T}^{miss} fromPV>0 phi"),
#    NTupleVariable("tkmetPuppiUsedInFitLoose_pt", lambda ev : ev.tkMetPuppiUsedInFitLoose.pt() if  hasattr(ev,'tkMetPuppiUsedInFitLoose') else  0, help="TK PuppiE_{T}^{miss} fromPV>0 pt"),
#    NTupleVariable("tkmetPuppiUsedInFitLoose_phi", lambda ev : ev.tkMetPuppiUsedInFitLoose.phi() if  hasattr(ev,'tkMetPuppiUsedInFitLoose') else  0, help="TK PuppiE_{T}^{miss} fromPV>0 phi"),
#    NTupleVariable("tkmetPuppiCompatibilityDz_pt", lambda ev : ev.tkMetPuppiCompatibilityDz.pt() if  hasattr(ev,'tkMetPuppiCompatibilityDz') else  0, help="TK PuppiE_{T}^{miss} fromPV>0 pt"),
#    NTupleVariable("tkmetPuppiCompatibilityDz_phi", lambda ev : ev.tkMetPuppiCompatibilityDz.phi() if  hasattr(ev,'tkMetPuppiCompatibilityDz') else  0, help="TK PuppiE_{T}^{miss} fromPV>0 phi"),
#    NTupleVariable("tkmetPuppiCompatibilityBTag_pt", lambda ev : ev.tkMetPuppiCompatibilityBTag.pt() if  hasattr(ev,'tkMetPuppiCompatibilityBTag') else  0, help="TK PuppiE_{T}^{miss} fromPV>0 pt"),
#    NTupleVariable("tkmetPuppiCompatibilityBTag_phi", lambda ev : ev.tkMetPuppiCompatibilityBTag.phi() if  hasattr(ev,'tkMetPuppiCompatibilityBTag') else  0, help="TK Puppi E_{T}^{miss} fromPV>0 phi"),
#    NTupleVariable("tkmetPuppiNotReconstructedPrimary_pt", lambda ev : ev.tkMetPuppiNotReconstructedPrimary.pt() if  hasattr(ev,'tkMetPuppiNotReconstructedPrimary') else  0, help="TK Puppi E_{T}^{miss} w/o PV"),
#    NTupleVariable("tkmetPuppiNotReconstructedPrimary_phi", lambda ev : ev.tkMetPuppiNotReconstructedPrimary.phi() if  hasattr(ev,'tkMetPuppiNotReconstructedPrimary') else  0, help="TK Puppi E_{T}^{miss} w/o PV"),
#    NTupleVariable("tkmetPuppiOtherDeltaZ_pt", lambda ev : ev.tkMetPuppiOtherDeltaZ.pt() if  hasattr(ev,'tkMetPuppiOtherDeltaZ') else  0, help="TK Puppi E_{T}^{miss} fromPV>0 pt"),
#    NTupleVariable("tkmetPuppiOtherDeltaZ_phi", lambda ev : ev.tkMetPuppiOtherDeltaZ.phi() if  hasattr(ev,'tkMetPuppiOtherDeltaZ') else  0, help="TK Puppi E_{T}^{miss} fromPV>0 phi"),

    NTupleVariable("puppiMetCh_pt", lambda ev : ev.puppiMetCh.pt(), help="TK E_{T}^{miss} Puppi Charged pt"),
    NTupleVariable("puppiMetCh_phi", lambda ev : ev.puppiMetCh.phi(), help="TK E_{T}^{miss} Puppi Charged phi"),
    NTupleVariable("puppiMetCh_sumEt", lambda ev : ev.puppiMetCh.sumEt, help="TK E_{T}^{miss} Puppi Charged sumEt"),

    NTupleVariable("puppiMetPh_pt", lambda ev : ev.puppiMetPh.pt(), help="TK E_{T}^{miss} Puppi PH pt"),
    NTupleVariable("puppiMetPh_phi", lambda ev : ev.puppiMetPh.phi(), help="TK E_{T}^{miss} Puppi PH phi"),
    NTupleVariable("puppiMetPh_sumEt", lambda ev : ev.puppiMetPh.sumEt, help="TK E_{T}^{miss} Puppi PH sumEt"),

    NTupleVariable("puppiMetNh_pt", lambda ev : ev.puppiMetNh.pt(), help="TK E_{T}^{miss} Puppi NH pt"),
    NTupleVariable("puppiMetNh_phi", lambda ev : ev.puppiMetNh.phi(), help="TK E_{T}^{miss} Puppi NH phi"),
    NTupleVariable("puppiMetNh_sumEt", lambda ev : ev.puppiMetNh.sumEt, help="TK E_{T}^{miss} Puppi NH sumEt"),

    NTupleVariable("puppiMetHF_pt", lambda ev : ev.puppiMetHF.pt(), help="TK E_{T}^{miss} Puppi HF pt"),
    NTupleVariable("puppiMetHF_phi", lambda ev : ev.puppiMetHF.phi(), help="TK E_{T}^{miss} Puppi HF phi"),
    NTupleVariable("puppiMetHF_sumEt", lambda ev : ev.puppiMetHF.sumEt, help="TK E_{T}^{miss} Puppi HF sumEt"),

    ]

met_globalObjects = {
    "met" : NTupleObject("met", metType, help="PF E_{T}^{miss}, after type 1 corrections"),
#    "met_jecUp" : NTupleObject("met_jecUp", metType, help="PF E_{T}^{miss}, after type 1 corrections with JEC up variation"),
#    "met_jecDown" : NTupleObject("met_jecDown", metType, help="PF E_{T}^{miss}, after type 1 corrections with JEC down variation"),
#    "metNoHF" : NTupleObject("metNoHF", metType, help="PF E_{T}^{miss}, after type 1 corrections (NoHF)"),
    "metPuppi" : NTupleObject("metPuppi", metType, help="PF E_{T}^{miss}, after type 1 corrections (Puppi)"),
#    "metPuppi_jecUp" : NTupleObject("metPuppi_jecUp", metType, help="PF E_{T}^{miss}, after type 1 corrections with JEC up variation (Puppi)"),
#    "metPuppi_jecDown" : NTupleObject("metPuppi_jecDown", metType, help="PF E_{T}^{miss}, after type 1 corrections with JEC down variation (Puppi)"),
#    "metraw" : NTupleObject("metraw", metType, help="PF E_{T}^{miss}"),
#    "metType1chs" : NTupleObject("metType1chs", metType, help="PF E_{T}^{miss}, after type 1 CHS jets"),
    #"tkMet" : NTupleObject("tkmet", metType, help="TK PF E_{T}^{miss}"),
    #"metNoPU" : NTupleObject("metNoPU", fourVectorType, help="PF noPU E_{T}^{miss}"),
    }

met_collections = {
#    "genleps"         : NTupleCollection("genLep",     genParticleWithLinksType, 10, help="Generated leptons (e/mu) from W/Z decays"),
#    "gentauleps"      : NTupleCollection("genLepFromTau", genParticleWithLinksType, 10, help="Generated leptons (e/mu) from decays of taus from W/Z/h decays"),
#    "gentaus"         : NTupleCollection("genTau",     genParticleWithLinksType, 10, help="Generated leptons (tau) from W/Z decays"),
#    "generatorSummary" : NTupleCollection("GenPart", genParticleWithLinksType, 100 , help="Hard scattering particles, with ancestry and links"),
    "selectedLeptons" : NTupleCollection("lep", leptonType, 50, help="Leptons after the preselection", filter=lambda l : l.pt()>10 ),
#    "selectedPhotons"    : NTupleCollection("gamma", photonType, 50, help="photons with pt>20 and loose cut based ID"),
#    "cleanJetsAll"       : NTupleCollection("jet", jetType, 100, help="all jets (w/ x-cleaning, w/ ID applied w/o PUID applied pt>20 |eta|<5.2) , sorted by pt", filter=lambda l : l.pt()>100  ),
    }
