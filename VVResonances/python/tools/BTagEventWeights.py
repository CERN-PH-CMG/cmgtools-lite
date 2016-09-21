import os
import ROOT

# from within CMSSW:
ROOT.gSystem.Load('libCondFormatsBTauObjects') 
ROOT.gSystem.Load('libCondToolsBTau') 



class BTagEventWeights(object):
    def __init__(self, name,csvfile):

        self.name = name
        self.csvfile = csvfile
        self.calibrator = ROOT.BTagCalibration(self.name, self.csvfile)
        self.reader=ROOT.BTagCalibrationReader(3,'central')
        self.reader.load(self.calibrator,0,'iterativefit')
        self.reader.load(self.calibrator,1,'iterativefit')
        self.reader.load(self.calibrator,2,'iterativefit')


    def getSF(self,pt,eta,flavor,btag):    
        if flavor==5:
            HF=0
        elif flavor==4:
            HF=1
        else:
            HF=2

        return self.reader.eval_auto_bounds('central',HF,eta,pt,btag)
