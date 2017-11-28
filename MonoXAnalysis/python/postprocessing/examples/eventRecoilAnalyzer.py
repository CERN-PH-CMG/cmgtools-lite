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
    

class eventRecoilAnalyzer(Module):
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
        self.out.branch("leadneut_pt", "F")
        for rtype in ["truth","gen","met", "puppimet", "tkMetPVchs", "tkMetPVLoose"]:
            for var in ['recoil_pt','recoil_phi', 'recoil_sphericity', 'm','n',
                        'recoil_e1','recoil_e2', 
                        'mt',
                        'dphi2met','dphi2puppimet','dphi2ntnpv','dphi2centralntnpv','dphi2centralmetdbeta','dphi2leadch','dphi2leadneut']:
                self.out.branch("{0}_{1}".format(rtype,var), "F")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        """actions taken at the end of the file"""
        pass

    def initReaders(self,tree): # this function gets the pointers to Value and ArrayReaders and sets them in the C++ worker class                                 
        self.nGenPart = tree.valueReader("nGenPart")
        for var in ["pt","eta","phi","mass","pdgId","status"] : 
            setattr(self,"GenPart_"+var, tree.arrayReader("GenPart_"+var))
        self._ttreereaderversion = tree._ttreereaderversion

    def getMCTruth(self,event):
        """computes the MC truth for this event"""

        #nothing to do for data :)
        if event.isData : return None,None,None

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
        visibleV,V=None,None
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

    def getRecoRecoil(self,event,met,visibleV):
        """computes the MC truth for this event"""

        #MET
        metP4=met.p4()

        #charged recoil estimators
        ht=met.sumEt
        h=ROOT.TVector3(-metP4.Px(),-metP4.Py(),0.)
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
        self.out.fillBranch('leadch_pt',   event.leadCharged_pt)
        self.out.fillBranch('leadneut_pt', event.leadNeutral_pt)

        #met estimators
        met               = Object(event,"met")
        puppimet          = Object(event,"puppimet")
        ntmet             = Object(event,"ntMet")
        ntCentralmet      = Object(event,"ntCentralMet")
        tkmet             = Object(event,"tkMetPVLoose")
        npvmet            = Object(event,"tkMetPUPVLoose")
        ntnpv             = ntmet.p4()+npvmet.p4()
        centralntnpv      = ntCentralmet.p4()+npvmet.p4()
        centralmetdbeta = tkmet.p4()+ntCentralmet.p4()-npvmet.p4()*0.5

        #recoil estimators
        for metType in ["truth","gen", "met","puppimet", "tkMetPVchs", "tkMetPVLoose"]:

            imet=None
            if metType=="truth":
                vis,h,ht=gen_visibleV.VectorT(),ROOT.TVector3(-gen_V.Px(),-gen_V.Py(),0),gen_V.Pt()
            elif metType=='gen':
                vis,h,ht=gen_visibleV.VectorT(),gen_h,gen_ht            
            else:
                imet=Object(event,metType)
                vis=visibleV.VectorT()
                h,ht,m=self.getRecoRecoil(event=event,met=imet,visibleV=visibleV)

            pt=h.Pt()
            phi=h.Phi()
            m=imet.p4().M() if imet else 0
            metphi=imet.p4().Phi() if imet else -99
            sphericity=pt/ht if ht>0 else -1   
            count=0
            try:
                count = getattr(event,'%s_Count'%metType)
            except:
                pass
            e1=gen_V.Pt()/h.Pt()
            e2=deltaPhi(gen_V.Phi()+np.pi,h.Phi())
            mt=np.sqrt( 2*vis.Pt()*((vis+h).Pt())+vis.Pt()**2+vis.Dot(h) )

            self.out.fillBranch('%s_recoil_pt'%metType,            pt)
            self.out.fillBranch('%s_recoil_phi'%metType,           phi)
            self.out.fillBranch('%s_m'%metType,                    m)
            self.out.fillBranch('%s_recoil_sphericity'%metType,    sphericity)
            self.out.fillBranch('%s_n'%metType,                    count)
            self.out.fillBranch('%s_recoil_e1'%metType,            e1)
            self.out.fillBranch('%s_recoil_e2'%metType,            e2)
            self.out.fillBranch('%s_mt'%metType,                   mt)
            self.out.fillBranch('%s_dphi2met'%metType,             deltaPhi(met.p4().Phi(),metphi) )
            self.out.fillBranch('%s_dphi2puppimet'%metType,        deltaPhi(puppimet.p4().Phi(),metphi) )
            self.out.fillBranch('%s_dphi2ntnpv'%metType,           deltaPhi(ntnpv.Phi(),metphi) )
            self.out.fillBranch('%s_dphi2centralntnpv'%metType,    deltaPhi(centralntnpv.Phi(),metphi) )
            self.out.fillBranch('%s_dphi2centralmetdbeta'%metType, deltaPhi(centralmetdbeta.Phi(),metphi) )
            self.out.fillBranch('%s_dphi2leadch'%metType,          deltaPhi(event.leadCharged_phi,metphi) )
            self.out.fillBranch('%s_dphi2leadneut'%metType,        deltaPhi(event.leadNeutral_phi,metphi) )

        return True
