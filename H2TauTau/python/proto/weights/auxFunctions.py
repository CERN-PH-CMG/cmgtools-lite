import math
import ROOT

def _crystalBallPositiveAlpha( x, alpha, n, mu, sigma):
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


def _crystalBall( x, alpha, n, mu, sigma, scale ):
    '''
    Generalised Crystal Ball function.
    The parameter alpha sets which side of the gaussian bulk
    the polinomial tail is attached to.
    '''
    
    if alpha > 0.:
        return scale * _crystalBallPositiveAlpha( x, alpha, n, mu, sigma ) 
    else:
        x1     = 2 * mu - x
        alpha1 = -alpha
        return scale * _crystalBallPositiveAlpha( x1, alpha1, n, mu, sigma ) 


def crystalBall(x, par):
    '''
    Function to be used as FCN in ROOT TH1 Fit method
    '''
    x     = x[0]
    alpha = par[0]
    n     = par[1]
    mu    = par[2]
    sigma = par[3]
    scale = par[4]
    return _crystalball(x, alpha, n, mu, sigma, scale)


def _crystalBallPlusStep(m, m0, sigma, alpha, n, norm):
    '''
    Approximate convolution of a Crystal Ball resolution 
    with a Heaviside step function.
    Used for trigger efficiency turn on curves.
    '''
  
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


def crystalBallPlusStep(x, par):
    '''
    Function to be used as FCN in ROOT TH1 Fit method
    '''
    x     = x[0]
    m0    = par[0]
    sigma = par[1]
    alpha = par[2]
    n     = par[3]
    norm  = par[4]
    return _crystalBallPlusStep( x, m0, sigma, alpha, n, norm )


def _definitePositiveErrorFunction(pt, threshold, resolution, plateau):
    '''
    Positive-definite error function.
    Corresponds to the convolution of a normal distribution with 
    a Heaviside step function.
    '''
    return 0.5 * (plateau * ROOT.TMath.Erf((pt-threshold)/resolution) + 1.)


def definitePositiveErrorFunction(x, par):
    '''
    Function to be used as FCN in ROOT TH1 Fit method
    '''
    pt         = x[0]
    threshold  = par[0]
    resolution = par[1]
    plateau    = par[2]

    return _definitePositiveErrorFunction( pt, threshold, resolution, plateau )


def _ErrorFunction(pt, threshold, resolution, plateau):
    '''
    Error function (can go negative).
    Corresponds to the convolution of a normal distribution with 
    a Heaviside step function.
    '''
    return plateau * ROOT.TMath.Erf((pt-threshold)/resolution)


def ErrorFunction(x, par):
    '''
    Function to be used as FCN in ROOT TH1 Fit method
    '''
    pt         = x[0]
    threshold  = par[0]
    resolution = par[1]
    plateau    = par[2]

    return _ErrorFunction( pt, threshold, resolution, plateau )



