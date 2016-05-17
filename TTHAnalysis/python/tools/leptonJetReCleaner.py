from CMGTools.TTHAnalysis.treeReAnalyzer import *
from CMGTools.TTHAnalysis.tools.conept import coneptRA5, coneptRA7
from PhysicsTools.HeppyCore.utils.deltar import matchObjectCollection3
import ROOT
import numpy as num
from math import copysign
ROOT.gSystem.Load('libCondFormatsBTauObjects') 

bottoms=[5,511,521 ]
charms=[4,411,421,441,443 ]
lights=[1,2,3,111,211,130,210,321,551,553 ]
promptMothers=[23,24,-24,1000024,-1000024]

class MyVarProxy:
    def __init__(self,lep):
        self._ob = lep
    def __getitem__(self,name):
        return self.__getattr__(name)
    def __getattr__(self,name):
        if name in self.__dict__: return self.__dict__[name]
        else: return getattr(self._ob,name)
    def eta(self): return self._ob.eta
    def phi(self): return self._ob.phi
    def pt(self): return self._ob.pt
    def pdgId(self): return self._ob.pdgId

class LeptonJetReCleaner:
#    def __init__(self,label,looseLeptonSel,cleaningLeptonSel,FOLeptonSel,tightLeptonSel,cleanJet,selectJet,doBtagRWT=False,isFastSim=False,cleanWithTaus=False,coneptdef=None):
    def __init__(self,label,looseLeptonSel,cleaningLeptonSel,FOLeptonSel,tightLeptonSel,cleanJet,selectJet,CSVbtagFileName=None,EFFbtagFileName=None,CSVbtagFileNameFastSim=None,isFastSim=False, jetPt=40, bJetPt=25, doVeto="RA5"):
        self.corr = "RA7" if doVeto=="RA7" else "RA5"
        self.label = "" if (label in ["",None]) else ("_"+label)
        self.looseLeptonSel = looseLeptonSel
        self.cleaningLeptonSel = cleaningLeptonSel # applied on top of looseLeptonSel
        self.FOLeptonSel = FOLeptonSel # applied on top of looseLeptonSel
        self.tightLeptonSel = tightLeptonSel # applied on top of looseLeptonSel
        self.doVeto = doVeto # version of mll vetos at tight and fake lepton selections (either RA5 or RA7)
        self.cleanJet = cleanJet
        self.selectJet = selectJet
        self.doBtagRWT = doBtagRWT
        self.isFastSim = isFastSim
        if self.isFastSim:
            print '-'*15
            print 'WARNING: will apply b-tag scale factors for FastSim'
            print '-'*15
        self.systsJEC = {0:"", 1:"_jecUp", -1:"_jecDown"}
        self.systsBTAG = dict(enumerate(["", "_JESUp", "_JESDown", "_LFUp", "_LFDown", "_HFUp", "_HFDown", \
                                             "_HFStats1Up", "_HFStats1Down", "_HFStats2Up", "_HFStats2Down", \
                                             "_LFStats1Up", "_LFStats1Down", "_LFStats2Up", "_LFStats2Down", \
                                             "_cErr1Up", "_cErr1Down", "_cErr2Up", "_cErr2Down" ]))
        self.cleanWithTaus = cleanWithTaus
        self.coneptdef = coneptdef
        self.debugprinted = False
        self.jetPt = str(jetPt)
        self.bJetPt = str(bJetPt) if bJetPt != jetPt else str(jetPt-5)
    def listBranches(self):
        label = self.label

        biglist = [
            ("nLepGood","I"), ("LepGood_conePt","F",20,"nLepGood"),
            ("nLepLoose"+label, "I"), ("iL"+label,"I",20), # passing loose
            ("nLepLooseVeto"+label, "I"), ("iLV"+label,"I",20), # passing loose + veto
            ("nLepCleaning"+label, "I"), ("iC"+label,"I",20), # passing cleaning
            ("nLepCleaningVeto"+label, "I"), ("iCV"+label,"I",20), # passing cleaning + veto
            ("nLepFO"+label, "I"), ("iF"+label,"I",20), # passing FO, sorted by conept
            ("nLepFOVeto"+label, "I"), ("iFV"+label,"I",20), # passing FO + veto, sorted by conept
            ("nLepTight"+label, "I"), ("iT"+label,"I",20), # passing tight, sorted by conept
            ("nLepTightVeto"+label, "I"), ("iTV"+label,"I",20), # passing tight + veto, sorted by conept
            ("LepGood_isLoose"+label,"I",20,"nLepGood"),("LepGood_isLooseVeto"+label,"I",20,"nLepGood"),
            ("LepGood_isCleaning"+label,"I",20,"nLepGood"),("LepGood_isCleaningVeto"+label,"I",20,"nLepGood"),
            ("LepGood_isFO"+label,"I",20,"nLepGood"),("LepGood_isFOVeto"+label,"I",20,"nLepGood"),
            ("LepGood_isTight"+label,"I",20,"nLepGood"),("LepGood_isTightVeto"+label,"I",20,"nLepGood"),
            ("LepGood_mcMatchPdgId","F",20,"nLepGood"), # calculate conept and matched charge, now calculated in production
            #("LepGood_mcMatchCode","I",20,"nLepGood"), # calculate match code
            ("LepGood_mcUSCXMatch","I",20,"nLepGood"), # calculate match code
            #prompt -> 0
            #prompt but charge flip -> 1
            #light flavour fake -> 2
            #heavy flavor fake -> 3
            #isolated photon conversion -> 4 
            ]

        biglist.extend([
                ("mZ1"+label,"F"), ("minMllAFAS"+label,"F"), ("minMllAFOS"+label,"F"), ("minMllAFSS"+label,"F"), ("minMllSFOS"+label,"F")
                ])

        if self.isFastSim: biglist.append(("pTGluinoPair","F"))
        for key in self.systsJEC:
            biglist.extend([
                    #("iJ"+label+self.systsJEC[key],"I",20,"nJetSel"+label),
                    #("iJ1"+label+self.systsJEC[key],"I"),
                    #("iJ2"+label+self.systsJEC[key],"I"),
                    ("nJetSel"+label+self.systsJEC[key], "I"), ("iJ"+label+self.systsJEC[key],"I",20,"nJetSel"+label+self.systsJEC[key]), # index >= 0 if in Jet; -1-index (<0) if in DiscJet
                    #("iJSel"+label+self.systsJEC[key],"I",20,"nJetSel"+label+self.systsJEC[key]),
                    ("nDiscJetSel"+label+self.systsJEC[key], "I"), ("iDiscJ"+label+self.systsJEC[key],"I",20,"nDiscJetSel"+label+self.systsJEC[key]), # index >= 0 if in Jet; -1-index (<0) if in DiscJet
                    ("nJet40"+label+self.systsJEC[key], "I"), "htJet40j"+label+self.systsJEC[key], ("nBJetLoose40"+label+self.systsJEC[key], "I"), ("nBJetMedium40"+label+self.systsJEC[key], "I"),
                    ("nJet25"+label+self.systsJEC[key], "I"), "htJet25j"+label+self.systsJEC[key], ("nBJetLoose25"+label+self.systsJEC[key], "I"), ("nBJetMedium25"+label+self.systsJEC[key], "I"),
                    "mhtJet25"+label+self.systsJEC[key],
#                    ("nJetSel"+self.systsJEC[key]+label, "I"), ("iJ"+self.systsJEC[key]+label,"I",20,"nJetSel"+self.systsJEC[key]+label), # index >= 0 if in Jet; -1-index (<0) if in DiscJet
                    ("nJet"+self.jetPt+self.systsJEC[key]+label, "I"), "htJet"+self.jetPt + "j"+self.systsJEC[key]+label, ("nBJetLoose"+self.jetPt+self.systsJEC[key]+label, "I"), ("nBJetMedium"+self.jetPt+self.systsJEC[key]+label, "I"),
                    ("nJet"+self.bJetPt+self.systsJEC[key]+label, "I"), "htJet"+self.bJetPt+"j"+self.systsJEC[key]+label, ("nBJetLoose"+self.bJetPt+self.systsJEC[key]+label, "I"), ("nBJetMedium"+self.bJetPt+self.systsJEC[key]+label, "I"),
                    ])
            for bkey in self.systsBTAG:
                thisvar = self.select_jec_btag_unc_combinations(key,bkey)
                if thisvar!=None:
                    biglist.extend([
                            ("eventBTagSF"+label+thisvar, "F")
                            ])
        for jfloat in "pt eta phi mass btagCSV rawPt".split():
            biglist.append( ("JetSel"+label+"_"+jfloat,"F",20,"nJetSel"+label) )
            biglist.append( ("DiscJetSel"+label+"_"+jfloat,"F",20,"nDiscJetSel"+label) )
        biglist.append( ("JetSel"+label+"_mcPt",     "F",20,"nJetSel"+label) )
        biglist.append( ("JetSel"+label+"_mcFlavour","I",20,"nJetSel"+label) )
        biglist.append( ("JetSel"+label+"_mcMatchId","I",20,"nJetSel"+label) )
        biglist.append( ("JetSel"+label+"_BT","I",20,"nJetSel"+label) )
        biglist.append( ("DiscJetSel"+label+"_mcPt",     "F",20,"nDiscJetSel"+label) )
        biglist.append( ("DiscJetSel"+label+"_mcFlavour","I",20,"nDiscJetSel"+label) )
        biglist.append( ("DiscJetSel"+label+"_mcMatchId","I",20,"nDiscJetSel"+label) )
        return biglist

