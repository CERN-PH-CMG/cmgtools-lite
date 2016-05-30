#!/usr/bin/env python
from CMGTools.TTHAnalysis.plotter.mcAnalysis import *
import sys, os, os.path

from searchBins import *
from math import hypot


## Trees -- skimmed with trig_base

Tdir = "/afs/desy.de/user/l/lobanov/public/CMG/SampLinks/MiniAODv2_hadrFlav_2p2fb/"
# MC
mcFTdir = "/afs/desy.de/user/l/lobanov/public/CMG/SampLinks/MiniAODv2_hadrFlav_2p2fb/Friends/MC/pu69mb_JECcentr/"
sigFTdir = "/afs/desy.de/user/l/lobanov/public/CMG/SampLinks/MiniAODv2_hadrFlav_2p2fb/T1tttt_Scan/../Friends/pu_69mb_allSF_wScale/"

# new data
dataFTdir = "/afs/desy.de/user/l/lobanov/public/CMG/SampLinks/MiniAODv2_hadrFlav_2p2fb/Friends/Data/trig_skim_2p2fb/"


#Dilepton stuff
#mcFTdir = "/nfs/dust/cms/user/kirschen/newSUSYStuff/CMSSW_7_4_12_patch4/src/CMGTools/SUSYAnalysis/macros/FreshFriends_V2"
#sigFTdir = "/nfs/dust/cms/user/kirschen/newSUSYStuff/CMSSW_7_4_12_patch4/src/CMGTools/SUSYAnalysis/macros/FreshFriends_V2/Signal"
#dataFTdir = "/nfs/dust/cms/user/kirschen/newSUSYStuff/CMSSW_7_4_12_patch4/src/CMGTools/SUSYAnalysis/macros/FreshFriends_V2/Data"




def addOptions(options):

    # LUMI (overwrite default 19/fb)
    if options.lumi > 19:
        options.lumi = 2.2

    # set tree options -- set only if not set in cmd line
    if options.path == "./":
        options.path = Tdir
        #options.friendTrees = [("sf/t",FTdir+"/evVarFriend_{cname}.root")]
        options.friendTreesMC = [("sf/t",mcFTdir+"/evVarFriend_{cname}.root")]
        options.friendTreesData = [("sf/t",dataFTdir+"/evVarFriend_{cname}.root")]
    options.tree = "treeProducerSusySingleLepton"

    # extra options
    options.doS2V = True
    options.weight = True
    options.final  = True
    options.allProcesses  = True
    #options.maxEntries = 1000

    # signal scan
    if options.signal:
        options.var =  "mLSP:mGo*(nEl-nMu)"
        #options.bins = "60,-1500,1500,30,0,1500"
        #options.bins = "34,-1700,1700,10,0,1500"
        options.bins = "161,-2012.5,2012.5,81,-12.5,2012.5"

        options.friendTreesMC = [("sf/t",sigFTdir+"/evVarFriend_{cname}.root")]
        options.cutsToAdd += [("base","Selected","Selected == 1")] # make always selected for signal

    elif options.grid:
        options.var =  "Selected:(nEl-nMu)"
        #options.bins = "3,-1.5,1.5,2,-1.5,1.5"
        options.bins = "5,-2.5,2.5,2,-1.5,1.5"#to cover dilept. as well will have to write content of 0 bin to 4th bin... to also cover for mixed case #CAVEAT/TOFIX: IGNORING ELE/MU mixed case for now (overwritten later with ele+mu)

    elif options.plot:

        options.cutsToAdd += [("base","Selected","Selected == 1")] # make always selected for plots

        #options.var/bins must be setup by user
        if options.var == "LT":
            options.bins = "[250,350,450,600,1200]"
        elif options.var == "HT":
            options.bins = "[500,750,1000,1250,1600]"
        elif options.var == "nTrueInt":
            options.bins = "20,0,20"
        elif options.var == "puRatio":
            options.bins = "200,0,200"
            #options.bins = "25,500,1500"

