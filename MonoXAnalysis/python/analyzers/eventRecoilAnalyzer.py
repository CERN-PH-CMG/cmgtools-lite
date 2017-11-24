from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from CMGTools.RootTools.fwlite.AutoHandle import AutoHandle
from PhysicsTools.HeppyCore.utils.deltar import deltaR,deltaPhi

import operator
import itertools
import copy
from math import *
import ROOT
import os 
 
class eventRecoilAnalyzer(Analyzer):
    '''
    Analyzes the event recoil and derives the corrections in pt and phi to bring the estimators to the true vector boson recoil.
    Loop on PF candidates, skipping selected leptons and storing useful variables.
    Based on the original code by N. Foppiani and O. Cerri (Pisa)
    '''

    def __init__(self, cfg_ana, cfg_comp, looperName ):
        super(eventRecoilAnalyzer,self).__init__(cfg_ana,cfg_comp,looperName)

    def declareHandles(self):
        super(eventRecoilAnalyzer, self).declareHandles()
        self.handles['pfcands'] = AutoHandle( self.cfg_ana.candidates, self.cfg_ana.candidatesTypes )

    def beginLoop(self, setup):
        super(eventRecoilAnalyzer,self).beginLoop(setup) 

    def getMCtruth(self,event):
        """loops over a gen level collection and returns the first V"""
        try:
            genColl=getattr(event,self.cfg_ana.mcTruth)
            for p in genColl:
                pid=abs(p.pdgId())
                if pid!=24 and pid!=23: continue
                if abs(p.eta())>6: continue
                return p
        except:
            pass
        return None
 
    def process(self, event):
 
        self.readCollections( event.input)

        #primary vertex
        if len(event.vertices)==0 : return
        vertex=event.vertices[0]

        #mc truth
        genBoson=self.getMCtruth(event)

        #possible recoil estimators
        LEP, CH_PU, CH_PV, CH_ALL, N_DBETA, N_ALL, N_DBETA_CENTRAL, N_CENTRAL, DBETA_CENTRAL, CENTRAL, DBETA_ALL, ALL = range(0,12)
                
        #lepton prefered direction
        sellepp4=[]
        lepsump4=ROOT.Math.LorentzVector(ROOT.Math.PxPyPzE4D('double'))(0,0,0,0)
        for i in xrange(0,len(event.selectedLeptons)):
            if i>self.cfg_ana.maxSelLeptons : break
            sellepp4.append( event.selectedLeptons[i].p4() )
            lepsump4+=sellepp4[-1]

        #build charged particle sums and identify leading particles
        leadChargedCand,leadNeutCand=None,None
        p4sums  = [ROOT.Math.LorentzVector(ROOT.Math.PxPyPzE4D('double'))(0,0,0,0) for i in xrange(0,ALL+1)]
        ptsums  = [0. for i in xrange(0,ALL+1)]        
        pcounts = [0. for i in xrange(0,ALL+1)]
        pfcands = self.handles['pfcands'].product()
        for particle in pfcands:

            charge = particle.charge()
            eta    = particle.eta()

            #charged
            if charge!=0:

                #association to PV
                pvflag = particle.fromPV()

                #clean up wrt to selected leptons
                veto=False
                for l in sellepp4:
                    if deltaR(l,particle.p4())>0.05: continue
                    veto=True
                    break
                if veto: continue

                p4sums[CH_ALL]  += particle.p4()
                ptsums[CH_ALL]  += particle.pt()
                pcounts[CH_ALL] += 1

                if abs(eta)<self.cfg_ana.centralEta:
                    if pvflag>self.cfg_ana.pvAssoc:
                        p4sums[CH_PV]  += particle.p4()
                        ptsums[CH_PV]  += particle.pt()
                        pcounts[CH_PV] += 1

                        #update leading charged candidate in tracker acceptance region
                        if not leadChargedCand or leadChargedCand.pt()<particle.pt():
                            leadChargedCand = particle 
                    else:
                        p4sums[CH_PU]  += particle.p4()
                        ptsums[CH_PU]  += particle.pt()
                        pcounts[CH_PU] += 1

            #neutrals
            else:

                p4sums[N_ALL]  += particle.p4()
                ptsums[N_ALL]  += particle.pt()
                pcounts[N_ALL] += 1

                if abs(eta)<self.cfg_ana.centralEta:
                    p4sums[N_CENTRAL]  += particle.p4()
                    ptsums[N_CENTRAL]  += particle.pt()
                    pcounts[N_CENTRAL] += 1

                    #update leading neutral candidate in tracker acceptance region
                    if not leadNeutCand or leadNeutCand.pt()<particle.pt():
                        leadNeutCand = particle 

        #leptonic
        pcounts[LEP]=len(sellepp4)
        p4sums[LEP]=lepsump4
        ptsums[LEP]=sum([ l.pt() for l in sellepp4 ]) if pcounts[LEP]>0 else 0.
        
        #inclusive
        p4sums[ALL]      = p4sums[CH_ALL]+p4sums[N_ALL]
        ptsums[ALL]      = ptsums[CH_ALL]+ptsums[N_ALL]
        pcounts[ALL]     = pcounts[CH_ALL]+pcounts[N_ALL]

        #central
        p4sums[CENTRAL]  = p4sums[CH_PV]+p4sums[N_CENTRAL]
        ptsums[CENTRAL]  = ptsums[CH_PV]+ptsums[N_CENTRAL]
        pcounts[CENTRAL] = pcounts[CH_PV]+pcounts[N_CENTRAL]

        #delta-beta estimator inclusive
        dbeta=self.cfg_ana.dbeta
        p4sums[DBETA_ALL]      = p4sums[CH_ALL]+p4sums[N_ALL]+p4sums[CH_PU]*dbeta
        ptsums[DBETA_ALL]      = ptsums[CH_ALL]+ptsums[N_ALL]+dbeta*ptsums[CH_PU]
        pcounts[DBETA_ALL]     = pcounts[CH_ALL]+pcounts[N_ALL]+dbeta*pcounts[CH_PU]

        #delta-beta estimator central
        p4sums[DBETA_CENTRAL]  = p4sums[CH_PV]+p4sums[N_CENTRAL]+p4sums[CH_PU]*dbeta
        ptsums[DBETA_CENTRAL]  = ptsums[CH_PV]+ptsums[N_CENTRAL]+dbeta*ptsums[CH_PU]
        pcounts[DBETA_CENTRAL] = pcounts[CH_PV]+pcounts[N_CENTRAL]+dbeta*pcounts[CH_PU]

        #delta-beta estimator neutral inclusive
        dbeta=self.cfg_ana.dbeta
        p4sums[N_DBETA]      = p4sums[N_ALL]+p4sums[CH_PU]*dbeta
        ptsums[N_DBETA]      = ptsums[N_ALL]+dbeta*ptsums[CH_PU]
        pcounts[N_DBETA]     = pcounts[N_ALL]+dbeta*pcounts[CH_PU]

        #delta-beta estimator neutral central
        p4sums[N_DBETA_CENTRAL]  = p4sums[N_CENTRAL]+p4sums[CH_PU]*dbeta
        ptsums[N_DBETA_CENTRAL]  = ptsums[N_CENTRAL]+dbeta*ptsums[CH_PU]
        pcounts[N_DBETA_CENTRAL] = pcounts[N_CENTRAL]+dbeta*pcounts[CH_PU]

        #dump info to event
        setattr(event,'leading_particle_tk_p4',leadChargedCand)
        setattr(event,'leading_particle_nt_p4',leadNeutCand)
        for idx,tag in [ (LEP,             'lep'), 
                         (CH_PV,           'chs'),
                         (ALL,             'inclusive'),
                         (CENTRAL,         'central'),
                         (DBETA_ALL,       'dbeta_inclusive'),
                         (DBETA_CENTRAL,   'dbeta_central'),
                         (N_DBETA,         'neutral_dbeta_inclusive'),
                         (N_DBETA_CENTRAL, 'neutral_dbeta_central')]:
            addTrueVal=False if ptsums[idx]==0 else True
            setattr(event,tag+'_pt',p4sums[idx].pt() if addTrueVal else 0.)
            setattr(event,tag+'_m',p4sums[idx].mass() if addTrueVal else 0.)            
            setattr(event,tag+'_ht',ptsums[idx] if addTrueVal else 0.)
            setattr(event,tag+'_ptoverht',p4sums[idx].pt()/ptsums[idx] if addTrueVal else 0.)
            setattr(event,tag+'_np',pcounts[idx] if addTrueVal else 0.)
            setattr(event,tag+'_dphi2vtx',         deltaPhi(vertex.p4().phi(),          p4sums[idx].phi()) if addTrueVal else 0.)
            setattr(event,tag+'_dphi2leadcharged', deltaPhi(leadChargedCand.p4().phi(), p4sums[idx].phi()) if addTrueVal else 0.)
            setattr(event,tag+'_dphi2leadneut',    deltaPhi(leadNeutCand.p4().phi(),    p4sums[idx].phi()) if addTrueVal else 0.)
            setattr(event,tag+'_dphi2all',         deltaPhi(p4sums[ALL].phi(),          p4sums[idx].phi()) if addTrueVal else 0.)
            setattr(event,tag+'_dphi2lepsys',      deltaPhi(lepsump4.phi(),             p4sums[idx].phi()) if addTrueVal else 0.)

            #recoil corrections (if available)
            e1,e2=0.,0.
            if genBoson and ptsums[idx]>0:
                e1=genBoson.pt()/ptsums[idx]
                e2=deltaPhi(genBoson.phi(),p4sums[idx].phi())            
            setattr(event,tag+'_e1',e1 if addTrueVal else 0.)
            setattr(event,tag+'_e2',e2 if addTrueVal else 0.)


