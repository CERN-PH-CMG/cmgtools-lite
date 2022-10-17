#!/usr/bin/env python
"""
makeLepTnPFriends.py

- Issues:
    > Fit plots are overwritten for each file when several files in one process
    > Could introduce another layer of caching for the raw mass histograms
"""

import sys, os, pickle
import ROOT

from array import array
from ROOT import TEfficiency
import os.path as osp

LUMI = 36.5
WEIGHT = "puWeight"
PAIRSEL = ("((pdgId*tag_pdgId==-11*11||pdgId*tag_pdgId==-13*13)"
           "&&abs(mass-91.)<30.&&abs(mcMatchId)>0)")
SELECTIONS = {
    'inclusive':               PAIRSEL,
    # mcMatchId is never ==1 for MC but always for data
    # 'runs (<= 275125)':        PAIRSEL+"&&(mcMatchId==1&&run<=275125)",
    # 'runs (>275125 <=275783)': PAIRSEL+"&&(mcMatchId==1&&run>275125&&run<=275783)",
    # 'runs (>275783 <=276384)': PAIRSEL+"&&(mcMatchId==1&&run>275783&&run<=276384)",
    # 'runs (>276384 <=276811)': PAIRSEL+"&&(mcMatchId==1&&run>276384&&run<=276811)",
    # 'singleTriggers': PAIRSEL+"&&passSingle",
    # 'doubleTriggers': PAIRSEL+"&&passDouble",
    # 'ttbar': "( (pdgId*tag_pdgId==-11*13)||"
    #           "  ( (pdgId*tag_pdgId==-11*11||pdgId*tag_pdgId==-13*13)"
    #           "&&abs(mass-91.)>15.&&met_pt>30.) )"
    #           "&&passDouble&&nJet25>=2&&nBJetLoose25>=2"
    #           "&&tag_pt>30&&abs(tag_mcMatchId)>0",
    # 'ttH'  : "abs(mcMatchId)>0&&passDouble",
}

LEPSEL = [
    ('eb', 'abs(pdgId)==11&&abseta<1.479',
           'Electrons Barrel (#eta < 1.479)'),
    ('ee', 'abs(pdgId)==11&&abseta>=1.479',
           'Electrons Endcap (#eta #geq 1.479)'),
    ('mb', 'abs(pdgId)==13&&abseta<1.2',
           'Muons Barrel (#eta < 1.2)'),
    ('me', 'abs(pdgId)==13&&abseta>=1.2',
           'Muons Endcap (#eta #geq 1.2)'),
]
## Eta binning for 2d plots:
LEPSEL2D = []
ETABINS2D_EL = [0,0.74,1.479,2.0,2.5]
for n in range(len(ETABINS2D_EL)-1):
    LEPSEL2D.append(('e%d'%n,
                   'abs(pdgId)==11&&abseta>={elo}&&abseta<{ehi}'.format(
                       elo=ETABINS2D_EL[n], ehi=ETABINS2D_EL[n+1]),
                   'Electrons {elo} #leq |#eta| < {ehi}'.format(
                       elo=ETABINS2D_EL[n], ehi=ETABINS2D_EL[n+1]) ) )

ETABINS2D_MU = [0,0.4,0.8,1.2,1.8,2.5]
for n in range(len(ETABINS2D_MU)-1):
    LEPSEL2D.append(('m%d'%n,
                   'abs(pdgId)==13&&abseta>={elo}&&abseta<{ehi}'.format(
                       elo=ETABINS2D_MU[n], ehi=ETABINS2D_MU[n+1]),
                   'Muons {elo} #leq |#eta| < {ehi}'.format(
                       elo=ETABINS2D_MU[n], ehi=ETABINS2D_MU[n+1]) ) )
LEPSEL.extend(LEPSEL2D)

MASSBINS  = range(61,122,1)
PTBINS    = [10.,15.,20.,25.,30.,37.5,45.,60.,80.,100.]
ETABINS   = [0.,0.25,0.50,0.75,1.00,1.25,1.50,2.00,2.50]
NVERTBINS = [0,4,7,8,9,10,11,12,13,14,15,16,17,19,22,25,30]
NJETBINS  = [0,1,2,3,4,5,6]
NBJETBINS = [0,1,2,3]
BINNINGS = [
    ('pt',            PTBINS,    'p_{T} [GeV]'),
    ('nVert',         NVERTBINS, 'N_{vertices}'),
#    ('nJet25',        NJETBINS,  'N_{jets}'),
#    ('nBJetMedium25', NBJETBINS, 'N_{bjets, CSVM}'),
]

DENOMINATOR = "passLoose" # or passFO?
NUMERATORS  = [
    ('2lss',"passTight&&passTCharge", 'same-sign 2 lepton definition'),
    ('3l',  "passTight", '3 lepton definition'),
]

