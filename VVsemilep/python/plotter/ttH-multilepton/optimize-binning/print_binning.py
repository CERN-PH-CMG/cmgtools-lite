import ROOT
import os
import sys

res = []
for myfile in sys.argv[1:]:
    x=[]
    f = ROOT.TFile(myfile)
    t = f.limit
    t.GetEntry(0)
    x.append(t.r_ttH)
    t.GetEntry(1)
    x.append(t.r_ttH)
    t.GetEntry(2)
    x.append(t.r_ttH)
    print myfile
    n=myfile.split('/')[-1].replace('higgsCombine','').split('.')[0].replace('m','-')
    res.append((n,x[0],x[1],x[2]))

for i in res:
    print i,' ---' if i[2]==max([x[2] for x in res]) else '',' +++' if i[3]==min([x[3] for x in res]) else '' 

