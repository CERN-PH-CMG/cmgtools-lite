#!/usr/bin/env python                                                                                                                                                        
from shutil import copyfile
import re, sys, os, os.path, subprocess, json, ROOT
import numpy as np

## open root file and make inclusive signal template (summing all rapidity bins and helicities)
## then copy them in a new file, adding also the other non-signal shapes

# python makeInclusiveWshape.py Wel_plus_shapes.root -o testMergeW/ -c plus -f el

from optparse import OptionParser
parser = OptionParser(usage="%prog [options] shapes.root ")
parser.add_option("-o", "--outdir",    dest="outdir", type="string", default="./", help="Output folder (current one as default)");
parser.add_option('-c','--charge', dest='charge', default='plus', type='string', help='process given charge (plus,minus): default is plus')
parser.add_option("-n", "--name",      dest="name",   type="string", default="", help="Name for output file (if not given, name is <oldname>_inclusiveW.root)");
parser.add_option("-f", "--flavour", dest="flavour", type="string", default='el', help="Channel: either 'el' or 'mu'");
(options, args) = parser.parse_args()

if len(sys.argv) < 1:
    parser.print_usage()
    quit()

if options.outdir != "./":
    if not os.path.exists(options.outdir):
        print "Creating folder", options.outdir
        os.system("mkdir -p " + options.outdir)
 
charge = options.charge
signalMatch = "W%s" % charge

# define systematics, then add also 60 pdf variations
sigVars = [ "nomi", "CMS_We_elescale", "alphaS", "wptSlope", "muR", "muF", "muRmuF"]
for i in range(1,61):
    sigVars.append("pdf%d" % i)

#print sigVars
#quit()

hWdict = {}
for var in sigVars:
    if var == "nomi": hWdict[var] = 0
    else:
        hWdict[var+"Up"] = 0
        hWdict[var+"Down"] = 0

endVars = [ "Down", "Up"]
helicities = [ "right", "left", "long"]

hists = []  # will contain the histograms to copy in output file


tf = ROOT.TFile.Open(args[0],"READ")

for k in tf.GetListOfKeys() :

    name=k.GetName()
    obj=k.ReadObj()
    if obj.InheritsFrom("TH1") and signalMatch in name and any(h in name for h in helicities):

        if any(ud in name for ud in endVars):
            syst = name.split('_')[-1]
            if "elescale" in syst: syst = "CMS_We_" + syst
        else:
            syst = "nomi"


        postfix = ("_"+syst) if syst != "nomi" else ""
        newname = 'x_W{ch}_{fl}{pfx}'.format(ch=charge,fl=options.flavour,pfx=postfix)
        if hWdict[syst] == 0:
            print "newname =", newname
            hWdict[syst] = obj.Clone(newname)
            hWdict[syst].SetDirectory(None)
            hists.append(hWdict[syst])
        else:
            hWdict[syst].Add(obj)            
    else:
        # copy all other objects
        obj.SetDirectory(None)
        hists.append(obj)

nInitialHists = len(tf.GetListOfKeys())
tf.Close()

inputfilename = args[0].split('/')[-1]            
if options.name == "":
    outfilename = inputfilename.replace(".root","_addInclW.root")
else:
    outfilename = options.name   
outputfile = options.outdir + "/" + outfilename

outFile = ROOT.TFile.Open(outputfile,'recreate')
outFile.cd()
print "#####################"
print "Writing new file", outputfile
for h in hists:
    print "Writing histo: ",h.GetName()
    h.Write()
print "---------------"
print "I wrote %d histograms (there were %d initially)" % (len(hists),nInitialHists)
outFile.Close()
