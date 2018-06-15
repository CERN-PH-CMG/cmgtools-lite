#!/usr/bin/env python
#from mcAnalysis import *
from CMGTools.TTHAnalysis.plotter.mcAnalysis import *
import CMGTools.TTHAnalysis.plotter.CMS_lumi as CMS_lumi
import itertools, math

CMS_lumi.writeExtraText = 1

_global_workspaces=[] # avoid crash in 80X, to be investigated

if "/bin2Dto1Dlib_cc.so" not in ROOT.gSystem.GetLibraries():
    ROOT.gROOT.ProcessLine(".L %s/src/CMGTools/TTHAnalysis/python/plotter/bin2Dto1Dlib.cc+" % os.environ['CMSSW_BASE']);
if "/fakeRate_cc.so" not in ROOT.gSystem.GetLibraries(): 
    ROOT.gROOT.ProcessLine(".L %s/src/CMGTools/TTHAnalysis/python/plotter/fakeRate.cc+" % os.environ['CMSSW_BASE']);

SAFE_COLOR_LIST=[
ROOT.kBlack, ROOT.kRed, ROOT.kGreen+2, ROOT.kBlue, ROOT.kMagenta+1, ROOT.kOrange+7, ROOT.kCyan+1, ROOT.kGray+2, ROOT.kViolet+5, ROOT.kSpring+5, ROOT.kAzure+1, ROOT.kPink+7, ROOT.kOrange+3, ROOT.kBlue+3, ROOT.kMagenta+3, ROOT.kRed+2,
]+range(11,40)
def _unTLatex(string):
    return string.replace("#chi","x").replace("#mu","m").replace("#rightarrow","->")
class PlotFile:
    def __init__(self,fileName,options):
        self._options = options
        self._plots = []
        defaults = {}
        infile = open(fileName,'r')
        for line in infile:
            if re.match("\s*#.*", line) or len(line.strip())==0: continue
            while line.strip()[-1] == "\\":
                line = line.strip()[:-1] + infile.next()
            extra = {}
            if ";" in line:
                (line,more) = line.split(";")[:2]
                more = more.replace("\\,",";")
                for setting in [f.strip().replace(";",",") for f in more.split(',')]:
                    if "=" in setting: 
                        (key,val) = [f.strip() for f in setting.split("=")]
                        extra[key] = eval(val)
                    else: extra[setting] = True
            line = re.sub("#.*","",line) 
            field = [f.strip().replace(";",":") for f in line.replace("::",";;").replace("\\:",";").split(':')]
            if len(field) == 1 and field[0] == "*":
                if len(self._plots): raise RuntimeError, "PlotFile defaults ('*') can be specified only before all plots"
                print "Setting the following defaults for all plots: "
                for k,v in extra.iteritems():
                    print "\t%s: %r" % (k,v)
                    defaults[k] = v
                continue
            else:
                for k,v in defaults.iteritems():
                    if k not in extra: extra[k] = v
            if len(field) <= 2: continue
            if len(options.plotselect):
                skipMe = True
                for p0 in options.plotselect:
                    for p in p0.split(","):
                        if re.match(p+"$", field[0]): skipMe = False
                if skipMe: continue
            if len(options.plotexclude):
                skipMe = False
                for p0 in options.plotexclude:
                    for p in p0.split(","):
                        if re.match(p+"$", field[0]): skipMe = True
                if skipMe: continue
            if options.globalRebin: extra['rebinFactor'] = options.globalRebin
            self._plots.append(PlotSpec(field[0],field[1],field[2],extra))
    def plots(self):
        return self._plots[:]

def getDataPoissonErrors(h, drawZeroBins=False, drawXbars=False):
    xaxis = h.GetXaxis()
    q=(1-0.6827)/2.;
    points = []
    errors = []
    for i in xrange(h.GetNbinsX()):
        N = h.GetBinContent(i+1);
        dN = h.GetBinError(i+1);
        if drawZeroBins or N > 0:
            if N > 0 and dN > 0 and abs(dN**2/N-1) > 1e-4: 
                #print "Hey, this is not Poisson to begin with! %.2f, %.2f, neff = %.2f, yscale = %.5g" % (N, dN, (N/dN)**2, (dN**2/N))
                yscale = (dN**2/N)
                N = (N/dN)**2
            else:
                yscale = 1
            x = xaxis.GetBinCenter(i+1);
            points.append( (x,yscale*N) )
            EYlow  = (N-ROOT.ROOT.Math.chisquared_quantile_c(1-q,2*N)/2.) if N > 0 else 0
            EYhigh = ROOT.ROOT.Math.chisquared_quantile_c(q,2*(N+1))/2.-N;
            EXhigh, EXlow = (xaxis.GetBinUpEdge(i+1)-x, x-xaxis.GetBinLowEdge(i+1)) if drawXbars else (0,0)
            errors.append( (EXlow,EXhigh,yscale*EYlow,yscale*EYhigh) )
    ret = ROOT.TGraphAsymmErrors(len(points))
    ret.SetName(h.GetName()+"_graph")
    for i,((x,y),(EXlow,EXhigh,EYlow,EYhigh)) in enumerate(zip(points,errors)):
        ret.SetPoint(i, x, y)
        ret.SetPointError(i, EXlow,EXhigh,EYlow,EYhigh)
    ret.SetLineWidth(h.GetLineWidth())
    ret.SetLineColor(h.GetLineColor())
    ret.SetLineStyle(h.GetLineStyle())
    ret.SetMarkerSize(h.GetMarkerSize())
    ret.SetMarkerColor(h.GetMarkerColor())
    ret.SetMarkerStyle(h.GetMarkerStyle())
    return ret

def PrintHisto(h):
    if not h:
        return
    print h.GetName()
    c=[]
    if "TH1" in h.ClassName():
        for i in xrange(h.GetNbinsX()):
            c.append((h.GetBinContent(i+1),h.GetBinError(i+1)))
    elif "TH2" in h.ClassName():
        for i in xrange(h.GetNbinsX()):
            for j in xrange(h.GetNbinsY()):
                c.append((h.GetBinContent(i+1,j+1),h.GetBinError(i+1,j+1)))
    else:
        print 'not th1 or th2'
    print c

def doSpam(text,x1,y1,x2,y2,align=12,fill=False,textSize=0.033,_noDelete={}):
    cmsprel = ROOT.TPaveText(x1,y1,x2,y2,"NDC");
    cmsprel.SetTextSize(textSize);
    cmsprel.SetFillColor(0);
    cmsprel.SetFillStyle(1001 if fill else 0);
    cmsprel.SetLineStyle(2);
    cmsprel.SetLineColor(0);
    cmsprel.SetTextAlign(align);
    cmsprel.SetTextFont(42);
    cmsprel.AddText(text);
    cmsprel.Draw("same");
    _noDelete[text] = cmsprel; ## so it doesn't get deleted by PyROOT
    return cmsprel

def doTinyCmsPrelim(textLeft="_default_",textRight="_default_",hasExpo=False,textSize=0.033,lumi=None, xoffs=0, options=None, doWide=False):
    if textLeft  == "_default_": textLeft  = options.lspam
    if textRight == "_default_": textRight = options.rspam
    if lumi      == None       : lumi      = options.lumi
    if   lumi > 3.54e+1: lumitext = "%.0f fb^{-1}" % lumi
    elif lumi > 3.54e+0: lumitext = "%.1f fb^{-1}" % lumi
    elif lumi > 3.54e-1: lumitext = "%.2f fb^{-1}" % lumi
    elif lumi > 3.54e-2: lumitext = "%.0f pb^{-1}" % (lumi*1000)
    elif lumi > 3.54e-3: lumitext = "%.1f pb^{-1}" % (lumi*1000)
    else               : lumitext = "%.2f pb^{-1}" % (lumi*1000)
    lumitext = "%.1f fb^{-1}" % lumi
    textLeft = textLeft.replace("%(lumi)",lumitext)
    textRight = textRight.replace("%(lumi)",lumitext)
    if textLeft not in ['', None]:
        doSpam(textLeft, (.28 if hasExpo else 0.07 if doWide else .16)+xoffs, .955, .60+xoffs, .995, align=12, textSize=textSize)
    if textRight not in ['', None]:
        doSpam(textRight,(0.5 if doWide else .58)+xoffs, .955, .98+xoffs, .995, align=32, textSize=textSize)

def reMax(hist,hist2,islog,factorLin=1.3,factorLog=2.0,doWide=False):
    if  hist.ClassName() == 'THStack':
        hist = hist.GetHistogram()
    max0 = hist.GetMaximum()
    max2 = hist2.GetMaximum()*(factorLog if islog else factorLin)
    if hasattr(hist2,'poissonGraph'):
       for i in xrange(hist2.poissonGraph.GetN()):
          max2 = max(max2, (hist2.poissonGraph.GetY()[i] + 1.3*hist2.poissonGraph.GetErrorYhigh(i))*(factorLog if islog else factorLin))
    elif "TH1" in hist2.ClassName():
       for b in xrange(1,hist2.GetNbinsX()+1):
          max2 = max(max2, (hist2.GetBinContent(b) + 1.3*hist2.GetBinError(b))*(factorLog if islog else factorLin))
    if max2 > max0:
        max0 = max2;
        if islog: hist.GetYaxis().SetRangeUser(0.1 if doWide else 0.9, max0)
        else:     hist.GetYaxis().SetRangeUser(0,max0)

def doShadedUncertainty(h):
    ret = h.graphAsymmTotalErrors()
    ret.SetFillStyle(3244);
    ret.SetFillColor(ROOT.kGray+2)
    ret.SetMarkerStyle(0)
    ret.Draw("PE2 SAME")
    return ret

