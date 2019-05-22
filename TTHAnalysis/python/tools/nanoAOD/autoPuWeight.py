from CMGTools.TTHAnalysis.tools.nanoAOD.componentDependentModuleWrapper import componentDependentModuleWrapper
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import puAutoWeight_2016, puAutoWeight_2017, puAutoWeight_2018

class autoPuWeightModule( componentDependentModuleWrapper ):
    def __init__(self, w2016, w2017, w2018):
        self._w2016 = w2016
        self._w2017 = w2017
        self._w2018 = w2018
    def initComponent(self, component):
        if component.isData:
            self._worker = None
        elif "Fall17" in component.dataset:
            self._worker = self._w2017()
        elif "Autumn18" in component.dataset:
            self._worker = self._w2018()
        elif "Summer16" in component.dataset:
            self._worker = self._w2016()
        else:
            raise RuntimeError("Can't detect PU scenario for %s, %s" % (component.name, component.dataset))

autoPuWeight = lambda : autoPuWeightModule(puAutoWeight_2016, puAutoWeight_2017, puAutoWeight_2018)
