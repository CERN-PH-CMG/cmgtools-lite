from CMGTools.H2TauTau.proto.weights.auxFunctions import _crystalBallPlusStep, _definitePositiveErrorFunction

# global parameters

parameters = {}

parameters['tt_Fall15_76X_data'] = (
    3.45412e+01, # threshold
    5.63353e+00, # sigma
    2.49242e+00, # alpha
    3.35896e+00, # n
    1.00000e+00, # norm
)

parameters['tt_Fall15_76X_mc'] = (
    3.60274e+01, # threshold
    5.89434e+00, # sigma
    5.82870e+00, # alpha
    1.83737e+00, # n
    9.58000e-01, # norm
)

def effData(pt, eta):
    return _crystalBallPlusStep(pt, 
                                parameters['tt_Fall15_76X_data'][0], 
                                parameters['tt_Fall15_76X_data'][1], 
                                parameters['tt_Fall15_76X_data'][2], 
                                parameters['tt_Fall15_76X_data'][3], 
                                parameters['tt_Fall15_76X_data'][4])

def effMC(pt, eta):
    return _crystalBallPlusStep(pt, 
                                parameters['tt_Fall15_76X_mc'][0], 
                                parameters['tt_Fall15_76X_mc'][1], 
                                parameters['tt_Fall15_76X_mc'][2], 
                                parameters['tt_Fall15_76X_mc'][3], 
                                parameters['tt_Fall15_76X_mc'][4])

if __name__ == '__main__':

    for pt in range(0, 200, 5):
        print 'pt %.2f\teff data %.3f\teff mc   %.3f\tdata/mc   %.2f' %(pt, effData(pt, 0.), effMC(pt, 0.), effData(pt, 0.) / effMC(pt, 0.))
        
    