INPUTS = {
    'data':[
        "Run2016",
        ],
    'DY':[
        "DYJetsToLL_M50_LO_ext_part1_treeProducerSusyMultilepton_tree",
        "DYJetsToLL_M50_LO_ext_part2_treeProducerSusyMultilepton_tree",
        "DYJetsToLL_M50_LO_ext_part3_treeProducerSusyMultilepton_tree",
        ],
    # 'ttbar':[
    #     "TTJets_DiLepton",
    #     "TTJets_SingleLeptonFromTbar_ext",
    #     "TTJets_SingleLeptonFromTbar",
    #     "TTJets_SingleLeptonFromT_ext",
    #     "TTJets_SingleLeptonFromT",
    #     ],
    # 'ttH':["TTHnobb"],
}

def getEfficiencyRatio(eff1, eff2, attributes_from_first=False):
    # This calculates eff1/eff2
    ratio = eff1.GetPassedHistogram().Clone("ratio")
    ratio.Sumw2()
    ratio.Divide(eff1.GetTotalHistogram())
    ratio.Multiply(eff2.GetTotalHistogram())
    ratio.Divide(eff2.GetPassedHistogram())
    # Pass on the attributes of the chosen argument
    for att in ['LineWidth','LineColor','MarkerStyle',
                'MarkerSize','MarkerColor']:
        if not attributes_from_first:
            getattr(ratio,'Set%s'%att)(getattr(eff2,'Get%s'%att)())
        else:
            getattr(ratio,'Set%s'%att)(getattr(eff1,'Get%s'%att)())
    return ratio

