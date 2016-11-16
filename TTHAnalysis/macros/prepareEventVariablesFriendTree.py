#!/usr/bin/env python
import os.path, re, types, itertools, sys
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
    def analyze(self,event):
        for name,mod in self._modules:
            keyvals = mod(event)
            for B,V in keyvals.iteritems():
                setattr(self.t, B, V)
                setattr(event,  B, V)
        self.t.fill()


import os, itertools
from optparse import OptionParser
parser = OptionParser(usage="%prog [options] <TREE_DIR> <OUT>")
parser.add_option("-m", "--modules", dest="modules",  type="string", default=[], action="append", help="Run these modules");
parser.add_option("-d", "--dataset", dest="datasets",  type="string", default=[], action="append", help="Process only this dataset (or dataset if specified multiple times)");
parser.add_option("-D", "--dm", "--dataset-match", dest="datasetMatches",  type="string", default=[], action="append", help="Process only this dataset (or dataset if specified multiple times): REGEXP");
parser.add_option("-c", "--chunk",   dest="chunks",    type="int",    default=[], action="append", help="Process only these chunks (works only if a single dataset is selected with -d)");
parser.add_option("--subChunk", dest="subChunk",    type="int",    default=None, nargs=1, help="Process sub-chunk iof this chunk");
parser.add_option("--fineSplit", dest="fineSplit",    type="int",    default=None, nargs=1, help="Split each chunk in N subchunks");
parser.add_option("-N", "--events",  dest="chunkSize", type="int",    default=500000, help="Default chunk size when splitting trees");
parser.add_option("-j", "--jobs",    dest="jobs",      type="int",    default=1, help="Use N threads");
parser.add_option("-p", "--pretend", dest="pretend",   action="store_true", default=False, help="Don't run anything");
parser.add_option("-T", "--tree-dir",   dest="treeDir",     type="string", default="sf", help="Directory of the friend tree in the file (default: 'sf')");
parser.add_option("-q", "--queue",   dest="queue",     type="string", default=None, help="Run jobs on lxbatch instead of locally");
parser.add_option("-t", "--tree",    dest="tree",      default='ttHLepTreeProducerTTH', help="Pattern for tree name");
parser.add_option("-V", "--vector",  dest="vectorTree", action="store_true", default=True, help="Input tree is a vector");
parser.add_option("-F", "--add-friend",    dest="friendTrees",  action="append", default=[], nargs=2, help="Add a friend tree (treename, filename). Can use {name}, {cname} patterns in the treename")
parser.add_option("--FMC", "--add-friend-mc",    dest="friendTreesMC",  action="append", default=[], nargs=2, help="Add a friend tree (treename, filename) to MC only. Can use {name}, {cname} patterns in the treename")
parser.add_option("--FD", "--add-friend-data",    dest="friendTreesData",  action="append", default=[], nargs=2, help="Add a friend tree (treename, filename) to data trees only. Can use {name}, {cname} patterns in the treename")
parser.add_option("-L", "--list-modules",  dest="listModules", action="store_true", default=False, help="just list the configured modules");
parser.add_option("-n", "--new",  dest="newOnly", action="store_true", default=False, help="Make only missing trees");
parser.add_option("-I", "--import", dest="imports",  type="string", default=[], action="append", help="Modules to import");
parser.add_option("--log", "--log-dir", dest="logdir", type="string", default=None, help="Directory of stdout and stderr");
parser.add_option("--env",   dest="env",     type="string", default="lxbatch", help="Give the environment on which you want to use the batch system (lxbatch, psi)");
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

jobs = []
for D in glob(args[0]+"/*"):
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
        data =  any(x in short for x in "DoubleMu DoubleEl DoubleEG MuEG MuonEG SingleMu SingleEl".split()) # FIXME
        f = ROOT.TFile.Open(fname)
        t = f.Get(treename)
        if not t:
            print "Corrupted ",fname
            continue
        entries = t.GetEntries()
        f.Close()
        if options.newOnly:
            fout = "%s/evVarFriend_%s.root" % (args[1],short)
            if os.path.exists(fout):
                f = ROOT.TFile.Open(fname);
                t = f.Get(treename)
                if t.GetEntries() != entries:
                    print "Component %s has to be remade, mismatching number of entries (%d vs %d)" % (short, entries, t.GetEntries())
                    f.Close()
                else:
                    print "Component %s exists already and has matching number of entries (%d)" % (short, entries)
                    continue
        chunk = options.chunkSize
        if entries < chunk:
            print "  ",os.path.basename(D),("  DATA" if data else "  MC")," single chunk"
            jobs.append((short,fname,"%s/evVarFriend_%s.root" % (args[1],short),data,xrange(entries),-1,None))
        else:
            nchunk = int(ceil(entries/float(chunk)))
            print "  ",os.path.basename(D),("  DATA" if data else "  MC")," %d chunks" % nchunk
            for i in xrange(nchunk):
                if options.chunks != []:
                    if i not in options.chunks: continue
                if not options.fineSplit:
                    r = xrange(int(i*chunk),min(int((i+1)*chunk),entries))
                    jobs.append((short,fname,"%s/evVarFriend_%s.chunk%d.root" % (args[1],short,i),data,r,i,None))
                else:
                    ev_per_fs = int(ceil(chunk/float(options.fineSplit)))
                    for ifs in xrange(options.fineSplit):
                        if options.subChunk and ifs != options.subChunk: continue
                        r = xrange(i*chunk + ifs*ev_per_fs, min(i*chunk + min((ifs+1)*ev_per_fs, chunk),entries))
                        jobs.append((short,fname,"%s/evVarFriend_%s.chunk%d.sub%d.root" % (args[1],short,i,ifs),data,r,i,(ifs,options.fineSplit)))
print "\n"
print "I have %d task(s) to process" % len(jobs)

if options.queue:
    import os, sys

    runner = ""
    super = ""
    if options.env == "cern":
        runner = "lxbatch_runner.sh"
        super  = "bsub -q {queue}".format(queue = options.queue)
    elif options.env == "psi":
        super  = "qsub -q {queue} -N friender".format(queue = options.queue)
        runner = "psibatch_runner.sh"
    elif options.env == "oviedo":
        if options.queue != "":
            options.queue = "batch" 
        super  = "qsub -q {queue} -N happyTreeFriend".format(queue = options.queue)
        runner = "lxbatch_runner.sh"
        theoutput= args[1].replace('/pool/ciencias/','/pool/cienciasrw/')
    else:
        raise RuntimeError, "I do not know what to do. Where am I? Please set the [env] option"

    basecmd = "{dir}/{runner} {dir} {cmssw} python {self} -N {chunkSize} -T {tdir} -t {tree} {data} {output}".format(
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



