import os, sys

def _filterSamples(samples,args):
    selsamples = []
    realargs = [ a for a in args if not(a.startswith("--")) ]
    if len(realargs) > 2:
        for x in realargs[2:]:
            for s in samples:
                if x in s.name and s not in selsamples:
                    selsamples.append(s)
    else:
        selsamples = samples
    return selsamples

def runMain(samples,args=None):
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


"""
   if "test" in args:
       from CMGTools.RootTools.samples.ComponentCreator import testSamples
       testSamples(selsamples, allowAAA=("--AAA" in args))
   if "locality" in args:
       import re
       from CMGTools.Production.localityChecker import LocalityChecker
       tier2Checker = LocalityChecker("T2_CH_CERN", datasets="/*/*/MINIAOD*")
       for comp in selsamples:
           if len(comp.files) == 0: 
               print '\033[34mE: Empty component: '+comp.name+'\033[0m'
               continue
           if not hasattr(comp,'dataset'): continue
           if not re.match("/[^/]+/[^/]+/MINIAOD(SIM)?", comp.dataset): continue
           if "/store/" not in comp.files[0]: continue
           if re.search("/store/(group|user|cmst3)/", comp.files[0]): continue
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
        from CMGTools.HToZZ4L.tools.configTools import printSummary
        dataSamples = samples
        printSummary(selsamples)

