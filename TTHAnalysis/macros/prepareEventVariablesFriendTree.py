#!/usr/bin/env python
import os, re, types, sys, subprocess
from collections import defaultdict

## Need to catch upfront if it's run with -t NanoAOD, even before parsing other options
def _getarg(opts,default):
    for opt in opts:
        if opt not in sys.argv: continue
        idx = sys.argv.index(opt)+1
        if idx < len(sys.argv): return sys.argv[idx]
    return default
if _getarg(("-t","--tree"),"NanoAOD") == "NanoAOD":
    isNano = True
    print "Will use the nanoAOD postprocessor"
    # catch attempt of instantiating older modules"
    class Module:
        def __init__(self,*args,**kwargs):
            raise RuntimeError("Trying to instantiate a old CMGTools module while using the postprocessor")
else:
    isNano = False
    if "--tra2" in sys.argv:
        print "Will use the CMGTools new version of treeReAnalyzer"
        from CMGTools.TTHAnalysis.treeReAnalyzer2 import Module, EventLoop, Booker, PyTree
    else:
        print "Will use the CMGTools version of treeReAnalyzer"
        from CMGTools.TTHAnalysis.treeReAnalyzer import Module, EventLoop, Booker, PyTree

from glob import glob
from math import ceil
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

MODULES = []

class VariableProducer(Module):
    def __init__(self,name,booker,modules):
        Module.__init__(self,name,booker)
        self._modules = [ (n,m() if type(m) == types.FunctionType else m) for (n,m) in modules ]
    def init(self,tree):
        for n,m in self._modules:
            if hasattr(m, 'init'): m.init(tree)
    def beginJob(self):
        self.t = PyTree(self.book("TTree","t","t"))
        self.branches = {}
        for name,mod in self._modules:
            print name
            print mod.listBranches()
            if hasattr(mod,'setOutputTree'):
                mod.setOutputTree(self.t)
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
    def endJob(self):
        for n,m in self._modules:
            if hasattr(m, 'endJob'): m.endJob()
    def analyze(self,event):
        for name,mod in self._modules:
            keyvals = mod(event)
            for B,V in keyvals.iteritems():
                setattr(self.t, B, V)
                setattr(event,  B, V)
        self.t.fill()


