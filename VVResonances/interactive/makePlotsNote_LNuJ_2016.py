from CMGTools.VVResonances.plotting.RooPlotter import *
from start16 import *
directory='plots16'
lumi='7650'
period='2016'


def makePileup():
    canvas,h1,h2,legend,pt=compare(WJets_quark,data,"nVert","lnujj_LV_mass>0","lnujj_LV_mass>0",60,0,60,'number of vertices','','Simulation','Data')
    cmslabel_prelim(canvas,period,12)
    canvas.SaveAs(directory+"/nVert.pdf")
    canvas.SaveAs(directory+"/nVert.png")
    canvas.SaveAs(directory+"/nVert.root")
    

def makeLeptonPlots():
    

    plot=lnujjStack.drawStack("lnujj_l1_l_pt","&&".join([cuts['common'],cuts['mu']]),lumi,50,53,553,'#mu p_{T}','GeV')
    cmslabel_prelim(plot['canvas'],period,11)
    plot['canvas'].SaveAs(directory+"/muonPt.pdf")
    plot['canvas'].SaveAs(directory+"/muonPt.png")
    plot['canvas'].SaveAs(directory+"/muonPt.root")

    plot=lnujjStack.drawStack("lnujj_l1_l_eta","&&".join([cuts['common'],cuts['mu']]),lumi,42,-2.1,2.1,'#mu #eta','',2)
    cmslabel_prelim(plot['canvas'],period,11)
    plot['canvas'].SaveAs(directory+"/muonEta.pdf")
    plot['canvas'].SaveAs(directory+"/muonEta.png")
    plot['canvas'].SaveAs(directory+"/muonEta.root")


    plot=lnujjStack.drawStack("lnujj_l1_l_pt","&&".join([cuts['common'],cuts['e']]),lumi,50,120,520,'e p_{T}','GeV')
    cmslabel_prelim(plot['canvas'],period,11)
    plot['canvas'].SaveAs(directory+"/electronPt.pdf")
    plot['canvas'].SaveAs(directory+"/electronPt.png")
    plot['canvas'].SaveAs(directory+"/electronPt.root")

    plot=lnujjStack.drawStack("lnujj_l1_l_eta","&&".join([cuts['common'],cuts['e']]),lumi,50,-2.5,2.5,'e #eta','',1)
    cmslabel_prelim(plot['canvas'],period,11)
    plot['canvas'].SaveAs(directory+"/electronEta.pdf")
    plot['canvas'].SaveAs(directory+"/electronEta.png")
    plot['canvas'].SaveAs(directory+"/electronEta.root")



def makeJetMass(which,blinded):
    if blinded:
        addCut='lnujj_l2_{which}_mass<65||lnujj_l2_{which}_mass>145'.format(which=which)
    else:
        addCut='lnujj_l2_{which}_mass>0'

    plot=lnujjStack.drawStack("lnujj_l2_"+which+"_mass","&&".join([cuts['common'],cuts['nob'],addCut]),lumi,60,0,240,which+' mass','GeV')
    cmslabel_prelim(plot['canvas'],period,11)
    plot['canvas'].SaveAs(directory+"/{which}_mass_nob.pdf".format(which=which))
    plot['canvas'].SaveAs(directory+"/{which}_mass_nob.png".format(which=which))
    plot['canvas'].SaveAs(directory+"/{which}_mass_nob.root".format(which=which))


    plot=lnujjStack.drawStack("lnujj_l2_"+which+"_mass","&&".join([cuts['common'],cuts['b']]),lumi,60,0,240,which+' mass','GeV')
    cmslabel_prelim(plot['canvas'],period,11)
    plot['canvas'].SaveAs(directory+"/{which}_mass_b.pdf".format(which=which))
    plot['canvas'].SaveAs(directory+"/{which}_mass_b.png".format(which=which))
    plot['canvas'].SaveAs(directory+"/{which}_mass_b.root".format(which=which))



