import math

from itertools import combinations

from PhysicsTools.Heppy.physicsobjects.PhysicsObjects import Muon, Tau
from PhysicsTools.Heppy.physicsobjects.Electron import Electron
from ROOT import TVector3


class DiObject(object):

    def __init__(self, diobject):
        self.diobject = diobject
        #p4 = LorentzVector( 1,0,0,1)
        # self.diobject.setP4(p4)
        self.leg1Gen = None
        self.leg2Gen = None
        self.leg1DeltaR = -1
        self.leg2DeltaR = -1
        # JAN: this doesn't work with electrons - put into the derived classes
        # self.diobject.setP4(self.p4())
        
    def leg1(self):
        return self.daughter(0)

    def leg2(self):
        return self.daughter(1)

    def mass(self):
        return self.p4().mass()

    def pt(self):
        return self.p4().pt()

    def p4(self):
        return self.leg1().p4() + self.leg2().p4()
    
    def sumPt(self):
        '''pt_leg1 + pt_leg2. used for finding the best DiTau.'''
        return self.leg1().pt() + self.leg2().pt()

    def __getattr__(self, name):
        '''all accessors  from cmg::DiObject are transferred to this class.'''
        return getattr(self.diobject, name)

    def __str__(self):
        header = '{cls}: mvis={mvis}, sumpT={sumpt}'.format(
            cls=self.__class__.__name__,
            mvis=self.mass(),
            sumpt=self.sumPt())
        return '\n'.join([header,
                          '\t'+str(self.leg1()),
                          '\t'+str(self.leg2())])


class DiTau(DiObject):

    def __init__(self, diobject):
        super(DiTau, self).__init__(diobject)

    def met(self):
        return self.daughter(2)

    def svfitMass(self):
        return self.userFloat('mass')

    def svfitTransverseMass(self):
        return self.userFloat('transverseMass') if self.hasUserFloat('transverseMass') else -999.

    def svfitMassError(self):
        return self.userFloat('massUncert') if self.hasUserFloat('massUncert') else -999.

    def svfitPt(self):
        return self.userFloat('pt') if self.hasUserFloat('pt') else -999.

    def svfitPtError(self):
        return self.userFloat('ptUncert') if self.hasUserFloat('ptUncert') else -999.

    def svfitEta(self):
        return self.userFloat('fittedEta') if self.hasUserFloat('fittedEta') else -999.

    def svfitPhi(self):
        return self.userFloat('fittedPhi') if self.hasUserFloat('fittedPhi') else -999.

    def pZeta(self):
        if not hasattr(self, 'pZetaVis_'):
            self.calcPZeta()
        return self.pZetaVis_ + self.pZetaMET_

    def pZetaVis(self):
        if not hasattr(self, 'pZetaVis_'):
            self.calcPZeta()
        return self.pZetaVis_

    def pZetaMET(self):
        if not hasattr(self, 'pZetaMET_'):
            self.calcPZeta()
        return self.pZetaMET_

    def pZetaDisc(self):
        if not hasattr(self, 'pZetaVis_'):
            self.calcPZeta()
        return self.pZetaMET_ - 0.5*self.pZetaVis_

    # Calculate the pzeta variables with the same algorithm
    # as previously in the C++ DiObject class
    def calcPZeta(self):
        tau1PT = TVector3(self.leg1().p4().x(), self.leg1().p4().y(), 0.)
        tau2PT = TVector3(self.leg2().p4().x(), self.leg2().p4().y(), 0.)
        metPT = TVector3(self.met().p4().x(), self.met().p4().y(), 0.)
        zetaAxis = (tau1PT.Unit() + tau2PT.Unit()).Unit()
        self.pZetaVis_ = tau1PT*zetaAxis + tau2PT*zetaAxis
        self.pZetaMET_ = metPT*zetaAxis

    def mTLeg1(self):
        if hasattr(self, 'mt1'):
            return self.mt1
        else:
            self.mt1 = self.calcMT(self.leg1(), self.met())
            return self.mt1

    def mTLeg2(self):
        if hasattr(self, 'mt2'):
            return self.mt2
        else:
            self.mt2 = self.calcMT(self.leg2(), self.met())
            return self.mt2

    # This is the default transverse mass by convention
    def mt(self):
        return self.mTLeg2()

    def mtTotal(self):
        mt2 = self.mTLeg1()**2 + self.mTLeg2()**2 + self.calcMT(self.leg1(), self.leg2())**2
        return math.sqrt(mt2)

    def mtSumLeptons(self):
        return self.mTLeg1() + self.mTLeg2()

    def mtSqSumLeptons(self):
        return math.sqrt(self.mTLeg1()**2 + self.mTLeg2()**2)

    # Calculate the transverse mass with the same algorithm
    # as previously in the C++ DiObject class
    @staticmethod
    def calcMT(cand1, cand2):
        pt = cand1.pt() + cand2.pt()
        px = cand1.px() + cand2.px()
        py = cand1.py() + cand2.py()
        try:
            return math.sqrt(pt*pt - px*px - py*py)
        except ValueError:
            print 'Funny rounding issue', pt, px, py
            print cand1.px(), cand1.py(), cand1.pt()
            print cand2.px(), cand2.py(), cand2.pt()
            return 0.

    @staticmethod
    def calcMtTotal(cands):
        return math.sqrt(sum(DiObject.calcMT(c1, c2)**2 for c1, c2 in combinations(cands, 2)))


