from CMGTools.TTHAnalysis.treeReAnalyzer import *
from ROOT import TLorentzVector, TVector2, std, TRandom2
import ROOT
import time
import itertools
import PhysicsTools.Heppy.loadlibs
import array
import operator


def minValueForIdxList(values,idxlist):
    cleanedValueList = [val for i,val in enumerate(values) if i in idxlist]
    if len(cleanedValueList)>0: return min(cleanedValueList)
    else: return -999


class EventVars1L_bkgDilep:
    def __init__(self):
        self.branches = [ 
                          "DL_LepGoodOne_pt", 'DL_LepGoodOne_pdgId', "DL_l1l2ovMET", "DL_Vecl1l2ovMET", "DL_DPhil1l2",
                          ("nLostLepTreatments","I"),
                          ("DL_ST","F",10,"nLostLepTreatments"),
                          ("DL_HT","F",10,"nLostLepTreatments"),
                          ("DL_dPhiLepW","F",10,"nLostLepTreatments"),
                          ("DL_nJets30Clean","F",10,"nLostLepTreatments"),
                          ("nMaxStat","I"),
                          ("DLMS_ST","F",2,"nMaxStat"),
                          ("DLMS_HT","F",2,"nMaxStat"),
                          ("DLMS_dPhiLepW","F",2,"nMaxStat"),
                          ("DLMS_nJets30Clean","F",2,"nMaxStat")
 
                          ]


    def listBranches(self):
        return self.branches[:]

    def calcDLDictionary(self, base = {}, keepIdx=0, discardIdx=1):
        outputdict = {}
        outputdict["DL_dPhiLepW"]          = []
        outputdict["DL_ST"]                = []
        outputdict["DL_HT"]                = []
        outputdict["DL_nJets30Clean"]      = []


        Met2D = TVector2(self.metp4.Px(),self.metp4.Py())
        LepToDiscard2D = TVector2(self.tightLeps[discardIdx].p4().Px(), self.tightLeps[discardIdx].p4().Py())
        LepToKeep2D = TVector2(self.tightLeps[keepIdx].p4().Px(), self.tightLeps[keepIdx].p4().Py())

        Met2D_AddFull = Met2D + LepToDiscard2D
        Met2D_AddThird = Met2D + (1/3.*LepToDiscard2D)
        
        recoWp4 = LepToKeep2D + Met2D
        outputdict["DL_dPhiLepW"].append(LepToKeep2D.DeltaPhi(recoWp4)) # [0]: not adding leptons to MET
        outputdict["DL_ST"].append(LepToKeep2D.Mod() + Met2D.Mod())
        outputdict["DL_HT"].append(base['HT'])
        outputdict["DL_nJets30Clean"].append(base['nJets30Clean'])

        recoWp4_AddFull = LepToKeep2D + Met2D_AddFull
        outputdict["DL_dPhiLepW"].append(LepToKeep2D.DeltaPhi(recoWp4_AddFull))# [0]: adding lost lepton pt to met
        outputdict["DL_ST"].append(LepToKeep2D.Mod() + Met2D_AddFull.Mod())
        dlht = base['HT'] + (LepToDiscard2D.Mod() if LepToDiscard2D.Mod()>30. else 0.)
        outputdict["DL_HT"].append(dlht)
        dlnjet = base['nJets30Clean']+ (1 if LepToDiscard2D.Mod()>30. else 0)
        outputdict["DL_nJets30Clean"].append(dlnjet)

        recoWp4_AddThird = LepToKeep2D + Met2D_AddThird
        outputdict["DL_dPhiLepW"].append(LepToKeep2D.DeltaPhi(recoWp4_AddThird))# [2]: adding 1/3 of lepton ptto met 
        outputdict["DL_ST"].append(LepToKeep2D.Mod() + Met2D_AddThird.Mod())
        dlht = base['HT'] + (2/3.*LepToDiscard2D.Mod() if 2/3.*LepToDiscard2D.Mod()>30 else 0.)
        outputdict["DL_HT"].append(dlht)
        dlnjet = base['nJets30Clean']+ (1 if 2/3.*LepToDiscard2D.Mod()>30. else 0)
        outputdict["DL_nJets30Clean"].append(dlnjet)

#        print base['nJets30Clean'], outputdict["DL_nJets30Clean"]

        outputdict["l1l2ovMET"]    =  (self.tightLeps[0].pt + self.tightLeps[1].pt)/self.metp4.Pt()
        outputdict["Vecl1l2ovMET"] = (LepToKeep2D + LepToDiscard2D).Mod()/self.metp4.Pt()
        
        outputdict["DPhil1l2"]     = LepToKeep2D.DeltaPhi(LepToDiscard2D)


        return outputdict

    def __call__(self,event,base = {}):
#        print base['nJets30Clean']
        # prepare output
        ret = {}
        for name in self.branches:
            if type(name) == 'tuple':
                ret[name] = []
            elif type(name) == 'str':
                ret[name] = -999.0

