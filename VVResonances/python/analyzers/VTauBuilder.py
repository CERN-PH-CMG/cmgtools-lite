from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer

from CMGTools.VVResonances.tools.Pair import Pair
from PhysicsTools.HeppyCore.utils.deltar import *
from CMGTools.VVResonances.tools.PyDiTauId import PyDiTauId
import itertools
import ROOT
class Substructure(object):
    def __init__(self):
        pass


class VTauBuilder(Analyzer):
    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(VTauBuilder,self).__init__(cfg_ana, cfg_comp, looperName)
        self.tauID=PyDiTauId()

    def copyLV(self,LV):
        out=[]
        for i in LV:
            out.append(ROOT.math.XYZTLorentzVector(i.px(),i.py(),i.pz(),i.energy()))
        return out    


    def substructure(self,jet):
        #if we already filled it exit
        if hasattr(jet,'substructure'):
            return
        
        constituents=[]
        LVs = ROOT.std.vector("math::XYZTLorentzVector")()

        for i in range(0,jet.numberOfDaughters()):
            if jet.daughter(i).numberOfDaughters()==0:
                if jet.daughter(i).pt()>13000 or jet.daughter(i).pt()==float('Inf'):
                    continue
                if hasattr(self.cfg_ana,"doPUPPI") and self.cfg_ana.doPUPPI and jet.daughter(i).puppiWeight()>0.0:                   
                    LVs.push_back(jet.daughter(i).p4()*jet.daughter(i).puppiWeight())
                else:
                    LVs.push_back(jet.daughter(i).p4())
            else:
                for j in range(0,jet.daughter(i).numberOfDaughters()):
                    if jet.daughter(i).daughter(j).pt()>13000 or jet.daughter(i).daughter(j).pt()==float('Inf'):
                        continue
                    if jet.daughter(i).daughter(j).numberOfDaughters()==0:
                        if hasattr(self.cfg_ana,"doPUPPI") and self.cfg_ana.doPUPPI and jet.daughter(i).daughter(j).puppiWeight()>0.0:
                            LVs.push_back(jet.daughter(i).daughter(j).p4()*jet.daughter(i).daughter(j).puppiWeight())
                        else:
                            LVs.push_back(jet.daughter(i).daughter(j).p4())
        
        interface = ROOT.cmg.FastJetInterface(LVs,-1.0,0.8,1,0.01,5.0,4.4)
        #make jets
        interface.makeInclusiveJets(0.0)
        
        outputJets = interface.get(True)
        if len(outputJets)==0:
            print 'NO RECLUSTERED JETS'
            return
        
        jet.substructure=Substructure()
        #OK!Now save the area
        jet.substructure.area=interface.getArea(1,0)
        #Get pruned lorentzVector and subjets
        interface.prune(True,0,0.1,0.5)       
        jet.substructure.prunedJet = self.copyLV(interface.get(False))[0]*jet.corr
        jet.substructure.softDropJet = self.copyLV(interface.get(False))[0]*jet.corr


    def makeTauTau(self,event,taus):
        output=[]
        #If two di-taus build pair
        taus=sorted(taus,key=lambda x: x.pt(),reverse=True)
        if len(taus)>1:
            VV=Pair(taus[0],taus[1])
            VV.LV=VV.LV+event.met.p4()
            output.append(VV)
        return output

    def makeTauJet(self,event,taus,jets):
        output=[]

        #If two di-taus build pair but you need a lepton!
        if len(taus)>0 and len(jets)>0:
            #since we trigger with lepton find taus that have a lepton
            tausWithLeptons=[]
            for t in taus:
                if t.nMuons+t.nElectrons>0:
                    leptonsOK=False
                    for c in t.signalConstituents:
                        if abs(c.pdgId()) ==11:
                            leptonsOK=True
                            break;
                        if abs(c.pdgId()) ==13:
                            leptonsOK=True
                            break;
                    if leptonsOK:
                        tausWithLeptons.append(t)
            
            if len(tausWithLeptons)==0:
                return output

            tau=max(tausWithLeptons,key=lambda x:x.pt())

            #cross clean jets
            crossCleanedJets = []
            for jet in jets:
                if deltaR(jet.eta(),jet.phi(),tau.eta(),tau.phi())>0.5:
                    if deltaPhi(jet.phi(),tau.phi())>0.5:
                        crossCleanedJets.append(jet)

            if len(crossCleanedJets)==0:
                return output;

            jet=max(crossCleanedJets,key=lambda x:x.pt())

            self.substructure(jet)
            if not hasattr(jet,'substructure'):
                print 'No substructure'
                return output
            VV=Pair(tau,jet)
            VV.LVWithMET=VV.LV+event.met.p4()
            output.append(VV)
        return output
      

    def process(self, event):


        #Take The jets
        jets= filter(lambda x: x.pt()>100.0 and abs(x.eta())<2.4,event.jets)       
        taus=[]




        looseTaus=[]
        looseJets=[]

        for j in jets:
            result = self.tauID.run(j)
            if not (result==None or (result.chargedIso+result.photonIso)/result.pt()>0.4):
                taus.append(result)
            if not (result==None or result.chargedIso/result.pt()>2):
                looseTaus.append(result)



        TauTau=self.makeTauTau(event,taus)
        TauJet =self.makeTauJet(event,taus,jets)
        TauTauLoose=self.makeTauTau(event,looseTaus)
        TauJetLoose =self.makeTauJet(event,looseTaus,jets)

        setattr(event,'TauTau'+self.cfg_ana.suffix,TauTau)
        setattr(event,'TauJet'+self.cfg_ana.suffix,TauJet)
        setattr(event,'TauTauLoose'+self.cfg_ana.suffix,TauTauLoose)
        setattr(event,'TauJetLoose'+self.cfg_ana.suffix,TauJetLoose)


