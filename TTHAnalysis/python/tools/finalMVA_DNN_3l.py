from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection as NanoAODCollection 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection as Collection 

from CMGTools.TTHAnalysis.treeReAnalyzer import Collection as CMGCollection
from CMGTools.TTHAnalysis.tools.nanoAOD.friendVariableProducerTools import declareOutput, writeOutput
from CMGTools.TTHAnalysis.tools.tfTool import TFTool
import os 
from math import sqrt, cos, sin
from copy import deepcopy
import ROOT as r 



class finalMVA_DNN_3l(Module):
    def __init__(self, variations=[], doSystJEC=True):
        self.outVars = []
        self._MVAs   = []
        cats_3l =  ["predictions_ttH",  "predictions_rest", "predictions_tH"]
        varorder = ['lep1_conePt', 'lep1_eta', 'lep1_phi', 'lep2_conePt', 'lep2_eta', 'lep2_phi', 'lep3_conePt', 'lep3_eta', 'lep3_phi', 'mindr_lep1_jet', 'mindr_lep2_jet', 'mindr_lep3_jet', 'min_dr_Lep', 'avg_dr_jet', 'met_LD', 'mbb_loose',  'leadFwdJet_eta', 'leadFwdJet_pt', 'min_Deta_leadfwdJet_jet', 'jet1_pt', 'jet1_eta', 'jet1_phi', 'jet2_pt', 'jet2_eta', 'jet2_phi', 'jet3_pt', 'jet3_eta', 'jet3_phi', 'sum_Lep_charge', 'HadTop_pt', 'res_HTT', 'nJet',   'nBJetLoose', 'nBJetMedium', 'nJetForward', 'nElectron', 'has_SFOS' ]
        self.systsJEC = {0:"",\
                         1:"_jesTotalCorrUp"  , -1:"_jesTotalCorrDown",\
                         2:"_jesTotalUnCorrUp", -2: "_jesTotalUnCorrDown",\
                         3:"_jerUp", -3: "_jerDown",\
                     } if doSystJEC else {0:""}
        if len(variations): 
            self.systsJEC = {0:""}
            for i,var in enumerate(variations):
                self.systsJEC[i+1]   ="_%sUp"%var
                self.systsJEC[-(i+1)]="_%sDown"%var
                
        for var in self.systsJEC: 
            self._MVAs.append( TFTool('DNN_3l%s'%self.systsJEC[var], os.environ['CMSSW_BASE'] + '/src/CMGTools/TTHAnalysis/data/kinMVA/tth/test_sig_2_rest_2_th_2_withWZ_2.pb',
                                      self.getVarsForVariation(self.systsJEC[var]), cats_3l, varorder))

            self.outVars.extend( ['DNN_3l%s_'%self.systsJEC[var] + x for x in cats_3l])

        vars_3l_unclEnUp = deepcopy(self.getVarsForVariation(''))
        vars_3l_unclEnUp['met_LD'                 ] =  lambda ev : (ev.MET_pt_unclustEnUp if ev.year != 2017 else ev.METFixEE2017_pt_unclustEnUp) *0.6 + ev.mhtJet25_Recl*0.4

        vars_3l_unclEnDown = deepcopy(self.getVarsForVariation(''))
        vars_3l_unclEnDown['met_LD'                 ] =  lambda ev : (ev.MET_pt_unclustEnDown if ev.year != 2017 else ev.METFixEE2017_pt_unclustEnDown) *0.6 + ev.mhtJet25_Recl*0.4

        worker_3l_unclUp   = TFTool("DNN_3l_unclUp", os.environ['CMSSW_BASE'] + '/src/CMGTools/TTHAnalysis/data/kinMVA/tth/test_sig_2_rest_2_th_2_withWZ_2.pb', vars_3l_unclEnUp, cats_3l, varorder)
        worker_3l_unclDown = TFTool("DNN_3l_unclDown", os.environ['CMSSW_BASE'] + '/src/CMGTools/TTHAnalysis/data/kinMVA/tth/test_sig_2_rest_2_th_2_withWZ_2.pb', vars_3l_unclEnDown,cats_3l,  varorder)

        self._MVAs.extend( [ worker_3l_unclUp, worker_3l_unclDown])
        self.outVars.extend( ['DNN_3l_unclUp_' + x for x in cats_3l] +  ['DNN_3l_unclDown_' + x for x in cats_3l])


    def getVarsForVariation(self, var):
        return {'avg_dr_jet'             : lambda ev : getattr(ev,'avg_dr_jet%s'%var),
                'min_dr_Lep'             : lambda ev : min([ev.drlep12, ev.drlep13, ev.drlep23]),
                'jet1_pt'                : lambda ev : getattr(ev,'JetSel_Recl_pt%s'%var)[0] if getattr(ev,'nJet25%s_Recl'%var) > 0 else 0,
                'lep1_conePt'            : lambda ev : ev.LepGood_conePt[int(ev.iLepFO_Recl[0])], 
                'mindr_lep1_jet'         : lambda ev : getattr(ev,'mindr_lep1_jet%s'%var),
                'jet2_pt'                : lambda ev : getattr(ev,'JetSel_Recl_pt%s'%var)[1] if getattr(ev,'nJet25%s_Recl'%var) > 1 else 0,
                'leadFwdJet_pt'          : lambda ev : getattr(ev,'FwdJet1_pt%s_Recl'%var) if getattr(ev,'nFwdJet%s_Recl'%var) else 0,
                'lep3_conePt'            : lambda ev : ev.LepGood_conePt[int(ev.iLepFO_Recl[2])],
                'mindr_lep2_jet'         : lambda ev : getattr(ev,'mindr_lep2_jet%s'%var),                   
                'nBJetMedium'            : lambda ev : getattr(ev,'nBJetMedium25%s_Recl'%var),
                'mindr_lep3_jet'         : lambda ev : getattr(ev,'mindr_lep3_jet%s'%var), #### 
                'mbb_loose'              : lambda ev : getattr(ev,'mbb_loose%s'%var),
                'met_LD'                 : lambda ev : (getattr(ev,'MET_pt%s'%var) if ev.year != 2017 else getattr(ev,'METFixEE2017_pt%s'%var)) *0.6 + getattr(ev,'mhtJet25%s_Recl'%var)*0.4,
                'lep2_conePt'            : lambda ev : ev.LepGood_conePt[int(ev.iLepFO_Recl[1])],
                'jet1_eta'               : lambda ev : abs(ev.JetSel_Recl_eta[0]) if getattr(ev,'nJet25%s_Recl'%var) > 0 else 0,
                'jet3_pt'                : lambda ev : getattr(ev,'JetSel_Recl_pt%s'%var)[2] if getattr(ev,'nJet25%s_Recl'%var) > 2 else 0,
                'HadTop_pt'              : lambda ev : getattr(ev,'BDThttTT_eventReco_HadTop_pt%s'%var) if  getattr(ev,'BDThttTT_eventReco_mvaValue%s'%var) > 0 else 0,
                'has_SFOS'               : lambda ev : ev.hasOSSF3l,
                'sum_Lep_charge'         : lambda ev : (ev.LepGood_charge[int(ev.iLepFO_Recl[0])]+ev.LepGood_charge[int(ev.iLepFO_Recl[1])]+ev.LepGood_charge[int(ev.iLepFO_Recl[2])]) if ev.nLepFO_Recl >= 3 else 0,
                'nJet'                   : lambda ev : getattr(ev,'nJet25%s_Recl'%var),
                'lep3_eta'               : lambda ev : abs(ev.LepGood_eta[int(ev.iLepFO_Recl[2])]) if ev.nLepFO_Recl >= 3 else 0,
                'res_HTT'                : lambda ev : getattr(ev,'BDThttTT_eventReco_mvaValue%s'%var) if getattr(ev,'BDThttTT_eventReco_mvaValue%s'%var) > 0 else 0,
                'lep1_eta'               : lambda ev : abs(ev.LepGood_eta[int(ev.iLepFO_Recl[0])]) if ev.nLepFO_Recl >= 1 else 0,
                'lep2_eta'               : lambda ev : abs(ev.LepGood_eta[int(ev.iLepFO_Recl[1])]) if ev.nLepFO_Recl >= 2 else 0,
                'lep3_eta'               : lambda ev : abs(ev.LepGood_eta[int(ev.iLepFO_Recl[2])]) if ev.nLepFO_Recl >= 3 else 0,
                'min_Deta_leadfwdJet_jet': lambda ev : getattr(ev,'min_Deta_leadfwdJet_jet%s'%var),
                'jet2_phi'               : lambda ev : ev.JetSel_Recl_phi[1] if getattr(ev,'nJet25%s_Recl'%var) >= 2 else 0,
                'jet1_phi'               : lambda ev : ev.JetSel_Recl_phi[0] if getattr(ev,'nJet25%s_Recl'%var) >= 1 else 0,
                'lep3_phi'               : lambda ev : (ev.LepGood_phi[int(ev.iLepFO_Recl[2])]) if ev.nLepFO_Recl >= 3 else 0,
                'lep2_phi'               : lambda ev : (ev.LepGood_phi[int(ev.iLepFO_Recl[1])]) if ev.nLepFO_Recl >= 2 else 0,
                'leadFwdJet_eta'         : lambda ev : abs(getattr(ev,'FwdJet1_eta%s_Recl'%var)) if getattr(ev,'nFwdJet%s_Recl'%var) else 0,
                'jet3_eta'               : lambda ev : abs(ev.JetSel_Recl_eta[2]) if getattr(ev,'nJet25%s_Recl'%var) >= 3 else 0,
                'jet2_eta'               : lambda ev : abs(ev.JetSel_Recl_eta[1]) if getattr(ev,'nJet25%s_Recl'%var) >= 2 else 0,
                'nElectron'              : lambda ev : ((abs(ev.LepGood_pdgId[int(ev.iLepFO_Recl[0])]) == 11) + (abs(ev.LepGood_pdgId[int(ev.iLepFO_Recl[1])]) == 11) + (abs(ev.LepGood_pdgId[int(ev.iLepFO_Recl[2])]) == 11)) if ev.nLepFO_Recl >= 3 else 0,
                'lep1_phi'               : lambda ev : (ev.LepGood_phi[int(ev.iLepFO_Recl[0])]) if ev.nLepFO_Recl >= 1 else 0,
                'jet3_phi'               : lambda ev : ev.JetSel_Recl_phi[2] if getattr(ev,'nJet25%s_Recl'%var) >= 3 else 0,
                'nBJetLoose'             : lambda ev : getattr(ev,'nBJetLoose25%s_Recl'%var),
                'nJetForward'            : lambda ev : getattr(ev,'nFwdJet%s_Recl'%var),
            }



    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        print self.outVars
        declareOutput(self, wrappedOutputTree, self.outVars)
        
    def analyze(self,event):
        myvars = [event.iLepFO_Recl[0],event.iLepFO_Recl[1],event.iLepFO_Recl[2]]
        ret = []
        for worker in self._MVAs:
            name = worker.name
            if not hasattr(event,"nJet25_jerUp_Recl") and ('_jes' in name or  '_jer' in name or '_uncl' in name): continue # using jer bc components wont change
            ret.extend( [(x,y) for x,y in worker(event).iteritems()])
            

            
        writeOutput(self, dict(ret))
        return True