#        if base['Selected']!=1: return ret #only run the full module on selected leptons, not the ones for QCD estimate
        # get some collections from initial tree
        leps = [l for l in Collection(event,"LepGood","nLepGood")]
        jets = [j for j in Collection(event,"Jet","nJet")]

        njet = len(jets); nlep = len(leps)

        # MET
        self.metp4 = ROOT.TLorentzVector(0,0,0,0)
        self.metp4.SetPtEtaPhiM(event.met_pt,event.met_eta,event.met_phi,event.met_mass)

        ####################################
        # import output from previous step #
        #base = keyvals
        ####################################

        # get selected leptons
        tightLeps = []
        tightLepsIdx = base['tightLepsIdx']
        tightLeps = [leps[idx] for idx in tightLepsIdx]
        nTightLeps = len(tightLeps)

        self.tightLeps = tightLeps
        # get selected jets
        centralJet30 = []
        centralJet30idx = base['Jets30Idx']
        centralJet30 = [jets[idx] for idx in centralJet30idx]
        nCentralJet30 = len(centralJet30)

        #print 'here',event.evt, nTightLeps, len(centralJet30), nBJetMedium30


        # deltaPhi between the (single) lepton and the reconstructed W (lep + MET)
        # ST of lepton and MET
        DL_ST = []
        DL_HT = []
        DL_dPhiLepW = []
        DL_nJets30Clean = []
        
        DLMS_ST = []
        DLMS_HT = []
        DLMS_dPhiLepW = []
        DLMS_nJets30Clean = []
        



        LepToKeep_pt = -999
        LepToKeep_pdgId = -999
        l1l2ovMET = -999
        Vecl1l2ovMET = -999

        DPhil1l2 = -999
        
        if len(tightLeps)==2:
            passPreSel = False
            SumP4 = tightLeps[0].p4()+tightLeps[1].p4()
            if tightLeps[0].charge!=tightLeps[1].charge: passPreSel= True
            if tightLeps[0].pdgId==-tightLeps[1].pdgId and abs(SumP4.M()-91.2)<10.: passPreSel= False
            
            if passPreSel:
                random = TRandom2(event.evt*event.lumi)
                uniform01 = random.Rndm()
                lepToKeep = int(uniform01>0.5)
                LepToKeep_pdgId = tightLeps[lepToKeep].pdgId
                LepToKeep_pt = tightLeps[lepToKeep].pt
                lepToDiscard = int(not lepToKeep)
                outdict = self.calcDLDictionary(base, keepIdx=lepToDiscard, discardIdx=lepToKeep)#reversed order to check both combinations and save them
                DLMS_ST           .append(outdict["DL_ST"      ][2])
                DLMS_HT           .append(outdict["DL_HT"      ][2])
                DLMS_dPhiLepW     .append(outdict["DL_dPhiLepW"][2])
                DLMS_nJets30Clean .append(outdict["DL_nJets30Clean"][2])
                
                outdict = self.calcDLDictionary(base, keepIdx=lepToKeep, discardIdx=lepToDiscard)
                DLMS_ST           .append(outdict["DL_ST"      ][2])
                DLMS_HT           .append(outdict["DL_HT"      ][2])
                DLMS_dPhiLepW     .append(outdict["DL_dPhiLepW"][2])
                DLMS_nJets30Clean .append(outdict["DL_nJets30Clean"][2])

                DL_ST = outdict["DL_ST"]
                DL_HT = outdict["DL_HT"]
                DL_dPhiLepW = outdict["DL_dPhiLepW"] 
                DL_nJets30Clean = outdict["DL_nJets30Clean"]
                
                l1l2ovMET   = outdict["l1l2ovMET"]    
                Vecl1l2ovMET= outdict["Vecl1l2ovMET"] 
                DPhil1l2    = outdict["DPhil1l2"]     


        ret["nLostLepTreatments"]=3
        if len(DL_ST)!=ret["nLostLepTreatments"]:
            for i in range(0,ret["nLostLepTreatments"]):
                DL_ST.append(-999)
                DL_HT.append(-999)
                DL_dPhiLepW.append(-999)
                DL_nJets30Clean.append(-999)

        ret["nMaxStat"]=2
        if len(DLMS_ST)!=ret["nMaxStat"]:
            for i in range(0,ret["nMaxStat"]):
                DLMS_ST           .append(-999)
                DLMS_HT           .append(-999)
                DLMS_dPhiLepW     .append(-999)
                DLMS_nJets30Clean .append(-999)
        
        ret["DL_ST"]    =DL_ST
        ret["DL_HT"]    =DL_HT
        ret["DL_dPhiLepW"] = DL_dPhiLepW
        ret["DL_nJets30Clean"]    =DL_nJets30Clean

        ret["DLMS_ST"      ] = DLMS_ST       
        ret["DLMS_HT"      ] = DLMS_HT       
        ret["DLMS_dPhiLepW"] = DLMS_dPhiLepW 
        ret["DLMS_nJets30Clean"      ] = DLMS_nJets30Clean


        ret['DL_LepGoodOne_pt'] = LepToKeep_pt
        ret['DL_LepGoodOne_pdgId'] = LepToKeep_pdgId
        ret['DL_l1l2ovMET'] = l1l2ovMET
        ret['DL_Vecl1l2ovMET'] = Vecl1l2ovMET
        ret['DL_DPhil1l2'] = DPhil1l2

#        print ret["DLMS_nJets30Clean"      ]
        return ret

if __name__ == '__main__':
    from sys import argv
    file = ROOT.TFile(argv[1])
    tree = file.Get("tree")
    class Tester(Module):
        def __init__(self, name):
            Module.__init__(self,name,None)
            self.sf = EventVars1L_bkgDilep()
        def analyze(self,ev):
            print "\nrun %6d lumi %4d event %d: leps %d" % (ev.run, ev.lumi, ev.evt, ev.nLepGood)
            print self.sf(ev,{})
    el = EventLoop([ Tester("tester") ])
    el.loop([tree], maxEvents = 50)
