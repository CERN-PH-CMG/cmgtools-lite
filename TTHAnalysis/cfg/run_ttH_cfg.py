##########################################################
##       CONFIGURATION FOR TTH MULTILEPTON TREES       ##
##########################################################
import PhysicsTools.HeppyCore.framework.config as cfg
import re


#-------- LOAD ALL ANALYZERS -----------

from CMGTools.TTHAnalysis.analyzers.susyCore_modules_cff import *
from PhysicsTools.HeppyCore.framework.heppy_loop import getHeppyOption

#-------- SET OPTIONS AND REDEFINE CONFIGURATIONS -----------

runData = getHeppyOption("runData",False)
runDataQCD = getHeppyOption("runDataQCD",False)
runQCDBM = getHeppyOption("runQCDBM",False)
runFRMC = getHeppyOption("runFRMC",False)
scaleProdToLumi = float(getHeppyOption("scaleProdToLumi",-1)) # produce rough equivalent of X /pb for MC datasets
removeJetReCalibration = getHeppyOption("removeJetReCalibration",False)
removeJecUncertainty = getHeppyOption("removeJecUncertainty",False)
doMETpreprocessor = getHeppyOption("doMETpreprocessor",False)
skipT1METCorr = getHeppyOption("skipT1METCorr",False)
forcedSplitFactor = getHeppyOption("splitFactor",-1)
forcedFineSplitFactor = getHeppyOption("fineSplitFactor",-1)
isTest = getHeppyOption("test",None) != None and not re.match("^\d+$",getHeppyOption("test"))
selectedEvents=getHeppyOption("selectEvents","")

runFRMC = True
#runData = True; runDataQCD = True
#runData = True
sample = "main"
#if runDataQCD or runFRMC: sample="qcd1l"
#sample = "z3l"

# Lepton Skimming
ttHLepSkim.minLeptons = 2
ttHLepSkim.maxLeptons = 999
#ttHLepSkim.idCut  = ""
#ttHLepSkim.ptCuts = []

# Run miniIso
lepAna.doMiniIsolation = True
lepAna.packedCandidates = 'packedPFCandidates'
lepAna.miniIsolationPUCorr = 'rhoArea'
lepAna.miniIsolationVetoLeptons = None # use 'inclusive' to veto inclusive leptons and their footprint in all isolation cones
lepAna.doIsolationScan = False

# Lepton Preselection
lepAna.loose_electron_id = "MVA_ID_NonTrig_Spring16_VLooseIdEmu"
isolation = "miniIso"

jetAna.lepSelCut = lambda lep : False # no cleaning of jets with leptons
jetAnaScaleDown.lepSelCut = lambda lep : False # no cleaning of jets with leptons
jetAnaScaleUp.lepSelCut = lambda lep : False # no cleaning of jets with leptons
jetAna.copyJetsByValue = True # do not remove this
metAna.copyMETsByValue = True # do not remove this
jetAna.doQG = True
if not removeJecUncertainty:
    jetAna.addJECShifts = True
    jetAna.jetPtOrUpOrDnSelection = True
    jetAnaScaleDown.copyJetsByValue = True # do not remove this
    jetAnaScaleDown.doQG = False
    metAnaScaleDown.copyMETsByValue = True # do not remove this
    jetAnaScaleUp.copyJetsByValue = True # do not remove this
    jetAnaScaleUp.doQG = False
    metAnaScaleUp.copyMETsByValue = True # do not remove this
    susyCoreSequence.insert(susyCoreSequence.index(jetAna)+1, jetAnaScaleDown)
    susyCoreSequence.insert(susyCoreSequence.index(jetAna)+1, jetAnaScaleUp)
    susyCoreSequence.insert(susyCoreSequence.index(metAna)+1, metAnaScaleDown)
    susyCoreSequence.insert(susyCoreSequence.index(metAna)+1, metAnaScaleUp)


if isolation == "miniIso": 
    lepAna.loose_muon_isoCut     = lambda muon : muon.miniRelIso < 0.4 and muon.sip3D() < 8
    lepAna.loose_electron_isoCut = lambda elec : elec.miniRelIso < 0.4 and elec.sip3D() < 8
elif isolation == None:
    lepAna.loose_muon_isoCut     = lambda muon : True
    lepAna.loose_electron_isoCut = lambda elec : True
elif isolation == "absIso04":
    lepAna.loose_muon_isoCut     = lambda muon : muon.RelIsoMIV04*muon.pt() < 10 and muon.sip3D() < 8
    lepAna.loose_electron_isoCut = lambda elec : elec.RelIsoMIV04*elec.pt() < 10 and elec.sip3D() < 8
else:
    # nothing to do, will use normal relIso03
    pass

# Switch off slow photon MC matching
photonAna.do_mc_match = False