def doDataNorm(pspec,pmap):
    if "data" not in pmap: return None
    total = sum([v.Integral() for k,v in pmap.iteritems() if k != 'data' and not hasattr(v,'summary')])
    sig = pmap["data"].Clone(pspec.name+"_data_norm")
    sig.SetFillStyle(0)
    sig.SetLineColor(1)
    sig.SetLineWidth(3)
    sig.SetLineStyle(2)
    if sig.Integral() > 0:
        sig.Scale(total/sig.Integral())
    sig.Draw("HIST SAME")
    return sig

def doStackSignalNorm(pspec,pmap,individuals,extrascale=1.0,norm=True):
    total = sum([v.Integral() for k,v in pmap.iteritems() if k != 'data' and not hasattr(v,'summary')])
    if options.noStackSig:
        total = sum([v.Integral() for k,v in pmap.iteritems() if not hasattr(v,'summary') and mca.isBackground(k) ])
    if individuals:
        sigs = []
        for sig in [pmap[x] for x in mca.listSignals() if pmap.has_key(x) and pmap[x].Integral() > 0]:
            sig = sig.Clone(sig.GetName()+"_norm")
            sig.SetFillStyle(0)
            sig.SetLineColor(sig.GetFillColor())
            sig.SetLineWidth(4)
            if norm: sig.Scale(total*extrascale/sig.Integral())
            sig.Draw("HIST SAME")
            sigs.append(sig)
        return sigs
    else:
        sig = None
        if "signal" in pmap: sig = pmap["signal"].Clone(pspec.name+"_signal_norm")
        else: 
            sigs = [pmap[x] for x in mca.listBackgrounds() if pmap.has_key(x) and pmap[x].Integral() > 0]
            sig = sigs[0].Clone(sigs.GetName()+"_norm")
        sig.SetFillStyle(0)
        sig.SetLineColor(206)
        sig.SetLineWidth(4)
        if norm and sig.Integral() > 0:
            sig.Scale(total*extrascale/sig.Integral())
        sig.Draw("HIST SAME")
        return [sig]

def doStackSigScaledNormData(pspec,pmap):
    if "data"       not in pmap: return (None,-1.0)
    if "signal"     not in pmap: return (None,-1.0)
    data = pmap["data"]
    sig = pmap["signal"].Clone("sig_refloat")
    bkg = None
    if "background" in pmap:
        bkg = pmap["background"]
    else:
        bkg = sig.raw().Clone(); bkg.Reset()
    sf = (data.Integral()-bkg.Integral())/sig.Integral()
    sig.Scale(sf)
    sig.Add(bkg)
    sig.SetFillStyle(0)
    sig.SetLineColor(206)
    sig.SetLineWidth(3)
    sig.SetLineStyle(2)
    sig.Draw("HIST SAME")
    return (sig,sf)

def doScaleSigNormData(pspec,pmap,mca):
    if "data"       not in pmap: return -1.0
    if "signal"     not in pmap: return -1.0
    data = pmap["data"]
    sig = pmap["signal"].Clone("sig_refloat")
    bkg = None
    if "background" in pmap:
        bkg = pmap["background"]
    else:
        bkg = sig.raw().Clone(); bkg.Reset()
    sf = (data.Integral()-bkg.Integral())/sig.Integral()
    signals = [ "signal" ] + mca.listSignals()
    for p,h in pmap.iteritems():
        if p in signals: h.Scale(sf)
    pspec.setLog("ScaleSig", [ "Signal processes scaled by %g" % sf ] )
    return sf

def doScaleBkgNormData(pspec,pmap,mca,list = []):
    if "data"       not in pmap: return -1.0
    if "background" not in pmap: return -1.0
    if any([l not in pmap for l in list]): return -1.0
    data = pmap["data"]
    bkg  = pmap["background"]
    int = sum([pmap[l].Integral() for l in list])
    rm = bkg.Integral() - int
    sf = (data.Integral() - rm) / int
    bkgs = ["background"] + list
    for p,h in pmap.iteritems():
        if p in bkgs: h.Scale(sf)
    return sf


def doNormFit(pspec,pmap,mca,saveScales=False):
    global _global_workspaces
    if "data" not in pmap: return None 
    # suppress roofit messages
    gKill = ROOT.RooMsgService.instance().globalKillBelow()
    ROOT.RooMsgService.instance().setGlobalKillBelow(ROOT.RooFit.WARNING)
    # create an empty workspace
    w = ROOT.RooWorkspace("w","w")
    w.nodelete = []
    _global_workspaces.append(w)
    # get the data, deal with non-empty bins where the MC prediction is zero
    hmc = mergePlots('htemp', [v for (k,v) in pmap.iteritems() if k != 'data'])
    hdata = pmap['data'].raw(); hdata.killbins = False
    for b in xrange(1,hmc.GetNbinsX()+2):
        if hdata.GetBinContent(b) > 0 and hmc.GetBinContent(b) == 0:
            if not hdata.killbins:
                hdata = hdata.Clone()
                hdata.killbins = True
            for b2 in xrange(b-1,0,-1):
                if hmc.GetBinContent(b2) > 0:
                    hdata.SetBinContent(b2, hdata.GetBinContent(b2) + hdata.GetBinContent(b))
                    hdata.SetBinContent(b, 0)
                    break
            if hdata.GetBinContent(b) > 0:
                for b2 in xrange(b+1,hmc.GetNbinsX()+2):
                    if hmc.GetBinContent(b2) > 0:
                        hdata.SetBinContent(b2, hdata.GetBinContent(b2) + hdata.GetBinContent(b))
                        hdata.SetBinContent(b, 0)
                        break
            if hdata.GetBinContent(b) > 0: hdata.SetBinContent(b, 0)
        if hdata.killbins: 
            print "WARNING: data has been modified to avoid non-zero observations for zero expectations in some bins"
    # create the nuisances
    nuisances = hmc.getVariationList()
    nuisanceList = ROOT.RooArgList()
    constraints = ROOT.RooArgList()
    for nuisance in nuisances:
        if nuisance.endswith("_lnU"):
            x = w.factory("%s[0,-1,1]" % nuisance);
        else:
            x = w.factory("Gaussian::%sPdf(%s[0,-7,7],0,1)" % (nuisance, nuisance));
            constraints.add(x)
        w.nodelete.append(x)
        nuisanceList.add(w.var(nuisance))
    # roofitize templates 
    roofit = roofitizeReport(pmap, w, xvarName=pspec.name, density=pspec.getOption('Density',False))
    # create the data
    obs = ROOT.RooArgList(roofit.xvar)
    roodata = ROOT.RooDataHist("data","data", obs, roofit.hist2roofit(hdata))
    pdfs   = ROOT.RooArgList()
    coeffs = ROOT.RooArgList()
    procNormMap = {}
    pois = addMyPOIs(roofit, pmap, mca)
    for p in mca.listBackgrounds(allProcs=True) + mca.listSignals(allProcs=True):
        if p not in pmap: continue
        if pmap[p].Integral() <= 0: continue
        (pdf,norm) = pmap[p].rooFitPdfAndNorm()
        if mca.getProcessOption(p,'FreeFloat',False) or pmap[p].hasVariations():
            procNormMap[p] = norm.getVal()
        pdfs.add(pdf)
        coeffs.add(norm)
    addpdf = ROOT.RooAddPdf("tot","",pdfs,coeffs,False)
    model  = addpdf
    if constraints.getSize() > 0:
        constraints.add(addpdf)
        model = ROOT.RooProdPdf("prod","",constraints)
    result = model.fitTo( roodata, ROOT.RooFit.Save(1) )
    postfit = PostFitSetup(fitResult=result)
    for k,h in pmap.iteritems():
        if k != "data" and h.Integral() > 0:
            h.setPostFitInfo(postfit,True)
    if saveScales:
        postfit._roofitContext = roofit # so it's not deleted
        mca._postFit = postfit
    fitlog = []
    for p in mca.listBackgrounds(allProcs=True) + mca.listSignals(allProcs=True):
        if p in pmap and p in procNormMap:
           norm0 = procNormMap[p]
           sf    = pmap[p].Integral()/norm0
           sferr = pmap[p].integralSystError()/norm0
           fitlog.append("Process %s scaled by %.3f +/- %.3f [ rel: %.3f ]" % (p,sf,sferr,sferr/sf if sf else 0))
           if saveScales: print fitlog[-1]
        # no need to recompute totals as they are also roofitized
    fitlog.append("")
    if pois:
        fitlog += [ "", "---- POI ----" ] 
        poilength = max(len(p) for p in pois)
        for poi in sorted(pois):
           fitlog.append("%-*s : % .3f +/- %.3f" % (poilength, poi, w.var(poi).getVal(), w.var(poi).getError()))
    if nuisances:
        fitlog += [ "", "---- NUISANCES ----" ] 
        nuisancelength = max(len(p) for p in nuisances)
        for nuis in sorted(nuisances):
           fitlog.append("%-*s : % .3f +/- %.3f" % (nuisancelength, nuis, w.var(nuis).getVal(), w.var(nuis).getError()))
    pspec.setLog("Fitting", fitlog)
    ROOT.RooMsgService.instance().setGlobalKillBelow(gKill)
    return postfit