from optparse import OptionParser
parser = OptionParser(usage="%prog [options] <TREE_DIR> <OUT>")
# common options, independent of the flavour chosen
parser.add_option("-d", "--dataset", dest="datasets",  type="string", default=[], action="append", help="Process only this dataset (or dataset if specified multiple times)");
parser.add_option("-D", "--dm", "--dataset-match", dest="datasetMatches",  type="string", default=[], action="append", help="Process only this dataset (or dataset if specified multiple times): REGEXP");
parser.add_option("--xD", "--de", "--dataset-exclude", dest="datasetExcludes",  type="string", default=[], action="append", help="Exclude these dataset (or dataset if specified multiple times): REGEXP");
parser.add_option("-c", "--chunk",   dest="chunks",    type="int",    default=[], action="append", help="Process only these chunks (works only if a single dataset is selected with -d)");
parser.add_option("--subChunk", dest="subChunk",    type="int",    default=None, nargs=None, help="Process sub-chunk of this chunk");
parser.add_option("--fineSplit", dest="fineSplit",    type="int",    default=None, nargs=1, help="Split each chunk in N subchunks");
parser.add_option("-N", "--events",  dest="chunkSize", type="int",    default=500000, help="Default chunk size when splitting trees");
parser.add_option("-j", "--jobs",    dest="jobs",      type="int",    default=1, help="Use N threads");
parser.add_option("-p", "--pretend", dest="pretend",   action="store_true", default=False, help="Don't run anything");
parser.add_option("--justcount", dest="justcount",   action="store_true", default=False, help="Don't run anything");
parser.add_option("--justtrivial", dest="justtrivial",   action="store_true", default=False, help="Don't run anything");
parser.add_option("--checkchunks", dest="checkchunks",   action="store_true", default=False, help="Check chunks that have been produced");
parser.add_option("--checkrunning", dest="checkrunning",   action="store_true", default=False, help="Check chunks that have been produced");
parser.add_option("--checkaliens", dest="checkaliens",   action="store_true", default=False, help="Check for aliens (existing files in friends dir corresponding to no input samples)");
parser.add_option("--quiet", dest="quiet",   action="store_true", default=False, help="Check chunks that have been produced");
parser.add_option("-q", "--queue",   dest="queue",     type="string", default=None, help="Run jobs on lxbatch queue or condor instead of locally");
parser.add_option("-a", "--accounting-group", dest="accounting_group", default=None, help="Accounting group for condor jobs");
parser.add_option("--maxruntime", "--time",  dest="maxruntime", type="int", default=360, help="Condor job wall clock time in minutes (default: 6h)");
parser.add_option("-n", "--new",  dest="newOnly", action="store_true", default=False, help="Make only missing trees");
parser.add_option("--log", "--log-dir", dest="logdir", type="string", default=None, help="Directory of stdout and stderr");
parser.add_option("--sub", "--subfile", dest="subfile", type="string", default="condor.sub", help="Subfile for condor (default: condor.sub)");
parser.add_option("--env",   dest="env",     type="string", default="lxbatch", help="Give the environment on which you want to use the batch system (lxbatch, psi, oviedo, uclouvain)");
parser.add_option("--run",   dest="runner",     type="string", default="lxbatch_runner.sh", help="Give the runner script (default: lxbatch_runner.sh)");
parser.add_option("--bk",   dest="bookkeeping",  action="store_true", default=False, help="If given the command used to run the friend tree will be stored");
parser.add_option("--tra2",  dest="useTRAv2", action="store_true", default=False, help="Use the new version of treeReAnalyzer");
parser.add_option("-t", "--tree", dest="tree", default='NanoAOD', help="Pattern for tree name");
# input friends
parser.add_option("-F", "--add-friend",    dest="friendTrees",  action="append", default=[], nargs=2, help="Add a friend tree (treename, filename). Can use {name}, {cname} patterns in the treename")
parser.add_option("--FMC", "--add-friend-mc",    dest="friendTreesMC",  action="append", default=[], nargs=2, help="Add a friend tree (treename, filename) to MC only. Can use {name}, {cname} patterns in the treename")
parser.add_option("--FD", "--add-friend-data",    dest="friendTreesData",  action="append", default=[], nargs=2, help="Add a friend tree (treename, filename) to data trees only. Can use {name}, {cname} patterns in the treename")
parser.add_option("--name",   dest="name",     type="string", default="Friender", help="Name for batch jobs");
# options that are different between old CMGTools and nanoAOD-tools
if isNano: # new nanoAOD-tools options
    # importing of modules
    parser.add_option("-I", "--import", dest="imports",  type="string", default=[], action="append", nargs=2, help="Import modules (python package, comma-separated list of ");
    # output file name pattern
    #parser.add_option("-o", "--outPattern",   dest="outPattern",     type="string", default="%s_Friend", help="Pattern string for output file name"); # not really configurable due to postprocessor limitations
    parser.add_option("-z", "--compression",  dest="compression", type="string", default=("ZLIB:3"), help="Compression: none, or (algo):(level) ")
else: # old CMGTools options
    # importing of modules
    parser.add_option("-m", "--modules", dest="modules",  type="string", default=[], action="append", help="Run these modules");
    parser.add_option("-I", "--import", dest="imports",  type="string", default=[], action="append", help="Modules to import");
    parser.add_option("-L", "--list-modules",  dest="listModules", action="store_true", default=False, help="just list the configured modules");
    # output file name pattern
    parser.add_option("-o", "--outPattern",   dest="outPattern",     type="string", default="evVarFriend_%s", help="Pattern string for output file name");
    parser.add_option("-T", "--tree-dir",   dest="treeDir",     type="string", default="sf", help="Directory of the friend tree in the file (default: 'sf')");
(options, args) = parser.parse_args()


if not isNano:
    if options.imports:
        MODULES = []
        from importlib import import_module
        for mod in options.imports:
            import_module(mod)
            obj = sys.modules[mod]
            for (name,x) in obj.MODULES:
                print "Loaded %s from %s " % (name, mod)
                MODULES.append((name,x))

    if options.listModules:
        print "List of modules"
        for (n,x) in MODULES:
            if type(x) == types.FunctionType: x = x()
            print "   '%s': %s" % (n,x)
        exit()

    if options.modules != []:
        found = False
        for m,v in MODULES:
            for pat in options.modules:
                if re.match(pat,m):
                    found = True
                    break
        if not found: 
            print "ERROR: no modules selected\n - selection was %s\n - list of modules is %s\n" % (
                        sorted(options.modules), sorted(_[0] for _ in MODULES))
            exit()

