import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
# group jec components 
# taken from https://docs.google.com/spreadsheets/d/1Feuj1n0MdotcPq19Mht7SUIgvkXkA4hiB0BxEuBShLw/edit?ouid=111820255692530107608&usp=sheets_home&ths=true

import os
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import math

class jetmetGrouper(Module):
    def __init__(self, groups, jetbranch, metbranch, dumpMore=[]):
        self.groups     = groups    
        self.jetbranch = jetbranch
        self.metbranch = metbranch
        self.dumpMore  = dumpMore

    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.wrappedOutputTree = wrappedOutputTree
        for group in self.groups:
            for sign in ['Up','Down']:
                self.wrappedOutputTree.branch("%s_pt_jes%s%s"%(self.jetbranch,group,sign) , "F", lenVar="n%s"%self.jetbranch)
                self.wrappedOutputTree.branch("%s_pt_jes%s%s"%(self.metbranch,group,sign) , "F")
                self.wrappedOutputTree.branch("%s_phi_jes%s%s"%(self.metbranch,group,sign) , "F")
        for br in self.dumpMore:
            self.wrappedOutputTree.branch(**br)
        
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):

        """Nominal variables"""
        jets = Collection(event, '%s'%self.jetbranch)
        met = Object(event, self.metbranch)
        metPt  = getattr(met, "pt_nom", "pt")
        metPhi = getattr(met, "phi_nom", "phi")
        metPx  = metPt*math.cos(metPhi)
        metPy  = metPt*math.sin(metPhi)


        for group in self.groups:
            for sign in ['Up','Down']:
                jetVar    = []
                metPxVar  = metPx
                metPyVar  = metPy
                for j in jets: 
                    thePt  = getattr(j, "pt_nom", "pt")
                    thePhi = getattr(j, "phi") 
                    jetVar.append(0)
                    for comp in self.groups[group]:
                        jetVar[-1] = (jetVar[-1]**2 + (getattr(j,"pt_jes"+ comp + sign)-thePt)**2)**0.5
                    
                    metPxVar    = metPxVar - (1 if sign == 'Up' else -1) * jetVar[-1] * math.cos(thePhi)
                    metPyVar    = metPyVar - (1 if sign == 'Up' else -1) * jetVar[-1] * math.sin(thePhi)
                    jetVar[-1]  = thePt + (1 if sign == 'Up' else -1) * jetVar[-1]
                self.wrappedOutputTree.fillBranch("%s_pt_jes%s%s"%(self.jetbranch,group,sign),  jetVar       )
                self.wrappedOutputTree.fillBranch("%s_pt_jes%s%s"%(self.metbranch,group,sign),  (metPxVar**2 + metPyVar**2)**0.5)
                
                self.wrappedOutputTree.fillBranch("%s_phi_jes%s%s"%(self.metbranch,group,sign), math.atan2(metPyVar,  metPxVar))
        for br in self.dumpMore:
            self.wrappedOutputTree.fillBranch(br['name'], getattr(event, br['name']))

        return True

moreVars = [
    {'name' : 'Jet_pt_nom'   ,'rootBranchType' : 'F','lenVar': 'nJet'},
    {'name' : 'MET_pt_jer'   ,'rootBranchType' : 'F'},
    {'name' : 'MET_pt_nom'   ,'rootBranchType' : 'F'},
    {'name' : 'MET_pt_unclustEnUp'   ,'rootBranchType' : 'F'},
    {'name' : 'MET_pt_unclustEnDown'   ,'rootBranchType' : 'F'},
    {'name' : 'MET_phi_unclustEnUp'   ,'rootBranchType' : 'F'},
    {'name' : 'MET_phi_unclustEnDown'   ,'rootBranchType' : 'F'},
]


moreVars2017 = [
    {'name' : 'Jet_pt_nom'   ,'rootBranchType' : 'F','lenVar': 'nJet'},
    {'name' : 'METFixEE2017_pt_nom'   ,'rootBranchType' : 'F'},
    {'name' : 'METFixEE2017_pt_jer'   ,'rootBranchType' : 'F'},
    {'name' : 'METFixEE2017_pt_unclustEnUp'   ,'rootBranchType' : 'F'},
    {'name' : 'METFixEE2017_pt_unclustEnDown'   ,'rootBranchType' : 'F'},
    {'name' : 'METFixEE2017_phi_unclustEnUp'   ,'rootBranchType' : 'F'},
    {'name' : 'METFixEE2017_phi_unclustEnDown'   ,'rootBranchType' : 'F'},
]

