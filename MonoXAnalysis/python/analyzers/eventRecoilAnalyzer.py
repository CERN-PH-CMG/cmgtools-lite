from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from CMGTools.RootTools.fwlite.AutoHandle import AutoHandle

import operator
import itertools
import copy
from math import *
import ROOT
import os 
 
class eventRecoilAnalyzer(Analyzer):
    '''
    Loop on PF candidates, skipping muons and storing useful variables.
 
    First declaring the auxiliar variables for tracks from primary vertex (tk), for neutral (nt).
    Secondly, loop on the candidates to compute the variables.
    Eventually, store the variables as attributes of the object event.
 
    event field needed:
        pf_candidates
        muons
        muon_W
 
    event field added:
        h_p4_tk
        sum_pt_tk
        N_tk
        h_eta_mean_tk
        leading_particle_tk_p4
        m_inv_tk
        leading12_pt_vector_sum_tk
        leading12_pt_scalar_sum_tk
        ratio_vec_scalar_tk
    '''

    def __init__(self, cfg_ana, cfg_comp, looperName ):
        super(eventRecoilAnalyzer,self).__init__(cfg_ana,cfg_comp,looperName)

    def declareHandles(self):
        super(eventRecoilAnalyzer, self).declareHandles()
        self.handles['pfcands'] = AutoHandle( self.cfg_ana.candidates, self.cfg_ana.candidatesTypes )

    def beginLoop(self, setup):
        super(eventRecoilAnalyzer,self).beginLoop(setup) 
 
    def process(self, event):
 
        self.readCollections( event.input)

        #possible recoil estimators
        CH_PU, CH_PV, CH_ALL, N_DBETA, N_ALL, N_DBETA_CENTRAL, N_CENTRAL, DBETA_CENTRAL, CENTRAL, DBETA_ALL, ALL = range(0,11)
        
        #lepton prefered direction
        sellepp4=[]
        lepsump4=ROOT.Math.LorentzVector(ROOT.Math.PxPyPzE4D('double'))(0,0,0,0)
        for i in xrange(0,len(event.selectedLeptons)):
            if i>self.cfg_ana.maxSelLeptons : break
            p4=event.selectedLeptons[i].p4()
            sellepp4.append(ROOT.Math.LorentzVector(ROOT.Math.PxPyPzE4D('double'))(p4.px(),p4.py(),p4.pz(),p4.e()))
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
                    print type(l),type(particle.p4())
                    if ROOT.Math.VectorUtil.DeltaR(l,particle.p4())>0.05: continue
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

        #primary vertex
        vertex=event.vertices[0]

        #dump info to event
        pfix=self.cfg_ana.collectionPostFix
        for idx,tag in [(CH_PV,           'chs'),
                        (ALL,'             inclusive'),
                        (CENTRAL,         'central'),
                        (DBETA_ALL,       'dbeta_inclusive'),
                        (DBETA_CENTRAL,   'dbeta_central'),
                        (N_DBETA,         'neutral_dbeta_inclusive'),
                        (N_DBETA_CENTRAL, 'neutral_dbeta_central')]:
            print idx,tag
            setattr(event,tag+'_pt'+pfix,p4sums[idx].pt())
            setattr(event,tag+'_m'+pfix,p4sums[idx].mass())            
            setattr(event,tag+'_ht'+pfix,ptsums[idx])
            pt_over_ht=-1 if ptsums[idx]==0 else p4sums[idx].pt()/ptsums[idx]
            setattr(event,tag+'_ptoverht'+pfix,pt_over_ht)
            setattr(event,tag+'_np'+pfix,pcounts[idx])
            setattr(event,tag+'_dphi2vtx'+pfix,         ROOT.Math.VectorUtil.DeltaPhi(vertex.p4(),          p4sums[idx]))
            setattr(event,tag+'_dphi2leadcharged'+pfix, ROOT.Math.VectorUtil.DeltaPhi(leadChargedCand.p4(), p4sums[idx]))
            setattr(event,tag+'_dphi2leadneut'+pfix,    ROOT.Math.VectorUtil.DeltaPhi(leadNeutCand.p4(),    p4sums[idx]))
            setattr(event,tag+'_dphi2all'+pfix,         ROOT.Math.VectorUtil.DeltaPhi(p4sums[ALL],          p4sums[idx]))
            setattr(event,tag+'_dphi2lepsys'+pfix,      ROOT.Math.VectorUtil.DeltaPhi(lepsump4,             p4sums[idx]))
            
        setattr(event,'leading_particle_tk_p4',leadChargedCand)
        setattr(event,'leading_particle_nt_p4',leadNeutCand)