# Loose Tau configuration
tauAna.loose_ptMin = 20
tauAna.loose_etaMax = 2.3
tauAna.loose_decayModeID = "decayModeFindingNewDMs"
tauAna.loose_tauID = "decayModeFindingNewDMs"
tauAna.loose_vetoLeptons = False # no cleaning with leptons in production
#    jetAna.cleanJetsFromTaus = True
#    jetAnaScaleUp.cleanJetsFromTaus = True
#    jetAnaScaleDown.cleanJetsFromTaus = True


#-------- ADDITIONAL ANALYZERS -----------

## Event Analyzer for susy multi-lepton (at the moment, it's the TTH one)
from CMGTools.TTHAnalysis.analyzers.ttHLepEventAnalyzer import ttHLepEventAnalyzer
ttHEventAna = cfg.Analyzer(
    ttHLepEventAnalyzer, name="ttHLepEventAnalyzer",
    minJets25 = 0,
    )

## JetTau analyzer, to be called (for the moment) once bjetsMedium are produced
from CMGTools.TTHAnalysis.analyzers.ttHJetTauAnalyzer import ttHJetTauAnalyzer
ttHJetTauAna = cfg.Analyzer(
    ttHJetTauAnalyzer, name="ttHJetTauAnalyzer",
    )

## Insert the SV analyzer in the sequence
susyCoreSequence.insert(susyCoreSequence.index(ttHCoreEventAna), 
                        ttHSVAna)
ttHSVAna.preselection = lambda ivf : abs(ivf.dxy.value())<2 and ivf.cosTheta>0.98


from CMGTools.TTHAnalysis.analyzers.treeProducerSusyMultilepton import * 
del susyMultilepton_collections['generatorSummary']
del susyMultilepton_collections['otherTaus']
del susyMultilepton_collections['otherLeptons']
del susyMultilepton_collections['discardedJets']
del susyMultilepton_collections['discardedLeptons']

# Spring16 electron MVA - follow instructions on pull request for correct area setup
leptonTypeSusy.addVariables([
        NTupleVariable("mvaIdSpring16HZZ",   lambda lepton : lepton.mvaRun2("Spring16HZZ") if abs(lepton.pdgId()) == 11 else 1, help="EGamma POG MVA ID, Spring16, HZZ; 1 for muons"),
        NTupleVariable("mvaIdSpring16GP",   lambda lepton : lepton.mvaRun2("Spring16GP") if abs(lepton.pdgId()) == 11 else 1, help="EGamma POG MVA ID, Spring16, GeneralPurpose; 1 for muons"),
        ])

if not removeJecUncertainty:
    susyMultilepton_globalObjects.update({
            "met_jecUp" : NTupleObject("met_jecUp", metType, help="PF E_{T}^{miss}, after type 1 corrections (JEC plus 1sigma)"),
            "met_jecDown" : NTupleObject("met_jecDown", metType, help="PF E_{T}^{miss}, after type 1 corrections (JEC minus 1sigma)"),
            })

## Tree Producer
treeProducer = cfg.Analyzer(
     AutoFillTreeProducer, name='treeProducerSusyMultilepton',
     vectorTree = True,
     saveTLorentzVectors = False,  # can set to True to get also the TLorentzVectors, but trees will be bigger
     defaultFloatType = 'F', # use Float_t for floating point
     PDFWeights = PDFWeights,
     globalVariables = susyMultilepton_globalVariables,
     globalObjects = susyMultilepton_globalObjects,
     collections = susyMultilepton_collections,
)


## histo counter
susyCoreSequence.insert(susyCoreSequence.index(skimAnalyzer),
                        susyCounter)
susyScanAna.doLHE=False # until a proper fix is put in the analyzer

treeProducer.globalVariables.append(NTupleVariable("Flag_badChargedHadronFilter", lambda ev: ev.badChargedHadron, help="bad charged hadron filter decision"))
treeProducer.globalVariables.append(NTupleVariable("Flag_badMuonFilter", lambda ev: ev.badMuon, help="bad muon filter decision"))


#additional MET quantities
metAna.doTkMet = True
treeProducer.globalVariables.append(NTupleVariable("met_trkPt", lambda ev : ev.tkMet.pt() if  hasattr(ev,'tkMet') else  0, help="tkmet p_{T}"))
treeProducer.globalVariables.append(NTupleVariable("met_trkPhi", lambda ev : ev.tkMet.phi() if  hasattr(ev,'tkMet') else  0, help="tkmet phi"))

if not skipT1METCorr:
    if doMETpreprocessor: 
        print "WARNING: you're running the MET preprocessor and also Type1 MET corrections. This is probably not intended."
    jetAna.calculateType1METCorrection = True
    metAna.recalibrate = "type1"
    jetAnaScaleUp.calculateType1METCorrection = True
    metAnaScaleUp.recalibrate = "type1"
    jetAnaScaleDown.calculateType1METCorrection = True
    metAnaScaleDown.recalibrate = "type1"


#-------- SAMPLES AND TRIGGERS -----------


