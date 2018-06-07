#!/usr/bin/env python
#from mcPlots import *
from CMGTools.TTHAnalysis.plotter.mcAnalysis import *

import array
import json
from glob import glob
from collections import defaultdict
import re
import ROOT

class CheckEventVetoList:
    _store={}
    def __init__(self,fname):
        self.loadFile(fname)
        print 'Initialized CheckEventVetoList from %s'%fname
        self.name = fname.strip().split('/')[-1]
    def loadFile(self,fname):
        with open(fname, 'r') as f:
            for line in f:
                if len(line.strip()) == 0 or line.strip()[0] == '#': continue
                run,lumi,evt = line.strip().split(':')
                self.addEvent(int(run),int(lumi),long(evt))
    def addEvent(self,run,lumi,evt):
        if (run,lumi) not in self._store:
            self._store[(run,lumi)]=array.array('L')
        self._store[(run,lumi)].append(evt)
    def filter(self,run,lumi,evt):
        mylist=self._store.get((run,lumi),None)
        return ((not mylist) or (long(evt) not in mylist))

class JSONSelector:
    jsonmap = {}
    def __init__(self,jsonfile):
        self.name = "jsonSelector"
        J = json.load(open(jsonfile, 'r'))
        for r,l in J.iteritems():
            self.jsonmap[long(r)] = l
        print "Loaded JSON %s with %d runs\n" % (jsonfile, len(self.jsonmap))
    def filter(self,run,lumi,evt):
        try:
            lumilist = self.jsonmap[run]
            for (start,end) in lumilist:
                if start <= lumi and lumi <= end:
                    return True
            return False
        except KeyError:
            return False

def _runIt(args):
        (tty,mysource,myoutpath,mycut,options,selectors) = args
        mytree = tty.getTree()
        ntot  = mytree.GetEntries() 
        if not options.justcount: print "  Start  %-40s: %8d" % (tty.cname(), ntot)
        timer = ROOT.TStopwatch(); timer.Start()
        # now we do
        os.system("mkdir -p "+myoutpath)
        os.system("cp -r %s/skimAnalyzerCount %s/" % (mysource,myoutpath))
        os.system("mkdir -p %s/%s" % (myoutpath,options.tree))
        histo = ROOT.gROOT.FindObject("Count")
        histo_w = ROOT.gROOT.FindObject("SumGenWeights")
        if not options.oldstyle:
            fout = ROOT.TFile("%s/%s/tree.root" % (myoutpath,options.tree), "RECREATE", "", options.compression);
        else:
            fout = ROOT.TFile("%s/%s/%s_tree.root" % (myoutpath,options.tree,options.tree), "RECREATE", "", options.compression);
        mytree.Draw('>>elist',mycut)
        elist = ROOT.gDirectory.Get('elist')
        if not elist:
            elist = ROOT.TEventList('elist')
        if len(selectors)>0:
            mytree.SetBranchStatus("*",0)
            mytree.SetBranchStatus("run",1)
            mytree.SetBranchStatus("lumi",1)
            mytree.SetBranchStatus("evt",1)
            mytree.SetBranchStatus("isData",1)
            elistveto = ROOT.TEventList("vetoevents","vetoevents")
            for ev in xrange(elist.GetN()):
                tev = elist.GetEntry(ev)
                mytree.GetEntry(tev)
                if not mytree.isData:
                    print "You don't want to filter by event number on MC, skipping for this sample"
                    break
                for selector in selectors:
                    if not selector.filter(mytree.run,mytree.lumi,mytree.evt):
                        if not ('json' in selector.name): print 'Selector %s rejected tree entry %d (%d among selected): %d:%d:%d'%(selector.name,tev,ev,mytree.run,mytree.lumi,mytree.evt)
                        elistveto.Enter(tev)
                        break
            mytree.SetBranchStatus("*",1)
            elist.Subtract(elistveto)
            print '%d events survived vetoes'%(elist.GetN(),)
        if options.justcount:
            print "  As if it were Done   %-40s: %8d/%8d" % (tty.cname(), elist.GetN(), ntot)
            return

        # drop and keep branches
        for drop in options.drop: mytree.SetBranchStatus(drop,0)
        for keep in options.keep: mytree.SetBranchStatus(keep,1)
        for keep in options.lazyKeeps:
            if mytree.GetBranch(keep): mytree.SetBranchStatus(keep,1)
        f2 = ROOT.TFile("%s/selection_eventlist.root"%myoutpath,"recreate")
        f2.cd()
        elist.Write()
        f2.Close()
        fout.cd()
        mytree.SetEventList(elist)
        out = mytree.CopyTree('1')
        npass = out.GetEntries()
        friends = out.GetListOfFriends() or []
        while friends and friends.GetSize() > 0:
            out.RemoveFriend(friends.At(0).GetTree())
            friends = out.GetListOfFriends() or []
        fout.WriteTObject(out,options.tree if options.oldstyle else "tree")
        if histo: histo.Write()
        if histo_w: histo_w.Write()
        fout.Close(); timer.Stop()
        print "  Done   %-40s: %8d/%8d %8.1f min" % (tty.cname(), npass, ntot, timer.RealTime()/60.)


