from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class xsecTagger( Module ):
    def __init__(self):
        self._xsec = None
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        if self._xsec:
            self.wrappedOutputTree = wrappedOutputTree
            self.wrappedOutputTree.branch('xsec','F')
    def analyze(self, event):
        if self._xsec:
            self.wrappedOutputTree.fillBranch('xsec', self._xsec)
        return True
    def initComponent(self, component):
        if component.isMC:
            self._xsec = getattr(component, 'xSection', None)

xsecTag = lambda : xsecTagger()