class EfficiencyPlot(object):
    """Simple class for making plots comparing TEfficiency objects"""
    def __init__(self, name):
        self.name = name
        self.effs = []
        self.effsforratio = []
        self.legentries = []
        self.plotformats = ['.pdf', '.png']
        self.xtitle = ''
        self.ytitle = 'MVA tight efficiency'
        self.tag = None
        self.tagpos = (0.92,0.35)
        self.subtag = None
        self.subtagpos = (0.92,0.29)

        self.colors = [ROOT.kBlack, ROOT.kAzure+1,
                       ROOT.kOrange+8, ROOT.kSpring-5]

        self.reference = None # reference for ratios
        self.invertratio = False
        self.ratiorange = (0.75, 1.15)

    def add(self,eff,tag,includeInRatio=True):
        self.effs.append(eff)
        self.legentries.append(tag)
        if includeInRatio:
            self.effsforratio.append(eff)

    def show(self, outname, outdir):
        ROOT.gROOT.SetBatch(1)
        ROOT.gStyle.SetOptTitle(0)
        ROOT.gStyle.SetOptStat(0)

        canv = ROOT.TCanvas("canv_%s"%(self.name), "efficiencies", 800, 800)
        canv.SetRightMargin(0.05)
        canv.SetTopMargin(0.05)

        rangex = (self.effs[0].GetTotalHistogram().GetXaxis().GetXmin(),
                  self.effs[0].GetTotalHistogram().GetXaxis().GetXmax())

        axes = ROOT.TH2D("axes_%s"%(self.name),"axes",
                         1, rangex[0], rangex[1], 1, 0.0, 1.0)
        axes.GetXaxis().SetTitle(self.xtitle)
        axes.GetYaxis().SetTitleOffset(1.2)
        axes.GetYaxis().SetTitle(self.ytitle)
        axes.Draw("axis")

        leg = ROOT.TLegend(.65,.15,.89,.30+0.037*max(len(self.effs)-3,0))

        leg.SetBorderSize(0)
        leg.SetFillColor(0)
        leg.SetFillStyle(0)
        leg.SetShadowColor(0)
        leg.SetTextFont(43)
        leg.SetTextSize(26)

        for eff,entry,color in zip(self.effs,self.legentries,self.colors):
            eff.SetLineColor(color)
            eff.SetLineWidth(2)
            eff.SetMarkerStyle(20)
            eff.SetMarkerSize(1.4)
            eff.SetMarkerColor(color)
            eff.Draw("PE same")
            leg.AddEntry(eff, entry, 'PL')
        leg.Draw()

        tlat = ROOT.TLatex()
        tlat.SetTextFont(43)
        tlat.SetNDC(1)
        tlat.SetTextAlign(33) # right aligned
        if self.tag:
            if self.tagpos[0] < 0.50:
                # left aligned if on the left side
                tlat.SetTextAlign(13)
            tlat.SetTextSize(26)
            tlat.DrawLatex(self.tagpos[0], self.tagpos[1], self.tag)
        if self.subtag:
            tlat.SetTextAlign(33) # right aligned
            if self.subtagpos[0] < 0.50:
                # left aligned if on the left side
                tlat.SetTextAlign(13)
            tlat.SetTextSize(22)
            tlat.DrawLatex(self.subtagpos[0], self.subtagpos[1], self.subtag)

        for ext in self.plotformats:
            canv.SaveAs(osp.join(outdir, "%s%s"%(outname,ext)))

    def show_with_ratio(self, outname, outdir):
        ROOT.gROOT.SetBatch(1)
        ROOT.gStyle.SetOptTitle(0)
        ROOT.gStyle.SetOptStat(0)

        canv = ROOT.TCanvas("canv_%s"%(self.name), "efficiencies", 600, 800)

        p2 = ROOT.TPad("pad2","pad2",0,0,1,0.31);
        ROOT.SetOwnership(p2, False)
        p2.SetTopMargin(0);
        p2.SetBottomMargin(0.30);
        p2.SetLeftMargin(0.1)
        p2.SetRightMargin(0.03)
        p2.SetFillStyle(0);
        p2.Draw();

        p1 = ROOT.TPad("pad1","pad1",0,0.31,1,1);
        ROOT.SetOwnership(p1, False)
        p1.SetBottomMargin(0);
        p1.SetLeftMargin(p2.GetLeftMargin())
        p1.SetRightMargin(p2.GetRightMargin())
        p1.Draw();

        ## Main pad
        p1.cd();

        mainframe = self.effs[0].GetTotalHistogram().Clone('mainframe')
        mainframe.Reset('ICE')
        mainframe.GetXaxis().SetTitleFont(43)
        mainframe.GetXaxis().SetLabelFont(43)
        mainframe.GetYaxis().SetTitleFont(43)
        mainframe.GetYaxis().SetLabelFont(43)

        if not self.ytitle:
            mainframe.GetYaxis().SetTitle('Efficiency')
        else:
            mainframe.GetYaxis().SetTitle(self.ytitle)
        mainframe.GetYaxis().SetLabelSize(22)
        mainframe.GetYaxis().SetTitleSize(26)
        mainframe.GetYaxis().SetTitleOffset(1.5)

        mainframe.GetXaxis().SetTitle('')
        mainframe.GetXaxis().SetLabelSize(0)
        mainframe.GetXaxis().SetTitleSize(0)
        mainframe.GetYaxis().SetNoExponent()
        mainframe.Draw()

        # leg = ROOT.TLegend(.12,.15,.60,.30+0.037*max(len(self.effs)-3,0))
        leg = ROOT.TLegend(.35,.03,.85,.13+0.053*max(len(self.effs)-3,0))

        leg.SetBorderSize(0)
        leg.SetFillColor(0)
        leg.SetFillStyle(0)
        leg.SetShadowColor(0)
        leg.SetTextFont(43)
        leg.SetTextSize(22)

        for eff,entry,color in zip(self.effs,self.legentries,self.colors):
            eff.SetLineColor(color)
            eff.SetLineWidth(2)
            eff.SetMarkerStyle(20)
            eff.SetMarkerSize(1.4)
            eff.SetMarkerColor(color)
            eff.Draw("PE same")
            leg.AddEntry(eff, entry, 'PL')
        leg.Draw()

        tlat = ROOT.TLatex()
        tlat.SetTextFont(43)
        tlat.SetNDC(1)
        tlat.SetTextAlign(33) # right aligned
        if self.tag:
            if self.tagpos[0] < 0.50:
                # left aligned if on the left side
                tlat.SetTextAlign(13)
            tlat.SetTextSize(26)
            tlat.DrawLatex(self.tagpos[0], self.tagpos[1], self.tag)
        if self.subtag:
            tlat.SetTextAlign(33) # right aligned
            if self.subtagpos[0] < 0.50:
                # left aligned if on the left side
                tlat.SetTextAlign(13)
            tlat.SetTextSize(22)
            tlat.DrawLatex(self.subtagpos[0], self.subtagpos[1], self.subtag)


        ## Ratio pad
        p2.cd()

        if not self.reference: # no reference given, take first
            self.reference = len(self.effsforratio)*[self.effs[0]]
        if len(self.reference) == 1: # one reference (compare all to this):
            self.reference = len(self.effsforratio)*[self.reference[0]]
        assert(len(self.reference) == len(self.effsforratio))

        # Ratio axes
        ratioframe = mainframe.Clone('ratioframe')
        ratioframe.Reset('ICE')
        ratioframe.GetYaxis().SetRangeUser(0.80,1.20)
        ratioframe.GetYaxis().SetTitle('Data/MC')
        ratioframe.GetXaxis().SetLabelSize(22)
        ratioframe.GetXaxis().SetTitleSize(32) # 26
        ratioframe.GetYaxis().SetNdivisions(5)
        ratioframe.GetYaxis().SetNoExponent()
        ratioframe.GetYaxis().SetTitleOffset(
                                 mainframe.GetYaxis().GetTitleOffset())
        ratioframe.GetXaxis().SetTitleOffset(3.0)

        # Calculate ratios
        self.ratios = []
        for eff,ref in zip(self.effsforratio, self.reference):
            if self.invertratio:
                self.ratios.append(getEfficiencyRatio(ref, eff))
            else:
                self.ratios.append(getEfficiencyRatio(eff, ref, attributes_from_first=True))

        if not self.xtitle:
            ratioframe.GetXaxis().SetTitle(
                self.ratios[0].GetXaxis().GetTitle())
        else:
            ratioframe.GetXaxis().SetTitle(self.xtitle)

        if self.ratiorange:
            ratmin, ratmax = self.ratiorange
            for ratio in self.ratios:
                ratio.SetMinimum(ratmin)
                ratio.SetMaximum(ratmax)
            ratioframe.SetMinimum(ratmin)
            ratioframe.SetMaximum(ratmax)
            ratioframe.GetYaxis().SetRangeUser(ratmin, ratmax)

        ratioframe.Draw()

        line = ROOT.TLine(self.ratios[0].GetXaxis().GetXmin(), 1.0,
                          self.ratios[0].GetXaxis().GetXmax(), 1.0)
        line.SetLineColor(ROOT.kGray)
        line.Draw()

        line2 = line.Clone("grid")
        line2.SetLineStyle(3)
        line2.DrawLine(self.ratios[0].GetXaxis().GetXmin(), 1.1,
                      self.ratios[0].GetXaxis().GetXmax(), 1.1)

        line2.DrawLine(self.ratios[0].GetXaxis().GetXmin(), 0.9,
                      self.ratios[0].GetXaxis().GetXmax(), 0.9)

        for ratio in reversed(self.ratios):
            ratio.Draw("E1 same")

        for ext in self.plotformats:
            canv.SaveAs(osp.join(outdir, "%s%s"%(outname,ext)))

