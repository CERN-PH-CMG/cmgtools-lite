import ROOT
import os
import numpy as np
ROOT.PyConfig.IgnoreCommandLineOptions = True
from math import *

from CMGTools.MonoXAnalysis.postprocessing.framework.datamodel import Collection 
from CMGTools.MonoXAnalysis.postprocessing.framework.eventloop import Module
from PhysicsTools.HeppyCore.utils.deltar import deltaR,deltaPhi
 
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
        for rtype in ["met", "tkMetPVchs", "tkMetPVLoose", "tkMetPVTight"]:
            for var in ['pt','e1','e2']:
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

        #helper p4
        p4=ROOT.TLorentzVector(0,0,0,0)

        #dressed leptons 
        dressedLeps=[]
        ngenLep=self.out._branches["nGenLepDressed"].buff[0]
        for i in xrange(0,ngenLep):
            dressedLeps.append( ROOT.TLorentzVector(0,0,0,0) )
            dressedLeps[-1].SetPtEtaPhiM( self.out._branches["GenLepDressed_pt"].buff[i],
                                          self.out._branches["GenLepDressed_eta"].buff[i],
                                          self.out._branches["GenLepDressed_phi"].buff[i],
                                          self.out._branches["GenLepDressed_mass"].buff[i] )

        #neutrinos
        nus=[]
        ngenNu=self.out._branches["nGenPromptNu"].buff[0]
        for i in xrange(0,ngenNu):
            nus.append( ROOT.TLorentzVector(0,0,0,0) )
            nus[-1].SetPtEtaPhiM( self.out._branches["GenPromptNu_pt"].buff[i],
                                  self.out._branches["GenPromptNu_eta"].buff[i],
                                  self.out._branches["GenPromptNu_phi"].buff[i],
                                  self.out._branches["GenPromptNu_mass"].buff[i] )

        #recoil
        gen_h=ROOT.TLorentzVector(event.met_genPt,0,event.met_genPhi,0)
        if len(nus) and len(dressedLeps) :
            gen_h += nus[0]+dressedLeps[0]
        gen_h *= (-1)
        return dressedLeps,nus,gen_h
    

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        if event._tree._ttreereaderversion > self._ttreereaderversion:
            self.initReaders(event._tree)

        #MC truth
        dressedLeps,nus,gen_h=self.getMCTruth(event)
        gen_v=dressedLeps[0]+nus[0]

        #selected leptons
        lepColl = Collection(event, "LepGood")
        leps=[]
        for l in lepColl:
            leps.append( ROOT.TLorentzVector(0,0,0,0) )
            leps[-1].SetPtEtaPhiM( l.pt, l.eta, l.phi, l.mass )
        if len(leps)==0 : return False
        if leps[0].Pt() <20 or abs(leps[0].Eta())>2.4 : return False

        #met estimators
        for met in ["met", "tkMetPVchs", "tkMetPVLoose", "tkMetPVTight"]:
            metp4=ROOT.TLorentzVector(0,0,0,0)
            metp4.SetPtEtaPhiM(getattr(event,'%s_pt'%met),0,getattr(event,'%s_phi'%met),0)
            h=(metp4+leps[0])*(-1)

            pt=h.Pt()
            e1=gen_h.Pt()/h.Pt()
            e2=deltaPhi(gen_h.Phi(),h.Phi())

            self.out.fillBranch('%s_pt'%met,pt)
            self.out.fillBranch('%s_e1'%met,e1)
            self.out.fillBranch('%s_e2'%met,e2)
             
        return True