from CMGTools.RootTools.samples.triggers_13TeV_DATA2016 import *
triggerFlagsAna.triggerBits = {
    'DoubleMu' : triggers_mumu_iso,
    'DoubleMuSS' : triggers_mumu_ss,
    'DoubleMuNoIso' : triggers_mumu_noniso,
    'DoubleEl' : triggers_ee,
    'MuEG'     : triggers_mue,
    'DoubleMuHT' : triggers_mumu_ht,
    'DoubleElHT' : triggers_ee_ht,
    'MuEGHT' : triggers_mue_ht,
    'TripleEl' : triggers_3e,
    'TripleMu' : triggers_3mu,
    'TripleMuA' : triggers_3mu_alt,
    'DoubleMuEl' : triggers_2mu1e,
    'DoubleElMu' : triggers_2e1mu,
    'SingleMu' : triggers_1mu_iso,
    'SingleEl'     : triggers_1e,
    'SOSHighMET' : triggers_SOS_highMET,
    'SOSDoubleMuLowMET' : triggers_SOS_doublemulowMET,
    'SOSTripleMu' : triggers_SOS_tripleMu,
    'LepTau' : triggers_leptau,
    'MET' : triggers_metNoMu90_mhtNoMu90,
    #'MonoJet80MET90' : triggers_Jet80MET90,
    #'MonoJet80MET120' : triggers_Jet80MET120,
    #'METMu5' : triggers_MET120Mu5,
}
triggerFlagsAna.unrollbits = True
triggerFlagsAna.saveIsUnprescaled = True
triggerFlagsAna.checkL1Prescale = True

from CMGTools.RootTools.samples.samples_13TeV_RunIISummer16MiniAODv2 import *
from CMGTools.RootTools.samples.samples_13TeV_DATA2016 import *
from CMGTools.HToZZ4L.tools.configTools import printSummary, configureSplittingFromTime, cropToLumi, prescaleComponents, insertEventSelector, mergeExtensions
from CMGTools.RootTools.samples.autoAAAconfig import *

selectedComponents = [TTLep_pow]


sig_ttv = [TTHnobb_pow,TTWToLNu_ext,TTWToLNu_ext2,TTZToLLNuNu_ext,TTZToLLNuNu_m1to10] # signal + TTV
ttv_lo = [TTW_LO,TTZ_LO] # TTV LO
rares = [ZZTo4L,GGHZZ4L,VHToNonbb,tZq_ll_ext,WpWpJJ,WWDouble,TTTT,tWll] # rares
single_t = [TToLeptons_sch_amcatnlo,T_tch_powheg,TBar_tch_powheg,T_tWch_ext,TBar_tWch_ext] # single top + tW
convs = [WGToLNuG_amcatnlo_ext,ZGTo2LG_ext,TGJets,TTGJets] # X+G
v_jets = [WJetsToLNu_LO,DYJetsToLL_M10to50_LO,DYJetsToLL_M50_LO_ext,WWTo2L2Nu] # V+jets
tt_1l = [TTJets_SingleLeptonFromT,TTJets_SingleLeptonFromT_ext,TTJets_SingleLeptonFromTbar,TTJets_SingleLeptonFromTbar_ext] # TT 1l
tt_2l = [TTJets_DiLepton]#,TTJets_DiLepton_ext] # TT 2l
boson = [WZTo3LNu]+TriBosons # multi-boson

samples_slow = sig_ttv + ttv_lo + rares + convs + boson + tt_2l
samples_fast = single_t + v_jets + tt_1l

cropToLumi(rares,500)
cropToLumi([T_tch_powheg,TBar_tch_powheg],50)
configureSplittingFromTime(samples_fast,50,6)
configureSplittingFromTime(samples_slow,100,6)

#selectedComponents = samples_slow+samples_fast

if scaleProdToLumi>0: # select only a subset of a sample, corresponding to a given luminosity (assuming ~30k events per MiniAOD file, which is ok for central production)
    target_lumi = scaleProdToLumi # in inverse picobarns
    for c in selectedComponents:
        if not c.isMC: continue
        nfiles = int(min(ceil(target_lumi * c.xSection / 30e3), len(c.files)))
        #if nfiles < 50: nfiles = min(4*nfiles, len(c.files))
        print "For component %s, will want %d/%d files; AAA %s" % (c.name, nfiles, len(c.files), "eoscms" not in c.files[0])
        c.files = c.files[:nfiles]
        c.splitFactor = len(c.files)
        c.fineSplitFactor = 1


if runData and not isTest: # For running on data

    is50ns = False
    dataChunks = []

