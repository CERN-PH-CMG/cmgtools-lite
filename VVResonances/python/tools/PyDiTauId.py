from PhysicsTools.HeppyCore.utils.deltar import *
import itertools
import ROOT



class PyDiTau(object):
    def __init__(self,p4,q,signalConstituents,allConstituents,decayMode=0):
        self.LV = ROOT.math.XYZTLorentzVector(p4.px(),p4.py(),p4.pz(),p4.energy())
        self.signalConstituents=signalConstituents
        self.allConstituents=allConstituents
        self.decayMode=decayMode
        self.q=q
        self.leadMuonPt=0.0
        self.leadElectronPt=0.0

    def p4(self):
        return self.LV
        
    def setLegs(self,l1,l2):
        self.leg1 = ROOT.math.XYZTLorentzVector(l1)
        self.leg2 = ROOT.math.XYZTLorentzVector(l2)

    def charge(self):
        return self.q
    def calculateMembers(self):
        self.nPions=0
        self.nMuons=0
        self.nPosMuons=0
        self.nNegMuons=0
        self.nPosElectrons=0
        self.nNegElectrons=0
        self.nElectrons=0
        self.nPhotons=0
        self.chargedIso=0
        self.photonIso=0
        self.neutralIso=0

        self.isolationConstituents=list(set(self.allConstituents)-set(self.signalConstituents))


        for c in self.signalConstituents:
            if abs(c.pdgId())==211:
                self.nPions+=1
            elif abs(c.pdgId()) ==11:
                if c.pt()>self.leadElectronPt:
                    self.leadElectronPt=c.pt()
                self.nElectrons+=1
                if c.charge()>0:
                    self.nPosElectrons+=1
                else:
                    self.nNegElectrons+=1
                    
            elif abs(c.pdgId()) ==13:
                if c.pt()>self.leadMuonPt:
                    self.leadMuonPt=c.pt()
                self.nMuons+=1
                if c.charge()>0:
                    self.nPosMuons+=1
                else:
                    self.nNegMuons+=1

            elif abs(c.pdgId()) ==22:
                self.nPhotons+=1
               
        for c in self.isolationConstituents:
            if deltaR(c.eta(),c.phi(),self.LV.eta(),self.LV.phi())>0.5:
                continue;
            if c.charge()!=0:
                self.chargedIso=self.chargedIso+c.pt()
            elif c.pdgId()==22:
                self.photonIso=self.photonIso+c.pt()
            else:    
                self.neutralIso=self.neutralIso+c.pt()


    def __getattr__(self, name):
        if name =='physObj':
            return self
        return getattr(self.LV,name)


class Strip(object):
    def __init__(self,p4,constituents):
        self.constituents=constituents
        self.LV = ROOT.math.XYZTLorentzVector(p4.px(),p4.py(),p4.pz(),p4.energy())

    def p4(self):
        return self.LV

    def addPhoton(self,photon):
        self.LV=self.LV+photon.p4()
        self.constituents.append(photon)

    def __getattr__(self, name):
        if name =='physObj':
            return self
        return getattr(self.LV,name)


class PyDiTauId(object):
        
    def makeStrips(self,photons):
        ptSorted = sorted(photons, key=lambda x: x.pt(),reverse=True)
        strips=[]
        
        while len(photons)>0:
            strips.append(Strip(photons[0].p4(),[photons[0]]))
            photons.remove(photons[0])
            s=strips[-1]
            for p in photons:
                if deltaPhi(s.phi(),p.phi())<0.2 and abs(p.eta()-s.eta())<0.03:
                    s.addPhoton(p)
            for p in s.constituents:
                if p in photons:
                    photons.remove(p)        


        #Set the strip mass to zero
        for s in strips:
            s.LV.SetXYZT(s.px(),s.py(),s.pz(),math.sqrt(s.P()*s.P()+0.135*0.135))
        return strips                



        
    def run(self,jet,doLS=False):    
#        print 'Starting di-tau ID'
        combinatorics=[]

        constituents=[]        
        leptons=[]
        pions=[]
        photons=[]
        hadrons=[]
#        print 'Reading jet'
        for i in range(0,jet.numberOfDaughters()):
            if jet.daughter(i).numberOfDaughters()==0:
                particle=jet.daughter(i)
#                if abs(particle.pdgId())==13:
#                    print 'muon',particle.pdgId(),particle.pt()

                if particle.pt()>13000 or particle.pt()==float('Inf'):
                    continue
                constituents.append(particle)
                if abs(particle.pdgId()) in [11,13]:
                    leptons.append(particle)
                elif abs(particle.pdgId()) in [211]:
                    pions.append(particle)
                elif abs(particle.pdgId()) in [22]:
                    photons.append(particle)
                else:
                    hadrons.append(particle)
            else:
                for j in range(0,jet.daughter(i).numberOfDaughters()):
                    particle=jet.daughter(i).daughter(j)
