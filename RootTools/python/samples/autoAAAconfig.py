def autoAAA(selectedComponents,quiet=False):
    import re, os
    from CMGTools.Production import changeComponentAccessMode
    from CMGTools.Production.localityChecker import LocalityChecker
    tier2CheckerMini = LocalityChecker("T2_CH_CERN", datasets="/*/*/MINIAOD*")
    tier2CheckerNano = LocalityChecker("T2_CH_CERN", datasets="/*/*/NANOAOD*")
    for comp in selectedComponents:
        if len(comp.files) == 0: print "ERROR, comp %s (dataset %s) has no files!" % (comp.name, getattr(comp,'dataset',None)); continue
        if not hasattr(comp,'dataset'): continue
        if "/store/" not in comp.files[0]: continue
        if re.search("/store/(group|user|cmst3)/", comp.files[0]): continue
        #if comp.isData and "PromptReco" in comp.dataset: continue
        if re.match("/[^/]+/[^/]+/MINIAOD(SIM)?", comp.dataset):
            tier2Checker = tier2CheckerMini
        elif re.match("/[^/]+/[^/]+/NANOAOD(SIM)?", comp.dataset):
            tier2Checker = tier2CheckerNano
        else:
            continue
        if not tier2Checker.available(comp.dataset):
            if not quiet: print "Dataset %s is not available, will use AAA" % comp.dataset
            changeComponentAccessMode.convertComponent(comp, "root://cms-xrd-global.cern.ch/%s")
            if 'X509_USER_PROXY' not in os.environ or "/afs/" not in os.environ['X509_USER_PROXY']:
                raise RuntimeError, "X509_USER_PROXY not defined or not pointing to /afs"
