from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle

class HBHENoiseFix( Analyzer ):

    
    def __init__(self, cfg_ana, cfg_comp, looperName ):
        super(HBHENoiseFix,self).__init__(cfg_ana,cfg_comp,looperName)

    #----------------------------------------
    # DECLARATION OF HANDLES OF LEPTONS STUFF   
    #----------------------------------------
        

    def declareHandles(self):
        super(HBHENoiseFix, self).declareHandles()

        #leptons
        self.handles['hcalNoise'] = AutoHandle("hcalnoise","HcalNoiseSummary")            

    def beginLoop(self, setup):
        super(HBHENoiseFix,self).beginLoop(setup)


    def hbheNoiseFilter(self,summary, minHPDHits=17, minHPDNoOtherHits=10, minZeros=99999, IgnoreTS4TS5ifJetInLowBVRegion=False):
        failCommon = (summary.maxHPDHits() >= minHPDHits  or
                      summary.maxHPDNoOtherHits() >= minHPDNoOtherHits or
                      summary.maxZeros() >= minZeros)
        goodJetFoundInLowBVRegion = False
        if IgnoreTS4TS5ifJetInLowBVRegion: goodJetFoundInLowBVRegion = summary.goodJetFoundInLowBVRegion();
        failRun2Loose = failCommon or (summary.HasBadRBXRechitR45Loose() and not goodJetFoundInLowBVRegion)
        return not failRun2Loose

    def hbheIsoNoiseFilter(self,summary):
        failIso = True
        if(summary.numIsolatedNoiseChannels() >=10): failIso=False
        if(summary.isolatedNoiseSumE() >=50) : failIso=False
        if(summary.isolatedNoiseSumEt() >=25): failIso=False
        return failIso


    def process(self, event):
        self.readCollections( event.input )
        noise = self.handles['hcalNoise'].product()
        event.HBHENoiseFilterFix=self.hbheNoiseFilter(noise, minZeros = 9e9,IgnoreTS4TS5ifJetInLowBVRegion=False)
        event.HBHENoiseIsoFilterFix=self.hbheIsoNoiseFilter(noise)