if "{P}" in args[1]: args[1] = args[1].replace("{P}",args[0])
if len(args) != 2:
    print args
    print "Usage: program <TREE_DIR> <OUT>"
    exit()
if not os.path.isdir(args[0]):
    print "Error. Input directory {input} does not exist".format(input=args[0])
    exit()
if not os.path.isdir(args[1]):
    tempOut = args[1].replace('/pool/ciencias/','/pool/cienciasrw/')
    os.system("mkdir -p "+tempOut)
    if not os.path.isdir(args[1]):
        print "Could not create output directory"
        exit()
if len(options.chunks) != 0 and len(options.datasets) != 1:
    print "must specify a single dataset with -d if using -c to select chunks"
    exit()

if isNano:
    options.outPattern = "%s_Friend"

done_chunks = defaultdict(set)
done_subchunks = defaultdict(set)
chunks_with_subs = defaultdict(set)
if options.checkchunks:
    npass, nfail = 0,0
    lsls = subprocess.check_output(["ls", "-l", args[1]])
    for line in sorted(lsls.split("\n")):
        if (options.outPattern % "") not in line: continue
        fields = line.split()
        size = int(fields[4])
        fname = fields[8]
        basepattern = options.outPattern % r"(\w+)"
        m1 = re.match(basepattern + r"%s.chunk(\d+).sub(\d+).root" % (), fname);
        m2 = re.match(basepattern + r"%s.chunk(\d+).root", fname);
        good = (size > 2048)
        if m1:
            sample = m1.group(1)
            chunk = int(m1.group(2))
            sub = int(m1.group(3))
            if good: done_subchunks[(sample,chunk)].add(sub)
            #done_chunks[sample].discard(chunk)
            chunks_with_subs[sample].add(chunk)
        elif m2:
            sample = m2.group(1)
            chunk = int(m2.group(2))
            sub = None
            if good: done_chunks[sample].add(chunk)
        else:
            continue
        if good: npass += 1
        else: nfail += 1
    print "Found %d good chunks, %d bad chunks" % (npass, nfail)
    if options.fineSplit:
        allsubs = set(range(options.fineSplit))
        if not os.path.isdir(args[1]+"/subchunks"):
            os.system("mkdir -p "+args[1]+"/subchunks")
        for sample, chunks in chunks_with_subs.iteritems():
            for chunk in chunks:
                if done_subchunks[(sample,chunk)] == allsubs:
                    print "%s chunk %s has all the fine splits -> doing the hadd " % (sample, chunk),
                    target = "%s.chunk%d.root" % (options.outPattern % sample, chunk)
                    inputs = [ "%s.chunk%d.sub%d.root" % (options.outPattern % sample, chunk, sub) for sub in range(options.fineSplit) ]
                    try:
                        haddout = subprocess.check_output(["hadd", "-f", target]+inputs, cwd=args[1])
                        subprocess.check_output(["mv", "-v" ]+inputs+["subchunks/"], cwd=args[1])
                        print " OK"
                    except subprocess.CalledProcessError:
                        print "ERROR"; print haddout
if options.checkrunning:
    nrunning = 0
    if options.queue == "condor":
        running = subprocess.check_output(["condor_q", "-nobatch","-wide"])
    elif options.queue == "cp3":
        running = subprocess.check_output(["squeue", "-u", os.environ["USER"]])
    else:
        running = subprocess.check_output(["bjobs", "-ww"])
    tomatch = re.compile(r"\s{self}\s.(?:.*\s)?{input}\s.*\s*{output}\s(?:.*\s)?-d\s+(\w+)\s+-c\s+(\d+)\b".format(self=sys.argv[0], input=args[0], output=args[1]))
    finespl = re.compile(r"--fineSplit\s+\d+\s+--subChunk\s+(\d+)")
    for line in running.split("\n"):
        if os.path.basename(sys.argv[0]) not in line: continue
        if args[1]+" " not in line: continue
        m = re.search(tomatch, line)
        if not m: continue
        nrunning += 1
        mfs = re.search(finespl, line)
        if options.fineSplit and mfs:
            name, chunk, sub = m.group(1), int(m.group(2)), int(mfs.group(1))
            done_subchunks[(name,chunk)].add(sub)
            chunks_with_subs[name].add(chunk)
        else:
            done_chunks[m.group(1)].add(int(m.group(2)))
    print "Found %d chunks running" % (nrunning)
