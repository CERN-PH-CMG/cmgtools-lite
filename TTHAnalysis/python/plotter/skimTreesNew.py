#!/usr/bin/env python
#from mcPlots import *
from CMGTools.TTHAnalysis.plotter.mcAnalysis import MCAnalysis, CutsFile, addMCAnalysisOptions, scalarToVector
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from collections import defaultdict
import os

def _runIt(args):
        (mysource,myoutpath,mycut,options) = args
        pp = PostProcessor(myoutpath,[mysource], postfix='',
                cut = mycut, 
                saveSelectionElist = options.elist,
                outputbranchsel = options.branchsel_out, 
                compression = options.compression,
                justcount = options.justcount,
                jsonInput = options.json)

        pp.run()

if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser(usage="%prog [options] mc.txt cuts.txt outputDir")
    parser.add_option("--json",        dest="json", type="string", default=None, help="JSON file selecting events to keep")
    parser.add_option("--pretend",    dest="pretend", default=False, action="store_true",  help="Pretend to skim, don't actually do it") 
    parser.add_option("--new","--skip-existing", dest="skipExisting", default=False, action="store_true",  help="Don't skim samples that already exist in the output directory") 
    parser.add_option("--justcount",  dest="justcount", default=False, action="store_true",  help="Pretend to skim, up to the point of counting passing events") 
    parser.add_option("--skim-friends",  dest="skimFriends", default=False, action="store_true",  help="Also run skimFTrees") 
    parser.add_option("-z", "--compression",  dest="compression", type="string", default=("ZLIB:3"), help="Compression: none, or (algo):(level) ")
    parser.add_option("--elist", dest="elist", type="string", default="skimTrees_elist", help="Name of the skim elist (default: skimTrees_elist)")
    parser.add_option("--bo", "--branch-selection-output",  dest="branchsel_out", type="string", default=None, help="Branch selection output")
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

    tasks = []
    fname2cuts = defaultdict(set)
    fname2friends = {}
    for proc in mca.listProcesses():
        print "Process %s" % proc
        for tty in mca._allData[proc]:
            if options.skipExisting:
                if os.path.isfile("%s/%s.root" % (outdir, tty.cname())):
                    print "\t component %-40s [ skipped as it already exists ]" % tty.cname()
                    continue
                else:
                    print "\t component %-40s [ missing %s ]" % (tty.cname(), "%s/%s.root" % (outdir, tty.cname()))
            else:
                print "\t component %-40s" % tty.cname()
            if options.pretend: continue
            mysource = tty.fname()
            ttys = [ tty ]
            for (var,vdir,vtty) in tty.getTTYVariations():
                if (not var.isTrivial(vdir)) and var.changesSelection(vdir):
                    ttys.append(vtty)
            for tty in ttys:
                mycut = tty.adaptExpr(cut.allCuts(),cut=True)
                if options.doS2V: mycut  = scalarToVector(mycut)
                fname2cuts[mysource].add(mycut)
            friends = ""
            if len(options.friendTrees + options.friendTreesMC + options.friendTreesData) > 0:
                raise RuntimeError("Sorry, only friends specified with --Fs, --FMCs, --FDs are supported")
            for D in options.friendTreesSimple + ( options.friendTreesMCSimple if not tty._isdata else []) + ( options.friendTreesDataSimple if tty._isdata else[]):
                friends += ",%s/%s_Friend.root" % (D.replace('{P}',tty.basepath()), tty.cname())
            if mysource in fname2friends:
                if friends != fname2friends[mysource]:
                    raise RuntimeError("Inconsistent friends between %s and %s" % (friends, fname2friends[mysource]))
            else:
                fname2friends[mysource] = friends
    for fname,cuts in fname2cuts.iteritems():
        if len(cuts) > 1: mycut = "(" + (")||(".join(cuts)) + ")"
        else:             mycut = cuts.pop()
        src = fname + fname2friends[fname]
        tasks.append((src,outdir,mycut,options))
    if options.jobs == 0: 
        map(_runIt, tasks)
    else:
        from multiprocessing import Pool
        Pool(options.jobs).map(_runIt, tasks)
    if options.skimFriends and not (options.pretend or options.justcount):
        skimFTrees = os.path.expandvars("$CMSSW_BASE/src/CMGTools/TTHAnalysis/python/plotter/skimFTreesNew.py")
        if not os.path.isfile(skimFTrees): raise RuntimeError("missing skimFTreesNew")
        for D in options.friendTreesSimple + options.friendTreesMCSimple + options.friendTreesDataSimple:
            for P in options.path:
                d = D.replace("{P}",P)
                if not os.path.exists(d): continue
                os.system("python %s --elist %s %s %s  > /dev/null" % (skimFTrees, options.elist, outdir, d))
            print "Skimmed %s" % os.path.basename(D)

