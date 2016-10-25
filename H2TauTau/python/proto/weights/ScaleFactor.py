import os
import imp
import ROOT
import array

class ScaleFactor(object):
    ''' HTT lepton scale factor class
    Translated to python from CMS-HTT/LeptonEff-interface
    '''
    def __init__(self, inputFile, histBaseName='ZMass'):
        ''' Polymorphic: can either compute the scale factors from 
        a root file containing either TGraph's or TF1's, or it can 
        analytically compute the SF from functiond defined in python
        '''
        if inputFile.endswith('.root'):
            if 'scalefactors' in inputFile: # Andrew's workspace
                self._initFromRooFit(inputFile, histBaseName)
            else: # DESY workspace
                self._initFromRoot(inputFile, histBaseName)
        elif inputFile.endswith('.py'):
            self._initFromPython(inputFile)

    def _initFromRooFit(self, inputRootFile, histBaseName):
        fileIn = ROOT.TFile(inputRootFile)
        self.ws = fileIn.Get('w')
        fileIn.Close()
        self.sf_name = histBaseName
        self.obj_tag = histBaseName.split('_')[0]

    def _initFromPython(self, inputPythonFile):
        path = inputPythonFile.split('/')
        explicitPathItems =[]
        for p in path:
            if '$' in p:
                p1 =  os.environ[p.replace('$', '')]
                explicitPathItems.append(p1)
            else:            
                explicitPathItems.append(p)
        explicitPath = '/'.join(explicitPathItems)
        efficiencies = imp.load_source(explicitPathItems[-1].replace('.py', ''), explicitPath)
        self.eff_data = efficiencies.effData
        self.eff_data_fakes = efficiencies.effDataFakeTau
        self.eff_mc = efficiencies.effMC
        self.eff_mc_fakes = efficiencies.effMCFakeTau

    def _initFromRoot(self, inputRootFile, histBaseName='ZMass'):
        self.fileIn = ROOT.TFile(inputRootFile, 'read')
        if self.fileIn.IsZombie():
            raise RuntimeError('Error in opening scale factor file', inputRootFile)

        self.etaBinsH = self.fileIn.Get('etaBinsH')
        self.eff_data = {}
        self.eff_mc = {}

        etaLabel = ''
        graphName = ''
        
        for iBin in xrange(self.etaBinsH.GetNbinsX()):
            etaLabel = self.etaBinsH.GetXaxis().GetBinLabel(iBin+1)

            for label, eff_dict in [('_Data', self.eff_data), ('_MC', self.eff_mc)]:
                graphName = histBaseName + etaLabel + label                
                graph = self.fileIn.Get(graphName) # RM: this can be either a TGraph or a TF1
                if not graph: 
                    continue
                eff_dict[etaLabel] = graph
                if isinstance(graph, ROOT.TF1):
                    continue
                self.setAxisBins(eff_dict[etaLabel])

            if etaLabel not in self.eff_mc:
                continue
            if isinstance(self.eff_mc[etaLabel], ROOT.TF1) and isinstance(self.eff_data[etaLabel], ROOT.TF1):
                continue
            elif not self.checkSameBinning(self.eff_mc[etaLabel], self.eff_data[etaLabel]):
                raise RuntimeError('ERROR in ScaleFactor::init_ScaleFactor(TString inputRootFile) from LepEffInterface/src/ScaleFactor.cc . Can not proceed because ScaleFactor::check_SameBinning returned different pT binning for data and MC for eta label', etaLabel)

    def setAxisBins(self, graph):
        ''' Wow this is crazy. No way in ROOT to do it?? '''

        nPoints = graph.GetN()
        # axisBins = array.array('d')
        bins = []
        for i in xrange(nPoints):
            bins.append(graph.GetX()[i] - graph.GetErrorXlow(i))
        bins.append(graph.GetX()[nPoints - 1] + graph.GetErrorXhigh(nPoints - 1))

        graph.GetXaxis().Set(nPoints, array.array('d', bins))


    def checkSameBinning(self, graph1, graph2):
        n1 = graph1.GetXaxis().GetNbins()
        n2 = graph2.GetXaxis().GetNbins()

        if n1 != n2:
            return False
        else:
            for i in xrange(n1):
                if graph1.GetXaxis().GetXbins().GetArray()[i] != graph2.GetXaxis().GetXbins().GetArray()[i]:
                    return False

        return True

    def getScaleFactor(self, pt, eta, isFake=False, iso=None):
        if hasattr(self, 'ws'):
            return self.getFactorWS(pt, eta, 'ratio', isFake=isFake, iso=iso)
        return self.getEfficiencyData(pt, eta, isFake)/max(self.getEfficiencyMC(pt, eta, isFake), 1.e-6)

    def getEfficiencyData(self, pt, eta, isFake=False, iso=None):
        if hasattr(self, 'ws'):
            return self.getFactorWS(pt, eta, 'data', isFake=isFake, iso=iso)
        return self.getEfficiency(pt, eta, self.eff_data_fakes if isFake and hasattr(self, 'eff_data_fakes') else self.eff_data)

    def getEfficiencyMC(self, pt, eta, isFake=False, iso=None):
        if hasattr(self, 'ws'):
            return self.getFactorWS(pt, eta, 'mc', isFake=isFake, iso=iso)
        return self.getEfficiency(pt, eta, self.eff_mc_fakes if isFake and hasattr(self, 'eff_mc_fakes') else self.eff_mc)

    def getFactorWS(self, pt, eta, tag, isFake=False, iso=None):
        ''' See https://github.com/CMS-HTT/CorrectionsWorkspace
        FIXME:  add proper isFake implementation (but may need to change inputs)
        '''
        self.ws.var('_'.join([self.obj_tag, 'pt'])).setVal(pt)
        self.ws.var('_'.join([self.obj_tag, 'eta'])).setVal(eta)
        if iso:
            self.ws.var('_'.join([self.obj_tag, 'iso'])).setVal(iso)

        return self.ws.function('_'.join([self.sf_name, tag])).getVal()

    def findEtaLabel(self, eta, eff_dict):
        eta = abs(eta)
        binNumber = self.etaBinsH.GetXaxis().FindFixBin(eta)
        label = self.etaBinsH.GetXaxis().GetBinLabel(binNumber)
        if label not in eff_dict:
            raise RuntimeError('ERROR in ScaleFactor::get_EfficiencyData(double pt, double eta) from LepEffInterface/src/ScaleFactor.cc : no object corresponding to eta label', label)
        return label

    def findPtBin(self, pt, g_eff):
        nPoints = g_eff.GetN()
        ptMax = g_eff.GetX()[nPoints-1] + g_eff.GetErrorXhigh(nPoints-1)
        ptMin = g_eff.GetX()[0] = g_eff.GetErrorXlow(0)

        if pt >= ptMax:
            return nPoints
        elif pt < ptMin:
            print 'WARNING in ScaleFactor::get_EfficiencyData(double pt, double eta) from LepEffInterface/src/ScaleFactor.cc: pT too low (pt = ', pt, '), min value is ', ptMin, '. Returned efficiency = 1. Weight will be 1.'
            return -99
        else:
            return g_eff.GetXaxis().FindFixBin(pt)

    def getEfficiency(self, pt, eta, eff_dict):
        
        # return efficiency for when using analytical function
        if not isinstance(eff_dict, dict):
            eff = eff_dict(pt, eta)
            return eff
        
        label = self.findEtaLabel(eta, eff_dict)
        
        g_eff = eff_dict[label]
        
        if isinstance(g_eff, ROOT.TF1):
            eff = g_eff.Eval(pt)
        
        else:
            ptBin = self.findPtBin(pt, g_eff)
    
            if ptBin == -99:
                return 1.
    
            eff = g_eff.GetY()[ptBin-1]
        
        if eff > 1.:
            print 'Warning: Efficiency larger 1'
        elif eff < 0.:
            print 'Warning: Efficiency negative'
        return eff

        return 1.