#                    if abs(particle.pdgId())==13:
#                        print 'muon',particle.pdgId(),particle.pt()
                    if particle.pt()>13000 or particle.pt()==float('Inf'):
                        continue
                    constituents.append(particle)
                    if abs(particle.pdgId()) in [11,13]:
                        leptons.append(particle)
                    elif abs(particle.pdgId()) in [211]:
                        pions.append(particle)
                    elif abs(particle.pdgId()) in [22]:
                        photons.append(particle)
                    else:
                        hadrons.append(particle)





#        print 'Preparing to make strips'
        strips=self.makeStrips(photons)        

#        print 'reducing combinatorics'
        # 6 pions, two strips,2 leptons
        
        if len(strips)>2:
            s=sorted(strips,key=lambda x:x.pt(), reverse=True)
            strips=s[:2]

#        if len(leptons)>2:
#            s=sorted(leptons,key=lambda x:x.pt(), reverse=True)
#            leptons=s[:2]

        if len(pions)>6:
            s=sorted(pions,key=lambda x:x.pt(), reverse=True)
            pions=s[:6]

#        print 'Leptons in this jet=',len(leptons)    

        #combinatorial di-tau algorithm. start with 2 leptons
        if len(leptons)>=2:
            for l1,l2 in itertools.combinations(leptons,2):
#                print 'Two leptons,charge=',l1.charge()+l2.charge(),'pt',(l1.p4()+l2.p4()).pt()
                OS =l1.charge()+l2.charge()==0 
                if  OS or  (doLS and not OS) :
                    tau = PyDiTau(l1.p4()+l2.p4(),(l1.charge()+l2.charge()),[l1,l2],constituents,1)
                    tau.setLegs(l1.p4(),l2.p4())
                    combinatorics.append(tau)
#                    print 'made ll'
        elif len(leptons)>=1:
            for l in leptons:
                for pi in pions:
                    OS=l.charge()+pi.charge()==0
                    if OS or (doLS and not OS):
                        tau=PyDiTau(l.p4()+pi.p4(),(l.charge()+pi.charge()==0),[l,pi],constituents,2)
                        tau.setLegs(l.p4(),pi.p4())
                        combinatorics.append(tau) # lpi
#                        print 'made lpi'
                        for s in strips:
                            mass= (pi.p4()+s.p4()).M()
                            if mass>0.3 and mass<1.7:
                                tau=PyDiTau(l.p4()+pi.p4()+s.p4(),(l.charge()+pi.charge()==0),[l,pi]+s.constituents,constituents,3)
                                tau.setLegs(l.p4(),pi.p4()+s.p4())
                                combinatorics.append(tau) #l rho
#                                print 'made lrho'

                if len(pions)>2:        
                    for p1,p2,p3 in itertools.combinations(pions,3):
                        OS=(p1.charge()+p2.charge()+p3.charge()+l.charge())==0
                        if OS or (doLS and not OS):
                            mass=(p1.p4()+p2.p4()+p3.p4()).M()
                            if mass>0.5 and mass<1.7:
                                tau=PyDiTau(l.p4()+p1.p4()+p2.p4()+p3.p4(),(p1.charge()+p2.charge()+p3.charge()+l.charge()),[l,p1,p2,p3],constituents,4)
                                tau.setLegs(l.p4(),p1.p4()+p2.p4()+p3.p4())
                                combinatorics.append(tau)
#                                print 'made la1'
                                
        elif len(leptons)==0:
            if len(pions)>1:
                for p1,p2 in itertools.combinations(pions,2):
                    OS=p1.charge()+p2.charge()==0
                    if OS or(doLS and not OS):
                        tau=PyDiTau(p1.p4()+p2.p4(),p1.charge()+p2.charge(),[p1,p2],constituents,5)
                        tau.setLegs(p1.p4(),p2.p4())
                        combinatorics.append(tau) #pi+pi-
#                        print 'made pipi'
                        if len(strips)>0:    
                            for s in strips:
                                m1=(p1.p4()+s.p4()).M()
                                m2=(p2.p4()+s.p4()).M()
                                if m1>0.3 and m1<1.7 or m2>0.3 and m2<1.7:
                                    tau=PyDiTau(p1.p4()+p2.p4()+s.p4(),p1.charge()+p2.charge(),[p1,p2]+s.constituents,constituents,6)
                                    tau.setLegs(p1.p4(),p2.p4()+s.p4())
                                    combinatorics.append(tau) #pi+rho