def getEventRecoilVariablesForTree():
    """ 
    declares variables of interest 
    in principle this could be simplified a lot with for loops and string replacement 
    but it looks like the variables get assigned the value of the last one declared
    """
    from PhysicsTools.Heppy.analyzers.core.autovars import NTupleVariable as ntv

    vList=[
        ntv('lep_pt',               lambda ev : getattr(ev,'lep_pt'),               float, help=''),
        ntv('lep_m',                lambda ev : getattr(ev,'lep_m'),                float, help=''),
        ntv('lep_ht',               lambda ev : getattr(ev,'lep_ht'),               float, help=''),
        ntv('lep_ptoverht',         lambda ev : getattr(ev,'lep_ptoverht'),         float, help=''),
        ntv('lep_dphi2vtx',         lambda ev : getattr(ev,'lep_dphi2vtx'),         float, help=''),
        ntv('lep_dphi2leadcharged', lambda ev : getattr(ev,'lep_dphi2leadcharged'), float, help=''),
        ntv('lep_dphi2leadneut',    lambda ev : getattr(ev,'lep_dphi2leadneut'),    float, help=''),
        ntv('lep_dphi2all',         lambda ev : getattr(ev,'lep_dphi2all'),         float, help=''),
        ntv('lep_dphi2lepsys',      lambda ev : getattr(ev,'lep_dphi2lepsys'),      float, help=''),
        ntv('lep_e1',               lambda ev : getattr(ev,'lep_e1'),               float, help=''),
        ntv('lep_e2',               lambda ev : getattr(ev,'lep_e2'),               float, help=''),

        ntv('chs_pt',               lambda ev : getattr(ev,'chs_pt'),               float, help=''),
        ntv('chs_m',                lambda ev : getattr(ev,'chs_m'),                float, help=''),
        ntv('chs_ht',               lambda ev : getattr(ev,'chs_ht'),               float, help=''),
        ntv('chs_ptoverht',         lambda ev : getattr(ev,'chs_ptoverht'),         float, help=''),
        ntv('chs_dphi2vtx',         lambda ev : getattr(ev,'chs_dphi2vtx'),         float, help=''),
        ntv('chs_dphi2leadcharged', lambda ev : getattr(ev,'chs_dphi2leadcharged'), float, help=''),
        ntv('chs_dphi2leadneut',    lambda ev : getattr(ev,'chs_dphi2leadneut'),    float, help=''),
        ntv('chs_dphi2all',         lambda ev : getattr(ev,'chs_dphi2all'),         float, help=''),
        ntv('chs_dphi2lepsys',      lambda ev : getattr(ev,'chs_dphi2lepsys'),      float, help=''),
        ntv('chs_e1',               lambda ev : getattr(ev,'chs_e1'),               float, help=''),
        ntv('chs_e2',               lambda ev : getattr(ev,'chs_e2'),               float, help=''),
     
        ntv('inclusive_pt',               lambda ev : getattr(ev,'inclusive_pt'),               float, help=''),
        ntv('inclusive_m',                lambda ev : getattr(ev,'inclusive_m'),                float, help=''),
        ntv('inclusive_ht',               lambda ev : getattr(ev,'inclusive_ht'),               float, help=''),
        ntv('inclusive_ptoverht',         lambda ev : getattr(ev,'inclusive_ptoverht'),         float, help=''),
        ntv('inclusive_dphi2vtx',         lambda ev : getattr(ev,'inclusive_dphi2vtx'),         float, help=''),
        ntv('inclusive_dphi2leadcharged', lambda ev : getattr(ev,'inclusive_dphi2leadcharged'), float, help=''),
        ntv('inclusive_dphi2leadneut',    lambda ev : getattr(ev,'inclusive_dphi2leadneut'),    float, help=''),
        ntv('inclusive_dphi2all',         lambda ev : getattr(ev,'inclusive_dphi2all'),         float, help=''),
        ntv('inclusive_dphi2lepsys',      lambda ev : getattr(ev,'inclusive_dphi2lepsys'),      float, help=''),
        ntv('inclusive_e1',               lambda ev : getattr(ev,'inclusive_e1'),               float, help=''),
        ntv('inclusive_e2',               lambda ev : getattr(ev,'inclusive_e2'),               float, help=''),

        ntv('central_pt',               lambda ev : getattr(ev,'central_pt'),               float, help=''),
        ntv('central_m',                lambda ev : getattr(ev,'central_m'),                float, help=''),
        ntv('central_ht',               lambda ev : getattr(ev,'central_ht'),               float, help=''),
        ntv('central_ptoverht',         lambda ev : getattr(ev,'central_ptoverht'),         float, help=''),
        ntv('central_dphi2vtx',         lambda ev : getattr(ev,'central_dphi2vtx'),         float, help=''),
        ntv('central_dphi2leadcharged', lambda ev : getattr(ev,'central_dphi2leadcharged'), float, help=''),
        ntv('central_dphi2leadneut',    lambda ev : getattr(ev,'central_dphi2leadneut'),    float, help=''),
        ntv('central_dphi2all',         lambda ev : getattr(ev,'central_dphi2all'),         float, help=''),
        ntv('central_dphi2lepsys',      lambda ev : getattr(ev,'central_dphi2lepsys'),      float, help=''),
        ntv('central_e1',               lambda ev : getattr(ev,'central_e1'),               float, help=''),
        ntv('central_e2',               lambda ev : getattr(ev,'central_e2'),               float, help=''),

        ntv('dbeta_inclusive_pt',               lambda ev : getattr(ev,'dbeta_inclusive_pt'),               float, help=''),
        ntv('dbeta_inclusive_m',                lambda ev : getattr(ev,'dbeta_inclusive_m'),                float, help=''),
        ntv('dbeta_inclusive_ht',               lambda ev : getattr(ev,'dbeta_inclusive_ht'),               float, help=''),
        ntv('dbeta_inclusive_ptoverht',         lambda ev : getattr(ev,'dbeta_inclusive_ptoverht'),         float, help=''),
        ntv('dbeta_inclusive_dphi2vtx',         lambda ev : getattr(ev,'dbeta_inclusive_dphi2vtx'),         float, help=''),
        ntv('dbeta_inclusive_dphi2leadcharged', lambda ev : getattr(ev,'dbeta_inclusive_dphi2leadcharged'), float, help=''),
        ntv('dbeta_inclusive_dphi2leadneut',    lambda ev : getattr(ev,'dbeta_inclusive_dphi2leadneut'),    float, help=''),
        ntv('dbeta_inclusive_dphi2all',         lambda ev : getattr(ev,'dbeta_inclusive_dphi2all'),         float, help=''),
        ntv('dbeta_inclusive_dphi2lepsys',      lambda ev : getattr(ev,'dbeta_inclusive_dphi2lepsys'),      float, help=''),
        ntv('dbeta_inclusive_e1',               lambda ev : getattr(ev,'dbeta_inclusive_e1'),               float, help=''),
        ntv('dbeta_inclusive_e2',               lambda ev : getattr(ev,'dbeta_inclusive_e2'),               float, help=''),

        ntv('dbeta_central_pt',               lambda ev : getattr(ev,'dbeta_central_pt'),               float, help=''),
        ntv('dbeta_central_m',                lambda ev : getattr(ev,'dbeta_central_m'),                float, help=''),
        ntv('dbeta_central_ht',               lambda ev : getattr(ev,'dbeta_central_ht'),               float, help=''),
        ntv('dbeta_central_ptoverht',         lambda ev : getattr(ev,'dbeta_central_ptoverht'),         float, help=''),
        ntv('dbeta_central_dphi2vtx',         lambda ev : getattr(ev,'dbeta_central_dphi2vtx'),         float, help=''),
        ntv('dbeta_central_dphi2leadcharged', lambda ev : getattr(ev,'dbeta_central_dphi2leadcharged'), float, help=''),
        ntv('dbeta_central_dphi2leadneut',    lambda ev : getattr(ev,'dbeta_central_dphi2leadneut'),    float, help=''),
        ntv('dbeta_central_dphi2all',         lambda ev : getattr(ev,'dbeta_central_dphi2all'),         float, help=''),
        ntv('dbeta_central_dphi2lepsys',      lambda ev : getattr(ev,'dbeta_central_dphi2lepsys'),      float, help=''),
        ntv('dbeta_central_e1',               lambda ev : getattr(ev,'dbeta_central_e1'),               float, help=''),
        ntv('dbeta_central_e2',               lambda ev : getattr(ev,'dbeta_central_e2'),               float, help=''),
        ]

    return vList
