#!/usr/bin/env python
import ROOT, os, re

class effWeighter:
    def __init__(self,hname,files,luminosities):
        self.hname = hname
        self.files = []
        for f in files:
            self.files.append(ROOT.TFile(f))
        self.luminosities = luminosities
    def __call__(self,outfile):
        self.tout = ROOT.TFile.Open(outfile,"recreate")
        lumi_tot = sum(l for l in self.luminosities)
        self.tout.cd()
        hweight = self.files[0].Get(self.hname).Clone("Lep_eff_weighted_"+self.hname)
        hweight.Reset()
        for i,f in enumerate(self.files):
            weight = self.luminosities[i]/lumi_tot
            print "weight for chunk ",i," = ",weight
            h = f.Get(self.hname).Clone(("Lep_eff_"+self.hname).replace("/","_"))
            f.Close()
            hweight.Add(h,weight)
        self.tout.WriteTObject(hweight.Clone())
        self.tout.Write()
        self.tout.Close()

if __name__ == '__main__':
    from sys import argv
    luminosities = [19.681,17.092]

    # Trigger part
    files = ["/afs/cern.ch/work/e/emanuele/public/wmass/leptonsf/MuonTriggerEfficienciesAndSF_RunBtoF.root",
             "/afs/cern.ch/work/e/emanuele/public/wmass/leptonsf/MuonTriggerEfficienciesAndSF_RunGtoH.root"]
    effw = effWeighter("IsoMu24_OR_IsoTkMu24_PtEtaBins/abseta_pt_ratio",files,luminosities)
    effw("/afs/cern.ch/work/e/emanuele/public/wmass/leptonsf/MuonTriggerEfficienciesAndSF_RunBtoH_Weighted.root")

    # ID part
    files = ["/afs/cern.ch/work/e/emanuele/public/wmass/leptonsf/MuonIDEfficienciesAndSF_BCDEF.root",
             "/afs/cern.ch/work/e/emanuele/public/wmass/leptonsf/MuonIDEfficienciesAndSF_GH.root"]
    effw = effWeighter("MC_NUM_TightID_DEN_genTracks_PAR_pt_eta/abseta_pt_ratio",files,luminosities)
    effw("/afs/cern.ch/work/e/emanuele/public/wmass/leptonsf/MuonIDEfficienciesAndSF_BCDEFGH_Weighted.root")

    # ISO part
    files = ["/afs/cern.ch/work/e/emanuele/public/wmass/leptonsf/MuonIsoEfficienciesAndSF_BCDEF.root",
             "/afs/cern.ch/work/e/emanuele/public/wmass/leptonsf/MuonIsoEfficienciesAndSF_GH.root"]
    effw = effWeighter("TightISO_TightID_pt_eta/abseta_pt_ratio",files,luminosities)
    effw("/afs/cern.ch/work/e/emanuele/public/wmass/leptonsf/MuonIsoEfficienciesAndSF_BCDEFGH_Weighted.root")
