# usage:  python w-helicity-13TeV/hadd_wy.py <input_folder> [<cut_name_ID>]
#
# first argument is list of folders with distributions for no or nominal selection
# second one, optional, is a key for the selection, which should be in some folder names
# See examples below

# script developed to work passing a folder containing other folders like the following:
# [mciprian@pccmsrm29 plotter]$ ls plots/gen/
# wgen_fullsel_minus         wgen_fullsel_pfmt30_plus   wgen_fullsel_pfmt40_plus   wgen_fullsel_pfmt50_plus  wgen_nosel_minus
# wgen_fullsel_pfmt30_minus  wgen_fullsel_pfmt40_minus  wgen_fullsel_pfmt50_minus  wgen_fullsel_plus         wgen_nosel_plus
# [mciprian@pccmsrm29 plotter]$ python w-helicity-13TeV/hadd_wy.py plots/gen/ pfmt
#
# it will create root files containing histograms with no selection and with any of the other selections (no pfmt or pfmtXX in this case)
#
# It works also in you have only nosel and nominal selection (4 folders). In this case, the second argument can be skipped

import sys, os
import ROOT, datetime, array
import re

inputdir = sys.argv[1]
# varcut = "pfmt"
# if varcut != "":
#     noAdditionalCut = False
# else:
#     noAdditionalCut = True

varcut = ""
noAdditionalCut = True
if len(sys.argv)>2:
    varcut = str(sys.argv[2])
    noAdditionalCut = False

#files = [ f for f in os.listdir(inputdir) if f.endswith('.root') ]
#files = list( [os.path.join(inputdir, f) for f in files] )

files = list()
for root, dirs, tmpfiles in os.walk(inputdir):
    for f in tmpfiles:
        if f.endswith(".root"):
            thisfile = os.path.join(root, f)
            print("Getting file --> %s " % str(thisfile))
            files.append(str(thisfile))

if len(files) > 4 and noAdditionalCut:
    print "==================================="
    print "WARNING: you have not specified any folder name tag, but I see more than 4 folders (%d)" % len(files)
    print "I cannot manage this situation correctly, please check. Exit"
    print "==================================="
    quit()

# for f in files:
#     print f
# quit()

helicities = ["right", "left", "long"]

tmpplots = []
varcut_thr_list = set([])
for f in files:
    print "Opening file: ",f
    tf = ROOT.TFile.Open(f)
    for k in tf.GetListOfKeys() :
        name=k.GetName()
        obj=k.ReadObj()
        #if '_wy_' in name and 'background' not in name and obj.InheritsFrom("TH1"):
        if '_wy_' in name and obj.InheritsFrom("TH1") and any(h in name for h in helicities):
            if 'fullsel' in f:
                tokens = name.split('_')
                if varcut != "" and varcut in f:
                    regex = re.compile(varcut+'([0-9]*)')
                    varcut_thr = regex.findall(f)
                    if len(varcut_thr):
                        #print int(varcut_thr[0])
                        varcut_thr_list.add(int(varcut_thr[0]))
                        newname = '_'.join( tokens[:2]+['reco_%s%d' % (varcut, int(varcut_thr[0]))]+tokens[2:] )                        
                else: 
                    newname = '_'.join( tokens[:2]+['reco']+tokens[2:] )
            else:
                newname = name
            newh = obj.Clone(newname)
            newh.SetDirectory(None)
            tmpplots.append(newh)
    #tf.Close()

outputfile = 'mc_reco_eff.root'
mergedFile = ROOT.TFile.Open(outputfile,'recreate')
mergedFile.cd()

print "#####################"
print "File ", outputfile
for p in tmpplots:
    if noAdditionalCut or varcut not in p.GetName():
        print "Writing histo: ",p.GetName()
        p.Write()
mergedFile.Close()


if not noAdditionalCut:

    print ""    
    print "thresholds for " + varcut + " cut: ",varcut_thr_list
    for thr in varcut_thr_list:
        outputfile = 'mc_reco_%s%d_eff.root' % (varcut, thr) 
        mergedFile = ROOT.TFile.Open(outputfile,'recreate')
        mergedFile.cd()
        print "#####################"
        print "File ", outputfile
        for p in tmpplots:
            if 'reco' not in p.GetName() or (str(thr) in p.GetName() and varcut in p.GetName()):
                tmpNameNoCut = p.GetName().replace("%s%d_" % (varcut, thr),"")
                print "%s%d: Writing histo: %s (original name --> %s)" % (varcut, thr, tmpNameNoCut, p.GetName())
                p.Write(tmpNameNoCut)
        mergedFile.Close()
    
