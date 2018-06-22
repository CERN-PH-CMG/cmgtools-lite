#!/usr/bin/env python
import os, re, types, sys, subprocess
from collections import defaultdict
if "--tra2" in sys.argv:
    print "Will use the new experimental version of treeReAnalyzer"
    from CMGTools.TTHAnalysis.treeReAnalyzer2 import Module, EventLoop, Booker, PyTree
else:
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
parser.add_option("-m", "--modules", dest="modules",  type="string", default=[], action="append", help="Run these modules");
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
parser.add_option("--quiet", dest="quiet",   action="store_true", default=False, help="Check chunks that have been produced");
parser.add_option("-T", "--tree-dir",   dest="treeDir",     type="string", default="sf", help="Directory of the friend tree in the file (default: 'sf')");
parser.add_option("-q", "--queue",   dest="queue",     type="string", default=None, help="Run jobs on lxbatch queue or condor instead of locally");
parser.add_option("--maxruntime", "--time",  dest="maxruntime", type="int", default=360, help="Condor job wall clock time in minutes (default: 6h)");
parser.add_option("-t", "--tree",    dest="tree",      default='ttHLepTreeProducerTTH', help="Pattern for tree name");
parser.add_option("-V", "--vector",  dest="vectorTree", action="store_true", default=True, help="Input tree is a vector");
parser.add_option("-F", "--add-friend",    dest="friendTrees",  action="append", default=[], nargs=2, help="Add a friend tree (treename, filename). Can use {name}, {cname} patterns in the treename")
parser.add_option("--FMC", "--add-friend-mc",    dest="friendTreesMC",  action="append", default=[], nargs=2, help="Add a friend tree (treename, filename) to MC only. Can use {name}, {cname} patterns in the treename")
parser.add_option("--FD", "--add-friend-data",    dest="friendTreesData",  action="append", default=[], nargs=2, help="Add a friend tree (treename, filename) to data trees only. Can use {name}, {cname} patterns in the treename")
parser.add_option("-L", "--list-modules",  dest="listModules", action="store_true", default=False, help="just list the configured modules");
parser.add_option("-n", "--new",  dest="newOnly", action="store_true", default=False, help="Make only missing trees");
parser.add_option("-I", "--import", dest="imports",  type="string", default=[], action="append", help="Modules to import");
parser.add_option("--log", "--log-dir", dest="logdir", type="string", default=None, help="Directory of stdout and stderr");
parser.add_option("--sub", "--subfile", dest="subfile", type="string", default="condor.sub", help="Subfile for condor (default: condor.sub)");
parser.add_option("--env",   dest="env",     type="string", default="lxbatch", help="Give the environment on which you want to use the batch system (lxbatch, psi, oviedo)");
parser.add_option("--run",   dest="runner",     type="string", default="lxbatch_runner.sh", help="Give the runner script (default: lxbatch_runner.sh)");
parser.add_option("--bk",   dest="bookkeeping",  action="store_true", default=False, help="If given the command used to run the friend tree will be stored");
parser.add_option("--tra2",  dest="useTRAv2", action="store_true", default=False, help="Use the new experimental version of treeReAnalyzer");
(options, args) = parser.parse_args()


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

done_chunks = defaultdict(set)
done_subchunks = defaultdict(set)
chunks_with_subs = defaultdict(set)
if options.checkchunks:
    npass, nfail = 0,0
    lsls = subprocess.check_output(["ls", "-l", args[1]])
    for line in sorted(lsls.split("\n")):
        if "evVarFriend" not in line: continue
        fields = line.split()
        size = int(fields[4])
        fname = fields[8]
        m1 = re.match(r"evVarFriend_(\w+).chunk(\d+).sub(\d+).root", fname);
        m2 = re.match(r"evVarFriend_(\w+).chunk(\d+).root", fname);
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
                    target = "evVarFriend_%s.chunk%d.root" % (sample, chunk)
                    inputs = [ "evVarFriend_%s.chunk%d.sub%d.root" % (sample, chunk, sub) for sub in range(options.fineSplit) ]
                    #print "hadd -f %s %s" % (target, " ".join(inputs))
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
jobs = []
for D in sorted(glob(args[0]+"/*")):
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
        data =  any(x in short for x in "DoubleMu DoubleEl DoubleEG MuEG MuonEG SingleMu SingleEl".split()) # FIXME
        f = ROOT.TFile.Open(fname)
        t = f.Get(treename)
        if not t:
            print "Corrupted ",fname
            continue
        entries = t.GetEntries()
        if options.justtrivial and entries > 0: continue
        f.Close()
        if options.newOnly:
            fout = "%s/evVarFriend_%s.root" % (args[1],short)
            if os.path.exists(fout):
                f = ROOT.TFile.Open(fname);
                t = f.Get(treename)
                if t.GetEntries() != entries:
                    if not options.quiet: print "Component %s has to be remade, mismatching number of entries (%d vs %d)" % (short, entries, t.GetEntries())
                    f.Close()
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
                jobs.append((short,fname,"%s/evVarFriend_%s.root" % (args[1],short),data,xrange(entries),-1,None))
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
                    r = xrange(int(i*chunk),min(int((i+1)*chunk),entries))
                    jobs.append((short,fname,"%s/evVarFriend_%s.chunk%d.root" % (args[1],short,i),data,r,i,None))
                else:
                    ev_per_fs = int(ceil(chunk/float(options.fineSplit)))
                    for ifs in xrange(options.fineSplit):
                        if i in chunks_with_subs[short] and ifs in done_subchunks[(short,i)]: continue
                        if options.subChunk != None and ifs != options.subChunk: continue
                        r = xrange(i*chunk + ifs*ev_per_fs, min(i*chunk + min((ifs+1)*ev_per_fs, chunk),entries))
                        jobs.append((short,fname,"%s/evVarFriend_%s.chunk%d.sub%d.root" % (args[1],short,i,ifs),data,r,i,(ifs,options.fineSplit)))
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

