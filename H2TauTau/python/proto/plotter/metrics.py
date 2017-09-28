from __future__ import division
import math

# AMS - approximate median significance

def ams(s, b, b_e=0.):
    if s == 0.:
        return 0.
    if b <= 0.:
        print 'No background but signal,', s, ' in AMS calculation; returning 0'
        # return float('nan')
        return 0.
    if b_e > 0.:
        return ams_cowan(s, b, b_e)

    val = 2*((s + b)*math.log(1 + s/b) - s)
    if val < 0.:
        print 'Getting negative temp value in ams calculation', val
        return 0.
    return math.sqrt(val)


def ams_cowan(s, b, b_e=0.0000000001):
    # https://indico.cern.ch/event/316800/attachments/608567/837395/cern.pdf#page=94
    b_zero = 0.5*(b - b_e**2 + math.sqrt((b - b_e**2)**2 + 4*(s + b)*b_e**2))

    ams = math.sqrt(2*((s+b)*math.log((s+b)/b_zero) - s - b + b_zero) + ((b - b_zero)**2)/(b_e**2))
    return ams

def squaresum(values):
    return math.sqrt(sum(v**2 for v in values))

def ams_lists(s_list, b_list, b_e=0.):
    return squaresum([ams(s, b, b_e) for s, b in zip(s_list, b_list)])

def ams_hists(s_hist, b_hist, b_e=0.):
    return ams_lists(th1_to_list(s_hist), th1_to_list(b_hist), b_e)

def ams_hists_rebin(s_hist, b_hist, max_rel_error=0.5, b_e=0., debug=False):
    for i in reversed(xrange(b_hist.GetNbinsX())):
        if i > 1 and (b_hist.GetBinContent(i) <= 0. or b_hist.GetBinError(i)/b_hist.GetBinContent(i) > 0.5):

            b_hist.SetBinContent(i-1, b_hist.GetBinContent(i) + b_hist.GetBinContent(i-1))
            b_hist.SetBinError(i-1, math.sqrt(b_hist.GetBinError(i)**2 + b_hist.GetBinError(i-1)**2))
            b_hist.SetBinContent(i, 0.)
            b_hist.SetBinError(i, 0.)

            s_hist.SetBinContent(i-1, s_hist.GetBinContent(i) + s_hist.GetBinContent(i-1))
            s_hist.SetBinError(i-1, math.sqrt(s_hist.GetBinError(i)**2 + s_hist.GetBinError(i-1)**2))
            s_hist.SetBinContent(i, 0.)
            s_hist.SetBinError(i, 0.)

    if debug:
        print th1_to_list(s_hist)
        print th1_to_list(b_hist)
    return ams_lists(th1_to_list(s_hist), th1_to_list(b_hist), b_e)

def th1_to_list(hist):
    return [hist.GetBinContent(i+1) for i in xrange(hist.GetNbinsX())]

if __name__ == '__main__':
    print 's=2, b=2', ams(2, 2)
    print 's=2, b=2', ams_cowan(2, 2)
    print 's=2, b=2, b_e=1', ams_cowan(2, 2, 1)
    print 'Additive?', squaresum([ams(1, 1), ams(1, 1)])
    print 'Change background levels', squaresum([ams(1, 1.5), ams(1, 0.5)])
    print 'Use lists', ams_lists([1, 1], [1.5, 0.5])

    print 's=20, b=20', ams(20, 20)
    print 'Additive?', squaresum([ams(10, 10), ams(10, 10)])
    print 'Change background levels', squaresum([ams(10, 15), ams(10, 5)])
    print 'Use lists', ams_lists([10, 10], [15, 5])