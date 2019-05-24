import re, os, sys
from CMGTools.RootTools.samples.configTools import printSummary, mergeExtensions, doTestN, configureSplittingFromTime, cropToLumi
from CMGTools.RootTools.samples.autoAAAconfig import autoAAA
from PhysicsTools.HeppyCore.framework.heppy_loop import getHeppyOption

from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()
def byCompName(components, regexps):
    return [ c for c in components if any(re.match(r, c.name) for r in regexps) ]

year = int(getHeppyOption("year", "2018"))
analysis = getHeppyOption("analysis", "main")
preprocessor = getHeppyOption("nanoPreProcessor")

# Samples
if preprocessor:
    if year == 2018:
        from CMGTools.RootTools.samples.samples_13TeV_RunIIAutumn18MiniAOD import samples as mcSamples_
        from CMGTools.RootTools.samples.samples_13TeV_DATA2018_MiniAOD import samples as allData
    elif year == 2017:
        from CMGTools.RootTools.samples.samples_13TeV_RunIIFall17MiniAOD import samples as mcSamples_
        from CMGTools.RootTools.samples.samples_13TeV_DATA2017 import dataSamples_31Mar2018 as allData
    elif year == 2016:
        from CMGTools.RootTools.samples.samples_13TeV_RunIISummer16MiniAODv3 import samples as mcSamples_
        from CMGTools.RootTools.samples.samples_13TeV_DATA2016 import dataSamples_17Jul2018 as allData
else:
    if year == 2018:
        from CMGTools.RootTools.samples.samples_13TeV_RunIIAutumn18NanoAODv4 import samples as mcSamples_
        from CMGTools.RootTools.samples.samples_13TeV_DATA2018_NanoAOD import samples as allData
    elif year == 2017:
        from CMGTools.RootTools.samples.samples_13TeV_RunIIFall17NanoAODv4 import samples as mcSamples_
        from CMGTools.RootTools.samples.samples_13TeV_DATA2017_NanoAOD import samples as allData
    elif year == 2016:
        from CMGTools.RootTools.samples.samples_13TeV_RunIISummer16NanoAODv4 import samples as mcSamples_
        from CMGTools.RootTools.samples.samples_13TeV_DATA2016_NanoAOD import samples as allData
autoAAA(mcSamples_+allData, quiet=not(getHeppyOption("verboseAAA",False))) # must be done before mergeExtensions
mcSamples_, _ = mergeExtensions(mcSamples_)

# Triggers
if year == 2018:
    from CMGTools.RootTools.samples.triggers_13TeV_DATA2018 import all_triggers as triggers
elif year == 2017:
    from CMGTools.RootTools.samples.triggers_13TeV_DATA2017 import all_triggers as triggers
    triggers["FR_1mu_iso"] = [] # they probably existed but we didn't use them in 2017
elif year == 2016:
    from CMGTools.RootTools.samples.triggers_13TeV_DATA2016 import all_triggers as triggers
    triggers["FR_1mu_noiso_smpd"] = [] 


DatasetsAndTriggers = []
if analysis == "main":
    mcSamples = byCompName(mcSamples_, [
        "WJetsToLNu_LO$", "DYJetsToLL_M10to50_LO$", "DYJetsToLL_M50$",
        "TTJets_SingleLeptonFromT$", "TTJets_SingleLeptonFromTbar$", "TTJets_DiLepton$",
        "T_sch_lep$", "T_tch$", "TBar_tch$", "T_tWch_noFullyHad$", "TBar_tWch_noFullyHad$",
        "TTGJets$", "TGJets_lep",
        "TTWToLNu_fxfx$", "TTZToLLNuNu_amc$", "TTZToLLNuNu_m1to10$",
        "TT[WZ]_LO$",
        "TTHnobb_pow$",
        "TZQToLL$", "tWll$", "TTTT$", "TTWW$",
        "WWTo2L2Nu$", "WZTo3LNu_fxfx$",  "ZZTo4L$", "WW_DPS$", "WpWpJJ$",
        "GGHZZ4L$", "VHToNonbb_ll$",
        "WWW_ll$", "WWZ$", "WZG$", "WZZ$", "ZZZ$",
    ])
    DatasetsAndTriggers.append( ("DoubleMuon", triggers["mumu_iso"] + triggers["3mu"]) )
    DatasetsAndTriggers.append( ("EGamma",     triggers["ee"] + triggers["3e"] + triggers["1e_iso"]) if year == 2018 else
                                ("DoubleEG",   triggers["ee"] + triggers["3e"]) )
    DatasetsAndTriggers.append( ("MuonEG",     triggers["mue"] + triggers["2mu1e"] + triggers["2e1mu"]) )
    DatasetsAndTriggers.append( ("SingleMuon", triggers["1mu_iso"]) )
    DatasetsAndTriggers.append( ("SingleElectron", triggers["1e_iso"]) if year != 2018 else (None,None) )