for jer in ['barrel','endcap1','endcap2highpt','endcap2lowpt' ,'forwardhighpt','forwardlowpt']:
    for var in ['Up','Down']:
        moreVars.extend( [
            {'name' : 'Jet_pt_jer%s%s'%(jer,var)   ,'rootBranchType' : 'F','lenVar': 'nJet'},
            {'name' : 'MET_pt_jer%s%s'%(jer,var)   ,'rootBranchType' : 'F'},
            {'name' : 'MET_phi_jer%s%s'%(jer,var)  ,'rootBranchType' : 'F'},
        ])
moreVars.extend( [
    {'name' : 'Jet_pt_HEMUp'   ,'rootBranchType' : 'F','lenVar': 'nJet'},
    {'name' : 'MET_pt_HEMUp'   ,'rootBranchType' : 'F'},
    {'name' : 'MET_phi_HEMUp'  ,'rootBranchType' : 'F'},
    {'name' : 'Jet_pt_HEMDown'   ,'rootBranchType' : 'F','lenVar': 'nJet'},
    {'name' : 'MET_pt_HEMDown'   ,'rootBranchType' : 'F'},
    {'name' : 'MET_phi_HEMDown'  ,'rootBranchType' : 'F'},
])

for jer in ['barrel','endcap1','endcap2highpt','endcap2lowpt' ,'forwardhighpt','forwardlowpt']:
    for var in ['Up','Down']:
        moreVars2017.extend( [
            {'name' : 'Jet_pt_jer%s%s'%(jer,var)   ,'rootBranchType' : 'F','lenVar': 'nJet'},
            {'name' : 'METFixEE2017_pt_jer%s%s'%(jer,var)   ,'rootBranchType' : 'F'},
            {'name' : 'METFixEE2017_phi_jer%s%s'%(jer,var)  ,'rootBranchType' : 'F'},
        ])
moreVars2017.extend( [
    {'name' : 'Jet_pt_HEMUp'   ,'rootBranchType' : 'F','lenVar': 'nJet'},
    {'name' : 'METFixEE2017_pt_HEMUp'   ,'rootBranchType' : 'F'},
    {'name' : 'METFixEE2017_phi_HEMUp'  ,'rootBranchType' : 'F'},
    {'name' : 'Jet_pt_HEMDown'   ,'rootBranchType' : 'F','lenVar': 'nJet'},
    {'name' : 'METFixEE2017_pt_HEMDown'   ,'rootBranchType' : 'F'},
    {'name' : 'METFixEE2017_phi_HEMDown'  ,'rootBranchType' : 'F'},
])



groups = {'HF'                 : ['PileUpPtHF', 'RelativeJERHF', 'RelativePtHF'], 
          'BBEC1_year'         : ['RelativeJEREC1', 'RelativePtEC1', 'RelativeStatEC'],
          'FlavorQCD'          : ['FlavorQCD'],
          'RelativeSample_year': ['RelativeSample'], 
          'EC2'                : ['PileUpPtEC2'],
          'HF_year'            : ['RelativeStatHF'], 
          'RelativeBal'        : ['RelativeBal'], 
          'Absolute_year'      : ['AbsoluteStat', 'RelativeStatFSR', 'TimePtEta'],
          'BBEC1'              : ['PileUpPtBB', 'PileUpPtEC1', 'RelativePtBB'], 
          'EC2_year'           : ['RelativeJEREC2', 'RelativePtEC2'], 
          'Absolute'           : ['AbsoluteMPFBias', 'AbsoluteScale', 'Fragmentation', 'PileUpDataMC', 'PileUpPtRef', 'RelativeFSR', 'SinglePionECAL', 'SinglePionHCAL']
}

jetMetCorrelate2016 = lambda  : jetmetGrouper( groups, "Jet", "MET", dumpMore=moreVars)
jetMetCorrelate2017 = lambda  : jetmetGrouper( groups, "Jet", "METFixEE2017", dumpMore=moreVars2017)
jetMetCorrelate2018 = lambda  : jetmetGrouper( groups, "Jet", "MET", dumpMore=moreVars)
