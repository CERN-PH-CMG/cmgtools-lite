import ROOT

from CMGTools.VVResonances.plotting.TreePlotter import TreePlotter
from CMGTools.VVResonances.plotting.MergedPlotter import MergedPlotter
from CMGTools.VVResonances.plotting.StackPlotter import StackPlotter



cuts={}

cuts['common'] = '(HLT_MU||HLT_ELE)&&Flag_goodVertices&&Flag_CSCTightHaloFilter&&Flag_HBHENoiseFilter&&Flag_HBHENoiseIsoFilter&&Flag_eeBadScFilter&&lnujj_nOtherLeptons==0'
cuts['mu'] = 'abs(lnujj_l1_l_pdgId)==13'
cuts['e'] = 'abs(lnujj_l1_l_pdgId)==11'
cuts['HP'] = 'lnujj_l2_tau2/lnujj_l2_tau1<0.6'
cuts['LP'] = 'lnujj_l2_tau2/lnujj_l2_tau1>0.6&&lnujj_l2_tau2/lnujj_l2_tau1<0.75'
cuts['nob'] = 'lnujj_nMediumBTags==0'
cuts['b'] = 'lnujj_nMediumBTags>0'

 

#create the W+jets plotters
wjPlotters=[]

for sample in ["WJetsToLNu_HT1200to2500","WJetsToLNu_HT2500toInf","WJetsToLNu_HT400to600","WJetsToLNu_HT600to800","WJetsToLNu_HT800to1200",'WJetsToLNu_HT100to200','WJetsToLNu_HT200to400']:
    wjPlotters.append(TreePlotter('samples/'+sample+'.root','tree'))
    wjPlotters[-1].setupFromFile('samples/'+sample+'.pck')
    wjPlotters[-1].addCorrectionFactor('xsec','tree')
    wjPlotters[-1].addCorrectionFactor('genWeight','tree')
    wjPlotters[-1].addCorrectionFactor('puWeight','tree')


WJets = MergedPlotter(wjPlotters)

tt=TreePlotter('samples/TTJets.root','tree')
tt.setupFromFile('samples/TTJets.pck')
tt.addCorrectionFactor('xsec','tree')
tt.addCorrectionFactor('genWeight','tree')
tt.addCorrectionFactor('puWeight','tree')




#create the Z+jets plotters

#zPlotters=[]
#for sample in ['DYJetsToLL_M50_HT100to200','DYJetsToLL_M50_HT200to400','DYJetsToLL_M50_HT400to600','DYJetsToLL_M50_HT600toInf']:  
#    zPlotters.append(TreePlotter('samples/'+sample+'.root','tree'))
#    zPlotters[-1].setupFromFile('samples/'+sample+'.pck')
#    zPlotters[-1].addCorrectionFactor('xsec','tree')
#    zPlotters[-1].addCorrectionFactor('genWeight','tree')
#    zPlotters[-1].addCorrectionFactor('puWeight','tree')
#ZJets = MergedPlotter(zPlotters)



gPlotters=[]
for sample in ['GJets_HT100to200','GJets_HT200to400','GJets_HT400to600','GJets_HT40to100','GJets_HT600toInf']:
    gPlotters.append(TreePlotter('samples/'+sample+'.root','tree'))
    gPlotters[-1].setupFromFile('samples/'+sample+'.pck')
    gPlotters[-1].addCorrectionFactor('xsec','tree')
    gPlotters[-1].addCorrectionFactor('genWeight','tree')
    gPlotters[-1].addCorrectionFactor('puWeight','tree')
GJets = MergedPlotter(gPlotters)



qcdPlotters=[]
for sample in ["QCD_HT1000to1500","QCD_HT1500to2000","QCD_HT2000toInf","QCD_HT200to300","QCD_HT300to500","QCD_HT500to700","QCD_HT700to1000"]:
    qcdPlotters.append(TreePlotter('samples/'+sample+'.root','tree'))
    qcdPlotters[-1].setupFromFile('samples/'+sample+'.pck')
    qcdPlotters[-1].addCorrectionFactor('xsec','tree')
    qcdPlotters[-1].addCorrectionFactor('genWeight','tree')
    qcdPlotters[-1].addCorrectionFactor('puWeight','tree')

QCD = MergedPlotter(qcdPlotters)



