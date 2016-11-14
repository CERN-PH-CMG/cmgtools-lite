from CMGTools.VVResonances.plotting.RooPlotter import *
from CMGTools.VVResonances.plotting.CMS_lumi import *

import ROOT
ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")







plotter=RooPlotter("combined.root")    
plotter.fix("MH",2000)
plotter.fix("r",0.0)
plotter.prefit()
#plotter.addContribution("XWW",True,"X #rightarrow WW",3,1,ROOT.kOrange+10,0,ROOT.kWhite)
plotter.addContribution("topRes",False," t#bar{t} (W)",2,1,ROOT.kBlack,1001,ROOT.kTeal-1)
plotter.addContribution("WW",False,"SM WW",2,1,ROOT.kBlack,1001,ROOT.kOrange)
plotter.addContribution("WZ",False,"SM WZ",2,1,ROOT.kBlack,1001,ROOT.kOrange+10)
plotter.addContribution("Wjets",False,"V+jets",2,1,ROOT.kBlack-3,1001,ROOT.kAzure-9,"_opt")
#plotter.addContribution("Wjets_quark",False,"V+jets(q)",2,1,ROOT.kBlack-3,1001,ROOT.kAzure-9)
#plotter.addContribution("Wjets_gluon",False,"V+jets(g)",2,1,ROOT.kBlack-3,1001,ROOT.kBlue+1)
plotter.addContribution("topNonRes",False,"t#bar{t} (other)",2,1,ROOT.kBlack,1001,ROOT.kSpring-5,"_opt")
plotter.drawStack("MJ","m_{j} [GeV]","nob_mu_HP_13TeV")
#




#plotter=RooPlotter("LNuJJ_topPreFit_HP.root")    
#plotter.prefit()
#plotter.addContribution("topRes",True,"t#bar{t}",1,1,ROOT.kRed,0,ROOT.kWhite)
#plotter.addContribution("topNonRes",False,"non-resonant t#bar{t}",1,1,ROOT.kBlack,1001,ROOT.kGreen-5)
#plotter.drawStack("MJ","m_{j} [GeV]","top_mu_HP_13TeV","top_mu_HP_13TeV")







