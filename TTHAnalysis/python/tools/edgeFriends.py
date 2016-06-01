## if MT2 doesnt work, put this line in the MT2 file: from ROOT.heppy import Davismt2

from CMGTools.TTHAnalysis.treeReAnalyzer import *
from CMGTools.TTHAnalysis.tools.eventVars_MT2 import *
print 'loading stuff for MT2'
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
ROOT.gSystem.Load("libFWCoreFWLite.so")
ROOT.gSystem.Load("libDataFormatsFWLite.so")
ROOT.AutoLibraryLoader.enable()
print 'done loading MT2 stuff.'

#ROOT.gSystem.Load('libCondFormatsBTagObjects') 
ROOT.gSystem.Load("pluginRecoBTagPerformanceDBplugins.so")

#ROOT.gROOT.ProcessLine('.L /afs/cern.ch/work/p/pablom/private/run/pruebaestupida/CMSSW_7_4_12/src/CMGTools/TTHAnalysis/python/tools/BTagCalibrationStandalone.cc+') 

import copy
import math
class edgeFriends:
    def __init__(self,label,tightLeptonSel,cleanJet):
        self.label = "" if (label in ["",None]) else ("_"+label)
        self.tightLeptonSel = tightLeptonSel
        self.cleanJet = cleanJet
        #self.isMC = isMC
        ## with nvtx self.puFile = open("/afs/cern.ch/work/m/mdunser/public/puWeighting/puWeightsVinceLumi1p28.txt","r")
        self.puFile = open("/afs/cern.ch/work/m/mdunser/public/puWeighting/puWeightsOfficialPrescription.txt","r")
        self.pu_dict = eval(self.puFile.read())
        self.puFile.close()
        ## filter things
        ## =================
        self.beamHaloListFile = open("/afs/cern.ch/user/p/pablom/public/Filters_27_01_2016/csc2015.txt", "r")
        self.fourthBadEESuperCrystalFile = open("/afs/cern.ch/user/p/pablom/public/Filters_27_01_2016/ecalscn1043093.txt","r")
        self.badResolutionTrackTaggerFile = open("/afs/cern.ch/user/p/pablom/public/Filters_27_01_2016/badResolutionTrack.txt","r")
        self.badMuonTrackTaggerFile = open("/afs/cern.ch/user/p/pablom/public/Filters_27_01_2016/muonBadTrack.txt","r")
        self.beamHaloSet = set()
        self.fourthBadEESuperCrystalSet = set()
        self.badResolutionTrackTaggerSet = set()
        self.badMuonTrackTaggerSet = set()
        for i in list(self.beamHaloListFile):
            self.beamHaloSet.add(i.rstrip('\n'))
        for i in list(self.fourthBadEESuperCrystalFile):
            self.fourthBadEESuperCrystalSet.add(i.rstrip('\n'))
        for i in list(self.badResolutionTrackTaggerFile):
            self.badResolutionTrackTaggerSet.add(i.rstrip('\n'))
        for i in list(self.badMuonTrackTaggerFile):
            self.badMuonTrackTaggerSet.add(i.rstrip('\n'))
        ##B-tagging stuff
        self.calib = ROOT.BTagCalibration("csvv2", "/afs/cern.ch/user/p/pablom/public/CSVv2.csv")
        self.reader_heavy    = ROOT.BTagCalibrationReader(self.calib, 1, "mujets", "central")
        self.reader_heavy_UP = ROOT.BTagCalibrationReader(self.calib, 1, "mujets", "up")
        self.reader_heavy_DN = ROOT.BTagCalibrationReader(self.calib, 1, "mujets", "down")
        self.reader_light    = ROOT.BTagCalibrationReader(self.calib, 1, "comb"  , "central")
        self.reader_light_UP = ROOT.BTagCalibrationReader(self.calib, 1, "comb"  , "up")
        self.reader_light_DN = ROOT.BTagCalibrationReader(self.calib, 1, "comb"  , "down")

        self.calibFASTSIM = ROOT.BTagCalibration("csvv2", "/afs/cern.ch/user/p/pablom/public/CSV_13TEV_Combined_20_11_2015.csv")
        self.reader_heavyFASTSIM    = ROOT.BTagCalibrationReader(self.calibFASTSIM, 1, "fastsim", "central")
        self.reader_heavy_UPFASTSIM = ROOT.BTagCalibrationReader(self.calibFASTSIM, 1, "fastsim", "up")
        self.reader_heavy_DNFASTSIM = ROOT.BTagCalibrationReader(self.calibFASTSIM, 1, "fastsim", "down")
        self.reader_lightFASTSIM    = ROOT.BTagCalibrationReader(self.calibFASTSIM, 1, "fastsim"  , "central")
        self.reader_light_UPFASTSIM = ROOT.BTagCalibrationReader(self.calibFASTSIM, 1, "fastsim"  , "up")
        self.reader_light_DNFASTSIM = ROOT.BTagCalibrationReader(self.calibFASTSIM, 1, "fastsim"  , "down")

        self.f_btag_eff      = ROOT.TFile("/afs/cern.ch/user/p/pablom/public/btageff__ttbar_powheg_pythia8_25ns.root")
        self.h_btag_eff_b    = copy.deepcopy(self.f_btag_eff.Get("h2_BTaggingEff_csv_med_Eff_b"   ))
        self.h_btag_eff_c    = copy.deepcopy(self.f_btag_eff.Get("h2_BTaggingEff_csv_med_Eff_c"   ))
        self.h_btag_eff_udsg = copy.deepcopy(self.f_btag_eff.Get("h2_BTaggingEff_csv_med_Eff_udsg"))
        self.f_btag_eff.Close()
        self.beamHaloListFile.close()
        self.fourthBadEESuperCrystalFile.close()
        self.badResolutionTrackTaggerFile.close()
        self.badMuonTrackTaggerFile.close()
        ## =================
        ## pdf things
        ## =================
        self.an_file = ROOT.TFile("/afs/cern.ch/work/m/mdunser/public/pdfsForLikelihood/pdfs_version23_savingTheWorkspace_may2016.root")
        self.wspace = copy.deepcopy( self.an_file.Get('w') )
        # data
        for t in ['DA','MC']:
            for var in [['mlb','sum_mlb_Edge'],['met','met_Edge'],['zpt','lepsZPt_Edge'],['ldr','lepsDR_Edge'],['a3d','d3D_Edge']]:
                print 'loading likelihoods for variable %s in %s'%(var[0],t)
                setattr(self,'h_lh_ana_%s_%s' %(var[0],t), self.wspace.pdf('%s_analyticalPDF_%s'%(var[0],t)))
                setattr(self,'var_ana_%s_%s'  %(var[0],t), self.wspace.var(var[1]))
                setattr(self,'frame_ana_%s_%s'%(var[0],t),getattr(self,'var_ana_%s_%s'%(var[0],t)).frame())
                getattr(self,'h_lh_ana_%s_%s' %(var[0],t)).plotOn(getattr(self,'frame_ana_%s_%s'%(var[0],t)))
                setattr(self,'obs_ana%s_%s'   %(var[0],t), ROOT.RooArgSet(self.wspace.var(var[1])))
        ## =================

        self.susymasslist = ['GenSusyMScan1'     , 'GenSusyMScan2'      , 'GenSusyMScan3'      , 'GenSusyMScan4'      ,
                             'GenSusyMGluino'    , 'GenSusyMGravitino'  , 'GenSusyMStop'       , 'GenSusyMSbottom'    ,
                             'GenSusyMStop2'     , 'GenSusyMSbottom2'   , 'GenSusyMSquark'     ,
                             'GenSusyMNeutralino', 'GenSusyMNeutralino2', 'GenSusyMNeutralino3', 'GenSusyMNeutralino4',
                             'GenSusyMChargino'  , 'GenSusyMChargino2']

        self.triggerlist = ['HLT_at51'      , 'HLT_at52'       , 'HLT_at53'       , 'HLT_at55'        , 'HLT_at57'     ,
                            'HLT_DoubleEl'  , 'HLT_el17el12_dz', 'HLT_el23el12_dz', 'HLT_ele33ele33'  ,
                            'HLT_DoubleMu'  , 'HLT_mu17mu8'    , 'HLT_mu17mu8_dz' , 'HLT_mu17tkmu8_dz', 'HLT_mu27tkmu8',
                            'HLT_MuEG'      , 'HLT_mu17el12'   , 'HLT_mu30ele30'  , 'HLT_mu8el17'     , 'HLT_mu8el23'  ,
                            'HLT_pfht200'   , 'HLT_pfht250'    , 'HLT_pfht300'    , 'HLT_pfht350'     , 'HLT_pfht400'  , 
                            'HLT_pfht475'   , 'HLT_pfht600'    , 'HLT_pfht800'    , 'HLT_pfht900'     ,
                            'HLT_DoubleElHT', 'HLT_DoubleMuHT' , 'HLT_MuEGHT'     , 
                            'HLT_HTJet'     , 'HLT_HTMET'      , 
                            'HLT_SingleEl'  , 'HLT_SingleMu']

    def listBranches(self):
        label = self.label
        biglist = [ ("evt"+label, "I"),
                    ("run"+label, "I"),
                    ("lumi"+label, "I"),
                    ("nVert"+label, "I"),
                    ("nLepTight"+label, "I"),
                    ("nJetSel"+label, "I"),
                    ("bestMjj"+label, "F"),
                    ("minMjj"+label, "F"),
                    ("maxMjj"+label, "F"),
                    ("hardMjj"+label, "F"),
                    ("hardJJDphi"+label, "F"),
                    ("hardJJDR"+label, "F"),
                    ("j1MetDPhi"+label, "F"),
                    ("j2MetDPhi"+label, "F"),
                    ("isLefthanded"+label, "I"),
                    ("isRighthanded"+label, "I"),
                    ("nPairLep"+label, "I"),
                    ("iLT"+label,"I",20,"nLepTight"+label), 
                    ("iJ"+label,"I",20,"nJetSel"+label), # index >= 0 if in Jet; -1-index (<0) if in DiscJet
                    ("nLepGood20"+label, "I"),
                    ("nLepGood20T"+label, "I"),
                    ("nJet35"+label, "I"), 
                    ("htJet35j"+label),
                    ("nBJetLoose25"+label, "I"),
                    ("nBJetLoose35"+label, "I"),
                    ("nBJetMedium25"+label, "I"), 
                    ("nBJetMedium35"+label, "I"), 
                    ("iL1T"+label, "I"),
                    ("iL2T"+label, "I"), 
                    ("lepsMll"+label, "F"),
                    ("lepsJZB"+label, "F"), 
                    ("lepsJZB_raw"+label, "F"),
                    ("lepsJZB_recoil"+label, "F"),
                    ("lepsDR"+label, "F"),
                    ("lepsMETRec"+label, "F"),
                    ("lepsZPt"+label, "F"),
                    ("metl1DPhi"+label, "F"),
                    ("metl2DPhi"+label, "F"),
                    ("met"+label, "F"),
                    ("met_phi"+label, "F"),
                    ("lepsDPhi"+label, "F"),
                    ("Lep1_pt"+label, "F"), 
                    ("Lep1_eta"+label, "F"), 
                    ("Lep1_phi"+label, "F"),
                    ("Lep1_miniRelIso"+label, "F"),
                    ("Lep1_pdgId"+label, "I"), 
                    ("Lep1_mvaIdSpring15"+label, "F"),
                    ("Lep1_minTauDR"+label, "F"),
                    ("Lep2_pt"+label, "F"), 
                    ("Lep2_eta"+label, "F"),
                    ("Lep2_phi"+label, "F"),
                    ("Lep2_miniRelIso"+label, "F"),
                    ("Lep2_pdgId"+label, "I"),
                    ("Lep2_mvaIdSpring15"+label, "F"),
                    ("Lep2_minTauDR"+label, "F"),
                    ("PileupW"+label, "F"), 
                    ("min_mlb1"+label, "F"),
                    ("min_mlb2"+label, "F"),
                    ("sum_mlb"+label, "F"), 
                    ("st"+label,"F"), 
                    ("srID"+label, "I"), 
                    ("mt2"+label, "F"),
                    ("lh_zpt_data"+label, "F"),
                    ("lh_a3d_data"+label, "F"),
                    ("lh_met_data"+label, "F"), 
                    ("lh_mlb_data"+label, "F"), 
                    ("lh_ldr_data"+label, "F"),
                    ("lh_zpt_mc"+label  , "F"),
                    ("lh_a3d_mc"+label  , "F"),
                    ("lh_met_mc"+label  , "F") , 
                    ("lh_mlb_mc"+label  , "F") , 
                    ("lh_ldr_mc"+label  , "F") ,
                    ("lh_ana_zpt_data"+label, "F") ,
                    ("lh_ana_a3d_data"+label, "F") ,
                    ("lh_ana_met_data"+label, "F") ,
                    ("lh_ana_mlb_data"+label, "F") , 
                    ("lh_ana_ldr_data"+label, "F") ,
                    ("lh_ana_zpt_mc"+label  , "F") , 
                    ("lh_ana_met_mc"+label  , "F") , 
                    ("lh_ana_mlb_mc"+label  , "F") , 
                    ("lh_ana_ldr_mc"+label  , "F") ,
                    ("lh_ana_a3d_mc"+label  , "F") ,
                    ("weight_btagsf"+label  , "F") ,
                    ("weight_btagsf_heavy_UP"+label, "F") ,
                    ("weight_btagsf_heavy_DN"+label, "F") ,
                    ("weight_btagsf_light_UP"+label, "F") ,
                    ("weight_btagsf_light_DN"+label, "F") ,
                    ("d3D" + label, "F"),
                    ("parPt" + label, "F"),
                    ("ortPt" + label, "F"),
                    ("dTheta" + label, "F"),
                    ('hbheFilterIso' +label, 'I'),
                    ('hbheFilterNew25ns' +label, 'I'),
                    ('Flag_eeBadScFilter' +label, 'I'),
                    ('genWeight' +label, 'F'),
                 ]
        for trig in self.triggerlist:
            biglist.append( ( '{tn}{lab}'.format(lab=label, tn=trig)) )
        for mass in self.susymasslist:
            biglist.append( ( '{tn}{lab}'.format(lab=label, tn=mass)) )
        ## for lfloat in 'pt eta phi miniRelIso pdgId'.split():
        ##     if lfloat == 'pdgId':
        ##         biglist.append( ("Lep"+label+"_"+lfloat,"I", 10, "nPairLep"+label) )
        ##     else:
        ##         biglist.append( ("Lep"+label+"_"+lfloat,"F", 10, "nPairLep"+label) )
        for jfloat in "pt eta phi mass btagCSV rawPt".split():
            biglist.append( ("JetSel"+label+"_"+jfloat,"F",20,"nJetSel"+label) )
        #if self.isMC:
        biglist.append( ("JetSel"+label+"_mcPt",     "F",20,"nJetSel"+label) )
        biglist.append( ("JetSel"+label+"_mcFlavour","I",20,"nJetSel"+label) )
        biglist.append( ("JetSel"+label+"_mcMatchId","I",20,"nJetSel"+label) )
        return biglist
    def __call__(self,event):
        leps  = [l for l in Collection(event,"LepGood","nLepGood")]
        lepso = [l for l in Collection(event,"LepOther","nLepOther")]
        jetsc = [j for j in Collection(event,"Jet","nJet")]
        jetsd = [j for j in Collection(event,"DiscJet","nDiscJet")]
        metco = [m for m in Collection(event,"metcJet","nDiscJet")]
        (met, metphi)  = event.met_pt, event.met_phi
        (met_raw, metphi_raw)  = event.met_rawPt, event.met_rawPhi
        if not event.isData:
            gentaus  = [t for t in Collection(event,"genTau","ngenTau")]
            ntrue = event.nTrueInt
        ## nvtx = event.nVert
        metp4 = ROOT.TLorentzVector()
        metp4.SetPtEtaPhiM(met,0,metphi,0)
        metp4_raw = ROOT.TLorentzVector()
        metp4_raw.SetPtEtaPhiM(met_raw,0,metphi_raw,0)
        ret = {}; jetret = {}; 
        lepret  = {}
        trigret = {}
        ret['met'] = met; ret['met_phi'] = metphi;
        ret['run'] = event.run
        ret['lumi'] = event.lumi
        ret['evt'] = event.evt
        ret['nVert'] = event.nVert
        
        ## copy the triggers, susy masses and filters!!
        for mass in self.susymasslist:
            ret[mass] = (-1 if not hasattr(event, mass) else getattr(event, mass) )
        for trig in self.triggerlist:
            trigret[trig] = (-1 if not hasattr(event, trig) else getattr(event, trig) )

        ## this will be slow
        ret['isLefthanded' ] = 0
        ret['isRighthanded'] = 0
        if not event.isData:
            genparts = [p for p in Collection(event,"GenPart","nGenPart")]
            for p in genparts:
                if p.status == 62:
                    if   abs(p.pdgId)-1000000 in [11, 13]: ret['isLefthanded' ] = 1
                    elif abs(p.pdgId)-2000000 in [11, 13]: ret['isRighthanded'] = 1
                    break

        ret['genWeight']          = ( 1. if not hasattr(event, 'genWeight'         ) else getattr(event, 'genWeight') )
        ret['hbheFilterIso'     ] = ( 1  if not hasattr(event, 'hbheFilterIso'     ) else int(getattr(event, 'hbheFilterIso'     )) )
        ret['hbheFilterNew25ns' ] = ( 1  if not hasattr(event, 'hbheFilterNew25ns' ) else int(getattr(event, 'hbheFilterNew25ns' )) )
        ret['Flag_eeBadScFilter'] = ( 1  if not hasattr(event, 'Flag_eeBadScFilter') else int(getattr(event, 'Flag_eeBadScFilter')) )

        #
        ### Define tight leptons
        ret["iLT"] = []; ret["nLepGood20T"] = 0

        # ====================
        # do pileupReweighting
        # ====================
        puWt = self.pu_dict[int(ntrue)] if not event.isData else 1.
        #if puWt > 10: puWt = 10.
        ret["PileupW"] = puWt

        # ===============================
        # new, simpler sorting of leptons
        # ===============================
        for il,lep in enumerate(leps):
            clean = True
            if self.tightLeptonSel(lep) and clean:
                ret["iLT"].append(il)
                if lep.pt > 20: ret["nLepGood20T"] += 1
        # other leptons, negative indices
        for il,lep in enumerate(lepso):
            clean = True
            if self.tightLeptonSel(lep) and clean:
                ret["iLT"].append(-1-il)
                if lep.pt > 20: ret["nLepGood20T"] += 1
        ret["nLepTight"] = len(ret["iLT"])
        #
        # sort the leptons by pT:
        ret["iLT"].sort(key = lambda idx : leps[idx].pt if idx >= 0 else lepso[-1-idx].pt, reverse = True)

        ## search for the lepton pair
        #lepst  = [ leps [il] for il in ret["iLT"] ]

        lepst = []
        for il in ret['iLT']:
            if il >=0: 
                lepst.append(leps[il])
            else: 
                lepst.append(lepso[-1-il])
        #
        iL1iL2 = self.getPairVariables(lepst, metp4, metp4_raw)
        ret['iL1T'] = ret["iLT"][ iL1iL2[0] ] if (len(ret["iLT"]) >=1 and iL1iL2[0] != -999) else -999
        ret['iL2T'] = ret["iLT"][ iL1iL2[1] ] if (len(ret["iLT"]) >=2 and iL1iL2[1] != -999) else -999
        ret['lepsMll'] = iL1iL2[2] 
        ret['lepsJZB'] = iL1iL2[3] 
        ret['lepsJZB_raw'] = iL1iL2[4] 
        ret['lepsDR'] = iL1iL2[5] 
        ret['lepsMETRec'] = iL1iL2[6] 
        ret['lepsZPt'] = iL1iL2[7] 
        ret['lepsDPhi'] = iL1iL2[8]
        ret['d3D']      = iL1iL2[9]
        ret['parPt']    = iL1iL2[10]
        ret['ortPt']    = iL1iL2[11]
        ret['dTheta']    = iL1iL2[12]

        #print 'new event =================================================='
        l1 = ROOT.TLorentzVector()
        l2 = ROOT.TLorentzVector()
        ltlvs = [l1, l2]
        lepvectors = []

        for lfloat in 'pt eta phi miniRelIso pdgId mvaIdSpring15'.split():
            if lfloat == 'pdgId':
                lepret["Lep1_"+lfloat+self.label] = -99
                lepret["Lep2_"+lfloat+self.label] = -99
            else:
                lepret["Lep1_"+lfloat+self.label] = -42.
                lepret["Lep2_"+lfloat+self.label] = -42.
        if ret['iL1T'] != -999 and ret['iL2T'] != -999:
            ret['nPairLep'] = 2
            # compute the variables for the two leptons in the pair
            lcount = 1
            for idx in [ret['iL1T'], ret['iL2T']]:
                lep = leps[idx] if idx >= 0 else lepso[-1-idx]
                minDRTau = 99.
                if not event.isData:
                    for tau in gentaus:
                        tmp_dr = deltaR(lep, tau)
                        if tmp_dr < minDRTau:
                            minDRTau = tmp_dr
                for lfloat in 'pt eta phi miniRelIso pdgId mvaIdSpring15'.split():
                    lepret["Lep"+str(lcount)+"_"+lfloat+self.label] = getattr(lep,lfloat)
                lepvectors.append(lep)
                lepret['metl'+str(lcount)+'DPhi'+self.label] = abs( deltaPhi( getattr(lep, 'phi'), metphi ))
                lepret["Lep"+str(lcount)+"_"+"minTauDR"+self.label] = minDRTau
                ltlvs[lcount-1].SetPtEtaPhiM(lep.pt, lep.eta, lep.phi, 0.0005 if lep.pdgId == 11 else 0.106)
                lcount += 1
                #print 'good lepton', getattr(lep,'pt'), getattr(lep,'eta'), getattr(lep,'phi'), getattr(lep,'pdgId') 
        else:
            ret['nPairLep'] = 0

        mt2 = -1.
        if ret['nPairLep'] == 2:
            l1mt2 = ROOT.reco.Particle.LorentzVector(lepvectors[0].p4().Px(), lepvectors[0].p4().Py(),lepvectors[0].p4().Pz(),lepvectors[0].p4().Energy())
            l2mt2 = ROOT.reco.Particle.LorentzVector(lepvectors[1].p4().Px(), lepvectors[1].p4().Py(),lepvectors[1].p4().Pz(),lepvectors[1].p4().Energy())
            metp4obj = ROOT.reco.Particle.LorentzVector(met*cos(metphi),met*sin(metphi),0,met)
            mt2 = computeMT2(l1mt2, l2mt2, metp4obj)
        ret['mt2'] = mt2
            
        ### Define jets
        ret["iJ"] = []
        # 0. mark each jet as clean
        for j in jetsc+jetsd: j._clean = True
        # set _clean flag of bad jets to False
        for j in jetsc+jetsd:
            if abs(j.eta) > 2.4 or j.pt < 35:
                j._clean = False
                continue
            for l in lepst:
                #lep = leps[l]
                if deltaR(l,j) < 0.4:
                    j._clean = False

        ## look for number of 25 GeV b-jets
        ret['nBJetLoose25' ] = 0
        ret['nBJetMedium25'] = 0
        for j in jetsc+jetsd:
            if abs(j.eta) < 2.4 and j.pt > 25. and j.btagCSV > 0.423:
                lepclear = True
                for l in lepst:
                    if deltaR(l,j) < 0.4: lepclear = False
                if lepclear: 
                    ret['nBJetLoose25'] += 1
                    if j.btagCSV > 0.890:
                        ret['nBJetMedium25'] += 1

        ## done looking for 25 GeV b-jets

        # 2. compute the jet list
        
        for ijc,j in enumerate(jetsc):
            if not j._clean: continue
            ret["iJ"].append(ijc)
        for ijd,j in enumerate(jetsd):
            if not j._clean: continue
            ret["iJ"].append(-1-ijd)
        ret['nJetSel'] = len(ret["iJ"])

        # 3. sort the jets by pt
        
        ret["iJ"].sort(key = lambda idx : jetsc[idx].pt if idx >= 0 else jetsd[-1-idx].pt, reverse = True)

        # 4. compute the variables
        
        for jfloat in "pt eta phi mass btagCSV rawPt".split():
            jetret[jfloat] = []
        if not event.isData:
            for jmc in "mcPt mcFlavour mcMatchId".split():
                jetret[jmc] = []
        for idx in ret["iJ"]:
            jet = jetsc[idx] if idx >= 0 else jetsd[-1-idx]
            for jfloat in "pt eta phi mass btagCSV rawPt".split():
                jetret[jfloat].append( getattr(jet,jfloat) )
            if not event.isData:
                for jmc in "mcPt mcFlavour mcMatchId".split():
                    jetret[jmc].append( getattr(jet,jmc) if not event.isData else -1.)
        
        # 5. compute the sums
        
        ret["nJet35"] = 0; ret["htJet35j"] = 0; ret["nBJetLoose35"] = 0; ret["nBJetMedium35"] = 0
        totalRecoil = ROOT.TLorentzVector()
        theJets = []
        for j in jetsc+jetsd:
            if not j._clean: continue
            theJets.append(j)
            ret["nJet35"] += 1; ret["htJet35j"] += j.pt; 
            if j.btagCSV>0.423: ret["nBJetLoose35"] += 1
            if j.btagCSV>0.890: ret["nBJetMedium35"] += 1
            jet = ROOT.TLorentzVector()
            jet.SetPtEtaPhiM(j.pt, j.eta, j.phi, j.mass)
            totalRecoil = totalRecoil + jet
          ## compute mlb for the two lepton  
        theJets = sorted(theJets, key = lambda j : j.pt, reverse = True)
        ret['lepsJZB_recoil'] = totalRecoil.Pt() - ret['lepsZPt']
        ret['bestMjj'] = self.getBestMjj(theJets)
        ret['minMjj']  = self.getMinMjj (theJets)
        ret['maxMjj']  = self.getMaxMjj (theJets)
        ret['hardMjj'] = self.getHardMjj(theJets)
        ret['hardJJDphi'] = self.getHardMjj(theJets, True)
        ret['hardJJDR'] = self.getHardMjj(theJets, True, True)
        ret['j1MetDPhi'] = deltaPhi(metphi, theJets[0].phi) if len(theJets) > 0 else -99.
        ret['j2MetDPhi'] = deltaPhi(metphi, theJets[1].phi) if len(theJets) > 1 else -99.
         
        [wtbtag, wtbtagUp_heavy, wtbtagUp_light, wtbtagDown_heavy, wtbtagDown_light] = (self.getWeightBtag(theJets) if not event.isData else [1., 1., 1., 1., 1.])

        ret['weight_btagsf'] = wtbtag
        ret['weight_btagsf_heavy_UP'] = wtbtagUp_heavy
        ret['weight_btagsf_heavy_DN'] = wtbtagDown_heavy
        ret['weight_btagsf_light_UP'] = wtbtagUp_light
        ret['weight_btagsf_light_DN'] = wtbtagDown_light
	
        jet = ROOT.TLorentzVector()
        min_mlb = 1e6
        max_mlb = 1e6
        _lind, _jind = -99, -99
        leplist = [l1, l2]
        # find the global minimum mlb (or mlj)
        jetIsB = False
        for lepton in leplist:
            if ret['nPairLep'] < 2: continue
            for j in jetsc+jetsd:
                if not j._clean: continue
                jet.SetPtEtaPhiM(j.pt, j.eta, j.phi, j.mass)           
                tmp = (lepton+jet).M()
                if j.btagCSV>0.814:   
                   if tmp < min_mlb: 
                         min_mlb  = tmp
                         jetisB = True 
                         _lind = leplist.index(lepton)
                         _jind = j
                else:
                     if tmp < min_mlb and jetIsB == False:
                         min_mlb = tmp
                         _lind = leplist.index(lepton)
                         _jind = j
        
        # compute the minimum mlb (or mlj) for the other lepton
        jetIsB = False
        for lepton in leplist: 
            if ret['nPairLep'] < 2: continue 
            for j in jetsc+jetsd: 
                if not j._clean: continue
                if j == _jind: continue
                jet.SetPtEtaPhiM(j.pt, j.eta, j.phi, j.mass)           
                tmp = ( (l1 if _lind == 1 else l2) +jet).M()
                if j.btagCSV>0.814:  
                    if tmp < max_mlb: 
                        max_mlb  = tmp
                        jetIsB = True
                else:
                    if tmp < max_mlb and jetIsB == False:
                        max_mlb = tmp   
        ret["min_mlb1"] = min_mlb if min_mlb < 1e6  else -1.
        ret["min_mlb2"] = max_mlb if max_mlb < 1e6  else -1.
        ret["sum_mlb"] = ret["min_mlb1"] + ret["min_mlb2"]
        ret["st"] = met+lepret["Lep1_pt"+self.label]+lepret["Lep2_pt"+self.label]

        ## beam halo filter list file:
        ## do this only for data
        if event.isData:
            evt_str = '%d:%d:%d'%(event.run, event.lumi, event.evt)
            if evt_str in self.beamHaloSet:
                ret['nPairLep'] = -1
            if evt_str in self.fourthBadEESuperCrystalSet:
                ret['nPairLep'] = -1
            if evt_str in self.badResolutionTrackTaggerSet:
                ret['nPairLep'] = -1
            if evt_str in self.badMuonTrackTaggerSet:
                ret['nPairLep'] = -1
        ## ====== done with beam halo and other filters check

        
        ## get the SR id which is 1xx for central and 2xx for forward. the 10 digit is the number of 
        ## b-tags and the signle digit is the mll region going from 1-5
        isBasicSREvent = (ret['nPairLep'] > 0 and ret["lepsDR"] > 0.1 and lepret["Lep1_pt"+self.label] > 20. and lepret["Lep2_pt"+self.label] > 20. and ret['lepsMll'] > 20.)
        isBasicSREvent = isBasicSREvent * (abs(lepret["Lep1_eta"+self.label] - 1.5) > 0.1 and abs(lepret["Lep2_eta"+self.label] - 1.5) > 0.1)
        isBasicSREvent = isBasicSREvent * (met > 150 and ret['nJetSel'] >= 2 ) ## adapting to 2016 selection
        if isBasicSREvent:
            srID = self.getSRID(ret['lepsMll'], lepret["Lep1_eta"+self.label], lepret["Lep2_eta"+self.label], ret["nBJetMedium35"])
            ret["srID"] = srID
            for t in  ['data','mc']:
                if t == 'data': nam = 'DA'
                else:           nam = 'MC'
                for u in ['_ana']:
                    for var in [['mlb',ret['sum_mlb'],'sum_mlb_Edge'],['met',met,'met_Edge'],
                                ['zpt',ret['lepsZPt'],'lepsZPt_Edge'],['ldr',ret['lepsDR'],'lepsDR_Edge'],
                                ['a3d',ret['d3D'],'d3D_Edge']]:
                        self.wspace.var(var[2]).setVal(var[1])
                        ret["lh%s_%s_%s"%(u,var[0],t)] = getattr(self,'h_lh_ana_%s_%s'%(var[0],nam)).getVal(getattr(self,'obs_ana%s_%s'%(var[0],nam)))
                    
                    if not ret["lh%s_mlb_%s"%(u,t)]: ret["lh%s_mlb_%s"%(u,t)] = 1e-50
                    if not ret["lh%s_ldr_%s"%(u,t)]: ret["lh%s_ldr_%s"%(u,t)] = 1e-50
                    if not ret["lh%s_met_%s"%(u,t)]: ret["lh%s_met_%s"%(u,t)] = 1e-50
                    if not ret["lh%s_zpt_%s"%(u,t)]: ret["lh%s_zpt_%s"%(u,t)] = 1e-50
                    if not ret["lh%s_a3d_%s"%(u,t)]: ret["lh%s_a3d_%s"%(u,t)] = 1e-50
                ## for u in ['']:
                ##     ret["lh%s_zpt_%s"%(u,t)] = getattr(self, 'h_lh%s_zpt_%s'%(u,t)).GetBinContent( getattr(self, 'h_lh%s_zpt_%s'%(u,t)).FindBin( ret["lepsZPt"]  ) ) 
                ##     ret["lh%s_met_%s"%(u,t)] = getattr(self, 'h_lh%s_met_%s'%(u,t)).GetBinContent( getattr(self, 'h_lh%s_met_%s'%(u,t)).FindBin( met             ) ) 
                ##     ret["lh%s_mlb_%s"%(u,t)] = getattr(self, 'h_lh%s_mlb_%s'%(u,t)).GetBinContent( getattr(self, 'h_lh%s_mlb_%s'%(u,t)).FindBin( ret["sum_mlb"]  ) ) 
                ##     ret["lh%s_ldr_%s"%(u,t)] = getattr(self, 'h_lh%s_ldr_%s'%(u,t)).GetBinContent( getattr(self, 'h_lh%s_ldr_%s'%(u,t)).FindBin( ret["lepsDR" ]  ) ) 
                ##     ret["lh%s_a3d_%s"%(u,t)] = getattr(self, 'h_lh%s_a3d_%s'%(u,t)).GetBinContent( getattr(self, 'h_lh%s_a3d_%s'%(u,t)).FindBin( ret['d3D'] )  )
                ##     if not ret["lh%s_mlb_%s"%(u,t)]: ret["lh%s_mlb_%s"%(u,t)] = 1e-50
                ##     if not ret["lh%s_ldr_%s"%(u,t)]: ret["lh%s_ldr_%s"%(u,t)] = 1e-50
                ##     if not ret["lh%s_met_%s"%(u,t)]: ret["lh%s_met_%s"%(u,t)] = 1e-50
                ##     if not ret["lh%s_zpt_%s"%(u,t)]: ret["lh%s_zpt_%s"%(u,t)] = 1e-50
                ##     if not ret["lh%s_a3d_%s"%(u,t)]: ret["lh%s_a3d_%s"%(u,t)] = 1e-50
        else:
            ret["srID"]      = -99
            for t in ['data', 'mc']:
                for u in ['_ana', '']:
                    ret["lh%s_mlb_%s"%(u,t)] = -999.
                    ret["lh%s_ldr_%s"%(u,t)] = -999.
                    ret["lh%s_met_%s"%(u,t)] = -999.
                    ret["lh%s_zpt_%s"%(u,t)] = -999.
                    ret["lh%s_a3d_%s"%(u,t)] = -999.

        
        fullret = {}
        for k,v in ret.iteritems(): 
            fullret[k+self.label] = v
        for k,v in jetret.iteritems(): 
            fullret["JetSel%s_%s" % (self.label,k)] = v
        #for k,v in lepret.iteritems(): 
        #    fullret["Lep%s_%s" % (self.label,k)] = v
        for k,v in lepret.iteritems(): 
            fullret[k] = v
        for k,v in trigret.iteritems(): 
            fullret[k+self.label] = v
        return fullret

    def getMll_JZB(self, l1, l2, met, met_raw):
        metrecoil = (met + l1 + l2).Pt()
        metrawrecoil = (met_raw + l1 + l2).Pt() 
        zpt = (l1 + l2).Pt()
        jzb = metrecoil - zpt
        jzb_raw = metrawrecoil - zpt
        v1 = l1.Vect()
        v2 = l2.Vect()
        return ((l1+l2).M(), jzb, jzb_raw, l1.DeltaR(l2), metrecoil, zpt, abs( deltaPhi( l1.Phi(), l2.Phi() )) , v1.Angle(v2))
    def getParOrtPt(self, l1, l2):
        if l1.Pt() > l2.Pt():
            v1 = l1.Vect()
            v2 = l2.Vect()
        else:
            v1 = l2.Vect()
            v2 = l1.Vect()
        u1 = v1.Unit()                              # direction of the harder lepton
        p1 = math.cos(v1.Angle(v2)) * v2.Mag() * u1 # projection of the softer lepton onto the harder
        o1 = v1 - p1                                # orthogonal to the projection of the softer onto the harder
        return  (p1.Perp(), o1.Perp())

    def getPairVariables(self,lepst, metp4, metp4_raw):
        ret = (-999,-999,-99., -9000., -9000, -99., -99., -99., -99.,-99.,-99.,-99.,-99.,-99.)
        if len(lepst) >= 2:
            [mll, jzb, jzb_raw, dr, metrec, zpt, dphi, d3D] = self.getMll_JZB(lepst[0].p4(), lepst[1].p4(), metp4, metp4_raw)
            [parPt, ortPt] = self.getParOrtPt(lepst[0].p4(),lepst[1].p4())
            ret = (0, 1, mll, jzb, jzb_raw, dr, metrec, zpt, dphi, d3D, parPt, ortPt, lepst[0].p4().Theta() - lepst[1].p4().Theta())
        return ret

    def getSRID(self, mll, eta1, eta2, nb):
        mllid, bid, etaid = -1, -1, -1
        if    20. < mll <  70.:
            mllid = 1
        elif  70. < mll <  81.:
            mllid = 2
        elif  81. < mll < 101.:
            mllid = 3
        elif 101. < mll < 120.:
            mllid = 4
        elif 120. < mll:
            mllid = 5
            
        if abs(eta1) < 1.4 and abs(eta2) < 1.4:
            etaid = 1
        else:
            etaid = 2

        return (100*etaid + 10*nb + mllid)

    def getBestMjj(self, jetsel):
        if len(jetsel) < 2: return -99.
        bestmjj = 1e6
        for jeti in jetsel:
            for jetj in jetsel:
                if jeti == jetj: continue
                jet1 = ROOT.TLorentzVector()
                jet1.SetPtEtaPhiM(jeti.pt, jeti.eta, jeti.phi, jeti.mass)
                jet2 = ROOT.TLorentzVector()
                jet2.SetPtEtaPhiM(jetj.pt, jetj.eta, jetj.phi, jetj.mass)
                dijetmass = (jet1+jet2).M()
                if abs(dijetmass - 80.385) < abs(bestmjj - 80.385):
                    bestmjj = dijetmass
        return bestmjj
    def getMinMjj(self, jetsel):
        if len(jetsel) < 2: return -99.
        minmjj = 1e6
        for jeti in jetsel:
            for jetj in jetsel:
                if jeti == jetj: continue
                jet1 = ROOT.TLorentzVector()
                jet1.SetPtEtaPhiM(jeti.pt, jeti.eta, jeti.phi, jeti.mass)
                jet2 = ROOT.TLorentzVector()
                jet2.SetPtEtaPhiM(jetj.pt, jetj.eta, jetj.phi, jetj.mass)
                dijetmass = (jet1+jet2).M()
                if dijetmass < minmjj:
                    minmjj = dijetmass
        return minmjj
    def getMaxMjj(self, jetsel):
        if len(jetsel) < 2: return -99.
        maxmjj = -99.
        for jeti in jetsel:
            for jetj in jetsel:
                if jeti == jetj: continue
                jet1 = ROOT.TLorentzVector()
                jet1.SetPtEtaPhiM(jeti.pt, jeti.eta, jeti.phi, jeti.mass)
                jet2 = ROOT.TLorentzVector()
                jet2.SetPtEtaPhiM(jetj.pt, jetj.eta, jetj.phi, jetj.mass)
                dijetmass = (jet1+jet2).M()
                if dijetmass > maxmjj:
                    maxmjj = dijetmass
        return maxmjj
    def getHardMjj(self, jetsel, _dphi = False, _dr = False):
        if len(jetsel) < 2: return -99.
        if not _dphi:
            jet1 = ROOT.TLorentzVector()
            jet2 = ROOT.TLorentzVector()
            jet1.SetPtEtaPhiM(jetsel[0].pt, jetsel[0].eta, jetsel[0].phi, jetsel[0].mass)
            jet2.SetPtEtaPhiM(jetsel[1].pt, jetsel[1].eta, jetsel[1].phi, jetsel[1].mass)
            retval = (jet1+jet2).M()
        else:         
            if not _dr: retval = deltaPhi( jetsel[0].phi, jetsel[1].phi)
            else:       retval = deltaR(jetsel[0], jetsel[1])
        return retval

   
    #############Pablin
    def get_SF_btag(self, pt, eta, mcFlavour):

       flavour = 2
       if abs(mcFlavour) == 5: flavour = 0
       elif abs(mcFlavour)==4: flavour = 1
  
       pt_cutoff  = max(30. , min(669., pt))
       eta_cutoff = min(2.39, abs(eta))

       if flavour == 2:
          SF = self.reader_light.eval(flavour,eta_cutoff, pt_cutoff);
          SFup = self.reader_light_UP.eval(flavour,eta_cutoff, pt_cutoff);
          SFdown = self.reader_light_DN.eval(flavour,eta_cutoff, pt_cutoff);
          SFcorr = self.reader_lightFASTSIM.eval(flavour,eta_cutoff, pt_cutoff);
          SFupcorr = self.reader_light_UPFASTSIM.eval(flavour,eta_cutoff, pt_cutoff);
          SFdowncorr = self.reader_light_DNFASTSIM.eval(flavour,eta_cutoff, pt_cutoff);
       else:
          SF = self.reader_heavy.eval(flavour,eta_cutoff, pt_cutoff)
          SFup  = self.reader_heavy_UP.eval(flavour,eta_cutoff, pt_cutoff)
          SFdown = self.reader_heavy_DN.eval(flavour,eta_cutoff, pt_cutoff)
          SFcorr = self.reader_heavyFASTSIM.eval(flavour,eta_cutoff, pt_cutoff)
          SFupcorr  = self.reader_heavy_UPFASTSIM.eval(flavour,eta_cutoff, pt_cutoff)
          SFdowncorr = self.reader_heavy_DNFASTSIM.eval(flavour,eta_cutoff, pt_cutoff)

       return [SF*SFcorr, SFup*SFupcorr, SFdown*SFdowncorr]


    def getBtagEffFromFile(self, pt, eta, mcFlavour):
    
       pt_cutoff = max(20.,min(399., pt))
       if (abs(mcFlavour) == 5): 
           h = self.h_btag_eff_b
           #use pt bins up to 600 GeV for b
           pt_cutoff = max(20.,min(599., pt))
       elif (abs(mcFlavour) == 4):
           h = self.h_btag_eff_c
       else:
           h = self.h_btag_eff_udsg
    
       binx = h.GetXaxis().FindBin(pt_cutoff)
       biny = h.GetYaxis().FindBin(fabs(eta))

       return h.GetBinContent(binx,biny)


    def getWeightBtag(self, jets):

        mcTag = 1.
        mcNoTag = 1.
        dataTag = 1.
        dataNoTag = 1.
        errHup   = 0
        errHdown = 0
        errLup   = 0
        errLdown = 0
    
        for jet in jets:
        
            csv = jet.btagCSV
            mcFlavor = (jet.hadronFlavour if hasattr(jet, 'hadronFlavour') else jet.mcFlavour)
            eta = jet.eta
            pt = jet.pt

            if(eta > 2.5): continue
            if(pt < 20): continue
            eff = self.getBtagEffFromFile(pt, eta, mcFlavor)

            istag = csv > 0.890 and eta < 2.5 and pt > 20
            SF = self.get_SF_btag(pt, eta, mcFlavor)
            if(istag):
                 mcTag = mcTag * eff
                 dataTag = dataTag * eff * SF[0]
                 if(mcFlavor == 5 or mcFlavor ==4):
	             errHup  = errHup + (SF[1] - SF[0]  )/SF[0]
	             errHdown = errHdown = (SF[0] - SF[2])/SF[0]
                 else: 
	             errLup = errLup + (SF[1] - SF[0])/SF[0]
                     errLdown = errLdown + (SF[0] - SF[2])/SF[0]
            else: 
                 mcNoTag = mcNoTag * (1 - eff)
                 dataNoTag = dataNoTag * (1 - eff*SF[0])
                 if mcFlavor==5 or mcFlavor==4:
	             errHup = errHup * -eff*(SF[1] - SF[0]  )/(1-eff*SF[0])
                     errHdown = errHdown * -eff*(SF[0] - SF[2])/(1-eff*SF[0])	
                 else:
	             errLup = errLup * -eff*(SF[1] - SF[0]  )/(1-eff*SF[0])
	             errLdown = errLdown * -eff*(SF[0] - SF[2])/(1-eff*SF[0]);	


        wtbtag = (dataNoTag * dataTag ) / ( mcNoTag * mcTag )
        wtbtagUp_heavy   = wtbtag*( 1 + errHup   )
        wtbtagUp_light   = wtbtag*( 1 + errLup   )
        wtbtagDown_heavy = wtbtag*( 1 - errHdown )
        wtbtagDown_light = wtbtag*( 1 - errLdown )

        return [wtbtag, wtbtagUp_heavy, wtbtagUp_light, wtbtagDown_heavy, wtbtagDown_light]



 