singleMu = TreePlotter('samples/SingleMuon_Run2015D_16Dec.root','tree')
singleEle = TreePlotter('samples/SingleElectron_Run2015D_16Dec.root','tree')
jet = TreePlotter('samples/JetHT_Run2015D_16Dec.root','tree')
met = TreePlotter('samples/MET_Run2015D_16Dec.root','tree')


dataEMUPlotters=[singleMu,singleEle]
dataJetPlotters=[jet]
dataMETPlotters=[met]


WWLNUJJ = TreePlotter('samples/BulkGravToWWToWlepWhad_narrow_4000.root','tree')
WWLNUJJ.setupFromFile('samples/BulkGravToWWToWlepWhad_narrow_4000.pck')
WWLNUJJ.addCorrectionFactor('xsec','tree')
WWLNUJJ.addCorrectionFactor('genWeight','tree')
WWLNUJJ.addCorrectionFactor('puWeight','tree')
WWLNUJJ.setFillProperties(0,ROOT.kWhite)
WWLNUJJ.setLineProperties(1,ROOT.kRed,3)


WZLNUJJ = TreePlotter('samples/WprimeToWZToWlepZhad_narrow_1000.root','tree')
WZLNUJJ.setupFromFile('samples/WprimeToWZToWlepZhad_narrow_1000.pck')
WZLNUJJ.addCorrectionFactor('xsec','tree')
WZLNUJJ.addCorrectionFactor('genWeight','tree')
WZLNUJJ.addCorrectionFactor('puWeight','tree')
WZLNUJJ.setFillProperties(0,ROOT.kWhite)
WZLNUJJ.setLineProperties(1,ROOT.kGreen+3,3)

WHLNUJJ = TreePlotter('samples/WprimeToWhToWlephbb_narrow_4000.root','tree')
WHLNUJJ.setupFromFile('samples/WprimeToWhToWlephbb_narrow_4000.pck')
WHLNUJJ.addCorrectionFactor('xsec','tree')
WHLNUJJ.addCorrectionFactor('genWeight','tree')
WHLNUJJ.addCorrectionFactor('puWeight','tree')
WHLNUJJ.setFillProperties(0,ROOT.kWhite)
WHLNUJJ.setLineProperties(1,ROOT.kBlue+3,3)


#Fill properties
WJets.setFillProperties(1001,ROOT.kAzure-9)
tt.setFillProperties(1001,ROOT.kGreen-5)
#ZJets.setFillProperties(1001,ROOT.kAzure+5)
GJets.setFillProperties(1001,ROOT.kYellow)
QCD.setFillProperties(1001,ROOT.kGray)



dataEMU = MergedPlotter(dataEMUPlotters)
dataJet = MergedPlotter(dataJetPlotters)


#Stack for lnu+J
lnujjStack = StackPlotter()
lnujjStack.addPlotter(QCD,"QCD","QCD multijet","background")
#lnujjStack.addPlotter(GJets,"GJets","#gamma+Jets","background")
lnujjStack.addPlotter(WJets,"WJets","W+Jets","background")
lnujjStack.addPlotter(tt,"tt","t#bar{t}","background")
lnujjStack.addPlotter(WWLNUJJ,"X1","X #rightarrow WW","signal")
lnujjStack.addPlotter(WZLNUJJ,"X2","X #rightarrow WZ","signal")
lnujjStack.addPlotter(WHLNUJJ,"X3","X #rightarrow WH","signal")
lnujjStack.addPlotter(dataEMU,"data_obs","Data","data")

#Stack for ll+J

#lljjStack = StackPlotter()
#lljjStack.addPlotter(tt,"tt","t#bar{t}","background")
#lljjStack.addPlotter(ZJets,"ZJets","Z+Jets","background")
#lljjStack.addPlotter(dataEMU,"data_obs","Data","data")

#jjStack = StackPlotter()
#jjStack.addPlotter(QCD,"QCD","QCD multijet","background")
#jjStack.addPlotter(tt,"tt","t#bar{t}","background")
#jjStack.addPlotter(dataJet,"data_obs","Data","data")


#ZNuNU not processed yet
#jjnunuStack = StackPlotter()
#jjnunuStack.addPlotter(QCD,"QCD","QCD multijet","background")
#jjnunuStack.addPlotter(tt,"tt","t#bar{t}","background")
#jjnunuStack.addPlotter(dataMET,"data_obs","Data","data")



