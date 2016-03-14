from CMGTools.H2TauTau.proto.weights.auxFunctions import _crystalBallPlusStep, _definitePositiveErrorFunction

# global parameters

parameters = {}

parameters['tt_Fall15_76X_data_up'] = (
    3.31713e+01, # threshold
    5.66551e+00, # sigma
    1.87175e+00, # alpha
    8.07790e+00, # n
    1.00000e+00, # norm
)

parameters['tt_Fall15_76X_mc_down'] = (
    3.62436e+01, # threshold
    5.58461e+00, # sigma
    5.12924e+00, # alpha
    2.05921e+00, # n
    9.32305e-01, # norm
)

def effData(pt, eta):
    return _crystalBallPlusStep(pt, 
                                parameters['tt_Fall15_76X_data_up'][0], 
                                parameters['tt_Fall15_76X_data_up'][1], 
                                parameters['tt_Fall15_76X_data_up'][2], 
                                parameters['tt_Fall15_76X_data_up'][3], 
                                parameters['tt_Fall15_76X_data_up'][4])

def effMC(pt, eta):
    return _crystalBallPlusStep(pt, 
                                parameters['tt_Fall15_76X_mc_down'][0], 
                                parameters['tt_Fall15_76X_mc_down'][1], 
                                parameters['tt_Fall15_76X_mc_down'][2], 
                                parameters['tt_Fall15_76X_mc_down'][3], 
                                parameters['tt_Fall15_76X_mc_down'][4])

if __name__ == '__main__':

    for pt in range(0, 200, 5):
        print 'pt %.2f\teff data %.3f\teff mc   %.3f\tdata/mc   %.2f' %(pt, effData(pt, 0.), effMC(pt, 0.), effData(pt, 0.) / effMC(pt, 0.))
        
    
