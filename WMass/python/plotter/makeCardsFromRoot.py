#!/usr/bin/env python                                                                                                                                                        
from shutil import copyfile
import re, sys, os, os.path, subprocess, json, ROOT
import numpy as np

from w_helicity_13TeV.make_diff_xsec_cards import getXYBinsFromGlobalBin
from w_helicity_13TeV.make_diff_xsec_cards import getArrayParsingString

## write datacard for counting experiment in each 2D template bin, using shapes from helicity datacards (after having summed up the signal components)
## python makeCardsFromRoot.py testMergeW_goodSyst/Wel_plus_shapes_addInclW.root [-2.5,-2.3,-2.1,-1.9,-1.7,-1.566,-1.4442,-1.3,-1.2,-1.1,-1.0,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.1,1.2,1.3,1.4442,1.566,1.7,1.9,2.1,2.3,2.5]*[30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45]  -o datacardWriterGoodSyst -f el -b Wel -s w-helicity-13TeV/wmass_e/systsEnv.txt --shape-syst-file w-helicity-13TeV/wmass_e/shapesystUtility.txt 

## old binning
# [-2.5,-2.25,-2.0,-1.8,-1.566,-1.4442,-1.3,-1.2,-1.1,-1.0,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.1,1.2,1.3,1.4442,1.566,1.8,2.0,2.25,2.5]*[30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45]

########################################
## shapesystUtility.txt is something like this
## ###############################
## #
## # names matches the histogram name in datacard (+ Up or Down)
## # 3rd field, if present, indicates that there are N variations (like for pfd, we have 60)
## #
## # ==================================================================
## # Fake rate uncertainties
## # Measurement of the fake rate: shapes (slope of FR)
## # ==================================================================
## CMS_We_FRe_pt        : data_fakes

## # ==================================================================
## # PDF and QCD scales
## # ==================================================================
## pdf                  : W.*|Z    : 60
## alphaS               : W.*|Z
## muR                  : W.*|Z
## muF                  : W.*|Z
## muRmuF               : W.*|Z

## # ==================================================================
## # W only
## # ==================================================================
## CMS_We_elescale      : W.*
## wptSlope             : W.*

#################################################################################
#################################################################################


from optparse import OptionParser
parser = OptionParser(usage="%prog [options] shapes.root binning")
parser.add_option("-o", "--outdir",    dest="outdir", type="string", default="./", help="Output folder (current one as default)");
parser.add_option("-n", "--name",      dest="name",   type="string", default="", help="Name for output datacard (if not given, name is <shapes>_card_<bin>.txt )");
parser.add_option("-f", "--flavour",   dest="flavour", type="string", default='el', help="Channel: either 'el' or 'mu'");
parser.add_option("-c", "--charge",    dest="charge", type="string", default='plus', help="Charge: either 'plus' or 'minus'");
parser.add_option("-b", "--bin",       dest="bin", default="ch1", type="string", help="name of the bin (the number of template bin used for each datacard is added to it)")
parser.add_option("-s", "--syst-file", dest="systfile", default="", type="string", help="File defining the systematics (only the constant ones are used)")
parser.add_option(      "--shape-syst-file", dest="shapesystfile", default="", type="string", help="File defining the systematics (only the constant ones are used)")
#parser.add_option(     "--netabins",  dest="netabins", default="38", type="int", help="Number of eta bins (or along x axis in general). Needed to associate global bin to 2D bin")
#parser.add_option(     "--nptbins", dest="nptbins", default="15", type="int", help="Number of pt bins (or along y axis in general)")
(options, args) = parser.parse_args()

if len(sys.argv) < 2:
    parser.print_usage()
    quit()

#nptbins = options.nptbins
#netabins = options.netabins

## open file and get number of bins in template by reading one key
#nTotBins = 1
# tf = ROOT.TFile.Open(args[0],"READ")
# for k in tf.GetListOfKeys() :
#     name=k.GetName()
#     obj=k.ReadObj()
#     if obj != 0 and obj.InheritsFrom("TH1"):
#         nTotBins = obj.GetNbinsX()
#         print "There are %d bins in the templates" % nTotBins
#         break
# tf.Close()


etabinning,ptbinning = args[1].split('*')    # args[1] is like "[a,b,c,...]*[d,e,f,...]", and is of type string. We need to get an array 
etabinning = getArrayParsingString(etabinning, makeFloat=True)
ptbinning = getArrayParsingString(ptbinning, makeFloat=True)
#tmpbinning = [float(x) for x in etabinning]  ## needed for constructor of TH2 below                                                                                      
#etabinning = tmpbinning
#tmpbinning = [float(x) for x in ptbinning]
#ptbinning = tmpbinning
nptbins = len(ptbinning)-1
netabins = len(etabinning)-1
nTotBins = (netabins)*(nptbins)
print "eta binning " + str(etabinning)
print "pt  binning " + str(ptbinning)
print "%d eta bins and %d pt bins (%d in total)" % (netabins, nptbins, nTotBins)
    
