import sys
from array import array
from math import hypot, sqrt

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gROOT.ProcessLine(".x tdrstyle.cc")
ROOT.gStyle.SetOptStat(0)


class FetchFromTH2POG:
    def __init__(self,filename,hname):
        self._file = ROOT.TFile.Open(filename)
        self._h2 = self._file.Get(hname)
        if not self._h2 :
            self._file.ls()
            raise RuntimeError
    def __call__(self,pt,eta):
        ipt = min(max(1, self._h2.GetXaxis().FindBin(pt)),       self._h2.GetNbinsX());
        iae = min(max(1, self._h2.GetYaxis().FindBin(abs(eta))), self._h2.GetNbinsY());
        return (self._h2.GetBinContent(ipt,iae), self._h2.GetBinError(ipt,iae))

class FetchFromTGraphsPts:
    def __init__(self,aetaFilename,gname):
        self._aetaBins = []
        for aeta, filename in aetaFilename:
            tfile = ROOT.TFile.Open(filename)
            tgraph = tfile.Get(gname)
            self._aetaBins.append( (aeta, tfile, tgraph) )
    def __call__(self,pt,eta):
        aeta = abs(eta)
        for aebin,tfile,tgraph in self._aetaBins:
            if aebin[0] <= aeta and aeta <= aebin[1]:
                for i in xrange(tgraph.GetN()):
                    x0 = tgraph.GetX()[i]
                    xh = x0 + tgraph.GetErrorXhigh(i)
                    xl = x0 - tgraph.GetErrorXlow(i)
                    if xl <= pt and pt <= xh:
                        return (tgraph.GetY()[i], max(tgraph.GetErrorYlow(i), tgraph.GetErrorYhigh(i)))
        raise RuntimeError, "Did not find pt %s, eta %s" % (pt,eta)

class FetchFromTGraphsEta:
    def __init__(self,filename,gname):
        self._tfile = ROOT.TFile.Open(filename)
        self._tgraph = self._tfile.Get(gname)
    def __call__(self,pt,eta):
        tgraph = self._tgraph
        for i in xrange(tgraph.GetN()):
            x0 = tgraph.GetX()[i]
            xh = x0 + tgraph.GetErrorXhigh(i)
            xl = x0 - tgraph.GetErrorXlow(i)
            if xl <= eta and eta <= xh:
                  return (tgraph.GetY()[i], max(tgraph.GetErrorYlow(i), tgraph.GetErrorYhigh(i)))
        raise RuntimeError, "Did not find pt %s, eta %s" % (pt,eta)


what = sys.argv[1]
if what not in ("HZZ","ttH"): raise RuntimeError, "Unsupported analysis: %s" % what

sfTrk = lambda pt, eta : (0.99,0.0) if pt <= 10 else (1.0,0.0)
sfIdEtaLow = FetchFromTGraphsEta("../plotting/plots/76X_220116/zTnP//mupog_v2_jpsi/00_harvest/mu_Loose_pt7.root", "ratio_syst")
sfIdPtEta  = FetchFromTH2POG("MuonID_Z_RunCD_Reco76X_Feb15.root", "MC_NUM_LooseID_DEN_genTracks_PAR_pt_spliteta_bin1/pt_abseta_ratio")
if what == "HZZ":
    sfSIPEta   = FetchFromTGraphsEta("../plotting/plots/76X_220116/zTnP//mupog_v3/00_harvest/mu_SIP4_pt20.root", "ratio_syst")
    sfIsoPt    = FetchFromTGraphsPts(
        [ ((0.0, 1.2), "../plotting/plots/76X_220116/zTnP/v4_harvest/mu_iso_barrel.root"),
          ((1.2, 2.4), "../plotting/plots/76X_220116/zTnP/v4_harvest/mu_iso_endcap.root") ],
        "ratio_syst"
    )
elif what == "ttH":
    sfSIPEta   = FetchFromTGraphsEta("../plotting/plots/76X_220116/zTnP//mupog_v3/00_harvest/mu_SIP8_pt20.root", "ratio_syst")
    sfIsoPt    = FetchFromTGraphsPts(
        [ ((0.0, 1.2), "../plotting/plots/76X_220116/zTnP/mupog_v3/00_harvest/mu_MiniIso04_barrel.root"),
          ((1.2, 2.4), "../plotting/plots/76X_220116/zTnP/mupog_v3/00_harvest/mu_MiniIso04_endcap.root") ],
        "ratio_syst"
    )

