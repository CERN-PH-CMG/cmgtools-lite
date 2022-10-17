from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from CMGTools.TTHAnalysis.tools.nanoAOD.friendVariableProducerTools import writeOutput


jesComponents = [
    "AbsoluteMPFBias",
    "AbsoluteScale"  ,
    "AbsoluteStat"   ,
    "FlavorQCD"      ,
    "Fragmentation"  ,
    "PileUpDataMC"   ,
    "PileUpPtBB"     ,
    "PileUpPtEC1"    ,
    "PileUpPtEC2"    ,
    "PileUpPtHF"     ,
    "PileUpPtRef"    ,
    "RelativeFSR"    ,
    "RelativeJEREC1" ,
    "RelativeJEREC2" ,
    "RelativeJERHF"  ,
    "RelativePtBB"   ,
    "RelativePtEC1"  ,
    "RelativePtEC2"  ,
    "RelativePtHF"   ,
    "RelativeBal"    ,
    #"RelativeSample" , not there...
    "RelativeStatEC" ,
    "RelativeStatFSR",
    "RelativeStatHF" ,
    "SinglePionECAL" ,
    "SinglePionHCAL" ,
    "TimePtEta"      ,    
]

class BtagSFs( Module ):
    def __init__(self, jetcoll, corrs={}):
        self.jetcoll = jetcoll
        self.corrs = corrs
        self.vars = ['', '_up_lf', '_down_lf', '_up_hf', '_down_hf', '_up_hfstats1', '_down_hfstats1', '_up_hfstats2', '_down_hfstats2', '_up_lfstats1', '_down_lfstats1', '_up_lfstats2', '_down_lfstats2', '_up_cferr1', '_down_cferr1', '_up_cferr2', '_down_cferr2'] + (['_up_jes', '_down_jes'] if not self.corrs else (['_up_jes%s'%x for x in jesComponents]+['_down_jes%s'%x for x in jesComponents]))
        self.vars = [ 'btagSF_shape%s'%x for x in self.vars ] 
        self.isGroups = False
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.wrappedOutputTree = wrappedOutputTree
        for var in self.vars:
            if self.corrs and 'jes' in var: continue
            self.wrappedOutputTree.branch(var,'F')
        if self.corrs: 
            for key in self.corrs: 
                if type(self.corrs[key]) != int and type(self.corrs[key]) != float: 
                    self.isGroups=True
                    break
            if not self.isGroups: 
                for br in ['up_jesCorr','down_jesCorr','up_jesUnCorr','down_jesUnCorr']:
                    self.wrappedOutputTree.branch('btagSF_shape_%s'%br, 'F')
            else: 
                for key in self.corrs:
                    self.wrappedOutputTree.branch('btagSF_shape_up_jes%s'%key, 'F')
                    self.wrappedOutputTree.branch('btagSF_shape_down_jes%s'%key, 'F')

    def analyze(self, event):
        jets = [ j for j in Collection(event, self.jetcoll)] 
        ret = {} 
        for var in self.vars: 
            res = 1
            for jet in jets: 
                if jet.pt<25: continue
                res *= getattr(jet,var)
            ret[var] = res
        if not self.isGroups: 
            resCorrUp  =0; resCorrDown=0;
            resUnCorrUp=0; resUnCorrDown=0;
            for corr in self.corrs:
                resCorrUp     = (resCorrUp**2   + self.corrs[corr]    *(ret['btagSF_shape_up_jes%s'  %corr]-ret['btagSF_shape'])**2)**0.5
                resCorrDown   = (resCorrDown**2 + self.corrs[corr]    *(ret['btagSF_shape_down_jes%s'%corr]-ret['btagSF_shape'])**2)**0.5
                resUnCorrUp   = (resUnCorrUp**2   + (1-self.corrs[corr])*(ret['btagSF_shape_up_jes%s'  %corr]-ret['btagSF_shape'])**2)**0.5
                resUnCorrDown = (resUnCorrDown**2 + (1-self.corrs[corr])*(ret['btagSF_shape_down_jes%s'%corr]-ret['btagSF_shape'])**2)**0.5
            if self.corrs:
                for corr in self.corrs: 
                    ret.pop( 'btagSF_shape_up_jes%s'%corr)
                    ret.pop( 'btagSF_shape_down_jes%s'%corr)
            ret['btagSF_shape_up_jesCorr']     = resCorrUp     + ret['btagSF_shape'] 
            ret['btagSF_shape_down_jesCorr']   = -resCorrDown   + ret['btagSF_shape']
            ret['btagSF_shape_up_jesUnCorr']   = resUnCorrUp   + ret['btagSF_shape']
            ret['btagSF_shape_down_jesUnCorr'] = -resUnCorrDown + ret['btagSF_shape']

        else: 
            for corr in self.corrs:
                ret['btagSF_shape_grouped_up_jes%s'%corr] =0; ret['btagSF_shape_grouped_down_jes%s'%corr] =0; 
                for comp in self.corrs[corr]:
                    if comp == "RelativeSample": continue # not here
                    ret['btagSF_shape_grouped_up_jes%s'%corr] = ( ret['btagSF_shape_grouped_up_jes%s'%corr]**2 + (ret['btagSF_shape_up_jes%s'  %comp]-ret['btagSF_shape'])**2)**0.5

                    ret['btagSF_shape_grouped_down_jes%s'%corr] = ( ret['btagSF_shape_grouped_down_jes%s'%corr]**2 + (ret['btagSF_shape_down_jes%s'  %comp]-ret['btagSF_shape'])**2)**0.5
                    ret.pop( 'btagSF_shape_up_jes%s'%comp)
                    ret.pop( 'btagSF_shape_down_jes%s'%comp)
                ret['btagSF_shape_up_jes%s'%corr]   = ret['btagSF_shape_grouped_up_jes%s'%corr] + ret['btagSF_shape'] 
                ret['btagSF_shape_down_jes%s'%corr] = -ret['btagSF_shape_grouped_down_jes%s'%corr] + ret['btagSF_shape'] 
                ret.pop( 'btagSF_shape_grouped_up_jes%s'%corr )
                ret.pop( 'btagSF_shape_grouped_down_jes%s'%corr )
        writeOutput(self, ret)
        return True
