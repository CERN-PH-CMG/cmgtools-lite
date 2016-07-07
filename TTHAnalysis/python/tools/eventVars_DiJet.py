from CMGTools.TTHAnalysis.treeReAnalyzer import *
from ROOT import TLorentzVector, TVector2, std
import ROOT
import time
import itertools
import PhysicsTools.Heppy.loadlibs
import array
import operator


def getPhysObjectArray(j): # https://github.com/HephySusySW/Workspace/blob/72X-master/RA4Analysis/python/mt2w.py
    px = j.pt*cos(j.phi )
    py = j.pt*sin(j.phi )
    pz = j.pt*sinh(j.eta )
    E = sqrt(px*px+py*py+pz*pz) #assuming massless particles...
    return array.array('d', [E, px, py,pz])

class EventVarsDiJet:
    def __init__(self):
        self.branches = [ "deltaPhiMin","deltaPhi","mindr_lep_jet1", "mindr_lep_jet2","mindr_lep_jet3", "mindr_lep_jet4",
                           "MT_met_J1", "MT_met_J2","MT_met_J3","minMT","minMTJ2J3","MT",
                           "HTJet40" , "nJetC", "J1_QG","J2_QG","J3_QG",
                            "J1_Genb", "J2_Genb","J3_Genb",
                            "J1_Genc", "J2_Genc","J3_Genc",
                            "J1_bCSV", "J2_bCSV","J3_bCSV",
                            "J1_cCsvL", "J2_cCsvL","J3_cCsvL",
                            "J1_cCsvB", "J2_cCsvB","J3_cCsvB",
                            "J1_b","J2_b","J3_b", "nbtag",
                            "J1_bL","J2_bL","J3_bL", "nbtagL",
                            "J1_c","J2_c","J3_c", "nctag",
                            "J1_cL","J2_cL","J3_cL", "nctagL",
                            "J1_cT","J2_cT","J3_cT", "nctagT",
                            "J1_pT","J2_pT","J3_pT","J4_pT",
                            "J1_phi","J2_phi","J3_phi","J4_phi",
                            "J1_eta","J2_eta","J3_eta","J4_eta",
                           "MCT2b","MCTall","MCTJ1",
                           "L1_pT","L2_pT","L1_eta","L2_eta","L1_phi","L2_phi",
                            "L1_minRI", "L1_RI","L2_minRI", "L2_RI",
                           "mSbot","mLSP",
                           "L1_Id","L2_Id","L1_Ch","L2_Ch","L1_tightId","L2_tightId",
                           "L1gen_pT","L2gen_pT","L1gen_eta","L2gen_eta","L1gen_phi","L2gen_phi","L1gen_Id","L2gen_Id",
                           "mindr_lep1_gen", "mindr_lep2_gen", 
                           "PD_DoubleEl","PD_DoubleMu",          
                           "J1J2mass", "dPhiJ1J2MET","dPhiJ1J2J3","dPhiJ1MET"]


    def listBranches(self):
        return self.branches[:]
    def __call__(self,event,keyvals):
        # make python lists as Collection does not support indexing in slices
        #isMC =False
        isMC =True
        isSignal =False
        leps = [l for l in Collection(event,"lep","nlep",10)]
        if event.isData ==False: 
           genleps = [g for g in Collection(event,"genLep","ngenLep",10)] 
           ngenlep = len(genleps)
        jets = [j for j in Collection(event,"jet","njet",100)]
        (met, metphi)  = event.met_pt, event.met_phi
        metp4 = ROOT.TLorentzVector(0,0,0,0)   
        metp4.SetPtEtaPhiM(event.met_pt,event.met_eta,event.met_phi,event.met_mass) 
       # njet = len(jets);
        nlep = len(leps)
        ret = dict([(name,0.0) for name in self.branches])
        ret["PD_DoubleEl"] =1
        ret["PD_DoubleMu"] =0
       
        msbootom = -99.0
        mlsp = -99.0 
        if isSignal ==True:   
           msbootom =event.GenSusyMScan1 
           mlsp = event.GenSusyMScan2


        ret['mSbot'] = msbootom
        ret['mLSP'] = mlsp

        if nlep > 0:

           ret["L1_pT"] = leps[0].pt  
           ret["L1_minRI"] = leps[0].miniRelIso  
           ret["L1_RI"] = leps[0].relIso03  
           ret["L2_pT"] = leps[1].pt if nlep > 1 else -99
           ret["L2_minRI"] = leps[1].miniRelIso if nlep > 1 else -99
           ret["L2_RI"] = leps[1].relIso03 if nlep > 1 else -99
           ret["L1_eta"] = leps[0].eta 
           ret["L2_eta"] = leps[1].eta if nlep > 1 else -99
           ret["L1_phi"] = leps[0].phi 
           ret["L2_phi"] = leps[1].phi if nlep > 1 else -99
           ret["L1_Id"] = leps[0].pdgId 
           ret["L2_Id"] = leps[1].pdgId if nlep > 1 else -99
           ret["L1_Ch"] = leps[0].charge 
           ret["L2_Ch"] = leps[1].charge if nlep > 1 else -99
           ret["L1_tightId"] = leps[0].tightId 
           ret["L2_tightId"] = leps[1].tightId if nlep > 1 else -99
           if event.isData ==False: 
           #ret["mindr_lep1_gen"] = Minl1 
             if ngenlep > 0:
                minL1g = min([deltaR(g,leps[0]) for g in genleps]) if  nlep > 0 else 99
                minL2g = min([deltaR(g,leps[1]) for g in genleps]) if  nlep > 1 else 99
                glep1pt = -99                 
                glep2pt = -99                 
                glep1eta = -99                 
                glep2eta = -99                 
                glep1phi = -99                 
                glep2phi = -99                 


           
                ret["mindr_lep1_gen"] = deltaR(genleps[0],leps[0]) if  nlep > 0 else 99
                ret["mindr_lep2_gen"] = deltaR(genleps[1],leps[1]) if  nlep > 1 and ngenlep >1 else 99
                ret["L1gen_pT"] = genleps[0].pt 
                ret["L2gen_pT"] = genleps[1].pt if ngenlep > 1 else -99
                ret["L1gen_eta"] = genleps[0].eta  
                ret["L2gen_eta"] = genleps[1].eta if ngenlep > 1 else -99
                ret["L1gen_phi"] = genleps[0].phi 
                ret["L2gen_phi"] = genleps[1].phi if ngenlep > 1 else -99
         



        # prepare output
        centralJet40 = []
        centralJet40idx = []
        for i,j in enumerate(jets):
            if j.pt>40 :
                centralJet40.append(j)
                centralJet40idx.append(i)
                
        ret['HTJet40'] = sum([j.pt for j in jets if j.pt > 40])
	ret['nJetC'] = len(centralJet40)
        njet = len(centralJet40)
 
        if njet > 0:

           J1_bJet = 0
           J2_bJet = 0
           J3_bJet = 0
           J1_bJetL = 0
           J2_bJetL = 0
           J3_bJetL = 0
           J1_cJet = 0
           J2_cJet = 0
           J3_cJet = 0
           J1_cJetL = 0
           J2_cJetL = 0
           J3_cJetL = 0
           J1_cJetT = 0
           J2_cJetT = 0
           J3_cJetT = 0
           J1_Gb = 0
           J2_Gb = 0 
           J3_Gb = 0

           J1_Gc = 0
           J2_Gc = 0 
           J3_Gc = 0

           J2_btag = -99.
           J3_btag = -99.

           J2_ctagL = -99.
           J3_ctagL = -99.

           J2_ctagB = -99.
           J3_ctagB = -99.

           JC2_pT = -99.
           JC3_pT = -99.
           JC4_pT = -99.
        
           JC2_eta = -99.
           JC3_eta = -99.
           JC4_eta = -99.

           JC2_phi = -99.
           JC3_phi = -99.
           JC4_phi = -99.
           
        
           J3QG = -99.  
  
           JC1_pT=  jets[0].pt
           if njet >1 : JC2_pT=  jets[1].pt
           if njet >2 : JC3_pT=  jets[2].pt
           if njet >3 : JC4_pT=  jets[3].pt
           JC1_phi=  jets[0].phi
           if njet >1 : JC2_phi=  jets[1].phi
           if njet >2 : JC3_phi=  jets[2].phi
           if njet >3 : JC4_phi=  jets[3].phi
  
           JC1_eta=  jets[0].eta
           if njet >1 : JC2_eta=  jets[1].eta
           if njet >2 : JC3_eta=  jets[2].eta
           if njet >3 : JC4_eta=  jets[3].eta

           J1QG=  jets[0].qgl
           if njet >1 :  J2QG=  jets[1].qgl
           if njet >2 :  J3QG=  jets[2].qgl

            
           if event.isData == False:   
    
               if abs(jets[0].mcFlavour) ==5: J1_Gb = 1    
               if njet >1 and abs(jets[1].mcFlavour) ==5: J2_Gb = 1    
               if njet >2 and abs(jets[2].mcFlavour) ==5: J3_Gb = 1    
 
               if abs(jets[0].mcFlavour) ==4: J1_Gc = 1    
               if njet >1  and abs(jets[1].mcFlavour) ==4: J2_Gc = 1    
               if njet >2  and abs(jets[2].mcFlavour) ==4: J3_Gc = 1    

           J1_btag = jets[0].btagCSV
           #J1_ctagL = jets[0].ctagCsvL
           #J1_ctagB = jets[0].ctagCsvB
           if njet >1 : J2_btag = jets[1].btagCSV 
           if njet >2 : J3_btag = jets[2].btagCSV
           #if njet >1 : J2_ctagL = jets[1].ctagCsvL 
           #if njet >2 : J3_ctagL = jets[2].ctagCsvL
           #if njet >1 : J2_ctagB = jets[1].ctagCsvB 
           #if njet >2 : J3_ctagB = jets[2].ctagCsvB

           if jets[0].btagCSV>0.890: J1_bJet = 1    
           if njet >1 and  jets[1].btagCSV>0.890: J2_bJet = 1    
           if njet > 2 and jets[2].btagCSV>0.890: J3_bJet = 1    
           if jets[0].btagCSV>0.605: J1_bJetL = 1    
           if njet >1 and jets[1].btagCSV>0.605: J2_bJetL = 1    
           if njet > 2 and  jets[2].btagCSV>0.605: J3_bJetL = 1    