<<<<<<< HEAD
    def fillCollWithVeto(self,ret,refcollection,leps,lab,labext,selection,lepsforveto=None,ht=-1,sortby=None,pad_zeros_up_to=20, event=None):
=======
    def fillCollWithVeto(self,ret,refcollection,leps,lab,labext,selection,lepsforveto,ht=-1,doVetoZ=True,doVetoLM=True):
>>>>>>> 9fab09c... changes at recleaner level and config
        ret['i'+lab] = [];
        ret['i'+lab+'V'] = [];
        for lep in leps:
            if (selection(lep) if ht<0 else selection(lep,ht)):
                ret['i'+lab].append(refcollection.index(lep))
        ret['i'+lab] = self.sortIndexListByFunction(ret['i'+lab],refcollection,sortby)
        ret['nLep'+labext] = len(ret['i'+lab])
        ret['LepGood_is'+labext] = [(1 if i in ret['i'+lab] else 0) for i in xrange(len(refcollection))]
        lepspass = [ refcollection[il] for il in ret['i'+lab]  ]
        if lepsforveto==None: lepsforveto = lepspass # if lepsforveto==None, veto selected leptons among themselves
        for lep in lepspass:
            if (not doVetoZ  or passMllTLVeto(lep, lepsforveto, 76, 106, True)) and \
               (not doVetoLM or passMllTLVeto(lep, lepsforveto,  0,  12, True)):
                ret['i'+lab+'V'].append(refcollection.index(lep))
        ret['i'+lab+'V'] = self.sortIndexListByFunction(ret['i'+lab+'V'],refcollection,sortby)
        ret['nLep'+labext+'Veto'] = len(ret['i'+lab+'V'])
        ret['LepGood_is'+labext+'Veto'] = [(1 if i in ret['i'+lab+'V'] else 0) for i in xrange(len(refcollection))]
        lepspassveto = [ refcollection[il] for il in ret['i'+lab+'V']  ]
        ret['i'+lab] = ret['i'+lab] + [0]*(pad_zeros_up_to-len(ret['i'+lab]))
        ret['i'+lab+'V'] = ret['i'+lab+'V'] + [0]*(pad_zeros_up_to-len(ret['i'+lab+'V']))
        return (ret,lepspass,lepspassveto)

    def sortIndexListByFunction(self,indexlist,parentcollection,func):
        if not func: return indexlist[:]
        newsort = sorted([(ij,parentcollection[ij]) for ij in indexlist], key = lambda x: func(x[1]), reverse=True)
        return [x[0] for x in newsort]

    def ptFirstPair(self, parts, pdgId, requireOnePair=False):
        gluinos = [p for p in parts if abs(p.pdgId)==pdgId]
        if len(gluinos)<2:
            if requireOnePair: raise RuntimeError, 'No pair found'
            return -1
        elif len(gluinos)>2:
            if requireOnePair: raise RuntimeError, 'More pairs found'
            gluinos = sorted(gluinos, key = lambda x : x.pt, reverse=True)[:2]
        dphi = gluinos[1].phi-gluinos[0].phi
        return hypot(gluinos[0].pt + (gluinos[1].pt)*cos(dphi), (gluinos[1].pt)*sin(dphi));


    def USMatchingLeptons(self, ret, leps, genParts, event):
        
        myleps = [MyVarProxy(lep) for lep in leps]
        mygenPs = [MyVarProxy(glep) for glep in genParts]

        def lepMatch(rec, gen):
            if gen.status !=1 and not (abs(gen.pdgId())==15 and gen.status ==2 ): return False
            #if min(rec.pt(), gen.pt())/max(rec.pt(), gen.pt())<0.1: return False
            if abs(rec.pdgId()) != abs(gen.pdgId()) and abs(gen.pdgId())!=15: return False
            #dr2 = deltaR2(rec.eta(),rec.phi(),gen.eta(),gen.phi())
            #if dr2 > 0.04: return False
            return True
        
        matchLep = matchObjectCollection3(myleps,mygenPs, 
                                          deltaRMax = 0.2, filter = lepMatch)
        
        def generalMatch(rec, gen):
            if gen.status !=1 and gen.status !=71: return False
            #if min(rec.pt(), gen.pt())/max(rec.pt(), gen.pt())<0.1: return False
            return True
        
        matchPart = matchObjectCollection3(myleps,mygenPs, 
                                           deltaRMax = 0.2, filter = generalMatch)
        
        for il, mylep in  enumerate(myleps):
            mygen = matchLep[mylep] if matchLep[mylep] else matchPart[mylep]
            code=-1
            
            if not mygen: 
                ret["LepGood_mcUSCXMatch"][il] =-1
                continue
            
            prompt = mygen.isPromptHard
            if mygen.pdgId()==22 or (mygen.motherId!=-9999 and mygen.motherId==22 and mygen.pdgId()==mylep.pdgId() ):
                if prompt: code= 4#-3
                else: code= -1#0

            if prompt or ((abs(mygen.pdgId())==abs(mylep.pdgId()) or abs(mygen.pdgId())==15 ) and ((mygen.motherId in promptMothers) or (abs(mygen.motherId)==15 and (mygen.grandMotherId in promptMothers)) ) ) :
                if mygen.pdgId()*mylep.pdgId()>0: code= 0#1
                else : code= 1 #2
            
            if (abs(mygen.pdgId()) in bottoms) or (mygen.motherId in bottoms) : code= 3#-1
            if (abs(mygen.pdgId()) in charms) or (mygen.motherId in charms) : code= 3#-2
            if (abs(mygen.pdgId()) in lights) or (mygen.motherId in lights) : code= 2#-2

            ret["LepGood_mcUSCXMatch"][il] =code


    def deepMatchLeptons(self, ret, leps, genParts,event):
       
        myleps = [MyVarProxy(lep) for lep in leps]
        mygenPs = [MyVarProxy(glep) for glep in genParts]
       
        def plausible(rec,gen):
            if abs(gen.pdgId()) in [12,14,16,23,24]: return False
            dr = deltaR(rec.eta(),rec.phi(),gen.eta(),gen.phi())
            if dr < 0.05 : return True
            if dr > 0.8: return False
            if min(rec.pt(),gen.pt())/max(rec.pt(),gen.pt()) < 0.1: return False
            return True
      
        match = matchObjectCollection3(myleps,mygenPs, 
                                       deltaRMax = 1.2, filter = plausible)
     
        for il, mylep in  enumerate(myleps):
            mygen = match[mylep]
            code=-1
            if mygen:
                if mygen.pdgId()==mylep.pdgId() or mygen.pdgId()==15*num.sign(mylep.pdgId()): code=0
                elif mygen.pdgId()==-1*mylep.pdgId(): code=1
                elif abs(mygen.pdgId())<=3 or mygen.pdgId()==21 or abs(mygen.pdgId())>100: code=2
                elif abs(mygen.pdgId())==4 or abs(mygen.pdgId())==5: code=3
                elif abs(mygen.pdgId())==22: code=4
                elif (abs(mygen.pdgId())+abs(mylep.pdgId()))==24: code=5

            ret["LepGood_mcMatchCode"][il] =code
            

    def matchLeptons(self, ret, leps, genleps, genlepsfromtau, event):

        # if precalculated, propagate the value and return
        if hasattr(event._tree,"LepGood_mcMatchPdgId"):
            if not hasattr(self,"printed_mcMatch_warning"):
                print 'Found LepGood_mcMatchPdgId in the event, will use that.'
                self.printed_mcMatch_warning = True
            for il,lep in enumerate(leps):
                ret["LepGood_mcMatchPdgId"][il] = lep.mcMatchPdgId
            return

        if not hasattr(self,"printed_mcMatch_warning"):
            print 'Will calculate LepGood_mcMatchPdgId in leptonJetReCleaner, the result will be similar to the precalculated one but not identical.'
            self.printed_mcMatch_warning = True

        def plausible(rec,gen):
            if abs(rec.pdgId()) == 11 and abs(gen.pdgId()) != 11:   return False
            if abs(rec.pdgId()) == 13 and abs(gen.pdgId()) != 13:   return False
            dr = deltaR(rec.eta(),rec.phi(),gen.eta(),gen.phi())
            if dr < 0.3: return True
            if rec.pt() < 10 and abs(rec.pdgId()) == 13 and gen.pdgId() != rec.pdgId(): return False
            if dr < 0.7: return True
            if min(rec.pt(),gen.pt())/max(rec.pt(),gen.pt()) < 0.3: return False
            return True

        allgenleps = genleps+genlepsfromtau
        myleps = [MyVarProxy(lep) for lep in leps]
        mygenleps = [MyVarProxy(glep) for glep in allgenleps]
        match = matchObjectCollection3(myleps,mygenleps, 
                                       deltaRMax = 1.2, filter = plausible)

        for il,mylep in enumerate(myleps):
            mygen = match[mylep]
            if mygen:
                if (mygen.sourceId != mylep.mcMatchId): raise RuntimeError, "Error in lepton re-matching: sourceId/mcMatchId %d %d"%(mygen.sourceId,mylep.mcMatchId)
                ret["LepGood_mcMatchPdgId"][il] = mygen.pdgId()
            else:
                if mylep.mcMatchId != 0:
                    if mylep.mcMatchId == 100:
                        print 'Warning (evt. %d): reco lepton which has mcMatchId==100, mcMatchAny==%d had been matched to a prompt lepton that was not included in the genLepton collections. It was not re-matched: assuming correct charge reconstruction in this case!'%(event.evt,mylep.mcMatchAny)
                        ret["LepGood_mcMatchPdgId"][il] = mylep.pdgId()
                    else: raise RuntimeError, "Error in lepton re-matching: lep.mcMatchId is %d for not matched"%(mylep.mcMatchId)

    def recleanJets(self,jetcollcleaned,jetcolldiscarded,lepcoll,postfix,ret,jetret,discjetret,doMatchQuantities=False,event=None):
        ### Define jets
        ret["iJ"+postfix] = []
        #ret["iJSel"+postfix] = []
        #ret["iJ1"+postfix] = 0
        #ret["iJ2"+postfix] = 0
        ret["iDiscJ"+postfix] = []
        # 0. mark each jet as clean
        for j in jetcollcleaned+jetcolldiscarded: j._clean = True
        # 1. associate to each lepton passing the cleaning selection its nearest jet 
        for lep in lepcoll:
            best = None; bestdr = 0.4
            for j in jetcollcleaned+jetcolldiscarded:
                dr = deltaR(lep,j)
                if dr < bestdr:
                    best = j; bestdr = dr
            if best is not None and self.cleanJet(lep,best,bestdr):
                best._clean = False
        # 2. compute the jet list
        for ijc,j in enumerate(jetcollcleaned):
            if not self.selectJet(j): continue
            elif not j._clean: ret["iDiscJ"+postfix].append(ijc)
            else: 
                ret["iJ"+postfix].append(ijc)
                #ret["JetSel"+postfix+"_BT"].append( getattr(j,jfloat)>0.8 )
                #ret["iJSel"+postfix].append(ijc)
        for ijd,j in enumerate(jetcolldiscarded):
            if not self.selectJet(j): continue
            elif not j._clean: ret["iDiscJ"+postfix].append(-1-ijd)
            else: 
                ret["iJ"+postfix].append(-1-ijd)
                #ret["JetSel"+postfix+"_BT"].append( getattr(j,jfloat)>0.8 )
        # 3. sort the jets by pt
        ret["iJ"+postfix].sort(key = lambda idx : jetcollcleaned[idx].pt if idx >= 0 else jetcolldiscarded[-1-idx].pt, reverse = True)
        ret["iDiscJ"+postfix].sort(key = lambda idx : jetcollcleaned[idx].pt if idx >= 0 else jetcolldiscarded[-1-idx].pt, reverse = True)
        #ret["JetSel"+postfix+"_BT"].sort(key = lambda idx : jetcollcleaned[idx].pt if idx >= 0 else jetcolldiscarded[-1-idx].pt, reverse = True)
        ret["nJetSel"+postfix] = len(ret["iJ"+postfix])
        ret["nDiscJetSel"+postfix] = len(ret["iDiscJ"+postfix])
        #ret["iJSel"+postfix].sort(key = lambda idx : jetcollcleaned[idx].pt if idx >= 0 else -100, reverse = True)
        #i1=ret["iJSel"+postfix][0] if len(ret["iJSel"+postfix])>=1 else 0
        #i2=ret["iJSel"+postfix][1] if len(ret["iJSel"+postfix])>1 else 0
        #ret["iJ1"+postfix], ret["iJ2"+postfix] = i1,i2
        # 4. compute the variables
        if doMatchQuantities:
            if not postfix==self.label: raise RuntimeError,'Inconsistent usage of postfix in LeptonJetReCleaner'
            for jfloat in "pt eta phi mass btagCSV rawPt".split():
                jetret[jfloat] = []
                discjetret[jfloat] = []
            for jmc in "mcPt mcFlavour mcMatchId".split():
                jetret[jmc] = []
                discjetret[jmc] = []
            for idx in ret["iJ"+postfix]:
                jet = jetcollcleaned[idx] if idx >= 0 else jetcolldiscarded[-1-idx]
                for jfloat in "pt eta phi mass btagCSV rawPt".split():
                    jetret[jfloat].append( getattr(jet,jfloat) )
                for jmc in "mcPt mcFlavour mcMatchId".split():
                    jetret[jmc].append( getattr(jet,jmc,-999) )
            for idx in ret["iDiscJ"+postfix]:
                jet = jetcollcleaned[idx] if idx >= 0 else jetcolldiscarded[-1-idx]
                for jfloat in "pt eta phi mass btagCSV rawPt".split():
                    discjetret[jfloat].append( getattr(jet,jfloat) )
                for jmc in "mcPt mcFlavour mcMatchId".split():
                    discjetret[jmc].append( getattr(jet,jmc,-999) )
        # 5. compute the sums