def doRatioHists(pspec,pmap,total,maxRange,fixRange=False,fitRatio=None,errorsOnRef=True,ratioNums="signal",ratioDen="background",ylabel="Data/pred.",yndiv=505,doWide=False,showStatTotLegend=False,textSize=0.035):
    numkeys = [ "data" ]
    if "data" not in pmap: 
        if len(pmap) >= 2 and ratioDen in pmap:
            numkeys = []
            for p in pmap.iterkeys():
                for s in ratioNums.split(","):
                    if re.match(s,p): 
                        numkeys.append(p)
                        break
            if len(numkeys) == 0:
                return (None,None,None,None)
            # do this first
            total.GetXaxis().SetLabelOffset(999) ## send them away
            total.GetXaxis().SetTitleOffset(999) ## in outer space
            total.GetYaxis().SetTitleSize(0.06)
            total.GetYaxis().SetTitleOffset(0.75 if doWide else 1.48)
            total.GetYaxis().SetLabelSize(0.05)
            total.GetYaxis().SetLabelOffset(0.007)
            # then we can overwrite total with background
            numkey = 'signal'
            total     = pmap[ratioDen]
        else:    
            return (None,None,None,None)
    ratios = [] #None
    for numkey in numkeys:
        if hasattr(pmap[numkey], 'poissonGraph'):
            ratio = pmap[numkey].poissonGraph.Clone("data_div"); 
            for i in xrange(ratio.GetN()):
                x    = ratio.GetX()[i]
                div  = total.GetBinContent(total.GetXaxis().FindBin(x))
                ratio.SetPoint(i, x, ratio.GetY()[i]/div if div > 0 else 0)
                ratio.SetPointError(i, ratio.GetErrorXlow(i), ratio.GetErrorXhigh(i), 
                                       ratio.GetErrorYlow(i)/div  if div > 0 else 0, 
                                       ratio.GetErrorYhigh(i)/div if div > 0 else 0) 
        else:
            ratio = pmap[numkey].Clone("data_div"); 
            ratio.Divide(total.raw())
        ratios.append(ratio)
    unity  = total.raw().Clone("")
    unityErr  = total.graphAsymmTotalErrors(relative=True)
    unityErr0 = total.graphAsymmTotalErrors(toadd=[],relative=True)
    rmin, rmax =  1,1
    for b in xrange(1,unity.GetNbinsX()+1):
        e,n = unity.GetBinError(b), unity.GetBinContent(b)
        unity.SetBinContent(b, 1 if n > 0 else 0)
        unity.SetBinError(b, 0)
        if not errorsOnRef: 
            raise RuntimeError("Not implemented yet with histoWithNuisances")
    rmin = min(1-2*unityErr.GetErrorYlow(b)  for b in xrange(unityErr.GetN())) if unityErr.GetN() else 1
    rmax = max(1+2*unityErr.GetErrorYhigh(b) for b in xrange(unityErr.GetN())) if unityErr.GetN() else 1
    for ratio in ratios:
        if ratio.ClassName() != "TGraphAsymmErrors":
            for b in xrange(1,unity.GetNbinsX()+1):
                if ratio.GetBinContent(b) == 0: continue
                rmin = min( rmin, ratio.GetBinContent(b) - 2*ratio.GetBinError(b) ) 
                rmax = max( rmax, ratio.GetBinContent(b) + 2*ratio.GetBinError(b) )  
        else:
            for i in xrange(ratio.GetN()):
                rmin = min( rmin, ratio.GetY()[i] - 2*ratio.GetErrorYlow(i)  ) 
                rmax = max( rmax, ratio.GetY()[i] + 2*ratio.GetErrorYhigh(i) )  
    if rmin < maxRange[0] or fixRange: rmin = maxRange[0]; 
    if rmax > maxRange[1] or fixRange: rmax = maxRange[1];
    if (rmax > 3 and rmax <= 3.4): rmax = 3.4
    if (rmax > 2 and rmax <= 2.4): rmax = 2.4
    unity.SetMarkerStyle(1);
    unity.SetMarkerColor(ROOT.kBlue-7);
    unityErr.SetFillStyle(1001);
    unityErr.SetFillColor(ROOT.kCyan);
    unityErr.SetMarkerStyle(1);
    unityErr.SetMarkerColor(ROOT.kCyan);
    unityErr0.SetFillStyle(1001);
    unityErr0.SetFillColor(ROOT.kBlue-7);
    unityErr0.SetMarkerStyle(1);
    unityErr0.SetMarkerColor(ROOT.kBlue-7);
    ROOT.gStyle.SetErrorX(0.5);
    unity.Draw("AXIS");
    if errorsOnRef:
        unityErr.Draw("E2");
    if fitRatio != None and len(ratios) == 1:
        from CMGTools.TTHAnalysis.tools.plotDecorations import fitTGraph
        fitTGraph(ratio,order=fitRatio)
        unityErr.SetFillStyle(3013);
        unityErr0.SetFillStyle(3013);
        if errorsOnRef:
            unityErr0.Draw("E2 SAME");
    else:
        if errorsOnRef:
            unityErr0.Draw("E2 SAME");
    unity.Draw("AXIS SAME");
    rmin = float(pspec.getOption("RMin",rmin))
    rmax = float(pspec.getOption("RMax",rmax))
    unity.GetYaxis().SetRangeUser(rmin,rmax);
    unity.GetXaxis().SetTitleFont(42)
    unity.GetXaxis().SetTitleSize(0.14)
    unity.GetXaxis().SetTitleOffset(1.0)
    unity.GetXaxis().SetLabelFont(42)
    unity.GetXaxis().SetLabelSize(0.1)
    unity.GetXaxis().SetLabelOffset(0.015)
    unity.GetYaxis().SetNdivisions(yndiv)
    unity.GetYaxis().SetTitleFont(42)
    unity.GetYaxis().SetTitleSize(0.14)
    offset = 0.32 if doWide else 0.62
    unity.GetYaxis().SetTitleOffset(offset)
    unity.GetYaxis().SetLabelFont(42)
    unity.GetYaxis().SetLabelSize(0.11)
    unity.GetYaxis().SetLabelOffset(0.01)
    unity.GetYaxis().SetDecimals(True) 
    unity.GetYaxis().SetTitle(ylabel)
    total.GetXaxis().SetLabelOffset(999) ## send them away
    total.GetXaxis().SetTitleOffset(999) ## in outer space
    total.GetYaxis().SetTitleSize(0.06)
    total.GetYaxis().SetTitleOffset(0.75 if doWide else 1.48)
    total.GetYaxis().SetLabelSize(0.05)
    total.GetYaxis().SetLabelOffset(0.007)
    binlabels = pspec.getOption("xBinLabels","")
    if binlabels != "" and len(binlabels.split(",")) == unity.GetNbinsX():
        blist = binlabels.split(",")
        for i in range(1,unity.GetNbinsX()+1): 
            unity.GetXaxis().SetBinLabel(i,blist[i-1]) 
        unity.GetXaxis().SetLabelSize(0.15*(textSize/0.035))
    #ratio.SetMarkerSize(0.7*ratio.GetMarkerSize()) # no it is confusing
    binlabels = pspec.getOption("xBinLabels","")
    if binlabels != "" and len(binlabels.split(",")) == unity.GetNbinsX():
        blist = binlabels.split(",")
        for i in range(1,unity.GetNbinsX()+1): 
            unity.GetXaxis().SetBinLabel(i,blist[i-1]) 
    #$ROOT.gStyle.SetErrorX(0.0);
    line = ROOT.TLine(unity.GetXaxis().GetXmin(),1,unity.GetXaxis().GetXmax(),1)
    line.SetLineWidth(2);
    line.SetLineColor(58);
    line.Draw("L")
    for ratio in ratios:
        ratio.Draw("E SAME" if ratio.ClassName() != "TGraphAsymmErrors" else "PZ SAME");
    leg0 = ROOT.TLegend(0.12 if doWide else 0.2, 0.84, 0.25 if doWide else 0.45, 0.94)
    leg0.SetFillColor(0)
    leg0.SetShadowColor(0)
    leg0.SetLineColor(0)
    leg0.SetTextFont(42)
    leg0.SetTextSize(textSize*0.7/0.3)
    leg0.AddEntry(unityErr0, "stat. unc.", "F")
    if showStatTotLegend: leg0.Draw()
    leg1 = ROOT.TLegend(0.25 if doWide else 0.45, 0.84, 0.38 if doWide else 0.7, 0.94)
    leg1.SetFillColor(0)
    leg1.SetShadowColor(0)
    leg1.SetLineColor(0)
    leg1.SetTextFont(42)
    leg1.SetTextSize(textSize*0.7/0.3)
    leg1.AddEntry(unityErr, "total unc.", "F")
    if showStatTotLegend: leg1.Draw()
    global legendratio0_, legendratio1_
    legendratio0_ = leg0
    legendratio1_ = leg1
    return (ratios, unity,(unityErr,unityErr0), line)

