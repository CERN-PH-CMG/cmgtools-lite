from PhysicsTools.HeppyCore.utils.deltar import *
import PhysicsTools.HeppyCore.framework.config as cfg
from  itertools import combinations
from CMGTools.VVResonances.tools.Pair import *
from copy import copy
import ROOT


class VectorBosonToolBox(object):

    def WMuNuPFIsolation(self,z):#does nothing / for common interface
       footPrintLeg1=0.0
       cleanedChargedIso = max(z.leg1.pfIsolationR04().sumChargedHadronPt,0.0)
       cleanedNeutralIsoDB=max( z.leg1.neutralHadronIso(0.4)+z.leg1.photonIso(0.4)-z.leg1.puChargedHadronIso(0.4)/2, 0.0)
       return (cleanedChargedIso+cleanedNeutralIsoDB)/z.leg1.pt()<0.2



    def ZMuMuPFIsolation(self,z):
        footPrintLeg1=0.0
        footPrintLeg2=0.0
        dr=deltaR(z.leg1.eta(),z.leg1.phi(),z.leg2.eta(),z.leg2.phi())
        if dr<0.4 and not z.leg2.isPFMuon():
            footPrintLeg1=z.leg2.pt()
        if dr<0.4 and not z.leg1.isPFMuon():
            footPrintLeg2=z.leg2.pt()

        cleanedChargedIso1 = max(z.leg1.pfIsolationR04().sumChargedHadronPt-footPrintLeg1,0.0)
        cleanedChargedIso2 = max(z.leg2.pfIsolationR04().sumChargedHadronPt-footPrintLeg2,0.0)
        cleanedNeutralIsoDB1=max( z.leg1.neutralHadronIso(0.4)+z.leg1.photonIso(0.4)-z.leg1.puChargedHadronIso(0.4)/2, 0.0)
        cleanedNeutralIsoDB2=max( z.leg2.neutralHadronIso(0.4)+z.leg2.photonIso(0.4)-z.leg2.puChargedHadronIso(0.4)/2, 0.0)

        return (cleanedChargedIso1+cleanedNeutralIsoDB1)/z.leg1.pt()<0.4 and (cleanedChargedIso2+cleanedNeutralIsoDB2)/z.leg2.pt()<0.4



    def WENuPFIsolation(self,z):
        footPrintChargedLeg1=0.0
        footPrintNeutralLeg1=0.0

        if not z.leg1.isPF():
            for i in range(0,z.leg1.associatedPackedPFCandidates().size()):
                c=z.leg1.associatedPackedPFCandidates()[i]
                dr = deltaR(z.leg1.eta(),z.leg1.phi(),c.eta(),c.phi())
                if z.leg1.isEB() or (dr>0.08 and dr<0.4):
                    if c.charge()>0:
                        footPrintChargedLeg1=footPrintChargedLeg1+c.pt()
                    else:
                        footPrintNeutralLeg1=footPrintNeutralLeg1+c.pt()

        cleanedChargedIso = max(z.leg1.chargedHadronIso(0.4)-footPrintChargedLeg1,0.0)
        cleanedNeutralIsoRho=max(z.leg1.neutralHadronIso(0.4)+z.leg1.photonIso(0.4)-footPrintNeutralLeg1-z.leg1.rho*z.leg1.EffectiveArea04,0)
        return (cleanedChargedIso + cleanedNeutralIsoRho)/z.leg1.pt()<0.2



    def ZEEPFIsolation(self,z):
        footPrintChargedLeg1=0.0
        footPrintChargedLeg2=0.0
        footPrintNeutralLeg1=0.0
        footPrintNeutralLeg2=0.0

        if not z.leg1.isPF():

            for i in range(0,z.leg1.associatedPackedPFCandidates().size()):
                c=z.leg1.associatedPackedPFCandidates()[i]
                dr = deltaR(z.leg1.eta(),z.leg1.phi(),c.eta(),c.phi())
                if z.leg1.isEB() or (dr>0.08 and dr<0.4):
                    if c.charge()>0:
                        footPrintChargedLeg1=footPrintChargedLeg1+c.pt()
                    else:
                        footPrintNeutralLeg1=footPrintNeutralLeg1+c.pt()
                dr = deltaR(z.leg2.eta(),z.leg2.phi(),c.eta(),c.phi())
                if z.leg2.isEB() or (dr>0.08 and dr<0.4):
                    if c.charge()>0:
                        footPrintChargedLeg2=footPrintChargedLeg2+c.pt()
                    else:
                        footPrintNeutralLeg2=footPrintNeutralLeg2+c.pt()

        if not z.leg2.isPF():
            for i in range(0,z.leg2.associatedPackedPFCandidates().size()):
                c=z.leg2.associatedPackedPFCandidates()[i]
                dr = deltaR(z.leg2.eta(),z.leg2.phi(),c.eta(),c.phi())
                if z.leg2.isEB() or (dr>0.08 and dr<0.4):
                    if c.charge()>0:
                        footPrintChargedLeg2=footPrintChargedLeg2+c.pt()
                    else:
                        footPrintNeutralLeg2=footPrintNeutralLeg2+c.pt()
                dr = deltaR(z.leg1.eta(),z.leg1.phi(),c.eta(),c.phi())
                if z.leg1.isEB() or (dr>0.08 and dr<0.4):
                    if c.charge()>0:
                        footPrintChargedLeg1=footPrintChargedLeg1+c.pt()
                    else:
                        footPrintNeutralLeg1=footPrintNeutralLeg1+c.pt()


        cleanedChargedIso1 = max(z.leg1.chargedHadronIso(0.4)-footPrintChargedLeg1,0.0)
        cleanedChargedIso2 = max(z.leg1.chargedHadronIso(0.4)-footPrintChargedLeg2,0.0)
        cleanedNeutralIsoRho1=max(z.leg1.neutralHadronIso(0.4)+z.leg1.photonIso(0.4)-footPrintNeutralLeg1-z.leg1.rho*z.leg1.EffectiveArea04,0)
        cleanedNeutralIsoRho2=max(z.leg2.neutralHadronIso(0.4)+z.leg2.photonIso(0.4)--footPrintNeutralLeg2-z.leg2.rho*z.leg2.EffectiveArea04,0)

        return (cleanedChargedIso1+cleanedNeutralIsoRho1)/z.leg1.pt()<0.4 and (cleanedChargedIso2+cleanedNeutralIsoRho2)/z.leg2.pt()<0.4

    def ZIsolation(self,z):
        if abs(z.leg1.pdgId())==11:
            return self.ZEEPFIsolation(z)
        else:
            return self.ZMuMuPFIsolation(z)


    def simpleWKinematicFit(self,pair):
        MW=80.390

        muonLV = ROOT.TLorentzVector(pair.leg1.px(),pair.leg1.py(),pair.leg1.pz(),pair.leg1.energy())
        metLV = ROOT.TLorentzVector(pair.leg2.px(),pair.leg2.py(),pair.leg2.pz(),pair.leg2.energy())

        #go to the rest frame of a muon
        muonBoost = ROOT.TVector3(0.0,0.0,-muonLV.BoostVector().Z())

        muonLV.Boost(muonBoost)
        metLV.Boost(muonBoost)

        u = (MW*MW+2*muonLV.Px()*metLV.Px()+2*muonLV.Py()*metLV.Py())/(2*muonLV.Energy())
        u=u*u-metLV.Px()*metLV.Px()-metLV.Py()*metLV.Py()
        if u<0.0:
            pair.alternateLV=pair.LV
            return


        #First solution
        metLV2 = ROOT.TLorentzVector(metLV)

        metLV.SetPxPyPzE(metLV.Px(),metLV.Py(),-math.sqrt(u),math.sqrt(metLV.Px()*metLV.Px()+metLV.Py()*metLV.Py()+u))
        metLV2.SetPxPyPzE(metLV.Px(),metLV.Py(),math.sqrt(u),math.sqrt(metLV.Px()*metLV.Px()+metLV.Py()*metLV.Py()+u))

        muonLV.Boost(-muonBoost)
        metLV.Boost(-muonBoost)
        metLV2.Boost(-muonBoost)