<<<<<<< HEAD
        ret["nJet25"+postfix] = 0; ret["htJet25j"+postfix] = 0; ret["nBJetLoose25"+postfix] = 0; ret["nBJetMedium25"+postfix] = 0
        ret["nJet40"+postfix] = 0; ret["htJet40j"+postfix] = 0; ret["nBJetLoose40"+postfix] = 0; ret["nBJetMedium40"+postfix] = 0
        cleanjets = [];
        mhtJet25vec = ROOT.TLorentzVector(0,0,0,0)
        for x in lepcoll: mhtJet25vec = mhtJet25vec - x.p4()
=======
        ret["nJet"+self.bJetPt+postfix] = 0; ret["htJet"+self.bJetPt+"j"+postfix] = 0; ret["nBJetLoose"+self.bJetPt+postfix] = 0; ret["nBJetMedium"+self.bJetPt+postfix] = 0
        ret["nJet"+self.jetPt+postfix] = 0; ret["htJet"+self.jetPt+"j"+postfix] = 0; ret["nBJetLoose"+self.jetPt+postfix] = 0; ret["nBJetMedium"+self.jetPt+postfix] = 0
        cleanjets = []; cleanBjets = []
>>>>>>> 9fab09c... changes at recleaner level and config
        for j in jetcollcleaned+jetcolldiscarded:
            if not (j._clean and self.selectJet(j)): continue
            cleanjets.append(j)