def projectFromTree(hist, varname, sel, tree, option=''):
    try:
        tree.Project(hist.GetName(),varname, sel, option)
        return True
    except Exception, e:
        raise e

def getHistoFromTree(tree, sel, bins, var="mass",
                     hname="histo",
                     titlex='', weight=''):
    histo = ROOT.TH1D(hname, "histo" , len(bins)-1, array('d', bins))
    if sel=="": sel = "1"
    sel = "(%s)" % sel
    if len(weight):
        sel = "%s*(%s)" % (sel, weight)
    projectFromTree(histo, var, sel, tree)
    histo.SetLineWidth(2)
    histo.GetXaxis().SetTitle(titlex)
    # histo.Sumw2()
    histo.SetDirectory(0)
    return histo

def shushRooFit():
    "Make RooFit shut up"
    msgSI = ROOT.RooMsgService.instance()
    msgSI.setSilentMode(True)
    for s in [0,1]:
        for t in ['Eval',
                  'NumIntegration',
                  'DataHandling',
                  'ObjectHandling',
                  'Minimization',
                  'Fitting',
                  'Plotting',
                  'InputArguments',
                  'Caching']:
            msgSI.getStream(s).removeTopic(getattr(ROOT.RooFit,t))

def putPHPIndex(odir):
    LOC = '/afs/cern.ch/user/s/stiegerb/www/ttH/index.php'
    try:
        os.symlink(LOC, os.path.join(odir,'index.php'))
    except OSError, e:
        if e.errno == 17:  # 'File exists'
            pass

def shapeCBBreitWigner(ws):
    ws.factory("RooBreitWigner::bw(mass, mZ0[91.188], gammaZ0[2.4952])")
    ws.factory("RooCBShape::cb_pdf(mass, cbb[0.07, -3.00, 3.0]," # bias
                                        "cbw[1.00,  0.00, 5.0]," # width
                                        "cba[1.20,  0.03, 4.0]," # alpha
                                        "cbn[5])")               # power

    ws.factory("RooFFTConvPdf::sig(mass, bw, cb_pdf)")

def shapeExpBackgr(ws):
    ws.factory("RooExponential::bg(mass,tau[-0.05,-40.,-0.01])")

def shapeRooCMSShape(ws):
    ws.factory("RooCMSShape::bg(mass, alpha[40.,20.,160.], "
                                     "beta[ 0.050, 0., 2.0], "
                                     "gamma[0.020, 0., 0.1], "
                                     "peak[91.2])")

