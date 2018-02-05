from PhysicsTools.HeppyCore.framework.heppy_loop import getHeppyOption
from CMGTools.RootTools.samples.configTools import *

def switchOffMEs(sequence, verbose=False):
    import CMGTools.HToZZ4L.analyzers.FourLeptonAnalyzerBase
    base = CMGTools.HToZZ4L.analyzers.FourLeptonAnalyzerBase.FourLeptonAnalyzerBase
    for item in sequence:
        if issubclass(item.class_object, base):
            if verbose: print "Switch off MEs for %s (%s)" % (item.name, item.class_object)
            item.doMEs = False

