#!/usr/bin/env python
import os
import os.path as osp
import re
import types
import itertools
import sys
import ROOT

from math import ceil

from CMGTools.TTHAnalysis.treeReAnalyzer import Module, EventLoop, Booker, PyTree

# Define the set of modules to be run.
# Has to be pairs of name, friendclass
#  where friendclass is a callable that takes event as input and
#  returns a dictionary of branchname -> value
MODULES = []

from CMGTools.TTHAnalysis.tools.tHqEventVariables import tHqEventVariableFriend
tHqEventVariables = tHqEventVariableFriend()
MODULES.append( ('tHqEventVariables', tHqEventVariables ))

class VariableProducer(Module):
    def __init__(self,name,booker,modules):
        Module.__init__(self,name,booker)
        self._modules = [ (n,m() if type(m) == types.FunctionType else m) for (n,m) in modules ]
    def beginJob(self):
        self.t = PyTree(self.book("TTree","t","t"))
        self.branches = {}
        for name,mod in self._modules:
            print name
            print mod.listBranches()
            for B in mod.listBranches():
                # don't add the same branch twice
                if B in self.branches:
                    print "Will not add branch %s twice" % (B,)
                    continue
                self.branches[B] = True
                if type(B) == tuple:
                    if len(B) == 2:
                        self.t.branch(B[0],B[1])
                    elif len(B) == 4:
                        self.t.branch(B[0],B[1],n=B[2],lenVar=B[3])
                    elif len(B) == 3:
                        self.t.branch(B[0],B[1],n=B[2],lenVar=None)
                else:
                    self.t.branch(B ,"F")
    def analyze(self,event):
        for name,mod in self._modules:
            keyvals = mod(event)
            for B,V in keyvals.iteritems():
                setattr(self.t, B, V)
                setattr(event,  B, V)
        self.t.fill()

def makeJobs(indir, outdir, options):
    from glob import glob
    jobs = []
    for procdir in glob(indir+"/*"):
        treename = options.tree
        treedir = osp.join(procdir, options.tree)
        fileloc = osp.join(treedir, "%s_tree.root" % options.tree)

        if not osp.exists(fileloc):
            if osp.exists(osp.join(treedir, 'tree.root')):
                treename = "tree"
                fileloc = osp.join(treedir, 'tree.root')

            elif osp.exists(osp.join(treedir, 'tree.root.url')):
                treename = "tree"
                fileloc = open(osp.join(treedir, 'tree.root.url'), 'r').readline().strip()

        if osp.exists(fileloc) or osp.exists(osp.join(treedir, 'tree.root.url')):
            short = osp.basename(procdir)
            if options.datasets != []:
                if short not in options.datasets: continue

            if options.datasetMatches != []:
                found = False
                for dm in  options.datasetMatches:
                    if re.match(dm,short): found = True
                if not found: continue

            # TODO: Unhardcode this
            isdata = any(x in short for x in "DoubleMu DoubleEl DoubleEG MuEG MuonEG SingleMu SingleEl".split())

            tfile = ROOT.TFile.Open(fileloc)
            ttree = tfile.Get(treename)
            try: ttree.GetEntries()
            except AttributeError:
                print "Corrupted ", fileloc
                continue

            fout = osp.join(outdir, "evVarFriend_%s.root" % short)
            entries = ttree.GetEntries()
            tfile.Close()
            if options.newOnly:
                if osp.exists(fout):
                    tfile = ROOT.TFile.Open(fileloc);
                    ttree = tfile.Get(treename)
                    if ttree.GetEntries() != entries:
                        print ("Component %s has to be remade, mismatching number of entries "
                               "(%d vs %d)" % (short, entries, ttree.GetEntries()))
                        tfile.Close()
                    else:
                        print ("Component %s exists already and has matching "
                               "number of entries (%d)" % (short, entries))
                        continue

            chunk = options.chunkSize
            if entries < chunk:

                print "  ",osp.basename(procdir),("  DATA" if isdata else "  MC")," single chunk"

                jobs.append((short, fileloc, fout, isdata, xrange(entries), -1, None))

            else:
                nchunk = int(ceil(entries/float(chunk)))

                print "  ",osp.basename(procdir),("  DATA" if isdata else "  MC")," %d chunks" % nchunk

                for ich in xrange(nchunk):
                    if options.chunks != []:
                        if ich not in options.chunks: continue

                    if not options.fineSplit:
                        evrange = xrange(int(ich*chunk), min(int((ich+1)*chunk), entries) )
                        fout = osp.join(outdir, "evVarFriend_%s.chunk%d.root" % (short, ich))
                        jobs.append((short, fileloc, fout, isdata, evrange, ich, None))

                    else:
                        ev_per_fs = int(ceil(chunk/float(options.fineSplit)))
                        for ifs in xrange(options.fineSplit):
                            if options.subChunk and ifs != options.subChunk: continue
                            evrange = xrange(ich*chunk + ifs*ev_per_fs,
                                             min(ich*chunk + min((ifs+1)*ev_per_fs, chunk), entries) )
                            fout = osp.join(outdir, "evVarFriend_%s.chunk%d.sub%d.root" % (short, ich, ifs))
                            jobs.append((short, fileloc, fout, isdata, evrange, ich, (ifs, options.fineSplit)))

    jobs = [j + (options,) for j in jobs]
    print "\nI have %d task(s) to process" % len(jobs)
    return jobs

