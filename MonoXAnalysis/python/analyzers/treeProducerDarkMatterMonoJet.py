from CMGTools.MonoXAnalysis.analyzers.treeProducerDarkMatterCore import *
from CMGTools.TTHAnalysis.analyzers.ntupleTypes import *

dmMonoJet_globalVariables = dmCore_globalVariables + [
    ##--------------------------------------------------
    ## Generator information
    ##--------------------------------------------------
    ##    NTupleVariable("genQScale", lambda ev : ev.genQScale, help="Generator level binning quantity, QScale"),
    
    ##--------------------------------------------------
    ## energy sums
    ##--------------------------------------------------
    ##-------- custom jets ------------------------------------------
    NTupleVariable("htJet25", lambda ev : ev.htJet25, help="H_{T} computed from leptons and jets (with |eta|<2.4, pt > 25 GeV)"),
    NTupleVariable("mhtJet25", lambda ev : ev.mhtJet25, help="H_{T}^{miss} computed from leptons and jets (with |eta|<2.4, pt > 25 GeV)"),
    NTupleVariable("htJet40j", lambda ev : ev.htJet40j, help="H_{T} computed from only jets (with |eta|<2.4, pt > 40 GeV)"),
    NTupleVariable("htJet40ja", lambda ev : ev.htJet40ja, help="H_{T} computed from only jets (with |eta|<4.7, pt > 40 GeV)"),
    NTupleVariable("htJet40", lambda ev : ev.htJet40, help="H_{T} computed from leptons and jets (with |eta|<2.4, pt > 40 GeV)"),
    NTupleVariable("htJet40a", lambda ev : ev.htJet40a, help="H_{T} computed from leptons and jets (with |eta|<4.7, pt > 40 GeV)"),
    NTupleVariable("mhtJet40", lambda ev : ev.mhtJet40, help="H_{T}^{miss} computed from leptons and jets (with |eta|<2.4, pt > 40 GeV)"),
    NTupleVariable("mhtJet40a", lambda ev : ev.mhtJet40a, help="H_{T}^{miss} computed from leptons and jets (with |eta|<4.7, pt > 40 GeV)"),
    ##--------------------------------------------------
    # MT2
    ##--------------------------------------------------
    # NTupleVariable("mt2_had", lambda ev: ev.mt2_had, float, help="mt2(j1,j2,met) with jets "),
    # NTupleVariable("mt2_bb", lambda ev: ev.mt2bb, float, help="mt2(b1,b2,met) with jets "),
    # NTupleVariable("mt2_gen", lambda ev: ev.mt2_gen, float, help="mt2(j1,j2,met) with jets at genInfo"),
    # NTupleVariable("mt2", lambda ev: ev.mt2, float, help="mt2(j1,j2,met) with jets and leptons"),
    ##--------------------------------------------------
    # RAZOR
    ##--------------------------------------------------
    # NTupleVariable("mr_had", lambda ev: ev.mr_had, float, help="mr(j1,j2,met) with jets "),
    # NTupleVariable("mr_bb", lambda ev: ev.mr_bb, float, help="mr(b1,b2,met) with jets "),
    # NTupleVariable("mr_lept", lambda ev: ev.mr_lept, float, help="mr(j1,j2,met) with leptons"),
    # NTupleVariable("mr_gen", lambda ev: ev.mr_gen, float, help="mr(j1,j2,met) with jets at genInfo"),
    # NTupleVariable("mr", lambda ev: ev.mr, float, help="mr(j1,j2,met) with jets and leptons"),
    # NTupleVariable("mtr_had", lambda ev: ev.mtr_had, float, help="mtr(j1,j2,met) with jets "),
    # NTupleVariable("mtr_bb", lambda ev: ev.mtr_bb, float, help="mtr(b1,b2,met) with jets "),
    # NTupleVariable("mtr_lept", lambda ev: ev.mtr_lept, float, help="mtr(j1,j2,met) with leptons"),
    # NTupleVariable("mtr_gen", lambda ev: ev.mtr_gen, float, help="mtr(j1,j2,met) with jets at genInfo"),
    # NTupleVariable("mtr", lambda ev: ev.mtr, float, help="mtr(j1,j2,met) with jets and leptons"),
    # NTupleVariable("r_had", lambda ev: ev.r_had, float, help="r(j1,j2,met) with jets "),
    # NTupleVariable("r_bb", lambda ev: ev.r_bb, float, help="r(b1,b2,met) with jets "),
    # NTupleVariable("r_lept", lambda ev: ev.r_lept, float, help="r(j1,j2,met) with leptons"),
    # NTupleVariable("r_gen", lambda ev: ev.r_gen, float, help="r(j1,j2,met) with jets at genInfo"),
    # NTupleVariable("r", lambda ev: ev.r, float, help="r(j1,j2,met) with jets and leptons"),
    ##-------------------------------------------------- 
    ## MonoJet specific ones
    ##-------------------------------------------------- 
    NTupleVariable("apcjetmetmin",  lambda ev: ev.apcjetmetmin, help="apcjetmetmin computed using jets with pt > 50, |eta|<3"),
    ##--------------------------------------------------            
    ## dilepton masses
    ##--------------------------------------------------            
    NTupleVariable("mZ1", lambda ev : ev.bestZ1[0], help="Best m(ll) SF/OS"),
    #NTupleVariable("mZ1SFSS", lambda ev : ev.bestZ1sfss[0], help="Best m(ll) SF/SS"),
    #NTupleVariable("minMllSFOS", lambda ev: ev.minMllSFOS, help="min m(ll), SF/OS"),
    #NTupleVariable("maxMllSFOS", lambda ev: ev.maxMllSFOS, help="max m(ll), SF/OS"),
    #NTupleVariable("minMllAFOS", lambda ev: ev.minMllAFOS, help="min m(ll), AF/OS"),
    #NTupleVariable("maxMllAFOS", lambda ev: ev.maxMllAFOS, help="max m(ll), AF/OS"),
    #NTupleVariable("minMllAFSS", lambda ev: ev.minMllAFSS, help="min m(ll), AF/SS"),
    #NTupleVariable("maxMllAFSS", lambda ev: ev.maxMllAFSS, help="max m(ll), AF/SS"),
    #NTupleVariable("minMllAFAS", lambda ev: ev.minMllAFAS, help="min m(ll), AF/AS"),
    #NTupleVariable("maxMllAFAS", lambda ev: ev.maxMllAFAS, help="max m(ll), AF/AS"),
    #NTupleVariable("m2l", lambda ev: ev.m2l, help="m(ll)"),
    
    ##--------------------------------------------------
    # Physics object multplicities
    ##--------------------------------------------------
    #NTupleVariable("nBJet25",    lambda ev: sum([j.btagWP("CSVv2IVFM") for j in ev.cleanJets if j.pt() > 25]), int, help="Number of jets with pt > 40 passing CSV medium"),
    #NTupleVariable("nFatJet100", lambda ev: sum([j.pt() > 100 for j in ev.fatJets]), int, help="Number of fat jets with pt > 100"),
    #NTupleVariable("nMuons10",   lambda ev: sum([l.pt() > 10 and abs(l.pdgId()) == 13 for l in ev.selectedLeptons]), int, help="Number of muons with pt > 10"),
    #NTupleVariable("nElectrons10", lambda ev: sum([l.pt() > 10 and abs(l.pdgId()) == 11 for l in ev.selectedLeptons]), int, help="Number of electrons with pt > 10"),
    #NTupleVariable("nTaus20",    lambda ev: sum([l.pt() > 20 for l in ev.selectedTaus]), int, help="Number of taus with pt > 20"),
    #NTupleVariable("nGammas20",  lambda ev: sum([l.pt() > 20 for l in ev.selectedPhotons]), int, help="Number of photons with pt > 20"),

    
    ##--------------------------------------------------
    # Generator variables
    ##--------------------------------------------------
    # NTupleVariable("LHEorigWeight",    lambda ev: ev.LHE_originalWeight, float, help="Central LHE weight of the sample"),


]


