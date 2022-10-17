########### author : Ashraf Mohamed ##########
########### institute : DESY, RWTH AACHEN #######################
########### Email : ashraf.mohamed@cern.ch #########
########### Date : Feb 2019 #######################
#### motivated by https://twiki.cern.ch/twiki/bin/viewauth/CMS/L1ECALPrefiringWeightRecipe

import math
import numpy
import ROOT

from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
import PhysicsTools.HeppyCore.framework.config as cfg
from PhysicsTools.HeppyCore.utils.deltar import deltaR2,deltaR
import PhysicsTools.HeppyCore.framework.config as cfg


def getPrefiringRate(eta,  pt, h_prefmap, fluctuation,prefiringRateSystUnc_):
    if (not h_prefmap  and not skipwarnings_) :
        print "Prefiring map not found, setting prefiring rate to 0 "
    if (not h_prefmap) : 
        return 0.
    #//Check pt is not above map overflow
    nbinsy = h_prefmap.GetNbinsY()
    maxy = h_prefmap.GetYaxis().GetBinLowEdge(nbinsy + 1)
    if (pt >= maxy):
        pt = maxy - 0.01
    thebin = h_prefmap.FindBin(eta, pt)

    prefrate = h_prefmap.GetBinContent(thebin)

    statuncty = h_prefmap.GetBinError(thebin)
    systuncty = prefiringRateSystUnc_ * prefrate

    if (fluctuation == 'up'):
        prefrate = min(1., prefrate + math.sqrt(pow(statuncty, 2) + pow(systuncty, 2)))
    if (fluctuation == 'down'):
        prefrate = max(0., prefrate - math.sqrt(pow(statuncty, 2) + pow(systuncty, 2)))
    return prefrate

##__________________________________________________________________||
class PrefiringAnalyzer(Analyzer):
    
    def __init__(self, cfg_ana, cfg_comp, looperName ):
        
         super(PrefiringAnalyzer,self).__init__(cfg_ana,cfg_comp,looperName)
         
         self.file_prefiringmaps_          = ROOT.TFile.Open(cfg_ana.L1Maps, 'read')
         self.dataera_                     = cfg_ana.DataEra
         self.useEMpt_                     = cfg_ana.UseJetEMPt
         self.prefiringRateSystUnc_        = cfg_ana.PrefiringRateSystematicUncty
         self.skipwarnings_                = cfg_ana.SkipWarnings
         ### warning messege if file is not exist
         if not self.file_prefiringmaps_ and not skipwarnings_: 
            print "File with maps not found. All prefiring weights set to 0. " 
         self.h_prefmap_photon             = self.file_prefiringmaps_.Get("L1prefiring_photonptvseta_"+self.dataera_)
         self.h_prefmap_jet                = self.file_prefiringmaps_.Get("L1prefiring_jetemptvseta_"+self.dataera_)
         ### warning messege if file is exist but the histograms are not 
         if not self.file_prefiringmaps_.Get("L1prefiring_photonptvseta_"+self.dataera_) and  not skipwarnings_ :
             print "Photon map not found. All photons prefiring weights set to 0. "
         if not self.file_prefiringmaps_.Get("L1prefiring_jetemptvseta_"+self.dataera_) and  not skipwarnings_ :
             print "Jet map not found. All jets prefiring weights set to 0. "

    def declareHandles(self):
        super(PrefiringAnalyzer, self).declareHandles()
    
    def beginLoop(self, setup):
        super(PrefiringAnalyzer,self).beginLoop(setup)

    def process(self, event):
        
        if not self.cfg_comp.isMC: return True
        
        fluctuations = ['central','up','down']
        thePhotons = event.selectedPhotons
        #//Jets
        theJets = event.cleanJetsAll

        #//Probability for the event NOT to prefire, computed with the prefiring maps per object.
        #//Up and down values correspond to the resulting value when shifting up/down all prefiring rates in prefiring maps.
        nonPrefiringProba = [1., 1., 1.]
        #//0: central, 1: up, 2: down
        
        for  i,fluct  in enumerate(fluctuations):
            for photon in thePhotons : 
                pt_gam = photon.pt()
                eta_gam = photon.eta()
                if (pt_gam < 20.) : continue
                if (abs(eta_gam) < 2.) : continue
                if (abs(eta_gam) > 3.) : continue
                prefiringprob_gam = getPrefiringRate(eta_gam, pt_gam, self.h_prefmap_photon , fluct,self.prefiringRateSystUnc_)
                nonPrefiringProba[i] *= (1. - prefiringprob_gam)
        
            #// Now applying the prefiring maps to jets in the affected regions.
            for jet in theJets:

                pt_jet = jet.pt()
                eta_jet = jet.eta()
                phi_jet = jet.phi()
                if pt_jet < 20. : continue
                if abs(eta_jet) < 2.: continue
                if abs(eta_jet) > 3.: continue

                #// Loop over photons to remove overlap
                nonprefiringprobfromoverlappingphotons = 1.
                for photon in thePhotons: 
                
                    pt_gam = photon.pt()
                    eta_gam = photon.eta()
                    phi_gam = photon.phi()
                    if pt_gam < 20. : continue
                    if abs(eta_gam) < 2. : continue
                    if abs(eta_gam) > 3. : continue
                    dR = deltaR(eta_jet, phi_jet, eta_gam, phi_gam)
                    if dR > 0.4: continue
                    prefiringprob_gam = getPrefiringRate(eta_gam, pt_gam, self.h_prefmap_photon, fluct,self.prefiringRateSystUnc_)
                    nonprefiringprobfromoverlappingphotons *= (1. - prefiringprob_gam)
                
                #// useEMpt = true if one wants to use maps parametrized vs Jet EM pt instead of pt.
                if self.useEMpt_ : 
                    pt_jet *= (jet.neutralEmEnergyFraction() + jet.chargedEmEnergyFraction())
                nonprefiringprobfromoverlappingjet = 1. - getPrefiringRate(eta_jet, pt_jet, self.h_prefmap_jet, fluct ,self.prefiringRateSystUnc_)

                if nonprefiringprobfromoverlappingphotons == 1. :
                    nonPrefiringProba[i] *= nonprefiringprobfromoverlappingjet
                
               
                # // If overlapping photons have a non prefiring rate larger than the jet, then replace these weights by the jet one
                elif nonprefiringprobfromoverlappingphotons > nonprefiringprobfromoverlappingjet:
                    if nonprefiringprobfromoverlappingphotons != 0. :
                        nonPrefiringProba[i] *= nonprefiringprobfromoverlappingjet / nonprefiringprobfromoverlappingphotons
                    else:
                        nonPrefiringProba[i] = 0.
        
        #print nonPrefiringProba
        event.prefiringweight = nonPrefiringProba[0]
        event.prefiringweightup = nonPrefiringProba[1]
        event.prefiringweightdown = nonPrefiringProba[2]
        
        pass
        return True
        
        
                #// Last case: if overlapping photons have a non prefiring rate smaller than the jet, don't consider the jet in the event weight, and do nothing.

setattr(PrefiringAnalyzer,"defaultConfig",cfg.Analyzer(
    class_object= PrefiringAnalyzer,
    L1Maps = 'L1PrefiringMaps.root',
    DataEra = "2017BtoF",
    UseJetEMPt = False ,
    PrefiringRateSystematicUncty =  0.2 , 
    SkipWarnings= True,
    )
)