class DirectDiTau(DiTau):

    ''' A di-tau directly created from input leptons and MET.
    Does not have SVfit or MVA MET precalculated.
    '''

    def __init__(self, leg1, leg2, met):
        self.leg1_ = leg1
        self.leg2_ = leg2
        self.met_ = met
        self.p4_ = (leg1.p4() + leg2.p4())

    def mass(self):
        return self.p4_.mass()

    def p4(self):
        return self.p4_

    def leg1(self):
        return self.leg1_

    def leg2(self):
        return self.leg2_

    def met(self):
        return self.met_

    def svfitMass(self):
        return -999.

    def svfitTransverseMass(self):
        return -999.

    def svfitMassError(self):
        return -999.

    def svfitPt(self):
        return -999.

    def svfitPtError(self):
        return -999.

    def svfitEta(self):
        return -999.

    def svfitPhi(self):
        return -999.

    def __getattr__(self, name):
        '''Redefine getattr to original version.'''
        raise AttributeError


class DiMuon(DiTau):

    def __init__(self, diobject):
        super(DiMuon, self).__init__(diobject)
        self.mu1 = Muon(super(DiMuon, self).leg1())
        self.mu2 = Muon(super(DiMuon, self).leg2())
        self.diobject.setP4(self.p4())

    def leg2(self):
        return self.mu2

    def leg1(self):
        return self.mu1

    def __str__(self):
        header = 'DiMuon: mvis=%3.2f, sumpT=%3.2f' \
                 % (self.diobject.mass(),
                    self.sumPt())
        return '\n'.join([header])


class TauMuon(DiTau):

    def __init__(self, diobject):
        super(TauMuon, self).__init__(diobject)
        self.tau = Tau(super(TauMuon, self).leg1())
        self.mu = Muon(super(TauMuon, self).leg2())
        self.diobject.setP4(self.p4())

    def leg2(self):
        return self.tau

    def leg1(self):
        return self.mu


class TauElectron(DiTau):

    def __init__(self, diobject):
        super(TauElectron, self).__init__(diobject)
        self.tau = Tau(super(TauElectron, self).leg1())
        self.ele = Electron(super(TauElectron, self).leg2())
        self.diobject.setP4(self.p4())

    def leg2(self):
        return self.tau

    def leg1(self):
        return self.ele


class MuonElectron(DiTau):

    def __init__(self, diobject):
        super(MuonElectron, self).__init__(diobject)
        self.mu = Muon(super(MuonElectron, self).leg1())
        self.ele = Electron(super(MuonElectron, self).leg2())
        self.diobject.setP4(self.p4())

    def leg2(self):
        return self.mu

    def leg1(self):
        return self.ele


class DirectTauTau(DirectDiTau):

    def __init__(self, leg1, leg2, met):
        self.leg1_ = leg1 if leg1.pt() > leg2.pt() else leg2
        self.leg2_ = leg2 if leg1.pt() > leg2.pt() else leg1
        self.met_ = met
        self.p4_ = (leg1.p4() + leg2.p4())


class TauTau(DiTau):

    def __init__(self, diobject, iso='byIsolationMVArun2v1DBoldDMwLTraw'):
        super(TauTau, self).__init__(diobject)
        # if super(TauTau, self).leg1().tauID(iso) > super(TauTau, self).leg2().tauID(iso):
        if super(TauTau, self).leg1().pt() > super(TauTau, self).leg2().pt():
            self.tau = Tau(super(TauTau, self).leg1())
            self.tau2 = Tau(super(TauTau, self).leg2())
        else:
            self.tau = Tau(super(TauTau, self).leg2())
            self.tau2 = Tau(super(TauTau, self).leg1())
        self.iso = iso
        self.diobject.setP4(self.p4())

    def leg1(self):
        return self.tau

    def leg2(self):
        return self.tau2