def doStatTests(total,data,test,legendCorner):
    #print "Stat tests for %s:" % total.GetName()
    #ksprob = data.KolmogorovTest(total,"XN")
    #print "\tKS  %.4f" % ksprob
    chi2l, chi2p, chi2gq, chi2lp, nb = 0, 0, 0, 0, 0
    for b in xrange(1,data.GetNbinsX()+1):
        oi = data.GetBinContent(b)
        ei = total.GetBinContent(b)
        dei = total.GetBinError(b)
        if ei <= 0: continue
        nb += 1
        chi2l += - 2*(oi*log(ei/oi)+(oi-ei) if oi > 0 else -ei)
        chi2p += (oi-ei)**2 / ei
        chi2gq += (oi-ei)**2 /(ei+dei**2)
        #chi2lp +=
    print "\tc2p  %.4f (%6.2f/%3d)" % (ROOT.TMath.Prob(chi2p,  nb), chi2p,  nb)
    print "\tc2l  %.4f (%6.2f/%3d)" % (ROOT.TMath.Prob(chi2l,  nb), chi2l,  nb)
    print "\tc2qg %.4f (%6.2f/%3d)" % (ROOT.TMath.Prob(chi2gq, nb), chi2gq, nb)
    #print "\tc2lp %.4f (%6.2f/%3d)" % (ROOT.TMath.Prob(chi2lp, nb), chi2lp, nb)
    chi2s = { "chi2l":chi2l, "chi2p":chi2p, "chi2gq":chi2gq, "chi2lp":chi2lp }
    if test in chi2s:
        chi2 = chi2s[test]
        pval = ROOT.TMath.Prob(chi2, nb)
        chi2fmt = ("%.1f" if nb < 10 else "%.0f") % chi2
        text = ("#chi^{2} %s/%d p-value %.3f" if pval < 0.02 else "#chi^{2} %s/%d p-value %.2f") % (chi2fmt, nb, pval)
    else:
        text = "Unknown test %s" % test
    if legendCorner == "TR":
        doSpam(text, .23, .85, .48, .93, align=12, textSize=0.05)
    elif legendCorner == "TL":
        doSpam(text, .75, .85, .93, .93, align=32, textSize=0.05)



legend_ = None;
def doLegend(pmap,mca,corner="TR",textSize=0.035,cutoff=1e-2,cutoffSignals=True,mcStyle="F",legWidth=0.18,legBorder=True,signalPlotScale=None,totalError=None,header="",doWide=False,columns=1):
        if (corner == None): return
        total = sum([x.Integral() for x in pmap.itervalues()])
        sigEntries = []; bgEntries = []
        for p in mca.listSignals(allProcs=True):
            if mca.getProcessOption(p,'HideInLegend',False): continue
            if p in pmap and pmap[p].Integral() > (cutoff*total if cutoffSignals else 0): 
                lbl = mca.getProcessOption(p,'Label',p)
                if signalPlotScale and signalPlotScale!=1: 
                    lbl=lbl+" x "+("%d"%signalPlotScale if floor(signalPlotScale)==signalPlotScale else "%.2f"%signalPlotScale)
                myStyle = mcStyle if type(mcStyle) == str else mcStyle[0]
                sigEntries.append( (pmap[p],lbl,myStyle) )
        backgrounds = mca.listBackgrounds(allProcs=True)
        for p in backgrounds:
            if mca.getProcessOption(p,'HideInLegend',False): continue
            if p in pmap and pmap[p].Integral() >= cutoff*total: 
                lbl = mca.getProcessOption(p,'Label',p)
                myStyle = mcStyle if type(mcStyle) == str else mcStyle[1]
                bgEntries.append( (pmap[p],lbl,myStyle) )
        nentries = len(sigEntries) + len(bgEntries) + ('data' in pmap)

        height = (.20 + textSize*max(nentries-3,0))
        if columns > 1: height = 1.3*height/columns
        (x1,y1,x2,y2) = (0.97-legWidth if doWide else .85-legWidth, .9 - height, .90, .91)
        if corner == "TR":
            (x1,y1,x2,y2) = (0.97-legWidth if doWide else .85-legWidth, .9 - height, .90, .91)
        elif corner == "TC":
            (x1,y1,x2,y2) = (.5, .9 - height, .55+legWidth, .91)
        elif corner == "TL":
            (x1,y1,x2,y2) = (.2, .9 - height, .25+legWidth, .91)
        elif corner == "BR":
            (x1,y1,x2,y2) = (.85-legWidth, .16 + height, .90, .15)
        elif corner == "BC":
            (x1,y1,x2,y2) = (.5, .16 + height, .5+legWidth, .15)
        elif corner == "BL":
            (x1,y1,x2,y2) = (.2, .16 + height, .2+legWidth, .15)

        leg = ROOT.TLegend(x1,y1,x2,y2)
        if header: leg.SetHeader(header.replace("\#", "#"))
        leg.SetFillColor(0)
        leg.SetShadowColor(0)
        if header: leg.SetHeader(header.replace("\#", "#"))       
        if not legBorder:
            leg.SetLineColor(0)
        leg.SetTextFont(42)
        leg.SetTextSize(textSize)
        leg.SetNColumns(columns)
        entries = []
        if 'data' in pmap: 
            entries.append((pmap['data'].raw(), mca.getProcessOption('data','Label','Data', noThrow=True), 'LPE'))
        for (plot,label,style) in sigEntries: entries.append((plot.raw(),label,style))
        for (plot,label,style) in  bgEntries: entries.append((plot.raw(),label,style))
        if totalError:  entries.append((totalError,"Total unc.","F"))
        nrows = int(ceil(len(entries)/float(columns)))
        for r in xrange(nrows):
            for c in xrange(columns):
                i = r+c*nrows
                if i >= len(entries): break
                leg.AddEntry(*entries[i])
        leg.Draw()
        ## assign it to a global variable so it's not deleted
        global legend_
        legend_ = leg 
        return leg

