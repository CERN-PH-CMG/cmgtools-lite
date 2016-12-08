class StitchingWeightForW(object):

    def __init__(self, Ninc=0, N1=0, N2=0, N3=0, N4=0):

        self.k_factor = 1.22125248
        self.sample_dict = {
            'WJetsToLNu_LO': {'LOxs': 50380},
            'W1JetsToLNu_LO': {'LOxs': 9644.5},
            'W2JetsToLNu_LO': {'LOxs': 3144.5},
            'W3JetsToLNu_LO': {'LOxs': 954.8},
            'W4JetsToLNu_LO': {'LOxs': 485.6},
        }

        self.eff_l_inc = Ninc/self.sample_dict['WJetsToLNu_LO']['LOxs']
        self.eff_l_1jet = N1/self.sample_dict['W1JetsToLNu_LO']['LOxs']
        self.eff_l_2jet = N2/self.sample_dict['W2JetsToLNu_LO']['LOxs']
        self.eff_l_3jet = N3/self.sample_dict['W3JetsToLNu_LO']['LOxs']
        self.eff_l_4jet = N4/self.sample_dict['W4JetsToLNu_LO']['LOxs']

        self.eff_l = [
            self.eff_l_1jet,
            self.eff_l_2jet,
            self.eff_l_3jet,
            self.eff_l_4jet
        ]

    def returnWeight(self, Nparton):

        if Nparton < 0 or Nparton > 4:
            print '[ERROR] Not correct Nparton'

        if Nparton == 0:
            return self.k_factor/self.eff_l_inc
        else:
            return self.k_factor/(self.eff_l_inc + self.eff_l[Nparton-1])


class StitchingWeightForDY(object):

    def __init__(self, Ninc=0, Ninc_ext=0, N1=0, N2=0, N3=0, N4=0, Nhigh=0):

        self.k_factor = 1.21622931

        self.sample_dict = {
            'DYJetsToLL_M50_LO': {'LOxs': 4954},
            'DY1JetsToLL_M50_LO': {'LOxs': 1012.5},
            'DY2JetsToLL_M50_LO': {'LOxs': 332.8},
            'DY3JetsToLL_M50_LO': {'LOxs': 101.8},
            'DY4JetsToLL_M50_LO': {'LOxs': 54.8},
            'DYJetsToTauTau_M150_LO': {'LOxs': 6.7}
        }

        self.eff_l_inc = Ninc/self.sample_dict['DYJetsToLNu_LO']['LOxs']
        self.eff_l_inc_ext = Ninc_ext/self.sample_dict['DYJetsToLNu_LO']['LOxs']
        self.eff_l_high = Nhigh/self.sample_dict['DYJetsToTauTau_M150_LO']['LOxs']
        self.eff_l_1jet = N1/self.sample_dict['DY1JetsToLNu_LO']['LOxs']
        self.eff_l_2jet = N2/self.sample_dict['DY2JetsToLNu_LO']['LOxs']
        self.eff_l_3jet = N3/self.sample_dict['DY3JetsToLNu_LO']['LOxs']
        self.eff_l_4jet = N4/self.sample_dict['DY4JetsToLNu_LO']['LOxs']

        self.eff_l = [
            self.eff_l_1jet,
            self.eff_l_2jet,
            self.eff_l_3jet,
            self.eff_l_4jet,
        ]

    def returnWeight(self, Nparton, Mass, Decay):

        if Nparton < 0 or Nparton > 4:
            print '[ERROR] Not correct Nparton'

        if Decay == 'TauTau':
            if Nparton == 0:
                if Mass < 150:
                    return self.k_factor/(self.eff_l_inc + self.eff_l_inc_ext)
                else:
                    return self.k_factor/(self.eff_l_inc + self.eff_l_inc_ext + self.eff_l_high)
            else:
                if Mass < 150:
                    return self.k_factor/(self.eff_l_inc + self.eff_l_inc_ext + self.eff_l[Nparton-1])
                else:
                    return self.k_factor/(self.eff_l_inc + self.eff_l_inc_ext + self.eff_l[Nparton-1] + self.eff_l_high)

        else:
            if Nparton == 0:
                return self.k_factor/(self.eff_l_inc + self.eff_l_inc_ext)
            else:
                return self.k_factor/(self.eff_l_inc + self.eff_l_inc_ext + self.eff_l[Nparton-1])