def makeTau21():
    plot=lnujjStack.drawStack("lnujj_l2_tau2/lnujj_l2_tau1","&&".join([cuts['common'],cuts['b'],'lnujj_l2_pruned_mass>60&&lnujj_l2_pruned_mass<100']),lumi,25,0,1.5,"#tau_{2}/#tau_{1}")
    cmslabel_prelim(plot['canvas'],period,11)
    plot['canvas'].SaveAs(directory+"/tau21_b.pdf")
    plot['canvas'].SaveAs(directory+"/tau21_b.png")
    plot['canvas'].SaveAs(directory+"/tau21_b.root")



    canvas,h1,h2,legend,pt=compare(QCD,data,"jj_l2_tau2/jj_l2_tau1","jj_l2_pruned_mass>60&&jj_l2_pruned_mass<100&&jj_LV_mass>1000&&(((HLT2_HT900||HLT2_HT800)&&run>100)||(run<100))&&Flag_goodVertices&&Flag_CSCTightHaloFilter&&Flag_HBHENoiseFilter&&Flag_HBHENoiseIsoFilter&&Flag_eeBadScFilter&&jj_nOtherLeptons==0","jj_l2_pruned_mass>60&&jj_l2_pruned_mass<100&&jj_LV_mass>1000&&(HLT2_HT900||HLT2_HT800)&&Flag_goodVertices&&Flag_CSCTightHaloFilter&&Flag_HBHENoiseFilter&&Flag_HBHENoiseIsoFilter&&Flag_eeBadScFilter&&jj_nOtherLeptons==0",75,0,1.5,'#tau_{2}/#tau_{1}','','Simulation','Data')
    cmslabel_prelim(canvas,period,11)
    canvas.SaveAs(directory+"/tau21_qcd.pdf")
    canvas.SaveAs(directory+"/tau21_qcd.png")
    canvas.SaveAs(directory+"/tau21_qcd.root")


#    plot=jjStack.drawStack("jj_l2_tau2/jj_l2_tau1",'jj_l2_pruned_mass>60&&jj_l2_pruned_mass<100&&jj_LV_mass>1000&&(HLT_HT900||HLT_HT800)&&Flag_goodVertices&&Flag_CSCTightHaloFilter&&Flag_HBHENoiseFilter&&Flag_HBHENoiseIsoFilter&&Flag_eeBadScFilter&&jj_nOtherLeptons==0',lumi,50,0,1,"#tau_{2}/#tau_{1}","",2)
#    cmslabel_prelim(plot['canvas'],period,11)
#    plot['canvas'].SaveAs(directory+"/tau21_qcd.pdf")
#    plot['canvas'].SaveAs(directory+"/tau21_qcd.png")
#    plot['canvas'].SaveAs(directory+"/tau21_qcd.root")




def makeWLPlots():
    plot=lnujjStack.drawStack("lnujj_l1_pt","&&".join([cuts['common'],cuts['mu']]),lumi,50,200,600,'W_{#mu} p_{T}','GeV')

    cmslabel_prelim(plot['canvas'],period,11)
    plot['canvas'].SaveAs(directory+"/WmuonPt.pdf")
    plot['canvas'].SaveAs(directory+"/WmuonPt.png")
    plot['canvas'].SaveAs(directory+"/WmuonPt.root")

    plot=lnujjStack.drawStack("lnujj_l1_mt","&&".join([cuts['common'],cuts['mu']]),lumi,50,0,150,'W_{#mu} M_{T}','GeV')
    cmslabel_prelim(plot['canvas'],period,11)
    plot['canvas'].SaveAs(directory+"/WmuonMT.pdf")
    plot['canvas'].SaveAs(directory+"/WmuonMT.png")
    plot['canvas'].SaveAs(directory+"/WmuonMT.root")

    plot=lnujjStack.drawStack("lnujj_l1_pt","&&".join([cuts['common'],cuts['e']]),lumi,50,200,600,'W_{e} p_{T}','GeV')
    cmslabel_prelim(plot['canvas'],period,11)
    plot['canvas'].SaveAs(directory+"/WelectronPt.pdf")
    plot['canvas'].SaveAs(directory+"/WelectronPt.png")
    plot['canvas'].SaveAs(directory+"/WelectronPt.root")

    plot=lnujjStack.drawStack("lnujj_l1_mt","&&".join([cuts['common'],cuts['e']]),lumi,50,0,150,'W_{e} M_{T}','GeV')
    cmslabel_prelim(plot['canvas'],period,11)
    plot['canvas'].SaveAs(directory+"/WelectronMT.pdf")
    plot['canvas'].SaveAs(directory+"/WelectronMT.png")
    plot['canvas'].SaveAs(directory+"/WelectronMT.root")



