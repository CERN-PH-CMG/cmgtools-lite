from ROOT import kViolet, kAzure, kTeal, kOrange, kGray, kSpring, kYellow


class Style:

    def __init__(self,
                 markerStyle=8,
                 markerColor=1,
                 markerSize=1,
                 lineStyle=1,
                 lineColor=1,
                 lineWidth=2,
                 fillColor=None,
                 fillStyle=1001,
                 drawAsData=False):
        self.markerStyle = markerStyle
        self.markerColor = markerColor
        self.markerSize = markerSize
        self.lineStyle = lineStyle
        self.lineColor = lineColor
        self.lineWidth = lineWidth
        if fillColor is None:
            self.fillColor = lineColor
        else:
            self.fillColor = fillColor
        self.fillStyle = fillStyle
        self.drawAsData = drawAsData

    def formatHisto(self, hist, title=None):
        hist.SetMarkerStyle(self.markerStyle)
        hist.SetMarkerColor(self.markerColor)
        hist.SetMarkerSize(self.markerSize)
        hist.SetLineStyle(self.lineStyle)
        hist.SetLineColor(self.lineColor)
        hist.SetLineWidth(self.lineWidth)
        hist.SetFillColor(self.fillColor)
        hist.SetFillStyle(self.fillStyle)
        if title is not None:
            hist.SetTitle(title)
        return hist

# the following standard files are defined and ready to be used.
# more standard styles can be added on demand.
# user defined styles can be created in the same way in any python module

sBlack = Style()
sData = Style(fillStyle=0, markerSize=1.3, drawAsData=True)
sBlue = Style(markerColor=4, fillColor=4)
sGreen = Style(markerColor=8, fillColor=8)
sRed = Style(markerColor=2, fillColor=2)
sYellow = Style(lineColor=1, markerColor=5, fillColor=5)
sViolet = Style(lineColor=1, markerColor=kViolet, fillColor=kViolet)
sSignal = Style(lineColor=kViolet, markerColor=kViolet, fillColor=0)

# qcdcol = TColor.GetColor(250,202,255)
sVV_QCD = Style(lineColor=1, markerColor=kGray, fillColor=kGray)
# dycol =  TColor.GetColor(248,206,104)
sVV_DYJets = Style(lineColor=1, markerColor=kAzure +
                   5, fillColor=kAzure + 5)
# wcol = TColor.GetColor(222,90,106)
sVV_WJets = Style(lineColor=1, markerColor=kAzure -
                  9, fillColor=kAzure - 9)
# ttcol = TColor.GetColor(155,152,204)
sVV_TTJets = Style(lineColor=1, markerColor=kSpring -
                   5, fillColor=kSpring - 5)
sVV_TTJetsNonW = Style(
    lineColor=1, markerColor=kTeal - 1, fillColor=kTeal - 1)
sVV_SingleTop = Style(lineColor=1, markerColor=kSpring, fillColor=kSpring)

# sVV_Higgs = Style(lineColor=kBlue, markerColor=2, lineStyle=2, fillColor=0)
# sVV_Higgs = Style(lineColor=kBlue, markerColor=0, lineStyle=2, fillColor=0, lineWidth=3)
# zlcol = TColor.GetColor(100,182,232)
# sVV_ZL = Style(lineColor=1, markerColor=kAzure+5, fillColor=zlcol)
# dibosoncol = TColor.GetColor(222,90,106)
sVV_VV = Style(lineColor=1, markerColor=kOrange, fillColor=kOrange)
sVV_GJets = Style(lineColor=1, markerColor=kYellow,
                  fillColor=kYellow)

sBlackSquares = Style(markerStyle=21)
sBlueSquares = Style(lineColor=4, markerStyle=21, markerColor=4)
sGreenSquares = Style(lineColor=8, markerStyle=21, markerColor=8)
sRedSquares = Style(lineColor=2, markerStyle=21, markerColor=2)


styleSet = [sBlue, sGreen, sRed, sYellow, sViolet,
            sBlackSquares, sBlueSquares, sGreenSquares, sRedSquares]
iStyle = 0


def nextStyle():
    global iStyle
    style = styleSet[iStyle]
    iStyle = iStyle + 1
    if iStyle >= len(styleSet):
        iStyle = 0
    return style

histPref = {}
histPref['Data'] = {'style': sData, 'layer': 2999, 'legend': 'Observed'}
histPref['data_*'] = {'style': sData, 'layer': 2999, 'legend': 'Observed'}
histPref['BulkGrav*'] = {'style': sSignal, 'layer': 0.9, 'legend': 'Bulk G #rightarrow VV'}
histPref['BulkGravToWW_narrow_2000'] = {'style': sSignal, 'layer': 0.9, 'legend': 'Bulk G #rightarrow WV (m = 2 TeV)'}
histPref['VBF_Radion*'] = {'style': sSignal, 'layer': 0.9, 'legend': 'VBF Radion #rightarrow VV'}
histPref['VBF_RadionToWW_narrow_2000'] = {'style': sSignal, 'layer': 0.9, 'legend': 'VBF Radion #rightarrow WW (m = 2 TeV)'}
histPref['ZTT*'] = {'style': sVV_DYJets,
                    'layer': 4, 'legend': 'Z#rightarrow#tau#tau'}
