#!/usr/bin/env python
#from mcPlots import *
from CMGTools.TTHAnalysis.plotter.mcAnalysis import *

import array
import ROOT
from collections import defaultdict
import hashlib
def hx(string): 
    return hashlib.md5(string).hexdigest()

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

def findPs(tty,mycut,options,selectors,verbose=2,forceps=None):
        mytree = tty.getTree()
        ntot  = mytree.GetEntries() 
        #mytree.SetEntryList(None) # make sure things are clean
        #mytree.Draw('>>elist',mycut)
        #elist = ROOT.gDirectory.Get('elist')
        if len(options.vetoevents)>0:
            raise RuntimError, "Not implemented"
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
                        print 'Selector %s rejected tree entry %d (%d among selected): %d:%d:%d'%(selector.name,tev,ev,mytree.run,mytree.lumi,mytree.evt)
                        elistveto.Enter(tev)
                        break
            mytree.SetBranchStatus("*",1)
            elist.Subtract(elistveto)
            if verbose: print '%d events survived vetoes'%(elist.GetN(),)
        #mytree.SetEventList(elist)
        ### Now determine event yield & stat. uncertainty
        #print mycut,"\t",hx(mycut)
        evyield, err, nev2 = tty._getYield(mytree, mycut, cutNeedsPreprocessing=False)
        if evyield > 0:
            ps_abserr = floor((max(options.absAcc,tty.getOption('AllowPrescaleAbsAcc',default=0))/err)**2) 
            ps_relerr = floor((max(options.relAcc,tty.getOption('AllowPrescaleRelAcc',default=0))/(err/evyield))**2) 
            if forceps:
                ps = forceps
            else:
                ps = min(max(ps_abserr,ps_relerr,1), max(1,nev2/options.minEvents))
            #if verbose: print "%-60s:  entries %8d/%8d  yield %8.3f +- %8.3f (%.4f, %8d)  -> PS rel %5d, PS abs %5d, final %5d (%7d events)" % (tty.cname(), elist.GetN(), ntot, evyield, err, err/evyield, nev2, ps_relerr, ps_abserr, ps, elist.GetN()/ps)
            if ps > 1:
                if verbose > 1: print "%-60s:  entries %8d/%8d  yield %9.2f +- %8.2f (%.4f, %8d)  -> PS rel %5d, PS abs %5d, final %5d (%7d events)" % (tty.cname(), nev2, ntot, evyield, err, err/evyield, nev2, ps_relerr, ps_abserr, ps, nev2/ps)
                mycut_postps = "(%s) * ((evt %% %d) == 0)" % (mycut, ps)
                evyield_postps, err_postps, nev2_postps = tty._getYield(mytree, mycut_postps, cutNeedsPreprocessing=False)
                wfactor = float(evyield)/evyield_postps
                if verbose > 0: print "%-60s   entries %8d/%8d  yield %9.2f +- %8.2f (%.4f, %8d)  post prescale %d; upweight by %.3f" % ("", nev2_postps, ntot, evyield_postps, err_postps, err_postps/evyield_postps, nev2_postps, ps, wfactor)
                return (ps, wfactor, nev2_postps)
            else:
                if verbose > 0: print "%-60s:  entries %8d/%8d  yield %9.2f +- %8.2f (%.4f, %8d)  -> PS rel %5d, PS abs %5d, final %5d (%7d events)" % (tty.cname(), nev2, ntot, evyield, err, err/evyield, nev2, ps_relerr, ps_abserr, 1, nev2)
                return (1, 1.0, nev2)
        else:
            #if verbose: print "%-60s:  entries %8d/%8d " % (tty.cname(), elist.GetN(), ntot)
            if verbose > 0: print "%-60s:  entries %8d/%8d " % (tty.cname(), nev2, ntot)
            return (0, 1.0, 0)