def makeVVPlots(blinded):
    if blinded:
        addCut='lnujj_l2_pruned_mass<65||lnujj_l2_pruned_mass>145'
    else:
        addCut='lnujj_l2_pruned_mass>0'

    plot=lnujjStack.drawStack("lnujj_LV_mass","&&".join([cuts['common'],cuts['mu'],addCut]),lumi,100,600,4000,'M_{VV}','GeV')
    cmslabel_prelim(plot['canvas'],period,11)
    plot['canvas'].SaveAs(directory+"/muonMVV.pdf")
    plot['canvas'].SaveAs(directory+"/muonMVV.png")
    plot['canvas'].SaveAs(directory+"/muonMVV.root")

    plot=lnujjStack.drawStack("lnujj_LV_mass","&&".join([cuts['common'],cuts['e'],addCut]),lumi,100,600,4000,'M_{VV}','GeV')
    cmslabel_prelim(plot['canvas'],period,11)
    plot['canvas'].SaveAs(directory+"/electronMVV.pdf")
    plot['canvas'].SaveAs(directory+"/electronMVV.png")
    plot['canvas'].SaveAs(directory+"/electronMVV.root")



def makeSignalMVVParamPlot(datacard,pdf,var='MLNuJ'):
    ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")
    F=ROOT.TFile(datacard)
    w=F.Get('w')
    frame=w.var(var).frame()
    for mass in [800,1200,1600,2000,2400,2800,3200,3600,4000]:
        w.var("MH").setVal(mass)
        w.pdf(pdf).plotOn(frame)
       

    frame.GetXaxis().SetTitle("M_{VV} (GeV)")
    frame.GetYaxis().SetTitle("a.u")
    frame.GetYaxis().SetTitleOffset(1.35)
    frame.SetTitle('')
    canvas=ROOT.TCanvas("c")
    canvas.cd()
    frame.Draw()
    cmslabel_sim(canvas,period,12)
    canvas.Update()
    canvas.SaveAs(directory+"/MVVParam.png")
    canvas.SaveAs(directory+"/MVVParam.pdf")
    canvas.SaveAs(directory+"/MVVParam.root")


def getMJJParams(filename,newname):
    F=ROOT.TFile(filename)
    canvas=F.Get('c')
    canvas.SetRightMargin(0.04)
    cmslabel_sim(canvas,period,12)
    canvas.Update()
    canvas.SaveAs(directory+"/"+newname+".png")
    canvas.SaveAs(directory+"/"+newname+".pdf")
    canvas.SaveAs(directory+"/"+newname+".root")


def makeShapeUncertaintiesMJJ(filename,sample,tag,syst):
    #MJJ
    f=ROOT.TFile(filename)
    hN = f.Get("histo").ProjectionY("nominal")
    hU = f.Get("histo_"+syst+"_"+sample+"_"+tag+"Up").ProjectionY("up")
    hD = f.Get("histo_"+syst+"_"+sample+"_"+tag+"Down").ProjectionY("down")
    hN.SetLineColor(ROOT.kBlack)
    hN.SetLineStyle(1)
    hN.SetLineWidth(2)
    hU.SetLineColor(ROOT.kBlack)
    hU.SetLineStyle(3)
    hU.SetLineWidth(2)

    hD.SetLineColor(ROOT.kBlack)
    hD.SetLineStyle(4)
    hD.SetLineWidth(2)

    c=ROOT.TCanvas("c")
    c.cd()
    frame=c.DrawFrame(40,0,160,0.07)
    frame.GetXaxis().SetTitle("M_{J} (GeV)")
    frame.GetYaxis().SetTitle("a.u")
    hN.Draw("HIST,SAME")
    hU.Draw("HIST,SAME")
    hD.Draw("HIST,SAME")
    cmslabel_sim(c,period,12)

