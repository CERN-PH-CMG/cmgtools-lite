import os
import PhysicsTools.HeppyCore.framework.config as cfg
from PhysicsTools.HeppyCore.framework.config     import printComps
from PhysicsTools.HeppyCore.framework.heppy_loop import getHeppyOption
from PhysicsTools.Heppy.utils.cmsswPreprocessor  import CmsswPreprocessor

# Tau-tau analyzers
from CMGTools.H2TauTau.proto.analyzers.FileCleaner                import FileCleaner
from CMGTools.H2TauTau.proto.analyzers.TauTauAnalyzer             import TauTauAnalyzer
from CMGTools.H2TauTau.proto.analyzers.H2TauTauTreeProducerTauTau import H2TauTauTreeProducerTauTau
from CMGTools.H2TauTau.proto.analyzers.TauDecayModeWeighter       import TauDecayModeWeighter
from CMGTools.H2TauTau.proto.analyzers.LeptonWeighter             import LeptonWeighter
from CMGTools.H2TauTau.proto.analyzers.TauP4Scaler                import TauP4Scaler
from CMGTools.H2TauTau.proto.analyzers.SVfitProducer              import SVfitProducer
from CMGTools.H2TauTau.proto.analyzers.L1TriggerAnalyzer          import L1TriggerAnalyzer

# common configuration and sequence
from CMGTools.H2TauTau.htt_ntuple_base_cff import commonSequence, genAna, dyJetsFakeAna, puFileData, puFileMC, eventSelector, susyCounter, skimAna

# Get all heppy options; set via '-o production' or '-o production=True'

# production = True run on batch, production = False (or unset) run locally
production = getHeppyOption('production')
production = False

# local switches
syncntuple    = False
computeSVfit  = False
pick_events   = False
cmssw         = False
calibrateTaus = False
data          = True

dyJetsFakeAna.channel = 'tt'

### Define tau-tau specific modules

tauP4Scaler = cfg.Analyzer(
  class_object = TauP4Scaler  ,
  name         = 'TauP4Scaler',
)


tauTauAna = cfg.Analyzer(
  class_object        = TauTauAnalyzer                     ,
  name                = 'TauTauAnalyzer'                   ,
  pt1                 = 40.                                ,
  eta1                = 2.1                                ,
  iso1                = 1.                                 ,
  looseiso1           = 999999999.                         ,
  pt2                 = 40.                                ,
  eta2                = 2.1                                ,
  iso2                = 1.                                 ,
  looseiso2           = 999999999.                         ,
  isolation           = 'byIsolationMVArun2v1DBoldDMwLTraw',
  m_min               = 10                                 ,
  m_max               = 99999                              ,
  dR_min              = 0.5                                ,
  jetPt               = 30.                                ,
  jetEta              = 4.7                                ,
  relaxJetId          = False                              ,
  verbose             = False                              ,
  from_single_objects = False                              ,
  scaleTaus           = calibrateTaus                      ,
  )

if not cmssw:
  tauTauAna.from_single_objects = True

from CMGTools.H2TauTau.proto.analyzers.MT2Analyzer import MT2Analyzer
tauTauMT2Ana = cfg.Analyzer(
    MT2Analyzer, name = 'MT2Analyzer',
    metCollection     = "slimmedMETs",
    doOnlyDefault = False,
    jetPt = 40.,
    collectionPostFix = "",
    verbose = True
    )

l1Ana = cfg.Analyzer(
    class_object=L1TriggerAnalyzer,
    name='L1TriggerAnalyzer',
    collections=['IsoTau'],
    requireMatches=['leg1', 'leg2'],
    dR=0.5
)

fileCleaner = cfg.Analyzer(
  FileCleaner         ,
  name = 'FileCleaner'
)

# tau1Calibration = cfg.Analyzer(
#   TauP4Scaler       ,
#   'TauP4Scaler_tau1',
#   leg      = 'leg1' ,
#   method   = 'peak' ,
#   scaleMET = True   ,
#   verbose  = False  ,
#   )

