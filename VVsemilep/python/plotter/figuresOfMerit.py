from math import sqrt

def _make_totals(mca, report, row=-1):
    tot_S, tot_B, tot_B_stat, tot_S_stat, tot_B_syst, tot_S_syst, data = 0, 0, 0, 0, 0, 0, 0
    for key,rep in report.iteritems():
        if key == 'data':
            data += rep[row][1][0]
        else:
            y = rep[row][1][0]
            y_stat = rep[row][1][1]
            y_syst = y * mca.getProcessOption(key,'NormSystematic',0.0) 
            if mca.isSignal(key):
                tot_S += y
                tot_S_stat += y_stat**2
                tot_S_syst += y_syst # note no ** 2 for signal syst
            else:
                tot_B += y
                tot_B_stat += y_stat**2
                tot_B_syst += y_syst**2 # note ** 2 for background syst
    return { 'S':(tot_S, sqrt(tot_S_stat), tot_S_syst), 'B':(tot_B, sqrt(tot_B_stat), sqrt(tot_B_syst)), 'D':data }

class S_over_B(object):
    def __init__(self, B_min=0.01):
        self.B_min = B_min
    def __call__(self, mca, report, row=-1):
        tots = _make_totals(mca, report, row)
        return tots['S'][0]/(max(tots['B'][0], self.B_min))

class S_over_Err(object):
    def __init__(self, Ws, Wb, Wsyst, B_min=0.01):
        self.Ws = Ws
        self.Wb = Wb
        self.Wsyst = Wsyst
        self.B_min = B_min
    def __call__(self, mca, report, row=-1):
        tots = _make_totals(mca, report, row)
        return tots['S'][0]/sqrt(
            self.Wb * (max(tots['B'][0], self.B_min) + self.Wsyst*(tots['B'][1]**2 + tots['B'][2]**2) ) +
            self.Ws * (    tots['S'][0]              + self.Wsyst*(tots['S'][1]**2 + tots['S'][2]**2) )  
        )

class Data_pull(object):
    def __init__(self, Ws, Wb=1, Wsyst=1, B_min=0.01):
        self.Ws = Ws
        self.Wb = Wb
        self.Wsyst = Wsyst
        self.B_min = B_min
    def __call__(self, mca, report, row=-1):
        tots = _make_totals(mca, report, row)
        return (tots['D'] - Ws*tots['S'][0] - self.Wb*tots['B'][0])/sqrt(
            self.Wb * (max(tots['B'][0], self.B_min) + self.Wsyst*(tots['B'][1]**2 + tots['B'][2]**2) ) +
            self.Ws * (    tots['S'][0]              + self.Wsyst*(tots['S'][1]**2 + tots['S'][2]**2) )  
        )

class Data_sf(object):
    def __init__(self, Ws=1, Wb=1):
        self.Ws = Ws
        self.Wb = Wb
    def __call__(self, mca, report, row=-1):
        tots = _make_totals(mca, report, row)
        totmc = self.Ws*tots['S'][0] + self.Wb*tots['B'][0]
        return (tots['D'] / totmc) if totmc > 0 else 1 


FOM_BY_NAME = {
    'S/B'    : S_over_B(),
    'S/sqB'  : S_over_Err(0,1,0),
    'S/sqSB' : S_over_Err(1,1,0),
    'S/errB' : S_over_Err(0,1,1),
    'S/errSB': S_over_Err(1,1,1),
    'pull_B':  Data_pull(0,1,1),
    'pull_S':  Data_pull(1,0,1),
    'pull_SB': Data_pull(1,1,1),
    'sf': Data_sf(1,1),
}
