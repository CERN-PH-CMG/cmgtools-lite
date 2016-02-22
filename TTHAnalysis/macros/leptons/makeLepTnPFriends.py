#!/usr/bin/env python
import sys, os, pickle
import ROOT

from array import array
from ROOT import TEfficiency
import os.path as osp

LUMI = 2.26
WEIGHT = "puWeight"
PAIRSEL = ("((pdgId*tag_pdgId==-11*11||pdgId*tag_pdgId==-13*13)"
           "&&abs(mass-91.)<20.&&abs(mcMatchId)>0)")
SELECTIONS = [
    ('inclusive',      PAIRSEL),
    # ('singleTriggers', PAIRSEL+"&&passSingle"),
    # ('doubleTriggers', PAIRSEL+"&&passDouble"),
    # ('ttbar', "( (pdgId*tag_pdgId==-11*13)||"
    #           "  ( (pdgId*tag_pdgId==-11*11||pdgId*tag_pdgId==-13*13)"
    #           "&&abs(mass-91.)>15.&&met_pt>30.) )&&passDouble"),
]

LEPSEL = [
    # ('e',  'abs(pdgId)==11', 'Electrons'),
    ('eb', 'abs(pdgId)==11&&abseta<1.479',
           'Electrons Barrel (#eta < 1.479)'),
    ('ee', 'abs(pdgId)==11&&abseta>=1.479',
           'Electrons Endcap (#eta #geq 1.479)'),
    # ('m',  'abs(pdgId)==13', 'Muons'),
    ('mb', 'abs(pdgId)==13&&abseta<1.2',  'Muons Barrel (#eta < 1.2)'),
    ('me', 'abs(pdgId)==13&&abseta>=1.2', 'Muons Endcap (#eta #geq 1.2)'),
]

PTBINS    = [10.,15.,20.,25.,30.,37.5,45.,60.,80.,100.]
ETABINS   = [0.,0.25,0.50,0.75,1.00,1.25,1.50,2.00,2.50]
NVERTBINS = [0,4,7,8,9,10,11,12,13,14,15,16,17,19,22,25,30]
NJETBINS  = [0,1,2,3,4,5,6]
NBJETBINS = [0,1,2,3]
BINNINGS = [
    ('pt',            PTBINS,    'p_{T} [GeV]'),
    ('abseta',        ETABINS,   '|#eta|'),
    ('nVert',         NVERTBINS, 'N_{vertices}'),
    ('nJet25',        NJETBINS,  'N_{jets}'),
    ('nBJetMedium25', NBJETBINS, 'N_{bjets, CSVM}'),
]

DENOMINATOR = "passLoose"
NUMERATORS  = [
    ('2lss',"passTight&&passTCharge", 'same-sign 2 lepton definition'),
    ('3l',  "passTight", '3 lepton definition'),
]

INPUTS = {
    'data':[
        "DoubleEG_Run2015C_25ns_16Dec2015",
        "DoubleEG_Run2015D_16Dec2015",
        "DoubleMuon_Run2015C_25ns_16Dec2015",
        "DoubleMuon_Run2015D_16Dec2015",
        "MuonEG_Run2015C_25ns_16Dec2015",
        "MuonEG_Run2015D_16Dec2015",
        "SingleElectron_Run2015C_25ns_16Dec2015",
        "SingleElectron_Run2015D_16Dec2015",
        "SingleMuon_Run2015C_25ns_16Dec2015",
        "SingleMuon_Run2015D_16Dec2015",
        ],
    'DY':["DYJetsToLL_M50"],
    'ttbar':[
        "TTJets_DiLepton",
        "TTJets_SingleLeptonFromTbar_ext",
        "TTJets_SingleLeptonFromTbar",
        "TTJets_SingleLeptonFromT_ext",
        "TTJets_SingleLeptonFromT",
        ],
    'ttH':["TTHnobb"],
}