dmMonoJet_globalObjects = dmCore_globalObjects.copy()
dmMonoJet_globalObjects.update({
        # put more here
})

leptonTypeMonoJet = NTupleObjectType("leptonMonoJet", baseObjectTypes = [ leptonType, leptonTypeExtra ], variables = [
        #NTupleVariable("r9",      lambda lepton : lepton.full5x5_r9() if abs(lepton.pdgId()) == 11 else -99, help="SuperCluster 5x5 r9 variable, only for electrons; -99 for muons"),
        #NTupleVariable("e5x5", lambda x: x.e5x5() if (abs(x.pdgId())==11 and hasattr(x,"e5x5")) else -999, help="Electron e5x5"),
        #NTupleVariable("sigmaIetaIeta", lambda x: x.sigmaIetaIeta() if (abs(x.pdgId())==11 and hasattr(x,"sigmaIetaIeta")) else -999, help="Electron sigmaIetaIeta"),
        #NTupleVariable("sigmaIphiIphi", lambda x: x.sigmaIphiIphi() if (abs(x.pdgId())==11 and hasattr(x,"sigmaIphiIphi")) else -999, help="Electron sigmaIphiIphi"),
        #NTupleVariable("hcalOverEcal", lambda x: x.hcalOverEcal() if (abs(x.pdgId())==11 and hasattr(x,"hcalOverEcal")) else -999, help="Electron hcalOverEcal"),
        NTupleVariable("full5x5_e5x5", lambda x: x.full5x5_e5x5() if (abs(x.pdgId())==11 and hasattr(x,"full5x5_e5x5")) else -999, help="Electron full5x5_e5x5"),
        NTupleVariable("full5x5_r9", lambda x: x.full5x5_r9() if (abs(x.pdgId())==11 and hasattr(x,"full5x5_r9")) else -999, help="Electron full5x5_r9"),
        NTupleVariable("full5x5_sigmaIetaIeta", lambda x: x.full5x5_sigmaIetaIeta() if (abs(x.pdgId())==11 and hasattr(x,"full5x5_sigmaIetaIeta")) else -999, help="Electron full5x5_sigmaIetaIeta"),
        NTupleVariable("full5x5_sigmaIphiIphi", lambda x: x.full5x5_sigmaIphiIphi() if (abs(x.pdgId())==11 and hasattr(x,"full5x5_sigmaIphiIphi")) else -999, help="Electron full5x5_sigmaIphiIphi"),
        NTupleVariable("full5x5_hcalOverEcal", lambda x: x.full5x5_hcalOverEcal() if (abs(x.pdgId())==11 and hasattr(x,"full5x5_hcalOverEcal")) else -999, help="Electron full5x5_hcalOverEcal"),
        NTupleVariable("correctedEcalEnergy", lambda x: x.correctedEcalEnergy() if (abs(x.pdgId())==11 and hasattr(x,"correctedEcalEnergy")) else -999, help="Electron correctedEcalEnergy"),
        NTupleVariable("eSuperClusterOverP", lambda x: x.eSuperClusterOverP() if (abs(x.pdgId())==11 and hasattr(x,"eSuperClusterOverP")) else -999, help="Electron eSuperClusterOverP"),
        #NTupleVariable("ecalEnergy", lambda x: x.ecalEnergy() if (abs(x.pdgId())==11 and hasattr(x,"ecalEnergy")) else -999, help="Electron ecalEnergy"),
        NTupleVariable("superCluster_rawEnergy", lambda x: x.superCluster().rawEnergy() if (abs(x.pdgId())==11 and hasattr(x,"superCluster")) else -999, help="Electron superCluster.rawEnergy"),
        NTupleVariable("superCluster_preshowerEnergy", lambda x: x.superCluster().preshowerEnergy() if (abs(x.pdgId())==11 and hasattr(x,"superCluster")) else -999, help="Electron superCluster.preshowerEnergy"),
        #NTupleVariable("superCluster_correctedEnergy", lambda x: x.superCluster().correctedEnergy() if (abs(x.pdgId())==11 and hasattr(x,"superCluster")) else -999, help="Electron superCluster.correctedEnergy"),
        #NTupleVariable("superCluster_energy", lambda x: x.superCluster().energy() if (abs(x.pdgId())==11 and hasattr(x,"superCluster")) else -999, help="Electron superCluster.energy"),
        #NTupleVariable("superCluster_clustersSize", lambda x: x.superCluster().clustersSize() if (abs(x.pdgId())==11 and hasattr(x,"superCluster")) else -999, help="Electron superCluster.clustersSize"),
        #NTupleVariable("superCluster_seed.energy", lambda x: x.superCluster().seed().energy() if (abs(x.pdgId())==11 and hasattr(x,"superCluster")) else -999, help="Electron superCluster.seed.energy"),

])