def getNSignalEvents(histo, dofit=True, odir='tnpfits/'):
    if not dofit:
        # Return cut&count values
        binlo = histo.GetXaxis().FindBin(71.)
        binhi = histo.GetXaxis().FindBin(101.)
        err = ROOT.Double(0.0)
        nev = histo.IntegralAndError(binlo,binhi,err)
        return nev,err

    os.system('mkdir -p %s'%odir)

    ROOT.gROOT.SetBatch(1)
    shushRooFit()

    ws = ROOT.RooWorkspace()
    mass = ws.factory('mass[61,121]')
    data = ROOT.RooDataHist(histo.GetName(),
                            histo.GetTitle(),
                            ROOT.RooArgList(mass),
                            histo)
    getattr(ws,'import')(data)

    # Define the pdfs:
    shapeCBBreitWigner(ws)
    shapeRooCMSShape(ws)
    # shapeExpBackgr(ws)

    # Define the fit model:
    nev = histo.Integral()
    nsig  = ws.factory('nsig[%.1f,%.1f,%.0f]'%(0.9*nev,0.2*nev,1.5*nev))
    nbkg  = ws.factory('nbkg[%.1f,0,%.0f]'%(0.1*nev,1.5*nev))
    shape = ws.factory('SUM::model(nsig*sig, nbkg*bg)')
    getattr(ws,'import')(shape)

    # Do the fit
    fitResult = shape.fitTo(data, ROOT.RooFit.Save())

    # Plot the result
    canv = ROOT.TCanvas('canv_%s'%histo.GetName(),'canvas', 800, 800)
    frame = mass.frame()
    data.plotOn(frame)
    shape.plotOn(frame,
               ROOT.RooFit.Name('total'),
               ROOT.RooFit.ProjWData(data),
               ROOT.RooFit.LineColor(ROOT.kBlue),
               ROOT.RooFit.LineWidth(2),
               ROOT.RooFit.MoveToBack())
    shape.plotOn(frame,
               ROOT.RooFit.Name('bkg'),
               ROOT.RooFit.ProjWData(data),
               ROOT.RooFit.Components('*bg*'),
               ROOT.RooFit.FillColor(ROOT.kGray),
               ROOT.RooFit.LineColor(ROOT.kGray),
               ROOT.RooFit.LineWidth(1),
               ROOT.RooFit.DrawOption('f'),
               ROOT.RooFit.FillStyle(1001),
               ROOT.RooFit.MoveToBack())
    frame.Draw()

    tlat = ROOT.TLatex()
    tlat.SetTextFont(83)
    tlat.SetNDC(1)
    tlat.SetTextSize(22)
    fitparms = ['cbb', 'cbw', 'cba', 'beta', 'gamma', 'alpha']
    for v in fitparms:
        val = ws.var(v).getVal()
        # if abs(val - ws.var(v).getMax()) < 1e-5:
        #     print ('########## %s is hitting maximum: %f (%f)' %
        #                   (v, val, ws.var(v).getMax()))
        # if abs(val - ws.var(v).getMin()) < 1e-5:
        #     print ('########## %s is hitting minimum: %f (%f)' %
        #                   (v, val, ws.var(v).getMin()))

        tlat.DrawLatex(0.14, 0.80-0.03*fitparms.index(v), '%-5s: %6.3f' % (v, val))
    tlat.DrawLatex(0.14, 0.86, 'Nsig : %8.1f' % (nsig.getVal()))
    tlat.DrawLatex(0.14, 0.83, 'Nbkg : %8.1f' % (nbkg.getVal()))


    canv.SaveAs(osp.join(odir,"massfit_%s.pdf"%(histo.GetName())))
    canv.SaveAs(osp.join(odir,"massfit_%s.png"%(histo.GetName())))
    if 'www' in odir: putPHPIndex(odir)

    return nsig.getVal(), nsig.getError()

