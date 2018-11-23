from PhysicsTools.HeppyCore.utils.deltar import deltaR, deltaPhi

from CMGTools.H2TauTau.proto.analyzers.tauIDs import tauIDs, tauIDs_extra

class Variable():
    def __init__(self, name, function=None, type=float, storageType="default"):
        self.name = name
        self.function = function
        if function is None:
            # Note: works for attributes, not member functions
            self.function = lambda x : getattr(x, self.name, -999.) 
        self.type = type
        self.storageType = storageType

def default():
    return -999.

# event variables
event_vars = [
    Variable('run', type=int),
    Variable('lumi', type=int),
    Variable('event', lambda ev : ev.eventId, type=int, storageType="l"),
    Variable('bx', lambda ev : (ev.input.eventAuxiliary().bunchCrossing() * ev.input.eventAuxiliary().isRealData()), type=int),
    Variable('orbit_number', lambda ev : (ev.input.eventAuxiliary().orbitNumber() * ev.input.eventAuxiliary().isRealData()), type=int),
    Variable('is_data', lambda ev: ev.input.eventAuxiliary().isRealData(), type=int),
    Variable('nPU', lambda ev : -99 if getattr(ev, 'nPU', -1) is None else getattr(ev, 'nPU', -1)),
    Variable('pass_leptons', lambda ev : ev.isSignal, type=int),
    Variable('veto_dilepton', lambda ev : not ev.leptonAccept, type=int),
    Variable('veto_thirdlepton', lambda ev : not ev.thirdLeptonVeto, type=int),
    Variable('veto_otherlepton', lambda ev : not ev.otherLeptonVeto, type=int),
    Variable('n_jets', lambda ev : len(ev.cleanJets30), type=int),
    Variable('n_jets_puid', lambda ev : sum(1 for j in ev.cleanJets30 if j.puJetId()), type=int),
    Variable('n_jets_20', lambda ev : len(ev.cleanJets), type=int),
    Variable('n_jets_20_puid', lambda ev : sum(1 for j in ev.cleanJets if j.puJetId()), type=int),
    Variable('n_bjets', lambda ev : len(ev.cleanBJets), type=int),
    Variable('n_bjets_loose', lambda ev : len(ev.cleanBJetsLoose), type=int),
    Variable('n_vertices', lambda ev : len(ev.vertices), type=int),
    Variable('rho', lambda ev : ev.rho),
    Variable('weight', lambda ev : ev.eventWeight),
    Variable('weight_vertex', lambda ev : ev.puWeight),
    # # Add back for embedded samples once needed
    # Variable('weight_embed', lambda ev : getattr(ev, 'embedWeight', 1.)),
    Variable('weight_njet', lambda ev : ev.NJetWeight),
    Variable('weight_dy', lambda ev : getattr(ev, 'dy_weight', 1.)),
    # # Add back the following only for ggH samples once needed
    # Variable('weight_hqt', lambda ev : getattr(ev, 'higgsPtWeight', 1.)),
    # Variable('weight_hqt_up', lambda ev : getattr(ev, 'higgsPtWeightUp', 1.)),
    # Variable('weight_hqt_down', lambda ev : getattr(ev, 'higgsPtWeightDown', 1.)),
    # Variable('weight_njet', lambda ev : ev.NJetWeight),
    # Variable('delta_phi_dil_jet1', lambda ev : deltaPhi(ev.diLepton.p4().phi(), ev.cleanJets[0].phi()) if len(ev.cleanJets)>0 else -999.),
    # Variable('delta_phi_dil_met', lambda ev : deltaPhi(ev.diLepton.p4().phi(), ev.diLepton.met().phi())),
    # Variable('delta_phi_dil_jet2', lambda ev : deltaPhi(ev.diLepton.p4().phi(), ev.cleanJets[1].phi()) if len(ev.cleanJets)>1 else -999.),
    # Variable('delta_eta_dil_jet1', lambda ev : abs(ev.diLepton.p4().eta() - ev.cleanJets[0].eta()) if len(ev.cleanJets)>0 else -999.),
    # Variable('delta_eta_dil_jet2', lambda ev : abs(ev.diLepton.p4().eta() - ev.cleanJets[1].eta()) if len(ev.cleanJets)>1 else -999.),
    Variable('Flag_HBHENoiseFilter', type=int),
    Variable('Flag_HBHENoiseIsoFilter', type=int),
    Variable('Flag_EcalDeadCellTriggerPrimitiveFilter', type=int),
    Variable('Flag_goodVertices', type=int),
    Variable('Flag_eeBadScFilter', type=int),
    Variable('Flag_globalTightHalo2016Filter', type=int),
    Variable('passBadMuonFilter', type=int),
    Variable('passBadChargedHadronFilter', type=int),
    Variable('badMuonMoriond2017', type=int),
    Variable('badCloneMuonMoriond2017', type=int)
]

