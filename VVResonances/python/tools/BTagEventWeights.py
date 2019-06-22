import os
import ROOT

# from within CMSSW:
ROOT.gSystem.Load('libCondFormatsBTauObjects') 
ROOT.gSystem.Load('libCondToolsBTau') 



class BTagEventWeights(object):
    def __init__(self, name,csvfile,operatingPoint=3,flavours=[0,1,2],method = 'iterativeFit'):

        self.name = name
        self.csvfile = csvfile
        self.calibrator = ROOT.BTagCalibration(self.name, self.csvfile)
        self.reader=ROOT.BTagCalibrationReader(operatingPoint,'central')
        for l in flavours:
            self.reader.load(self.calibrator,l,method)


    def getSF(self,pt,eta,flavor,btag):    
        if flavor==5:
            HF=0
        elif flavor==4:
            HF=1
        else:
            HF=2

        return self.reader.eval_auto_bounds('central',HF,eta,pt,btag)