#    json = os.environ['CMSSW_BASE']+'/src/CMGTools/TTHAnalysis/data/json/Cert_271036-276811_13TeV_PromptReco_Collisions16_JSON_NoL1T.txt' # 12.9/fb #276811 ICHEP LastRun
    json = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/ReReco/Final/Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt' # 36.5/fb

    for era in 'BCDEFGH': dataChunks.append((json,filter(lambda dset: 'Run2016'+era in dset.name,dataSamples_23Sep2016PlusPrompt),'2016'+era,[],False))
    #for era in 'C': dataChunks.append((json,filter(lambda dset: 'Run2016'+era in dset.name,dataSamples_23Sep2016PlusPrompt),'2016'+era,[],False))
    #for era in 'C': dataChunks.append((json,filter(lambda dset: 'Run2016'+era in dset.name,[DoubleMuon_Run2016C_02Feb2017]),'2016'+era,[],False))

    DatasetsAndTriggers = []
    selectedComponents = [];
    exclusiveDatasets = True; # this will veto triggers from previous PDs in each PD, so that there are no duplicate events
 
    DatasetsAndTriggers.append( ("DoubleMuon", triggers_mumu_iso + triggers_mumu_ss + triggers_mumu_ht + triggers_3mu + triggers_3mu_alt) )
    #DatasetsAndTriggers.append( ("DoubleEG",   triggers_ee + triggers_ee_ht + triggers_3e) )
    #DatasetsAndTriggers.append( ("MuonEG",     triggers_mue + triggers_mue_ht + triggers_2mu1e + triggers_2e1mu) )
    #DatasetsAndTriggers.append( ("SingleMuon", triggers_1mu_iso + triggers_1mu_noniso) )
    #DatasetsAndTriggers.append( ("SingleElectron", triggers_1e) )

    if runDataQCD: # for fake rate measurements in data
        FRTrigs_mu = triggers_FR_1mu_noiso
        FRTrigs_el = triggers_FR_1e_noiso
        DatasetsAndTriggers = [
            #("DoubleMuon", FRTrigs_mu ),
            #("DoubleEG",   FRTrigs_el ),
            ("SingleMuon", triggers_FR_muNoIso ),
            #("JetHT",   triggers_FR_jet )
        ]
        triggers_FR_muNoIso = [ 'HLT_Mu27_v*', 'HLT_Mu50_v*' ]
        triggerAna.myTriggerPrescales = { 'HLT_Mu50_v*':10 }
        exclusiveDatasets = False
    if runDataQCD and runQCDBM: # for fake rate measurements in data
        FRTrigs_mu = triggers_FR_1mu_iso + triggers_FR_1mu_noiso
        FRTrigs_el = triggers_FR_1e_noiso + triggers_FR_1e_iso + triggers_FR_1e_b2g
        DatasetsAndTriggers = [
            ("SingleMuon", triggers_FR_muNoIso ),
            #("DoubleMuon",  triggers_FR_1mu_noiso ),
        ]
        exclusiveDatasets = True
    for json,dsets,short,run_ranges,useAAA in dataChunks:
        if len(run_ranges)==0: run_ranges=[None]
        vetos = []
        for pd,triggers in DatasetsAndTriggers:
            for run_range in run_ranges:
                label = ""
                if run_range!=None:
                    label = "_runs_%d_%d" % run_range if run_range[0] != run_range[1] else "run_%d" % (run_range[0],)
                _ds = filter(lambda dset : re.match('%s_.*'%pd,dset.name),dsets)
                for idx,_comp in enumerate(_ds):
                    compname = pd+"_"+short+label
                    if (len(_ds)>1): compname += '_ds%d'%(idx+1)
                    comp = kreator.makeDataComponent(compname, 
                                                     _comp.dataset,
                                                     "CMS", ".*root", 
                                                     json=json, 
                                                     run_range=(run_range if "PromptReco" not in _comp.dataset else None), 
                                                     triggers=triggers[:], vetoTriggers = vetos[:],
                                                     useAAA=useAAA)
                    if "PromptReco" in comp.dataset:
                        from CMGTools.Production.promptRecoRunRangeFilter import filterComponent
                        filterComponent(comp, verbose=0)
                    #print "Will process %s (%d files)" % (comp.name, len(comp.files))
                    comp.splitFactor = len(comp.files)/8 if 'Single' not in comp.name else len(comp.files)/16
                    comp.fineSplitFactor = 1
                    selectedComponents.append( comp )
            if exclusiveDatasets: vetos += triggers
    if json is None:
        susyCoreSequence.remove(jsonAna)
    if runDataQCD: # for fake rate measurements in data
         configureSplittingFromTime(selectedComponents, 3.5, 2, maxFiles=15)
    #configureSplittingFromTime(selectedComponents, 10, 1, maxFiles=2)

#printSummary(selectedComponents)