if options.checkaliens:
    pattern = re.compile( (options.outPattern % "(\\w+)") + r"\.root")
    for fname in glob(args[1] + "/" + (options.outPattern % "*") + ".root"):
        m = re.match(pattern, os.path.basename(fname))
        if not m: 
            print "Extra alien friend found? %s" % fname
            continue
        totest = args[0] + "/" + m.group(1) + (".root" if isNano else "")
        if not os.path.exists(totest):
            print "Alien friend found? %s with no %s" % (fname, totest)
            continue
jobs = []
for D in sorted(glob(args[0]+"/*")):
    if isNano:
        treename = "Events"
        if os.path.isfile(D) and D.endswith(".root"):
            fname = D
        elif os.path.isdir(D) and os.path.isfile("%s/%s.root" % (D, os.path.basename(D))):
            fname = "%s/%s.root" % (D, os.path.basename(D))
        else:
            continue
    else:
        treename = options.tree
        fname    = "%s/%s/%s_tree.root" % (D,options.tree,options.tree)
        if (not os.path.exists(fname)) and (os.path.exists("%s/%s/tree.root" % (D,options.tree)) ):
            treename = "tree"
            fname    = "%s/%s/tree.root" % (D,options.tree)
        if (not os.path.exists(fname)) and (os.path.exists("%s/%s/tree.root.url" % (D,options.tree)) ):
            treename = "tree"
            fname    = "%s/%s/tree.root" % (D,options.tree)
            fname    = open(fname+".url","r").readline().strip()
    if os.path.exists(fname) or (os.path.exists("%s/%s/tree.root.url" % (D,options.tree))):
        short = os.path.basename(D)
        if short.endswith(".root"): short = short[:-len(".root")] # rstrip does not do what one would like
        if options.datasets != []:
            if short not in options.datasets: continue
        if options.datasetMatches != []:
            found = False
            for dm in  options.datasetMatches:
                if re.match(dm,short): found = True
            if not found: continue
        if options.datasetExcludes != []:
            found = False
            for dm in  options.datasetExcludes:
                if re.match(dm,short): found = True
            if found: continue
        data =  any(x in short for x in "DoubleMu DoubleEl DoubleEG MuEG MuonEG SingleMu SingleEl EGamma".split()) # FIXME
        f = ROOT.TFile.Open(fname)
        t = f.Get(treename)
        if not t:
            print "Corrupted ",fname
            continue
        entries = t.GetEntries()
        if options.justtrivial and entries > 0: continue
        f.Close()
        fout = "%s/%s.root" % (args[1],options.outPattern%short)
        if options.newOnly:
            if os.path.exists(fout):
                f2 = ROOT.TFile.Open(fout)
                if (not f2) or f2.IsZombie() or f2.TestBit(ROOT.TFile.kRecovered): 
                    if f2: f2.Close()
                    if not options.quiet: print "Component %s has to be remade, output tree is invalid or corrupted" % (short, entries, t2.GetEntries())
                else:
                    t2 = f2.Get("Friends" if isNano else (options.treeDir+"/t"))
                    if t2.GetEntries() != entries:
                        if not options.quiet: print "Component %s has to be remade, mismatching number of entries (%d vs %d)" % (short, entries, t2.GetEntries())
                        f2.Close()
                    else:
                        if not options.quiet: print "Component %s exists already and has matching number of entries (%d)" % (short, entries)
                        continue
        chunk = options.chunkSize
        if entries < chunk:
            if not options.quiet: print "  ",os.path.basename(D),("  DATA" if data else "  MC")," single chunk (%d events)" % entries
            if 1 in done_chunks[short]: continue
            if options.queue == "condor":
                jobs.append((short,data,1))
            else:
                jobs.append((short,fname,"%s/%s.root" % (args[1],options.outPattern%short),data,(0,entries),-1,None))
        else:
            nchunk = int(ceil(entries/float(chunk)))
            if not options.quiet: print "  ",os.path.basename(D),("  DATA" if data else "  MC")," %d chunks (%d events)" % (nchunk, entries)
            if options.queue == "condor":
                if options.checkchunks:
                    for i in xrange(nchunk):
                        if i in done_chunks[short]: continue
                        if options.fineSplit:
                            if i in chunks_with_subs[short]:
                                for ifs in xrange(options.fineSplit):
                                    if ifs in done_subchunks[(short,i)]: continue
                                    jobs.append((short,data,i,ifs))
                            else:
                                jobs.append((short,data,i,-1))
                        else:
                            jobs.append((short,data,i))
                else:
                    jobs.append((short,data,nchunk))
                continue
            for i in xrange(nchunk):
                if i in done_chunks[short]: continue
                if options.chunks != []:
                    if i not in options.chunks: continue
                if not options.fineSplit:
                    r = (int(i*chunk),min(int((i+1)*chunk),entries))
                    jobs.append((short,fname,"%s/%s.chunk%d.root" % (args[1],options.outPattern%short,i),data,r,i,None))
                else:
                    ev_per_fs = int(ceil(chunk/float(options.fineSplit)))
                    for ifs in xrange(options.fineSplit):
                        if i in chunks_with_subs[short] and ifs in done_subchunks[(short,i)]: continue
                        if options.subChunk != None and ifs != options.subChunk: continue
                        r = (i*chunk + ifs*ev_per_fs, min(i*chunk + min((ifs+1)*ev_per_fs, chunk),entries))
                        jobs.append((short,fname,"%s/%s.chunk%d.sub%d.root" % (args[1],options.outPattern%short,i,ifs),data,r,i,(ifs,options.fineSplit)))
