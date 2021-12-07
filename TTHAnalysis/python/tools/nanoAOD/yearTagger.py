from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class yearTagger( Module ):
    def __init__(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.wrappedOutputTree = wrappedOutputTree
        self.wrappedOutputTree.branch('year','i')
        self.wrappedOutputTree.branch('suberaId','i')
    def analyze(self, event):
        self.wrappedOutputTree.fillBranch('year', self._year)
        self.wrappedOutputTree.fillBranch('suberaId', self._suberaId)
        return True
    def initComponent(self, component):
        if hasattr(component, 'year'):
            self._year = component.year
        elif ("Autumn18" in component.dataset) or ("UL18" in component.dataset) or ("Run2018" in component.dataset):
            self._year = 2018
        elif ("Fall17" in component.dataset) or ("UL17" in component.dataset) or ("Run2017" in component.dataset):
            self._year = 2017
        elif ("Summer16" in component.dataset) or ("UL16" in component.dataset)or ("Run2016" in component.dataset):
            self._year = 2016
        else:
            raise RuntimeError("Can't detect year scenario for %s, %s" % (component.name, component.dataset))

        if hasattr(component, 'suberaId'):
            self._suberaId = component.suberaId
        elif self._year ==2016:
            if ('APV' in component.dataset) or ('HIPM' in component.dataset): 
                self._suberaId=0  # pre-VFP
            else:
                self._suberaId=1 # post-VFP
        else:
            self._suberaId = 0 # no suberas for 2017 or 18

yearTag = lambda : yearTagger()
