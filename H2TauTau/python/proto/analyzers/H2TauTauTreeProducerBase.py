from PhysicsTools.Heppy.analyzers.core.TreeAnalyzerNumpy import TreeAnalyzerNumpy

from CMGTools.H2TauTau.proto.analyzers.varsDictionary import vars as var_dict
from CMGTools.H2TauTau.proto.analyzers.TreeVariables import event_vars, ditau_vars, particle_vars, lepton_vars, electron_vars, muon_vars, tau_vars, tau_vars_extra, jet_vars, jet_vars_extra, geninfo_vars, vbf_vars, svfit_vars

from CMGTools.H2TauTau.proto.physicsobjects.DiObject import DiTau

class H2TauTauTreeProducerBase(TreeAnalyzerNumpy):

    '''
       Base H->tautau tree producer.
       Provides basic functionality for tau-tau specific trees.

       The branch names can be changed by means of a dictionary.
    '''

    def __init__(self, *args):
        super(H2TauTauTreeProducerBase, self).__init__(*args)
        self.varStyle = 'std'
        self.varDict = var_dict
        self.skimFunction = 'True'
        if hasattr(self.cfg_ana, 'varStyle'):
            self.varStyle = self.cfg_ana.varStyle
        if hasattr(self.cfg_ana, 'varDict'):
            self.varDict = self.cfg_ana.varDict
        if hasattr(self.cfg_ana, 'skimFunction'):
            self.skimFunction = self.cfg_ana.skimFunction

    def var(self, tree, varName, type=float):
        tree.var(self.varName(varName), type)

    def fill(self, tree, varName, value):
        tree.fill(self.varName(varName), value)

    def varName(self, name):
        try:
            return self.varDict[name][self.varStyle]
        except:
            if self.verbose:
                print 'WARNING: self.varDict[{NAME}][{VARSTYLE}] does not exist'.format(NAME=name, VARSTYLE=self.varStyle)
                print '         using {NAME}'.format(NAME=name)
            return name

    def fillTree(self, event):
        if eval(self.skimFunction):
            self.tree.tree.Fill()

    def bookGeneric(self, tree, var_list, obj_name=None):
        for var in var_list:
            names = [obj_name, var.name] if obj_name else [var.name]
            self.var(tree, '_'.join(names), var.type)

    def fillGeneric(self, tree, var_list, obj, obj_name=None):
        for var in var_list:
            names = [obj_name, var.name] if obj_name else [var.name]
            try:
                self.fill(tree, '_'.join(names), var.function(obj))
            except TypeError:
                print 'Problem in filling value into tree'
                print var.name, var.function(obj), obj
                raise

    def declareVariables(self, setup):
        ''' Declare all variables here in derived calss
        '''
        pass

    def process(self, event):
        ''' Fill variables here in derived class

        End implementation with self.fillTree(event)
        '''
        # needed when doing handle.product(), goes back to
        # PhysicsTools.Heppy.analyzers.core.Analyzer
        self.tree.reset()

        if not eval(self.skimFunction):
            return False

        # self.fillTree(event)

    # event
    def bookEvent(self, tree):
        self.bookGeneric(tree, event_vars)

    def fillEvent(self, tree, event):
        self.fillGeneric(tree, event_vars, event)

    # simple particle
    def bookParticle(self, tree, p_name):
        self.bookGeneric(tree, particle_vars, p_name)

    def fillParticle(self, tree, p_name, particle):
        self.fillGeneric(tree, particle_vars, particle, p_name)

    # simple gen particle
    def bookGenParticle(self, tree, p_name):
        self.bookParticle(tree, p_name)
        self.var(tree, '{p_name}_pdgId'.format(p_name=p_name))

    def fillGenParticle(self, tree, p_name, particle):
        self.fillParticle(tree, p_name, particle)
        self.fill(tree, '{p_name}_pdgId'.format(p_name=p_name), particle.pdgId() if not hasattr(particle, 'detFlavour') else particle.detFlavour)

    # di-tau
    def bookDiLepton(self, tree, fill_svfit=True, svfit_extra=False):
        # RIC: to add
        # svfit 'fittedDiTauSystem', 'fittedMET', 'fittedTauLeptons'
        self.bookGeneric(tree, ditau_vars)
        if fill_svfit:
            self.bookGeneric(tree, svfit_vars)
        if svfit_extra:
            self.bookParticle(tree, 'svfit_l1')
            self.bookParticle(tree, 'svfit_l2')

    def fillDiLepton(self, tree, diLepton, fill_svfit=True, svfit_extra=False):
        self.fillGeneric(tree, ditau_vars, diLepton)
        if fill_svfit:
            self.fillGeneric(tree, svfit_vars, diLepton)
        if svfit_extra:
            if hasattr(diLepton, 'svfit_Taus'):
                for i, tau in enumerate(diLepton.svfitTaus()):
                    self.fillParticle(tree, 'svfit_l' + str(i + 1), tau)

    # lepton
    def bookLepton(self, tree, p_name):
        self.bookParticle(tree, p_name)
        self.bookParticle(tree, p_name + '_jet')
        self.bookGeneric(tree, lepton_vars, p_name)

    def fillLepton(self, tree, p_name, lepton):
        self.fillParticle(tree, p_name, lepton)
        if hasattr(lepton, 'jet'):
            self.fillParticle(tree, p_name + '_jet', lepton.jet)
        self.fillGeneric(tree, lepton_vars, lepton, p_name)

    # muon
    def bookMuon(self, tree, p_name):
        self.bookLepton(tree, p_name)
        self.bookGeneric(tree, muon_vars, p_name)

    def fillMuon(self, tree, p_name, muon):
        self.fillLepton(tree, p_name, muon)
        self.fillGeneric(tree, muon_vars, muon, p_name)

    # ele
    def bookEle(self, tree, p_name):
        self.bookLepton(tree, p_name)
        self.bookGeneric(tree, electron_vars, p_name)

    def fillEle(self, tree, p_name, ele):
        self.fillLepton(tree, p_name, ele)
        self.fillGeneric(tree, electron_vars, ele, p_name)

    # tau
    def bookTau(self, tree, p_name, fill_extra=False):
        self.bookLepton(tree, p_name)
        self.bookGeneric(tree, tau_vars, p_name)
        if fill_extra:
            self.bookGeneric(tree, tau_vars_extra, p_name)

    def fillTau(self, tree, p_name, tau, fill_extra=False):
        self.fillLepton(tree, p_name, tau)
        self.fillGeneric(tree, tau_vars, tau, p_name)
        if fill_extra:
            self.fillGeneric(tree, tau_vars_extra, tau, p_name)

    # jet
    def bookJet(self, tree, p_name, fill_extra=False):
        self.bookParticle(tree, p_name)
        self.bookGeneric(tree, jet_vars, p_name)
        if fill_extra:
            self.bookGeneric(tree, jet_vars_extra, p_name)

    def fillJet(self, tree, p_name, jet, fill_extra=False):
        self.fillParticle(tree, p_name, jet)
        self.fillGeneric(tree, jet_vars, jet, p_name)
        if fill_extra:
            self.fillGeneric(tree, jet_vars_extra, jet, p_name)

    # vbf
    def bookVBF(self, tree, p_name):
        self.bookGeneric(tree, vbf_vars, p_name)

    def fillVBF(self, tree, p_name, vbf):
        self.fillGeneric(tree, vbf_vars, vbf, p_name)

    # generator information
    def bookGenInfo(self, tree):
        self.bookGeneric(tree, geninfo_vars)

    def fillGenInfo(self, tree, event):
        self.fillGeneric(tree, geninfo_vars, event)

    # additional METs
    def bookExtraMetInfo(self, tree):
        self.var(tree, 'puppimet_pt')
        self.var(tree, 'puppimet_phi')
        self.var(tree, 'puppimet_mt1')
        self.var(tree, 'puppimet_mt2')
        self.var(tree, 'puppimet_mttotal')

        self.var(tree, 'pfmet_pt')
        self.var(tree, 'pfmet_phi')
        self.var(tree, 'pfmet_mt1')
        self.var(tree, 'pfmet_mt2')
        self.var(tree, 'pfmet_mttotal')

    def fillExtraMetInfo(self, tree, event):
        self.fill(tree, 'puppimet_pt', event.puppimet.pt())
        self.fill(tree, 'puppimet_phi', event.puppimet.phi())
        self.fill(tree, 'puppimet_mt1', DiTau.calcMT(event.puppimet, event.leg1))
        self.fill(tree, 'puppimet_mt2', DiTau.calcMT(event.puppimet, event.leg2))

        self.fill(tree, 'pfmet_pt', event.pfmet.pt())
        self.fill(tree, 'pfmet_phi', event.pfmet.phi())
        self.fill(tree, 'pfmet_mt1', DiTau.calcMT(event.pfmet, event.leg1))
        self.fill(tree, 'pfmet_mt2', DiTau.calcMT(event.pfmet, event.leg2))

    # TauSpinner information
    def bookTauSpinner(self, tree):
        self.var(tree, 'TauSpinnerWTisValid')
        self.var(tree, 'TauSpinnerWT')
        self.var(tree, 'TauSpinnerWThminus')
        self.var(tree, 'TauSpinnerWThplus')
        self.var(tree, 'TauSpinnerTauPolFromZ')
        self.var(tree, 'TauSpinnerWRight')
        self.var(tree, 'TauSpinnerWLeft')
        self.var(tree, 'TauSpinnerIsRightLeft')

    def fillTauSpinner(self, tree, event):
        self.fill(tree, 'TauSpinnerWTisValid', event.TauSpinnerWTisValid)
        self.fill(tree, 'TauSpinnerWT', float(event.TauSpinnerWT))
        self.fill(tree, 'TauSpinnerWThminus', float(event.TauSpinnerWThminus))
        self.fill(tree, 'TauSpinnerWThplus', float(event.TauSpinnerWThplus))
        self.fill(tree, 'TauSpinnerTauPolFromZ', float(event.TauSpinnerTauPolFromZ))
        self.fill(tree, 'TauSpinnerWRight', float(event.TauSpinnerWRight))
        self.fill(tree, 'TauSpinnerWLeft', float(event.TauSpinnerWLeft))
        self.fill(tree, 'TauSpinnerIsRightLeft', float(event.TauSpinnerIsRightLeft))

    def bookTopPtReweighting(self, tree):
        self.var(tree, 'gen_top_1_pt')
        self.var(tree, 'gen_top_2_pt')
        self.var(tree, 'gen_top_weight')

    def fillTopPtReweighting(self, tree, event):
        '''FIXME: Move this to extra class - only do inline calculations here'''
        if not self.cfg_comp.isMC:
            self.fill(tree, 'gen_top_weight', 1.)
            return

        self.fill(tree, 'gen_top_1_pt', getattr(event, 'top_1_pt', -999.))
        self.fill(tree, 'gen_top_2_pt', getattr(event, 'top_2_pt', -999.))
        self.fill(tree, 'gen_top_weight', getattr(event, 'topweight', 1.))