# di-tau object variables
ditau_vars = [
    Variable('mvis', lambda dil : dil.mass()),
    Variable('dil_pt', lambda dil : dil.p4().pt()),
    Variable('dil_eta', lambda dil : dil.p4().eta()),
    Variable('dil_phi', lambda dil : dil.p4().phi()),
    Variable('mt_total', lambda dil : dil.mtTotal()),
    # Variable('sum_lepton_mt', lambda dil : dil.mtSumLeptons()),
    # Variable('sqsum_lepton_mt', lambda dil : dil.mtSqSumLeptons()),
    Variable('pzeta_met', lambda dil : dil.pZetaMET()),
    Variable('pzeta_vis', lambda dil : dil.pZetaVis()),
    Variable('pzeta_disc', lambda dil : dil.pZetaDisc()),
    Variable('mt', lambda dil : dil.mTLeg1()),
    Variable('mt_leg2', lambda dil : dil.mTLeg2()),
    # Variable('mt_leg1', lambda dil : dil.mTLeg1()), # redundant
    Variable('met_cov00', lambda dil : dil.mvaMetSig(0, 0) if dil.mvaMetSig else 0.),
    # Variable('met_cov01', lambda dil : dil.mvaMetSig(0, 1) if dil.mvaMetSig else 0.), # redundant
    Variable('met_cov10', lambda dil : dil.mvaMetSig(1, 0) if dil.mvaMetSig else 0.),
    Variable('met_cov11', lambda dil : dil.mvaMetSig(1, 1) if dil.mvaMetSig else 0.),
    Variable('met_phi', lambda dil : dil.met().phi()),
    # Variable('met_px', lambda dil : dil.met().px()),
    # Variable('met_py', lambda dil : dil.met().py()),
    Variable('met_pt', lambda dil : dil.met().pt()),
    Variable('pthiggs', lambda dil : (dil.leg1().p4() + dil.leg2().p4() + dil.met().p4()).pt()),
    # Variable('delta_phi_l1_l2', lambda dil : deltaPhi(dil.leg1().phi(), dil.leg2().phi())),
    # Variable('delta_eta_l1_l2', lambda dil : abs(dil.leg1().eta() - dil.leg2().eta())),
    Variable('delta_r_l1_l2', lambda dil : deltaR(dil.leg1().eta(), dil.leg1().phi(), dil.leg2().eta(), dil.leg2().phi())),
    # Variable('delta_phi_l1_met', lambda dil : deltaPhi(dil.leg1().phi(), dil.met().phi())),
    # Variable('delta_phi_l2_met', lambda dil : deltaPhi(dil.leg2().phi(), dil.met().phi())),
]

svfit_vars = [
    Variable('svfit_mass', lambda dil : dil.svfitMass()),
    Variable('svfit_transverse_mass', lambda dil : dil.svfitTransverseMass()),
    Variable('svfit_mass_error', lambda dil : dil.svfitMassError()),
    Variable('svfit_pt', lambda dil : dil.svfitPt()),
    # Variable('svfit_pt_error', lambda dil : dil.svfitPtError()),
    # Variable('svfit_eta', lambda dil : dil.svfitEta()),
    # Variable('svfit_phi', lambda dil : dil.svfitPhi()),
    # Variable('svfit_met_pt', lambda dil : dil.svfitMET().Rho() if hasattr(dil, 'svfitMET') else default()),
    # Variable('svfit_met_e', lambda dil : dil.svfitMET().mag2() if hasattr(dil, 'svfitMET') else default()),
    # Variable('svfit_met_phi', lambda dil : dil.svfitMET().phi() if hasattr(dil, 'svfitMET') else default()),
    # Variable('svfit_met_eta', lambda dil : dil.svfitMET().eta() if hasattr(dil, 'svfitMET') else default()),
]