#    cmslabel_sim(canvas,period,12)
    c.Update()
    c.SaveAs(directory+"/"+sample+"_"+syst+tag+".png")
    c.SaveAs(directory+"/"+sample+"_"+syst+tag+".root")
    c.SaveAs(directory+"/"+sample+"_"+syst+tag+".pdf")


def makeShapeUncertaintiesMVV(filename,sample,tag,syst):
    #MJJ
    f=ROOT.TFile(filename)
    hN = f.Get("histo").ProjectionX("nominal")
    hU = f.Get("histo_"+syst+"_"+sample+"_"+tag+"Up").ProjectionX("up")
    hD = f.Get("histo_"+syst+"_"+sample+"_"+tag+"Down").ProjectionX("down")
    hN.SetLineColor(ROOT.kBlack)
    hN.SetLineStyle(1)
    hN.SetLineWidth(2)
    hU.SetLineColor(ROOT.kBlack)
    hU.SetLineStyle(3)
    hU.SetLineWidth(2)

    hD.SetLineColor(ROOT.kBlack)
    hD.SetLineStyle(4)
    hD.SetLineWidth(2)

    c=ROOT.TCanvas("c")
    c.cd()
    frame=c.DrawFrame(600,0,4800,0.07)
    frame.GetXaxis().SetTitle("M_{VV} (GeV)")
    frame.GetYaxis().SetTitle("a.u")
    hN.Draw("HIST,SAME")
    hU.Draw("HIST,SAME")
    hD.Draw("HIST,SAME")
    cmslabel_sim(c,period,12)

#    cmslabel_sim(canvas,period,12)
    c.Update()
    c.SaveAs(directory+"/"+sample+"_"+syst+tag+".png")
    c.SaveAs(directory+"/"+sample+"_"+syst+tag+".root")
    c.SaveAs(directory+"/"+sample+"_"+syst+tag+".pdf")


def makeShapeUncertainties2D(filename,sample,tag,syst):
    #MJJ
    f=ROOT.TFile(filename)
    hN = f.Get("histo")
    hU = f.Get("histo_"+syst+"_"+sample+"_"+tag+"Up")
    hD = f.Get("histo_"+syst+"_"+sample+"_"+tag+"Down")
    hU.Divide(hN)
    hD.Divide(hN)


    c=ROOT.TCanvas("c")
    c.cd()
    hU.Draw("COLZ")
    c.SaveAs(directory+"/"+sample+"_"+syst+tag+"Up.png")
    c.SaveAs(directory+"/"+sample+"_"+syst+tag+"Up.root")
    c.SaveAs(directory+"/"+sample+"_"+syst+tag+"Up.pdf")

    c=ROOT.TCanvas("c")
    c.cd()
    hD.Draw("COLZ")
    c.SaveAs(directory+"/"+sample+"_"+syst+tag+"Down.png")
    c.SaveAs(directory+"/"+sample+"_"+syst+tag+"Down.root")
    c.SaveAs(directory+"/"+sample+"_"+syst+tag+"Down.pdf")
    