stack = [ ( sfIdEtaLow, (0.0, 20.), (-2.4, 2.4) ),
          ( sfIdPtEta , (20., 80.), (-2.4, 2.4) ),
          ( sfSIPEta  , (0.0, 80.), (-2.4, 2.4) ),
          ( sfIsoPt   , (0.0, 80.), (-2.4, 2.4) ), 
          ( sfTrk     , (0.0, 80.), (-2.4, 2.4) ), ]


if what == "HZZ":
    etaBins = [ -2.4,-2.1,-1.6,-1.2,-0.9,-0.6,-0.3,-0.2,0.2,0.3,0.6,0.9,1.2,1.6,2.1,2.4 ]
    ptBins  = [ 5,6,7,8,10,12,15,20,25,30,35,40,50,60,80 ]
elif what == "ttH":
    etaBins = [ -2.4,-2.1,-1.6,-1.2,-0.9,-0.6,-0.3,-0.2,0.2,0.3,0.6,0.9,1.2,1.6,2.1,2.4 ]
    ptBins  = [ 10,12,15,20,25,30,35,40,50,60,80 ]

TH2  = ROOT.TH2F("FINAL","FINAL; #eta; p_{T} (GeV)",len(etaBins)-1,array('f',etaBins),len(ptBins)-1,array('f',ptBins))
TH2e = ROOT.TH2F("ERROR","ERROR; #eta; p_{T} (GeV)",len(etaBins)-1,array('f',etaBins),len(ptBins)-1,array('f',ptBins))

for ix in xrange(1,TH2.GetNbinsX()+1):
    for iy in xrange(1,TH2.GetNbinsY()+1):
        eta = TH2.GetXaxis().GetBinCenter(ix)
        pt  = TH2.GetYaxis().GetBinCenter(iy)
        sf, sfe  = 1.0, 0.0
        for prod,ptr,etar in stack:
            if ptr[0] <= pt and pt <= ptr[1]:
                if etar[0] <= eta and eta <= etar[1]:
                    f,e = prod(pt,eta)
                    sf *= f
                    sfe += e**2
        TH2.SetBinContent(ix,iy, sf) 
        TH2.SetBinError(ix,iy, sqrt(sfe)) 
        TH2e.SetBinContent(ix,iy, sqrt(sfe)) 
out = ROOT.TFile("final_%s.root" % what,"RECREATE")
TH2.GetZaxis().SetRangeUser(0.97,1.01)
TH2e.GetZaxis().SetRangeUser(0.0,0.03)
for H in TH2, TH2e:
    H.GetZaxis().SetDecimals()
    H.GetYaxis().SetTitleOffset(0.9)
    H.GetXaxis().SetLabelSize(0.05)
    H.GetYaxis().SetLabelSize(0.05)
    H.GetZaxis().SetLabelSize(0.05)
    H.SetContour(100)
    out.WriteTObject(H)

stops = array('d', [ 0.0000, 0.1250, 0.2500, 0.3750, 0.5000, 0.6250, 0.7500, 0.8750, 1.0000 ])
red = array('d', [  61./255.,  99./255., 136./255., 181./255., 213./255., 225./255., 198./255., 136./255., 24./255. ])
green = array('d', [ 149./255., 140./255.,  96./255.,  83./255., 132./255., 178./255., 190./255., 135./255., 22./255. ])
blue = array('d', [ 214./255., 203./255., 168./255., 135./255., 110./255., 100./255., 111./255., 113./255., 22./255. ])
ROOT.TColor.CreateGradientColorTable(9, stops, red, green, blue, 255);

c1 = ROOT.TCanvas("c1","c1",800,500)
c1.SetRightMargin(0.2)
TH2.Draw("COLZ")
c1.Print("final_%s.pdf" % what)
c1.Print("final_%s.png" % what)
TH2e.Draw("COLZ")
c1.Print("final_%s_errors.pdf" % what)
c1.Print("final_%s_errors.png" % what)

out.Close()