def getPassTotalHistos((key, output,
                        tag, floc, pairsel,
                        probnum, probdenom, var, bins,
                        options)):
    totalsel  = '(%s)&&(%s)' % (pairsel, probdenom)
    passedsel = '(%s)&&(%s)' % (pairsel, probnum)

    bincut = "({var}>={binlo}&&{var}<{binhi})"
    binsels = []
    for nbin in xrange(len(bins)-1):
        binlo, binhi = bins[nbin], bins[nbin+1]
        binsels.append(bincut.format(var=var,binlo=binlo,binhi=binhi))

    treefile = ROOT.TFile(floc,"READ")
    tree = treefile.Get('fitter_tree')

    htemp = getHistoFromTree(tree,"0",bins,var,hname="htemp_%s"%(var))
    htemp.Reset("ICE")

    hpassed = htemp.Clone("%s_passed"%var)
    hpassed.SetDirectory(0)
    htotal = htemp.Clone("%s_total"%var)
    htotal.SetDirectory(0)

    plotDir = osp.join(options.outDir, 'tnpfits', *tuple(tag.split('_')))
    proc = tag.split('_',1)[0]
    dofit = [proc in ['data','DY']] and not options.cutNCount

    for n,binsel in enumerate(binsels):
        print "  ... processing %-36s" % binsel,
        totalbinsel = "%s&&%s" % (totalsel, binsel)
        htotalbin = getHistoFromTree(tree,totalbinsel,MASSBINS,"mass",
                                   hname="%s_total_%d"%(var,n),
                                   weight=WEIGHT,
                                   titlex='Dilepton Mass [GeV]')
        passedbinsel = "%s&&%s" % (passedsel, binsel)
        hpassedbin = getHistoFromTree(tree,passedbinsel,MASSBINS,"mass",
                                   hname="%s_passed_%d"%(var,n),
                                   weight=WEIGHT,
                                   titlex='Dilepton Mass [GeV]')

        npass,passerr = getNSignalEvents(hpassedbin,
                                         dofit=dofit,
                                         odir=plotDir)
        ntot,toterr   = getNSignalEvents(htotalbin,
                                         dofit=dofit,
                                         odir=plotDir)
        print 'pass: %8.1f +- %5.1f' % (npass,passerr),
        print 'tot:  %8.1f +- %5.1f' % (ntot,toterr),

        ## Some cheating (i.e. taking cut&count in some cases):
        ##  npass > ntot (can only happen if the fit goes wrong)
        ##  for the threshold bin containing pT of 50 GeV
        if npass > ntot or (50.>=bins[n] and 50.<bins[n+1]):
            npass,passerr = getNSignalEvents(hpassedbin,dofit=False)
            ntot,toterr   = getNSignalEvents(htotalbin, dofit=False)

        hpassed.SetBinContent(n+1, npass)
        hpassed.SetBinError(n+1, passerr)
        htotal.SetBinContent(n+1, ntot)
        htotal.SetBinError(n+1, toterr)
        print "DONE"

    output[key] = (hpassed, htotal)

def getPassTotalHistosSimple((key, output,
                              tag, floc, pairsel,
                              probnum, probdenom, var, bins,
                              options)):
    totalsel  = '(%s)&&(%s)' % (pairsel, probdenom)
    passedsel = '(%s)&&(%s)' % (pairsel, probnum)

    treefile = ROOT.TFile(floc,"READ")
    tree = treefile.Get('fitter_tree')

    htotal = getHistoFromTree(tree,totalsel,bins,var,
                               hname="%s_total_simple_%s"%(var,tag),
                               weight=WEIGHT)
    hpassed = getHistoFromTree(tree,passedsel,bins,var,
                               hname="%s_passed_simple_%s"%(var,tag),
                               weight=WEIGHT)

    output[key] = (hpassed, htotal)

def makePassedFailed(proc,fnames,indir,
                     options, stump='.root'):

    try:
        with open('.xsecweights.pck', 'r') as cachefile:
            xsecweights = pickle.load(cachefile)
            print '>>> Read xsecweights from cache (.xsecweights.pck)'
    except IOError:
        print ("Please run makeXSecWeights.py first to apply "
               "cross section weights.")
        xsecweights = {}

    result = {}
    for pname in fnames:
        floc = osp.join(indir, "%s%s"%(pname,stump))
        if not osp.isfile(floc):
            print "Missing file: %s" % floc
            raw_input(" ... press key to continuing without")
            continue

        print '... processing', pname
        if proc != 'data':
            weight = LUMI*xsecweights.get(pname, 1.0/LUMI)
            print '    weighting histos by', weight
        else: weight = 1.0

        tasks = []    # do the fit for these
        tasks_cc = [] # do cut & count for these

        if options.jobs>1:
            from multiprocessing import Manager, Pool
            manager = Manager()
            result_dict = manager.dict()
        else:
            result_dict = {}

        for lep,lepsel,_ in LEPSEL:
            for sname,sel in SELECTIONS.iteritems():
                if sname == 'ttH' and proc != 'ttH': continue
                if sname.startswith('runs') and proc != 'data': continue
                finalsel = '(%s)&&(%s)' % (lepsel, sel)
                for nname,num,_ in NUMERATORS:
                    for var,bins,_ in BINNINGS:

                        # Some special cases:
                        # Skip eta binnings for non pt vars
                        if (not lep in ['eb','ee','mb','me'] and
                            var != 'pt'): continue

                        # Cut at pt>30 for njet and nbjet binnings
                        if 'Jet' in var: fsel = finalsel+'&&pt>30'
                        else: fsel = finalsel

                        tag = '_'.join([proc, lep, nname])
                        key = (lep,sname,nname,var)

                        task = (key, result_dict, tag, floc, fsel, num,
                                DENOMINATOR, var, bins, options)

                        if proc not in ['DY', 'data']:
                            tasks_cc.append(task)
                        else:
                            tasks.append(task)


        print 'Have %d tasks to process' % (len(tasks)+len(tasks_cc))

        if options.jobs > 1:
            Pool(options.jobs).map(getPassTotalHistos, tasks)
            Pool(options.jobs).map(getPassTotalHistosSimple, tasks_cc)
        else:
            map(getPassTotalHistos, tasks)
            map(getPassTotalHistosSimple, tasks_cc)

        for key in [t[0] for t in tasks+tasks_cc]:
            hpass, htot = result_dict[key]

            hpass.Scale(weight)
            htot.Scale(weight)

            if key in result:
                result[key][0].Add(hpass)
                result[key][1].Add(htot)
            else:
                result[key] = (hpass,htot)

        print '      %s done' % pname

    return result