elif analysis == "frqcd":
    mcSamples = byCompName(mcSamples_, [
        "QCD_Mu15", "QCD_Pt(20|30|50|80|120|170)to.*_Mu5", 
        "QCD_Pt(20|30|50|80|120|170)to.*_EMEn.*", 
      (r"QCD_Pt(20|30|50|80|120|170)to\d+$"       if year == 2018 else  
        "QCD_Pt(20|30|50|80|120|170)to.*_bcToE.*" ),        
        "WJetsToLNu_LO", "DYJetsToLL_M50_LO", "DYJetsToLL_M10to50_LO", "TT(Lep|Semi)_pow"
    ])
    DatasetsAndTriggers.append( ("DoubleMuon", triggers["FR_1mu_noiso"] + triggers["FR_1mu_iso"]) )
    DatasetsAndTriggers.append( ("EGamma",         triggers["FR_1e_noiso"] + triggers["FR_1e_iso"]) if year == 2018 else
                                ("SingleElectron", triggers["FR_1e_noiso"] + triggers["FR_1e_iso"]) )
    DatasetsAndTriggers.append( ("SingleMuon", triggers["FR_1mu_noiso_smpd"]) )

# make MC
mcTriggers = sum((trigs for (pd,trigs) in DatasetsAndTriggers), [])
if getHeppyOption('applyTriggersInMC'):
    for comp in mcSamples:
        comp.triggers = mcTriggers

# make data
dataSamples = []; vetoTriggers = []
for pd, trigs in DatasetsAndTriggers:
    if not trigs: continue
    for comp in byCompName(allData, [pd]):
        comp.triggers = trigs[:]
        comp.vetoTriggers = vetoTriggers[:]
        dataSamples.append(comp)
    vetoTriggers += trigs[:]

selectedComponents = mcSamples + dataSamples
if getHeppyOption('selectComponents'):
    selectedComponents = byCompName(selectedComponents, getHeppyOption('selectComponents').split(","))
autoAAA(selectedComponents, quiet=not(getHeppyOption("verboseAAA",False)))
configureSplittingFromTime(selectedComponents,100 if preprocessor else 10,4)
selectedComponents, _ = mergeExtensions(selectedComponents)

# create and set preprocessor if requested
if preprocessor:
    from CMGTools.Production.nanoAODPreprocessor import nanoAODPreprocessor
    preproc_cfg = {2016: ("mc94X2016","data94X2016"),
                   2017: ("mc94Xv2","data94Xv2"),
                   2018: ("mc102X","data102X_ABC","data102X_D")}
    preproc_cmsswArea = "/afs/cern.ch/user/p/peruzzi/work/cmgtools_tth/CMSSW_10_2_14"
    preproc_mc = nanoAODPreprocessor(cfg='%s/src/PhysicsTools/NanoAOD/test/%s_NANO.py'%(preproc_cmsswArea,preproc_cfg[year][0]),cmsswArea=preproc_cmsswArea,keepOutput=True)
    if year==2018:
        preproc_data_ABC = nanoAODPreprocessor(cfg='%s/src/PhysicsTools/NanoAOD/test/%s_NANO.py'%(preproc_cmsswArea,preproc_cfg[year][1]),cmsswArea=preproc_cmsswArea,keepOutput=True)
        preproc_data_D = nanoAODPreprocessor(cfg='%s/src/PhysicsTools/NanoAOD/test/%s_NANO.py'%(preproc_cmsswArea,preproc_cfg[year][2]),cmsswArea=preproc_cmsswArea,keepOutput=True)
        for comp in selectedComponents:
            if comp.isData:
                comp.preprocessor = preproc_data_D if '2018D' in comp.name else preproc_data_ABC
            else:
                comp.preprocessor = preproc_mc
    else:
        preproc_data = nanoAODPreprocessor(cfg='%s/src/PhysicsTools/NanoAOD/test/%s_NANO.py'%(preproc_cmsswArea,preproc_cfg[year][1]),cmsswArea=preproc_cmsswArea,keepOutput=True)
        for comp in selectedComponents:
            comp.preprocessor = preproc_data if comp.isData else preproc_mc
    if year==2017:
        preproc_mcv1 = nanoAODPreprocessor(cfg='%s/src/PhysicsTools/NanoAOD/test/%s_NANO.py'%(preproc_cmsswArea,"mc94Xv1"),cmsswArea=preproc_cmsswArea,keepOutput=True)
        for comp in selectedComponents:
            if comp.isMC and "Fall17MiniAODv2" not in comp.dataset:
                print "Warning: %s is MiniAOD v1, dataset %s" % (comp.name, comp.dataset)
                comp.preprocessor = preproc_mcv1
    if analysis == "frqcd":
        for comp in selectedComponents:
            comp.preprocessor._keepOutput = False
            comp.preprocessor._injectTriggerFilter = True
            comp.preprocessor._injectJSON = True
            if 'Mu' in comp.dataset:
                comp.preprocessor._cfgHasFilter = True
                comp.preprocessor._inlineCustomize = ("""
process.skim1Mu = cms.EDFilter("PATMuonRefSelector",
    src = cms.InputTag("slimmedMuons"),
    cut = cms.string("pt > %g && miniPFIsolation.chargedHadronIso < 0.45*pt && abs(dB('PV3D')) < 8*edB('PV3D')"),
    filter = cms.bool(True),
)
process.nanoAOD_step.insert(0, process.skim1Mu)
""" % (7.5 if "DoubleMuon" in comp.dataset else 4.5))
            elif 'QCD_Pt' in comp.dataset:
                comp.preprocessor._cfgHasFilter = True
                comp.preprocessor._inlineCustomize = ("""
process.skim1El = cms.EDFilter("PATElectronRefSelector",
    src = cms.InputTag("slimmedElectrons"),
    cut = cms.string("pt > 6 && miniPFIsolation.chargedHadronIso < 0.45*pt && abs(dB('PV3D')) < 8*edB('PV3D')"),
    filter = cms.bool(True),
)
process.nanoAOD_step.insert(0, process.skim1El)
""")
if analysis == "frqcd":
    cropToLumi(selectedComponents, 1.0)
    cropToLumi(byCompName(selectedComponents,["QCD"]), 0.3)
    cropToLumi(byCompName(selectedComponents,["QCD_Pt\d+to\d+$"]), 0.1)
    configureSplittingFromTime(selectedComponents, 10, 3, maxFiles=8)
    configureSplittingFromTime(byCompName(selectedComponents, ["EGamma","Single.*Run2017.*","SingleMuon_Run2018.*"]), 10, 4, maxFiles=12) 
    configureSplittingFromTime(byCompName(selectedComponents, ["WJ","TT","DY"]), 60, 3, maxFiles=6) 
    configureSplittingFromTime(byCompName(selectedComponents, [r"QCD_Pt\d+to\d+$","QCD.*EME"]), 60, 3, maxFiles=6) 