# tau2Calibration = cfg.Analyzer(
#   TauP4Scaler       ,
#   'TauP4Scaler_tau2',
#   leg      = 'leg2' ,
#   method   = 'peak' ,
#   scaleMET = True   ,
#   verbose  = False  ,
#   )

tauDecayModeWeighter = cfg.Analyzer(
  TauDecayModeWeighter   ,
  name='TauDecayModeWeighter' ,
  legs = ['leg1', 'leg2'],
  )

tau1Weighter = cfg.Analyzer(
  LeptonWeighter                    ,
  name        ='LeptonWeighter_tau1',
  scaleFactorFiles = {
      'trigger'     : '$CMSSW_BASE/src/CMGTools/H2TauTau/data/Tau_diTau35_fall15.py'     , # include in the event's overall weight
  },

  otherScaleFactorFiles = {
      'trigger_up'  : '$CMSSW_BASE/src/CMGTools/H2TauTau/data/Tau_diTau35_fall15_up.py'  , # DO NOT include in the event's overall weight
      'trigger_down': '$CMSSW_BASE/src/CMGTools/H2TauTau/data/Tau_diTau35_fall15_down.py', # DO NOT include in the event's overall weight
  },
  lepton      = 'leg1'              ,
  verbose     = True                ,
  disable     = False               ,
  )

tau2Weighter = cfg.Analyzer(
  LeptonWeighter                    ,
  name        ='LeptonWeighter_tau2',
  scaleFactorFiles = {
      'trigger'     : '$CMSSW_BASE/src/CMGTools/H2TauTau/data/Tau_diTau35_fall15.py'     , # include in the event's overall weight
  },

  otherScaleFactorFiles = {
      'trigger_up'  : '$CMSSW_BASE/src/CMGTools/H2TauTau/data/Tau_diTau35_fall15_up.py'  , # DO NOT include in the event's overall weight
      'trigger_down': '$CMSSW_BASE/src/CMGTools/H2TauTau/data/Tau_diTau35_fall15_down.py', # DO NOT include in the event's overall weight
  },
  lepton      = 'leg2'              ,
  verbose     = True                ,
  disable     = False               ,
  )

treeProducer = cfg.Analyzer(
  H2TauTauTreeProducerTauTau         ,
  name = 'H2TauTauTreeProducerTauTau'
  )

syncTreeProducer = cfg.Analyzer(
  H2TauTauTreeProducerTauTau                     ,
  name         = 'H2TauTauSyncTreeProducerTauTau',
  varStyle     = 'sync'                          ,
  #skimFunction = 'event.isSignal' #don't cut out any events from the sync tuple
  )

svfitProducer = cfg.Analyzer(
  SVfitProducer,
  name                       = 'SVfitProducer',
  integration                = 'MarkovChain'  , # 'VEGAS'
  integrateOverVisPtResponse = False          ,
  visPtResponseFile          = os.environ['CMSSW_BASE']+'/src/CMGTools/SVfitStandalone/data/svFitVisMassAndPtResolutionPDF.root', # Christian's for uncalibrated taus
  verbose                    = False          ,
  l1type                     = 'tau'          ,
  l2type                     = 'tau'
  )

###################################################
### CONNECT SAMPLES TO THEIR ALIASES AND FILES  ###
###################################################
from CMGTools.RootTools.utils.splitFactor import splitFactor
from CMGTools.H2TauTau.proto.samples.data15.data import data_tau
from CMGTools.H2TauTau.proto.samples.fall15.htt_common import backgrounds, sm_signals, mssm_signals, data_tau, sync_list
from CMGTools.H2TauTau.proto.samples.fall15.higgs_susy import HiggsSUSYGG160 as ggh160
from CMGTools.H2TauTau.proto.samples.fall15.higgs_susy import HiggsSUSYGG90 as ggh90
from CMGTools.H2TauTau.proto.samples.fall15.higgs_susy import HiggsSUSYGG1000 as ggh1000
from CMGTools.H2TauTau.proto.samples.fall15.triggers_tauTau import mc_triggers, mc_triggerfilters, data_triggers, data_triggerfilters

data_list = data_tau
samples = backgrounds + sm_signals + mssm_signals
split_factor = 1e5

