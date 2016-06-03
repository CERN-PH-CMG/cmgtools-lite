# here we set all crab options that are not fixed
# values we'll be taken from environment variables set in launchall.py
# fixed options will be taken from heppy_crab_config.py

import imp
file = open( "heppy_crab_config.py", 'r' )
cfg = imp.load_source( 'cfg', "heppy_crab_config.py", file)
config = cfg.config
import os
import re
dataset=os.environ["CMG_DATASET"]
datasetname=os.environ["CMG_COMPONENT_NAME"]
m=re.match("\/(.*)\/(.*)\/(.*)",dataset)
if not m : 
  print "NO GOOD DATASET"

sample=m.group(1)+"_"+m.group(2)
print "sample = ",sample


#NJOBS=int(os.environ["NJOBS"])
production_label = os.environ["CMG_PROD_LABEL"]
cmg_version = os.environ["CMG_VERSION"]
config.Data.unitsPerJob = int(os.environ["CMG_UNITS_PER_JOB"])
if "CMG_TOTAL_UNITS" in os.environ:
  config.Data.totalUnits = int(os.environ["CMG_TOTAL_UNITS"])

config.Data.inputDataset = dataset
config.Data.publishDataName = m.group(2)+"_"+production_label
lumiMask =  os.environ["CMG_LUMI_MASK"]
if lumiMask != "None":
  config.Data.lumiMask = lumiMask
print "Using lumiMask: %s"%lumiMask
#config.Data.publishDataName += "_"+sample
print "Will send dataset", dataset , "with", config.Data.unitsPerJob, " files / jobs"

#config.General.requestName = sample + "_" + cmg_version # task name
config.General.requestName = production_label+"_"+cmg_version # task name
config.General.workArea = 'crab_' + production_label + "_" + sample # crab dir name

## this will divide task in *exactly* NJOBS jobs (for this we need JobType.pluginName = 'PrivateMC' and Data.splitting = 'EventBased')
#config.Data.unitsPerJob = 10
#config.Data.totalUnits = config.Data.unitsPerJob * NJOBS

## arguments to pass to scriptExe. They have to be like "arg=value". 
#config.JobType.scriptArgs = ["dataset="+dataset, "total="+str(NJOBS), "useAAA="+str(useAAA)]
config.JobType.scriptArgs = ["datasetname="+datasetname]

## output will be .../$outLFN/$PRIMARY_DS/$PUBLISH_NAME/$TIMESTAMP/$COUNTER/$FILENAME
## https://twiki.cern.ch/twiki/bin/view/CMSPublic/Crab3DataHandling
#config.Data.outLFNDirBase += '/babies/' + cmg_version
#config.Data.outLFNDirBase = config.Data.outLFNDirBase.replace("/adamwo","/adamw")
#config.Data.primaryDataset =  production_label
#config.Data.publishDataName = dataset
##final output: /store/user/$USER/babies/cmg_version/production_label/dataset/150313_114158/0000/foo.b

config.JobType.inputFiles.append("sample_"+datasetname+".pkl")

if "INPUT_DBS" in os.environ:
  config.Data.inputDBS = os.environ["INPUT_DBS"]

## if NEVENTS variable is set then only nevents will be run
#try: 
#    NEVENTS
#except NameError:
#    pass
#else:
#    config.JobType.scriptArgs += ["nevents="+str(NEVENTS)]