def makeEfficiencies(passedtotal):
    result = {}

    # Calculate raw efficiencies
    for proc, histos in passedtotal.iteritems():
        proc_effs = {}
        for key,(p,f) in histos.iteritems():
            eff = TEfficiency(p, f)
            proc_effs[key] = eff
        result[proc] = proc_effs

    # # Calculate background corrected efficiencies
    # # I.e. subtract ttbar MC from data
    # for key in passedtotal.values()[0].keys():
    #     print '... processing', key
    #     passdata,totdata = passedtotal['data'][key]
    #     passtt,  tottt   = passedtotal['ttbar'][key]

    #     pcorr = passdata.Clone("pass_corrected")
    #     fcorr = totdata.Clone("tot_corrected")
    #     pcorr.Add(passtt, -1.0)
    #     fcorr.Add(tottt, -1.0)
    #     result.setdefault('data_corr', {})[key] = TEfficiency(pcorr, fcorr)

    return result

def makePlots(efficiencies, options):
    for lep,_,lname in LEPSEL:
        for nname,_,ntitle in NUMERATORS:
            for var,bins,xtitle in BINNINGS:

                if not lep in ['ee','eb','mb','me']: continue

                # Compare data/MC for each binning
                plot = EfficiencyPlot('%s_%s_%s'%(lep,nname,var))
                plot.xtitle = xtitle
                plot.tag = '%s'%(lname)
                plot.subtag = '%s'%(ntitle)
                plot.colors = [ROOT.kBlack,
                               ROOT.kAzure+1,
                               ROOT.kGreen+3,
                               ROOT.kGreen-2,
                               ROOT.kGreen-6,
                               ROOT.kGreen-9
                               ]
                # plot.colors = [ROOT.kBlack,  ROOT.kAzure+1,
                #                ROOT.kGray+1, ROOT.kSpring-8,
                #                ROOT.kPink+9]

                plot.tagpos = (0.92,0.35+0.1)
                plot.subtagpos = (0.92,0.29+0.1)
                if lep == 'ee':
                    plot.tagpos = (0.92,0.85)
                    plot.subtagpos = (0.92,0.79)


                if 'Jet' in var:
                    plot.subtag = '%s, p_{T} > 30 GeV' % ntitle

                plot.reference = [efficiencies['DY'][(lep,'inclusive',nname,var)]]

                fitlabel = 'Z mass fit' if not options.cutNCount else 'cut & count'

                plot.add(efficiencies['data'][(lep,'inclusive',nname,var)],
                         'Data (%.2f fb^{-1}), %s' % (LUMI, fitlabel),
                         includeInRatio=True)
                plot.add(efficiencies['DY'][(lep,'inclusive',nname,var)],
                         'DY MC, %s' % fitlabel,
                         includeInRatio=False)

                for selname in SELECTIONS.keys():
                    if selname == 'inclusive': continue
                    plot.add(efficiencies['data'][(lep, selname, nname, var)],
                         'Data %s'%selname, includeInRatio=True)

                # plot.add(efficiencies['data'][(lep,'ttbar',nname,var)],
                #          'Data, t#bar{t} dilepton, cut & count',
                #          includeInRatio=False)
                # plot.add(efficiencies['ttbar'][(lep,'ttbar',nname,var)],
                #          't#bar{t} MC, t#bar{t} dilepton, cut & count',
                #          includeInRatio=True)
                # plot.add(efficiencies['ttH'][(lep,'ttH',nname,var)],
                #          't#bar{t}H MC, inclusive',
                #          includeInRatio=False)

                # plot.reference = [plot.effs[0], plot.effs[1]]
                # plot.reference = [plot.effs[0], plot.effs[2]]

                plot.show_with_ratio('tnp_eff_%s'%(plot.name),
                                      options.outDir)

