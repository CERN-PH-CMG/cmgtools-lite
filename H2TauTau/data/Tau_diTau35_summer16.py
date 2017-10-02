from CMGTools.H2TauTau.proto.weights.auxFunctions import crystalballEfficiency
from CMGTools.H2TauTau.proto.weights.tauh_trigger_effs import parameters
# global parameters


# https://github.com/rmanzoni/triggerSF/tree/moriond17/di-tau

def effData(pt, eta, dm, wp='Tight'):
    return crystalballEfficiency(pt, parameters['data_genuine_{wp}Iso_dm{dm}'.format(wp=wp, dm=dm)])

def effDataFakeTau(pt, eta, dm, wp='Tight'):
    return crystalballEfficiency(pt, parameters['data_fake_{wp}Iso_dm{dm}'.format(wp=wp, dm=dm)])

def effMC(pt, eta, dm, wp='Tight'):
    return crystalballEfficiency(pt, parameters['mc_genuine_{wp}Iso_dm{dm}'.format(wp=wp, dm=dm)])

def effMCFakeTau(pt, eta, dm, wp='Tight'):
    return crystalballEfficiency(pt, parameters['mc_genuine_{wp}Iso_dm{dm}'.format(wp=wp, dm=dm)])

if __name__ == '__main__':

    for pt in range(20, 200, 5):
        print 'pt %.2f\teff data %.3f\teff mc   %.3f\tdata/mc   %.2f' % (pt, effData(pt, 0., 0), effMC(pt, 0., 0), effData(pt, 0., 0) / effMC(pt, 0., 0))
        print 'pt %.2f\teff data %.3f\teff mc   %.3f\tdata/mc   %.2f' % (pt, effDataFakeTau(pt, 0., 10), effMC(pt, 0., 10), effData(pt, 0., 10) / effMC(pt, 0., 10))