def _runIt(args):
        print "in runIt"
        (tty,mysource,myoutpath,cut,mycut,options,selectors,ps,wfactor,nev) = args
        mytree = tty.getTree()
        ntot  = mytree.GetEntries() 
        timer = ROOT.TStopwatch(); timer.Start()
        # now we do
        os.system("mkdir -p "+myoutpath)
        os.system("mkdir -p %s/%s" % (myoutpath,options.tree))
        histo = ROOT.gROOT.FindObject("Count")
        if not options.oldstyle:
            fout = ROOT.TFile("%s/%s/tree.root" % (myoutpath,options.tree), "RECREATE");
        else:
            fout = ROOT.TFile("%s/%s/%s_tree.root" % (myoutpath,options.tree,options.tree), "RECREATE");
        mytree.SetEntryList(None) # make sure things are clean
        mycut = "(%s) && ((evt %% %d) == %d)" % (mycut, ps, options.psoffset) if ps!=0 else "(%s)"%mycut
        mytree.Draw('>>elist',mycut)
        elist = ROOT.gDirectory.Get('elist').Clone()
        if len(options.vetoevents)>0:
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
                        print 'Selector %s rejected tree entry %d (%d among selected): %d:%d:%d'%(selector.name,tev,ev,mytree.run,mytree.lumi,mytree.evt)
                        elistveto.Enter(tev)
                        break
            mytree.SetBranchStatus("*",1)
            elist.Subtract(elistveto)
            print '%d events survived vetoes'%(elist.GetN(),)
        # drop and keep branches
        for drop in options.drop: mytree.SetBranchStatus(drop,0)
        for keep in options.keep: mytree.SetBranchStatus(keep,1)
        mytree.SetEventList(elist)
        if ps > 1:
            pckfile_in  = "%s/skimAnalyzerCount/SkimReport.pck" % mysource
            pckobj_in   = pickle.load(open(pckfile_in,'r'))
            counters_in = dict(pckobj_in)
            counters_out = [ (k, w/wfactor) for (k,w) in counters_in.iteritems() ]
            os.mkdir("%s/skimAnalyzerCount" % myoutpath)
            pckfout = open("%s/skimAnalyzerCount/SkimReport.pck" % myoutpath, 'w')
            pickle.dump(counters_out, pckfout)
            pckfout.close()
        else:
            os.system("cp -r %s/skimAnalyzerCount %s/" % (mysource,myoutpath))
        f2 = ROOT.TFile("%s/selection_eventlist.root"%myoutpath,"recreate")
        f2.cd()
        elist.Write()
        f2.Close()
        fout.cd()
        out = mytree.CopyTree('1')
        npass = out.GetEntries()
        friends = out.GetListOfFriends() or []
        while friends and friends.GetSize() > 0:
            out.RemoveFriend(friends.At(0).GetTree())
            friends = out.GetListOfFriends() or []
        fout.WriteTObject(out,options.tree if options.oldstyle else "tree")
        if histo: histo.Write()
        fout.Close(); timer.Stop()
        print "  Done   %-40s: %8d/%8d %8.1f min" % (tty.cname(), npass, ntot, timer.RealTime()/60.)


