# usage:  python w-helicity-13TeV/hadd_wy.py ../../data/efficiency/ [<variable>]
# <variable> is an optional tag used to distinguish files based on the selection used to make them

import sys, os
import ROOT, datetime, array
import re

inputdir = sys.argv[1]
varcut = "pfmt"

#files = [ f for f in os.listdir(inputdir) if f.endswith('.root') ]
#files = list( [os.path.join(inputdir, f) for f in files] )

files = list()
for root, dirs, tmpfiles in os.walk(inputdir):
    for f in tmpfiles:
        if f.endswith(".root"):
            thisfile = os.path.join(root, f)
            print("Getting file --> %s " % str(thisfile))
            files.append(str(thisfile))

# for f in files:
#     print f
# quit()

helicities = ["right", "left", "long"]

tmpplots = []
outputfile = 'mc_reco_eff.root'
mergedFile = ROOT.TFile.Open(outputfile,'recreate')
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
                        newname = '_'.join( tokens[:2]+['reco_%s%d' % (varcut, int(varcut_thr[0]))]+tokens[2:] )                        
                else: 
                    newname = '_'.join( tokens[:2]+['reco']+tokens[2:] )
            else:
                newname = name
            newh = obj.Clone(newname)
            newh.SetDirectory(None)
            tmpplots.append(newh)
    #tf.Close()

mergedFile.cd()
for p in tmpplots:
    print "Writing histo: ",p.GetName()
    p.Write()
mergedFile.Close()
