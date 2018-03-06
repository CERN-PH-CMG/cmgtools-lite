# based on BTagScaleFactors.py, tailored for CSV full-shape reweighting only and using CMSSW integrated code

import os
import ROOT
ROOT.gSystem.Load('libCondFormatsBTauObjects')
ROOT.gSystem.Load('libCondToolsBTau')
from ROOT import BTagCalibration, BTagCalibrationReader


class BTagCSVFullShape(object):
    def __init__(self, csvfile,
                 verbose=False):
        self.csvfile = csvfile
        self.verbose = True#verbose
        self.algo = 'deepcsv'
        
        self.iterative_systs = ['jes',
                                'lf', 'hf',
                                'hfstats1', 'hfstats2',
                                'lfstats1', 'lfstats2',
                                'cferr1', 'cferr2' ]

        self.init()
        self.create_readers()

    def init(self):
        if self.verbose:
            print "Initializing btag calibrator from %s" % self.csvfile
        self.calibrator = BTagCalibration(self.algo, self.csvfile)

    def create_readers(self):
        if self.verbose:
            print "Setting up btag calibration readers"

        self.v_sys = getattr(ROOT, 'vector<string>')()
        for syst in self.iterative_systs:
            self.v_sys.push_back('up_'+syst)
            self.v_sys.push_back('down_'+syst)
        
        self.reader = BTagCalibrationReader(3,'central',self.v_sys)
        self.reader.load(self.calibrator,0,'iterativefit')
        self.reader.load(self.calibrator,1,'iterativefit')
        self.reader.load(self.calibrator,2,'iterativefit')

    def get_SF(self, pt, eta, flavor, val, syst='central'):

        fl_index = min(-flavor+5,2)
        """
            Note the flavor convention: hadronFlavor is b=5, c=4, f=0
            Convert them to the btagging group convention of 0,1,2
        """

        syst = syst.lower()
        return self.reader.eval_auto_bounds(syst if self.relevant_iterative_systs(fl_index,syst) else 'central',fl_index,eta,pt,val)

    def relevant_iterative_systs(self,flavor, syst):
        """Returns true if a flavor/syst combination is relevant"""
        if flavor==0:
            return syst in ["central",
                            "up_jes", "down_jes",
                            "up_lf", "down_lf",
                            "up_hfstats1", "down_hfstats1",
                            "up_hfstats2", "down_hfstats2"]
        elif flavor==1:
            return syst in ["central",
                            "up_cferr1", "down_cferr1",
                            "up_cferr2", "down_cferr2" ]
        elif flavor==2:
            return syst in ["central",
                            "up_jes", "down_jes",
                            "up_hf", "down_hf",
                            "up_lfstats1", "down_lfstats1",
                            "up_lfstats2", "down_lfstats2" ]
        return True
