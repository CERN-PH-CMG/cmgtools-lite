import os, sys, re

def _filterSamples(samples,args):
    selsamples = []
    use_regexp = ( "--re" in args or "--regexp" in args or "--regex" in args)
    noext = ("--noext" in args)
    realargs = [ a for a in args if not(a.startswith("--")) ]
    if len(realargs) > 2:
        for x in realargs[2:]:
            regexp = re.compile(x if use_regexp else re.escape(x))
            for s in samples:
                if re.search(regexp, s.name) and s not in selsamples:
                    if noext and "_ext" in s.name: 
                        continue
                    selsamples.append(s)
    else:
        selsamples = samples
    return selsamples

def runMain(samples,args=None,localobjs=None):
   if args == None: args = sys.argv
   selsamples = _filterSamples(samples,args)
   if "help" in args or "--help" in args or "-h" in args:
       print """

python samplefile.py test [--AAA] [samples] :
        tries accessing the first file of each sample
        option -AAA: allow AAA as fallback

python samplefile.py locality [samples] :
        check the locality of the samples

python samplefile.py refresh [samples] [ --pretend ] [ --suspicious ]: 
        forces a refresh of the cache
        option --pretend: print the list of samples to refresh, instead of actually refreshing them
        option --suspicious: selects for refresh the samples that look bogus (zero files, or zero events for official CMS datasets)

python samplefile.py list [samples]:  
python samplefile.py summary [samples]:   
        two equivalent commands that prints a list of samples, with number of files, events, equivalent luminosity, etc

python samplefile.py genXSecAna [samples] [ --pretend ] [ --verbose ] [ --AAA ]:  
        check the cross sections using genXSecAna on one of the files

python samplefile.py checkdecl:  
        check that all samples are declared in the samples list

"""
   if "test" in args:
       from CMGTools.RootTools.samples.ComponentCreator import testSamples
       testSamples(selsamples, allowAAA=("--AAA" in args))
   if "locality" in args:
       import re
       from CMGTools.Production.localityChecker import LocalityChecker
       tier2CheckerMini = LocalityChecker("T2_CH_CERN", datasets="/*/*/MINIAOD*")
       tier2CheckerNano = LocalityChecker("T2_CH_CERN", datasets="/*/*/NANOAOD*")
       for comp in selsamples:
           if len(comp.files) == 0: 
               print '\033[34mE: Empty component: '+comp.name+'\033[0m'
               continue
           if not hasattr(comp,'dataset'): continue
           if "/store/" not in comp.files[0]: continue
           if re.search("/store/(group|user|cmst3)/", comp.files[0]): continue
           if re.match("/[^/]+/[^/]+/MINIAOD(SIM)?", comp.dataset):
                tier2Checker = tier2CheckerMini
           elif re.match("/[^/]+/[^/]+/NANOAOD(SIM)?", comp.dataset):
                tier2Checker = tier2CheckerNano
           else:
                continue
           if not tier2Checker.available(comp.dataset):
               print "\033[1;31mN: Dataset %s (%s) is not available on T2_CH_CERN\033[0m" % (comp.name,comp.dataset)
           else: print "Y: Dataset %s (%s) is available on T2_CH_CERN" % (comp.name,comp.dataset)
   if "refresh" in args:
        from CMGTools.Production.cacheChecker import CacheChecker
        checker = CacheChecker()
        for d in selsamples:
            if "--suspicious" in args:
                if len(d.files) > 0:
                    if "/store/mc " in d.files[0] or "/store/data" in d.files[0]:
                        if getattr(d, 'dataset_entries', -1) > 0:
                            continue
                    else:
                        continue
            print "Checking ",d.name," aka ",d.dataset
            if "--pretend" in args: continue
            checker.checkComp(d, verbose=True)
   if "check_versions" in args:
        from CMGTools.Production.datasetVersionChecker import DatasetVersionChecker
        checker = DatasetVersionChecker()
        for d in selsamples:
            if "--pretend" in args: 
                print "Would check ",d.name," aka ",d.dataset
            else:
                print "Checking",d.name," ",
                checker.checkComp(d, verbose=True)
   if "list" in args or "summary" in args:
        from CMGTools.RootTools.samples.configTools import printSummary, mergeExtensions
        if "--merge-extensions" in args or "--mex" in args:
            selsamples = mergeExtensions(selsamples, verbose=True)[0]
        printSummary(selsamples)
   if "genXSecAna" in args:
        import subprocess, re;
        if "--fetch" in args or not os.path.exists("%s/src/genXSecAna.py" % os.environ['CMSSW_BASE']):
            print "Retrieving genXSecAna.py"
            os.system("wget -O "+os.environ['CMSSW_BASE']+"/src/genXSecAna.py  https://raw.githubusercontent.com/syuvivida/generator/master/cross_section/runJob/ana.py")
        for d in selsamples:
            if not hasattr(d, 'xSection'): 
                print "Skipping %s which has no cross section" % d.name
                continue
            if "--pretend" in args: 
                print "Would check ",d.name," aka ",d.dataset
                continue
            if "--AAA" in args:
                from CMGTools.Production.changeComponentAccessMode import convertComponent
                convertComponent(d, "root://cms-xrd-global.cern.ch/%s")
            else: # use LFNs
                d.files = [ re.sub(".*(/store/.*)(?:\\?.*)?","\\1",f) for f in d.files[:] ]
            print "Sample %s: XS(sample file) = %g pb, ... " % (d.name,d.xSection),
            if len(d.files) == 0: 
                print "\n\033[01;31m ERROR: no files in sample, so cannot run the analyzer \033[00m"
                continue
            if "--verbose" in args: 
                print "\n ".join(["cmsRun", os.environ['CMSSW_BASE']+"/src/genXSecAna.py", "inputFiles=%s" % d.files[0], "maxEvents=-1"])
            xsecAnaOut = subprocess.check_output(["cmsRun", os.environ['CMSSW_BASE']+"/src/genXSecAna.py", "inputFiles=%s" % d.files[0], "maxEvents=-1"], stderr=subprocess.STDOUT)
            if "--verbose" in args: 
                for l in xsecAnaOut.split("\n"): print "\t>> "+l
            m = re.search(r"After filter: final cross section = (\S+) \+- (\S+) pb", xsecAnaOut)
            if m and float(m.group(1)) == 0:
                m  = re.search(r"Before matching: total cross section = (\S+) \+- (\S+) pb", xsecAnaOut)
                m1 = re.search(r"After matching: total cross section = (\S+) \+- (\S+) pb", xsecAnaOut)
                if m1 and m and float(m1.group(1)) < 0 and float(m.group(1)) > 0 and abs(float(m1.group(1))/float(m.group(1))+1)<1e-2:
                    print "\033[01;33m [after filter Xsec is zero, using before filter one] \033[00m"
                else: m = None
            if not m or float(m.group(1)) <= 0:
                print "\n\033[01;31m ERROR: could not find After filter cross section in the output, or it's zero. \033[00m"
                continue
            xs, xserr = float(m.group(1)), float(m.group(2))
            kfactor = d.xSection/xs
            if abs(xs-d.xSection) < min(3*xserr,1e-2*xs): (col,stat) = '\033[01;36m', "OK"
            elif 0.8 < kfactor and kfactor < 1.4: (col,stat) = '\033[01;36m', "OK?" 
            elif 0.5 < kfactor and kfactor < 2.0: (col,stat) = '\033[01;33m', "WARNING" 
            else:                                 (col,stat) = '\033[01;31m', "ERROR"
            m = re.search(r"After filter: final fraction of events with negative weights = (\S+) \+- (\S+)", xsecAnaOut)
            if m:
                fnegv, fnegerr =  (float(m.group(1)), float(m.group(2)))
                fneg = "  f(negw): %.3f +- %.3f " % (fnegv, fnegerr)
                if getattr(d,'fracNegWeights',None) != None:
                    if abs(d.fracNegWeights - fnegv) < 0.02:
                        fneg += "(%.3f in sample file, \033[01;36mOK\033[00m)" % d.fracNegWeights
                    else:
                        fneg += "(%.3f in sample file, \033[01;33mWARNING\033[00m)" % d.fracNegWeights
            else: fneg = ""
            print "XS(genAnalyzer) = %g +/- %g pb : %s kFactor = %g %s\033[00m%s" % (xs, xserr, col, kfactor, stat, fneg)
   if "hasfnegw" in args:
        for d in selsamples:
            dataset = getattr(d, 'dataset', None)
            if not dataset or len(dataset.split("/")) != 4: 
                continue
            if "amcatnlo" in dataset or "FXFX" in dataset:
                if not hasattr(d, 'xSection'): 
                    print "Skipping %s which has no cross section" % d.name
                    continue
                if getattr(d, 'fracNegWeights', None) == None:
                    print "WARNING: no fracNegWeights for component %s dataset %s" % (d.name, dataset)
   if "checkdecl" in args:
        if localobjs == None: raise RuntimeError("you have to runMain(samples,localobjs=locals())")
        import PhysicsTools.HeppyCore.framework.config as cfg
        ok = 0
        for name,obj in localobjs.iteritems():
            if name == "comp": continue # local variable used in loops
            if isinstance(obj, cfg.Component):  
                if obj not in samples:
                    print "\tERROR: component %s is not added to the samples list " % name
                elif obj.name != name:
                    print "\tERROR: component %s has inconsistent name %s " % (name, obj.name)
                else:
                    ok += 1
        print "\tINFO: %d correctly declared components" % ok
        found_datasets = {}
        for comp in samples:
            dataset = getattr(comp, 'dataset', None)
            if not dataset or len(dataset.split("/")) != 4: 
                continue
            if dataset in found_datasets: 
                print "WARNING: components %s and %s share the same dataset %s" % (comp.name, found_datasets[dataset], dataset)
            else:
                found_datasets[dataset] = comp.name
