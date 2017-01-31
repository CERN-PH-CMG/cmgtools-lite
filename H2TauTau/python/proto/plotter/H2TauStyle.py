from ROOT import TColor, kViolet, kBlue, kRed, kAzure

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
        if title != None:
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

# John's colours
qcdcol = TColor.GetColor(250,202,255)
dycol =  TColor.GetColor(248,206,104)
wcol = TColor.GetColor(222,90,106)
ttcol = TColor.GetColor(155,152,204)
zlcol = TColor.GetColor(100,182,232)
dibosoncol = TColor.GetColor(222,90,106)

# Backgrounds
sHTT_QCD = Style(lineColor=1, markerColor=qcdcol, fillColor=qcdcol)
sHTT_DYJets = Style(lineColor=1, markerColor=dycol, fillColor=dycol)
sHTT_WJets = Style(lineColor=1, markerColor=wcol, fillColor=wcol)
sHTT_TTJets = Style(lineColor=1, markerColor=ttcol, fillColor=ttcol)
sHTT_ZL = Style(lineColor=1, markerColor=zlcol, fillColor=zlcol)
sHTT_VV = Style(lineColor=1, markerColor=dibosoncol, fillColor=dibosoncol)

# Signals
sHTT_Higgs = Style(lineColor=kBlue, markerColor=0, lineStyle=2, fillColor=0, lineWidth=3)
sHTT_Higgs2 = Style(lineColor=kAzure+8, markerColor=0, lineStyle=3, fillColor=0, lineWidth=3)


sBlackSquares = Style(markerStyle=21)
sBlueSquares = Style(lineColor=4, markerStyle=21, markerColor=4)
sGreenSquares = Style(lineColor=8, markerStyle=21, markerColor=8)
sRedSquares = Style(lineColor=2, markerStyle=21, markerColor=2)


styleSet = [sBlue, sGreen, sRed, sYellow, sViolet, sBlackSquares, sBlueSquares, sGreenSquares, sRedSquares]
iStyle = 0


def nextStyle():
    global iStyle
    style = styleSet[iStyle]
    iStyle = iStyle+1
    if iStyle >= len(styleSet):
        iStyle = 0
    return style

histPref = {}
histPref['Data'] = {'style':sData, 'layer':2999, 'legend':'Observed'}
histPref['data_*'] = {'style':sData, 'layer':2999, 'legend':'Observed'}
histPref['ZTT*'] = {'style':sHTT_DYJets, 'layer':4, 'legend':'Z#rightarrow#tau#tau'}
histPref['embed_*'] = {'style':sViolet, 'layer':4.1, 'legend':None}
histPref['TT'] = {'style':sHTT_TTJets, 'layer':1, 'legend':'t#bar{t}'} 
histPref['T*tW*'] = {'style':sHTT_TTJets, 'layer':1, 'legend':'Single t'} 
histPref['TTo*'] = {'style':sHTT_TTJets, 'layer':1, 'legend':'Single t'} 
histPref['TBarTo*'] = {'style':sHTT_TTJets, 'layer':1, 'legend':'Single t'} 
histPref['Single t'] = {'style':sHTT_TTJets, 'layer':1, 'legend':'Single t'} 
histPref['WW*'] = {'style':sHTT_VV, 'layer':0.9, 'legend':'Diboson'} 
histPref['WZ*'] = {'style':sHTT_VV, 'layer':0.8, 'legend':'Diboson'} 
histPref['ZZ*'] = {'style':sHTT_VV, 'layer':0.7, 'legend':'Diboson'} 
histPref['Diboson'] = {'style':sHTT_VV, 'layer':0.7, 'legend':'Diboson'} 
histPref['VV*'] = {'style':sHTT_VV, 'layer':0.7, 'legend':'Diboson'} 
histPref['Electroweak'] = {'style':sHTT_VV, 'layer':0.7, 'legend':'Electroweak'} 
histPref['QCD*'] = {'style':sHTT_QCD, 'layer':2, 'legend':'QCD multijet'}
histPref['W'] = {'style':sHTT_WJets, 'layer':3, 'legend':'W+jets'}  
histPref['WJ*'] = {'style':sHTT_WJets, 'layer':3, 'legend':'W+jets'}  
histPref['W*Jets'] = {'style':sHTT_WJets, 'layer':3, 'legend':'W+jets'}  
histPref['EWK'] = {'style':sHTT_WJets, 'layer':3, 'legend':'EWK'}  
histPref['ElectroWeak'] = {'style':sHTT_WJets, 'layer':3, 'legend':'ElectroWeak'}  
histPref['ZJ*'] = {'style':sHTT_DYJets, 'layer':3.1, 'legend':'Z#rightarrow#tau#tau/Z#rightarrow ll, j#rightarrow#tau'}
histPref['ZL*'] = {'style':sHTT_ZL, 'layer':3.2, 'legend':'Z#rightarrow ll'}
histPref['Zl0jet*'] = {'style':sHTT_ZL, 'layer':3.2, 'legend':'Z#rightarrow ll + 0 jets'}
histPref['Zl1jet*'] = {'style':sHTT_DYJets, 'layer':3.2, 'legend':'Z#rightarrow ll + 1 jet'}
histPref['Zl2jet*'] = {'style':sHTT_Higgs, 'layer':3.2, 'legend':'Z#rightarrow ll + #geq 2 jets'}
histPref['ZLL'] = {'style':sHTT_ZL, 'layer':3.2, 'legend':'Z#rightarrow ll'}
histPref['Ztt_TL'] = {'style':sViolet, 'layer':4.1, 'legend':'Z#rightarrow#tau#tau/Z#rightarrow ll, j#rightarrow#tau'}
histPref['HiggsGGH125'] = {'style':sHTT_Higgs, 'layer':1001, 'legend':'H_{125}#rightarrow#tau#tau (ggH)'}
histPref['HiggsVBF125'] = {'style':sHTT_Higgs2, 'layer':1001, 'legend':'H_{125}#rightarrow#tau#tau (VBF)'}
histPref['ggH*'] = {'style':sHTT_Higgs, 'layer':1001, 'legend':None}
histPref['bbH*'] = {'style':sHTT_Higgs, 'layer':1001, 'legend':None}
histPref['SMS*'] = {'style':sHTT_Higgs, 'layer':1001, 'legend':None}