print "\n"
njobs = len(jobs)
if options.queue == "condor": 
    if options.checkchunks and options.fineSplit: njobs = sum(((options.fineSplit if r[-1] == -1 else 1) for r in jobs),0)
    elif not options.checkchunks: njobs = sum((r[-1] for r in jobs),0)
print "I have %d task(s) to process" % njobs
if options.justcount: sys.exit()
if options.queue == "condor":
    subfile = open(options.subfile, "w")
    logdir = (options.logdir if options.logdir else args[1]+"/logs").replace("{P}", args[0]).replace("{O}", args[1])
    os.system("mkdir -p "+logdir)
    chunk = "Step"
    if options.checkchunks:
        chunk = "Chunk"
        if options.fineSplit:
            chunk = "Chunk).$(Step"
    subfile.write("""##### BEGIN condor submit file
Executable = {runner}
Universe   = vanilla
Error      = {logdir}/err.$(cluster).$(Dataset).$({chunk})
Output     = {logdir}/out.$(cluster).$(Dataset).$({chunk})
Log        = {logdir}/log.$(cluster).$(Dataset).$({chunk})

use_x509userproxy = $ENV(X509_USER_PROXY)
getenv = True
request_memory = 2000
+MaxRuntime = {maxruntime}
{accounting_group}
""".format(runner = options.runner, logdir = logdir, maxruntime = options.maxruntime * 60, chunk = chunk,
           accounting_group = '+AccountingGroup = "%s"'%options.accounting_group if options.accounting_group else ''))