class PlotMaker:
    def __init__(self,tdir,options):
        self._options = options
        self._dir = tdir
        ROOT.gROOT.ProcessLine(".x tdrstyle.cc")
        ROOT.gROOT.ProcessLine(".L smearer.cc+")
        ROOT.gStyle.SetOptStat(0)
        ROOT.gStyle.SetOptTitle(0)
        if self._options.perBin and not "txt" in self._options.printPlots: raise RuntimeError, "Error: cannot print yields per bin if txt option not given" 
 
    def run(self,mca,cuts,plots,makeStack=True,makeCanvas=True):
        if self._options.wideplot: ROOT.gStyle.SetTitleYOffset(0.55)
        sets = [ (None, 'all cuts', cuts.allCuts()) ]
        if not self._options.final:
            allcuts = cuts.sequentialCuts()
            if self._options.nMinusOne or self._options.nMinusOneInverted: 
                if not self._options.nMinusOneSelection:
                    allcuts = cuts.nMinusOneCuts(inverted=self._options.nMinusOneInverted)+[None] # add a dummy entry since we use allcuts[:-1] below
                else:
                    allcuts = cuts.nMinusOneSelectedCuts(self._options.nMinusOneSelection,inverted=self._options.nMinusOneInverted)+[None]
            for i,(cn,cv) in enumerate(allcuts[:-1]): # skip the last one which is equal to all cuts
                cnsafe = "cut_%02d_%s" % (i, re.sub("[^a-zA-Z0-9_.]","",cn.replace(" ","_")))
                sets.append((cnsafe,cn,cv))
        elist = (self._options.elist == True) or (self._options.elist == 'auto' and len(plots.plots()) > 2)
        for subname, title, cut in sets:
            print "cut set: ",title
            if elist: mca.applyCut(cut)
            dir = self._dir
            if subname:
                if self._dir.Get(subname):
                    dir = self._dir.Get(subname)
                else:
                    dir = self._dir.mkdir(subname,title)
            dir.cd()
            pspecs = plots.plots()
            if self._options.preFitData:
                matchspec = [ p for p in pspecs if p.name == self._options.preFitData ]
                if not matchspec: raise RuntimeError, "Error: plot %s not found" % self._options.preFitData
                pspecs = matchspec + [ p for p in pspecs if p.name != self._options.preFitData ]
            for pspec in pspecs:
                print "    plot: ",pspec.name
                pmap = mca.getPlots(pspec,cut,makeSummary=True,closeTreeAfter=True)
                #
                # blinding policy
                blind = pspec.getOption('Blinded','None') if 'data' in pmap else 'None'
                if self._options.unblind == True: blind = 'None'
                xblind = [9e99,-9e99]
                if re.match(r'(bin|x)\s*([<>]?)\s*(\+|-)?\d+(\.\d+)?|(\+|-)?\d+(\.\d+)?\s*<\s*(bin|x)\s*<\s*(\+|-)?\d+(\.\d+)?', blind):
                    xfunc = (lambda h,b: b)             if 'bin' in blind else (lambda h,b : h.GetXaxis().GetBinCenter(b));
                    test  = eval("lambda bin : "+blind) if 'bin' in blind else eval("lambda x : "+blind) 
                    hdata = pmap['data']
                    for b in xrange(1,hdata.GetNbinsX()+1):
                        if test(xfunc(hdata,b)):
                            #print "blinding bin %d, x = [%s, %s]" % (b, hdata.GetXaxis().GetBinLowEdge(b), hdata.GetXaxis().GetBinUpEdge(b))
                            hdata.SetBinContent(b,0)
                            hdata.SetBinError(b,0)
                            xblind[0] = min(xblind[0],hdata.GetXaxis().GetBinLowEdge(b))
                            xblind[1] = max(xblind[1],hdata.GetXaxis().GetBinUpEdge(b))
                    #print "final blinded range x = [%s, %s]" % (xblind[0],xblind[1])
                elif blind != "None":
                    raise RuntimeError, "Unrecongnized value for 'Blinded' option, stopping here"
                #
                # Pseudo-data?
                if self._options.pseudoData: # to be fixed with HistoWithNuisances
                    if "data" in pmap: raise RuntimeError, "Can't use --pseudoData if there's also real data (maybe you want --xp data?)"
                    if "background" in self._options.pseudoData:
                        pdata = pmap["background"]
                        pdata = pdata.Clone(str(pdata.GetName()).replace("_background","_data"))
                    elif "all" in self._options.pseudoData:
                        pdata = pmap["background"]
                        pdata = pdata.Clone(str(pdata.GetName()).replace("_background","_data"))
                        if "signal" in pmap: pdata.Add(pmap["signal"])
                    else:
                        raise RuntimeError, "Pseudo-data option %s not supported" % self._options.pseudoData
                    if "asimov" not in self._options.pseudoData:
                        if "TH1" in pdata.ClassName():
                            for i in xrange(1,pdata.GetNbinsX()+1):
                                pdata.SetBinContent(i, ROOT.gRandom.Poisson(pdata.GetBinContent(i)))
                                pdata.SetBinError(i, sqrt(pdata.GetBinContent(i)))
                        elif "TH2" in pdata.ClassName():
                            for ix in xrange(1,pdata.GetNbinsX()+1):
                              for iy in xrange(1,pdata.GetNbinsY()+1):
                                pdata.SetBinContent(ix, iy, ROOT.gRandom.Poisson(pdata.GetBinContent(ix, iy)))
                                pdata.SetBinError(ix, iy, sqrt(pdata.GetBinContent(ix, iy)))
                        else:
                            raise RuntimeError, "Can't make pseudo-data for %s" % pdata.ClassName()
                    pmap["data"] = pdata
                #
                if not makeStack: 
                    for k,v in pmap.iteritems():
                        if hasattr(v,'writeToFile'):
                            v.writeToFile(dir)
                        else:
                            if v.InheritsFrom("TH1"): v.SetDirectory(dir) 
                            dir.WriteTObject(v.raw())
                    continue
                #
                if self._options.scaleSignalToData: 
                    self._sf = doScaleSigNormData(pspec,pmap,mca)
                elif self._options.scaleBackgroundToData != []: 
                    self._sf = doScaleBkgNormData(pspec,pmap,mca,self._options.scaleBackgroundToData)
                elif self._options.fitData: 
                    doNormFit(pspec,pmap,mca)
                elif self._options.preFitData and pspec.name == self._options.preFitData:
                    doNormFit(pspec,pmap,mca,saveScales=True)
                #
                for k,v in pmap.iteritems():
                    if hasattr(v,'writeToFile'):
                        v.writeToFile(dir)
                    else:
                        if v.InheritsFrom("TH1"): v.SetDirectory(dir) 
                        dir.WriteTObject(v.raw())
                #
                self.printOnePlot(mca,pspec,pmap,
                                  xblind=xblind,
                                  makeCanvas=makeCanvas,
                                  outputDir=dir,
                                  printDir=self._options.printDir+(("/"+subname) if subname else ""))
                if getattr(mca,'_altPostFits',None):
                    roofit = roofitizeReport(pmap)
                    if self._options.processesToPeg == []:
                        hasR = False
                        for pfs in mca._altPostFits.itervalues():
                            if pfs.fitResult.floatParsFinal().find("r"):
                                hasR = True
                        if hasR: addExternalDefaultPOI(roofit,pmap,mca,"r")
                    else:
                        addExternalPhysicsModelPOIs(roofit,pmap,mca,self._options.processesToPeg)
                    for key,pfs in mca._altPostFits.iteritems():
                        for k,h in pmap.iteritems():
                            if k != "data":
                                h.setPostFitInfo(pfs,True)
                        subdir = dir.GetDirectory("post_"+key);
                        if not subdir: subdir = dir.mkdir("post_"+key)
                        if getattr(pfs, 'label', None):
                            legendHeaderBackup = self._options.legendHeader
                            self._options.legendHeader = pfs.label
                        self.printOnePlot(mca,pspec,pmap,
                                          xblind=xblind,
                                          makeCanvas=makeCanvas,
                                          outputDir=subdir,
                                          printDir=self._options.printDir+(("/"+subname) if subname else "")+"/post_"+key)
                        if getattr(pfs, 'label', None):
                            self._options.legendHeader = legendHeaderBackup
                if pspec.getOption("SlicesY",None):
                    h0 = pmap.values()[0]
                    for iy in xrange(1,h0.GetNbinsY()+1):
                        postfix = "_"+(pspec.getOption("SlicesY") % (h0.GetYaxis().GetBinLowEdge(iy), h0.GetYaxis().GetBinUpEdge(iy)))
                        bins_slice = pspec.bins.split("*",1) if "[" == pspec.bins[0] else ",".join(pspec.bins.split(",")[:3])
                        pspec_slice = PlotSpec(pspec.name+postfix, pspec.expr, bins_slice, pspec.opts)
                        pmap_slice = dict( (k,h.projectionX(h.GetName()+postfix,iy,iy)) for (k,h) in pmap.iteritems() )
                        allprocs = mca.listSignals(True)+mca.listBackgrounds(True)+["data"]
                        for k,h in pmap_slice.iteritems():
                            if k in allprocs:
                                stylePlot(h,pspec_slice, lambda opt, deft: mca.getProcessOption(k, opt, deft))
                        self.printOnePlot(mca,pspec_slice,pmap_slice,
                                          xblind=xblind, makeCanvas=makeCanvas, outputDir=dir,
                                          printDir=self._options.printDir+(("/"+subname) if subname else ""))
            if elist: mca.clearCut()

    def printOnePlot(self,mca,pspec,pmapIn,mytotal=None,makeCanvas=True,outputDir=None,printDir=None,xblind=[9e99,-9e99],extraProcesses=[],plotmode="auto",outputName=None):
                pmap = dict( (k, h if isinstance(h,HistoWithNuisances) else HistoWithNuisances(h)) for (k,h) in pmapIn.iteritems() )
                options = self._options
                if printDir == None: printDir=self._options.printDir
                if outputDir == None: outputDir = self._dir
                if plotmode == "auto": plotmode = self._options.plotmode
                if outputName == None: outputName = pspec.name
                stack = ROOT.THStack(outputName+"_stack",outputName)
                if mytotal != None:
                    total = mytotal
                else:
                    hists = [v for k,v in pmap.iteritems() if k != 'data'  and v.Integral() > 0 ]
                    if not hists: hists = [v for k,v in pmap.iteritems() if k != 'data' ]
                    total = hists[0].Clone(outputName+"_total"); total.Reset()
                if plotmode == "norm": 
                    if 'data' in pmap:
                        total.GetYaxis().SetTitle(total.GetYaxis().GetTitle()+" (normalized)")
                    else:
                        total.GetYaxis().SetTitle("density/bin")
                    total.GetYaxis().SetDecimals(True)

                for p in itertools.chain(reversed(mca.listBackgrounds(allProcs=True)), reversed(mca.listSignals(allProcs=True)), extraProcesses):
                    if p in pmap: 
                        plot = pmap[p]
                        #if plot.Integral() == 0:
                        #    print 'Warning: plotting histo %s with zero integral, there might be problems in the following'%p
                        if plot.Integral() < 0:
                            print 'Warning: plotting histo %s with negative integral (%f), the stack plot will probably be incorrect.'%(p,plot.Integral())
                        if 'TH1' in plot.ClassName():
                            for b in xrange(1,plot.GetNbinsX()+1):
                                if plot.GetBinContent(b)<0: print 'Warning: histo %s has bin %d with negative content (%f), the stack plot will probably be incorrect.'%(p,b,plot.GetBinContent(b))
                        elif 'TH2' in plot.ClassName():
                            for b1 in xrange(1,plot.GetNbinsX()+1):
                                for b2 in xrange(1,plot.GetNbinsY()+1):
                                    if plot.GetBinContent(b1,b2)<0: print 'Warning: histo %s has bin %d,%d with negative content (%f), the stack plot will probably be incorrect.'%(p,b1,b2,plot.GetBinContent(b1,b2))
