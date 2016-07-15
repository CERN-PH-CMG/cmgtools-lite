from CMGTools.H2TauTau.proto.weights.auxFunctions import crystalballEfficiency

# global parameters

parameters = {}

# 2.1 fb-1 
# https://indico.cern.ch/event/544712/contributions/2213574/attachments/1295299/1930984/htt_tau_trigger_17_6_2016.pdf

parameters['tt_Spring16_80X_data_vtight'] = (
    3.77850E+01,  # m0
    4.93611E+00,  # sigma
    4.22634E+00,  # alpha
    2.85533E+00,  # n
    9.92196E-01,  # norm
)

parameters['tt_Spring16_80X_data_fakes_vtight'] = (
    3.92867E+01,  # m0
    7.22249E+00,  # sigma
    1.14726E+01,  # alpha
    1.32792E+00,  # n
    1.00000e+00,  # norm
)

def effData(pt, eta):
    return crystalballEfficiency(pt, parameters['tt_Spring16_80X_data_vtight'])

def effDataFakeTau(pt, eta):
    return crystalballEfficiency(pt, parameters['tt_Spring16_80X_data_fakes_vtight'])

def effMC(pt, eta):
    return 1.

def effMCFakeTau(pt, eta):
    return 1.

if __name__ == '__main__':

    for pt in range(0, 200, 5):
        print 'pt %.2f\teff data %.3f\teff mc   %.3f\tdata/mc   %.2f' % (pt, effData(pt, 0.), effMC(pt, 0.), effData(pt, 0.) / effMC(pt, 0.))
        print 'pt %.2f\teff data %.3f\teff mc   %.3f\tdata/mc   %.2f' % (pt, effDataFakeTau(pt, 0.), effMC(pt, 0.), effData(pt, 0.) / effMC(pt, 0.))
