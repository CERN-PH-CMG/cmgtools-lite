#!/usr/bin/env python
from __future__ import print_function
import os, sys, imp, pickle, multiprocessing, types, json
from copy import copy
from math import ceil

def _loadHeppyGlobalOptions(options):
    from PhysicsTools.HeppyCore.framework.heppy_loop import _heppyGlobalOptions
    for opt in options.extraOptions:
        if "=" in opt:
            (key,val) = opt.split("=",1)
            _heppyGlobalOptions[key] = val
        else:
            _heppyGlobalOptions[opt] = True
    if options.optionFile:
        opt = json.load(open(options.optionFile, 'r'))
        for key,val in opt.iteritems(): 
            _heppyGlobalOptions[key] = val

def _processOneComponent(pp, comp, outdir, preprocessor, options):
    if not comp.files: return

    if isinstance(pp, str) or isinstance(pp, unicode):
        _loadHeppyGlobalOptions(options)
        cfo = imp.load_source(os.path.basename(pp).rstrip('.py'), pp, open(pp,'r'))
        pp = cfo.POSTPROCESSOR

    pp.postfix = "_nanopy"
    pp.noOut = options.noOut
    pp.justcount = options.justcount
    if options.prefetch is not None: 
        pp.prefetch = options.prefetch
    if options.longTermCache is not None: 
        pp.longTermCache = options.longTermCache
    if options.maxEntries: 
        pp.maxEntries = options.maxEntries
    fineSplit = getattr(comp, 'fineSplit', None)
    if fineSplit:
        if len(comp.files) != 1:
            raise RuntimeError("FineSplitting not supported for component %s with %d files" % (comp.name, len(comp.files)))
        fineSplitIndex, fineSplitFactor = fineSplit
        if fineSplitFactor <= 1:
            raise RuntimeError("FineSplitting not supported for component %s with %r fineSplitFactor" % (comp.name, fineSplitFactor))
        import ROOT
        ROOT.PyConfig.IgnoreCommandLineOptions = True
        tfile = ROOT.TFile.Open(comp.files[0])
        totEvents = min(tfile.Get("Events").GetEntries(), pp.maxEntries)
        tfile.Close()
        pp.maxEntries = int(ceil(totEvents/float(fineSplitFactor)))
        pp.firstEntry = fineSplitIndex * pp.maxEntries
        pp.postfix += "_fineSplit_%d" % fineSplitIndex

    preprocessor = getattr(comp, 'preprocessor', preprocessor)
    if preprocessor:
        if fineSplit: raise RuntimeError("FineSplitting not supported for component %s with preprocessor at the moment" % comp.name)
        comp.files = [ preprocessor.preProcessComponent(comp, outdir, options.maxEntries, options.single) ]
    
    # unwrap any module still wrapped by a lambda
    pp.modules = [ (m() if isinstance(m,types.FunctionType) else m) for m in pp.modules ]
    print("Processing component %s (%d files)" % (comp.name, len(comp.files)))
    # setting specific configuration for the modules, if needed
    for mod in pp.modules:
        if hasattr(mod, 'initComponent'): mod.initComponent(comp)
    # reading cut string (and apply trigger bits together with it) 
    cut = getattr(comp, 'cut', pp.cut)
    trigSel = getattr(comp, 'triggers', [])
    trigVeto = getattr(comp, 'vetoTriggers', [])
    if trigSel:
        cut = "(%s) && (%s)" % (cut if cut else 1, " || ".join(t.rstrip("_v*") for t in trigSel))
        if trigVeto: cut += " && !(%s)" % (" || ".join(t.rstrip("_v*") for t in trigVeto))
    elif trigVeto: raise RuntimeError("vetoTriggers specified without triggers for component %s" % comp.name)
    pp.cut = cut
    # input
    pp.inputFiles = comp.files[:]
    pp.json = getattr(comp, 'json', pp.json)
    # output
    pp.outputDir = outdir if (options.single or not preprocessor) else os.path.join(outdir, comp.name)
    target = os.path.join(pp.outputDir, comp.name + ".root")
    if len(pp.inputFiles) > 1: pp.haddFileName = target 
    # go and have fun
    pp.run()
    # clean up intermediate files if needed
    if len(pp.inputFiles) > 1:
        for f in pp.inputFiles:
            of = os.path.join(pp.outputDir, os.path.basename(f).replace(".root",pp.postfix+".root"))
            if os.path.isfile(of): 
                print("removing temporary file "+of)
                os.unlink(of)
    else:
        of = os.path.join(pp.outputDir, os.path.basename(pp.inputFiles[0]).replace(".root",pp.postfix+".root"))
        os.rename(of, target)
    if preprocessor:
        preprocessor.doneProcessComponent(comp, outdir, options.single)