class EfficiencyPlot(object):
    """Simple class for making plots comparing TEfficiency objects"""
    def __init__(self, name):
        self.name = name
        self.effs = []
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
        self.ratiorange = (0.75, 1.15)

    def add(self,eff,tag):
        self.effs.append(eff)
        self.legentries.append(tag)

    def show(self, outname, outdir):
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

    def getRatio(self, eff1, eff2):
        ratio = eff1.GetPassedHistogram().Clone("ratio")
        ratio.Sumw2()
        ratio.Divide(eff1.GetTotalHistogram())
        ratio.Multiply(eff2.GetTotalHistogram())
        ratio.Divide(eff2.GetPassedHistogram())
        for att in ['LineWidth','LineColor','MarkerStyle',
                    'MarkerSize','MarkerColor']:
            getattr(ratio,'Set%s'%att)(getattr(eff2,'Get%s'%att)())
        return ratio

    def show_with_ratio(self, outname, outdir):
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
        leg = ROOT.TLegend(.63,.12,.92,.22+0.037*max(len(self.effs)-3,0))

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


        ## Ratio pad
        p2.cd()

        if not self.reference: # no reference given, take first
            self.reference = (len(self.effs)-1)*[self.effs[0]]

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
        for eff in self.effs[1:]:
            self.ratios.append(self.getRatio(self.reference, eff))

        if not self.xtitle:
            ratioframe.GetXaxis().SetTitle(self.ratios[0].GetXaxis().GetTitle())
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

def getPassFailHistos((tree, pairsel, probnum, probdenom, var, bins)):
    failedsel = '(%s)&&(%s)' % (pairsel, probdenom)
    passedsel = '(%s)&&(%s)' % (pairsel, probnum)
    hfailed = getHistoFromTree(tree,failedsel,bins,var,
                               hname="%s_failed"%var,
                               weight=WEIGHT)
    hpassed = getHistoFromTree(tree,passedsel,bins,var,
                               hname="%s_passed"%var,
                               weight=WEIGHT)

    return hpassed, hfailed

def makePassedFailed(proc,fnames,indir):
    stump = '_treeProducerSusyMultilepton_tree.root'

    try:
        with open('.xsecweights.pck', 'r') as cachefile:
            xsecweights = pickle.load(cachefile)
            print '>>> Read xsecweights from cache (.xsecweights.pck)'
    except IOError:
        print "Please run makeXSecWeights.py first"
        return None

    result = {}
    for pname in fnames:
        floc = osp.join(indir, "%s%s"%(pname,stump))
        if not osp.isfile(floc):
            print "Missing file: %s" % floc
            print " ... continuing without"
            continue

        print '... processing', pname
        weight = LUMI*xsecweights[pname]
        print '    weighting histos by', weight

        treefile = ROOT.TFile(floc,"READ")
        tree = treefile.Get('fitter_tree')

        for lep,lepsel,_ in LEPSEL:
            for sname,sel in SELECTIONS:
                finalsel = '(%s)&&(%s)' % (lepsel, sel)
                for var,bins,_ in BINNINGS:
                    for nname,num,_ in NUMERATORS:

                        hpass, hfail = getPassFailHistos((tree, finalsel,
                                              num, DENOMINATOR, var,bins))

                        hpass.Scale(weight)
                        hfail.Scale(weight)

                        key = (lep,sname,nname,var)

                        if key in result:
                            result[key][0].Add(hpass)
                            result[key][1].Add(hfail)
                        else:
                            result[key] = (hpass,hfail)

    return result

def makeEfficiencies(passedfailed):
    result = {}

    # Calculate raw efficiencies
    for proc, histos in passedfailed.iteritems():
        proc_effs = {}
        for key,(p,f) in histos.iteritems():
            eff = TEfficiency(p, f)
            proc_effs[key] = eff
        result[proc] = proc_effs

    # Calculate background corrected efficiencies
    # I.e. subtract ttbar MC from data
    for key in passedfailed.values()[0].keys():
        print '... processing', key
        passdata,faildata = passedfailed['data'][key]
        passtt,  failtt   = passedfailed['ttbar'][key]

        pcorr = passdata.Clone("pass_corrected")
        fcorr = faildata.Clone("fail_corrected")
        pcorr.Add(passtt, -1.0)
        fcorr.Add(failtt, -1.0)
        result.setdefault('data_corr', {})[key] = TEfficiency(pcorr, fcorr)

    return result

