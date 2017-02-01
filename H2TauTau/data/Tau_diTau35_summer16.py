from CMGTools.H2TauTau.proto.weights.auxFunctions import crystalballEfficiency
from CMGTools.H2TauTau.proto.weights.eff_ditauh35_tightMVAiso import parameters
# global parameters


# https://github.com/rmanzoni/triggerSF/tree/moriond17/di-tau

lumi_weight_bcdefg = 27916.0/36773.0
lumi_weight_h = (36773.0-27916.0)/36773.0

def effData(pt, eta, dm):
    if dm == 0:
        return lumi_weight_bcdefg * crystalballEfficiency(pt, parameters['Data BCDEFG decay mode =  0']) + lumi_weight_h *  crystalballEfficiency(pt, parameters['Data H decay mode =  0'])
    elif dm == 1:
        return lumi_weight_bcdefg * crystalballEfficiency(pt, parameters['Data BCDEFG decay mode =  1']) + lumi_weight_h *  crystalballEfficiency(pt, parameters['Data H decay mode =  1'])
    elif dm == 10:
        return lumi_weight_bcdefg * crystalballEfficiency(pt, parameters['Data BCDEFG decay mode = 10']) + lumi_weight_h * crystalballEfficiency(pt, parameters['Data H decay mode = 10'])
    
    raise RuntimeError('Unsupported decay mode', dm)

def effDataFakeTau(pt, eta, dm):
    return effData(pt, eta, dm)

def effMC(pt, eta, dm):
    if dm == 0:
        return crystalballEfficiency(pt, parameters['MC decay mode =  0'])
    elif dm == 1:
        return crystalballEfficiency(pt, parameters['MC decay mode =  1'])
    elif dm == 10:
        return crystalballEfficiency(pt, parameters['MC decay mode = 10'])

def effMCFakeTau(pt, eta, dm):
    return effMC(pt, eta, dm)

if __name__ == '__main__':

    for pt in range(20, 200, 5):
        print 'pt %.2f\teff data %.3f\teff mc   %.3f\tdata/mc   %.2f' % (pt, effData(pt, 0., 0), effMC(pt, 0., 0), effData(pt, 0., 0) / effMC(pt, 0., 0))
        print 'pt %.2f\teff data %.3f\teff mc   %.3f\tdata/mc   %.2f' % (pt, effDataFakeTau(pt, 0., 10), effMC(pt, 0., 10), effData(pt, 0., 10) / effMC(pt, 0., 10))