def _processOneComponentAsync(args):
    try:
        _processOneComponent(*args)
    except Exception:
        import traceback
        print("ERROR processing component %s" % args[1].name)
        print(args[1])
        print("STACK TRACE: ")
        print(traceback.format_exc())
        raise

if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser(usage="%prog [options] outputDir inputCfg [ component ]")
    parser.add_option("--single",  dest="single", action="store_true",  default=False, help="Run on a single component, single-threaded, without creating subdirectories")
    parser.add_option("--prefetch", dest="prefetch", action="store_true",  default=None, help="Prefetch remote files with xrdcp (overrides what is in the cfg file)")
    parser.add_option("--no-prefetch", dest="prefetch", action="store_false",  default=None, help="Do not prefetch remote files with xrdcp (overrides what is in the cfg file)")
    parser.add_option("--long-term-cache", dest="longTermCache", action="store_true",  default=None, help="Keep prefetched files across runs (overrides what is in the cfg file)")
    parser.add_option("--no-long-term-cache", dest="longTermCache", action="store_false",  default=None, help="Keep prefetched files across runs (overrides what is in the cfg file)")
    parser.add_option("-N", "--nevents", "--max-entries", dest="maxEntries", type="long",  default=None, help="Maximum number of entries to process from any single given input tree")
    parser.add_option("-j", dest="ntasks", type="int",  default=4, help="Maximum number of entries to processes to run simultaneously")
    parser.add_option("--noout",  dest="noOut", action="store_true",  default=False, help="Do not produce output, just run modules")
    parser.add_option("--justcount",   dest="justcount", default=False, action="store_true",  help="Just report the number of selected events") 
    parser.add_option("-o", "--option", dest="extraOptions", type="string", action="append", default=[], help="Save one extra option (either a flag, or a key=value pair) that can be then accessed from the job config file")
    parser.add_option('--options', dest='optionFile', default=None, help='options specified as a json file')
    (options, args) = parser.parse_args()

    if len(args) < 2 :
	 parser.print_help()
         sys.exit(1)
    outdir = args[0] 

    # this must be done before calling the source
    _loadHeppyGlobalOptions(options)

    cfg = args[1]
    cfo = imp.load_source(os.path.basename(cfg).rstrip('.py'), cfg, open(cfg,'r'))
    pp = cfo.POSTPROCESSOR

    if len(args) == 2:
        components = cfo.selectedComponents
    else:
        components = [ pickle.load(open(arg, 'r')) for arg in args[2:] ]

    preprocessor = getattr(cfo, 'PREPROCESSOR', None)

    if options.single:
        if len(components) > 1: 
            print("WARNING: option --single specified but multiple components found")
        for comp in components:
            _processOneComponent(copy(pp), comp, outdir, preprocessor, options)

    else:
        from PhysicsTools.HeppyCore.framework.heppy_loop import split
        components = split(components)
        if options.ntasks == 0 or len(components) == 1: # single core, for debugging
            map(_processOneComponentAsync, [(copy(pp), comp, outdir, preprocessor, options) for comp in components ])
        else:
            pool = multiprocessing.Pool(processes=min(len(components),options.ntasks,multiprocessing.cpu_count()))
            pool.map(_processOneComponentAsync, [(cfg, comp, outdir, preprocessor, options) for comp in components ])
            pool.close()
            pool.join()
            del pool

    print("\nDone")
