from __future__ import print_function
import os, subprocess, time

class nanoAODPreprocessor:
    def __init__(self, cfg, cmsswArea=None, outputModuleName=None, name="preprocessor", outputFileName="cmsswPreProcessing.root", keepOutput=False):
        if not os.path.isfile(cfg): 
            raise RuntimeError("Preprocessor created for non-existing cfg file %r" % cfg)
        self._cfg = cfg
        self._cmsswArea = cmsswArea if cmsswArea else os.environ['CMSSW_BASE']
        self._outputModuleName = outputModuleName
        self._outputFileName = outputFileName
        self._keepOutput = keepOutput
        self._name = name
    def preProcessComponent(self, comp, outdir, maxEntries, verbose=True):
        if verbose: print("Pre-processing component %s (%d files) with %s" % (comp.name, len(comp.files), self._cfg))
        workingDir = os.path.join(outdir, comp.name)
        subprocess.check_output(["mkdir","-p", workingDir])
        if not os.path.isdir(workingDir): raise RuntimeError("Can't create preprocessor working directory: "+comp)
        # make cfg file
        outputModuleName = self._outputModuleName if self._outputModuleName else ("NANOAODSIMoutput" if comp.isMC else "NANOAODoutput")
        cmsswCfg = open(os.path.join(workingDir, self._name+"_cfg.py"), "w")
        cmsswCfg.write("".join(open(self._cfg, "r")))
        cmsswCfg.write("\n### === POSTFIX ====\n")
        cmsswCfg.write("process.source.fileNames = %r\n" % [ ("file:"+f if os.path.isfile(f) else f) for f in comp.files])
        cmsswCfg.write("process.%s.fileName = %r\n" % (outputModuleName, self._outputFileName))
        cmsswCfg.write("process.maxEvents.input = %g\n" % (maxEntries if maxEntries else -1))
        cmsswCfg.close()
        # make script 
        scriptName = os.path.join(workingDir, self._name+".sh")
        scriptFile = open(scriptName, "w")
        scriptFile.write("#!/bin/bash\n")
        scriptFile.write("cd %s\neval $(scram runtime -sh)\ncd %s\n" % (self._cmsswArea, os.path.abspath(workingDir)))
        scriptFile.write("cmsRun %s_cfg.py 2>&1 | tee %s.log\n" % (self._name, self._name));
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
        return os.path.join(workingDir, self._outputFileName)
    def doneProcessComponent(self, comp, outdir, verbose=True):
        if not self._keepOutput:
            tmpfile = os.path.join(outdir, comp.name, self._outputFileName)
            if os.path.isfile(tmpfile):
                if verbose: print("removing temporary file %s from preprocessor" % tmpfile)
                os.unlink(tmpfile)


