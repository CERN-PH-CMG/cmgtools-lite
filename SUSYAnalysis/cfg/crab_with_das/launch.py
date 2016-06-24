#! /usr/bin/env python
import imp, os, sys
from optparse import OptionParser

# datasets to run as defined from run_susyMT2.cfg
# number of jobs to run per dataset decided based on splitFactor and fineSplitFactor from cfg file
# in principle one only needs to modify the following two lines:

parser = OptionParser(usage="python launch.py [options] component1 [ component2 ...]", \
                          description="Launch heppy jobs with CRAB3. Components correspond to the variables defined in heppy_samples.py (their name attributes)")
parser.add_option("--production_label", dest="production_label", help="production label", default="heppy")
parser.add_option("--remoteDir", dest="remoteDir", help="remote subdirectory", default="")
parser.add_option("--cmg_version", dest="cmg_version", help="CMG version", \
                      default="CMGTools-from-CMSSW_7_4_7_LocalDevelopments")
parser.add_option("--unitsPerJob", dest="unitsPerJob", help="Nr. of units (files) / crab job", type="int", default=1)
parser.add_option("--totalUnits", dest="totalUnits", help="Total nr. of units (files)", type="int", default=None)
parser.add_option("--inputDBS", dest="inputDBS", help="dbs instance", default=None)
parser.add_option("--lumiMask", dest="lumiMask", help="lumi mask (for data)", default=None)
( options, args ) = parser.parse_args()

handle = open("heppy_samples.py", 'r')
cfo = imp.load_source("heppy_samples", "heppy_samples.py", handle)
handle.close()

import PhysicsTools.HeppyCore.framework.config as cfg
allComponents = { }
for d in cfo.__dict__:
    c = cfo.__dict__[d]
    if isinstance(c,cfg.Component):
        if c.name in allComponents:
            print "Ignoring duplicate component: variable name = ",d," component name = ",c.name
        allComponents[c.name] = c

selectedComponents = [ ]
for c in args:
    if c in allComponents:
        selectedComponents.append(allComponents[c])
    else:
        print "*** Skipping undefined component: ",c
if not selectedComponents:
    print "Did not find any matching component! Available components are"
    for c in sorted(allComponents.keys()):
        print "   ",c
    sys.exit(1)

os.system("scram runtime -sh")
os.system("source /cvmfs/cms.cern.ch/crab3/crab.sh")

os.environ["CMG_PROD_LABEL"]  = options.production_label
os.environ["CMG_REMOTE_DIR"]  = options.remoteDir
os.environ["CMG_VERSION"] = options.cmg_version
os.environ["CMG_UNITS_PER_JOB"] = str(options.unitsPerJob)
os.environ["CMG_LUMI_MASK"] = options.lumiMask if options.lumiMask else "None"
if options.totalUnits:
    os.environ["CMG_TOTAL_UNITS"] = str(options.totalUnits)
else:
    if "CMG_TOTAL_UNITS" in os.environ:
        del os.environ["CMG_TOTAL_UNITS"]
if options.inputDBS:
    os.environ["INPUT_DBS"] = options.inputDBS

#from PhysicsTools.HeppyCore.framework.heppy import split
import pickle
for comp in selectedComponents:
#    print "generating sample_"+comp.name+".pkl"
    print "Processing ",comp.name
    fout = open("sample_"+comp.name+".pkl","wb")
    pickle.dump(comp,fout)
    fout.close()
#    os.environ["DATASET"] = str(comp.name)
    os.environ["CMG_DATASET"] = comp.dataset
    if hasattr(comp, "json") and comp.json:
        os.environ["CMG_JSON"] = os.path.expandvars(comp.json)
    os.environ["CMG_COMPONENT_NAME"] = comp.name
#    os.system("python tmp.py > tmp.lis")
    os.system("which crab")
    os.system("crab submit -c heppy_crab_config_env.py")


#os.system("rm -f python.tar.gz")
#os.system("rm -f cmgdataset.tar.gz")
#os.system("rm -f cafpython.tar.gz")
