import random
import math
from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.Heppy.physicsobjects.PhysicsObjects import Jet
from PhysicsTools.Heppy.physicsutils.JetReCalibrator import JetReCalibrator

from PhysicsTools.HeppyCore.utils.deltar import *
import PhysicsTools.HeppyCore.framework.config as cfg

class monoXSubJetsSoftDropAnalyzer( Analyzer ):
    """Taken from RootTools.JetAnalyzer, simplified, modified, added corrections    """
    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(monoXSubJetsSoftDropAnalyzer,self).__init__(cfg_ana, cfg_comp, looperName)
        mcGT   = cfg_ana.mcGT   if hasattr(cfg_ana,'mcGT')   else "PHYS14_25_V2"
        dataGT = cfg_ana.dataGT if hasattr(cfg_ana,'dataGT') else "GR_70_V2_AN1"
        self.shiftJEC = self.cfg_ana.shiftJEC if hasattr(self.cfg_ana, 'shiftJEC') else 0
        self.recalibrateJets = self.cfg_ana.recalibrateJets
        self.addJECShifts = self.cfg_ana.addJECShifts if hasattr(self.cfg_ana, 'addJECShifts') else 0
        if   self.recalibrateJets == "MC"  : self.recalibrateJets =     self.cfg_comp.isMC
        elif self.recalibrateJets == "Data": self.recalibrateJets = not self.cfg_comp.isMC
        elif self.recalibrateJets not in [True,False]: raise RuntimeError, "recalibrateJets must be any of { True, False, 'MC', 'Data' }, while it is %r " % self.recalibrateJets
        self.doJEC = self.recalibrateJets or (self.shiftJEC != 0) or self.addJECShifts
        if self.doJEC:
          doResidual = getattr(cfg_ana, 'applyL2L3Residual', 'Data')
          if   doResidual == "MC":   doResidual = self.cfg_comp.isMC
          elif doResidual == "Data": doResidual = not self.cfg_comp.isMC
          elif doResidual not in [True,False]: raise RuntimeError, "If specified, applyL2L3Residual must be any of { True, False, 'MC', 'Data'(default)}"
          GT = getattr(cfg_comp, 'jecGT', mcGT if self.cfg_comp.isMC else dataGT)
          # instantiate the jet re-calibrator
####          self.jetReCalibrator = JetReCalibrator(GT, cfg_ana.recalibrationType, doResidual, cfg_ana.jecPath)

        self.jetLepDR = self.cfg_ana.jetLepDR  if hasattr(self.cfg_ana, 'jetLepDR') else 0.5
        self.lepPtMin = self.cfg_ana.minLepPt  if hasattr(self.cfg_ana, 'minLepPt') else -1


    def declareHandles(self):
        super(monoXSubJetsSoftDropAnalyzer, self).declareHandles()
        #print "+++++", self.cfg_comp.isMC
        if self.cfg_comp.isMC==True:
         #print "Taking right MC collection for SoftDrop Subjets"
         self.handles['jets'] = AutoHandle( (self.cfg_ana.jetCol, 'SubJets','PAT'), 'std::vector<pat::Jet>' )  #RECO for DATA, PAT for MC
        else:
         #print "Taking right Data collection for SoftDrop Subjets"
         self.handles['jets'] = AutoHandle( (self.cfg_ana.jetCol, 'SubJets','RECO'), 'std::vector<pat::Jet>' )
        self.handles['rho'] = AutoHandle( self.cfg_ana.rho, 'double' )

    def beginLoop(self, setup):
        super(monoXSubJetsSoftDropAnalyzer,self).beginLoop(setup)
        
    def process(self, event):
        self.readCollections( event.input )
        rho  = float(self.handles['rho'].product()[0])
        self.rho = rho

        ## Read jets, if necessary recalibrate and shift MET
        allJets = map(Jet, self.handles['jets'].product()) 

        self.deltaMetFromJEC = [0.,0.]
        self.type1METCorr    = [0.,0.,0.]
        if self.doJEC:
            if not self.recalibrateJets:  # check point that things won't change
                jetsBefore = [ (j.pt(),j.eta(),j.phi(),j.rawFactor()) for j in allJets ]
####            self.jetReCalibrator.correctAll(allJets, rho, delta=self.shiftJEC, 
####                                                addCorr=True, addShifts=self.addJECShifts,
####                                                metShift=self.deltaMetFromJEC, type1METCorr=self.type1METCorr )
            if not self.recalibrateJets: 
                jetsAfter = [ (j.pt(),j.eta(),j.phi(),j.rawFactor()) for j in allJets ]
                if len(jetsBefore) != len(jetsAfter): 
                    print "ERROR: I had to recompute jet corrections, and they rejected some of the jets:\nold = %s\n new = %s\n" % (jetsBefore,jetsAfter)
                else:
                    for (told, tnew) in zip(jetsBefore,jetsAfter):
                        if (deltaR2(told[1],told[2],tnew[1],tnew[2])) > 0.0001:
                            print "ERROR: I had to recompute jet corrections, and one jet direction moved: old = %s, new = %s\n" % (told, tnew)
                        elif abs(told[0]-tnew[0])/(told[0]+tnew[0]) > 0.5e-3 or abs(told[3]-tnew[3]) > 0.5e-3:
                            print "ERROR: I had to recompute jet corrections, and one jet pt or corr changed: old = %s, new = %s\n" % (told, tnew)

        ## Apply jet selection
        event.subJetSoftDrop     = []
        event.subJetSoftDropNoID = []
        for jet in allJets:
            if self.testJetNoID( jet ): 
                event.subJetSoftDropNoID.append(jet) 
                if self.testJetID ( jet ):
                    #print "++++++++++++++++++++++ ", jet.pt()
                    event.subJetSoftDrop.append(jet)

        ## Associate jets to leptons
        leptons = event.inclusiveLeptons if hasattr(event, 'inclusiveLeptons') else event.selectedLeptons
        jlpairs = matchObjectCollection( leptons, allJets, self.jetLepDR**2)

        for jet in allJets:
            jet.leptons = [l for l in jlpairs if jlpairs[l] == jet ]

        for lep in leptons:
            jet = jlpairs[lep]
            if jet is None:
                lep.fatjet = lep.jet
            else:
                lep.fatjet = jet   
                

    def testJetID(self, jet):
        #jet.puJetIdPassed = jet.puJetId() 
      return True
#####        jet.pfJetIdPassed = jet.jetID('POG_PFID_Loose') 
#####        if self.cfg_ana.relaxJetId:
#####            return True
#####        else:
#####            return jet.pfJetIdPassed
#####            #return jet.pfJetIdPassed and (jet.puJetIdPassed or not(self.doPuId)) 
        
    def testJetNoID( self, jet ):
        return jet.pt() > self.cfg_ana.jetPt and \
               abs( jet.eta() ) < self.cfg_ana.jetEta;
 