if __name__ == '__main__':
#     sf = ScaleFactor('$CMSSW_BASE/src/CMGTools/H2TauTau/data/Electron_Ele23_fall15.root')
#     for pt, eta in [(29.3577, 1.4845), (50., 0.2), (17., 0.05), (1000., 2.04)]:
#         print 'Eff data', sf.getEfficiencyData(pt, eta)
#         print 'Eff MC', sf.getEfficiencyMC(pt, eta)
#         print 'SF', sf.getScaleFactor(pt, eta)



#     sf = ScaleFactor('$CMSSW_BASE/src/CMGTools/H2TauTau/data/Tau_diTau35_fall15.root', 
#                      histBaseName='Eff')

    sf = ScaleFactor('$CMSSW_BASE/src/CMGTools/H2TauTau/data/Tau_diTau35_fall15.py', )

    for pt, eta in [(  29.3577, 1.4845), 
                    (  50.    , 0.2   ), 
                    (  17.    , 0.05  ), 
                    (  45.    , 0.05  ), 
                    (  50.    , 0.05  ), 
                    (  55.    , 0.05  ), 
                    (  60.    , 0.05  ), 
                    (  80.    , 0.05  ), 
                    ( 100.    , 0.05  ), 
                    (1000.    , 2.04  )]:
        print '\n==========>'
        print 'pt %f, eta %f' %(pt, eta)
        print 'Eff data', sf.getEfficiencyData(pt, eta)
        print 'Eff MC', sf.getEfficiencyMC(pt, eta)
        print 'SF', sf.getScaleFactor(pt, eta)