if options.queue:
    runner = ""
    super = ""
    theoutput = args[1]
    if options.env == "psi":
        super  = "qsub -q {queue} -N friender".format(queue = options.queue)
        runner = "psibatch_runner.sh"
    elif options.env == "oviedo":
        super  = "qsub -q {queue} -N {name}".format(queue = options.queue, name=options.name)
        runner = "lxbatch_runner.sh"
        theoutput = theoutput.replace('/pool/ciencias/','/pool/cienciasrw/')
    elif options.env == "uclouvain":
        options.subfile="slurm_submitter_of_stuff_"
        super = "sbatch --partition cp3 "
    else: # Use lxbatch by default
        runner = options.runner
        super  = "bsub -q {queue}".format(queue = options.queue)

    basecmd = "{dir}/{runner} {dir} {cmssw} python {self} -j 0 -N {chunkSize}  -t {tree} {data} {output}".format(
                dir = os.getcwd(), runner=runner, cmssw = os.environ['CMSSW_BASE'],
                self=sys.argv[0], chunkSize=options.chunkSize,
                tree=options.tree, data=args[0], output=theoutput)
    if not isNano: basecmd += " -T %s " % options.treeDir

    if options.queue == "cp3":
        basecmd = "python {dir}/{self} -j 0 -N {chunkSize} -t {tree} {data} {output}".format(
                dir = os.getcwd(), runner=runner, cmssw = os.environ['CMSSW_BASE'],
                self=sys.argv[0], chunkSize=options.chunkSize,
                tree=options.tree, data=args[0], output=theoutput)
        if not isNano: basecmd = "python {dir}/{self} -j 0 -N {chunkSize} -T {tdir} -t {tree} {data} {output}".format(
                dir = os.getcwd(), runner=runner, cmssw = os.environ['CMSSW_BASE'],
                self=sys.argv[0], chunkSize=options.chunkSize, tdir=options.treeDir,
                tree=options.tree, data=args[0], output=theoutput)
    writelog = ""
    logdir   = ""
    if options.logdir: logdir = options.logdir.rstrip("/")

    if options.useTRAv2: basecmd += " --tra2 "
    friendPost =  "".join(["  -F  %s %s " % (fn,ft) for fn,ft in options.friendTrees])
    friendPost += "".join([" --FM %s %s " % (fn,ft) for fn,ft in options.friendTreesMC])
    friendPost += "".join([" --FD %s %s " % (fn,ft) for fn,ft in options.friendTreesData])
    if isNano:
        friendPost += "".join(["  -I  '%s' '%s' " % m for m in options.imports])
        friendPost += " --compression '%s' " % options.compression
    else:
        friendPost += "".join(["  -m  '%s'  " % m for m in options.modules])
        friendPost += "".join(["  -I  '%s'  " % m for m in options.imports])

    if options.queue == "condor":
      baseargs = basecmd[len(os.getcwd())+len(runner)+2:] + friendPost
      baseargs = baseargs.replace("'","")
      if options.checkchunks:
          if options.fineSplit:
              if any(j for j in jobs if j[-1] == -1): # entire pieces to split
                  subfile.write("\nArguments = {base} -d $(Dataset) -c $(Chunk) --fineSplit {FS} --subChunk $(Step) \n\n".format(base = baseargs, FS=options.fineSplit))
                  subfile.write("Queue {FS} Dataset, Chunk from (\n".format(FS=options.fineSplit))
                  for (name, data, chunk, fs) in jobs:
                      if fs == -1: subfile.write("    {name}, {chunk}\n".format(name=name, chunk=chunk))
                  subfile.write(")\n")
              if any(j for j in jobs if j[-1] != -1): # individual subchunks to re-run
                  subfile.write("\nArguments = {base} -d $(Dataset) -c $(Chunk) --fineSplit {FS} --subChunk $(Step) \n\n".format(base = baseargs, FS=options.fineSplit))
                  subfile.write("Queue Dataset, Chunk, Step from (\n".format(FS=options.fineSplit))
                  for (name, data, chunk, fs) in jobs:
                      if fs != -1: subfile.write("    {name}, {chunk}, {fs}\n".format(name=name, chunk=chunk, fs=fs))
                  subfile.write(")\n")
          else:
              subfile.write("\nArguments = {base} -d $(Dataset) -c $(Chunk)\n\n".format(base = baseargs))
              subfile.write("Queue Dataset, Chunk from (\n")
              for (name, data, chunk) in jobs:
                subfile.write("    {name}, {chunk}\n".format(name=name, chunk=chunk))
              subfile.write(")\n")
      else:
          subfile.write("\nArguments = {base} -d $(Dataset) -c $(Step)\n\n".format(base = baseargs))
          for (name, data, nchunks) in jobs:
            subfile.write("Queue {njobs} Dataset in {name}\n".format(name=name, njobs=nchunks))
      subfile.close()
      print "Saved condor submit file to %s" % options.subfile
      if not options.pretend:
         os.system("condor_submit "+options.subfile)
    else:
      for (name,fin,fout,data,range,chunk,fs) in jobs:
        if chunk != -1:
            if options.logdir: writelog = "-o {logdir}/{data}_{chunk}.out -e {logdir}/{data}_{chunk}.err".format(logdir=logdir, data=name, chunk=chunk)
            cmd = "{super} {writelog} {base} -d {data} -c {chunk} {post}".format(super=super, writelog=writelog, base=basecmd, data=name, chunk=chunk, post=friendPost)
            if options.queue == "batch" and options.env != "oviedo":
                cmd = "echo \"{base} -d {data} -c {chunk} {post}\" | {super} {writelog}".format(super=super, writelog=writelog, base=basecmd, data=name, chunk=chunk, post=friendPost)
            elif options.env == "oviedo":
                cmd = "{super} {writelog} {base} -d {data} -c {chunk} {post} ".format(super=super, writelog=writelog, base=basecmd, data=name, chunk=chunk, post=friendPost)
            if options.queue == "cp3" and options.env == "uclouvain":
                full_subfile = "{subfile}{data}_{chunk}.sh".format(subfile=options.subfile, data=name, chunk=chunk)
                subfile = open(full_subfile, "w")
                subfile.write("""#! /bin/bash
#SBATCH --ntasks=8

""")

                dacmd = "{base} -d {data} -c {chunk} {post}".format(base=basecmd, data=name, chunk=chunk, post=friendPost)
                subfile.write("""srun -N1 -n1 -c1 --exclusive {cmd} &
wait

""".format(cmd=dacmd))
                subfile.close()
                print "Saved slurm submit file to %s" % full_subfile
                cmd = "{super} {subfile}".format(super=super, subfile=full_subfile)
            if fs:
                cmd += " --fineSplit %d --subChunk %d" % (fs[1], fs[0])
        else:
            if options.logdir: writelog = "-o {logdir}/{data}.out -e {logdir}/{data}.err".format(logdir=logdir, data=name)
            cmd = "{super} {writelog} {base} -d {data} {post}".format(super=super, writelog=writelog, base=basecmd, data=name, chunk=chunk, post=friendPost)

            if options.queue == "batch" and options.env != "oviedo":
                cmd = "echo \"{base} -d {data} {post}\" | {super} {writelog}".format(super=super, writelog=writelog, base=basecmd, data=name, chunk=chunk, post=friendPost)
            elif options.env == "oviedo":
                cmd = "{super} {base} -d {data} {post} {writelog}".format(super=super, writelog=writelog, base=basecmd, data=name, chunk=chunk, post=friendPost)
            if options.queue == "cp3" and options.env == "uclouvain":
                full_subfile = "{subfile}{data}_{chunk}.sh".format(subfile=options.subfile, data=name, chunk=chunk)
                subfile = open(full_subfile, "w")
                subfile.write("""#! /bin/bash
#SBATCH --ntasks=8

""")
                dacmd = "{base} -d {data} -c {chunk} {post}".format(base=basecmd, data=name, chunk=chunk, post=friendPost)
                subfile.write("""srun -N1 -n1 -c1 --exclusive {cmd} &
wait

""".format(cmd=dacmd))
                subfile.close()
                print "Saved slurm submit file to %s" % full_subfile
                cmd = "{super} {subfile}".format(super=super, subfile=full_subfile)
        print cmd
        if not options.pretend:
            os.system(cmd)

    exit()

