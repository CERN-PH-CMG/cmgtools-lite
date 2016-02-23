import sys
import ROOT

if sys.argv[1]==sys.argv[2]: raise RuntimeError

f = ROOT.TFile(sys.argv[1],"read")
t = f.Get('sf/t')
t.MakeProxy("run","eventBTagRWT.C")
t.Process("run.h+O",sys.argv[2])