#    def getMCtruth(self,event):
#        """retrieves the true boson and recoil kinematics from the generator level particles"""
#
#        mcTruthColl=self.cfg_ana.mcTruth
#
#        #generated boson kinematics
#        genV=None
#        try:
#            genV=getattr(event,mcTruthColl['V'])[0].p4()
#        except: 
#            pass
#
#        #generated leptons kinematics
#        genLepSum=None        
#        try:
#            genLeps=[l.p4() for l in getattr(event,mcTruthColl['lep'])]
#            genLepSum=genLeps[0].p4()
#        except:
#            pass
#
#        #true recoil (final state particles excluding forward particles)
#        genRecoil=None
#        try:
#            genColl=getattr(event,mcTruthColl['particles'])
#            for p in genColl:
#                if p.status()!=1 : continue
#                if abs(p.eta())>4.7 : continue
#                #if abs(p.pdgId()) in [12,14,16]: continue
#                if genRecoil : genRecoil += p.p4()
#                else         : genRecoil  = p.p4()
#            genRecoil -= genLepSum
#        except:
#            pass
#
#        return genV,genRecoil
#
# 
#    def process(self, event):
# 
#        self.readCollections( event.input)
#
#        #primary vertex
#        if len(event.vertices)==0 : return
#        vertex=event.vertices[0]
#
#        #mc truth
#        genBoson,genRecoil=self.getMCtruth(event)
#
#        #possible recoil estimators
#        TRUTH, LEP, CH_PU, CH_PV, CH_ALL, N_DBETA, N_ALL, N_DBETA_CENTRAL, N_CENTRAL, DBETA_CENTRAL, CENTRAL, DBETA_ALL, ALL = range(0,13)
#                
#        #lepton prefered direction
#        sellepp4=[]
#        sellepid=[]
#        lepsump4=ROOT.Math.LorentzVector(ROOT.Math.PxPyPzE4D('double'))(0,0,0,0)
#        for i in xrange(0,len(event.selectedLeptons)):
#            if i>self.cfg_ana.maxSelLeptons : break
#            sellepid.append( event.selectedLeptons[i].pdgId() )
#            sellepp4.append( event.selectedLeptons[i].p4() )
#            lepsump4+=sellepp4[-1]
#
#        #build charged particle sums and identify leading particles
#        leadChargedCand,leadNeutCand=None,None
#        p4sums  = [ROOT.Math.LorentzVector(ROOT.Math.PxPyPzE4D('double'))(0,0,0,0) for i in xrange(0,ALL+1)]
#        ptsums  = [0. for i in xrange(0,ALL+1)]        
#        pcounts = [0. for i in xrange(0,ALL+1)]
#        pfcands = self.handles['pfcands'].product()
#        for particle in pfcands:
#
#            charge = particle.charge()
#            eta    = particle.eta()
#
#            #charged
#            if charge!=0:
#
#                #association to PV
#                pvflag = particle.fromPV()
#
#                #clean up wrt to selected leptons
#                veto=False
#                for il in xrange(0,len(sellepp4)):
#                    if particle.pdgId()!=sellepid[il] : continue
#                    if deltaR(sellepp4[il],particle.p4())>0.05: continue
#                    veto=True
#                    break
#                if veto: continue
#
#                p4sums[CH_ALL]  += particle.p4()
#                ptsums[CH_ALL]  += particle.pt()
#                pcounts[CH_ALL] += 1
#
#                if abs(eta)<self.cfg_ana.centralEta:
#                    if pvflag>self.cfg_ana.pvAssoc:
#                        p4sums[CH_PV]  += particle.p4()
#                        ptsums[CH_PV]  += particle.pt()
#                        pcounts[CH_PV] += 1
#
#                        #update leading charged candidate in tracker acceptance region
#                        if not leadChargedCand or leadChargedCand.pt()<particle.pt():
#                            leadChargedCand = particle 
#                    else:
#                        p4sums[CH_PU]  += particle.p4()
#                        ptsums[CH_PU]  += particle.pt()
#                        pcounts[CH_PU] += 1
#
#            #neutrals
#            else:
#
#                p4sums[N_ALL]  += particle.p4()
#                ptsums[N_ALL]  += particle.pt()
#                pcounts[N_ALL] += 1
#
#                if abs(eta)<self.cfg_ana.centralEta:
#                    p4sums[N_CENTRAL]  += particle.p4()
#                    ptsums[N_CENTRAL]  += particle.pt()
#                    pcounts[N_CENTRAL] += 1
#
#                    #update leading neutral candidate in tracker acceptance region
#                    if not leadNeutCand or leadNeutCand.pt()<particle.pt():
#                        leadNeutCand = particle 
#
#        #truth
#        pcounts[TRUTH]=1             if genRecoil else 0
#        p4sums[TRUTH]=genRecoil      if genRecoil else 0
#        ptsums[TRUTH]=genRecoil.pt() if genRecoil else 0
#
#        #leptonic
#        pcounts[LEP]=len(sellepp4)
#        p4sums[LEP]=lepsump4
#        ptsums[LEP]=sum([ l.pt() for l in sellepp4 ]) if pcounts[LEP]>0 else 0.
#        
#        #inclusive
#        p4sums[ALL]      = p4sums[CH_ALL]+p4sums[N_ALL]
#        ptsums[ALL]      = ptsums[CH_ALL]+ptsums[N_ALL]
#        pcounts[ALL]     = pcounts[CH_ALL]+pcounts[N_ALL]
#
#        #central
#        p4sums[CENTRAL]  = p4sums[CH_PV]+p4sums[N_CENTRAL]
#        ptsums[CENTRAL]  = ptsums[CH_PV]+ptsums[N_CENTRAL]
#        pcounts[CENTRAL] = pcounts[CH_PV]+pcounts[N_CENTRAL]
#
#        #delta-beta estimator inclusive
#        dbeta=self.cfg_ana.dbeta
#        p4sums[DBETA_ALL]      = p4sums[CH_ALL]+p4sums[N_ALL]+p4sums[CH_PU]*dbeta
#        ptsums[DBETA_ALL]      = ptsums[CH_ALL]+ptsums[N_ALL]+dbeta*ptsums[CH_PU]
#        pcounts[DBETA_ALL]     = pcounts[CH_ALL]+pcounts[N_ALL]+dbeta*pcounts[CH_PU]
#
#        #delta-beta estimator central
#        p4sums[DBETA_CENTRAL]  = p4sums[CH_PV]+p4sums[N_CENTRAL]+p4sums[CH_PU]*dbeta
#        ptsums[DBETA_CENTRAL]  = ptsums[CH_PV]+ptsums[N_CENTRAL]+dbeta*ptsums[CH_PU]
#        pcounts[DBETA_CENTRAL] = pcounts[CH_PV]+pcounts[N_CENTRAL]+dbeta*pcounts[CH_PU]
#
#        #delta-beta estimator neutral inclusive
#        dbeta=self.cfg_ana.dbeta
#        p4sums[N_DBETA]      = p4sums[N_ALL]+p4sums[CH_PU]*dbeta
#        ptsums[N_DBETA]      = ptsums[N_ALL]+dbeta*ptsums[CH_PU]
#        pcounts[N_DBETA]     = pcounts[N_ALL]+dbeta*pcounts[CH_PU]
#
#        #delta-beta estimator neutral central
#        p4sums[N_DBETA_CENTRAL]  = p4sums[N_CENTRAL]+p4sums[CH_PU]*dbeta
#        ptsums[N_DBETA_CENTRAL]  = ptsums[N_CENTRAL]+dbeta*ptsums[CH_PU]
#        pcounts[N_DBETA_CENTRAL] = pcounts[N_CENTRAL]+dbeta*pcounts[CH_PU]
#        
#        #invert the sign for the recoil
#        for i in xrange(0,len(p4sums)):
#            if i in [LEP,TRUTH] : continue
#            p4sums[i]=p4sums[i]*(-1)
#
#        #dump info to event
#        setattr(event,'leading_particle_tk_p4',leadChargedCand)
#        setattr(event,'leading_particle_nt_p4',leadNeutCand)
#        for idx,tag in [ (TRUTH,            'truth'),
#                         (LEP,             'lep'), 
#                         (CH_PV,           'chs'),
#                         (ALL,             'inclusive'),
#                         (CENTRAL,         'central'),
#                         (DBETA_ALL,       'dbeta_inclusive'),
#                         (DBETA_CENTRAL,   'dbeta_central'),
#                         (N_DBETA,         'neutral_dbeta_inclusive'),
#                         (N_DBETA_CENTRAL, 'neutral_dbeta_central')]:
#            addTrueVal=False if ptsums[idx]==0 else True
#            setattr(event,tag+'_pt',p4sums[idx].pt() if addTrueVal else 0.)
#            setattr(event,tag+'_phi',p4sums[idx].phi() if addTrueVal else 0.)
#            setattr(event,tag+'_m',p4sums[idx].mass() if addTrueVal else 0.)            
#            setattr(event,tag+'_ht',ptsums[idx] if addTrueVal else 0.)
#            setattr(event,tag+'_ptoverht',p4sums[idx].pt()/ptsums[idx] if addTrueVal else 0.)
#            setattr(event,tag+'_np',pcounts[idx] if addTrueVal else 0.)
#            setattr(event,tag+'_dphi2vtx',         deltaPhi(vertex.p4().phi(),          p4sums[idx].phi()) if addTrueVal else 0.)
#            setattr(event,tag+'_dphi2leadcharged', deltaPhi(leadChargedCand.p4().phi(), p4sums[idx].phi()) if addTrueVal else 0.)
#            setattr(event,tag+'_dphi2leadneut',    deltaPhi(leadNeutCand.p4().phi(),    p4sums[idx].phi()) if addTrueVal else 0.)
#            setattr(event,tag+'_dphi2all',         deltaPhi(p4sums[ALL].phi(),          p4sums[idx].phi()) if addTrueVal else 0.)
#            setattr(event,tag+'_dphi2lepsys',      deltaPhi(lepsump4.phi(),             p4sums[idx].phi()) if addTrueVal else 0.)
#
#            #recoil corrections (if available)
#            e1,e2=0.,0.
#            if genRecoil and p4sums[idx].pt()>0:
#                e1=genRecoil.pt()/p4sums[idx].pt()
#                e2=deltaPhi(genRecoil.phi(),p4sums[idx].phi())            
#            setattr(event,tag+'_e1',e1 if addTrueVal else 0.)
#            setattr(event,tag+'_e2',e2 if addTrueVal else 0.)
#