for sample in data_list:
    sample.triggers = data_triggers
    sample.triggerobjects = data_triggerfilters
    sample.splitFactor = splitFactor(sample, split_factor)
    sample.json = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Cert_246908-260627_13TeV_PromptReco_Collisions15_25ns_JSON_v2.txt'
    sample.lumi = 2260.

for sample in samples:
    sample.triggers = mc_triggers
    sample.triggerobjects = mc_triggerfilters
    sample.splitFactor = splitFactor(sample, split_factor)

###################################################
###              ASSIGN PU to MC                ###
###################################################
for mc in samples:
    mc.puFileData = puFileData
    mc.puFileMC   = puFileMC

###################################################
###             SET COMPONENTS BY HAND          ###
###################################################
selectedComponents = samples
if data:
  selectedComponents = data_list

###################################################
###                  SEQUENCE                   ###
###################################################
sequence = commonSequence
if calibrateTaus:
    sequence.insert(sequence.index(genAna), tauP4Scaler)
sequence.insert(sequence.index(genAna), tauTauAna)
sequence.insert(sequence.index(genAna), l1Ana)
# sequence.append(tau1Calibration)
# sequence.append(tau2Calibration)
sequence.append(tauDecayModeWeighter)
sequence.append(tau1Weighter)
sequence.append(tau2Weighter)
sequence.append(tauTauMT2Ana)
sequence.insert(sequence.index(skimAna), susyCounter)
if computeSVfit:
    sequence.append(svfitProducer)
sequence.append(treeProducer)
if syncntuple:
    sequence.append(syncTreeProducer)
if not cmssw:
    module = [s for s in sequence if s.name == 'MCWeighter'][0]
    sequence.remove(module)

###################################################
###             CHERRY PICK EVENTS              ###
###################################################
if pick_events:

#     import csv
#     fileName = '/afs/cern.ch/work/m/manzoni/diTau2015/CMSSW_7_4_3/src/CMGTools/H2TauTau/cfgPython/2015-sync/Imperial.csv'
# #     fileName = '/afs/cern.ch/work/m/manzoni/diTau2015/CMSSW_7_4_3/src/CMGTools/H2TauTau/cfgPython/2015-sync/CERN.csv'
#     f = open(fileName, 'rb')
#     reader = csv.reader(f)
    evtsToPick = [158340]

    # for i, row in enumerate(reader):
    #     evtsToPick += [int(j) for j in row]

    eventSelector.toSelect = evtsToPick
    sequence.insert(0, eventSelector)

## output histogram
outputService=[]
from PhysicsTools.HeppyCore.framework.services.tfile import TFileService
output_service = cfg.Service(
    TFileService,
    'outputfile',
    name="outputfile",
    fname='testtree.root',
    option='recreate'
    )    
outputService.append(output_service)

###################################################
###            SET BATCH OR LOCAL               ###
###################################################
if not production:
  # comp                 = ggh160
  comp                 = data_list[0]
  selectedComponents   = [comp]
  comp.splitFactor     = 1
  comp.fineSplitFactor = 1
  #comp.files           = ['/afs/cern.ch/work/m/mzeinali/public/020136C0-B12B-E611-8695-00145EFC5B60.root']
  comp.files           = comp.files[:1]
    
preprocessor = None
if cmssw:
    sequence.append(fileCleaner)
    cfg_name = "$CMSSW_BASE/src/CMGTools/H2TauTau/prod/h2TauTauMiniAOD_ditau_data_cfg.py" if data else "$CMSSW_BASE/src/CMGTools/H2TauTau/prod/h2TauTauMiniAOD_ditau_cfg.py"
    preprocessor = CmsswPreprocessor(cfg_name, addOrigAsSecondary=False)

# the following is declared in case this cfg is used in input to the
# heppy.py script
from PhysicsTools.HeppyCore.framework.eventsfwlite import Events
config = cfg.Config( components   = selectedComponents,
                     sequence     = sequence          ,
                     #services     = []                ,
		     services = outputService, 
                     preprocessor = preprocessor      ,
                     events_class = Events
                     )

printComps(config.components, True)
