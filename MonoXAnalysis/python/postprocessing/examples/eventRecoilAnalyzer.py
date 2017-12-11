import ROOT
import os
import numpy as np
ROOT.PyConfig.IgnoreCommandLineOptions = True
from math import *

from CMGTools.MonoXAnalysis.postprocessing.framework.datamodel import Collection,Object
from CMGTools.MonoXAnalysis.postprocessing.framework.eventloop import Module
from PhysicsTools.HeppyCore.utils.deltar import deltaR,deltaPhi
 
class VisibleVectorBoson():
    def __init__(self,selLeptons):
        self.p4=ROOT.TLorentzVector(0,0,0,0)
        self.sumEt=0
        self.legs=[]
        for l in selLeptons:
            self.legs.append(l)
            self.p4+=l
            self.sumEt+=l.Pt()
    def VectorT(self):
        return ROOT.TVector3(self.p4.Px(),self.p4.Py(),0)
    

class EventRecoilAnalyzer(Module):
    '''
    Analyzes the event recoil and derives the corrections in pt and phi to bring the estimators to the true vector boson recoil.
    Loop on PF candidates, skipping selected leptons and storing useful variables.
    Based on the original code by N. Foppiani and O. Cerri (Pisa)
    '''
    def __init__(self, tag ):
        self.tag=tag

    def beginJob(self):
        """actions taken start of the job"""
        pass

    def endJob(self):
        """actions taken end of the job"""
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        """actions taken at the start of the file"""

        #start by calling init readers
        self.initReaders(inputTree)

        #define output
        self.out = wrappedOutputTree    
        self.out.branch("leadch_pt",   "F")
        self.out.branch("leadch_phi",   "F")
        self.out.branch("leadneut_pt", "F")
        self.out.branch("leadneut_phi", "F")
    
        #recoil types
        for rtype in ["truth","gen","met", "puppimet", 'ntmet','ntcentralmet', 'tkmet', 'chsmet', 'npvmet', 'ntnpv', 'centralntnpv', 'centralmetdbeta']:
            for var in ['recoil_pt','recoil_phi', 'recoil_sphericity', 'm','n','recoil_e1','recoil_e2', 'mt',
                        'dphi2met','dphi2puppimet','dphi2ntnpv','dphi2centralntnpv','dphi2centralmetdbeta','dphi2leadch','dphi2leadneut']:
                self.out.branch("{0}_{1}".format(rtype,var), "F")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        """actions taken at the end of the file"""
        pass

    def initReaders(self,tree): # this function gets the pointers to Value and ArrayReaders and sets them in the C++ worker class                                 
        try:
            self.nGenPart = tree.valueReader("nGenPart")
            for var in ["pt","eta","phi","mass","pdgId","status"] : 
                setattr(self,"GenPart_"+var, tree.arrayReader("GenPart_"+var))
        except:
            print '[eventRecoilAnalyzer][Warning] Unable to attach to generator-level particles, only reco info will be made available'
        self._ttreereaderversion = tree._ttreereaderversion

    def getMCTruth(self,event):
        """computes the MC truth for this event"""

        #dummy values
        visibleV,V,h,ht=VisibleVectorBoson(selLeptons=[]),ROOT.TLorentzVector(0,0,0,0),ROOT.TVector3(0,0,0),0

        #nothing to do for data :)
        if event.isData : 
            return visibleV,V,h,ht

        #get the neutrinos
        ngenNu = self.out._branches["nGenPromptNu"].buff[0]
        nuSum=ROOT.TLorentzVector(0,0,0,0)
        for i in xrange(0,ngenNu):
            p4=ROOT.TLorentzVector(0,0,0,0)
            p4.SetPtEtaPhiM( self.out._branches["GenPromptNu_pt"].buff[i],
                             self.out._branches["GenPromptNu_eta"].buff[i],
                             self.out._branches["GenPromptNu_phi"].buff[i],
                             self.out._branches["GenPromptNu_mass"].buff[i] )
            nuSum+=p4
            break

        #construct the visible boson
        dressedLeps=[]
        ngenLep=self.out._branches["nGenLepDressed"].buff[0]
        for i in xrange(0,ngenLep):
            dressedLeps.append( ROOT.TLorentzVector(0,0,0,0) )
            dressedLeps[-1].SetPtEtaPhiM( self.out._branches["GenLepDressed_pt"].buff[i],
                                          self.out._branches["GenLepDressed_eta"].buff[i],
                                          self.out._branches["GenLepDressed_phi"].buff[i],
                                          self.out._branches["GenLepDressed_mass"].buff[i] )
            if i==0 :
                visibleV=VisibleVectorBoson(selLeptons=[dressedLeps[-1]])
                V=visibleV.p4+nuSum
            for j in xrange(0,i):
                ll=dressedLeps[j]+dressedLeps[i]
                if abs(ll.M()-91)>15 : continue
                visibleV=VisibleVectorBoson(selLeptons=[dressedLeps[j],dressedLeps[i]])
                V=visibleV.p4
                break

        #hadronic recoil
        met=ROOT.TLorentzVector(0,0,0,0)
        met.SetPtEtaPhiM(event.tkGenMet_pt,0,event.tkGenMet_phi,0.)
        if visibleV : met+=visibleV.p4
        h=ROOT.TVector3(-met.Px(),-met.Py(),0.)
        ht=event.tkGenMetInc_sumEt
        if visibleV : ht -= visibleV.sumEt

        return visibleV,V,h,ht

    def getVisibleV(self,event):
        """
        tries to reconstruct a Z from the selected leptons
        for a W only the leading lepton is returned
        """
        
        lepColl = Collection(event, "LepGood")
        leps=[]
        zCand=None
        nl=len(lepColl)
        for i in xrange(0,nl):
            l=lepColl[i]
            leps.append( l.p4() )

            #check if a Z candidate can be formed
            for j in xrange(0,i):
                if lepColl[i].pdgId != lepColl[j].pdgId : continue
                ll=leps[i]+leps[j]
                if abs(ll.M()-91)>15 : continue
                zCand=(i,j)
                break

        #build the visible V from what has been found
        visibleV=VisibleVectorBoson(selLeptons=[leps[0]]) if len(leps)>0  else None
        if zCand:
            visibleV=VisibleVectorBoson(selLeptons=[leps[zCand[0]],leps[zCand[1]]])

        return visibleV

    def summarizeMetEstimator(self,event, metObjects=['met'], weights=[] ):
        """gets the summary out of a met estimator"""
        p4,sumEt,count=None,0,0
        for i in xrange(0,len(metObjects)):
            wgt=weights[i]
            imet=Object(event,metObjects[i])
            if p4 is None: p4 = imet.p4()*wgt
            else : p4 += imet.p4()*wgt
            sumEt += imet.sumEt*wgt
            try:
                count += getattr(event,'%s_Count'%metObjects[i])*wgt
            except:
                pass
        return p4,sumEt,count

    def getRecoRecoil(self,event,metP4,sumEt,visibleV):
        """computes the MC truth for this event"""

        #charged recoil estimators
        h=ROOT.TVector3(-metP4.Px(),-metP4.Py(),0.)
        ht=sumEt
        if visibleV:
            for l in visibleV.legs:
                ht -= l.Pt()
                h  -= l.Vect()

        return h,max(ht,0.),metP4.M()
    
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""

        if event._tree._ttreereaderversion > self._ttreereaderversion:
            self.initReaders(event._tree)

        #MC truth
        gen_visibleV,gen_V,gen_h,gen_ht=self.getMCTruth(event)

        #selected leptons at reco level
        visibleV=self.getVisibleV(event)
        if not visibleV : return False
        
        #leading PF candidates
        self.out.fillBranch('leadch_pt',    event.leadCharged_pt)
        self.out.fillBranch('leadch_phi',   event.leadCharged_phi)
        self.out.fillBranch('leadneut_pt',  event.leadNeutral_pt)
        self.out.fillBranch('leadneut_phi', event.leadNeutral_phi)

        #met estimators
        metEstimators={
            'met'               : self.summarizeMetEstimator(event,
                                                             ['met'], 
                                                             [1]),
            'puppimet'          : self.summarizeMetEstimator(event,
                                                             ['puppimet'], 
                                                             [1]),
            'ntmet'             : self.summarizeMetEstimator(event,
                                                             ['ntMet'],       
                                                             [1]),
            'ntcentralmet'      : self.summarizeMetEstimator(event,
                                                             ['ntCentralMet'], 
                                                             [1]),             
            'tkmet'             : self.summarizeMetEstimator(event,
                                                             ['tkMetPVLoose'], 
                                                             [1]),  
            'chsmet'            : self.summarizeMetEstimator(event,
                                                             ['tkMetPVchs'], 
                                                             [1]),  
            'npvmet'            : self.summarizeMetEstimator(event,
                                                             ['tkMetPUPVLoose'],                               
                                                             [1]),  
            'ntnpv'             : self.summarizeMetEstimator(event,
                                                             ['ntMet','tkMetPUPVLoose'],                       
                                                             [1,1]),  
            'centralntnpv'      : self.summarizeMetEstimator(event,
                                                             ['ntCentralMet','tkMetPUPVLoose'],                
                                                             [1,1]),  
            'centralmetdbeta'   : self.summarizeMetEstimator(event,
                                                             ['tkMetPVLoose','ntCentralMet','tkMetPUPVLoose'], 
                                                             [1,1,0.5]),  
            }
       
        #recoil estimators
        for metType in metEstimators.keys() + ["truth","gen"]:

            #some may need to be specified
            if metType=="truth":
                vis   = gen_visibleV.VectorT()
                metP4 = gen_V
                h     = ROOT.TVector3(-gen_V.Px(),-gen_V.Py(),0)                
                ht    = gen_V.Pt()
                m     = gen_V.M()
                count = 0
            elif metType=='gen':
                vis   = gen_visibleV.VectorT()
                metP4=ROOT.TLorentzVector(0,0,0,0)
                metP4.SetPtEtaPhiM(event.tkGenMet_pt,0,event.tkGenMet_phi,0.)
                h     = gen_h
                ht    = gen_ht
                m     = 0
                count = 0
            else:
                vis = visibleV.VectorT()
                metP4, sumEt, count = metEstimators[metType]
                h, ht, m = self.getRecoRecoil(event=event,metP4=metP4,sumEt=sumEt,visibleV=visibleV)

            #save information to tree
            pt=h.Pt()
            phi=h.Phi()
            metphi=metP4.Phi()
            sphericity=pt/ht if ht>0 else -1               
            e1=gen_V.Pt()/h.Pt() if h.Pt()>0 else -1
            e2=deltaPhi(gen_V.Phi()+np.pi,h.Phi())
            mt2= 2*vis.Pt()*((vis+h).Pt())+vis.Pt()**2+vis.Dot(h) 
            mt=np.sqrt(mt2) if mt2>=0. else -np.sqrt(-mt2)

            self.out.fillBranch('%s_recoil_pt'%metType,            pt)
            self.out.fillBranch('%s_recoil_phi'%metType,           phi)
            self.out.fillBranch('%s_m'%metType,                    m)
            self.out.fillBranch('%s_recoil_sphericity'%metType,    sphericity)
            self.out.fillBranch('%s_n'%metType,                    count)
            self.out.fillBranch('%s_recoil_e1'%metType,            e1)
            self.out.fillBranch('%s_recoil_e2'%metType,            e2)
            self.out.fillBranch('%s_mt'%metType,                   mt)
            self.out.fillBranch('%s_dphi2met'%metType,             deltaPhi(metEstimators['met'][0].Phi(),             metphi) )
            self.out.fillBranch('%s_dphi2puppimet'%metType,        deltaPhi(metEstimators['puppimet'][0].Phi(),        metphi) )
            self.out.fillBranch('%s_dphi2ntnpv'%metType,           deltaPhi(metEstimators['ntnpv'][0].Phi(),           metphi) )
            self.out.fillBranch('%s_dphi2centralntnpv'%metType,    deltaPhi(metEstimators['centralntnpv'][0].Phi(),    metphi) )
            self.out.fillBranch('%s_dphi2centralmetdbeta'%metType, deltaPhi(metEstimators['centralmetdbeta'][0].Phi(), metphi) )
            self.out.fillBranch('%s_dphi2leadch'%metType,          deltaPhi(event.leadCharged_phi,                     metphi) )
            self.out.fillBranch('%s_dphi2leadneut'%metType,        deltaPhi(event.leadNeutral_phi,                     metphi) )

        return True

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed
eventRecoilAnalyzer = lambda : EventRecoilAnalyzer(tag='')