if runFRMC: 
    QCD_Mu5 = [ QCD_Pt20to30_Mu5, QCD_Pt30to50_Mu5, QCD_Pt50to80_Mu5, QCD_Pt80to120_Mu5, QCD_Pt120to170_Mu5, QCD_Pt170to300_Mu5 ]
    autoAAA(QCDPtEMEnriched+QCDPtbcToE)
    QCDEm, _ = mergeExtensions([q for q in QCDPtEMEnriched+QCDPtbcToE if "toInf" not in q.name])
    selectedComponents = [QCD_Mu15] + QCD_Mu5 + [WJetsToLNu_LO,DYJetsToLL_M10to50_LO,DYJetsToLL_M50_LO_ext] + QCDEm
    selectedComponents = [TTJets_DiLepton]#TTJets_SingleLeptonFromT,TTJets_SingleLeptonFromTbar]
    selectedComponents = [TBar_tWch_noFullyHad,T_tWch_noFullyHad]
    TTJets_DiLepton.fineSplitFactor = 2
    #selectedComponents = TT_pow 
    cropToLumi(selectedComponents, 1.0)
    time = 5.0; extra = dict(maxFiles=10)
    configureSplittingFromTime([WJetsToLNu_LO],20,time, **extra)
    configureSplittingFromTime([DYJetsToLL_M10to50_LO],10,time, **extra)
    configureSplittingFromTime([DYJetsToLL_M50_LO_ext],40,time, **extra)
    configureSplittingFromTime([QCD_Mu15]+QCD_Mu5,40,time, **extra)
    configureSplittingFromTime(QCDEm, 40, time, **extra)
    #configureSplittingFromTime([ QCD_HT100to200, QCD_HT200to300 ],10,time, **extra)
    #configureSplittingFromTime([ QCD_HT300to500, QCD_HT500to700 ],15,time, **extra)
    if runQCDBM:
        configureSplittingFromTime([QCD_Mu15]+QCD_Mu5,15,time, **extra)
    for c in selectedComponents:
        c.triggers = []
        c.vetoTriggers = [] 
    #printSummary(selectedComponents)

if runFRMC or runDataQCD:
    ttHLepSkim.minLeptons = 1
    if ttHJetMETSkim in susyCoreSequence: susyCoreSequence.remove(ttHJetMETSkim)
    if getHeppyOption("fast"): raise RuntimeError, 'Already added ttHFastLepSkimmer with 2-lep configuration, this is wrong.'
    FRTrigs = triggers_FR_1mu_iso + triggers_FR_1mu_noiso + triggers_FR_1e_noiso + triggers_FR_1e_iso + triggers_FR_1e_b2g + triggers_FR_jet + triggers_FR_muNoIso
    for t in FRTrigs:
        tShort = t.replace("HLT_","FR_").replace("_v*","")
        triggerFlagsAna.triggerBits[tShort] = [ t ]
    treeProducer.collections = {
        "selectedLeptons" : NTupleCollection("LepGood",  leptonTypeSusyExtraLight, 8, help="Leptons after the preselection"),
        "cleanJets"       : NTupleCollection("Jet",     jetTypeSusyExtraLight, 15, help="Cental jets after full selection and cleaning, sorted by pt"),
        "selectedTaus"    : NTupleCollection("TauGood",  tauTypeSusy, 8, help="Taus after the preselection"),
    }
    if True: # 
        from CMGTools.TTHAnalysis.analyzers.ttHLepQCDFakeRateAnalyzer import ttHLepQCDFakeRateAnalyzer
        ttHLepQCDFakeRateAna = cfg.Analyzer(ttHLepQCDFakeRateAnalyzer, name="ttHLepQCDFakeRateAna",
            #jetSel = lambda jet : jet.pt() > (25 if abs(jet.eta()) < 2.4 else 30),
            jetSel = lambda jet : jet.pt() > 30 and abs(jet.eta()) < 2.4,
            pairSel = lambda lep, jet: deltaR(lep.eta(),lep.phi(), jet.eta(), jet.phi()) > 0.7,
        )
        susyCoreSequence.insert(susyCoreSequence.index(jetAna)+1, ttHLepQCDFakeRateAna)
        leptonTypeSusyExtraLight.addVariables([
            NTupleVariable("awayJet_pt", lambda x: x.awayJet.pt() if x.awayJet else 0, help="pT of away jet"),
            NTupleVariable("awayJet_eta", lambda x: x.awayJet.eta() if x.awayJet else 0, help="eta of away jet"),
            NTupleVariable("awayJet_phi", lambda x: x.awayJet.phi() if x.awayJet else 0, help="phi of away jet"),
            NTupleVariable("awayJet_btagCSV", lambda x: x.awayJet.btag('pfCombinedInclusiveSecondaryVertexV2BJetTags') if x.awayJet else 0, help="b-tag disc of away jet"),
            NTupleVariable("awayJet_mcFlavour", lambda x: x.awayJet.partonFlavour() if x.awayJet else 0, int, mcOnly=True, help="pT of away jet"),
        ])
    if True: # drop events that don't have at least one lepton+jet pair (reduces W+jets by ~50%)
        ttHLepQCDFakeRateAna.minPairs = 1
    if True: # fast skim 
        from CMGTools.TTHAnalysis.analyzers.ttHFastLepSkimmer import ttHFastLepSkimmer
        fastSkim = cfg.Analyzer(
            ttHFastLepSkimmer, name="ttHFastLepSkimmer1lep",
            muons = 'slimmedMuons', muCut = lambda mu : mu.pt() > 3 and mu.isLooseMuon(),
            electrons = 'slimmedElectrons', eleCut = lambda ele : ele.pt() > 5,
            minLeptons = 1,
        )
        susyCoreSequence.insert(susyCoreSequence.index(jsonAna)+1, fastSkim)
        susyCoreSequence.remove(lheWeightAna)
        susyCounter.doLHE = False
    if runQCDBM:
        fastSkimBM = cfg.Analyzer(
            ttHFastLepSkimmer, name="ttHFastLepSkimmerBM",
            muons = 'slimmedMuons', muCut = lambda mu : mu.pt() > 8,
            electrons = 'slimmedElectrons', eleCut = lambda ele : False,
            minLeptons = 1,
        )
        fastSkim.minLeptons = 2
        ttHLepSkim.maxLeptons = 1
        susyCoreSequence.insert(susyCoreSequence.index(skimAnalyzer)+1, fastSkimBM)
        from PhysicsTools.Heppy.analyzers.core.TriggerMatchAnalyzer import TriggerMatchAnalyzer
        trigMatcher1Mu2J = cfg.Analyzer(
            TriggerMatchAnalyzer, name="trigMatcher1Mu",
            label='1Mu',
            processName = 'PAT',
            fallbackProcessName = 'RECO',
            unpackPathNames = True,
            trgObjSelectors = [ lambda t : t.path("HLT_Mu8_v*",1,0) or t.path("HLT_Mu17_v*",1,0) or t.path("HLT_Mu22_v*",1,0) or t.path("HLT_Mu27_v*",1,0) or t.path("HLT_Mu45_eta2p1_v*",1,0) or t.path("HLT_L2Mu10_v*",1,0) ],
            collToMatch = 'cleanJetsAll',
            collMatchSelectors = [ lambda l,t : True ],
            collMatchDRCut = 0.4,
            univoqueMatching = True,
            verbose = False,
            )
        susyCoreSequence.insert(susyCoreSequence.index(jetAna)+1, trigMatcher1Mu2J)
        ttHLepQCDFakeRateAna.jetSel = lambda jet : jet.pt() > 25 and abs(jet.eta()) < 2.4 and jet.matchedTrgObj1Mu