#        print 'Muon Z',muonLV.Pz() , 'METz 1',metLV.Pz(),'METz2',metLV2.Pz(),'Delta1',abs(muonLV.Pz()-metLV.Pz()),'Delta2',abs(muonLV.Pz()-metLV2.Pz()),math.cos(muonLV.Angle(metLV.Vect())),'Angles',math.cos(muonLV.Angle(metLV.Vect())),math.cos(muonLV.Angle(metLV2.Vect()))


#        W1=metLV+muonLV
#        W2=metLV2+muonLV

        p2 =pair.leg2.p4()
        p2.SetPxPyPzE(metLV.Px(),metLV.Py(),metLV.Pz(),metLV.Energy())
        if abs(metLV2.Pz())>abs(metLV.Pz()):
            pair.LV = pair.leg1.p4()+p2
            p2.SetPxPyPzE(metLV2.Px(),metLV2.Py(),metLV2.Pz(),metLV2.Energy())
            pair.alternateLV = pair.leg1.p4()+p2
            p2.SetPxPyPzE(metLV.Px(),metLV.Py(),0.0,math.sqrt(metLV.Px()*metLV.Px()+metLV.Py()*metLV.Py()))
        else:
            pair.alternateLV = pair.leg1.p4()+p2
            p2.SetPxPyPzE(metLV2.Px(),metLV2.Py(),metLV2.Pz(),metLV2.Energy())
            pair.LV = pair.leg1.p4()+p2
            p2.SetPxPyPzE(metLV.Px(),metLV.Py(),0.0,math.sqrt(metLV.Px()*metLV.Px()+metLV.Py()*metLV.Py()))



    def defaultWKinematicFit(self,pair):
        MW=80.390

        muonLV = ROOT.TLorentzVector(pair.leg1.px(),pair.leg1.py(),pair.leg1.pz(),pair.leg1.energy())
        metLV = ROOT.TLorentzVector(pair.leg2.px(),pair.leg2.py(),pair.leg2.pz(),pair.leg2.energy())


        MET2 = metLV.Pt()*metLV.Pt()
        R = (0.5*(MW*MW+muonLV.Px()*metLV.Px()+muonLV.Py()*metLV.Py()))/muonLV.E();

        A = (muonLV.Pz()*muonLV.Pz())/(muonLV.P()*muonLV.P())-1;
        B = 2*R*muonLV.Pz()/muonLV.P();
        C = R*R-metLV.Pt()*metLV.Pt();

        D = B*B-4*A*C;


        if D>0:
            pz1=(-B+math.sqrt(D))/(2*A)
            pz2=(-B-math.sqrt(D))/(2*A)
            if abs(pz1)<abs(pz2):
                pp1 =pair.leg2.p4()
                pp1.SetPxPyPzE(metLV.Px(),metLV.Py(),pz1,math.sqrt(MET2+pz1*pz1))
                pair.LV=pair.leg1.p4()+pp1
                pp2 =pair.leg2.p4()
                pp2.SetPxPyPzE(metLV.Px(),metLV.Py(),pz2,math.sqrt(MET2+pz2*pz2))
                pair.alternateLV=pair.leg1.p4()+pp2
            else:
                pp2 =pair.leg2.p4()
                pp2.SetPxPyPzE(metLV.Px(),metLV.Py(),pz1,math.sqrt(MET2+pz1*pz1))
                pair.alternateLV=pair.leg1.p4()+pp2
                pp1 =pair.leg2.p4()
                pp1.SetPxPyPzE(metLV.Px(),metLV.Py(),pz2,math.sqrt(MET2+pz2*pz2))
                pair.LV=pair.leg1.p4()+pp1

        else:
            pz=-B/(2*A)
            pp =pair.leg2.p4()
            pp.SetPxPyPzE(metLV.Px(),metLV.Py(),pz,math.sqrt(MET2+pz*pz))
            pair.LV=pair.leg1.p4()+pp
            pair.alternateLV=pair.LV

    def reconstructLeptonicW(self, pair):
        MW = 80.390

        muonLV = ROOT.TLorentzVector(pair.leg1.px(), pair.leg1.py(), pair.leg1.pz(), pair.leg1.energy())
        metLV = ROOT.TLorentzVector(pair.leg2.px(), pair.leg2.py(), pair.leg2.pz(), pair.leg2.energy())

        MET2 = metLV.Pt()*metLV.Pt()

        R = MW*MW + 2*muonLV.Px()*metLV.Px() + 2*muonLV.Py()*metLV.Py()
        A = 4.0*(muonLV.E()*muonLV.E() - muonLV.Pz()*muonLV.Pz())
        B = -4.0*R*muonLV.Pz()
        C = 4.0*muonLV.E()*muonLV.E()*MET2 - R*R
        D = B*B - 4.0*A*C

        pz1 = 0.
        pz2 = 0.
        # newPtneutrino1 = 0
        # newPtneutrino2 = 0

        if D < 0:
            pz1 = -B/(2*A)
            pz2 = pz1
            # recalculate the neutrino pT
            # solve quadratic eq. discriminator = 0 for pT of nu
            # pnu = metLV.Pt()
            # Delta = MW*MW
            # alpha = (muonLV.Px()*metLV.Px()/pnu + muonLV.Py()*metLV.Py()/pnu)
            # ptnu = math.sqrt(MET2)
            # AA = 4.*muonLV.Pz()*muonLV.Pz() - 4*muonLV.E()*muonLV.E() + 4*alpha*alpha
            # BB = 4.*alpha*Delta
            # CC = Delta*Delta
            # tmpdisc = BB*BB - 4.0*AA*CC
            # tmpsolpt1 = (-BB + math.sqrt(tmpdisc))/(2.0*AA)
            # tmpsolpt2 = (-BB - math.sqrt(tmpdisc))/(2.0*AA)
            # if (abs(tmpsolpt1 - ptnu) < abs(tmpsolpt2 - ptnu)):
            #     newPtneutrino1 = tmpsolpt1
            #     newPtneutrino2 = tmpsolpt2
            # else:
            #     newPtneutrino1 = tmpsolpt2
            #     newPtneutrino2 = tmpsolpt1
        else:
            tmpsol1 = (-B + math.sqrt(D))/(2.0*A)
            tmpsol2 = (-B - math.sqrt(D))/(2.0*A)
            # pick the most central root
            if (abs(tmpsol1) < abs(tmpsol2)):
                pz1 = tmpsol1
                pz2 = tmpsol2
            else:
                pz1 = tmpsol2
                pz2 = tmpsol1

        pp1 = pair.leg2.p4()
        pp1.SetPxPyPzE(metLV.Px(), metLV.Py(), pz1, math.sqrt(MET2+pz1*pz1))
        pair.LV = pair.leg1.p4()+pp1
        pp2 = pair.leg2.p4()
        pp2.SetPxPyPzE(metLV.Px(), metLV.Py(), pz2, math.sqrt(MET2+pz2*pz2))
        pair.alternateLV = pair.leg1.p4()+pp2


    def makeZ(self,leptonList):
        output=[]
        for l1,l2 in combinations(leptonList,2):
            if  (l1.pdgId() == -l2.pdgId()):
                pair = Pair(l1,l2,23)
                m=pair.p4().mass()
                isMU = abs(l1.pdgId())==13
                if l1.pt()>l2.pt():
                    leading=l1
                    subleading=l2
                else:
                    leading=l2
                    subleading=l1
                if isMU:
                    ID = (l1.highPtID and l2.highPtID) or (l1.highPtID and l2.highPtTrackID ) or (l2.highPtID and l1.highPtTrackID )
                else:
                    ID=True

                if m>70.0 and m<110.0 and ID and self.ZIsolation(pair) and pair.p4().pt()>200.0 and ((isMU and leading.pt()>50 and abs(leading.eta())<2.1) or ((not isMU) and leading.pt()>115 )):
                    output.append(pair)
        return output


    def makeW(self,leptonList,MET):
        output=[]
        for l1 in leptonList:
            pair = Pair(l1,MET,l1.charge()*24)
            self.reconstructLeptonicW(pair)
            if  pair.pt()>200.0 and ((abs(l1.pdgId())==13 and MET.pt()>40) or (abs(l1.pdgId())==11 and MET.pt()>80)) :
                output.append(pair)
        return output