""".format(runner = options.runner, logdir = logdir, maxruntime = options.maxruntime * 60, chunk = chunk))
if options.queue:
    runner = ""
    super = ""
    theoutput = args[1]
    if options.env == "psi":
        super  = "qsub -q {queue} -N friender".format(queue = options.queue)
        runner = "psibatch_runner.sh"
    elif options.env == "oviedo":
        if options.queue != "":
            options.queue = "batch" 
        super  = "qsub -q {queue} -N happyTreeFriend".format(queue = options.queue)
        runner = "lxbatch_runner.sh"
        theoutput = theoutput.replace('/pool/ciencias/','/pool/cienciasrw/')
    else: # Use lxbatch by default
        runner = options.runner
        super  = "bsub -q {queue}".format(queue = options.queue)

    basecmd = "{dir}/{runner} {dir} {cmssw} python {self} -j 0 -N {chunkSize} -T {tdir} -t {tree} {data} {output}".format(
                dir = os.getcwd(), runner=runner, cmssw = os.environ['CMSSW_BASE'],
                self=sys.argv[0], chunkSize=options.chunkSize, tdir=options.treeDir,
                tree=options.tree, data=args[0], output=theoutput)

    writelog = ""
    logdir   = ""
    if options.logdir: logdir = options.logdir.rstrip("/")

    if options.vectorTree: basecmd += " --vector "
    if options.useTRAv2:   basecmd += " --tra2 "
    friendPost =  "".join(["  -F  %s %s " % (fn,ft) for fn,ft in options.friendTrees])
    friendPost += "".join([" --FM %s %s " % (fn,ft) for fn,ft in options.friendTreesMC])
    friendPost += "".join([" --FD %s %s " % (fn,ft) for fn,ft in options.friendTreesData])
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
    else:
      for (name,fin,fout,data,range,chunk,fs) in jobs:
        if chunk != -1:
            if options.logdir: writelog = "-o {logdir}/{data}_{chunk}.out -e {logdir}/{data}_{chunk}.err".format(logdir=logdir, data=name, chunk=chunk)
            cmd = "{super} {writelog} {base} -d {data} -c {chunk} {post}".format(super=super, writelog=writelog, base=basecmd, data=name, chunk=chunk, post=friendPost)
            if options.queue == "batch":
                cmd = "echo \"{base} -d {data} -c {chunk} {post}\" | {super} {writelog}".format(super=super, writelog=writelog, base=basecmd, data=name, chunk=chunk, post=friendPost)
            if fs:
                cmd += " --fineSplit %d --subChunk %d" % (fs[1], fs[0])
        else:
            if options.logdir: writelog = "-o {logdir}/{data}.out -e {logdir}/{data}.err".format(logdir=logdir, data=name)
            cmd = "{super} {writelog} {base} -d {data} {post}".format(super=super, writelog=writelog, base=basecmd, data=name, chunk=chunk, post=friendPost)

            if options.queue == "batch":
                cmd = "echo \"{base} -d {data} {post}\" | {super} {writelog}".format(super=super, writelog=writelog, base=basecmd, data=name, chunk=chunk, post=friendPost)
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
    if options.vectorTree:
        tb.vectorTree = True
    else:
        tb.vectorTree = False

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
    el.loop([tb], eventRange=range)
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
        fcmd = open(fout[:fout.rfind("/")] + "/cmd/" + fout[fout.rfind("/")+1:].rstrip(".root") + "_command.txt", "w")
        fcmd.write("%s\n\n" % " ".join(sys.argv)) 
        fcmd.write("%s\n%s\n" % (args,options)) 
        fcmd.close()
    return (name,(nev,time))

if options.jobs > 0:
    from multiprocessing import Pool
    pool = Pool(options.jobs)
    ret  = dict(pool.map(_runIt, jobs)) if options.jobs > 0 else dict([_runIt(j) for j in jobs])
else:
    ret = dict(map(_runIt, jobs))
fulltime = maintimer.RealTime()
totev   = sum([ev   for (ev,time) in ret.itervalues()])
tottime = sum([time for (ev,time) in ret.itervalues()])
print "Done %d tasks in %.1f min (%d entries, %.1f min)" % (len(jobs),fulltime/60.,totev,tottime/60.)



