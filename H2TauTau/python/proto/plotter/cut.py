import copy


class Cut(object):

    def __init__(self, cutstr):
        self.cutstr = cutstr

    def __and__(self, other):
        newone = copy.deepcopy(self)
        newone.cutstr = '({cut1}) && ({cut2})'.format(cut1=str(self), cut2=str(other))
        return newone

    def __or__(self, other):
        newone = copy.deepcopy(self)
        newone.cutstr = '(({cut1}) || ({cut2}))'.format(cut1=str(self), cut2=str(other))
        return newone

    def __str__(self):
        return self.cutstr
    
    def __invert__(self):
        newone = copy.deepcopy(self)
        newone.cutstr = '!({cut})'.format(cut=str(self))
        return newone
    
    # RIC: this is a bit dangerous as it depends exactly on
    #      how the string is typed in. 
    def replace(self, oldcut, newcut):
        newone = copy.deepcopy(self)
        newone.cutstr = newone.cutstr.replace(oldcut.cutstr, newcut.cutstr)
        return newone
        
if __name__ == '__main__':

    sig_mu = Cut('l2_relIso05<0.1 && l2_tightId>0.5 && l2_dxy<0.045 && l2_dz<0.2')
    sig_tau = Cut('l1_looseMvaIso>0.5 && (l1_EOverp>0.2 || l1_decayMode!=0) && l1_againstMuonTight>0.5 && l1_againstElectronLoose>0.5 && l1_dxy<0.045 && l1_dz<0.2')
    #  import pdb; pdb.set_trace()
    print sig_mu
    sig = sig_mu & sig_tau
    print sig
    print ~sig_mu
    oldcut = Cut('l2_relIso05<0.1')
    newcut = Cut('this works!')
    print sig_mu.replace(oldcut, newcut)