dmMonoJet_collections = dmCore_collections.copy()
dmMonoJet_collections.update({
            # put more here
            #"genleps"         : NTupleCollection("genLep",     genParticleWithLinksType, 10, help="Generated leptons (e/mu) from W/Z decays"), 
            ##------------------------------------------------                       
            "monoxSelectedTaus" : NTupleCollection("TauGood",  tauTypeSusy, 3, help="Taus after the preselection"),
            "selectedLeptons"   : NTupleCollection("LepGood",  leptonTypeMonoJet, 10, help="Leptons after the preselection"),
            "selectedPhotons"   : NTupleCollection("GammaGood", photonTypeSusy, 20, help="photons with pt>20 and loose cut based ID"),
            ##------------------------------------------------
            "cleanJets"       : NTupleCollection("Jet",     jetTypeSusyExtra, 20, help="Cental jets after full selection and cleaning, sorted by pt"),
            "cleanJetsFwd"    : NTupleCollection("JetFwd",  jetTypeSusyExtra,  5, help="Forward jets after full selection and cleaning, sorted by pt"),
            "fatJets"         : NTupleCollection("FatJet",  fatJetType,       20, help="AK8 jets, sorted by pt"),
            ##------------------------------------------------
            #"discardedJets"    : NTupleCollection("DiscJet", jetTypeSusyExtra, 10, help="Jets discarted in the jet-lepton cleaning"),
            #"discardedLeptons" : NTupleCollection("DiscLep", leptonTypeSusyExtra, 8, help="Leptons discarded in the jet-lepton cleaning"),
            ##------------------------------------------------
            "selectedIsoTrack"    : NTupleCollection("isoTrack", isoTrackType, 50, help="isoTrack, sorted by pt"),
            ##------------------------------------------------
            "LHE_weights"    : NTupleCollection("LHEweight",  weightsInfoType, 1000, mcOnly=True, help="LHE weight info"),
            ##------------------------------------------------
            #"genBHadrons"  : NTupleCollection("GenBHad", heavyFlavourHadronType, 20, mcOnly=True, help="Gen-level B hadrons"),
            #"genDHadrons"  : NTupleCollection("GenDHad", heavyFlavourHadronType, 20, mcOnly=True, help="Gen-level D hadrons"),
})
        
jetTypeSusyExtra.addVariables([
        NTupleVariable("puMva", lambda x: x.puMva(), float, help="Value of the pu MVA discriminator")
])


# no more present in MINIAOD V2 in 8.0.X
fatJetType.removeVariable("trimmedMass")
fatJetType.removeVariable("filteredMass")
# substitute this with the JEC corrected one
fatJetType.removeVariable("prunedMass")
fatJetType.addVariables([
        NTupleVariable("puMva", lambda x: x.puMva(), float, help="Value of the pu MVA discriminator"),
        NTupleVariable("prunedMass", lambda x: x.userFloat("ak8PFJetsCHSPrunedMass") * (x.corr if hasattr(x,'corr') else 1.0), float, help="pruned mass"),
])