#                        if plot.Integral() <= 0: continue
                        if mca.isSignal(p): plot.Scale(options.signalPlotScale)
                        if mca.isSignal(p) and options.noStackSig == True: 
                            plot.SetLineWidth(3)
                            plot.SetLineColor(plot.GetFillColor())
                            continue 
                        if plotmode == "stack":
                            stack.Add(plot.raw())
                            if mytotal == None: total+=plot
                        else:
                            plot.SetLineColor(plot.GetFillColor())
                            plot.SetLineWidth(3)
                            plot.SetFillStyle(0)
                            if plotmode == "norm" and (plot.ClassName()[:2] == "TH"):
                                ref = pmap['data'].Integral() if 'data' in pmap else 1.0
                                if (plot.Integral()): plot.Scale(ref/plot.Integral())
                            stack.Add(plot.raw())
                            total.SetMaximum(max(total.GetMaximum(),1.3*plot.GetMaximum()))
                        if self._options.errors and plotmode != "stack":
                            plot.SetMarkerColor(plot.GetFillColor())
                            plot.SetMarkerStyle(21)
                            plot.SetMarkerSize(1.5)
                        else:
                            plot.SetMarkerStyle(0)

                binlabels = pspec.getOption("xBinLabels","")
                if binlabels != "" and len(binlabels.split(",")) == total.GetNbinsX():
                    blist = binlabels.split(",")
                    for i in range(1,total.GetNbinsX()+1): 
                        total.GetXaxis().SetBinLabel(i,blist[i-1]) 
                        total.GetYaxis().SetLabelSize(0.05)

                if not self._options.emptyStack and stack.GetNhists() == 0:
                    print "ERROR: for %s, all histograms are empty\n " % pspec.name
                    return

                # define aspect ratio
                doWide = True if self._options.wideplot or pspec.getOption("Wide",False) else False
                plotformat = (1200,600) if doWide else (600,600)
                sf = 20./plotformat[0]
                ROOT.gStyle.SetPadLeftMargin(600.*0.18/plotformat[0])

                stack.Draw("GOFF")
                ytitle = "Events" if not self._options.printBinning else "Events / %s" %(self._options.printBinning)
                total.GetXaxis().SetTitleFont(42)
                total.GetXaxis().SetTitleSize(0.05)
                total.GetXaxis().SetTitleOffset(1.1)
                total.GetXaxis().SetLabelFont(42)
                total.GetXaxis().SetLabelSize(0.05)
                total.GetXaxis().SetLabelOffset(0.007)
                total.GetYaxis().SetTitleFont(42)
                total.GetYaxis().SetTitleSize(0.05)
                total.GetYaxis().SetTitleOffset(0.9 if doWide else 2.0)
                total.GetYaxis().SetLabelFont(42)
                total.GetYaxis().SetLabelSize(0.05)
                total.GetYaxis().SetLabelOffset(0.007)
                total.GetYaxis().SetTitle(pspec.getOption('YTitle',ytitle))
                total.GetXaxis().SetTitle(pspec.getOption('XTitle',outputName))
                total.GetXaxis().SetNdivisions(pspec.getOption('XNDiv',510))
                if outputDir: outputDir.WriteTObject(stack)
                # 
                if not makeCanvas and not self._options.printPlots: return
                doRatio = self._options.showRatio and ('data' in pmap or (plotmode != "stack")) and ("TH2" not in total.ClassName())
                islog = pspec.hasOption('Logy'); 
                if doRatio: ROOT.gStyle.SetPaperSize(20.,sf*(plotformat[1]+150))
                else:       ROOT.gStyle.SetPaperSize(20.,sf*plotformat[1])
                # create canvas
                height = plotformat[1]+150 if doRatio else plotformat[1]
                c1 = ROOT.TCanvas(outputName+"_canvas", outputName, plotformat[0], height)
                c1.SetTopMargin(c1.GetTopMargin()*options.topSpamSize);
                topsize = 0.12*600./height if doRatio else 0.06*600./height
                if self._options.doOfficialCMS: c1.SetTopMargin(topsize*1.2 if doWide else topsize)
                c1.Draw()
                p1, p2 = c1, None # high and low panes
                # set borders, if necessary create subpads
                if doRatio:
                    c1.SetWindowSize(plotformat[0] + (plotformat[0] - c1.GetWw()), (plotformat[1]+150 + (plotformat[1]+150 - c1.GetWh())));
                    p1 = ROOT.TPad("pad1","pad1",0,0.30,1,1);
                    p1.SetTopMargin(p1.GetTopMargin()*options.topSpamSize);
                    p1.SetBottomMargin(0 if options.attachRatioPanel else 0.025);
                    p1.Draw();
                    p2 = ROOT.TPad("pad2","pad2",0,0,1,0.30);
                    p2.SetTopMargin(0 if options.attachRatioPanel else 0.06);
                    p2.SetBottomMargin(0.3);
                    p2.SetFillStyle(0);
                    p2.Draw();
                    p1.cd();
                else:
                    c1.SetWindowSize(plotformat[0] + (plotformat[0] - c1.GetWw()), plotformat[1] + (plotformat[1] - c1.GetWh()));
                p1.SetLogy(islog)
                p1.SetLogz(True if pspec.hasOption('Logz') else False)
                if pspec.hasOption('Logx'):
                    p1.SetLogx(True)
                    if p2: p2.SetLogx(True)
                    total.GetXaxis().SetNoExponent(True)
                    total.GetXaxis().SetMoreLogLabels(True)
                if islog: total.SetMaximum(2*total.GetMaximum())
                if not islog: total.SetMinimum(0)
                total.Draw("HIST")
                if plotmode == "stack":
                    stack.Draw("SAME HIST")
                    total.Draw("AXIS SAME")
                else: 
                    if self._options.errors:
                        ROOT.gStyle.SetErrorX(0.5)
                        stack.Draw("SAME E NOSTACK")
                    else:
                        stack.Draw("SAME HIST NOSTACK")
                if pspec.getOption('MoreY',1.0) > 1.0:
                    total.SetMaximum(pspec.getOption('MoreY',1.0)*total.GetMaximum())
                totalError=None
                if options.showMCError:
                    totalError = doShadedUncertainty(total)
                is2D = total.InheritsFrom("TH2")
                if 'data' in pmap: 
                    if options.poisson and not is2D:
                        pdata = getDataPoissonErrors(pmap['data'], True, True)
                        pdata.Draw("PZ SAME")
                        pmap['data'].poissonGraph = pdata ## attach it so it doesn't get deleted
                    else:
                        pmap['data'].Draw("E SAME")
                    reMax(total,pmap['data'],islog,doWide=doWide)
                    if xblind[0] < xblind[1]:
                        blindbox = ROOT.TBox(xblind[0],total.GetYaxis().GetXmin(),xblind[1],total.GetMaximum())
                        blindbox.SetFillColor(ROOT.kBlue+3)
                        blindbox.SetFillStyle(3944)
                        blindbox.Draw()
                        xblind.append(blindbox) # so it doesn't get deleted
                    if options.doStatTests:
                        doStatTests(total, pmap['data'], options.doStatTests, legendCorner=pspec.getOption('Legend','TR'))
                if pspec.hasOption('YMin') and pspec.hasOption('YMax'):
                    total.GetYaxis().SetRangeUser(pspec.getOption('YMin',1.0), pspec.getOption('YMax',1.0))
                elif pspec.hasOption('YMin'):
                    total.SetMinimum(pspec.getOption('YMin'))
                if pspec.hasOption('ZMin') and pspec.hasOption('ZMax'):
                    total.GetZaxis().SetRangeUser(pspec.getOption('ZMin',1.0), pspec.getOption('ZMax',1.0))
                #if options.yrange: 
                #    total.GetYaxis().SetRangeUser(options.yrange[0], options.yrange[1])
                if options.addspam:
                    if pspec.getOption('Legend','TR')=="TL":
                        doSpam(options.addspam, .68, .855, .9, .895, align=32, textSize=(0.045 if doRatio else 0.033)*options.topSpamSize)
                    else:
                        doSpam(options.addspam, .23, .855, .6, .895, align=12, textSize=(0.045 if doRatio else 0.033)*options.topSpamSize)
                legendCutoff = pspec.getOption('LegendCutoff', 1e-5 if c1.GetLogy() else 1e-2)
                if plotmode == "norm": legendCutoff = 0 
                if plotmode == "stack":
                    if options.noStackSig: mcStyle = ("L","F")
                    else:                  mcStyle = "F"
                else: mcStyle = "L"
                doLegend(pmap,mca,corner=pspec.getOption('Legend','TR'),
                                  cutoff=legendCutoff, mcStyle=mcStyle,
                                  cutoffSignals=not(options.showSigShape or options.showIndivSigShapes or options.showSFitShape), 
                                  textSize=( (0.045 if doRatio else 0.022) if options.legendFontSize <= 0 else options.legendFontSize ),
                                  legWidth=pspec.getOption('LegendWidth',options.legendWidth), legBorder=options.legendBorder, signalPlotScale=options.signalPlotScale,
                                  header=self._options.legendHeader if self._options.legendHeader else pspec.getOption("LegendHeader", ""),
                                  doWide=doWide, totalError=totalError, columns = pspec.getOption('LegendColumns',options.legendColumns))
                if self._options.doOfficialCMS:
                    CMS_lumi.lumi_13TeV = "%.1f fb^{-1}" % self._options.lumi
                    CMS_lumi.extraText  = self._options.cmsprel
                    CMS_lumi.lumi_sqrtS = self._options.cmssqrtS
                    CMS_lumi.CMS_lumi(ROOT.gPad, 4, 0, -0.005 if doWide and doRatio else 0.01 if doWide else 0.05)
                else: 
                    doTinyCmsPrelim(hasExpo = total.GetMaximum() > 9e4 and not c1.GetLogy(),textSize=(0.045 if doRatio else 0.033)*options.topSpamSize, options=options,doWide=doWide)
                signorm = None; datnorm = None; sfitnorm = None
                if options.showSigShape or options.showIndivSigShapes or options.showIndivSigs: 
                    signorms = doStackSignalNorm(pspec,pmap,options.showIndivSigShapes or options.showIndivSigs,extrascale=options.signalPlotScale, norm=not options.showIndivSigs)
                    for signorm in signorms:
                        if outputDir: 
                            signorm.SetDirectory(outputDir); outputDir.WriteTObject(signorm)
                        reMax(total,signorm,islog,doWide=doWide)
                if options.showDatShape: 
                    datnorm = doDataNorm(pspec,pmap)
                    if datnorm != None:
                        if outputDir: 
                            datnorm.SetDirectory(outputDir); outputDir.WriteTObject(datnorm)
                        reMax(total,datnorm,islog,doWide=doWide)
                if options.showSFitShape: 
                    (sfitnorm,sf) = doStackSigScaledNormData(pspec,pmap)
                    if sfitnorm != None:
                        if outputDir: 
                            sfitnorm.SetDirectory(outputDir); outputDir.WriteTObject(sfitnorm)
                        reMax(total,sfitnorm,islog,doWide=doWide)
                if options.flagDifferences and len(pmap) == 4:
                    new = pmap['signal']
                    ref = pmap['background']
                    if "TH1" in new.ClassName():
                        for b in xrange(1,new.GetNbinsX()+1):
                            if abs(new.GetBinContent(b) - ref.GetBinContent(b)) > options.toleranceForDiff*ref.GetBinContent(b):
                                print "Plot: difference found in %s, bin %d" % (outputName, b)
                                p1.SetFillColor(ROOT.kYellow-10)
                                if p2: p2.SetFillColor(ROOT.kYellow-10)
                                break
                if makeCanvas and outputDir: outputDir.WriteTObject(c1)
                rdata,rnorm,rnorm2,rline = (None,None,None,None)
                if doRatio:
                    p2.cd(); 
                    rdata,rnorm,rnorm2,rline = doRatioHists(pspec,pmap,total, maxRange=options.maxRatioRange, fixRange=options.fixRatioRange,
                                                            fitRatio=options.fitRatio, errorsOnRef=options.errorBandOnRatio, 
                                                            ratioNums=options.ratioNums, ratioDen=options.ratioDen, ylabel=options.ratioYLabel, yndiv=options.ratioYNDiv, doWide=doWide, showStatTotLegend=options.showStatTotLegend, textSize=options.legendFontSize)
                if self._options.printPlots:
                    for ext in self._options.printPlots.split(","):
                        fdir = printDir;
                        if not os.path.exists(fdir): 
                            os.makedirs(fdir); 
                            if os.path.exists("/afs/cern.ch"): os.system("cp /afs/cern.ch/user/g/gpetrucc/php/index.php "+fdir)
                            elif os.path.exists("/pool/ciencias/"): os.system("cp /pool/ciencias/HeppyTrees/RA7/additionalReferenceCode/index.php "+fdir)
                        if ext == "txt" and self._options.perBin:
                            dump = open("%s/%s_perBin.%s" % (fdir, outputName, ext), "w")
                            maxlen = max([len(mca.getProcessOption(p,'Label',p)) for p in mca.listSignals(allProcs=True) + mca.listBackgrounds(allProcs=True)]+[7])
                            step = (plot.GetXaxis().GetXmax()-plot.GetXaxis().GetXmin())/plot.GetNbinsX()
                            bins = [plot.GetXaxis().GetXmin()+i*step for i in range(plot.GetNbinsX())]
                            fmh    = "%%-%ds" % (maxlen+1)
                            fmt    = "%9.2f +/- %9.2f (stat)"
                            dump.write(fmh % pspec.expr + " " + " ".join("%d" % (i) for i in bins) + "\n")
                            dump.write(("-"*(maxlen+45))+"\n");
                            bkgsyst = [0 for i in range(pmap["background"].GetNbinsX())]; sigsyst = bkgsyst
                            for p in mca.listSignals(allProcs=True) + mca.listBackgrounds(allProcs=True) + ["signal", "background"]:
                                if p not in pmap: continue
                                plot = pmap[p]
                                if plot.Integral() <= 0: continue
                                norm = plot.Integral()
                                if p not in ["signal","background"] and mca.isSignal(p): norm /= options.signalPlotScale # un-scale what was scaled
                                if p == "signal": dump.write(("-"*(maxlen+45))+"\n");
                                dump.write(fmh % (_unTLatex(mca.getProcessOption(p,'Label',p) if p not in ["signal", "background"] else p.upper())))
                                bins = []
                                for b in range(1,plot.GetNbinsX()+1):
                                    syst = plot.GetBinContent(b) * mca.getProcessOption(p,'NormSystematic',0.0) if p not in ["signal", "background"] else 0;
                                    if p in mca.listBackgrounds(allProcs=True): bkgsyst[b-1] += syst*syst 
                                    if p in mca.listSignals(allProcs=True)    : sigsyst[b-1] += syst*syst
                                    line = fmt % (plot.GetBinContent(b), plot.GetBinError(b))
                                    #if syst: line += " +/- %9.2f (syst)"  % syst
                                    if   p == "signal"     and sigsyst[b-1]: line += " +/- %9.2f (syst)" % math.sqrt(sigsyst[b-1])
                                    elif p == "background" and bkgsyst[b-1]: line += " +/- %9.2f (syst)" % math.sqrt(bkgsyst[b-1])
                                    else: line += " +/- %9.2f (syst)"  % syst
                                    bins.append(line)
                                dump.write(" ".join(bins) + "\n")
                            if 'data' in pmap: 
                                dump.write(("-"*(maxlen+45))+"\n");
                                dump.write("%%%ds " % (maxlen+1) % ('DATA'))
                                plot = pmap['data']
                                bins = []
                                for b in range(1,plot.GetNbinsX()+1):
                                    bins.append("%7.0f" % plot.GetBinContent(b))
                                dump.write(" ".join(bins) + "\n")
                            for logname, loglines in pspec.allLogs():
                                dump.write("\n\n --- %s --- \n" % logname)
                                for line in loglines: dump.write("%s\n" % line)
                                dump.write("\n")
                            dump.close()
                        if ext == "txt" and "TProfile" not in total.ClassName():
                            dump = open("%s/%s.%s" % (fdir, outputName, ext), "w")
                            maxlen = max([len(mca.getProcessOption(p,'Label',p)) for p in mca.listSignals(allProcs=True) + mca.listBackgrounds(allProcs=True)]+[10])
                            fmt    = "%%-%ds %%9.2f +/- %%9.2f (stat)" % (maxlen+1)
                            for p in mca.listSignals(allProcs=True) + mca.listBackgrounds(allProcs=True) + ["signal", "background","total"]:
                                if p not in pmap: continue
                                plot = pmap[p]
                                if plot.Integral() <= 0: continue
                                norm = plot.Integral()
                                if p not in ["signal","background","total"] and mca.isSignal(p): norm /= options.signalPlotScale # un-scale what was scaled
                                stat = sqrt(sum([plot.GetBinError(b)**2 for b in xrange(1,plot.GetNbinsX()+1)]))
                                syst = plot.integralSystError(symmetrize=True)
                                if p == "signal": dump.write(("-"*(maxlen+45))+"\n");
                                dump.write(fmt % (_unTLatex(mca.getProcessOption(p,'Label',p) if p not in ["signal", "background","total"] else p.upper()), norm, stat))
                                if syst: dump.write(" +/- %9.2f (syst) = +/- %9.2f (all)"  % (syst, math.hypot(stat,syst)))
                                dump.write("\n")
                            if 'data' in pmap: 
                                dump.write(("-"*(maxlen+45))+"\n");
                                dump.write(("%%-%ds %%7.0f\n" % (maxlen+1)) % ('DATA', pmap['data'].Integral()))
                            for logname, loglines in pspec.allLogs():
                                dump.write("\n\n --- %s --- \n" % logname)
                                for line in loglines: dump.write("%s\n" % line)
                                dump.write("\n")
                            dump.close()
                        if ext != "txt":
                            savErrorLevel = ROOT.gErrorIgnoreLevel; ROOT.gErrorIgnoreLevel = ROOT.kWarning;
                            if "TH2" in total.ClassName() or "TProfile2D" in total.ClassName():
                                pmap["total"] = total
                                for p in mca.listSignals(allProcs=True) + mca.listBackgrounds(allProcs=True) + ["signal", "background", "data", "total"]:
                                    if p not in pmap: continue
                                    plot = pmap[p]
                                    if "TGraph" in plot.ClassName(): continue
                                    c1.SetRightMargin(0.20)
                                    plot.SetContour(100)
                                    ROOT.gStyle.SetPaintTextFormat(pspec.getOption("PaintTextFormat","g"))
                                    plot.SetMarkerSize(pspec.getOption("MarkerSize",1))
                                    if pspec.hasOption('ZMin') and pspec.hasOption('ZMax'):
                                        plot.GetZaxis().SetRangeUser(pspec.getOption('ZMin',1.0), pspec.getOption('ZMax',1.0))
                                    plot.SetMarkerStyle(mca.getProcessOption(p,'MarkerStyle',1,noThrow=True))
                                    plot.SetMarkerColor(mca.getProcessOption(p,'FillColor',ROOT.kBlack,noThrow=True))
                                    plot.Draw(pspec.getOption("PlotMode","COLZ TEXT45"))
                                    c1.Print("%s/%s_%s.%s" % (fdir, outputName, p, ext))
                                if "data" in pmap and "TGraph" in pmap["data"].ClassName():
                                    pmap["data"].SetMarkerStyle(mca.getProcessOption('data','MarkerStyle',1))
                                    pmap["data"].SetMarkerSize(pspec.getOption("MarkerSize",1.6))
                                    for p in ["signal", "background", "total"]:
                                        if p not in pmap: continue
                                        plot = pmap[p]
                                        c1.SetRightMargin(0.20)
                                        plot.SetContour(100)
                                        plot.Draw(pspec.getOption("PlotMode","COLZ TEXT45"))
                                        pmap["data"].Draw("P SAME")
                                        c1.Print("%s/%s_data_%s.%s" % (fdir, outputName, p, ext))
                            else:
                                c1.Print("%s/%s.%s" % (fdir, outputName, ext))
                            ROOT.gErrorIgnoreLevel = savErrorLevel;
                c1.Close()

