import ROOT
from array import array

etaBins = [ -2.4,-2.1,-1.6,-1.2,-0.9,-0.6,-0.3,-0.2,0.2,0.3,0.6,0.9,1.2,1.6,2.1,2.4 ]
ptBins  = [ 10,12,15,20,25,30,35,40,50,60,80 ]

TH2 = ROOT.TH2F("FINAL","FINAL",len(etaBins)-1,array('f',etaBins),len(ptBins)-1,array('f',ptBins))

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
        return self._h2.GetBinContent(ipt,iae)

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
                        return tgraph.GetY()[i]
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
                return tgraph.GetY()[i]
        raise RuntimeError, "Did not find pt %s, eta %s" % (pt,eta)


sfIdEtaLow = FetchFromTGraphsEta("../plotting/plots/76X_220116/zTnP//mupog_v2_jpsi/00_harvest/mu_Loose_pt7.root", "ratio_syst")
sfIdPtEta  = FetchFromTH2POG("MuonID_Z_RunCD_Reco76X_Feb15.root", "MC_NUM_LooseID_DEN_genTracks_PAR_pt_spliteta_bin1/pt_abseta_ratio")
sfSIPEta   = FetchFromTGraphsEta("../plotting/plots/76X_220116/zTnP//mupog_v3/00_harvest/mu_SIP8_pt20.root", "ratio_syst")
sfIsoPt    = FetchFromTGraphsPts(
    [ ((0.0, 1.2), "../plotting/plots/76X_220116/zTnP/mupog_v3/00_harvest/mu_MiniIso04_barrel.root"),
      ((1.2, 2.4), "../plotting/plots/76X_220116/zTnP/mupog_v3/00_harvest/mu_MiniIso04_endcap.root") ],
    "ratio_syst"
)
sfTrk = lambda pt, eta : 0.99 if pt <= 10 else 1.0

stack = [ ( sfIdEtaLow, (0.0, 20.), (-2.4, 2.4) ),
          ( sfIdPtEta , (20., 80.), (-2.4, 2.4) ),
          ( sfSIPEta  , (0.0, 80.), (-2.4, 2.4) ),
          ( sfIsoPt   , (0.0, 80.), (-2.4, 2.4) ), 
          ( sfTrk     , (0.0, 80.), (-2.4, 2.4) ), ]
for ix in xrange(1,TH2.GetNbinsX()+1):
    for iy in xrange(1,TH2.GetNbinsY()+1):
        eta = TH2.GetXaxis().GetBinCenter(ix)
        pt  = TH2.GetYaxis().GetBinCenter(iy)
        sf  = 1.0
        for prod,ptr,etar in stack:
            if ptr[0] <= pt and pt <= ptr[1]:
                if etar[0] <= eta and eta <= etar[1]:
                    sf *= prod(pt,eta)
        TH2.SetBinContent(ix,iy, sf) 
out = ROOT.TFile("final_ttH.root","RECREATE")
out.WriteTObject(TH2)
out.Close()
                                

