# usage:  python w-helicity-13TeV/hadd_wy.py ../../data/efficiency/

import sys, os
import ROOT, datetime, array

inputdir = sys.argv[1]
files = [ f for f in os.listdir(inputdir) if f.endswith('.root') ]
files = list( [os.path.join(inputdir, f) for f in files] )

tmpplots = []
outputfile = 'mc_reco_eff.root'
mergedFile = ROOT.TFile.Open(outputfile,'recreate')
for f in files:
    print "Opening file: ",f
    tf = ROOT.TFile.Open(f)
    for k in tf.GetListOfKeys() :
        name=k.GetName()
        obj=k.ReadObj()
        if '_wy_' in name and 'background' not in name and obj.InheritsFrom("TH1"):
            if 'fullsel' in f:
                tokens = name.split('_')
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