## not needed anymore, leave for future development
##def getEvenBinning(histo):
##    if list(histo.GetXaxis().GetXbins()) == []:
##        return (histo.GetXaxis().GetXmax()-histo.GetXaxis().GetXmin())/histo.GetXaxis().GetNbins()
##    return -1
     

def addPlotMakerOptions(parser, addAlsoMCAnalysis=True):
    if addAlsoMCAnalysis: addMCAnalysisOptions(parser)
    parser.add_option("--ss",  "--scale-signal", dest="signalPlotScale", default=1.0, type="float", help="scale the signal in the plots by this amount");
    #parser.add_option("--lspam", dest="lspam",   type="string", default="CMS Simulation", help="Spam text on the right hand side");
    parser.add_option("--lspam", dest="lspam",   type="string", default="#bf{CMS} #it{Preliminary}", help="Spam text on the right hand side");
    parser.add_option("--rspam", dest="rspam",   type="string", default="%(lumi) (13 TeV)", help="Spam text on the right hand side");
    parser.add_option("--addspam", dest="addspam", type = "string", default=None, help="Additional spam text on the top left side, in the frame");
    parser.add_option("--topSpamSize", dest="topSpamSize",   type="float", default=1.2, help="Zoom factor for the top spam");
    parser.add_option("--print", dest="printPlots", type="string", default="png,pdf,txt", help="print out plots in this format or formats (e.g. 'png,pdf,txt')");
    parser.add_option("--pdir", "--print-dir", dest="printDir", type="string", default="plots", help="print out plots in this directory");
    parser.add_option("--showSigShape", dest="showSigShape", action="store_true", default=False, help="Superimpose a normalized signal shape")
    parser.add_option("--showIndivSigShapes", dest="showIndivSigShapes", action="store_true", default=False, help="Superimpose normalized shapes for each signal individually")
    parser.add_option("--showIndivSigs", dest="showIndivSigs", action="store_true", default=False, help="Superimpose shapes for each signal individually (normalized to their expected event yield)")
    parser.add_option("--noStackSig", dest="noStackSig", action="store_true", default=False, help="Don't add the signal shape to the stack (useful with --showSigShape)")
    parser.add_option("--showDatShape", dest="showDatShape", action="store_true", default=False, help="Stack a normalized data shape")
    parser.add_option("--showSFitShape", dest="showSFitShape", action="store_true", default=False, help="Stack a shape of background + scaled signal normalized to total data")
    parser.add_option("--showMCError", dest="showMCError", action="store_true", default=False, help="Show a shaded area for MC uncertainty")
    parser.add_option("--showRatio", dest="showRatio", action="store_true", default=False, help="Add a data/sim ratio plot at the bottom")
    parser.add_option("--ratioDen", dest="ratioDen", type="string", default="background", help="Denominator of the ratio, when comparing MCs")
    parser.add_option("--ratioNums", dest="ratioNums", type="string", default="signal", help="Numerator(s) of the ratio, when comparing MCs (comma separated list of regexps)")
    parser.add_option("--ratioYLabel", dest="ratioYLabel", type="string", default="Data/pred.", help="Y axis label of the ratio histogram.")
    parser.add_option("--ratioYNDiv", dest="ratioYNDiv", type="int", default=505, help="Y axis divisions in the ratio histogram.")
    parser.add_option("--noErrorBandOnRatio", dest="errorBandOnRatio", action="store_false", default=True, help="Do not show the error band on the reference in the ratio plots")
    parser.add_option("--noStatTotLegendOnRatio", dest="showStatTotLegend", action="store_false", default=True, help="Do not show the legend in the ratio plots")
    parser.add_option("--attachRatioPanel", dest="attachRatioPanel", action="store_true", default=False, help="Attach the ratio panel to the main plot, without a white spacer in between")
    parser.add_option("--fitRatio", dest="fitRatio", type="int", default=None, help="Fit the ratio with a polynomial of the specified order")
    parser.add_option("--scaleSigToData", dest="scaleSignalToData", action="store_true", default=False, help="Scale all signal processes so that the overall event yield matches the observed one")
    parser.add_option("--scaleBkgToData", dest="scaleBackgroundToData", action="append", default=[], help="Scale all background processes so that the overall event yield matches the observed one")
    parser.add_option("--showSF", dest="showSF", action="store_true", default=False, help="Show scale factor extracted from either --scaleSigToData or --scaleBkgToData on the plot")
    parser.add_option("--fitData", dest="fitData", action="store_true", default=False, help="Perform a fit to the data")
    parser.add_option("--preFitData", dest="preFitData", type="string", default=None, help="Perform a pre-fit to the data using the specified distribution, then plot the rest")
    parser.add_option("--maxRatioRange", dest="maxRatioRange", type="float", nargs=2, default=(0.0, 5.0), help="Min and max for the ratio")
    parser.add_option("--fixRatioRange", dest="fixRatioRange", action="store_true", default=False, help="Fix the ratio range to --maxRatioRange")
    parser.add_option("--doStatTests", dest="doStatTests", type="string", default=None, help="Do this stat test: chi2p (Pearson chi2), chi2l (binned likelihood equivalent of chi2)")
    parser.add_option("--plotmode", dest="plotmode", type="string", default="stack", help="Show as stacked plot (stack), a non-stacked comparison (nostack) and a non-stacked comparison of normalized shapes (norm)")
    parser.add_option("--rebin", dest="globalRebin", type="int", default="0", help="Rebin all plots by this factor")
    parser.add_option("--poisson", dest="poisson", action="store_true", default=True, help="Draw Poisson error bars (default)")
    parser.add_option("--no-poisson", dest="poisson", action="store_false", default=True, help="Don't draw Poisson error bars")
    parser.add_option("--unblind", dest="unblind", action="store_true", default=False, help="Unblind plots irrespectively of plot file")
    parser.add_option("--select-plot", "--sP", dest="plotselect", action="append", default=[], help="Select only these plots out of the full file")
    parser.add_option("--exclude-plot", "--xP", dest="plotexclude", action="append", default=[], help="Exclude these plots from the full file")
    parser.add_option("--legendWidth", dest="legendWidth", type="float", default=0.25, help="Width of the legend")
    parser.add_option("--legendBorder", dest="legendBorder", type="int", default=0, help="Use a border in the legend (1=yes, 0=no)")
    parser.add_option("--legendFontSize", dest="legendFontSize", type="float", default=0.055, help="Font size in the legend (if <=0, use the default)")
    parser.add_option("--flagDifferences", dest="flagDifferences", action="store_true", default=False, help="Flag plots that are different (when using only two processes, and plotmode nostack")
    parser.add_option("--toleranceForDiff", dest="toleranceForDiff", default=0.0, type="float", help="set numerical tollerance to define when two histogram bins are considered different");
    parser.add_option("--pseudoData", dest="pseudoData", type="string", default=None, help="If set to 'background' or 'all', it will plot also a pseudo-dataset made from background (or signal+background) with Poisson fluctuations in each bin.")
    parser.add_option("--wide", dest="wideplot", action="store_true", default=False, help="Draw a wide canvas")
    parser.add_option("--elist", dest="elist", action="store_true", default='auto', help="Use elist (on by default if making more than 2 plots)")
    parser.add_option("--no-elist", dest="elist", action="store_false", default='auto', help="Don't elist (which are on by default if making more than 2 plots)")
    #if not parser.has_option("--yrange"): parser.add_option("--yrange", dest="yrange", default=None, nargs=2, type='float', help="Y axis range");
    parser.add_option("--emptyStack", dest="emptyStack", action="store_true", default=False, help="Allow empty stack in order to plot, for example, only signals but no backgrounds.")
    parser.add_option("--perBin", dest="perBin", action="store_true", default=False, help="Print the contents of every bin in another txt file");
    parser.add_option("--legendHeader", dest="legendHeader", type="string", default=None, help="Put a header to the legend")
    parser.add_option("--legendColumns", dest="legendColumns", type="int", default=1, help="Number of columns in the legend")
    parser.add_option("--ratioOffset", dest="ratioOffset", type="float", default=0.0, help="Put an offset between ratio and main pad")
    parser.add_option("--noCms", dest="doOfficialCMS", action="store_false", default=True, help="Use official tool to write CMS spam")
    parser.add_option("--cmsprel", dest="cmsprel", type="string", default="Preliminary", help="Additional text (Simulation, Preliminary, Internal)")
    parser.add_option("--cmssqrtS", dest="cmssqrtS", type="string", default="13 TeV", help="Sqrt of s to be written in the official CMS text.")
    parser.add_option("--printBin", dest="printBinning", type="string", default=None, help="Write 'Events/xx' instead of 'Events' on the y axis")

