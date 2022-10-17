#!/usr/bin/env python
from math import *
import re, string
from CMGTools.TTHAnalysis.plotter.mcDump import *

from optparse import OptionParser
import json

class TTHDumper(Module):
    def __init__(self,name,options=None,booker=None):
        Module.__init__(self,name,booker)
        self.options = options
        self.passing_entries = 0
        self.dumpFile = None
    def __del__(self):
        if self.dumpFile: self.dumpFile.close()
    def beginComponent(self,tty):
        pass
    def openOutFile(self,dumpFileName):
        if self.dumpFile: raise RuntimeError,'Output file already open'
        self.dumpFile = open(dumpFileName,'w')
    def getPassingEntries(self):
        return self.passing_entries
    def analyze(self,ev):
        self.makeVars(ev)
        out = self.makeText(ev)
        if len(out)>0:
            self.passing_entries += 1
            if self.dumpFile: self.dumpFile.write(out+'\n')
            else:             print out
        return True
    def makeVars(self,ev):
        self.leps = [l for l in Collection(ev,"LepGood","nLepGood") ]

        jets1 = Collection(ev,"Jet","nJet")
        jets2 = Collection(ev,"DiscJet","nDiscJet")
        ijets = ev.iJ_Recl
        self.jets = [ (jets1[ijets[i]] if ijets[i] >= 0 else jets2[-1-ijets[i]]) for i in xrange(ev.nJetSel_Recl) ]
        self.jets.sort(key = lambda j : j.pt, reverse=True)
    def makeText(self,ev):
        ret = ""
        ret += "run %6d lumi %4d event %11d (id: %d:%d:%d) \n" % (ev.run, ev.lumi, ev.evt, ev.run, ev.lumi, ev.evt)
        for i,l in enumerate(self.leps):
            ret += "    lepton %d: id %+2d pt %5.1f eta %+4.2f phi %+4.2f   FO %d tight %d  mvaTTH %+5.3f miniRelIso %5.3f sip3d %5.2f " % (
                    i+1, l.pdgId,l.pt,l.eta,l.phi, l.isFO_Recl, l.isTight_Recl, l.mvaTTH, l.miniRelIso, l.sip3d,  )
            if self.options.ismc:
                ret += "   mcMatch id %+4d, any %+2d" % (l.mcMatchId, l.mcMatchAny)
            if self.options.ismore:
                ret += " ptRatio %4.2f ptRel %5.1f jetBTag %5.3f dxy %+4.3f dz %+4.3f eleId %+5.3f muId %d lostHits %1d convVeto %d tightCharge %d" % (
                        l.jetPtRatiov2, l.jetPtRelv2, max(0,l.jetBTagCSV), l.dxy, l.dz, l.mvaIdSpring15, l.mediumMuonId, l.lostHits,l.convVeto, l.tightCharge)
            ret += "\n"
        for i,j in enumerate(self.jets):
            ret += "    jet %d:  pt %5.1f (raw %5.1f) eta %+4.2f phi %+4.2f  btag %4.3f" % (i+1, j.pt, j.rawPt, j.eta, j.phi, min(1.,max(0.,j.btagCSV)))
            if self.options.ismc:
                ret += " mcMatch %2d mcFlavour %2d mcPt %5.1f" % (j.mcMatchId, j.mcFlavour, j.mcPt)
            ret += "\n"
        ret += "    met %6.2f (phi %+4.2f)  htJet25j %7.2f mhtJet25 %6.2f\n" % (ev.met_pt, ev.met_phi, ev.htJet25j_Recl, ev.mhtJet25_Recl)
        ret += "    vertices %d\n" % (ev.nVert)
        ret += "    HLT: " + " ".join([t for t in "Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_DZ Ele23_WPLoose_Gsf Ele27_eta2p1_WP75_Gsf Ele27_eta2p1_WPLoose_Gsf IsoMu20 IsoTkMu20 Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL".split() if getattr(ev,"HLT_BIT_HLT_"+t+"_v")]+[t for t in "DoubleMu DoubleElMu DoubleMuEl TripleMu TripleMuA".split() if getattr(ev,"HLT_"+t)]) + "\n"
        ret += ""
        return ret

if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser(usage="%prog [options] mca.txt cuts.txt 'format string' ")
    parser.add_option("-m", "--mc", dest="ismc",  default=False, action="store_true",  help="print MC match info")
    parser.add_option("-M", "--more", dest="ismore",  default=False, action="store_true",  help="print MC match info")
    addMCDumpOptions(parser)
    (options, args) = parser.parse_args()
    mca = MCAnalysis(args[0],options)
    cut = CutsFile(args[1],options).allCuts()
    mcdm = TTHDumper("dump",options)
    if options.dumpFile: mcdm.openOutFile(options.dumpFile)
    el = EventLoop([mcdm])
    mca.processEvents(EventLoop([mcdm]), cut=cut)
    #print 'Passing entries:',mcdm.getPassingEntries()