<<<<<<< HEAD
            if j.pt > 25:
                ret["nJet25"+postfix] += 1; ret["htJet25j"+postfix] += j.pt; 
                if j.btagCSV>0.460: ret["nBJetLoose25"+postfix] += 1
                if j.btagCSV>0.800: ret["nBJetMedium25"+postfix] += 1
                mhtJet25vec = mhtJet25vec - j.p4()
            if j.pt > 40:
                ret["nJet40"+postfix] += 1; ret["htJet40j"+postfix] += j.pt; 
                if j.btagCSV>0.460: ret["nBJetLoose40"+postfix] += 1
                if j.btagCSV>0.800: ret["nBJetMedium40"+postfix] += 1
        ret["mhtJet25"+postfix] = mhtJet25vec.Pt()
        return cleanjets

    def bestZ1TL(self,lepsl,lepst,cut=lambda lep:True):
          pairs = []
          for l1 in lepst:
            if not cut(l1): continue
            for l2 in lepsl:
                if not cut(l2): continue
                if l1.pdgId == -l2.pdgId:
                   mz = (l1.p4() + l2.p4()).M()
                   diff = abs(mz-91.2)
                   pairs.append( (diff,mz) )
          if len(pairs):
              pairs.sort()
              return pairs[0][1]
          return 0.
    def minMllTL(self, lepsl, lepst, bothcut=lambda lep:True, onecut=lambda lep:True, paircut=lambda lep1,lep2:True):
            pairs = []
            for l1 in lepst:
                if not bothcut(l1): continue
                for l2 in lepsl:
                    if l2 == l1 or not bothcut(l2): continue
                    if not onecut(l1) and not onecut(l2): continue
                    if not paircut(l1,l2): continue
                    mll = (l1.p4() + l2.p4()).M()
                    pairs.append(mll)
            if len(pairs):
                return min(pairs)
            return -1
