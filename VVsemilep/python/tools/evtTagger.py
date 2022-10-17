from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection as NanoAODCollection 
from CMGTools.TTHAnalysis.tools.nanoAOD.friendVariableProducerTools import declareOutput, writeOutput



class EvtTagger(Module):
    def __init__(self,label,sel):
        self.label = label
        self.sel = sel

    # old interface
    def listBranches(self):
        biglist = [(self.label,"I")]
        return biglist
    def __call__(self,event):
        return self.runIt(event)

    # new interface
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        declareOutput(self,wrappedOutputTree, [(self.label,"I")])

    def analyze(self, event):
        writeOutput(self, self.runIt(event))
        return True

    def runIt(self,event):
        ret = {}
        good = True
        for sel in self.sel:
            if not sel(event):
                good = False
                break
        ret[self.label] = 1 if good else 0
        return ret

if __name__ == '__main__':
    from sys import argv
    file = ROOT.TFile(argv[1])
    tree = file.Get("tree")
    tree.vectorTree = True
    class Tester(Module):
        def __init__(self, name):
            Module.__init__(self,name,None)
            self.sf1 = EvtTagger("Met50",[lambda ev : ev.met_pt >= 50])
        def analyze(self,ev):
            print "\nrun %6d lumi %4d event %d" % (ev.run, ev.lumi, ev.evt)
            print self.sf1(ev)
    el = EventLoop([ Tester("tester") ])
    el.loop([tree], maxEvents = 50)

        