def _susyEdge(lep):
        if lep.pt <= 10.: return False
        if abs(lep.eta) > 2.4: return False
        if abs(lep.dxy) > 0.05: return False
        if abs(lep.dz ) > 0.10: return False
        if abs(lep.eta) > 1.4 and abs(lep.eta) < 1.6: return False
        # marc aug07 if abs(lep.pdgId) == 13 and lep.muonMediumId != 1: return False
        if abs(lep.pdgId) == 13:
          if lep.mediumMuonId != 1: return False
          if lep.miniRelIso > 0.2: return False
        #if abs(lep.pdgId) == 11 and (lep.tightId < 1 or (abs(lep.etaSc) > 1.4442 and abs(lep.etaSc) < 1.566)) : return False
        if abs(lep.pdgId) == 11:
          etatest = (abs(lep.etaSc) if hasattr(lep, 'etaSc') else abs(lep.eta))
          if (etatest > 1.4442 and etatest < 1.566) : return False
          if (lep.convVeto == 0) or (lep.lostHits > 0) : return False
          ## phys14 training if (abs(lep.eta) < 0.8 and lep.mvaIdPhys14 < 0.73) : return False
          ## phys14 training if (abs(lep.eta) > 0.8 and abs(lep.eta) < 1.479 and lep.mvaIdPhys14 < 0.57) : return False
          ## phys14 training if (abs(lep.eta) > 1.479 and lep.mvaIdPhys14 < 0.05) : return False
          if (abs(lep.eta) < 0.8 and lep.mvaIdSpring15 < 0.87) : return False
          if (abs(lep.eta) > 0.8 and abs(lep.eta) < 1.479 and lep.mvaIdSpring15 < 0.60) : return False
          if (abs(lep.eta) > 1.479 and lep.mvaIdSpring15 < 0.17) : return False
          if lep.miniRelIso > 0.1: return False
        return True

if __name__ == '__main__':
    from sys import argv
    file = ROOT.TFile(argv[1])
    tree = file.Get("tree")
    tree.vectorTree = True
    class Tester(Module):
        def __init__(self, name):
            Module.__init__(self,name,None)
            self.sf1 = edgeFriends("Edge", 
                lambda lep : _susyEdge(lep),
                cleanJet = lambda lep,jet,dr : (jet.pt < 35 and dr < 0.4 and abs(jet.eta) > 2.4))
        def analyze(self,ev):
            print "\nrun %6d lumi %4d event %d: leps %d" % (ev.run, ev.lumi, ev.evt, ev.nLepGood)
            print self.sf1(ev)
            print self.sf2(ev)
            print self.sf3(ev)
            print self.sf4(ev)
            print self.sf5(ev)
    el = EventLoop([ Tester("tester") ])
    el.loop([tree], maxEvents = 50)