outdir = options.outdir
if not outdir.endswith('/'): outdir += "/"

if outdir != "./":
    if not os.path.exists(outdir):
        print "Creating folder", outdir
        os.system("mkdir -p " + outdir)

charge = options.charge
flavour = options.flavour
signalMatch = "W%s" % charge

## keep signal as the second (data will be removed from the datacard processes list, so signal is the first bin, which has number 0)
processes = ["data_obs", "W{ch}_{fl}".format(ch=charge, fl=flavour), "Z", "TauDecaysW", "Top", "DiBosons", "data_fakes"]
if flavour == "el": processes.append("Flips")

# hbin goes from 1 to TH1::GetNbinsX() included
for hbin in range(1,nTotBins+1):   

    binname = options.bin + "_%d" % hbin

    procBinContent = {}
    tf = ROOT.TFile.Open(args[0],"READ")
    ## get nominal integrals in the given bin
    for key in processes:
        hname = "x_%s" % key
        hist = tf.Get(hname)
        if not hist:
            raise RuntimeError('Unable to retrieve histogram named {hn}'.format(hn=hname))    
        else:           
            procBinContent[key] = hist.GetBinContent(hbin)
    tf.Close()

    cardname = options.name
    if cardname == "":
        shapename = args[0].split('.')[0]
        shapename = shapename.split('/')[-1] 
        cardname = outdir + shapename + "_card_bin" + str(hbin) + ".txt"

    card = open(cardname,'w')

    ieta,ipt = getXYBinsFromGlobalBin(hbin-1,netabins)
    card.write("### template bin = %d, ieta in [%.3g, %.3g], ipt in [%.3g, %.3g]\n" % (hbin,
                                                                                       etabinning[ieta],etabinning[ieta+1],
                                                                                       ptbinning[ipt],ptbinning[ipt+1]))
    card.write("imax 1\n")
    card.write("jmax *\n")
    card.write("kmax *\n")
    card.write("##-----------------------------\n")
    card.write("shapes * * FAKE\n")
    card.write("##-----------------------------\n")
    card.write("bin %s\n" % binname)
    card.write("observation %s\n" % procBinContent["data_obs"])
    card.write("##-----------------------------\n")

    processesNoData = [p for p in processes if p != "data_obs"]

    maxproclen = 0
    for proc in processes:
        if len(proc) > maxproclen:
            maxproclen = len(proc)
    klen = min(20,maxproclen + 3)
    kpatt = " %%%ds "  % klen
    card.write('bin                 %s \n' % ' '.join([kpatt % binname for p in processesNoData]))
    card.write('process             %s \n' % ' '.join([kpatt % p for p in processesNoData]))
    card.write('process             %s \n' % ' '.join([kpatt % str(i) for i in xrange(len(processesNoData))]))
    card.write('rate                %s \n' % ' '.join([kpatt % "{0:.3f}".format(procBinContent[key]) for key in processesNoData]))
    card.write("---------------------------------------------------------------------------------------\n")

    # now luminosity uncertainty and CMS_W, which are not in systfile
    lumipar = "1.026"  # 2.6%
    Wxsec   = "1.038"  # 3.8% 
    card.write(('%-16s lnN' % "CMS_lumi_13TeV") + ' '.join([kpatt % ("-"   if "data" in key else lumipar) for key in processesNoData]) + "\n")
    card.write(('%-16s lnN' % "CMS_W"         ) + ' '.join([kpatt % (Wxsec if "W"    in key else "-"    ) for key in processesNoData]) + "\n")

    # now other systematics
    #First those that are constant, from w-helicity-13TeV/wmass_e/systsEnv.txt
    #print "Now loading systematics"
    truebinname = binname  # this is just a dummy variable, it is used below to match binmap from the sysfile: as far as I know is always binmap='.*' (all bins)
    if options.systfile != "":
        sysfile = os.environ['CMSSW_BASE']+'/src/CMGTools/WMass/python/plotter/'+options.systfile
        systs = {}
        for line in open(sysfile, 'r'):
            if re.match("\s*#.*", line): continue
            line = re.sub("#.*","",line).strip()
            if len(line) == 0: continue
            field = [f.strip() for f in line.split(':')]
            #print field
            if len(field) < 4:
                raise RuntimeError, "Malformed line %s in file %s"%(line.strip(),sysfile)
            elif len(field) == 4 or field[4] == "lnN":
                (name, procmap, binmap, amount) = field[:4]
                if re.match(binmap+"$",truebinname) == None: continue
                if name not in systs: systs[name] = []
                systs[name].append((re.compile(procmap+"$"),amount))
        #print "Loaded %d systematics" % len(systs)

        for name in systs.keys():
            effmap = {}
            for p in processesNoData:
                effect = "-"
                for (procmap,amount) in systs[name]:
                    if re.match(procmap, p): effect = amount
                # if effect not in ["-","0","1"]:
                #     if "/" in effect:
                #         e1, e2 = effect.split("/")
                #         effect = "%.3f/%.3f" % (mca._projection.scaleSyst(name, float(e1)), mca._projection.scaleSyst(name, float(e2)))
                #     else:
                #         effect = str(mca._projection.scaleSyst(name, float(effect)))
                effmap[p] = effect
            systs[name] = effmap
        for name,effmap in systs.iteritems():
            card.write(('%-16s lnN' % name) + " ".join([kpatt % effmap[p]   for p in processesNoData]) +"\n")


    ## now the shape systematics
    systProc = {}  # associate array of processes to a given systematic (to write the datacard)
    if options.shapesystfile != "":
        shapesysfile = os.environ['CMSSW_BASE']+'/src/CMGTools/WMass/python/plotter/'+options.shapesystfile
        #print shapesysfile
        for line in open(shapesysfile, 'r'):
            if re.match("\s*#.*", line): continue
            line = re.sub("#.*","",line).strip()
            if len(line) == 0: continue
            field = [f.strip() for f in line.split(':')]
            #print field
            if len(field) >= 2: 
                systname = field[0]
                procmap = field[1]        
                for proc in processes:
                    if re.match(procmap, proc):            
                        varsyst = 1
                        if len(field)>2:
                            varsyst = int(field[2])
                        for i in range(varsyst):
                            systname_var = systname + (str(i+1) if varsyst > 1 else "")
                            if systname_var not in systProc: systProc[systname_var] = []
                            systProc[systname_var].append(proc)


    # check
    #for key,value in systProc.iteritems():
    #    print "%s  %s" % (key, value)
    #quit()

    ## open the root file again
    #sort pdf keys
    pdfsyst = [x for x in systProc if "pdf" in x]
    nonpdfsyst = [x for x in systProc if not "pdf" in x]
    #print pdfsyst
    #print nonpdfsyst
    sortedsyst = nonpdfsyst + ["pdf%d" % i for i in range(1,1+len(pdfsyst)) ]

    tf = ROOT.TFile.Open(args[0],"READ")
    dc_element = {}
    for syst in sortedsyst:
        for pr in systProc[syst]:
            hname = "x_%s" % pr
            hnomi = tf.Get(hname)
            hup = tf.Get("%s_%sUp" % (hname,syst))
            hdn = tf.Get("%s_%sDown" % (hname,syst))
            if not hnomi:
                raise RuntimeError, "I didn't find histogram %s"%hname
            if not hup:
                raise RuntimeError, "I didn't find histogram %s_%sUp" % (hname,syst)
            if not hdn:
                raise RuntimeError, "I didn't find histogram %s_%sDown" % (hname,syst)
            binContent = hnomi.GetBinContent(hbin)
            if binContent != 0.0:
                upVar = hup.GetBinContent(hbin)/binContent
                dnVar = hdn.GetBinContent(hbin)/binContent
                dc_element[syst,pr] = "%.3f/%.3f" % (dnVar,upVar)
            else:
                dc_element[syst,pr] = "1.0"

        card.write(('%-16s lnN' % syst) + " ".join([kpatt % (dc_element[syst,p] if p in systProc[syst] else "-") for p in processesNoData]) +"\n")

    tf.Close()

    ## define groups of systematics
    card.write("\n")
    card.write("pdfs group = %s\n\n" % ' '.join(["pdf%d" % i for i in range(1,1+len(pdfsyst))] ) )
    #card.write("pdfs group = %s\n\n" % ' '.join(pdf for pdf in pdfsyst ))
    card.write("scales group = muR muF muRmuF\n\n")
    card.write("alphaS group = alphaS\n\n")
    card.write("wpt group = wptSlope\n\n")
    card.write("frshape group = CMS_We_FRe_pt\n\n")

    card.write("\n")
    card.write("## THE END!\n")
    card.close()