def makeLepYieldGrid(hist, options):

    for ybin in range(1,hist.GetNbinsY()+1):
        ymu = hist.GetBinContent(1,ybin)+hist.GetBinContent(2,ybin) #this is ok as only one of the two bins will be filled for both nLep=1/2
        yele = hist.GetBinContent(4,ybin)+hist.GetBinContent(5,ybin) #this is ok as only one of the two bins will be filled for both nLep=1/2
        yDLMix = hist.GetBinContent(3,ybin)
        #reshuffling to preserve the nEl=nMu=1 information separately for the dilepton case
        
        print hist.GetBinError(1,ybin), hist.GetBinError(2,ybin), hist.GetBinError(3,ybin), hist.GetBinError(4,ybin), hist.GetBinError(5,ybin)

        ymuErr = hist.GetBinError(1,ybin)+hist.GetBinError(2,ybin) #this is ok as only one of the two bins will be filled for both nLep=1/2
        yeleErr = hist.GetBinError(4,ybin)+hist.GetBinError(5,ybin)#this is ok as only one of the two bins will be filled for both nLep=1/2
        yDLMixErr = hist.GetBinError(3,ybin)

        # set MC errors to be sqrt(N)
        if options.mcPoissonErrors:
            #print "Setting Poisson errors for MC"
            ymuErr = sqrt(ymu)
            yeleErr = sqrt(yele)
            yDLMixErr = sqrt(yDLMix)

        ylep = ymu+yele+yDLMix
        ylepErr = hypot(yDLMixErr,hypot(ymuErr,yeleErr))

        hist.SetBinContent(1,ybin,ymu)
        hist.SetBinError(1,ybin,ymuErr)

        hist.SetBinContent(2,ybin,ylep)
        hist.SetBinError(2,ybin,ylepErr)

        hist.SetBinContent(3,ybin,yele)
        hist.SetBinError(3,ybin,yeleErr)

        hist.SetBinContent(4,ybin,yDLMix)
        hist.SetBinError(4,ybin,yDLMixErr)

        hist.SetBinContent(5,ybin,0.)#unused for now
        hist.SetBinError(5,ybin,0.)#unused for now


        if options.verbose > 1:
            print 'Summary for', hist.GetName()
            print 'Mu yields:\t', ymu, ymuErr
            print 'Ele yields:\t', yele, yeleErr
            print 'Mu+Ele yields:\t', ylep, ylepErr
            print 'Mixed case (non-zero for dilepton only) yields:\t', yDLMix, yDLMixErr

def makeUpHist(hist, options):

    hist.SetName(hist.GetName().replace('x_','')) # replace x_

    if options.grid:
        hist.SetStats(0)

        hist.GetXaxis().SetTitle("")
        hist.GetYaxis().SetTitle("")

        hist.GetXaxis().SetBinLabel(1,"mu")
        hist.GetXaxis().SetBinLabel(2,"mu+ele")
        hist.GetXaxis().SetBinLabel(3,"ele")
        hist.GetXaxis().SetBinLabel(4,"DLMix")

        hist.GetYaxis().SetBinLabel(1,"anti")
        hist.GetYaxis().SetBinLabel(2,"selected")

        makeLepYieldGrid(hist, options)

    if options.signal:
        hist.SetStats(0)

        hist.GetXaxis().SetTitle("m_{#tildeg}")
        hist.GetYaxis().SetTitle("m_{LSP}")

def writeYields(options):

    addOptions(options)

    if options.verbose > 1:
        print options

    # make MCA and cut vars
    mca  = MCAnalysis(options.mcaFile,options)
    cuts = CutsFile(options.cutFile,options)

    if options.bin.endswith("_DLCR"):
        cuts = CutsFile(options.cutFileDL,options)

    print options.bin, cuts.allCuts()
        
    # make bin name and outdir names
    binname = options.bin
    if options.outdir == None:
        outdir = "test/"
    else:
        outdir = options.outdir

    # get report
    if options.pretend:
        report = []
    else:
        if options.verbose > 1: print cuts.allCuts()
        report = mca.getPlotsRaw("x", options.var, options.bins, cuts.allCuts(), nodata=options.asimov)