if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser(usage="%prog [options] mc.txt cuts.txt outputDir")
    parser.add_option("-D", "--drop",  dest="drop", type="string", default=[], action="append",  help="Branches to drop, as per TTree::SetBranchStatus") 
    parser.add_option("-K", "--keep",  dest="keep", type="string", default=[], action="append",  help="Branches to keep, as per TTree::SetBranchStatus") 
    parser.add_option("--oldstyle",    dest="oldstyle", default=False, action="store_true",  help="Oldstyle naming (e.g. file named as <analyzer>_tree.root)") 
    parser.add_option("--vetoevents",  dest="vetoevents", type="string", default=[], action="append",  help="File containing list of events to filter out")
    parser.add_option("--pretend",     dest="pretend", default=False, action="store_true",  help="Pretend to skim, don't actually do it") 
    parser.add_option("--justcount",   dest="pretend", default=False, action="store_true",  help="Pretend to skim, up to the point of counting passing events") 
    parser.add_option("--consolidate", dest="consolidate", default="minps", type="string",  help="Consolidate N components: 'minps' = use minimum prescale, 'orps' = compute PS for the OR") 
    parser.add_option("--relAcc",      dest="relAcc", default=0.05, type="float",  help="Target this relative accuracy on the yields") 
    parser.add_option("--absAcc",      dest="absAcc", default=0.07, type="float",  help="Target this absolute accuracy on the yields") 
    parser.add_option("--minEv",       dest="minEvents", default=10, type="int",  help="Minimum number of events") 
    parser.add_option("--ps-offset",   dest="psoffset", default=0, type="int",  help="Offset on the prescale") 
    parser.add_option("-v", "--verbose",     dest="verbose", default=4, type="int",  help="Minimum number of events") 
    parser.add_option("--skim-friends",  dest="skimFriends", default=False, action="store_true",  help="Also run skimFTrees") 
    addMCAnalysisOptions(parser)
    (options, args) = parser.parse_args()
    options.final = True
    mca  = MCAnalysis(args[0],options)
    cut = CutsFile(args[1],options)
    outdir = args[2]

    print "Will write selected trees to "+outdir
    if not os.path.exists(outdir):
        os.system("mkdir -p "+outdir)

    selectors=[CheckEventVetoList(fname) for fname in options.vetoevents]

    tasks = []; ttys = defaultdict(list)
    # check whether I need to consolidate cuts
    for proc in mca.listProcesses():
        print "Process %s" % proc
        for tty in mca._allData[proc]:
            print "\t component %-40s" % tty.cname()
            ttys[tty.cname()].append((tty,tty._getCut(cut.allCuts()),proc))
    for ttyn in sorted(ttys.iterkeys()):
        ttycuts = ttys[ttyn]
        (tty, mycut,p) = ttycuts[0]
        myoutpath = outdir+"/"+tty.cname()
        for path in options.path:
            mysource  = path+"/"+tty.cname()
            if os.path.exists(mysource): break
        if len(ttycuts) > 1:
            if options.verbose > 2: print "Consolidating cuts for %s (%d different cuts), strategy = %s" % (ttyn, len(ttycuts), options.consolidate)
            #for ttyi, mycuti, proc in ttycuts: print "\t",proc,"\t",mycuti,"\t",hx(mycuti)
            if options.consolidate == 'minps':
                pses = [ findPs(tty,mycuti,options,selectors,verbose=options.verbose-2) for (ttyi,mycuti,p) in ttycuts ]
                pses_nonzero = [ p[0] for p in pses if p[0] != 0 ]
                ps = min(pses_nonzero) if len(pses_nonzero) else 1
                mycut = "(" + "||".join("((%s) != 0)" % c for (t,c,p) in ttycuts) + ")"
                (ps, wfactor, nev) = findPs(tty,mycut,options,selectors,forceps=ps)
            else:
                mycut = "(" + "||".join("((%s) != 0)" % c for (t,c,p) in ttycuts) + ")"
                (ps, wfactor, nev) = findPs(tty,mycut,options,selectors,verbose=options.verbose)
        else:
            (ps, wfactor, nev) = findPs(tty,mycut,options,selectors,verbose=options.verbose)
        tasks.append((tty,mysource,myoutpath,cut,mycut,options,selectors,ps,wfactor,nev))
    print "Total number of selected events: %d; largest contributors:" % sum((r[-1] for r in tasks), 0)
    for n,e in sorted([ (r[0].cname(), r[-1]) for r in tasks ], key = lambda p : p[1], reverse = True)[:20]:
        print "    %-40s: %8d" % (n,e)
    if options.pretend: exit()
    print "\n\n"
    if options.jobs == 0: 
        map(_runIt, tasks)
    else:
        raise RuntimeError, 'Multithreading crashes with skimTreesWithPrescales, please run with -j 0'
        from multiprocessing import Pool
        Pool(options.jobs).map(_runIt, tasks)
    if options.skimFriends:
        if not os.path.exists("skimFTrees.py"): raise RuntimeError("missing skimFTrees")
        for D in options.friendTreesSimple + options.friendTreesMCSimple + options.friendTreesDataSimple:
            for P in options.path:
                d = D.replace("{P}",P)
                if not os.path.exists(d): continue
                os.system("python skimFTrees.py %s %s %s > /dev/null" % (outdir, d, outdir))
            print "Skimmed %s" % os.path.basename(D)