# generic particle
particle_vars = [
    Variable('pt', lambda p: p.pt()),
    Variable('eta', lambda p: p.eta()),
    Variable('phi', lambda p: p.phi()),
    Variable('charge', lambda p: p.charge() if hasattr(p, 'charge') else 0), # charge may be non-integer for gen particles
    Variable('mass', lambda p: p.mass()),
]

# generic lepton
lepton_vars = [
    Variable('dxy', lambda lep : lep.dxy()),
    Variable('dxy_error', lambda lep : lep.edxy() if hasattr(lep, 'edxy') else lep.dxy_error()),
    Variable('dz', lambda lep : lep.leadChargedHadrCand().dz() if hasattr(lep, 'leadChargedHadrCand') else lep.dz()),
    Variable('dz_error', lambda lep : lep.edz() if hasattr(lep, 'edz') else -1.),
    Variable('weight'),
    Variable('weight_trigger', lambda lep : getattr(lep, 'weight_trigger', 1.)),
    # Variable('eff_trigger_data', lambda lep : getattr(lep, 'eff_data_trigger', -999.)),
    # Variable('eff_trigger_mc', lambda lep : getattr(lep, 'eff_mc_trigger', -999.)),
    Variable('weight_idiso', lambda lep : getattr(lep, 'weight_idiso', 1.)),
    # Variable('eff_idiso_data', lambda lep : getattr(lep, 'eff_data_idiso', -999.)),
    # Variable('eff_idiso_mc', lambda lep : getattr(lep, 'eff_mc_idiso', -999.)),
    Variable('gen_match', type=int)
]

# electron
electron_vars = [
    # Variable('eid_nontrigmva_loose', lambda ele : ele.mvaIDRun2("NonTrigPhys14", "Loose")),
    Variable('eid_nontrigmva_loose', lambda ele : ele.mvaRun2('NonTrigSpring15MiniAOD')),
    Variable('eid_nontrigmva_tight', lambda ele : ele.mvaIDRun2("NonTrigSpring15MiniAOD", "POG80")),
    Variable('eid_veto', lambda ele : ele.cutBasedId('POG_SPRING15_25ns_v1_Veto')),
    Variable('eid_loose', lambda ele : ele.cutBasedId('POG_SPRING15_25ns_v1_Loose')),
    Variable('eid_medium', lambda ele : ele.cutBasedId('POG_SPRING15_25ns_v1_Medium')),
    Variable('eid_tight', lambda ele : ele.cutBasedId('POG_SPRING15_25ns_v1_Tight')),
    Variable('nhits_missing', lambda ele : ele.physObj.gsfTrack().hitPattern().numberOfHits(1), int),
    Variable('pass_conv_veto', lambda ele : ele.passConversionVeto()),
    Variable('reliso05', lambda lep : lep.relIso(0.3, dbeta_factor=0.5, all_charged=0)),
    Variable('reliso05_04', lambda lep : lep.relIso(0.4, dbeta_factor=0.5, all_charged=0)),
    Variable('reliso05_04', lambda lep : lep.relIso(0.4, dbeta_factor=0.5, all_charged=0)),
    Variable('weight_tracking', lambda lep : getattr(lep, 'weight_tracking', 1.)),
]

# muon
muon_vars = [
    Variable('reliso05', lambda lep : lep.relIso(0.4, dbeta_factor=0.5, all_charged=0)),
    Variable('reliso05_03', lambda lep : lep.relIso(0.3, dbeta_factor=0.5, all_charged=0)),
    Variable('muonid_loose', lambda muon : muon.muonID('POG_ID_Loose')),
    Variable('muonid_medium', lambda muon : muon.muonID('POG_ID_Medium_ICHEP')),
    Variable('muonid_tight', lambda muon : muon.muonID('POG_ID_Tight')),
    Variable('muonid_tightnovtx', lambda muon : muon.muonID('POG_ID_TightNoVtx')),
    Variable('muonid_highpt', lambda muon : muon.muonID('POG_ID_HighPt')),
    Variable('dxy_innertrack', lambda muon : muon.innerTrack().dxy(muon.associatedVertex.position())),
    Variable('dz_innertrack', lambda muon : muon.innerTrack().dz(muon.associatedVertex.position())),
    Variable('weight_tracking', lambda muon : getattr(muon, 'weight_tracking', 1.)),
]