def submitJobsLxBatch(jobs, options):
    import os, sys

    runner = "lxbatch_runner.sh"
    subcmd = "bsub -q {queue}".format(queue=options.queue)
    if options.queue in ["all.q", "short.q", "long.q"] and options.env == "psi":
        subcmd = "qsub -q {queue} -N friender".format(queue = options.queue)
        runner = "psibatch_runner.sh"

    basecmd = "{dir}/{runner} {dir} {cmssw} python {self} -N {chunkSize} -T {tdir} -t {tree} {data} {output}"
    basecmd = basecmd.format(dir=os.getcwd(), runner=runner, cmssw=os.environ['CMSSW_BASE'],
                             self=sys.argv[0], chunkSize=options.chunkSize, tdir=options.treeDir,
                             tree=options.tree, data=args[0], output=args[1])

    writelog = ""
    logdir   = ""
    if options.logdir: logdir = options.logdir.rstrip("/")

    if options.vectorTree: basecmd += " --vector "
    friendPost =  "".join(["  -F  %s %s " % (fn,ft) for fn,ft in options.friendTrees])
    friendPost += "".join([" --FM %s %s " % (fn,ft) for fn,ft in options.friendTreesMC])
    friendPost += "".join([" --FD %s %s " % (fn,ft) for fn,ft in options.friendTreesData])
    friendPost += "".join(["  -m  '%s'  " % m for m in options.modules])
    friendPost += "".join(["  -I  '%s'  " % m for m in options.imports])
    for (name,fin,fout,data,range,chunk,fs,_) in jobs:
        if chunk != -1:
            if options.logdir:
                writelog = "-o {logdir}/{data}_{chunk}.out -e {logdir}/{data}_{chunk}.err".format(
                              logdir=logdir, data=name, chunk=chunk)
            cmd = "{subcmd} {writelog} {base} -d {data} -c {chunk} {post}".format(
                              subcmd=subcmd, writelog=writelog, base=basecmd,
                              data=name, chunk=chunk, post=friendPost)
            if fs:
                cmd += " --fineSplit %d --subChunk %d" % (fs[1], fs[0])
        else:
            if options.logdir:
                writelog = "-o {logdir}/{data}.out -e {logdir}/{data}.err".format(logdir=logdir, data=name)
            cmd = "{subcmd} {writelog} {base} -d {data} {post}".format(
                subcmd=subcmd, writelog=writelog, base=basecmd, data=name, chunk=chunk, post=friendPost)
        print cmd
        if not options.pretend:
            os.system(cmd)