def makePlots(efficiencies, options):
    ROOT.gROOT.SetBatch(1)
    ROOT.gStyle.SetOptTitle(0)
    ROOT.gStyle.SetOptStat(0)

    ptitle = {
        'data'      : 'Data',
        'data_corr' : 'Data (t#bar{t} subtracted',
        'DY'        : 'DY MC'
    }

    seltitle = {
        'inclusive'      : '',
        'singleTriggers' : ', Single lepton triggers',
        'doubleTriggers' : ', Double lepton triggers',
        'ttbar'          : 'ttbar',
    }

    for lep,_,lname in LEPSEL:
        for nname,_,ntitle in NUMERATORS:
            for var,bins,xtitle in BINNINGS:

                if lep in ['ee','eb','mb','me'] and 'abseta' in var: continue

                # Compare data/MC in each binning/selection
                plot = EfficiencyPlot('%s_%s_%s'%(lep,nname,var))
                plot.xtitle = xtitle
                plot.tag = '%s'%(lname)
                plot.subtag = '%s'%(ntitle)

                legentries, effs_to_plot = [], []
                for pname in ['data','DY']:
                    plot.add(efficiencies[pname]
                                   [(lep,'inclusive',nname,var)],
                             ptitle.get(pname,pname))
                plot.reference = efficiencies['data'][(lep,'inclusive',nname,var)]

                plot.show_with_ratio('tnp_eff_%s'%(plot.name), options.outDir)

                # Compare single/double triggers:
                if lep in ['ee','eb','mb','me']: continue
                for pname,effs in efficiencies.iteritems():
                    plot = EfficiencyPlot('%s_%s_%s_%s'%(
                                            lep,nname,var,pname))
                    plot.xtitle = xtitle
                    plot.tag = '%s, %s'%(lname,
                                         ptitle.get(pname, pname))
                    plot.subtag = '%s'%(ntitle)

                    legentries, effs_to_plot = [], []
                    for sname,_ in SELECTIONS:
                        plot.add(effs[(lep,sname,nname,var)],
                                 seltitle.get(sname,sname))

                    plot.show('tnp_eff_%s'%(plot.name), options.outDir)

if __name__ == '__main__':
    from optparse import OptionParser
    usage = "%prog [options] tnpTreeDir"
    parser = OptionParser(usage=usage)
    parser.add_option("-o", "--outDir", default="tnp_effs",
                      action="store", type="string", dest="outDir",
                      help=("Output directory for eff plots "
                            "[default: %default/]"))
    (options, args) = parser.parse_args()

    # Gather all the passed/failed histograms
    cachefilename = "tnppassedfailed.pck"
    if not osp.isfile(cachefilename):
        passedfailed = {}
        for proc,fnames in INPUTS.iteritems():
            passedfailed[proc] = makePassedFailed(proc,fnames,args[0])

        cachefile = open(cachefilename, 'w')
        pickle.dump(passedfailed, cachefile, pickle.HIGHEST_PROTOCOL)
        print ('>>> Wrote tnp passed failed histograms to cache (%s)' %
                                                    cachefilename)
        cachefile.close()
    else:
        cachefile = open(cachefilename, 'r')
        passedfailed = pickle.load(cachefile)
        print ('>>> Read tnp passed failed histograms from cache (%s)' %
                                                    cachefilename)
        cachefile.close()

    os.system('mkdir -p %s'%options.outDir)

    efficiencies = makeEfficiencies(passedfailed)
    makePlots(efficiencies, options)



