#    print mca._backgrounds
#    print mca.listBackgrounds()

    if not options.pretend and not options.systs:

        # add sum MC entry
        totalMC = []; ewkMC = []

        for p in mca.listBackgrounds():
            if p in report and 'TTdiLep' not in p and 'TTsemiLep' not in p and 'TTincl' not in p and 'DiLep_' not in p and 'T1ttt' not in p:
            #if p in report and 'TTdiLep' not in p and 'TTsemiLep' not in p:
                print 'adding for background',p
                totalMC.append(report[p])
                if 'QCD' not in p:
                    print 'adding for ewk', p
                    ewkMC.append(report[p])

        if len(totalMC) > 0:
            report['x_background'] = mergePlots("x_background", totalMC)
        if len(ewkMC) > 0:
            report['x_EWK'] = mergePlots("x_EWK", ewkMC)


    elif options.systs:
        names = mca.listBackgrounds()

        cnames = [] # list of all central samples
        labels = ["Up","up","down","Down","EWK","TTdiLep","TTsemiLep","TTincl","T1ttt","Env","RMS"] # labels to ignore
        for name in names:
            for lab in labels:
                if lab in name: break
            else:
                cnames.append(name)
        print cnames

        if len(cnames) > 0:
            sumnames = {}; ref = cnames[0]
            for name in names:
                if ref in name:
                    sumnames[name.replace(ref,"EWK")] = []

            print sumnames

            for name in sumnames:
                varname = name.replace("EWK","")
                for cname in cnames:
                    pname = cname + varname
                    print name, pname, cname, varname
                    sumnames[name].append(report[pname])

                report['x_'+ name] = mergePlots("x_"+name, sumnames[name])

    '''
    if options.asimov:
        tomerge = []
        for p in mca.listBackgrounds():
            if p in report: tomerge.append(report[p])
        report['data_obs'] = mergePlots(binname+"_data_obs", tomerge)
    #else:
    #    report['data_obs'] = report['data'].Clone(binname+"_data_obs")
    '''

    ydir = outdir+"/"
    if not os.path.exists(ydir): os.system("mkdir -p "+ydir)

    if not options.plot:
        foutname = ydir+binname+".yields.root"
    else:
        foutname = ydir+binname+".plots.root"

    workspace = ROOT.TFile.Open(foutname, "RECREATE")
    if options.verbose > 0:
        print 'Writing', foutname
        print 'Yields:'

    if not options.pretend:
        #for n,h in report.iteritems():
        # sort by hist names
        hlist = sorted(report.values(), key = lambda h: h.GetName())

        for h in hlist:
            makeUpHist(h,options)

            if options.verbose > 0 and options.grid:
                print "\t%s (%8.3f selected events)" % (h.GetName(),h.GetBinContent(2,2))
            if options.verbose > 0 and options.signal:
                print "\t%s (%8.3f total events)" % (h.GetName(),h.Integral())

            workspace.WriteTObject(h,h.GetName())
    workspace.Close()

    return 1

# dict of Nb cut and corresp. Nb weights
mcaName = {}
mcaName["NB1"] = "mca-MC_syst_btag_1b_NB1.txt"
mcaName["NB1i"] = "mca-MC_syst_btag_1b_NB1p.txt"
mcaName["NB2"] = "mca-MC_syst_btag_1b_NB2.txt"
mcaName["NB2i"] = "mca-MC_syst_btag_1b_NB2p.txt"
mcaName["NB3i"] = "mca-MC_syst_btag_1b_NB3p.txt"

nbNames = {"NB0":"0", "NB1":"1", "NB1i":"1p", "NB2":"2", "NB2i":"2p", "NB3":"3", "NB3i":"3p"}

#import shutil

def makeBtagMCA(nbbin = "NB1",options = None):#oldmca = "../systs/btag/mca-MC_syst_btag_1b_NBX.txt"):

    oldmca = options.mcaFile

    if "NBX" not in oldmca:
        print("Error! Provided MCA has no wildcard for NBX")
        return oldmca

    newmca = options.outdir + "/" + os.path.basename(oldmca)
    newmca = newmca.replace("NBX",nbbin)

    if os.path.exists(newmca): return newmca

    # copy old to new mca

    omca = open(oldmca,"r")
    nmca = open(newmca,"w")

    # replace NBX with real bin
    print "Created new mca for current NB cut:", newmca

    for line in omca.readlines():
        nline = line.replace("NBX",nbNames[nbbin])
        nmca.write(nline)

    omca.close()
    nmca.close()

    return newmca