#        print "\nrun %6d lumi %4d event %d: btag %f" % (event.run, event.lumi, event.evt, jets[0].btagCSV)

           ret["mindr_lep_jet1"] = (deltaR(jets[0],leps[0])) if nlep >= 1 else -99
           ret["mindr_lep_jet2"] = (deltaR(jets[1],leps[0])) if nlep >= 1 and njet >1 else -99 
           ret["mindr_lep_jet3"] = (deltaR(jets[2],leps[0])) if nlep >= 1 and njet > 2 else -99 
           ret["mindr_lep_jet4"] = (deltaR(jets[3],leps[0])) if nlep >= 1 and njet > 3 else -99 
	   ret['J1_pT'] = JC1_pT
	   ret['J2_pT'] = JC2_pT
	   ret['J3_pT'] = JC3_pT
	   ret['J4_pT'] = JC4_pT
 
	   ret['J1_phi'] = JC1_phi
	   ret['J2_phi'] = JC2_phi
	   ret['J3_phi'] = JC3_phi
	   ret['J4_phi'] = JC4_phi

	   ret['J1_eta'] = JC1_eta
	   ret['J2_eta'] = JC2_eta
	   ret['J3_eta'] = JC3_eta
	   ret['J4_eta'] = JC4_eta

 	   ret['J1_b'] = J1_bJet
	   ret['J2_b'] = J2_bJet
	   ret['J3_b'] = J3_bJet
    
           ret['J1_bCSV'] = J1_btag
           ret['J2_bCSV'] = J2_btag
           ret['J3_bCSV'] = J3_btag

           #ret['J1_cCsvL'] = J1_ctagL
           #ret['J2_cCsvL'] = J2_ctagL
           #ret['J3_cCsvL'] = J3_ctagL

           #ret['J1_cCsvB'] = J1_ctagB
           #ret['J2_cCsvB'] = J2_ctagB
           #ret['J3_cCsvB'] = J3_ctagB

	   ret['J1_bL'] = J1_bJetL
	   ret['J2_bL'] = J2_bJetL
	   ret['J3_bL'] = J3_bJetL
	   ret['J1_Genb'] = J1_Gb
	   ret['J2_Genb'] = J2_Gb
	   ret['J3_Genb'] = J3_Gb
	   ret['J1_Genc'] = J1_Gc
	   ret['J2_Genc'] = J2_Gc
	   ret['J3_Genc'] = J3_Gc


        if njet > 1:
           MT_J3 = -999.
           deltaPhiMin_had3 = 999.
           bTagWP = 0.890
           MCT_2b = -99.0
           minMTall = -99.
           J1 = ROOT.TLorentzVector(0,0,0,0)
           MCT_J1 =-99.0
           J1J2 = ROOT.TLorentzVector(0,0,0,0)   
           J1J2M =-99.
           J2J3 = ROOT.TLorentzVector(0,0,0,0)   
           J2J3M =-99.
           MT_J1 =  sqrt( 2*jets[0].pt*met*(1-cos(jets[0].phi-metphi)) )
           MT_J2 =  sqrt( 2*jets[1].pt*met*(1-cos(jets[1].phi-metphi)) )
           MTJ1J2  = min(MT_J1,MT_J2)
           minMTall = min(MT_J1,MT_J2) 
           if njet > 2: 
              MT_J3 =  sqrt( 2*jets[2].pt*met*(1-cos(jets[2].phi-metphi)) )
              min2JMT =  min(MT_J1,MT_J2) 
              minMTall = min(min2JMT,MT_J3)
           MCT_all = sqrt( 2*jets[0].pt*jets[1].pt*(1+cos(jets[0].phi-jets[1].phi)) )  
           if jets[0].btagCSV > bTagWP and jets[1].btagCSV > bTagWP : 
              MCT_2b = sqrt( 2*jets[0].pt*jets[1].pt*(1+cos(jets[0].phi-jets[1].phi)) )  

           J1 = jets[0].p4()
           J1J2 = (jets[0].p4()+jets[1].p4())
           J1J2M = (jets[0].p4()+jets[1].p4()).M() 
           if njet>2: J2J3 = (jets[1].p4()+jets[2].p4())
           if njet>2: J2J3M = (jets[1].p4()+jets[2].p4()).M()
           if njet>2: MCT_J1 = sqrt( 2*jets[1].pt*jets[2].pt*(1+cos(jets[1].phi-jets[2].phi)) )  

           ret["MT_met_J1"] = MT_J1
           ret["MT_met_J2"] = MT_J2
           ret["MT_met_J3"] = MT_J3
           ret["minMT"] = minMTall
           ret["MT"] = MTJ1J2
           ret["minMTJ2J3"] = min(MT_J2,MT_J3)
           ret["deltaPhi"] = abs( deltaPhi( jets[0].phi, jets[1].phi ) )
           ret["MCT2b"] =MCT_2b
           ret["MCTall"] =MCT_all
           ret["MCTJ1"] =MCT_J1
           ret["J1J2mass"] =J1J2M
           ret["dPhiJ1J2MET"] =abs(metp4.DeltaPhi(J1J2) )
           ret["dPhiJ1J2J3"] =abs(J1.DeltaPhi(J2J3) )
           ret["dPhiJ1MET"] =abs(metp4.DeltaPhi(J1) )



           for n,j in enumerate(jets):
               if n>3:  break
               thisDeltaPhi = abs( deltaPhi( j.phi, metphi ) )
               if thisDeltaPhi < deltaPhiMin_had3 : deltaPhiMin_had3 = thisDeltaPhi



           ret["deltaPhiMin"] = deltaPhiMin_had3
                


        return ret

if __name__ == '__main__':
    from sys import argv
    file = ROOT.TFile(argv[1])
    tree = file.Get("tree")
    class Tester(Module):
        def __init__(self, name):
            Module.__init__(self,name,None)
            self.sf = EventVarsDiJet()
        def analyze(self,ev):
            print "\nrun %6d lumi %4d event %d: leps %d" % (ev.run, ev.lumi, ev.evt, ev.nlep)
            print self.sf(ev)
    el = EventLoop([ Tester("tester") ])
    el.loop([tree], maxEvents = 50)