def _runIt((name,fin,fout,data,evrange,chunk,fineSplit,options)):
    timer = ROOT.TStopwatch()
    fetchedfile = None
    if 'LSB_JOBID' in os.environ or 'LSF_JOBID' in os.environ:
        if fin.startswith("root://"):
            try:
                tmpdir = os.environ['TMPDIR'] if 'TMPDIR' in os.environ else "/tmp"
                tmpfile =  "%s/%s" % (tmpdir, osp.basename(fin))
                print "xrdcp %s %s" % (fin, tmpfile)
                os.system("xrdcp %s %s" % (fin, tmpfile))
                if osp.exists(tmpfile):
                    fin = tmpfile
                    fetchedfile = fin
                    print "success :-)"

            except: # TODO: Make this explicit. As it is, it hides anything that might go wrong.
                print "failed: %s" % fin
                pass

        fb = ROOT.TFile.Open(fin)

    elif "root://" in fin:
        ROOT.gEnv.SetValue("TFile.AsyncReading", 1);
        fb = ROOT.TXNetFile(fin+"?readaheadsz=65535&DebugLevel=0")
        os.environ["XRD_DEBUGLEVEL"] = "0"
        os.environ["XRD_DebugLevel"] = "0"
        os.environ["DEBUGLEVEL"] = "0"
        os.environ["DebugLevel"] = "0"

    else:
        fb = ROOT.TFile.Open(fin)
        print fb

    print "getting tree.."
    tb = fb.Get(options.tree)
    if not tb: tb = fb.Get("tree") # new trees

    if options.vectorTree:
        tb.vectorTree = True
    else:
        tb.vectorTree = False

    friends = options.friendTrees[:]
    friends += (options.friendTreesData if data else options.friendTreesMC)
    friends_ = [] # to make sure pyroot does not delete them
    for tf_tree,tf_file in friends:
        tf = tb.AddFriend(tf_tree, tf_file.format(name=name, cname=name)),
        friends_.append(tf) # to make sure pyroot does not delete them

    nev = tb.GetEntries()
    if options.pretend:
        print "==== pretending to run %s (%d entries, %s) ====" % (name, nev, fout)
        return (name,(nev,0))

    print "==== %s starting (%d entries) ====" % (name, nev)
    booker = Booker(fout)
    modulesToRun = MODULES
    if options.modules != []:
        toRun = {}
        for m,v in MODULES:
            for pat in options.modules:
                if re.match(pat,m):
                    toRun[m] = True
        modulesToRun = [ (m,v) for (m,v) in MODULES if m in toRun ]

    el = EventLoop([ VariableProducer(options.treeDir,booker,modulesToRun), ])
    el.loop([tb], eventRange=evrange)
    booker.done()
    fb.Close()
    time = timer.RealTime()
    print "=== %s done (%d entries, %.0f s, %.0f e/s) ====" % ( name, nev, time,(nev/time) )

    if fetchedfile and osp.exists(fetchedfile):
        print 'Cleaning up: removing %s'%fetchedfile
        os.system("rm %s"%fetchedfile)

    return (name, (nev, time))

def main(args, options):
    jobs = makeJobs(args[0], args[1], options)

    maintimer = ROOT.TStopwatch()

    if options.queue:
        submitJobsLxBatch(jobs, options)
        sys.exit(0)

    if options.jobs > 0:
        from multiprocessing import Pool
        pool = Pool(options.jobs)
        ret = dict(pool.map(_runIt, jobs))
    else:
        ret = dict(map(_runIt, jobs))

    fulltime = maintimer.RealTime()
    totev   = sum([ev   for (ev,time) in ret.itervalues()])
    tottime = sum([time for (ev,time) in ret.itervalues()])
    print "Done %d tasks in %.1f min (%d entries, %.1f min)" % (len(jobs),fulltime/60.,totev,tottime/60.)