def getBTagWstring(cuts, options):

    print "Cuts before NB check:", cuts

    nbcut = None

    # find NBcut and remove from cuts
    for cut in cuts:
        if "nBJet" in cut[2]:
            print cut
            nbcut = cut
            cuts.remove(cut)

    # make weight string
    if nbcut == None:
        return (cuts,bWgt)
    else:
        print "Removed NB cut", cuts

        #if nbcut[1] in mcaName: mca = mcaName[nbcut[1]]
        #print "Going to use weights", mca
        #mca = "../systs/btag/" + mca

        # auto mca
        mca =  makeBtagMCA(nbcut[1],options)
        print "Going to use weights", mca

    return (cuts,mca)

def submitJobs(args, nchunks, outdir = "./"):

    if not os.path.exists(outdir): os.makedirs(outdir)

    # make unique name for jobslist
    import time
    itime = int(time.time())
    jobListName = outdir+"/"+'jobList_%i.txt' %(itime)
    jobList = open(jobListName,'w')
    print 'Filling %s with job commands' % (jobListName)

    # not to run again
    if '-b' in args: args.remove('-b')

    # execute only one thread
    args += ['-j','1']

    for chunk in range(nchunks):
        chargs = args + ['-c',str(chunk)]
        runcmd = " ".join(str(arg) for arg in chargs )
        jobList.write(runcmd + '\n')

    # check log dir
    logdir = 'logs'
    if not os.path.exists(logdir): os.system("mkdir -p "+logdir)

    # submit job array on list
    subCmd = 'qsub -t 1-%s -o logs nafbatch_runner.sh %s' %(nchunks,jobListName)
    print 'Going to submit', nchunks, 'jobs with', subCmd
    os.system(subCmd)

    jobList.close()
    return 1

if __name__ == "__main__":

    from optparse import OptionParser
    parser = OptionParser()

    parser.usage = '%prog [options]'
    parser.description="""
    Make yields from trees
    """

    addMCAnalysisOptions(parser)

    # extra options for tty
    parser.add_option("--mca", dest="mcaFile",default="mca-Spring15.txt",help="MCA sample list")
    parser.add_option("--cuts", dest="cutFile",default="trig_base.txt",help="Baseline cuts file")
    parser.add_option("--cutsDL", dest="cutFileDL",default="trig_DLbase.txt",help="Baseline cuts file for dilepton CR")
    parser.add_option("--binname", dest="binname",default="test",help="Binname")

    # options for cards
    parser.add_option("--var", dest="var",default="1",help="Variable")
    parser.add_option("--bins", dest="bins",default="[0.5,1.5]",help="Histo Bins")

    # I/O options
    parser.add_option("-o",   "--out",    dest="outname", type="string", default=None, help="output name")
    parser.add_option("--od", "--outdir", dest="outdir", type="string", default=None, help="output name")

    # running options
    parser.add_option("-v","--verbose",  dest="verbose",  default=0,  type="int",    help="Verbosity level (0 = quiet, 1 = verbose, 2+ = more)")
    parser.add_option("--pretend", dest="pretend",default=False, action="store_true",help="pretend to do it")
    parser.add_option("--systs", dest="systs",default=False, action="store_true",help="run for systs")

    # Btag SF method selection
    parser.add_option("--btag1B", dest="doBtagMeth1b",default=False, action="store_true",help="use btag SF weight method 1B")

    # batch options
    parser.add_option("-c","--chunk", dest="chunk",type="int",default=None,help="Number of chunk")
    parser.add_option("-b","--batch", dest="batch",default=False, action="store_true", help="batch command for submission")
    parser.add_option("--jobList","--jobList", dest="jobListName",default="jobList.txt",help="job list name")

    # more options
    parser.add_option("--asimov", dest="asimov", action="store_true", default=False, help="Make Asimov pseudo-data")
    parser.add_option("--mcPoisson", dest="mcPoissonErrors", action="store_true", default=False, help="Make MC errors poisson")
    parser.add_option("--signal", dest="signal", action="store_true", default=False, help="Is signal scan")
    parser.add_option("--grid", dest="grid", action="store_true", default=False, help="Plot 2d grid: ele/mu vs selected/anti")

    # make normal plots
    parser.add_option("--plot", dest="plot", action="store_true", default=False, help="Do normal plot")

    # Read options and args
    (options,args) = parser.parse_args()

    if options.verbose > 0 and len(args) > 0:
        print 'Arguments', args

    if not os.path.exists(options.outdir): os.makedirs(options.outdir)

    # make cut list
    cDict = {}

    doDLCR = False

    doNjet6 = True
    if doNjet6:
        cDict.update(cutDictCR)
        cDict.update(cutDictSR)
        if doDLCR: cDict.update(cutDictDLCR)


    doNjet9 = True
    if doNjet9:
        cDict.update(cutDictSRf9)
        cDict.update(cutDictCRf9)
        if doDLCR: cDict.update(cutDictDLCRf9)


    doNjet5 = False
    if doNjet5:
        cDict.update(cutDictSRf5)
        cDict.update(cutDictCRf5)

    doFew = True
    if doFew:
        cDict.update(cutDictSRf68Few)
        cDict.update(cutDictCRf68Few)
        cDict.update(cutDictSRf9Few)
        cDict.update(cutDictCRf9Few)