=======
            if j.btagCSV>0.890: cleanBjets.append(j)
            if j.pt > float(self.bJetPt):
                ret["nJet"+self.bJetPt+postfix] += 1; ret["htJet"+self.bJetPt+"j"+postfix] += j.pt; 
                if j.btagCSV>0.605: ret["nBJetLoose"+self.bJetPt+postfix] += 1
                if j.btagCSV>0.890: ret["nBJetMedium"+self.bJetPt+postfix] += 1
            if j.pt > float(self.jetPt):
                ret["nJet"+self.jetPt+postfix] += 1; ret["htJet"+self.jetPt+"j"+postfix] += j.pt; 
                if j.btagCSV>0.605: ret["nBJetLoose"+self.jetPt+postfix] += 1
                if j.btagCSV>0.890: ret["nBJetMedium"+self.jetPt+postfix] += 1
        return (cleanjets,cleanBjets)

>>>>>>> 9fab09c... changes at recleaner level and config

    def __call__(self,event):
        self.ev = event
        fullret = {}
        leps = [l for l in Collection(event,"LepGood","nLepGood")]
<<<<<<< HEAD
        if not self.coneptdef: raise RuntimeError, 'Choose the definition to be used for cone pt'
        for lep in leps: lep.conept = self.coneptdef(lep)
        taus_forclean = [t for t in Collection(event,"TauGood","nTauGood")] if self.cleanWithTaus else []
=======
        if self.corr == "RA7": 
            for lep in leps: lep.conept = coneptRA7(lep.pt,lep.miniRelIso,lep.jetPtRatiov2,lep.jetPtRelv2,lep.pdgId,2)
        else: 
            for lep in leps: lep.conept = coneptRA5(lep.pt,lep.miniRelIso,lep.jetPtRatiov2,lep.jetPtRelv2,lep.pdgId,2)
>>>>>>> 9fab09c... changes at recleaner level and config
        jetsc={}
        jetsd={}
        for var in self.systsJEC:
            _var = var
            if not hasattr(event,"nJet"+self.systsJEC[var]):
                _var = 0
                if not self.debugprinted:
                    print '-'*15
                    print 'WARNING: jet energy scale variation %s not found, will set it to central value'%self.systsJEC[var]
                    print '-'*15
            jetsc[var] = [j for j in Collection(event,"Jet"+self.systsJEC[_var],"nJet"+self.systsJEC[_var])]
            jetsd[var] = [j for j in Collection(event,"DiscJet"+self.systsJEC[_var],"nDiscJet"+self.systsJEC[_var])]
        self.debugprinted = True
        ret = {}; retwlabel = {}; jetret = {}; discjetret = {};

        lepsl = []; lepslv = [];
<<<<<<< HEAD
        ret, lepsl, lepslv = self.fillCollWithVeto(ret,leps,leps,'L','Loose',self.looseLeptonSel,event=event)
=======
        ret, lepsl, lepslv = self.fillCollWithVeto(ret,leps,leps,'L','Loose',self.looseLeptonSel,None,-1,self.doVeto)