def makeSignalMJJParam(fileW,fileZ,purity='HP'):
    FW=ROOT.TFile(fileW)
    FZ=ROOT.TFile(fileZ)


    c=ROOT.TCanvas("c")
    frame=c.DrawFrame(800,70,4500,100)
    frame.GetXaxis().SetTitle("M_{X} (GeV)")
    frame.GetYaxis().SetTitle("#mu (GeV)")

    g1=FW.Get("mean")
    g1.SetName("mean1")
    g1.SetMarkerColor(ROOT.kRed)
    g1.SetMarkerStyle(20)
    g1.SetMarkerSize(0.8)
    g1.SetLineColor(ROOT.kRed)
    g1.Draw("Psame")

    g2=FZ.Get("mean")
    g2.SetName("mean2")
    g2.SetMarkerColor(ROOT.kBlue)
    g2.SetMarkerStyle(21)
    g2.SetMarkerSize(0.8)
    g2.SetLineColor(ROOT.kBlue)
    g2.Draw("Psame")


    l=ROOT.TLegend(0.6,0.7,0.9,0.8)
    l.AddEntry(g1,"X #rightarrow WW","p")
    l.AddEntry(g2,"X #rightarrow WZ","p")

    l.SetBorderSize(0)
    l.SetFillColor(ROOT.kWhite)
    l.Draw()

    cmslabel_sim(c,period,11)
    c.SaveAs(directory+"/"+purity+"MJJParam_mean.png")
    c.SaveAs(directory+"/"+purity+"MJJParam_mean.pdf")
    c.SaveAs(directory+"/"+purity+"MJJParam_mean.root")




    c=ROOT.TCanvas("c")
    frame=c.DrawFrame(800,0,4500,15)
    frame.GetXaxis().SetTitle("M_{X} (GeV)")
    frame.GetYaxis().SetTitle("#sigma (GeV)")

    g1=FW.Get("sigma")
    g1.SetName("sigma1")
    g1.SetMarkerColor(ROOT.kRed)
    g1.SetMarkerStyle(20)
    g1.SetMarkerSize(0.8)
    g1.SetLineColor(ROOT.kRed)
    g1.Draw("Psame")

    g2=FZ.Get("sigma")
    g2.SetName("sigma2")
    g2.SetMarkerColor(ROOT.kBlue)
    g2.SetMarkerStyle(21)
    g2.SetMarkerSize(0.8)
    g2.SetLineColor(ROOT.kBlue)
    g2.Draw("Psame")


    l=ROOT.TLegend(0.6,0.7,0.9,0.8)
    l.AddEntry(g1,"X #rightarrow WW","p")
    l.AddEntry(g2,"X #rightarrow WZ","p")

    l.SetBorderSize(0)
    l.SetFillColor(ROOT.kWhite)
    l.Draw()

    cmslabel_sim(c,period,11)
    c.SaveAs(directory+"/"+purity+"MJJParam_sigma.png")
    c.SaveAs(directory+"/"+purity+"MJJParam_sigma.pdf")
    c.SaveAs(directory+"/"+purity+"MJJParam_sigma.root")




    c=ROOT.TCanvas("c")
    frame=c.DrawFrame(800,0,4500,3)
    frame.GetXaxis().SetTitle("M_{X} (GeV)")
    frame.GetYaxis().SetTitle("#alpha")

    g1=FW.Get("alpha")
    g1.SetName("alpha1")
    g1.SetMarkerColor(ROOT.kRed)
    g1.SetMarkerStyle(20)
    g1.SetMarkerSize(0.8)
    g1.SetLineColor(ROOT.kRed)
    g1.Draw("Psame")

    g2=FZ.Get("alpha")
    g2.SetName("alpha2")
    g2.SetMarkerColor(ROOT.kBlue)
    g2.SetMarkerStyle(21)
    g2.SetMarkerSize(0.8)
    g2.SetLineColor(ROOT.kBlue)
    g2.Draw("Psame")


    l=ROOT.TLegend(0.6,0.7,0.9,0.8)
    l.AddEntry(g1,"X #rightarrow WW","p")
    l.AddEntry(g2,"X #rightarrow WZ","p")

    l.SetBorderSize(0)
    l.SetFillColor(ROOT.kWhite)
    l.Draw()

    cmslabel_sim(c,period,11)
    c.SaveAs(directory+"/"+purity+"MJJParam_alpha.png")
    c.SaveAs(directory+"/"+purity+"MJJParam_alpha.pdf")
    c.SaveAs(directory+"/"+purity+"MJJParam_alpha.root")