def addOptions(parser):
    parser.add_option("-m", "--modules", dest="modules",  type="string",
                      default=[], action="append",
                      help="Run these modules")
    parser.add_option("-d", "--dataset", dest="datasets",  type="string",
                      default=[], action="append",
                      help="Process only this dataset (or dataset if specified multiple times)")
    parser.add_option("-D", "--dm", "--dataset-match", dest="datasetMatches",  type="string",
                      default=[], action="append",
                      help="Process only this dataset (or dataset if specified multiple times): REGEXP")
    parser.add_option("-c", "--chunk", dest="chunks", type="int", default=[], action="append",
                      help="Process only these chunks (works only if a single dataset is selected with -d)")
    parser.add_option("--subChunk", dest="subChunk", type="int", default=None, nargs=1,
                      help="Process sub-chunk iof this chunk")
    parser.add_option("--fineSplit", dest="fineSplit", type="int", default=None, nargs=1,
                      help="Split each chunk in N subchunks")
    parser.add_option("-N", "--events", dest="chunkSize", type="int", default=500000,
                      help="Default chunk size when splitting trees")
    parser.add_option("-j", "--jobs", dest="jobs", type="int", default=1,
                      help="Use N threads")
    parser.add_option("-p", "--pretend", dest="pretend", action="store_true",
                      default=False,
                      help="Don't run anything")
    parser.add_option("-T", "--tree-dir", dest="treeDir", type="string",
                      default="sf",
                      help="Directory of the friend tree in the file (default: 'sf')")
    parser.add_option("-q", "--queue", dest="queue", type="string",
                      default=None,
                      help=("Run jobs on lxbatch instead of locally. "
                            "Use '1nd' for 24h, '8nh' for 8h"))
    parser.add_option("-t", "--tree", dest="tree", default='ttHLepTreeProducerTTH',
                      help="Pattern for tree name")
    parser.add_option("-V", "--vector", dest="vectorTree", action="store_true",
                      default=True,
                      help="Input tree is a vector")
    parser.add_option("-F", "--add-friend", dest="friendTrees", action="append",
                      default=[], nargs=2,
                      help=("Add a friend tree (treename, filename). "
                            "Can use {name}, {cname} patterns in the treename"))
    parser.add_option("--FMC", "--add-friend-mc", dest="friendTreesMC", action="append",
                      default=[], nargs=2,
                      help=("Add a friend tree (treename, filename) to MC only. "
                            "Can use {name}, {cname} patterns in the treename"))
    parser.add_option("--FD", "--add-friend-data", dest="friendTreesData", action="append",
                      default=[], nargs=2,
                      help=("Add a friend tree (treename, filename) to data trees only. "
                            "Can use {name}, {cname} patterns in the treename"))
    parser.add_option("-L", "--list-modules", dest="listModules", action="store_true",
                      default=False,
                      help="just list the configured modules")
    parser.add_option("-n", "--new",  dest="newOnly", action="store_true",
                      default=False,
                      help="Make only missing trees")
    parser.add_option("-I", "--import", dest="imports", type="string",
                      default=[], action="append",
                      help="Modules to import")
    parser.add_option("--fastsim", dest="isFastSim", action="store_true",
                      default=False,
                      help="Run with configuration for FastSim samples")
    parser.add_option("--log", "--log-dir", dest="logdir", type="string",
                      default=None,
                      help="Directory of stdout and stderr")
    parser.add_option("--env", dest="env", type="string",
                      default="lxbatch",
                      help=("Give the environment on which you want to use the batch system (lxbatch, psi)"))

if __name__ == '__main__':
    from optparse import OptionParser
    usage = """
    %prog [options] <TREE_DIR> <OUT_DIR>

    Test this on a single chunk like so:
    python prepareTHQEventVariableFriends.py -m tHqEventVariables -t treeProducerSusyMultilepton
      -N 100 ra5trees/809_June9_ttH/ tHq_eventvars_Aug5 -d TTHnobb_mWCutfix_ext1 -c 1 --pretend

    """
    parser = OptionParser(usage=usage)
    addOptions(parser)
    (options, args) = parser.parse_args()

    if options.imports:
        MODULES = []
        from importlib import import_module
        for mod in options.imports:
            import_module(mod)
            obj = sys.modules[mod]
            for (name, x) in obj.MODULES:
                print "Loaded %s from %s " % (name, mod)
                MODULES.append((name,x))

    if options.listModules:
        print "List of modules"
        for (n,x) in MODULES:
            if type(x) == types.FunctionType: x = x()
            print "   '%s': %s" % (n,x)
        sys.exit(1)

    if "{P}" in args[1]:
        args[1] = args[1].replace("{P}", args[0])

    if len(args) != 2 or not osp.isdir(args[0]):
        parser.print_usage()
        sys.exit(1)

    if not osp.isdir(args[1]):
        os.system("mkdir -p "+args[1])
        if not osp.isdir(args[1]):
            print "Could not create output directory"
            sys.exit(1)

    if len(options.chunks) != 0 and len(options.datasets) != 1:
        print "must specify a single dataset with -d if using -c to select chunks"
        sys.exit(1)

    main(args, options)
    sys.exit(0)