>>>>>>> 9fab09c... changes at recleaner level and config
        lepsc = []; lepscv = [];
        ret, lepsc, lepscv = self.fillCollWithVeto(ret,leps,lepsl,'C','Cleaning',self.cleaningLeptonSel,lepsl,-1,self.doVeto)

        ret['mZ1'] = self.bestZ1TL(lepsl, lepsl)
        ret['minMllAFAS'] = self.minMllTL(lepsl, lepsl) 
        ret['minMllAFOS'] = self.minMllTL(lepsl, lepsl, paircut = lambda l1,l2 : l1.charge !=  l2.charge) 
        ret['minMllAFSS'] = self.minMllTL(lepsl, lepsl, paircut = lambda l1,l2 : l1.charge ==  l2.charge) 
        ret['minMllSFOS'] = self.minMllTL(lepsl, lepsl, paircut = lambda l1,l2 : l1.pdgId  == -l2.pdgId) 

        cleanjets={}
        for var in self.systsJEC:
            cleanjets[var] = self.recleanJets(jetsc[var],jetsd[var],lepsc+taus_forclean,self.label+self.systsJEC[var],retwlabel,jetret,discjetret,(var==0),event=event)
            for btagsyst in self.systsBTAG:
                thisvar = self.select_jec_btag_unc_combinations(var,btagsyst)
                if thisvar!=None: retwlabel["eventBTagSF"+self.label+thisvar] = self.bTag_eventRWT_SF(event,lepsc,cleanjets[var],self.systsBTAG[btagsyst]) if self.doBtagRWT else 1

<<<<<<< HEAD
        # calculate FOs and tight leptons using the cleaned HT, sorted by conept
        lepsf = []; lepsfv = [];
        ret, lepsf, lepsfv = self.fillCollWithVeto(ret,leps,lepsl,'F','FO',self.FOLeptonSel,lepsl,retwlabel["htJet40j"+self.label],sortby = lambda x: x.conept)
        lepst = []; lepstv = [];
        ret, lepst, lepstv = self.fillCollWithVeto(ret,leps,lepsl,'T','Tight',self.tightLeptonSel,lepsl,retwlabel["htJet40j"+self.label],sortby = lambda x: x.conept, event=event)
=======
        # calculate FOs and tight leptons using the cleaned HT
        veto = lepsl; doZ = True; doLMf = True; doLMt = True
        if self.doVeto == "RA7": veto = None; doZ = False; doLMf = False; doLMt = True
        lepsf = []; lepsfv = [];
        ret, lepsf, lepsfv = self.fillCollWithVeto(ret,leps,lepsl,'F','FO'   , self.FOLeptonSel   ,veto,ret["htJet"+self.jetPt+"j"],doZ,doLMf)
        lepst = []; lepstv = [];
        ret, lepst, lepstv = self.fillCollWithVeto(ret,leps,lepsl,'T','Tight', self.tightLeptonSel,veto,ret["htJet"+self.jetPt+"j"],doZ,doLMt)
>>>>>>> 9fab09c... changes at recleaner level and config

        ### attach labels and return
        fullret["nLepGood"]=len(leps)
        fullret["LepGood_conePt"] = [lep.conept for lep in leps]
        fullret["LepGood_mcMatchPdgId"] = [0] * len(leps)
        if not event.isData: self.matchLeptons(fullret,leps,[l for l in Collection(event,"genLep","ngenLep")],[l for l in Collection(event,"genLepFromTau","ngenLepFromTau")],event)
        #fullret["LepGood_mcMatchCode"] = [-1] * len(leps)
        fullret["LepGood_mcUSCXMatch"] = [-1] * len(leps)
        #if not event.isData: self.deepMatchLeptons(fullret, leps, Collection(event,'GenPart','nGenPart'),event)
        if not event.isData: self.USMatchingLeptons(fullret, leps, Collection(event,'GenPart','nGenPart'),event)
        if self.isFastSim:  fullret["pTGluinoPair"] = self.ptFirstPair(Collection(event,'GenPart','nGenPart'), 1000021, requireOnePair=True)
        for k,v in ret.iteritems(): 
            fullret[k+self.label] = v
        fullret.update(retwlabel)
        for k,v in jetret.iteritems(): 
            fullret["JetSel%s_%s" % (self.label,k)] = v
        for k,v in discjetret.iteritems(): 
            fullret["DiscJetSel%s_%s" % (self.label,k)] = v
        return fullret

    def bTag_eventRWT_SF(self,ev,leps,jets,systlabel):
        if ev.isData: return 1
        sf = 1
        for l in leps: sf = sf * getattr(l,"jetBTagCSVWeight"+systlabel)
        for j in jets: sf = sf * getattr(j,"btagCSVWeight"+systlabel)
        return sf
    def select_jec_btag_unc_combinations(self,jetunc,btagunc):
        if "JESUp" in self.systsBTAG[btagunc]: return "_jecUp" if self.systsJEC[jetunc]=="_jecUp" else None
        if "JESDown" in self.systsBTAG[btagunc]: return "_jecDown" if self.systsJEC[jetunc]=="_jecDown" else None
        return self.systsBTAG[btagunc]+self.systsJEC[jetunc] if self.systsJEC[jetunc]=="" else None

def passMllVeto(l1, l2, mZmin, mZmax, isOSSF ):
    if  l1.pdgId == -l2.pdgId or not isOSSF:
        mz = (l1.p4() + l2.p4()).M()
        if mz > mZmin and  mz < mZmax:
            return False
    return True

def passMllTLVeto(lep, lepsl, mZmin, mZmax, isOSSF):
    for ll in lepsl:
        if ll == lep: continue
        if not passMllVeto(lep, ll, mZmin, mZmax, isOSSF):
            return False
    return True

def passTripleMllVeto(l1, l2, l3, mZmin, mZmax, isOSSF ):
    ls = [passMllVeto(l1, l2, mZmin, mZmax, isOSSF), \
          passMllVeto(l1, l3, mZmin, mZmax, isOSSF), \
          passMllVeto(l2, l3, mZmin, mZmax, isOSSF)]
    if all(ls): return True
    return False

