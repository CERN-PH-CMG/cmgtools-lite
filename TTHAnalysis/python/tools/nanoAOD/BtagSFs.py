from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 

class BtagSFs( Module ):
    def __init__(self, jetcoll):
        self.jetcoll = jetcoll
        self.vars = ['btagSF_shape', 'btagSF_shape_up_jes', 'btagSF_shape_down_jes', 'btagSF_shape_up_lf', 'btagSF_shape_down_lf', 'btagSF_shape_up_hf', 'btagSF_shape_down_hf', 'btagSF_shape_up_hfstats1', 'btagSF_shape_down_hfstats1', 'btagSF_shape_up_hfstats2', 'btagSF_shape_down_hfstats2', 'btagSF_shape_up_lfstats1', 'btagSF_shape_down_lfstats1', 'btagSF_shape_up_lfstats2', 'btagSF_shape_down_lfstats2', 'btagSF_shape_up_cferr1', 'btagSF_shape_down_cferr1', 'btagSF_shape_up_cferr2', 'btagSF_shape_down_cferr2']

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        for var in self.vars:
            self.out.branch(var,'F')

    def analyze(self, event):
        jets = [ j for j in Collection(event, self.jetcoll)] 
        for var in self.vars: 
            res = 1
            for jet in jets: res *= getattr(jet,var)
            self.out.fillBranch(var,res) 
        return True
