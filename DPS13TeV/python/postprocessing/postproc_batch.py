#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from glob import glob
import re, pickle, math
from CMGTools.DPS13TeV.postprocessing.framework.postprocessor import PostProcessor

DEFAULT_MODULES = [##("CMGTools.DPS13TeV.postprocessing.examples.puWeightProducer", "puWeight,puWeightXsecup,puWeightXsecdown"),
                   ##("CMGTools.DPS13TeV.postprocessing.examples.lepSFProducer","lepSF,trgSF"),
                   ##("CMGTools.DPS13TeV.postprocessing.examples.lepVarProducer","eleRelIsoEA,lepQCDAwayJet,eleCalibrated"),
                   ("CMGTools.DPS13TeV.postprocessing.examples.jetReCleaner","jetReCleaner"),
                   ##("CMGTools.DPS13TeV.postprocessing.examples.genFriendProducer","genQEDJets"),
                   ##("CMGTools.DPS13TeV.postprocessing.examples.bdtWeigthsDPS_WZ_and_fakes","BDT_WZ_and_fakes"),
                   ]

RECOILTEST_MODULES=[("CMGTools.DPS13TeV.postprocessing.examples.puWeightProducer", "puWeight,puWeightXsecup,puWeightXsecdown"),
                    ("CMGTools.DPS13TeV.postprocessing.examples.lepSFProducer","lepSF,trgSF"),
                    ("CMGTools.DPS13TeV.postprocessing.examples.lepVarProducer","eleRelIsoEA,lepQCDAwayJet,eleCalibrated"),
                    ("CMGTools.DPS13TeV.postprocessing.examples.jetReCleaner","jetReCleaner"),
                    ("CMGTools.DPS13TeV.postprocessing.examples.genFriendProducer","genQEDJets"),
                    ("CMGTools.DPS13TeV.postprocessing.examples.eventRecoilAnalyzer","eventRecoilAnalyzer"),
                   ]

