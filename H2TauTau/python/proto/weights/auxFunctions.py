import math
import ROOT
from scipy.stats import norm


def doubleGauss(x, par):
    x      = x[0]
    mu1    = par[0]
    sigma1 = par[1]
    scale1 = par[2]
    mu2    = par[3]
    sigma2 = par[4]
    scale2 = par[5]
    return _doubleGauss(x, mu1, sigma1, scale1, mu2, sigma2, scale2)


def doubleGaussSameMean(x, par):
    x      = x[0]
    mu     = par[0]
    sigma1 = par[1]
    scale1 = par[2]
    sigma2 = par[3]
    scale2 = par[4]
    return _doubleGauss(x, mu, sigma1, scale1, mu, sigma2, scale2)


def crystalball(x, par):
    x     = x[0]
    alpha = par[0]
    n     = par[1]
    mu    = par[2]
    sigma = par[3]
    scale = par[4]
    return _crystalball(x, alpha, n, mu, sigma, scale)


def doubleSidedCrystalball(x, par):
    x      = x[0]
    mu     = par[0] # common gaussian core
    sigma  = par[1] # common gaussian core

    alpha1 = par[2]
    n1     = par[3]
    scale1 = par[4]
    alpha2 = par[5]
    n2     = par[6]
    
    # impose continuity by joining the two halves at the gauss peak. 
    # Derivability comes for free. Thanks Carl Friedrich!
    scale2 = _crystalball(mu, alpha1, n1, mu, sigma, scale1) / _crystalball(mu, alpha2, n2, mu, sigma, 1.)

    if x > mu:
        if alpha1 < 0:
            return _crystalball(x, alpha1, n1, mu, sigma, scale1)
        elif alpha2 < 0:
            return _crystalball(x, alpha2, n2, mu, sigma, scale2)
        else: 
            raise ValueError('The two alpha paremters must have opposite sign!')
    elif x <= mu:
        if alpha1 > 0:
            return _crystalball(x, alpha1, n1, mu, sigma, scale1)
        elif alpha2 > 0:
            return _crystalball(x, alpha2, n2, mu, sigma, scale2)
        else: 
            raise ValueError('The two alpha paremters must have opposite sign!')


def crystalballEfficiency(x, par):
    if isinstance(par, dict):
        par = [par['m_{0}'], par['sigma'], par['alpha'], par['n'], par['norm']]
    # x     = x[0]
    m0    = par[0]
    sigma = par[1]
    alpha = par[2]
    n     = par[3]
    norm  = par[4]
    return _crystalballEfficiency( x, m0, sigma, alpha, n, norm )


def _doubleGauss(x, mu1, sigma1, scale1, mu2, sigma2, scale2):
    
    gaus1 = scale1 * norm(mu1, sigma1).pdf(x)
    gaus2 = scale2 * norm(mu2, sigma2).pdf(x)

    return gaus1 + gaus2


def _crystalballPositiveAlpha( x, alpha, n, mu, sigma):
    '''
    https://en.wikipedia.org/wiki/Crystal_Ball_function
    ''' 
    
    expArg = -0.5 * ROOT.TMath.Power(abs(alpha), 2.)
    gauss  = ROOT.TMath.Exp(expArg)
        
    A = ROOT.TMath.Power( (n/abs(alpha)), n) * gauss
    B = n / abs(alpha) - abs(alpha)
    C = n / (abs(alpha) * (n - 1.)) * gauss
    D = math.sqrt(math.pi/2.) * (1. + ROOT.TMath.Erf(abs(alpha)/math.sqrt(2.))) 
    N = 1. / (sigma * (C + D))

    pull = (x - mu)/sigma 
        
    if pull > -alpha:
        func = N * ROOT.TMath.Gaus(x, mu, sigma)
    else:
        func = N * A * ROOT.TMath.Power( (B - pull), -n )

    return func


def _crystalball( x, alpha, n, mu, sigma, scale ):
    
    if alpha > 0.:
        return scale * _crystalballPositiveAlpha( x, alpha, n, mu, sigma ) 
    else:
        x1     = 2 * mu - x
        alpha1 = -alpha
        return scale * _crystalballPositiveAlpha( x1, alpha1, n, mu, sigma ) 


def _crystalballEfficiency(m, m0, sigma, alpha, n, norm):
  
    sqrtPiOver2 = math.sqrt(ROOT.TMath.PiOver2())
    sqrt2       = math.sqrt(2.)
    sig         = abs(sigma)
    t           = (m - m0)/sig * alpha / abs(alpha)
    absAlpha    = abs(alpha/sig)
    a           = ROOT.TMath.Power(n/absAlpha, n) * ROOT.TMath.Exp(-0.5 * absAlpha * absAlpha)
    b           = absAlpha - n/absAlpha
    arg         = absAlpha / sqrt2;
  
    if   arg >  5.: ApproxErf =  1.
    elif arg < -5.: ApproxErf = -1.
    else          : ApproxErf = ROOT.TMath.Erf(arg)
  
    leftArea    = (1. + ApproxErf) * sqrtPiOver2
    rightArea   = ( a * 1./ROOT.TMath.Power(absAlpha-b, n-1) ) / (n - 1)
    area        = leftArea + rightArea
  
    if t <= absAlpha:
        arg = t / sqrt2
        if   arg >  5.: ApproxErf =  1.
        elif arg < -5.: ApproxErf = -1.
        else          : ApproxErf = ROOT.TMath.Erf(arg)
        return norm * (1 + ApproxErf) * sqrtPiOver2 / area
  
    else:
        return norm * (leftArea + a * (1/ROOT.TMath.Power(t-b,n-1) - \
                                       1/ROOT.TMath.Power(absAlpha - b,n-1)) / (1 - n)) / area
  