def _tthlep_lepId(lep):
        #if lep.pt <= 10: return False
        if abs(lep.pdgId) == 13:
            if lep.pt <= 5: return False
            if not lep.tightCharge >= 1: return False
            return True
        elif abs(lep.pdgId) == 11:
            if lep.pt <= 7: return False
            if not (lep.convVeto and lep.lostHits == 0 and lep.tightCharge >= 2): 
                return False
            return True
        return False

def _ttH_idEmu_cuts_E2(lep):
    if (abs(lep.pdgId)!=11): return True
    if (lep.hadronicOverEm>=(0.10-0.03*(abs(lep.etaSc)>1.479))): return False
    if (abs(lep.dEtaScTrkIn)>=(0.01-0.002*(abs(lep.etaSc)>1.479))): return False
    if (abs(lep.dPhiScTrkIn)>=(0.04+0.03*(abs(lep.etaSc)>1.479))): return False
    if (lep.eInvMinusPInv<=-0.05): return False
    if (lep.eInvMinusPInv>=(0.01-0.005*(abs(lep.etaSc)>1.479))): return False
    if (lep.sigmaIEtaIEta>=(0.011+0.019*(abs(lep.etaSc)>1.479))): return False
    return True

def _susy2lss_lepId_CBloose(lep):
        if abs(lep.pdgId) == 13:
            if lep.pt <= 5: return False
            return True #lep.mediumMuonId > 0
        elif abs(lep.pdgId) == 11:
            if lep.pt <= 7: return False
            if not (lep.convVeto and lep.lostHits <= 1): 
                return False
            if not lep.mvaIdSpring15 > -0.70+(-0.83+0.70)*(abs(lep.etaSc)>0.8)+(-0.92+0.83)*(abs(lep.etaSc)>1.479):
                return False
            if not _susy2lss_idEmu_cuts(lep): return False
            return True
        return False

def _susy2lss_lepConePt1015(lep):
    if lep.conept <= (10 if abs(lep.pdgId)==13 else 15): return False
    return True

def _susy2lss_lepId_loosestFO(lep):
    if not _susy2lss_lepId_CBloose(lep): return False
    if abs(lep.pdgId) == 13:
        return lep.mediumMuonId > 0 and lep.tightCharge > 0
    elif abs(lep.pdgId) == 11:
        return (lep.convVeto and lep.tightCharge > 1 and lep.lostHits == 0)
    return False

def _susy2lss_lepId_tighterFO(lep):
    if not _susy2lss_lepId_loosestFO(lep): return False
    if abs(lep.pdgId)==11:
        if not lep.mvaIdSpring15 > -0.155+(-0.56+0.155)*(abs(lep.etaSc)>0.8)+(-0.76+0.56)*(abs(lep.etaSc)>1.479):
            return False
        if not _susy2lss_idIsoEmu_cuts(lep): return False
    return True

def _susy2lss_lepId_inSituLoosestFO(lep):
    if not _susy2lss_lepId_loosestFO(lep): return False
    if abs(lep.pdgId)==11:
        if not lep.mvaIdSpring15 > -0.363+(-0.579+0.363)*(abs(lep.etaSc)>0.8)+(-0.623+0.579)*(abs(lep.etaSc)>1.479):
            return False
    return True

def _susy2lss_lepId_inSituTighterFO(lep):
    if not _susy2lss_lepId_loosestFO(lep): return False
    if abs(lep.pdgId)==11:
        if not lep.mvaIdSpring15 > 0.051+(-0.261-0.051)*(abs(lep.etaSc)>0.8)+(-0.403+0.261)*(abs(lep.etaSc)>1.479):
            return False
        if not _susy2lss_idIsoEmu_cuts(lep): return False
    return True

def _susy2lss_lepId_IPcuts(lep):
    if not lep.sip3d<4: return False
    if not (abs(lep.dxy)<0.05): return False
    if not (abs(lep.dz)<0.1): return False
    return True

def _susy2lss_lepId_CB(lep):
    if not _susy2lss_lepId_CBloose(lep): return False
    if not _susy2lss_lepId_IPcuts(lep): return False
    if abs(lep.pdgId) == 13:
        return lep.mediumMuonId > 0 and lep.tightCharge > 0
    elif abs(lep.pdgId) == 11:
        if not (lep.convVeto and lep.tightCharge > 1 and lep.lostHits == 0): 
            return False
        return lep.mvaIdSpring15 > 0.87+(0.60-0.87)*(abs(lep.etaSc)>0.8)+(0.17-0.60)*(abs(lep.etaSc)>1.479)
    return False

def _susy2lss_idEmu_cuts(lep):
    if (abs(lep.pdgId)!=11): return True
    if (lep.sigmaIEtaIEta>=(0.011 if abs(lep.etaSc)<1.479 else 0.031)): return False
    if (lep.hadronicOverEm>=0.08): return False
    if (abs(lep.dEtaScTrkIn)>=0.01): return False
    if (abs(lep.dPhiScTrkIn)>=(0.04 if abs(lep.etaSc)<1.479 else 0.08)): return False
    if (abs(lep.eInvMinusPInv)>=0.01): return False
    return True

def _susy2lss_idIsoEmu_cuts(lep):
    if (abs(lep.pdgId)!=11): return True
    if not _susy2lss_idEmu_cuts(lep): return False
    if (lep.ecalPFClusterIso>=0.45*lep.pt): return False
    if (lep.hcalPFClusterIso>=0.25*lep.pt): return False
    if (lep.dr03TkSumPt>=0.2*lep.pt): return False
    return True

def _susy2lss_multiIso(lep):
        if abs(lep.pdgId) == 13: A,B,C = (0.16,0.76,7.2)
        else:                    A,B,C = (0.12,0.80,7.2)
        return lep.miniRelIso < A and (lep.jetPtRatiov2 > B or lep.jetPtRelv2 > C)

