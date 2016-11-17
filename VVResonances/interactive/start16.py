import ROOT
from CMGTools.VVResonances.plotting.TreePlotter import TreePlotter
from CMGTools.VVResonances.plotting.MergedPlotter import MergedPlotter
from CMGTools.VVResonances.plotting.StackPlotter import StackPlotter
from CMGTools.VVResonances.plotting.tdrstyle import *
setTDRStyle()
from  CMGTools.VVResonances.plotting.CMS_lumi import *



def compare(p1,p2,var,cut1,cut2,bins,mini,maxi,title,unit,leg1,leg2):
    canvas = ROOT.TCanvas("canvas","")
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetOptTitle(0)
    canvas.cd()
    legend = ROOT.TLegend(0.62,0.2,0.92,0.4,"","brNDC")
    legend.SetBorderSize(0)
    legend.SetLineColor(1)
    legend.SetLineStyle(1)
    legend.SetLineWidth(1)
    legend.SetFillColor(0)
    legend.SetFillStyle(0)
    legend.SetTextFont(42)


    h1=p1.drawTH1(var,cut1,"1",bins,mini,maxi,title,unit)
    h2=p2.drawTH1(var,cut2,"1",bins,mini,maxi,title,unit)
    h1.DrawNormalized("HIST")
    h2.DrawNormalized("SAME")
    legend.AddEntry(h1,leg1,"LF")
    legend.AddEntry(h2,leg2,"P")
    legend.Draw()

    pt =ROOT.TPaveText(0.1577181,0.9562937,0.9580537,0.9947552,"brNDC")
    pt.SetBorderSize(0)
    pt.SetTextAlign(12)
    pt.SetFillStyle(0)
    pt.SetTextFont(42)
    pt.SetTextSize(0.03)
#    text = pt.AddText(0.01,0.3,"CMS Preliminary 2016")
#    text = pt.AddText(0.25,0.3,"#sqrt{s} = 13 TeV")
    pt.Draw()   


    return canvas,h1,h2,legend,pt


cuts={}

cuts['common'] = '(((HLT2_MU||HLT2_ELE||HLT2_ISOMU||HLT2_ISOELE||HLT2_MET120)&&run>2000)+(run<2000)*lnujj_sf)*(Flag_goodVertices&&Flag_CSCTightHaloFilter&&Flag_HBHENoiseFilter&&Flag_HBHENoiseIsoFilter&&Flag_eeBadScFilter&&lnujj_nOtherLeptons==0&&lnujj_l2_pruned_mass>0&&lnujj_LV_mass>600&&Flag_badChargedHadronFilter&&Flag_badMuonFilter&&(abs(lnujj_l1_l_pdgId)==11||(abs(lnujj_l1_l_pdgId)==13&&lnujj_l1_l_relIso04<0.1)))'


cuts['mu'] = '(abs(lnujj_l1_l_pdgId)==13)'
cuts['e'] = '(abs(lnujj_l1_l_pdgId)==11)'
cuts['HP'] = '(lnujj_l2_tau2/lnujj_l2_tau1<0.6)'
cuts['LP'] = '(lnujj_l2_tau2/lnujj_l2_tau1>0.6&&lnujj_l2_tau2/lnujj_l2_tau1<0.75)'
cuts['nob'] = '(lnujj_nMediumBTags==0)*lnujj_btagWeight'
cuts['b'] = '(lnujj_nMediumBTags>0)*lnujj_btagWeight'






#change the CMS_lumi variables (see CMS_lumi.py)
lumi_13TeV = "12.9 fb^{-1}"
lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)
iPeriod=4
iPos = 11





 

#create the W+jets plotters
wjPlotters=[]


for sample in ["WJetsToLNu_HT1200to2500","WJetsToLNu_HT2500toInf","WJetsToLNu_HT400to600","WJetsToLNu_HT600to800","WJetsToLNu_HT800to1200",'WJetsToLNu_HT100to200','WJetsToLNu_HT200to400']:
#for sample in ["WJetsToLNu_HT1200to2500","WJetsToLNu_HT2500toInf","WJetsToLNu_HT400to600","WJetsToLNu_HT600to800","WJetsToLNu_HT800to1200",'WJetsToLNu_HT100to200','WJetsToLNu_HT200to400']:
    wjPlotters.append(TreePlotter('samples/'+sample+'.root','tree'))
    wjPlotters[-1].setupFromFile('samples/'+sample+'.pck')
    wjPlotters[-1].addCorrectionFactor('xsec','tree')
    wjPlotters[-1].addCorrectionFactor('genWeight','tree')
    wjPlotters[-1].addCorrectionFactor('puWeight','tree')
#    wjPlotters[-1].addCorrectionFactor('0.82','flat')

WJets = MergedPlotter(wjPlotters)



ttO=TreePlotter('samples/TTJets.root','tree')
ttO.setupFromFile('samples/TTJets.pck')
ttO.addCorrectionFactor('xsec','tree')
ttO.addCorrectionFactor('genWeight','tree')
ttO.addCorrectionFactor('puWeight','tree')
ttO.addCorrectionFactor('(!(lnujj_l2_mergedVTruth==1&&lnujj_l2_nearestBDRTruth>0.8))','tree')