if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser(usage="%prog [options] mc.txt cuts.txt plots.txt")
    addPlotMakerOptions(parser)
    parser.add_option("-o", "--out", dest="out", default=None, help="Output file name. by default equal to plots -'.txt' +'.root'");
    (options, args) = parser.parse_args()
    mca  = MCAnalysis(args[0],options)
    cuts = CutsFile(args[1],options)
    plots = PlotFile(args[2],options)
    outname  = options.out if options.out else (args[2].replace(".txt","")+".root")
    if options.printDir:
        if not options.out:
            outname = options.printDir + "/"+os.path.basename(args[2].replace(".txt","")+".root")
        else:
            outname = outname.replace("{O}",options.printDir)
    if os.path.dirname(outname) and not os.path.exists(os.path.dirname(outname)):
        os.system("mkdir -p "+os.path.dirname(outname))
        if os.path.exists("/afs/cern.ch"): os.system("cp /afs/cern.ch/user/g/gpetrucc/php/index.php "+os.path.dirname(outname))
        elif os.path.exists("/pool/ciencias/"): os.system("cp /pool/ciencias/HeppyTrees/RA7/additionalReferenceCode/index.php "+os.path.dirname(outname))
    print "Will save plots to ",outname
    fcmd = open(re.sub("\.root$","",outname)+"_command.txt","w")
    fcmd.write("%s\n\n" % " ".join(sys.argv))
    fcmd.write("%s\n%s\n" % (args,options))
    fcmd.close()
    fcut = open(re.sub("\.root$","",outname)+"_cuts.txt","w")
    fcut.write("%s\n" % cuts); fcut.close()
    os.system("cp %s %s " % (args[2], re.sub("\.root$","",outname)+"_plots.txt"))
    os.system("cp %s %s " % (args[0], re.sub("\.root$","",outname)+"_mca.txt"))
    #fcut = open(re.sub("\.root$","",outname)+"_cuts.txt")
    #fcut.write(cuts); fcut.write("\n"); fcut.close()
    outfile  = ROOT.TFile(outname,"RECREATE")
    plotter = PlotMaker(outfile,options)
    plotter.run(mca,cuts,plots)
    outfile.Close()