# tau
tau_vars = [
    Variable('decayMode', lambda tau : tau.decayMode(), type=int),
    Variable('zImpact', lambda tau : tau.zImpact()),
    Variable('dz_selfvertex', lambda tau : tau.vertex().z() - tau.associatedVertex.position().z()),
    Variable('ptScale', lambda tau : getattr(tau, 'ptScale', -999.)),
]
for tau_id in tauIDs:
    if type(tau_id) is str:
        # Need to use eval since functions are otherwise bound to local
        # variables
        tau_vars.append(Variable(tau_id, eval('lambda tau : tau.tauID("{id}")'.format(id=tau_id))))
    else:
        sum_id_str = ' + '.join('tau.tauID("{id}")'.format(id=tau_id[0].format(wp=wp)) for wp in tau_id[1])
        tau_vars.append(Variable(tau_id[0].format(wp=''), 
            eval('lambda tau : ' + sum_id_str), int))

tau_vars_extra = []
for tau_id in tauIDs_extra:
    if type(tau_id) is str:
        # Need to use eval since functions are otherwise bound to local
        # variables
        tau_vars_extra.append(Variable(tau_id, eval('lambda tau : tau.tauID("{id}")'.format(id=tau_id))))
    else:
        sum_id_str = ' + '.join('tau.tauID("{id}")'.format(id=tau_id[0].format(wp=wp)) for wp in tau_id[1])
        tau_vars_extra.append(Variable(tau_id[0].format(wp=''), 
            eval('lambda tau : ' + sum_id_str), int))


# jet
jet_vars = [
    Variable('mva_pu', lambda jet : jet.puMva('pileupJetId:fullDiscriminant')),
    # Variable('id_loose', lambda jet : jet.looseJetId()),
    Variable('id_pu', lambda jet : jet.puJetId() + jet.puJetId(wp='medium') + jet.puJetId(wp='tight')),
    # Variable('area', lambda jet : jet.jetArea()),
    Variable('flavour_parton', lambda jet : jet.partonFlavour()),
    Variable('csv', lambda jet : jet.btagMVA),
    Variable('genjet_pt', lambda jet : jet.matchedGenJet.pt() if hasattr(jet, 'matchedGenJet') and jet.matchedGenJet else -999.),
]

# extended jet vars
jet_vars_extra = [
    Variable('nConstituents', lambda jet : getattr(jet, 'nConstituents', default)(), type=int),
    Variable('rawFactor', lambda jet : getattr(jet, 'rawFactor', default)()),
    Variable('chargedHadronEnergy', lambda jet : getattr(jet, 'chargedHadronEnergy', default)()),
    Variable('neutralHadronEnergy', lambda jet : getattr(jet, 'neutralHadronEnergy', default)()),
    Variable('neutralEmEnergy', lambda jet : getattr(jet, 'neutralEmEnergy', default)()),
    Variable('muonEnergy', lambda jet : getattr(jet, 'muonEnergy', default)()),
    Variable('chargedEmEnergy', lambda jet : getattr(jet, 'chargedEmEnergy', default)()),
    Variable('chargedHadronMultiplicity', lambda jet : getattr(jet, 'chargedHadronMultiplicity', default)()),
    Variable('chargedMultiplicity', lambda jet : getattr(jet, 'chargedMultiplicity', default)(), type=int),
    Variable('neutralMultiplicity', lambda jet : getattr(jet, 'neutralMultiplicity', default)(), type=int),
]


# gen info
geninfo_vars = [
    Variable('geninfo_mcweight', lambda ev : getattr(ev, 'mcweight', 1.)),
    Variable('geninfo_nup', lambda ev : getattr(ev, 'NUP', -1), type=int),
    Variable('geninfo_htgen', lambda ev : getattr(ev, 'genPartonHT', -1)),
    Variable('geninfo_invmass', lambda ev : getattr(ev, 'geninvmass', -1)),
    Variable('weight_gen'),
    Variable('genmet_pt'),
    # Variable('genmet_eta'),
    # Variable('genmet_e'),
    # Variable('genmet_px'),
    # Variable('genmet_py'),
    Variable('genmet_phi'),
]

vbf_vars = [
    Variable('mjj'),
    Variable('deta'),
    Variable('n_central20', lambda vbf : len(vbf.centralJets), int),
    Variable('n_central', lambda vbf : sum([1 for j in vbf.centralJets if j.pt() > 30.]), int),
    Variable('jdphi', lambda vbf : vbf.dphi),
    Variable('dijetpt'),
    Variable('dijetphi'),
    Variable('dphidijethiggs'),
    Variable('mindetajetvis', lambda vbf : vbf.visjeteta),
]