ttM=TreePlotter('samples/TTJets.root','tree')
ttM.setupFromFile('samples/TTJets.pck')
ttM.addCorrectionFactor('xsec','tree')
ttM.addCorrectionFactor('genWeight','tree')
ttM.addCorrectionFactor('puWeight','tree')
ttM.addCorrectionFactor('(lnujj_l2_mergedVTruth==1&&lnujj_l2_nearestBDRTruth>0.8)','tree')




qcdPlotters=[]
for sample in ["QCD_HT1000to1500","QCD_HT1500to2000","QCD_HT2000toInf","QCD_HT500to700","QCD_HT700to1000"]:
    qcdPlotters.append(TreePlotter('samples/'+sample+'.root','tree'))
    qcdPlotters[-1].setupFromFile('samples/'+sample+'.pck')
    qcdPlotters[-1].addCorrectionFactor('xsec','tree')
    qcdPlotters[-1].addCorrectionFactor('genWeight','tree')
    qcdPlotters[-1].addCorrectionFactor('puWeight','tree')

QCD = MergedPlotter(qcdPlotters)

singleMu = TreePlotter('samples/SingleMuon_Run2016B_PromptReco_v2.root','tree')
singleEle = TreePlotter('samples/SingleElectron_Run2016B_PromptReco_v2.root','tree')
jet = TreePlotter('samples/JetHT_Run2016B_PromptReco_v2.root','tree')
met = TreePlotter('samples/MET_Run2016B_PromptReco_v2.root','tree')

singleMuC = TreePlotter('samples/SingleMuon_Run2016C_PromptReco_v2.root','tree')
singleEleC = TreePlotter('samples/SingleElectron_Run2016C_PromptReco_v2.root','tree')
jetC = TreePlotter('samples/JetHT_Run2016C_PromptReco_v2.root','tree')
metC = TreePlotter('samples/MET_Run2016C_PromptReco_v2.root','tree')

singleMuD = TreePlotter('samples/SingleMuon_Run2016D_PromptReco_v2.root','tree')
singleEleD = TreePlotter('samples/SingleElectron_Run2016D_PromptReco_v2.root','tree')
jetD = TreePlotter('samples/JetHT_Run2016D_PromptReco_v2.root','tree')
metD = TreePlotter('samples/MET_Run2016D_PromptReco_v2.root','tree')

dataPlotters=[singleMu,singleEle,jet,met,singleMuC,singleEleC,metC,jetC,singleMuD,singleEleD,metD,jetD]



vvPlotters=[]
for sample in ['WWTo1L1Nu2Q','WZTo1L1Nu2Q']:
    vvPlotters.append(TreePlotter('samples/'+sample+'.root','tree'))
    vvPlotters[-1].setupFromFile('samples/'+sample+'.pck')
    vvPlotters[-1].addCorrectionFactor('xsec','tree')
    vvPlotters[-1].addCorrectionFactor('genWeight','tree')
    vvPlotters[-1].addCorrectionFactor('puWeight','tree')

vv=MergedPlotter(vvPlotters)



WWLNUJJ = TreePlotter('samples/VBF_RadionToWW_narrow_3000.root','tree')
WWLNUJJ.setupFromFile('samples/VBF_RadionToWW_narrow_3000.pck')
WWLNUJJ.addCorrectionFactor('xsec','tree')
WWLNUJJ.addCorrectionFactor(100,'flat')
WWLNUJJ.addCorrectionFactor('genWeight','tree')
WWLNUJJ.addCorrectionFactor('puWeight','tree')
WWLNUJJ.setFillProperties(0,ROOT.kWhite)
WWLNUJJ.setLineProperties(1,ROOT.kRed,3)


#Fill properties
WJets.setFillProperties(1001,ROOT.kAzure-9)
vv.setFillProperties(1001,ROOT.kOrange)
ttO.setFillProperties(1001,ROOT.kSpring-5)
ttM.setFillProperties(1001,ROOT.kTeal-1)
#ZJets.setFillProperties(1001,ROOT.kAzure+5)
#GJets.setFillProperties(1001,ROOT.kYellow)
QCD.setFillProperties(1001,ROOT.kGray)



data = MergedPlotter(dataPlotters)


#Stack for lnu+J
lnujjStack = StackPlotter()
#lnujjStack.addPlotter(QCD,"QCD","QCD multijet","background")
lnujjStack.addPlotter(ttO,"tt","t#bar{t} (other)","background")
lnujjStack.addPlotter(WJets,"WJets","W+Jets","background")
lnujjStack.addPlotter(ttM,"tt","t#bar{t} (W)","background")
lnujjStack.addPlotter(vv,"VV","SM WV","background")
#lnujjStack.addPlotter(WWLNUJJ,"X1","VBF X #rightarrow WW","signal")
#lnujjStack.addPlotter(WZLNUJJ,"X2","X #rightarrow WZ","signal")
#lnujjStack.addPlotter(WHLNUJJ,"X3","X #rightarrow WH","signal")
lnujjStack.addPlotter(data,"data_obs","Data","data")


jjStack = StackPlotter()
jjStack.addPlotter(QCD,"QCD","QCD multijet","background")
jjStack.addPlotter(data,"data_obs","Data","data")