#                                    print 'made pirho'
                                
                        if len(strips)>1:
                            masses1=[]
                            masses2=[]
                            for s1,s2 in itertools.combinations(strips,2):
                                m11=(p1.p4()+s1.p4()).M()
                                m12=(p2.p4()+s2.p4()).M()
                                m21=(p1.p4()+s2.p4()).M()
                                m22=(p2.p4()+s1.p4()).M()

                                if (m11>0.3 and m11<1.7 and m12>0.3 and m12<1.7):
                                    tau=PyDiTau(p1.p4()+p2.p4()+s1.p4()+s2.p4(),p1.charge()+p2.charge(),[p1,p2]+s1.constituents+s2.constituents,constituents,7)
                                    tau.setLegs(p1.p4()+s1.p4(),p2.p4()+s2.p4())
                                    combinatorics.append(tau)#rhorho
                                elif  (m21>0.3 and m21<1.7 and m22>0.3 and m22<1.7):     
                                    tau=PyDiTau(p1.p4()+p2.p4()+s1.p4()+s2.p4(),p1.charge()+p2.charge(),[p1,p2]+s1.constituents+s2.constituents,constituents,7)
                                    tau.setLegs(p2.p4()+s1.p4(),p1.p4()+s2.p4())
                                    combinatorics.append(tau)#rhorho

            if len(pions)>3:
                for p1,p2,p3,p4 in itertools.combinations(pions,4):
                    OS=(p1.charge()+p2.charge()+p3.charge()+p4.charge()==0)
                    if OS or (doLS and not OS):
                        for pp1,pp2,pp3 in itertools.combinations([p1,p2,p3,p4],3):
                            if abs(pp1.charge()+pp2.charge()+pp3.charge())==1:
                                m=(pp1.p4()+pp2.p4()+pp3.p4()).M()
                                if m>0.5 and m<1.7:
                                    tau=PyDiTau(p1.p4()+p2.p4()+p3.p4()+p4.p4(),p1.charge()+p2.charge()+p3.charge()+p4.charge(),[p1,p2,p3,p4],constituents,8)
                                    tau.setLegs(tau.p4()-(pp1.p4()+pp2.p4()+pp3.p4()),pp1.p4()+pp2.p4()+pp3.p4())
                                    combinatorics.append(tau)# pi+ a0
#                                    print 'made pi a1'

                                    break;
                        for s in strips:
                            for pp1,pp2,pp3,pp4 in itertools.permutations([p1,p2,p3,p4],4):                               
                                if abs(pp1.charge()+pp2.charge()+pp3.charge())==1:
                                    lv1=(pp1.p4()+pp2.p4()+pp3.p4())
                                    m1=lv1.M()
                                    if m1>0.5 and m1<1.7:
                                        lv2=pp4.p4()+s.p4()
                                        m2=lv2.M()
                                        if m2>0.3 and m2<1.7:
                                            tau=PyDiTau(p1.p4()+p2.p4()+p3.p4()+p4.p4()+s.p4(),p1.charge()+p2.charge()+p3.charge()+p4.charge(),[p1,p2,p3,p4]+s.constituents,constituents,9)
                                            tau.setLegs(lv1,lv2)
                                            combinatorics.append(tau)# rho a0
                                            break
                                

            if len(pions)>5:
                for p1,p2,p3,p4,p5,p6 in itertools.combinations(pions,6):
                    OS=p1.charge()+p2.charge()+p3.charge()+p4.charge()+p5.charge()+p6.charge()==0
                    if OS or (doLS and not OS):
                        for pp1,pp2,pp3,pp4,pp5,pp6 in itertools.permutations([p1,p2,p3,p4,p5,p6],6):
                            lv1=(p1.p4()+p2.p4()+p3.p4())
                            lv2=(p4.p4()+p5.p4()+p6.p4())
                            m1=lv1.M()
                            m2=lv2.M()
                            if m1>0.5 and m2>0.5 and m1<1.7 and m2<1.7:
                                tau=PyDiTau(p1.p4()+p2.p4()+p3.p4()+p4.p4()+p5.p4()+p6.p4(),p1.charge()+p2.charge()+p3.charge()+p4.charge()+p5.charge()+p6.charge(),[p1,p2,p3,p4,p5,p6],constituents,10)
                                tau.setLegs(lv1,lv2)
                                combinatorics.append(tau)
                                break;

                            
                            
                            
 
        if len(combinatorics)==0:
            return None
            #Now similarilly to the HPS take the most isolated

        bestTau = max(combinatorics,key=lambda x: x.pt())
        bestTau.calculateMembers()
        
        return bestTau

                