if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser(usage="%prog [options] inputDir outputDir")
    parser.add_option("-J", "--json",  dest="json", type="string", default=None, help="Select events using this JSON file")
    parser.add_option("-C", "--cut",  dest="cut", type="string", default=None, help="Cut string")
    parser.add_option("-b", "--branch-selection",  dest="branchsel", type="string", default=None, help="Branch selection")
    parser.add_option("--friend",  dest="friend", action="store_true", default=True, help="Produce friend trees in output (current default is to produce full trees)")
    parser.add_option("--full",  dest="friend", action="store_false",  default=False, help="Produce full trees in output (this is the current default)")
    parser.add_option("--noout",  dest="noOut", action="store_true",  default=False, help="Do not produce output, just run modules")
    parser.add_option("--justcount",   dest="justcount", default=False, action="store_true",  help="Just report the number of selected events") 
    parser.add_option("-I", "--import", dest="imports",  type="string", default=[], action="append", nargs=2, help="Import modules (python package, comma-separated list of ");
    parser.add_option("-z", "--compression",  dest="compression", type="string", default=("LZMA:9"), help="Compression: none, or (algo):(level) ")
    parser.add_option("-d", "--dataset", dest="datasets",  type="string", default=[], action="append", help="Process only this dataset (or dataset if specified multiple times)");
    parser.add_option("-c", "--chunk",   dest="chunks",    type="int",    default=[], action="append", help="Process only these chunks (works only if a single dataset is selected with -d)");
    parser.add_option("-N", "--events",  dest="chunkSize", type="int",    default=1000000, help="Default chunk size when splitting trees");
    parser.add_option("-p", "--pretend", dest="pretend",   action="store_true", default=False, help="Don't run anything");
    parser.add_option("-j", "--jobs",    dest="jobs",      type="int",    default=1, help="Use N threads");
    parser.add_option("-q", "--queue",   dest="queue",     type="string", default=None, help="Run jobs on lxbatch instead of locally");
    parser.add_option("-t", "--tree",    dest="tree",      default='treeProducerSusyMultilepton', help="Pattern for tree name");
    parser.add_option("--log", "--log-dir", dest="logdir", type="string", default=None, help="Directory of stdout and stderr");
    parser.add_option("--env",   dest="env", type="string", default="lxbatch", help="Give the environment on which you want to use the batch system (lxbatch, psi, oviedo)");
    parser.add_option("--run",   dest="runner",  type="string", default="lxbatch_runner.sh", help="Give the runner script (default: lxbatch_runner.sh)");
    parser.add_option("--mconly", dest="mconly",  action="store_true", default=False, help="Run only on MC samples");
    parser.add_option("--signals", dest="signals", default="WJetsToLNu", help="declare signals (CSV list) [%default]",type='string');
    parser.add_option("-m", "--modules", dest="modules",  type="string", default=[], action="append", help="Run only these modules among the imported ones");
    parser.add_option(      "--moduleList", dest="moduleList",  type="string", default='DEFAULT_MODULES', help="use this list as a starting point for the modules to run [%default]")

    (options, args) = parser.parse_args()

    if options.friend:
        if options.cut or options.json: raise RuntimeError("Can't apply JSON or cut selection when producing friends")

    if len(args) != 2 or not os.path.isdir(args[0]):
        parser.print_help()
        sys.exit(1)
    if len(options.chunks) != 0 and len(options.datasets) != 1:
        print "must specify a single dataset with -d if using -c to select chunks"
        sys.exit(1)

    treedir = args[0]; outdir=args[1]; args = args[2:]

    jobs = []
    for D in glob(treedir+"/*"):
        treename = "tree"
        fname    = "%s/%s/tree.root" % (D,options.tree)
        pckfile  = "%s/skimAnalyzerCount/SkimReport.pck" % (D)
        if (not os.path.exists(fname)) and os.path.exists("%s/%s/tree.root" % (D,options.tree)):
            treename = "tree"
            fname    = "%s/%s/tree.root" % (D,options.tree)
     
        if (not os.path.exists(fname)) and (os.path.exists("%s/%s/tree.root.url" % (D,options.tree)) ):
            treename = "tree"
            fname    = "%s/%s/tree.root" % (D,options.tree)
            fname    = open(fname+".url","r").readline().strip()
     
        if os.path.exists(fname) or (os.path.exists("%s/%s/tree.root.url" % (D,options.tree))):
            short = os.path.basename(D)
            if options.datasets != []:
                if short not in options.datasets: continue
            data = any(x in short for x in "DoubleMu DoubleEG MuEG MuonEG SingleMuon SingleElectron".split())
            if data and options.mconly: continue
            pckobj  = pickle.load(open(pckfile,'r'))
            counters = dict(pckobj)
            if ('Sum Weights' in counters):
                sample_nevt = counters['Sum Weights']
            else:
                sample_nevt = counters['All Events']
            f = ROOT.TFile.Open(fname);
            t = f.Get(treename)
            entries = t.GetEntries()
            f.Close()
            chunk = options.chunkSize
            if entries < chunk:
                print "  ",os.path.basename(D),("  DATA" if data else "  MC")," single chunk"
                jobs.append((short,fname,sample_nevt,"_Friend_%s"%short,data,xrange(entries),-1))
            else:
                nchunk = int(math.ceil(entries/float(chunk)))
                print "  ",os.path.basename(D),("  DATA" if data else "  MC")," %d chunks" % nchunk
                for i in xrange(nchunk):
                    if options.chunks != []:
                        if i not in options.chunks: continue
                    r = xrange(int(i*chunk),min(int((i+1)*chunk),entries))
                    jobs.append((short,fname,sample_nevt,"_Friend_%s.chunk%d" % (short,i),data,r,i))

    #print jobs
    print "\n"
    print "I have %d taks to process" % len(jobs)

    print 'I\'m using the following list of modules',options.moduleList
    imports = globals()[options.moduleList] + options.imports
    if options.queue:
        import os, sys

        runner = ""
        super = ""
        if options.env == "lxbatch": # Only lxbatch for now
            runner = options.runner
            super  = "bsub -q {queue}".format(queue = options.queue)

        basecmd = "{dir}/{runner} {dir} {cmssw} python {self} -N {chunkSize} -t {tree} --moduleList {moduleList} {data} {output}".format(
                    dir = os.getcwd(), runner=runner, cmssw = os.environ['CMSSW_BASE'], 
                    self=sys.argv[0], chunkSize=options.chunkSize, tree=options.tree, moduleList=options.moduleList, data=treedir, output=outdir)

        writelog = ""
        logdir   = ""
        if options.logdir: 
            logdir = options.logdir.rstrip("/")
            if not os.path.exists(logdir):
                os.system("mkdir -p "+logdir)
        friendPost = ""
        if options.friend: 
            friendPost += " --friend " 
        for (name,fin,sample_nevt,fout,data,range,chunk) in jobs:
            if chunk != -1:
                if options.logdir: writelog = "-o {logdir}/{data}_{chunk}.out -e {logdir}/{data}_{chunk}.err".format(logdir=logdir, data=name, chunk=chunk)
                cmd = "{super} {writelog} {base} -d {data} -c {chunk} {post}".format(super=super, writelog=writelog, base=basecmd, data=name, chunk=chunk, post=friendPost)
                if options.queue == "batch":
                    cmd = "echo \"{base} -d {data} -c {chunk} {post}\" | {super} {writelog}".format(super=super, writelog=writelog, base=basecmd, data=name, chunk=chunk, post=friendPost)
            else:
                if options.logdir: writelog = "-o {logdir}/{data}.out -e {logdir}/{data}.err".format(logdir=logdir, data=name)
                cmd = "{super} {writelog} {base} -d {data} {post}".format(super=super, writelog=writelog, base=basecmd, data=name, chunk=chunk, post=friendPost)
     
                if options.env == "lxbatch":
                    cmd = "echo \"{base} -d {data} {post}\" | {super} {writelog}".format(super=super, writelog=writelog, base=basecmd, data=name, chunk=chunk, post=friendPost)

                print "{base} -d {data}".format(base=basecmd, data=name, chunk=chunk)
            print cmd
            if not options.pretend:
                os.system(cmd)

        exit()

    maintimer = ROOT.TStopwatch()
    def _runIt(myargs):
        (dataset,fin,sample_nevt,fout,data,range,chunk) = myargs
        modules = []
        for mod, names in imports: 
            import_module(mod)
            obj = sys.modules[mod]
            selnames = names.split(",")
            for name in dir(obj):
                if name[0] == "_": continue
                if name in selnames:
                    print "Modules to run: ",options.modules,"  name = ",name
                    if len(options.modules) and name not in options.modules: continue
                    print "Loading %s from %s " % (name, mod)
                    print "Running on dataset = ",dataset
                    signal = any(x in dataset for x in options.signals.split(','))
                    if name=='genQEDJets' and not signal: continue
                    modules.append(getattr(obj,name)())
        if options.noOut:
            if len(modules) == 0: 
                raise RuntimeError("Running with --noout and no modules does nothing!")
        ppargs=[fin]+args
        p=PostProcessor(outdir,ppargs,options.cut,options.branchsel,modules,options.compression,options.friend,fout,options.json,options.noOut,options.justcount,range)
        p.run()

    if options.jobs > 0:
        from multiprocessing import Pool
        pool = Pool(options.jobs)
        pool.map(_runIt, jobs) if options.jobs > 0 else [_runIt(j) for j in jobs]
    else:
        ret = dict(map(_runIt, jobs))
