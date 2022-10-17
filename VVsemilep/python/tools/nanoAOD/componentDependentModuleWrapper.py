from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class componentDependentModuleWrapper( Module ):
    def __init__(self):
        self._worker = None
    def beginJob(self):
        if self._worker: self._worker.beginJob()
    def endJob(self):
        if self._worker: self._worker.endJob()
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        if self._worker: self._worker.beginFile(inputFile, outputFile, inputTree, wrappedOutputTree)
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        if self._worker: self._worker.endFile(inputFile, outputFile, inputTree, wrappedOutputTree)
    def analyze(self, event):
        return self._worker.analyze(event) if self._worker else True
    def initComponent(self, component):
        raise RuntimeError("This method should be implemented, setting self._worker to a meaningful module.")