maintimer = ROOT.TStopwatch()
def _runIt(myargs):
    (name,fin,ofout,data,range,chunk,fineSplit) = myargs
    timer = ROOT.TStopwatch()
    fetchedfile = None

    fout = ofout.replace('/pool/ciencias/', '/pool/cienciasrw/')
    
    if 'LSB_JOBID' in os.environ or 'LSF_JOBID' in os.environ:
        if fin.startswith("root://"):
            try:
                tmpdir = os.environ['TMPDIR'] if 'TMPDIR' in os.environ else "/tmp"
                tmpfile =  "%s/%s" % (tmpdir, os.path.basename(fin))
                print "xrdcp %s %s" % (fin, tmpfile)
                os.system("xrdcp %s %s" % (fin, tmpfile))
                if os.path.exists(tmpfile):
                    fin = tmpfile
                    fetchedfile = fin
                    print "success :-)"
            except:
                pass
        fb = ROOT.TFile.Open(fin)
    elif "root://" in fin:
        ROOT.gEnv.SetValue("TFile.AsyncReading", 1);
        fb   = ROOT.TXNetFile(fin+"?readaheadsz=65535&DebugLevel=0")
        os.environ["XRD_DEBUGLEVEL"]="0"
        os.environ["XRD_DebugLevel"]="0"
        os.environ["DEBUGLEVEL"]="0"
        os.environ["DebugLevel"]="0"
    else:
        fb = ROOT.TFile.Open(fin)
        print fb

    print "getting tree.."
    tb = fb.Get(options.tree)

    if not tb: tb = fb.Get("tree") # new trees
    tb.vectorTree = True

    friends = options.friendTrees[:]
    friends += (options.friendTreesData if data else options.friendTreesMC)
    friends_ = [] # to make sure pyroot does not delete them
    for tf_tree,tf_file in friends:
        tf = tb.AddFriend(tf_tree, tf_file.format(name=name, cname=name, P=args[0])),
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
    el.loop([tb], eventRange=xrange(range))
    booker.done()
    fb.Close()
    time = timer.RealTime()
    nev = el._doneEvents
    print "=== %s done (%d entries, %.0f s, %.0f e/s) ====" % ( name, nev, time,(nev/time) )
    if fetchedfile and os.path.exists(fetchedfile):
        print 'Cleaning up: removing %s'%fetchedfile
        os.system("rm %s"%fetchedfile)
    if options.bookkeeping:
        if not os.path.exists(fout[:fout.rfind("/")] + "/cmd"): os.system("mkdir -p " + fout[:fout.rfind("/")] + "/cmd")
        fcmd = open(fout[:fout.rfind("/")] + "/cmd/" + fout[fout.rfind("/")+1:-len(".root")] + "_command.txt", "w")
        fcmd.write("%s\n\n" % " ".join(sys.argv)) 
        fcmd.write("%s\n%s\n" % (args,options)) 
        fcmd.close()
    return (name,(nev,time))