def _susy2lss_multiIso_relaxedForInSituApp(lep):
        if abs(lep.pdgId) == 13: A,B,C = (0.4,0.76,7.2)
        else:                    A,B,C = (0.4,0.80,7.2)
        return lep.miniRelIso < A and (1/lep.jetPtRatiov2 < (1/B + lep.miniRelIso) or lep.jetPtRelv2 > C)

#def _susy2lss_multiIso_withMiniIsoRelaxed_ConePtJetPtRatiov2(lep):
#        if abs(lep.pdgId) == 13: A,B,C = (0.4,0.76,7.2)
#        else:                    A,B,C = (0.4,0.80,7.2)
#        return lep.miniRelIso < A and (conept(lep.pt,lep.miniRelIso,lep.jetPtRatiov2,lep.jetPtRelv2,lep.pdgId,2)/lep.pt*lep.jetPtRatiov2 > B or lep.jetPtRelv2 > C)
#def _susy2lss_multiIso_withMiniIsoRelaxed_CutForFO4(lep):
#        if abs(lep.pdgId) == 13: A,B,C = (0.4,0.76,7.2)
#        else:                    A,B,C = (0.4,0.80,7.2)
#        return lep.miniRelIso < A and (1/lep.jetPtRatiov2 < (1/B + lep.miniRelIso))

#def _susy2lss_lepId_CBOld(lep):
#        if lep.pt <= 10: return False
#        if abs(lep.pdgId) == 13:
#            return lep.tightId > 0
#        elif abs(lep.pdgId) == 11:
#            return lep.tightId >= 2 and lep.convVeto and lep.tightCharge > 1 and lep.lostHits == 0
#        return False

## CH: RA7 selection for Moriond

def _susy3l_multiIso(lep):
    # CH: looser WP than for RA5 (electrons -> medium, muons -> loose)
    if abs(lep.pdgId) == 13: A,B,C = (0.20,0.69,6.0)
    else:                    A,B,C = (0.16,0.76,7.2)
    return lep.miniRelIso < A and (lep.jetPtRatiov2 > B or lep.jetPtRelv2 > C)

def _susy3l_lepId_loosestFO(lep):
    # CH: the same as the 2lss one but without tightCharge
    if not _susy2lss_lepId_CBloose(lep): return False
    if abs(lep.pdgId) == 13:
        return lep.mediumMuonId > 0
    elif abs(lep.pdgId) == 11:
        return (lep.convVeto and lep.lostHits == 0)
    return False

def _susy3l_lepId_CB(lep):
    # CH: the same as the 2lss one but without tightCharge
    if not _susy2lss_lepId_CBloose(lep): return False
    if not _susy2lss_lepId_IPcuts(lep): return False
    if abs(lep.pdgId) == 13:
        return lep.mediumMuonId > 0
    elif abs(lep.pdgId) == 11:
        if not (lep.convVeto and lep.lostHits == 0): 
            return False
        return lep.mvaIdSpring15 > 0.87+(0.60-0.87)*(abs(lep.eta)>0.8)+(0.17-0.60)*(abs(lep.eta)>1.479)
    return False

if __name__ == '__main__':
    from sys import argv
    file = ROOT.TFile(argv[1])
    tree = file.Get("tree")
    tree.vectorTree = True
    class Tester(Module):
        def __init__(self, name):
            Module.__init__(self,name,None)
            self.sf1 = LeptonJetReCleaner("Old", 
                lambda lep : lep.relIso03 < 0.5, 
                lambda lep : lep.relIso03 < 0.1 and lep.sip3d < 4 and _susy2lss_lepId_CB(lep),
                cleanJet = lambda lep,jet,dr : (lep.pt > 10 and dr < 0.4))
            self.sf2 = LeptonJetReCleaner("PtRel", 
                lambda lep : lep.relIso03 < 0.4 or lep.jetPtRel > 5, 
                lambda lep : (lep.relIso03 < 0.1 or lep.jetPtRel > 14) and lep.sip3d < 4 and _susy2lss_lepId_CB(lep),
                cleanJet = lambda lep,jet,dr : (lep.pt > 10 and dr < 0.4))
            self.sf3 = LeptonJetReCleaner("MiniIso", 
                lambda lep : lep.miniRelIso < 0.4, 
                lambda lep : lep.miniRelIso < 0.05 and lep.sip3d < 4 and _susy2lss_lepId_CB(lep),
                cleanJet = lambda lep,jet,dr : (lep.pt > 10 and dr < 0.4))
            self.sf4 = LeptonJetReCleaner("PtRelJC", 
                lambda lep : lep.relIso03 < 0.4 or lep.jetPtRel > 5, 
                lambda lep : (lep.relIso03 < 0.1 or lep.jetPtRel > 14) and lep.sip3d < 4 and _susy2lss_lepId_CB(lep),
                cleanJet = lambda lep,jet,dr : (lep.pt > 10 and dr < 0.4 and not (lep.jetPtRel > 5 and lep.pt*(1/lep.jetPtRatio-1) > 25)))
            self.sf5 = LeptonJetReCleaner("MiniIsoJC", 
                lambda lep : lep.miniRelIso < 0.4, 
                lambda lep : lep.miniRelIso < 0.05 and lep.sip3d < 4 and _susy2lss_lepId_CB(lep),
                cleanJet = lambda lep,jet,dr : (lep.pt > 10 and dr < 0.4 and not (lep.jetDR > 0.5*10/min(50,max(lep.pt,200)) and lep.pt*(1/lep.jetPtRatio-1) > 25)))
        def analyze(self,ev):
            print "\nrun %6d lumi %4d event %d: leps %d" % (ev.run, ev.lumi, ev.evt, ev.nLepGood)
            print self.sf1(ev)
            print self.sf2(ev)
            print self.sf3(ev)
            print self.sf4(ev)
            print self.sf5(ev)
    el = EventLoop([ Tester("tester") ])
    el.loop([tree], maxEvents = 50)

        
