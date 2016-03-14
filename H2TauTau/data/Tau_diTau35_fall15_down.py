from CMGTools.H2TauTau.proto.weights.auxFunctions import _crystalBallPlusStep, _definitePositiveErrorFunction

# global parameters

parameters = {}

parameters['tt_Fall15_76X_data_down'] = (
    3.56264e+01, # threshold
    5.30711e+00, # sigma
    2.81591e+00, # alpha
    2.40649e+00, # n
    9.99958e-01, # norm
)

parameters['tt_Fall15_76X_mc_up'] = (
    3.56012e+01, # threshold
    5.97209e+00, # sigma
    6.09604e+00, # alpha
    1.68740e+00, # n
    9.87653e-01, # norm
)

def effData(pt, eta):
    return _crystalBallPlusStep(pt, 
                                parameters['tt_Fall15_76X_data_down'][0], 
                                parameters['tt_Fall15_76X_data_down'][1], 
                                parameters['tt_Fall15_76X_data_down'][2], 
                                parameters['tt_Fall15_76X_data_down'][3], 
                                parameters['tt_Fall15_76X_data_down'][4])

def effMC(pt, eta):
    return _crystalBallPlusStep(pt, 
                                parameters['tt_Fall15_76X_mc_up'][0], 
                                parameters['tt_Fall15_76X_mc_up'][1], 
                                parameters['tt_Fall15_76X_mc_up'][2], 
                                parameters['tt_Fall15_76X_mc_up'][3], 
                                parameters['tt_Fall15_76X_mc_up'][4])

if __name__ == '__main__':

    for pt in range(0, 200, 5):
        print 'pt %.2f\teff data %.3f\teff mc   %.3f\tdata/mc   %.2f' %(pt, effData(pt, 0.), effMC(pt, 0.), effData(pt, 0.) / effMC(pt, 0.))
        
    