def makeTopMJJParam(fileW,purity='HP'):
    FW=ROOT.TFile(fileW)
    ROOT.gStyle.SetOptFit(0)

    c=ROOT.TCanvas("c")
    frame=c.DrawFrame(600,-20,1500,20)
    frame.GetXaxis().SetTitle("M_{VV} (GeV)")
    frame.GetYaxis().SetTitle("#mu offset (GeV)")

    g1=FW.Get("mean")
    g1.SetMarkerColor(ROOT.kRed)
    g1.SetMarkerStyle(20)
    g1.SetMarkerSize(0.8)
    g1.SetLineColor(ROOT.kRed)
    g1.Draw("Psame")

    cmslabel_sim(c,period,11)
    c.SaveAs(directory+"/"+purity+"topMJJParam_mean.png")
    c.SaveAs(directory+"/"+purity+"topMJJParam_mean.pdf")
    c.SaveAs(directory+"/"+purity+"topMJJParam_mean.root")



    c=ROOT.TCanvas("c")
    frame=c.DrawFrame(600,0,1500,5)
    frame.GetXaxis().SetTitle("M_{VV} (GeV)")
    frame.GetYaxis().SetTitle("#alpha_{R} (GeV)")

    g1=FW.Get("alpha2")
    g1.SetMarkerColor(ROOT.kRed)
    g1.SetMarkerStyle(20)
    g1.SetMarkerSize(0.8)
    g1.SetLineColor(ROOT.kRed)
    g1.Draw("Psame")
    cmslabel_sim(c,period,11)
    c.SaveAs(directory+"/"+purity+"topMJJParam_alphaR.png")
    c.SaveAs(directory+"/"+purity+"topMJJParam_alphaR.pdf")
    c.SaveAs(directory+"/"+purity+"topMJJParam_alphaR.root")



def makeBackgroundMVVParamPlot(datacard,pdf,var='MLNuJ',nametag='Wjets'):
    ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")
    F=ROOT.TFile(datacard)
    w=F.Get('w')
    frame=w.var(var).frame()
    masses={40:ROOT.kRed, 60:ROOT.kBlue, 80:ROOT.kMagenta, 100:ROOT.kOrange, 120:ROOT.kTeal, 140: ROOT.kBlack}

    l=ROOT.TLegend(0.6,0.4,0.8,0.9)
    for mass,color in sorted(masses.iteritems()):
        w.var("MJ").setVal(mass)
        w.pdf(pdf).plotOn(frame,ROOT.RooFit.LineColor(color),ROOT.RooFit.Name("curve_"+str(mass)))
        curve=frame.getCurve("curve_"+str(mass))
        l.AddEntry(curve,"M_{J} = "+str(mass)+" GeV","l")
      

    l.SetBorderSize(0)
    l.SetFillColor(ROOT.kWhite)

    frame.GetXaxis().SetTitle("M_{VV} (GeV)")
    frame.GetYaxis().SetTitle("a.u")
    frame.GetYaxis().SetTitleOffset(1.35)
    canvas=ROOT.TCanvas("c")
    canvas.cd()    
    frame.Draw()
    cmslabel_sim(canvas,period,11)
    canvas.Update()
    l.Draw()
    canvas.SaveAs(directory+"/"+nametag+"MVVParam.png")
    canvas.SaveAs(directory+"/"+nametag+"MVVParam.pdf")
    canvas.SaveAs(directory+"/"+nametag+"MVVParam.root")
    






def makePostFit(card,MH,slices,bkgOnly=True,cut=''):
    ROOT.gSystem.Load('libHiggsAnalysisCombinedLimit')
    plotter=RooPlotter(card)    
    plotter.fix("MH",MH)
    if bkgOnly:
        plotter.fix("r",0.0)
    else:
        plotter.addContribution("XWW",True,"X #rightarrow WW",3,1,ROOT.kOrange+10,0,ROOT.kWhite)
    plotter.prefit()


    plotter.addContribution("topRes",False," t#bar{t} (W)",2,1,ROOT.kBlack,1001,ROOT.kTeal-1)
    plotter.addContribution("WW",False,"SM WW",2,1,ROOT.kBlack,1001,ROOT.kOrange)
    plotter.addContribution("WZ",False,"SM WZ",2,1,ROOT.kBlack,1001,ROOT.kOrange+10)
    plotter.addContribution("Wjets",False,"V+jets",2,1,ROOT.kBlack-3,1001,ROOT.kAzure-9,"_opt")
    plotter.addContribution("topNonRes",False,"t#bar{t} (other)",2,1,ROOT.kBlack,1001,ROOT.kSpring-5,"_opt")

    for s in slices:
        if s.find('nob')!=-1:
            blind=1
        else:
            blind=0
        plotter.drawStack("MJ","M_{j} (GeV)",s,cut,blind)
        cmslabel_prelim(plotter.canvas,period,11)
        plotter.canvas.SaveAs(directory+"/MJ_"+s+".png")
        plotter.canvas.SaveAs(directory+"/MJ_"+s+".pdf")
        plotter.canvas.SaveAs(directory+"/MJ_"+s+".root")
        plotter.drawStack("MLNuJ","M_{VV} (GeV)",s,cut,blind,1)
        cmslabel_prelim(plotter.canvas,period,11)
        plotter.canvas.SaveAs(directory+"/MVV_"+s+".png")
        plotter.canvas.SaveAs(directory+"/MVV_"+s+".pdf")
        plotter.canvas.SaveAs(directory+"/MVV_"+s+".root")