if sample == "z3l":
    ttHLepSkim.minLeptons = 3
    if getHeppyOption("fast"): raise RuntimeError, 'Already added ttHFastLepSkimmer with 2-lep configuration, this is wrong.'
    treeProducer.collections = {
        "selectedLeptons" : NTupleCollection("LepGood", leptonTypeSusyExtraLight, 8, help="Leptons after the preselection"),
        "cleanJets"       : NTupleCollection("Jet",     jetTypeSusyExtraLight, 15, help="Cental jets after full selection and cleaning, sorted by pt"),
    }
    from CMGTools.TTHAnalysis.analyzers.ttHFastLepSkimmer import ttHFastLepSkimmer
    fastSkim = cfg.Analyzer(
        ttHFastLepSkimmer, name="ttHFastLepSkimmer3lep",
        muons = 'slimmedMuons', muCut = lambda mu : mu.pt() > 3 and mu.isLooseMuon(),
        electrons = 'slimmedElectrons', eleCut = lambda ele : ele.pt() > 5,
        minLeptons = 3,
    )
    fastSkim2 = cfg.Analyzer(
        ttHFastLepSkimmer, name="ttHFastLepSkimmer2lep",
        muons = 'slimmedMuons', muCut = lambda mu : mu.pt() > 10 and mu.isLooseMuon(),
        electrons = 'slimmedElectrons', eleCut = lambda ele : ele.pt() > 10,
        minLeptons = 2,
    )
    susyCoreSequence.insert(susyCoreSequence.index(jsonAna)+1, fastSkim)
    susyCoreSequence.insert(susyCoreSequence.index(jsonAna)+1, fastSkim2)
    susyCoreSequence.remove(lheWeightAna)
    susyCoreSequence.remove(ttHJetMETSkim)
    susyCounter.doLHE = False
    if not runData:
        selectedComponents = [DYJetsToLL_M50_LO]
        #prescaleComponents([DYJetsToLL_M50_LO], 2)
        #configureSplittingFromTime([DYJetsToLL_M50_LO],4,1.5)
        selectedComponents = [WZTo3LNu,ZZTo4L]
        cropToLumi([WZTo3LNu,ZZTo4L], 50)
        #configureSplittingFromTime([WZTo3LNu,ZZTo4L],20,1.5)
    else:
        if True:
            from CMGTools.Production.promptRecoRunRangeFilter import filterComponent
            for c in selectedComponents:  
                if "PromptReco" in c.name: filterComponent(c, 1)
        if analysis == 'SOS':
            configureSplittingFromTime(selectedComponents,10,2)

if removeJetReCalibration:
    jetAna.recalibrateJets = False
    jetAnaScaleUp.recalibrateJets = False
    jetAnaScaleDown.recalibrateJets = False

if getHeppyOption("noLepSkim",False):
    ttHLepSkim.minLeptons=0

if forcedSplitFactor>0 or forcedFineSplitFactor>0:
    if forcedFineSplitFactor>0 and forcedSplitFactor!=1: raise RuntimeError, 'splitFactor must be 1 if setting fineSplitFactor'
    for c in selectedComponents:
        if forcedSplitFactor>0: c.splitFactor = forcedSplitFactor
        if forcedFineSplitFactor>0: c.fineSplitFactor = forcedFineSplitFactor