def make2DMap(efficiencies, options):
    outdir = osp.join(options.outDir, 'map')
    os.system('mkdir -p %s'%outdir)
    if 'www' in outdir: putPHPIndex(outdir)

    sfhistos = {}

    for nname,_,ntitle in NUMERATORS:
        for lepton in ['e', 'm']:
            # Make data/MC plots
            for lep,_,lname in LEPSEL2D:
                if not lep.startswith(lepton): continue

                plot = EfficiencyPlot('%s_%s_%s'%(lep,nname,'pt'))
                plot.xtitle = 'p_{T} [GeV]'
                plot.tag = '%s'%(lname)
                plot.subtag = '%s'%(ntitle)

                plot.add(efficiencies['data'][(lep,'inclusive',nname,'pt')],
                         'Data, Z mass fit', includeInRatio=False)
                plot.add(efficiencies['DY'][(lep,'inclusive',nname,'pt')],
                         'DY MC, Z mass fit', includeInRatio=True)

                plot.reference = [plot.effs[0]]

                plot.show_with_ratio('tnp_eff_%s'%(plot.name),outdir)

            ## Make the 2D histograms
            etabins = {'e': ETABINS2D_EL, 'm': ETABINS2D_MU}[lepton]
            sfhisto_2d = ROOT.TH2F("sf_%s"%lepton,
                                   "mva tight data/mc scale factors",
                                   len(PTBINS)-1, array('d', PTBINS),
                                   len(etabins)-1, array('d', etabins))
            sfhisto_2d.SetName('%s_%s'%(lepton, nname))
            sfhisto_2d.SetDirectory(0)

            for ny in range(len(etabins)-1):
                lep = '%s%d' % (lepton, ny)

                # each of these is binned in pt:
                sfhisto = getEfficiencyRatio(
                    efficiencies['data'][(lep,'inclusive',nname,'pt')],
                    efficiencies['DY']  [(lep,'inclusive',nname,'pt')])

                for nx in range(len(PTBINS)):
                    sfhisto_2d.SetBinContent(nx+1, ny+1,
                                             sfhisto.GetBinContent(nx+1))
                    sfhisto_2d.SetBinError(nx+1, ny+1,
                                             sfhisto.GetBinError(nx+1))

            sfhistos[(lepton,nname)] = sfhisto_2d

    for (lepton,nname),histo in sfhistos.iteritems():
        fname = 'lepMVAEffSF_%s_%s.root' % (lepton, nname)
        floc = osp.join(options.outDir,fname)
        ofile = ROOT.TFile(floc, 'RECREATE')
        ofile.cd()
        histo.Write('sf')
        ofile.Write()
        ofile.Close()
        print " wrote %s" % floc

def main(args, options):
    try:
        if not osp.exists(args[0]):
            print "Input directory does not exists: %s" % args[0]
            sys.exit(-1)
    except IndexError:
        parser.print_usage()
        sys.exit(-1)

    # Gather all the passed/total histograms
    cachefilename = "tnppassedtotal.pck"
    if not osp.isfile(cachefilename):
        passedtotal = {}
        for proc,fnames in INPUTS.iteritems():
            passedtotal[proc] = makePassedFailed(proc,fnames,args[0],options,stump='.root')

        print "#"*30
        print "ALL DONE"
        print "#"*30

        with open(cachefilename, 'w') as cachefile:
            pickle.dump(passedtotal, cachefile, pickle.HIGHEST_PROTOCOL)
            print ('>>> Wrote tnp passed total histograms to cache (%s)' %
                                                        cachefilename)
    else:
        with open(cachefilename, 'r') as cachefile:
            passedtotal = pickle.load(cachefile)
            print ('>>> Read tnp passed total histograms from cache (%s)' %
                                                        cachefilename)

    os.system('mkdir -p %s'%options.outDir)
    if 'www' in options.outDir: putPHPIndex(options.outDir)

    # Calculate efficiencies
    efficiencies = makeEfficiencies(passedtotal)

    # Make plots
    makePlots(efficiencies, options)
    make2DMap(efficiencies, options)


if __name__ == '__main__':
    from optparse import OptionParser
    usage = "%prog [options] tnptrees/"
    parser = OptionParser(usage=usage)
    parser.add_option("-o", "--outDir", default="tnp_effs",
                      action="store", type="string", dest="outDir",
                      help=("Output directory for eff plots "
                            "[default: %default/]"))
    parser.add_option('-c', '--cutNCount', dest='cutNCount',
                      action="store_true",
                      help='Do cut & count instead of fitting mass shape')
    parser.add_option('-j', '--jobs', dest='jobs', action="store",
                      type='int', default=1,
                      help=('Number of jobs to run in parallel '
                        '[default: single]'))
    (options, args) = parser.parse_args()

    main(args, options)