# print summary of components to process
if getHeppyOption("justSummary"): 
    printSummary(selectedComponents)
    sys.exit(0)

from CMGTools.TTHAnalysis.tools.nanoAOD.ttH_modules import *

from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

# in the cut string, keep only the main cuts to have it simpler
modules = ttH_sequence_step1
cut = ttH_skim_cut
compression = "ZLIB:3" #"LZ4:4" #"LZMA:9"
branchsel_in = os.environ['CMSSW_BASE']+"/src/CMGTools/TTHAnalysis/python/tools/nanoAOD/branchsel_in.txt"
branchsel_out = None

if analysis == "frqcd":
    modules = ttH_sequence_step1_FR
    cut = ttH_skim_cut_FR
    compression = "LZMA:9"
    branchsel_out = os.environ['CMSSW_BASE']+"/src/CMGTools/TTHAnalysis/python/plotter/ttH-multilepton/qcd1l-skim-ec.txt"

POSTPROCESSOR = PostProcessor(None, [], modules = modules,
        cut = cut, prefetch = True, longTermCache = True,
        branchsel = branchsel_in, outputbranchsel = branchsel_out, compression = compression)

test = getHeppyOption("test")
if test == "94X-MC":
    TTLep_pow = kreator.makeMCComponent("TTLep_pow", "/TTTo2L2Nu_mtop166p5_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1/MINIAODSIM", "CMS", ".*root", 831.76*((3*0.108)**2) )
    TTLep_pow.files = ["/afs/cern.ch/user/g/gpetrucc/cmg/NanoAOD_94X_TTLep.root"]
    lepSkim.requireSameSignPair = False
    lepSkim.minJets = 0
    lepSkim.minMET = 0
    lepSkim.prescaleFactor = 0
    selectedComponents = [TTLep_pow]
elif test == "94X-MC-miniAOD":
    TTLep_pow = kreator.makeMCComponent("TTLep_pow", "/TTTo2L2Nu_mtop166p5_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1/MINIAODSIM", "CMS", ".*root", 831.76*((3*0.108)**2) )
    TTLep_pow.files = [ 'root://cms-xrd-global.cern.ch//store/mc/RunIIFall17MiniAOD/TTTo2L2Nu_mtop166p5_TuneCP5_PSweights_13TeV-powheg-pythia8/MINIAODSIM/94X_mc2017_realistic_v10-v1/70000/3CC234EB-44E0-E711-904F-FA163E0DF774.root' ]
    localfile = os.path.expandvars("/tmp/$USER/%s" % os.path.basename(TTLep_pow.files[0]))
    if os.path.exists(localfile): TTLep_pow.files = [ localfile ] 
    from CMGTools.Production.nanoAODPreprocessor import nanoAODPreprocessor
    TTLep_pow.preprocessor = nanoAODPreprocessor("/afs/cern.ch/work/g/gpetrucc/ttH/CMSSW_10_4_0/src/nanov4_NANO_cfg.py")
    selectedComponents = [TTLep_pow]
elif test == "102X-MC":
    TTLep_pow = kreator.makeMCComponent("TTLep_pow", "/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM", "CMS", ".*root", 831.76*((3*0.108)**2), useAAA=True )
    TTLep_pow.files = TTLep_pow.files[:1]
    selectedComponents = [TTLep_pow]
elif test in ('2','3','3s'):
    doTestN(test, selectedComponents)