if selectedEvents!="":
    events=[ int(evt) for evt in selectedEvents.split(",") ]
    print "selecting only the following events : ", events
    eventSelector= cfg.Analyzer(
        EventSelector,'EventSelector',
        toSelect = events
        )
    susyCoreSequence.insert(susyCoreSequence.index(lheWeightAna), eventSelector)

#-------- SEQUENCE -----------

sequence = cfg.Sequence(susyCoreSequence+[
        ttHJetTauAna,
        ttHEventAna,
        treeProducer,
    ])
preprocessor = None

#-------- HOW TO RUN -----------

test = getHeppyOption('test')
if test == '1':
    comp = selectedComponents[0]
    if getHeppyOption('manyfiles'):
        filesPerJob = max(len(comp.files)/comp.splitFactor, 1)
        comp.files = comp.files[:filesPerJob]
    else:
        #comp.files = comp.files[:1]
        comp.files = comp.files[8:9]
    comp.splitFactor = 1
    comp.fineSplitFactor = 1
    selectedComponents = [ comp ]
elif test == '2':
    sel = getHeppyOption('sel','.*')
    for comp in selectedComponents[:]:
        if sel and not any(re.search(p.strip(),comp.name) for p in sel.split(",")):
            selectedComponents.remove(comp)
            continue
        comp.files = comp.files[:1]
        comp.splitFactor = 1
        comp.fineSplitFactor = 1
elif test == '3':
    for comp in selectedComponents:
        comp.files = comp.files[:1]
        comp.splitFactor = 1
        comp.fineSplitFactor = 4
elif test == '5':
    for comp in selectedComponents:
        comp.files = comp.files[:5]
        comp.splitFactor = 1
        comp.fineSplitFactor = 5
elif test == '21':
    for comp in selectedComponents:
        comp.files = comp.files[:7]
        comp.splitFactor = 1
        comp.fineSplitFactor = 3
elif test == "tau-sync":
    comp = cfg.MCComponent( files = [ "root://eoscms.cern.ch//store/mc/RunIISpring16MiniAODv2/TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/50000/8E84F4BB-B620-E611-BBD8-B083FECFF2BF.root"], name="TTW_Tau" )
    comp.triggers = []
    comp.splitFactor = 1
    comp.fineSplitFactor = 6
    selectedComponents = [ comp ]
    sequence.remove(jsonAna)
    ttHLepSkim.minLeptons = 0
elif test == '80X-MC':
    what = getHeppyOption("sample","TTLep")
    if what == "TTLep":
        TTLep_pow = kreator.makeMCComponent("TTLep_pow", "/TTTo2L2Nu_13TeV-powheg/RunIISpring16MiniAODv1-PUSpring16_80X_mcRun2_asymptotic_2016_v3_ext1-v1/MINIAODSIM", "CMS", ".*root", 831.76*((3*0.108)**2) )
        selectedComponents = [ TTLep_pow ]
        comp = selectedComponents[0]
        comp.triggers = []
        comp.files = [ '/store/mc/RunIISpring16MiniAODv1/TTTo2L2Nu_13TeV-powheg/MINIAODSIM/PUSpring16_80X_mcRun2_asymptotic_2016_v3_ext1-v1/00000/002606A5-C909-E611-85DA-44A8423D7E31.root' ]
        tmpfil = os.path.expandvars("/tmp/$USER/002606A5-C909-E611-85DA-44A8423D7E31.root")
        if not os.path.exists(tmpfil):
            os.system("xrdcp root://eoscms//eos/cms%s %s" % (comp.files[0],tmpfil))
        comp.files = [ tmpfil ]
        if not getHeppyOption("single"): comp.fineSplitFactor = 4
    else: raise RuntimeError, "Unknown MC sample: %s" % what
elif test == '80X-Data':
    DoubleMuon = kreator.makeDataComponent("DoubleMuon_Run2016B_run274315", "/DoubleMuon/Run2016B-PromptReco-v2/MINIAOD", "CMS", ".*root", run_range = (274315,274315), triggers = triggers_mumu)
    DoubleEG = kreator.makeDataComponent("DoubleEG_Run2016B_run274315", "/DoubleEG/Run2016B-PromptReco-v2/MINIAOD", "CMS", ".*root", run_range = (274315,274315), triggers = triggers_ee)
    DoubleMuon.files = [ 'root://eoscms//eos/cms/store/data/Run2016B/DoubleMuon/MINIAOD/PromptReco-v2/000/274/315/00000/A287989F-E129-E611-B5FB-02163E0142C2.root' ]
    DoubleEG.files = [ 'root://eoscms//eos/cms/store/data/Run2016B/DoubleEG/MINIAOD/PromptReco-v2/000/274/315/00000/FEF59D1D-EE29-E611-8793-02163E0143AE.root' ]
    selectedComponents = [ DoubleMuon, DoubleEG ]
    for comp in selectedComponents:
        comp.json = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/Cert_271036-275125_13TeV_PromptReco_Collisions16_JSON.txt'
        tmpfil = os.path.expandvars("/tmp/$USER/%s" % os.path.basename(comp.files[0]))
        if not os.path.exists(tmpfil): os.system("xrdcp %s %s" % (comp.files[0],tmpfil)) 
        comp.files = [tmpfil]
        comp.splitFactor = 1
        comp.fineSplitFactor = 4