#makeTrigger()
#makePileup()
#makeLeptonPlots()
#makeJetMass('pruned',1)
#makeTau21()
#makeWLPlots()
#makeVVPlots(1)

#makeSignalMVVParamPlot("LNUJJ_2016/combined.root","XWW_MVV_b_mu_HP_13TeV")

#getMJJParams('LNUJJ_2016/debugLNuJJ_MJJ_Wjets_HP.root','Wjets_MJJ_HP')
#getMJJParams('LNUJJ_2016/debugLNuJJ_MJJ_Wjets_LP.root','Wjets_MJJ_LP')

#makeSignalMJJParam('LNUJJ_2016/LNuJJ_XWW_MJJ_HP.root','LNUJJ/LNuJJ_XWZ_MJJ_HP.root','HP')
#makeSignalMJJParam('LNUJJ_2016/LNuJJ_XWW_MJJ_HP.root','LNUJJ/LNuJJ_XWZ_MJJ_LP.root','LP')

#makeTopMJJParam("LNUJJ_2016/LNuJJ_MJJ_topRes_HP.root",'HP')
#makeTopMJJParam("LNUJJ_2016/LNuJJ_MJJ_topRes_LP.root",'LP')


#makeBackgroundMVVParamPlot("LNUJJ_2016/combinedSlow.root","Wjets_MVV_nob_mu_HP_13TeV",'MLNuJ','Wjets_mu_')
#makeBackgroundMVVParamPlot("LNUJJ_2016/combinedSlow.root","Wjets_MVV_nob_e_HP_13TeV",'MLNuJ','Wjets_e_')
#makePostFit("LNUJJ_2016/combined.root",2000,['nob_mu_HP_13TeV','nob_mu_LP_13TeV','nob_e_HP_13TeV','nob_e_LP_13TeV','b_mu_HP_13TeV','b_mu_LP_13TeV','b_e_HP_13TeV','b_e_LP_13TeV'],1)



#makeShapeUncertaintiesMJJ("LNUJJ_2016/LNuJJ_MVVHist_Wjets_mu_HP.root","Wjets","HP","slopeSystMJJ")
#makeShapeUncertaintiesMJJ("LNUJJ_2016/LNuJJ_MVVHist_Wjets_mu_HP.root","Wjets","HP","meanSystMJJ")
#makeShapeUncertaintiesMJJ("LNUJJ_2016/LNuJJ_MVVHist_Wjets_mu_HP.root","Wjets","HP","widthSystMJJ")

#makeShapeUncertaintiesMJJ("LNUJJ_2016/LNuJJ_MVVHist_Wjets_mu_LP.root","Wjets","LP","slopeSystMJJ")
#makeShapeUncertaintiesMJJ("LNUJJ_2016/LNuJJ_MVVHist_Wjets_mu_LP.root","Wjets","LP","meanSystMJJ")
#makeShapeUncertaintiesMJJ("LNUJJ_2016/LNuJJ_MVVHist_Wjets_mu_LP.root","Wjets","LP","widthSystMJJ")


#makeShapeUncertaintiesMVV("LNUJJ_2016/LNuJJ_MVVHist_Wjets_mu_HP.root","Wjets","mu","slopeSyst")
#makeShapeUncertaintiesMVV("LNUJJ_2016/LNuJJ_MVVHist_Wjets_mu_HP.root","Wjets","mu","meanSyst0")
#makeShapeUncertaintiesMVV("LNUJJ_2016/LNuJJ_MVVHist_Wjets_mu_HP.root","Wjets","mu","widthSyst")
makeShapeUncertainties2D("LNUJJ_2016/LNuJJ_MVVHist_Wjets_mu_HP.root","Wjets","mu","meanSyst1")