def _runItNano(myargs):
    (name,fin,ofout,data,range,chunk,fineSplit) = myargs
    timer = ROOT.TStopwatch()
    command = ["nano_postproc.py", "--friend", os.path.dirname(ofout), "--postfix", os.path.basename(ofout)[len(name):-len(".root")] ]
    for i in options.imports:  command += [ "-I", i[0], i[1] ]
    command += [ "-z", options.compression ]
    fin = fin
    friends = options.friendTrees[:] + (options.friendTreesData if data else options.friendTreesMC)
    for tf_tree,tf_file in friends:
        if tf_tree not in ("Friends", "Events"): print "Unsupported friend tree name %s" % tf_tree
        fin += ",%s" % tf_file.format(name=name, cname=name, P=args[0])
    command += [ fin, "--first-entry", str(range[0]), "-N", str(range[1] - range[0]) ]
    if options.pretend:
        print "==== pretending to run %s (%d entries starting from %d, %s) ====" % (name, range[1] - range[0], range[0], ofout)
        print "# ", "  ".join(command)
        return (name,(range[1] - range[0],0))
    print "==== %s starting (%d entries starting from %d, %s) ====" % (name, range[1] - range[0], range[0], ofout)
    print "  ".join(command)
    subprocess.call(command)
    time = timer.RealTime()
    print "=== %s done (%d entries starting from %d, %.0f s, %.0f e/s, %s) ====" % ( name, range[1] - range[0], range[0], time, (range[1] - range[0]/time), ofout )
    return (name,(range[1] - range[0],time))
    
_run = _runItNano if isNano else _runIt
if options.jobs > 0:
    from multiprocessing import Pool
    pool = Pool(options.jobs)
    ret  = dict(pool.map(_run, jobs)) if options.jobs > 0 else dict([_run(j) for j in jobs])
else:
    ret = dict(map(_run, jobs))
fulltime = maintimer.RealTime()
totev   = sum([ev   for (ev,time) in ret.itervalues()])
tottime = sum([time for (ev,time) in ret.itervalues()])
print "Done %d tasks in %.1f min (%d entries, %.1f min)" % (len(jobs),fulltime/60.,totev,tottime/60.)