elif test == 'mem-sync':
    ttHLepSkim.minLeptons=3
    selectedComponents = [TTWToLNu_ext]
    comp = selectedComponents[0]
    comp.files = ['root://eoscms//store/mc/RunIISummer16MiniAODv2/TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1/110000/0015BB42-9BAA-E611-8C7F-0CC47A7E0196.root']
    #if not getHeppyOption("single"): comp.fineSplitFactor = 8
elif test == 'ttH-sync':
    ttHLepSkim.minLeptons=0
    jetAna.recalibrateJets = False # JEC from MiniAOD for sync
    selectedComponents = [TTWToLNu_ext]
    comp = selectedComponents[0]
    comp.files = ['/store/mc/RunIISummer16MiniAODv2/TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1/110000/0015BB42-9BAA-E611-8C7F-0CC47A7E0196.root']
    tmpfil = os.path.expandvars("/tmp/$USER/0015BB42-9BAA-E611-8C7F-0CC47A7E0196.root")
    if not os.path.exists(tmpfil):
        os.system("xrdcp root://eoscms//eos/cms%s %s" % (comp.files[0],tmpfil))
    comp.files = [ tmpfil ]
    if not getHeppyOption("single"): comp.fineSplitFactor = 8
elif test != None:
    raise RuntimeError, "Unknown test %r" % test

## FAST mode: pre-skim using reco leptons, don't do accounting of LHE weights (slow)"
## Useful for large background samples with low skim efficiency
if getHeppyOption("fast"):
    susyCounter.doLHE = False
    from CMGTools.TTHAnalysis.analyzers.ttHFastLepSkimmer import ttHFastLepSkimmer
    fastSkim = cfg.Analyzer(
        ttHFastLepSkimmer, name="ttHFastLepSkimmer2lep",
        muons = 'slimmedMuons', muCut = lambda mu : mu.pt() > 3 and mu.isLooseMuon(),
        electrons = 'slimmedElectrons', eleCut = lambda ele : ele.pt() > 5,
        minLeptons = 2, 
    )
    if jsonAna in sequence:
        sequence.insert(sequence.index(jsonAna)+1, fastSkim)
    else:
        sequence.insert(sequence.index(skimAnalyzer)+1, fastSkim)
if getHeppyOption("prescale"):
    from CMGTools.TTHAnalysis.analyzers.ttHPrescaler import ttHPrescaler
    psvalue =int( getHeppyOption("prescale") ) 
    if psvalue <= 1: raise RuntimeError
    thePrescale = cfg.Analyzer(ttHPrescaler, name="ttHPrescaler", 
            prescaleFactor = psvalue,
            useEventNumber = True)
    if jsonAna in sequence:
        sequence.insert(sequence.index(jsonAna)+1, thePrescale)
    else:
        sequence.insert(sequence.index(skimAnalyzer)+1, thePrescale)

if not getHeppyOption("keepLHEweights",False):
    if "LHE_weights" in treeProducer.collections: treeProducer.collections.pop("LHE_weights")
    if lheWeightAna in sequence: sequence.remove(lheWeightAna)
    susyCounter.doLHE = False

## Auto-AAA
if not getHeppyOption("isCrab"):
    autoAAA(selectedComponents)

## output histogram
outputService=[]
from PhysicsTools.HeppyCore.framework.services.tfile import TFileService
output_service = cfg.Service(
    TFileService,
    'outputfile',
    name="outputfile",
    fname='treeProducerSusyMultilepton/tree.root',
    option='recreate'
    )    
outputService.append(output_service)


selectComponents = getHeppyOption('selectComponents',None)
if selectComponents:
    for comp in selectedComponents[:]:
        if not any(re.search(p.strip(),comp.name) for p in selectComponents.split(",")):
            selectedComponents.remove(comp)

# print summary of components to process
printSummary(selectedComponents)

# the following is declared in case this cfg is used in input to the heppy.py script
from PhysicsTools.HeppyCore.framework.eventsfwlite import Events
from CMGTools.TTHAnalysis.tools.EOSEventsWithDownload import EOSEventsWithDownload
event_class = EOSEventsWithDownload if not preprocessor else Events
EOSEventsWithDownload.aggressive = 2 # always fetch if running on Wigner
if getHeppyOption("nofetch") or getHeppyOption("isCrab"):
    event_class = Events
    if preprocessor: preprocessor.prefetch = False
config = cfg.Config( components = selectedComponents,
                     sequence = sequence,
                     services = outputService, 
                     preprocessor = preprocessor, 
                     events_class = event_class)