histPref['embed_*'] = {'style': sViolet, 'layer': 4.1, 'legend': None}
histPref['Top'] = {'style': sVV_TTJets, 'layer': 5, 'legend': 'top'}
histPref['TT'] = {'style': sVV_TTJets, 'layer': 1, 'legend': 't#bar{t}'}
histPref['TT*_W'] = {'style': sVV_TTJets, 'layer': 3.6, 'legend': 't#bar{t} (W)'}
histPref['TT*_nonW'] = {'style': sVV_TTJetsNonW,
                        'layer': 2.6, 'legend': 't#bar{t} (other)'}
histPref['T*tW*'] = {'style': sVV_SingleTop, 'layer': 1, 'legend': 'Single t'}
histPref['TTo*'] = {'style': sVV_SingleTop, 'layer': 1, 'legend': 'Single t'}
histPref['TBarTo*'] = {'style': sVV_SingleTop, 'layer': 1, 'legend': 'Single t'}
histPref['Single t'] = {'style': sVV_SingleTop, 'layer': 1, 'legend': 'Single t'}
histPref['WW*'] = {'style': sVV_VV, 'layer': 3.9, 'legend': 'Diboson'}
histPref['WZ*'] = {'style': sVV_VV, 'layer': 3.8, 'legend': 'Diboson'}
histPref['ZZ*'] = {'style': sVV_VV, 'layer': 3.7, 'legend': 'Diboson'}
histPref['Diboson'] = {'style': sVV_VV, 'layer': 4.0, 'legend': 'Diboson'}
histPref['VV*'] = {'style': sVV_VV, 'layer': 4.0, 'legend': 'Diboson'}
histPref['Electroweak'] = {'style': sVV_VV,
                           'layer': 4.0, 'legend': 'Electroweak'}
histPref['QCD*'] = {'style': sVV_QCD, 'layer': 2, 'legend': 'QCD multijet'}
histPref['W'] = {'style': sVV_WJets, 'layer': 3, 'legend': 'W+jets'}
histPref['WJ*'] = {'style': sVV_WJets, 'layer': 3, 'legend': 'W+jets'}
histPref['W*Jets'] = {'style': sVV_WJets, 'layer': 3, 'legend': 'W+jets'}
histPref['V*Jets'] = {'style': sVV_WJets, 'layer': 4, 'legend': 'V+jets'}
histPref['EWK'] = {'style': sVV_WJets, 'layer': 3, 'legend': 'EWK'}
histPref['ElectroWeak'] = {'style': sVV_WJets,
                           'layer': 3, 'legend': 'ElectroWeak'}
histPref['ZJ*'] = {'style': sVV_DYJets, 'layer': 3.1,
                   'legend': 'Z+jets'}
histPref['ZL*'] = {'style': sVV_DYJets, 'layer': 3.2, 'legend': 'DY + jets'}
histPref['Zl0jet*'] = {'style': sVV_DYJets, 'layer': 3.2,
                       'legend': 'Z#rightarrow ll + 0 jets'}
histPref['Zl1jet*'] = {'style': sVV_DYJets,
                       'layer': 3.2, 'legend': 'Z#rightarrow ll + 1 jet'}
# histPref['Zl2jet*'] = {'style': sVV_Higgs, 'layer': 3.2,
#                        'legend': 'Z#rightarrow ll + #geq 2 jets'}
histPref['ZLL'] = {'style': sVV_DYJets, 'layer': 3.2, 'legend': 'Z#rightarrow ll'}
histPref['DYJetsToLL*'] = {'style': sVV_DYJets, 'layer': 3.2, 'legend': 'Z/#gamma #rightarrow ll'}
histPref['Ztt_TL'] = {'style': sViolet, 'layer': 4.1,
                      'legend': 'Z#rightarrow#tau#tau/Z#rightarrow ll, j#rightarrow#tau'}
histPref['MC'] = {'style': sVV_WJets, 'layer': 3, 'legend': 'simulation'}
# histPref['Higgs*'] = {'style': sVV_Higgs, 'layer': 1001, 'legend': None}
# histPref['ggH*'] = {'style': sVV_Higgs, 'layer': 1001, 'legend': None}
# histPref['bbH*'] = {'style': sVV_Higgs, 'layer': 1001, 'legend': None}
# histPref['SMS*'] = {'style': sVV_Higgs, 'layer': 1001, 'legend': None}
