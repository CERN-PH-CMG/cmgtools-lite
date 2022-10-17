#!/usr/bin/env python
#from tree2yield import *
from CMGTools.TTHAnalysis.plotter.tree2yield import *
from CMGTools.TTHAnalysis.plotter.projections import *
from CMGTools.TTHAnalysis.plotter.mcAnalysis import *
from CMGTools.TTHAnalysis.plotter.mcPlots import *
from CMGTools.TTHAnalysis.plotter.mcDump import MCDumpEvent
from CMGTools.TTHAnalysis.treeReAnalyzer2 import *
import string

if "/fakeRate_cc.so" not in ROOT.gSystem.GetLibraries(): 
    ROOT.gROOT.ProcessLine(".L %s/src/CMGTools/TTHAnalysis/python/plotter/fakeRate.cc+" % os.environ['CMSSW_BASE']);

class MCNtupleModule(Module):
    def __init__(self,name,cut,columns,options=None,booker=None):
        Module.__init__(self,name,booker)
        self.cut = cut 
        self.columns = columns[:]
        self.options = options
        self.mcde = MCDumpEvent()
        self.dumpFile = None
        self.dumpFileName = None
    def __del__(self):
        if self.dumpFile: self.endJob()
    def beginComponent(self,tty):
        if self.dumpFile: self.endJob()
        self.mcde.beginComponent(tty)
        if self.dumpFileName:
            self.dumpFile = self.dumpFileName.format(cname=tty.cname())
            self.dumpTFile = ROOT.TFile.Open(self.dumpFile, "RECREATE")
            self.dumpTTree = ROOT.TTree("t","t")
            self.dumpPyTree = PyTree(self.dumpTTree)
            for p in self.columns: 
                self.dumpPyTree.branch(p.name,"F" if 'evt'!=p.name else "l")
            self.dumpPyTree.branch("_weight_","F")
            self.thisWeight = tty.getWeightForCut(self.cut)
    def openOutFile(self,dumpFileName):
        if "{cname}" not in dumpFileName: raise RuntimeError
        self.dumpFileName = dumpFileName
    def analyze(self,ev):
        self.mcde.update(ev)
        weight = self.mcde.get(self.thisWeight, adapt=False)
        if weight != 0:
            for p in self.columns:
                setattr(self.dumpPyTree, p.name, self.mcde.get(p.expr))
            setattr(self.dumpPyTree, "_weight_", weight)
            self.dumpPyTree.fill()
        return True
    def endJob(self):
        if self.dumpFile:
            self.dumpTFile.WriteTObject(self.dumpTTree)
            print "Wrote tree for %s with %d events" % (self.dumpFile, self.dumpTTree.GetEntries())
            self.dumpTFile.Close()
            del self.dumpPyTree
            del self.dumpTTree
            del self.dumpTFile
            self.dumpFile = None

def addMCNtupleOptions(parser):
    addPlotMakerOptions(parser)
    parser.add_option("--dumpFile",  dest="dumpFile", default=None, type="string", help="Ntuple file name")

if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser(usage="%prog [options] mca.txt cuts.txt  plots.txt outputfileName")
    addMCNtupleOptions(parser)
    (options, args) = parser.parse_args()
    mca = MCAnalysis(args[0],options)
    cut = CutsFile(args[1],options).allCuts()
    plots = PlotFile(args[2],options).plots()
    mcdm = MCNtupleModule("dump",cut,plots,options)
    mcdm.openOutFile(args[3])
    el = EventLoop([mcdm])
    mca.processEvents(EventLoop([mcdm]),cut=cut)
