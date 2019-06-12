from __future__ import print_function
import os, subprocess, time, hashlib

def _stripv(x):
    return x[:-len("_v*")] if x.endswith("_v*") else x
class nanoAODPreprocessor:
    def __init__(self, cfg, cmsswArea=None, outputModuleName=None, name="preprocessor", outputFileName="cmsswPreProcessing.root", keepOutput=False, injectTriggerFilter=False, injectJSON=False, inlineCustomize=None, cfgHasFilter=False, nanoStep="nanoAOD_step"):
        if not os.path.isfile(cfg): 
            raise RuntimeError("Preprocessor created for non-existing cfg file %r" % cfg)
        self._cfg = cfg
        self._cmsswArea = cmsswArea if cmsswArea else os.environ['CMSSW_BASE']
        self._outputModuleName = outputModuleName
        self._outputFileName = outputFileName
        self._keepOutput = keepOutput
        self._injectTriggerFilter = injectTriggerFilter
        self._injectJSON = injectJSON
        self._inlineCustomize = inlineCustomize
        self._nanoStep = nanoStep
        self._cfgHasFilter = cfgHasFilter
        self._name = name
    def clone(self, **kwargs):
        import copy
        ret = copy.copy(self)
        for k,v in kwargs.items():
            if not hasattr(self, "_"+k): raise RuntimeError("No parameter %s to be modified" % k)
            setattr(ret, "_"+k, v)
        return ret
    def prefetchFile(self, fname, longTermCache=False, verbose=True):
        tmpdir = os.environ['TMPDIR'] if 'TMPDIR' in os.environ else "/tmp"
        if not fname.startswith("root://"):
            return fname, False
        rndchars  = "".join([hex(ord(i))[2:] for i in os.urandom(8)]) if not longTermCache else "long_cache-id%d-%s" % (os.getuid(), hashlib.sha1(fname).hexdigest());
        localfile = "%s/%s-%s.root" % (tmpdir, os.path.basename(fname).replace(".root",""), rndchars)
        if longTermCache and os.path.exists(localfile):
            if verbose: print("Filename %s is already available in local path %s " % (fname,localfile))
            return localfile, False
        try:
            if verbose: print("Filename %s is remote, will do a copy to local path %s " % (fname,localfile))
            start = time.clock()
            subprocess.check_output(["xrdcp","-f","-N",fname,localfile])
            if verbose: print("Time used for transferring the file locally: %s s" % (time.clock() - start))
            return localfile, (not longTermCache)
        except:
            if verbose: print("Error: could not save file locally, will run from remote" )
            if os.path.exists(localfile):
                if verbose: print("Deleting partially transferred file %s" % localfile)
                try:
                    os.unlink(localfile)
                except:
                    pass
            return fname, False
    def preProcessComponent(self, comp, outdir, maxEntries, noSubDir=False, verbose=False, prefetch=False, longTermCache=False):
        if verbose: print("Pre-processing component %s (%d files) with %s" % (comp.name, len(comp.files), self._cfg))
        workingDir = outdir if noSubDir else os.path.join(outdir, comp.name)
        subprocess.check_output(["mkdir","-p", workingDir])
        if not os.path.isdir(workingDir): raise RuntimeError("Can't create preprocessor working directory: "+comp)
        # make list of temporary files to be deleted later
        self.toDelete = getattr(self, 'toDelete', [])
        # possible prefetch
        if prefetch:
            files = []
            for fname in comp.files:
                ftoread, toBeDeleted = self.prefetchFile(fname, verbose=verbose, longTermCache=longTermCache)
                files.append(ftoread)
                if toBeDeleted: self.toDelete.append(ftoread)
        else:
            files = comp.files[:]
        # make cfg file
        outputModuleName = self._outputModuleName if self._outputModuleName else ("NANOAODSIMoutput" if comp.isMC else "NANOAODoutput")
        cmsswCfg = open(os.path.join(workingDir, self._name+"_cfg.py"), "w")
        cmsswCfg.write("".join(open(self._cfg, "r")))
        cmsswCfg.write("\n### === POSTFIX ====\n")
        cmsswCfg.write("process.source.fileNames = %r\n" % [ str("file:"+f if os.path.isfile(f) else f) for f in files])
        cmsswCfg.write("process.%s.fileName = %r\n" % (outputModuleName, self._outputFileName))
        cmsswCfg.write("process.maxEvents.input = %g\n" % (maxEntries if maxEntries else -1))
        cmsswCfg.write("process.MessageLogger.cerr.FwkReport.reportEvery = 100\n") 
        cmsswCfg.write("if hasattr(process,'options'): process.options.wantSummary = cms.untracked.bool(True)\n")
        hasFilter = self._cfgHasFilter
        if self._injectTriggerFilter and getattr(comp, 'triggers', []):
            cmsswCfg.write("## --- trigger bit filter ---\n")
            cmsswCfg.write("import HLTrigger.HLTfilters.triggerResultsFilter_cfi as hlt\n")
            cmsswCfg.write("""process.triggerFilter = hlt.triggerResultsFilter.clone(
    hltResults = "TriggerResults::HLT",
    triggerConditions =  %r ,
    l1tResults = '',
    throw = False
)\n""" % ( [ (_stripv(p)+"_v*") for p in comp.triggers ]))
            if getattr(comp, 'vetoTriggers', []):
                cmsswCfg.write("process.triggerFilterVeto = process.triggerFilter.clone(\n    triggerConditions = %r)\n" % ([ (_stripv(p)+"_v*") for p in comp.vetoTriggers ] ))
                cmsswCfg.write("process.%s.insert(0, process.triggerFilter + ~process.triggerFilterVeto)\n" % self._nanoStep)
            else:
                cmsswCfg.write("process.%s.insert(0, process.triggerFilter)\n" % self._nanoStep)
            hasFilter=True
        if self._injectJSON and getattr(comp, 'json', None):
            cmsswCfg.write("## --- json filter ---\n")
            cmsswCfg.write("import FWCore.PythonUtilities.LumiList as LumiList\n")
            cmsswCfg.write("process.source.lumisToProcess = LumiList.LumiList(filename = %r).getVLuminosityBlockRange()\n" % comp.json)
        if self._inlineCustomize:
            cmsswCfg.write("## --- inline customization\n")
            cmsswCfg.write(self._inlineCustomize+"\n")
        if hasFilter:
            cmsswCfg.write("process.%s.SelectEvents = cms.untracked.PSet( SelectEvents = cms.vstring('%s') )\n" % (outputModuleName, self._nanoStep))
            cmsswCfg.write("""
if hasattr(process, 'genWeightsTable') and process.{seq}.contains(process.genWeightsTable):
    process.{seq}.remove(process.genWeightsTable)
    process.{seq}.insert(0, process.genWeightsTable)
""".format(seq = self._nanoStep))
        cmsswCfg.close()
        # make script 
        scriptName = os.path.join(workingDir, self._name+".sh")
        scriptFile = open(scriptName, "w")
        scriptFile.write("#!/bin/bash\n")
        scriptFile.write("cd %s\neval $(scram runtime -sh)\ncd %s\n" % (self._cmsswArea, os.path.abspath(workingDir)))
        scriptFile.write("cmsRun %s_cfg.py 2>&1 | tee %s.log\n" % (self._name, self._name));
        if not verbose:
            scriptFile.write("gzip -9 %s.log\n" % (self._name))
        scriptFile.close()
        subprocess.check_output(["chmod","+x", scriptName])
        # run
        if verbose:
            t0 = time.clock()
            os.system(scriptName) # this sends the output also to the console
            print("Pre-processing component %s done after %s s" % (comp.name, time.clock()-t0))
        else:
            subprocess.check_output([scriptName])
        # return 
        ret = os.path.join(workingDir, self._outputFileName)
        if not self._keepOutput: self.toDelete.append(ret)
        return ret
    def doneProcessComponent(self, comp, outdir, noSubDir=False, verbose=True):
        for tmpfile in getattr(self, 'toDelete', []):
            if os.path.isfile(tmpfile):
                if verbose: print("removing temporary file %s from preprocessor" % tmpfile)
                os.unlink(tmpfile)