#    print cutDict
    #cDict = cutQCDsyst #QCD

    #cDict = cutIncl #Inclusive
    #print sorted([k for k in cDict.keys() if "NB0i" in k])
    #print sorted([k for k in cDict.keys() if "NB1" in k])
    #exit(0)

    # for LT/HT plots
    #cDict = cutLTbinsSR
    #cDict.update(cutLTbinsCR)

    #print cDict.keys(); exit(0)

    '''
    d = {}

    for bin in cDict:
        if "NB1i" in bin: d[bin] = cDict[bin]
    cDict = d
    print cDict
    '''

    binList = sorted(cDict.keys())

#    doBtagMeth1b = True

    if options.batch:
        print "Going to prepare batch jobs..."
        subargs =  sys.argv
        submitJobs(subargs, len(binList),options.outdir)
        exit(0)

    print "Beginning processing locally..."
    if options.chunk == None:
        # execute all bins locally
        for idx,bin in enumerate(binList):
            cuts = cDict[bin]
            options.bin = bin

            if options.verbose > 0:
                print 80*'#'
                print 'Processing bin #%i/%i' %(idx,len(binList))
                print '%s with cuts' %(bin),
                for cut in cuts:
                    print cut[2],'+',
                print
            else:
                print '.',

            if options.doBtagMeth1b == True:
                (cuts,options.mcaFile) = getBTagWstring(cuts,options)
                print cuts,options.mcaFile

            options.cutsToAdd = cuts

            writeYields(options)
        print
    elif options.chunk < len(binList):
        # to test a single job
        bin = binList[options.chunk]
        idx = options.chunk

        cuts = cDict[bin]
        options.bin = bin

        if options.verbose > 0:
            print 80*'#'
            print 'Processing chunk #%i/%i' %(idx,len(binList))
            print '%s with cuts' %(bin),
            for cut in cuts:
                print cut[2],'+',
            print
        else:
            print '.',
        if options.verbose > 2:
            print 80*'#'
            for idx,bin in enumerate(binList):
                print 'Processing chunk #%i/%i' %(idx,len(binList))
                print '%s with cuts' %(bin),
                cuts = cDict[bin]
                for cut in cuts:
                    print cut[2],'+',
                print

        if options.doBtagMeth1b == True:
            (cuts,options.mcaFile) = getBTagWstring(cuts,options)
            print cuts,options.mcaFile

        options.cutsToAdd = cuts

        writeYields(options)
    else:
        print "Nothing to process!"

    print 'Finished'
