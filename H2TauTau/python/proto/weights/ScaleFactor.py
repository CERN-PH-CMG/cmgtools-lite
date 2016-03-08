import ROOT
import array

class ScaleFactor(object):
    ''' HTT lepton scale factor class
    Translated to python from CMS-HTT/LeptonEff-interface
    '''
    def __init__(self, inputRootFile, histBaseName='ZMass'):
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
                eff_dict[etaLabel] = self.fileIn.Get(graphName)
                self.setAxisBins(eff_dict[etaLabel])

            if not self.checkSameBinning(self.eff_mc[etaLabel], self.eff_data[etaLabel]):
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

    def getScaleFactor(self, pt, eta):
        return self.getEfficiencyData(pt, eta)/self.getEfficiencyMC(pt, eta)

    def getEfficiencyData(self, pt, eta):
        return self.getEfficiency(pt, eta, self.eff_data)

    def getEfficiencyMC(self, pt, eta):
        return self.getEfficiency(pt, eta, self.eff_mc)


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
        label = self.findEtaLabel(eta, eff_dict)
        
        g_eff = eff_dict[label]
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
    sf = ScaleFactor('$CMSSW_BASE/src/CMGTools/H2TauTau/data/Electron_Ele23_fall15.root')
    for pt, eta in [(29.3577, 1.4845), (50., 0.2), (17., 0.05), (1000., 2.04)]:
        print 'Eff data', sf.getEfficiencyData(pt, eta)
        print 'Eff MC', sf.getEfficiencyMC(pt, eta)
        print 'SF', sf.getScaleFactor(pt, eta)