if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser(usage="%prog [options] mc.txt cuts.txt outputDir")
    parser.add_option("-D", "--drop",  dest="drop", type="string", default=[], action="append",  help="Branches to drop, as per TTree::SetBranchStatus") 
    parser.add_option("-K", "--keep",  dest="keep", type="string", default=[], action="append",  help="Branches to keep, as per TTree::SetBranchStatus") 
    parser.add_option("--oldstyle",    dest="oldstyle", default=False, action="store_true",  help="Oldstyle naming (e.g. file named as <analyzer>_tree.root)") 
    parser.add_option("--vetoevents",  dest="vetoevents", type="string", default=[], action="append",  help="File containing list of events to filter out")
    parser.add_option("--json",        dest="json", type="string", default=None, help="JSON file selecting events to keep")
    parser.add_option("--pretend",    dest="pretend", default=False, action="store_true",  help="Pretend to skim, don't actually do it") 
    parser.add_option("--justcount",  dest="justcount", default=False, action="store_true",  help="Pretend to skim, up to the point of counting passing events") 
    parser.add_option("--vf", "--vars-files", dest="varfiles",  type="string", default=[], action="append",  help="File from which to get a list of possibly-used branches; globs are allowed")
    parser.add_option("--skim-friends",  dest="skimFriends", default=False, action="store_true",  help="Also run skimFTrees") 
    parser.add_option("--compression",   dest="compression", type="int", default=1, help="Compression for output ROOT file")
    addMCAnalysisOptions(parser)
    (options, args) = parser.parse_args()
    options.weight = False
    options.final = True
    mca  = MCAnalysis(args[0],options)
    cut = CutsFile(args[1],options)
    outdir = args[2]

    print "Will write selected trees to "+outdir
    if not os.path.exists(outdir):
        os.system("mkdir -p "+outdir)

    selectors=[CheckEventVetoList(fname) for fname in options.vetoevents]
    if options.json: selectors.append(JSONSelector(options.json))

    options.lazyKeeps = []
    if options.varfiles:
        mykeeps = set(["run","lumi","evt","genWeight","xsec","isData"])
        def _process(vfname,_norecurse=set()):
            #sys.stderr.write("processing %s\n" % vfname)
            _norecurse.add(vfname)
            for line in open(vfname,'r'):
                mykeeps.update(re.findall(r"[A-Za-z_]\w+",line))
                for inc in re.findall("[\"'][A-Za-z0-9_\\-/\+]+\.txt[\"']",line):
                    vfn = inc[1:-1]
                    if vfn not in _norecurse and os.path.exists(vfn):
                        _process(vfn)
        _process(args[0]); _process(args[1])
        if options.variationsFile: _process(options.variationsFile)
        for vglob in options.varfiles:
            for vfname in glob(vglob):
                _process(vfname)
        for proc in mca.listProcesses():
            for tty in mca._allData[proc]:
                ttys = [ tty ]
                for (var,vdir,vtty) in tty.getTTYVariations():
                    if not var.isTrivial(vdir):
                        ttys.append(vtty)
                for tty in ttys:
                    mycut = tty.adaptExpr(cut.allCuts(),cut=True)
                    if options.doS2V: mycut  = scalarToVector(mycut)
                    mykeeps.update(re.findall(r"[A-Za-z_]\w+",tty.getWeightForCut("1")))
        if options.doS2V:
            keeps2 = set()
            for k in mykeeps:
                keeps2.add(re.sub(r"\[\d+\]","",scalarToVector(k)))
            mykeeps = keeps2
        options.lazyKeeps = list(mykeeps)
        #print sorted(options.lazyKeeps); exit();
        
    tasks = []
    fname2cuts = defaultdict(set)
    fname2out  = {}
    fname2tty  = {}
    for proc in mca.listProcesses():
        print "Process %s" % proc
        for tty in mca._allData[proc]:
            print "\t component %-40s" % tty.cname()
            if options.pretend: continue
            myoutpath = outdir+"/"+tty.cname()
            for path in options.path:
                mysource  = path+"/"+tty.cname()
                if os.path.exists(mysource): break
            ttys = [ tty ]
            for (var,vdir,vtty) in tty.getTTYVariations():
                if (not var.isTrivial(vdir)) and var.changesSelection(vdir):
                    ttys.append(vtty)
            for tty in ttys:
                mycut = tty.adaptExpr(cut.allCuts(),cut=True)
                if options.doS2V: mycut  = scalarToVector(mycut)
                fname2cuts[mysource].add(mycut)
            fname2out[mysource] = myoutpath
            fname2tty[mysource] = ttys[0]
    for fname,cuts in fname2cuts.iteritems():
        if len(cuts) > 1: mycut = "(" + (")||(".join(cuts)) + ")"
        else:             mycut = cuts.pop()
        tasks.append((fname2tty[fname],fname,fname2out[fname],mycut,options,selectors))
    if options.jobs == 0: 
        map(_runIt, tasks)
    else:
        from multiprocessing import Pool
        Pool(options.jobs).map(_runIt, tasks)
    if options.skimFriends and not (options.pretend or options.justcount):
        if not os.path.exists("skimFTrees.py"): raise RuntimeError("missing skimFTrees")
        for D in options.friendTreesSimple + options.friendTreesMCSimple + options.friendTreesDataSimple:
            for P in options.path:
                d = D.replace("{P}",P)
                if not os.path.exists(d): continue
                os.system("python skimFTrees.py %s %s %s > /dev/null" % (outdir, d, outdir))
            print "Skimmed %s" % os.path.basename(D)

