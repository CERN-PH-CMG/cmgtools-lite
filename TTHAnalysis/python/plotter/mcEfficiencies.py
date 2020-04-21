#!/usr/bin/env python
#from mcPlots import *
from CMGTools.TTHAnalysis.plotter.mcPlots import *

if "/fakeRate_cc.so" not in ROOT.gSystem.GetLibraries():
    ROOT.gROOT.ProcessLine(".L %s/src/CMGTools/TTHAnalysis/python/plotter/fakeRate.cc+" % os.environ['CMSSW_BASE']);

if "/bin2Dto1Dlib_cc.so" not in ROOT.gSystem.GetLibraries():
    ROOT.gROOT.ProcessLine(".L %s/src/CMGTools/TTHAnalysis/python/plotter/bin2Dto1Dlib.cc+" % os.environ['CMSSW_BASE']);

def addMCEfficiencyOptions(parser):
    addMCAnalysisOptions(parser)
    parser.add_option("--select-plot", "--sP", dest="plotselect", action="append", default=[], help="Select only these plots out of the full file")
    parser.add_option("--exclude-plot", "--xP", dest="plotexclude", action="append", default=[], help="Exclude these plots from the full file")
    parser.add_option("-o", "--out", dest="out", default=None, help="Output file name. by default equal to plots -'.txt' +'.root'");
    parser.add_option("--weightNumerator", dest="weightNumerator", default=None, help="Adds a weight only to the numerator (MC only) for closures tests of scale factors")
    parser.add_option("--rebin", dest="globalRebin", type="int", default="0", help="Rebin all plots by this factor")
    parser.add_option("--xrange", dest="xrange", default=None, nargs=2, type='float', help="X axis range");
    parser.add_option("--xcut", dest="xcut", default=None, nargs=2, type='float', help="X axis cut");
    parser.add_option("--xline", dest="xlines", default=[], action="append", type='float', help="Lines to draw at given X axis values");
    if not parser.has_option("--yrange"): parser.add_option("--yrange", dest="yrange", default=None, nargs=2, type='float', help="Y axis range");
    parser.add_option("--logy", dest="logy", default=False, action='store_true', help="Do y axis in log scale");
    parser.add_option("--ytitle", dest="ytitle", default="Efficiency", type='string', help="Y axis title");
    parser.add_option("--fontsize", dest="fontsize", default=0.045, type='float', help="Legend font size");
    parser.add_option("--grid", dest="showGrid", action="store_true", default=False, help="Show grid lines")
    parser.add_option("--groupBy",  dest="groupBy",  default="process",  type="string", help="Group by: cut, process")
    parser.add_option("--legend",  dest="legend",  default="TR",  type="string", help="Legend position (BR, TR)")
    parser.add_option("--legendWidth", dest="legendWidth", type="float", default=0.35, help="Width of the legend")
    parser.add_option("--compare", dest="compare", default="", help="Samples to compare (by default, all except the totals)")
    parser.add_option("--showRatio", dest="showRatio", action="store_true", default=False, help="Add a data/sim ratio plot at the bottom")
    parser.add_option("--shiftPoints", dest="shiftPoints", type="float", default=0, help="Shift x coordinates of points by this fraction of the error bar in thew plot to make them more visible when stacking.")
    parser.add_option("--rr", "--ratioRange", dest="ratioRange", type="float", nargs=2, default=(-1,-1), help="Min and max for the ratio")
    parser.add_option("--normEffUncToLumi", dest="normEffUncToLumi", action="store_true", default=False, help="Normalize the dataset to the given lumi for the uncertainties on the calculated efficiency")


def doLegend(rocs,options,textSize=0.035,header=None):
        lwidth = options.legendWidth
        if options.legend == "TR":
            (x1,y1,x2,y2) = (.93-lwidth, .98 - 1.2*textSize*max(len(rocs),3), .93, .98)
        elif options.legend == "TL":
            (x1,y1,x2,y2) = (.2, .98 - 1.2*textSize*max(len(rocs),3), .2+lwidth, .98)
        else:
            (x1,y1,x2,y2) = (.93-lwidth, .18 + 1.2*textSize*max(len(rocs),3), .93, .18)
        leg = ROOT.TLegend(x1,y1,x2,y2)
        leg.SetFillColor(0)
        leg.SetShadowColor(0)
        leg.SetTextFont(42)
        leg.SetTextSize(textSize)
        if header: leg.SetHeader(header.replace("\#", "#"))       
        for key,val in rocs:
            leg.AddEntry(val, key, "LP")
        leg.Draw()
        ## assign it to a global variable so it's not deleted
        global legend_;
        legend_ = leg 
        return leg

def effFromH2D(h2d,options,uncertainties="CP", customNum=None, name=None):
    points = []
    for xbin in xrange(1,h2d.GetNbinsX()+1):
        xval = h2d.GetXaxis().GetBinCenter(xbin)
        if options.xcut and (xval < options.xcut[0] or xval > options.xcut[1]):
            continue
        xerrs = h2d.GetXaxis().GetBinLowEdge(xbin)-xval, h2d.GetXaxis().GetBinUpEdge(xbin)-xval 
        if customNum and 'data' not in name: 
            ypass,ypassErr, yfail,yfailErr = customNum.GetBinContent(xbin,2),customNum.GetBinError(xbin,2), h2d.GetBinContent(xbin,1),h2d.GetBinError(xbin,1)
            ypass2,ypassErr2 = h2d.GetBinContent(xbin,2),h2d.GetBinError(xbin,2)
            yall = ypass2+yfail
            
        else:
            ypass,ypassErr, yfail,yfailErr = h2d.GetBinContent(xbin,2),h2d.GetBinError(xbin,2), h2d.GetBinContent(xbin,1),h2d.GetBinError(xbin,1)
            yall = ypass+yfail
        if yall <= 0: continue
        if ypass < 0:
            print "Warning: effFromH2D for %s at x = %g: ypass = %g +- %g  yfail = %g +- %g\n" % (h2d.GetName(), xval, ypass, ypassErr, yfail, yfailErr)
            if uncertainties == "CP": continue
            if ypass + 2*ypassErr < 0: continue
            ypass, yall = 0, yfail
        eff = ypass/yall 
        neff = (yall**2)/(ypassErr**2 + yfailErr**2)
        if uncertainties == "CP":
            errs = [ ROOT.TEfficiency.ClopperPearson(int(neff),int(neff*eff), 0.6827, i)-eff for i in (False,True) ]
        elif uncertainties == "PF":
            err = hypot(yfail * ypassErr, ypass * yfailErr)/(yall*yall)
            errs = [ -err, err ]
        #print h2d.GetName(), xval, ypass, ypassErr, yfail, yfailErr, eff, neff, eff*neff, (1-eff)*neff, errs
        points.append( (xval, xerrs, eff, errs) )
    if not points: return None
    ret = ROOT.TGraphAsymmErrors(len(points))
    for i,(xval, xerrs, yval, yerrs) in enumerate(points):
        ret.SetPoint(i, xval, yval)
        ret.SetPointError(i, -xerrs[0], xerrs[1], -yerrs[0], yerrs[1])
    ret._xrange = h2d.GetXaxis().GetXmin(), h2d.GetXaxis().GetXmax()
    ret.GetXaxis().SetRangeUser(ret._xrange[0], ret._xrange[1])
    ret.GetXaxis().SetTitle(h2d.GetXaxis().GetTitle())
    ret.SetName(h2d.GetName()+"_graph")
    return ret

def dumpEffFromH2D(h2d,xbin):
    ret = ""
    ypass,ypassErr,yfail,yfailErr = h2d.GetBinContent(xbin,2),h2d.GetBinError(xbin,2), h2d.GetBinContent(xbin,1),h2d.GetBinError(xbin,1)
    yall = ypass+yfail
    if yall == 0: return " <empty>"
    eff = ypass/yall 
    ret +=  "pass %10.1f +- %8.1f, fail %10.1f +- %8.1f, eff = %.4f" % (ypass,ypassErr,yfail,yfailErr,eff)
    neff = (yall**2)/(ypassErr**2 + yfailErr**2)
    weff = yall/neff
    ret += " nEff = %9.2f w = %9.2f pEff = %9.2f" % (neff,weff,neff*eff)
    errBin0 = hypot(ypass*yfailErr, yfail*ypassErr)/(yall**2)
    errBin1 = hypot(ypass*hypot(yfailErr,weff), yfail*hypot(ypassErr,weff))/(yall**2)
    ret += " errBin0 = %.4f " % errBin0
    ret += " errBin1 = %.4f " % errBin1
    errsCP = [ ROOT.TEfficiency.ClopperPearson(int(neff),int(neff*eff), 0.6827, i)-eff for i in (False,True) ]
    ret += " errsCP = % .4f/%.4f " % (errsCP[0], errsCP[1])
    ret += "\t%s" % getattr(h2d, '_cname', '<nil>')
    return ret


def shiftEffsX(effs, amount=0.4):
    ng = len(effs)
    if ng <= 1 or amount == 0: return effs
    shiftedEffs = []
    for ig, (k,g) in enumerate(effs):
        gc = g.Clone()
        delta = 2*ig/float(ng-1) - 1 # -1 for first, +1 for last
        for i in xrange(g.GetN()):
            x0 = g.GetX()[i]
            dxm = g.GetErrorXlow(i)
            dxp = g.GetErrorXhigh(i)
            xnew = x0 + amount * delta * ( dxm if delta <= 0 else dxp )
            gc.SetPoint(i, xnew, g.GetY()[i])
            gc.SetPointError(i, xnew-(x0-dxm), (x0+dxp)-xnew, g.GetErrorYlow(i), g.GetErrorYhigh(i))
        g._shifted = gc
        shiftedEffs.append((k,gc))
    return shiftedEffs

def stackEffs(outname,x,effs,options,legHeader=None):
    if effs[0][1].ClassName() == "TProfile2D": 
        return stackInXYSlices(outname,x,effs,options)
    if effs[0][1].ClassName() != "TGraphAsymmErrors": 
        print "Cannot stack %s: %s" % (effs[0][1].GetName(), effs[0][1].ClassName())
        return
    first = effs[0][1]
    if hasattr(first, '_xrange'): 
        xmin, xmax = first._xrange
    else:
        xmin = first.GetX()[0] - first.GetErrorXlow(0) 
        xmax = first.GetX()[first.GetN()-1] + first.GetErrorXhigh(first.GetN()-1)

    ymax = 0 
    for title, eff in effs:
        ymax = max(ymax, max([ eff.GetY()[i] + eff.GetErrorYhigh(i)*1.3 for i in xrange(eff.GetN()) ]))

    frame = ROOT.TH1D("frame","frame",100,xmin,xmax)
    frame.GetXaxis().SetTitle(first.GetXaxis().GetTitle())
    frame.GetYaxis().SetTitle(first.GetYaxis().GetTitle())
    frame.GetYaxis().SetRangeUser(0,ymax)
    frame.GetYaxis().SetDecimals()
    frame.GetYaxis().SetTitle(options.ytitle)

    doRatio = options.showRatio and len(effs) > 1
    # define aspect ratio
    if doRatio: ROOT.gStyle.SetPaperSize(20.,25.)
    else:       ROOT.gStyle.SetPaperSize(20.,20.)
    # create canvas
    c1 = ROOT.TCanvas(outname+"_canvas", outname, 600, (750 if doRatio else 600))
    c1.Draw()
    p1, p2 = c1, None # high and low panes
    # set borders, if necessary create subpads
    if doRatio:
        c1.SetWindowSize(600 + (600 - c1.GetWw()), (750 + (750 - c1.GetWh())));
        p1 = ROOT.TPad("pad1","pad1",0,0.31,1,1);
        p1.SetBottomMargin(0);
        p1.Draw();
        p2 = ROOT.TPad("pad2","pad2",0,0,1,0.31);
        p2.SetTopMargin(0);
        p2.SetBottomMargin(0.3);
        p2.SetFillStyle(0);
        p2.Draw();
        p1.cd();
    else:
        c1.SetWindowSize(600 + (600 - c1.GetWw()), 600 + (600 - c1.GetWh()));
    p1.SetGridy(options.showGrid)
    p1.SetGridx(options.showGrid)
    p1.SetLogx(x.getOption('Logx',False) if x else False)
    p1.SetLogy(options.logy)

    frame.Draw()
    for title, eff in shiftEffsX(effs,options.shiftPoints): 
        eff.Draw("P0 SAME")

    if options.xrange:
        frame.GetXaxis().SetRangeUser(options.xrange[0], options.xrange[1])
    if options.yrange:
        frame.GetYaxis().SetRangeUser(options.yrange[0], options.yrange[1])

    liner = ROOT.TLine(); liner.SetLineStyle(2)
    for x in options.xlines:
        liner.DrawLine(x, frame.GetYaxis().GetXmin(), x, frame.GetYaxis().GetXmax())

    leg = doLegend(effs,options,textSize=options.fontsize,header=legHeader)
    if doRatio:
        p2.cd()
        keepme = doEffRatio(x,effs,frame,options)
        frame.GetXaxis().SetLabelOffset(999) ## send them away
        frame.GetXaxis().SetTitleOffset(999) ## in outer space
        frame.GetYaxis().SetLabelSize(0.05)
    c1.Print(outname.replace(".root","")+".png")
    c1.Print(outname.replace(".root","")+".eps")
    c1.Print(outname.replace(".root","")+".pdf")
    dump = open(outname.replace(".root","")+".txt","w")
    for n,e in effs:
        dump.write(" ===  %s === \n" % n)
        dump.write("  x min    x max      eff   -err   +err  \n")
        dump.write("-------- --------    ----- ------ ------ \n")
        for i in xrange(e.GetN()):
            dump.write("%8.3f %8.3f    %.3f -%.3f +%.3f \n" % (
                 e.GetX()[i]-e.GetErrorXlow(i),
                 e.GetX()[i]+e.GetErrorXhigh(i),
                 e.GetY()[i], e.GetErrorYlow(i), e.GetErrorYhigh(i) ))
        dump.write("\n\n");
def graphFromSlice(h,axis,bins):
        (aobj,ai) = (h.GetXaxis(),0) if axis == "X" else (h.GetYaxis(),1)
        ret = ROOT.TGraphAsymmErrors(len(bins))
        for (i,bin) in enumerate(bins):
            x = aobj.GetBinCenter(bin[ai])
            xlo = aobj.GetBinLowEdge(bin[ai])
            xhi = aobj.GetBinUpEdge(bin[ai])
            y = h.GetBinContent(bin[0],bin[1])
            dy = h.GetBinError(bin[0],bin[1])
            ret.SetPoint(i, x, y)
            ret.SetPointError(i, x-xlo, xhi-x, min(y,dy), dy)
        ret.SetName(h.GetName()+"_slice"+axis)
        return ret
def graphFromXSlice(h,ybin):
    return graphFromSlice(h,"X", [ (i,ybin) for i in xrange(1,h.GetNbinsX()+1)  ])

def stackInXYSlices(outname,x,effs,options):
    h2d = effs[0][1]
    names = ("X","Y")
    axes  = h2d.GetXaxis(), h2d.GetYaxis()
    nbins = h2d.GetNbinsX(), h2d.GetNbinsY()
    for sliceaxis in 0,1:
        runaxis = 1-sliceaxis
        sliceobj = axes[sliceaxis]
        for islice in xrange(1,nbins[sliceaxis]+1):
            bins = [ ((i,islice) if runaxis == 0 else (islice,i)) for i in xrange(1,nbins[runaxis]+1) ]
            slice_effs = [ (n,graphFromSlice(h,names[runaxis],bins)) for (n,h) in effs ]
            stackEffs(outname.replace(".root",".slice%s_bin%d.root" % (names[sliceaxis],islice+1)),
                      slice_effs, bins, options)
    

def doEffRatio(x,effs,frame,options):
    cframe = frame.Clone("frame_ratio"); cframe.Reset()
    cframe.Draw()
    effrels = [ e.Clone(n+"_rel") for (n,e) in effs ]
    unity   = effrels[0]; ref = effs[0][1]
    rmin, rmax = 1,1
    def find(graph, x):
        for i in xrange(graph.GetN()):
            if graph.GetX()[i]-graph.GetErrorYlow(i) <= x:
                if x <= graph.GetX()[i]+graph.GetErrorYhigh(i):
                    return i
        return -1
    for ie,eff in enumerate(effrels):
        points = []
        for b in xrange(eff.GetN()):
            xv = eff.GetX()[b]
            b2 = find(ref, xv)
            if b2 == -1: continue
            if ref.GetY()[b2] == 0: continue
            points.append((b, b2))
        eff.Set(len(points))
        for i,(b, b2) in enumerate(points):
            scale = ref.GetY()[b2]
            src = effs[ie][1]
            eff.SetPoint(i, src.GetX()[b], src.GetY()[b]/scale)
            eff.SetPointError(i, src.GetErrorXlow(b), src.GetErrorXhigh(b), 
                                 src.GetErrorYlow(b)/scale, src.GetErrorYhigh(b)/scale)
            if ie == 0:
                eff.SetFillStyle(3013)
                eff.SetFillColor(src.GetLineColor())
                eff.SetMarkerStyle(0)
            else:
                eff.SetLineColor(src.GetLineColor())
                eff.SetLineWidth(src.GetLineWidth())
                eff.SetMarkerColor(src.GetMarkerColor())
                eff.SetMarkerStyle(src.GetMarkerStyle())
            rmax = max(rmax, eff.GetY()[i]+2*eff.GetErrorYhigh(i))
            rmin = min(rmin, max(0,eff.GetY()[i]-2*eff.GetErrorYlow(i)))
    if options.ratioRange != (-1,-1):
        rmin,rmax = options.ratioRange
    cframe.Draw()
    cframe.GetYaxis().SetRangeUser(rmin,rmax);
    cframe.GetXaxis().SetTitleSize(0.14)
    cframe.GetYaxis().SetTitleSize(0.14)
    cframe.GetXaxis().SetLabelSize(0.11)
    cframe.GetYaxis().SetLabelSize(0.11)
    cframe.GetYaxis().SetNdivisions(505)
    cframe.GetYaxis().SetDecimals(True)
    cframe.GetYaxis().SetTitle("X / "+effs[0][0])
    cframe.GetYaxis().SetTitleOffset(0.52);
    line = ROOT.TLine(cframe.GetXaxis().GetXmin(),1,cframe.GetXaxis().GetXmax(),1)
    line.SetLineWidth(3);
    line.SetLineColor(effs[0][1].GetLineColor());
    line.DrawLine(cframe.GetXaxis().GetXmin(),1,cframe.GetXaxis().GetXmax(),1)
    unity.Draw("E2 SAME");
    for _, ratio in shiftEffsX([(None,r) for r in effrels[1:]], options.shiftPoints): 
        ratio.Draw("P0Z SAME");

    liner = ROOT.TLine(); liner.SetLineStyle(2)
    for x in options.xlines: liner.DrawLine(x, rmin, x, rmax)

    return (cframe,line,effrels)

    
def makeDataSub(report,mca):
    data_sub      = report['data'].Clone(report['data'].GetName()+'_sub')
    data_sub_syst = report['data'].Clone(report['data'].GetName()+'_sub_syst')
    for p in mca.listBackgrounds():
        if p not in report: continue
        b = report[p]
        data_sub.Add(b, -1.0)
        data_sub_syst.Add(b, -1.0)
        syst = mca.getProcessOption(p,'NormSystematic',0.) 
        #print "subtracting background %s from data with systematic %r" % (p,syst)
        if syst <= 0: continue
        if "TH1" in b.ClassName():
            for bx in xrange(1,b.GetNbinsX()+1):
                data_sub_syst.SetBinError(bx, hypot(data_sub_syst.GetBinError(bx), syst * b.GetBinContent(bx)))
        elif "TH2" in b.ClassName():
            for (bx,by) in itertools.product(range(1,b.GetNbinsX()+1), range(1,b.GetNbinsY()+1)):
                data_sub_syst.SetBinError(bx, by, hypot(data_sub_syst.GetBinError(bx, by), syst * b.GetBinContent(bx, by)))
        elif "TH3" in b.ClassName():
            for (bx,by,bz) in itertools.product(range(1,b.GetNbinsX()+1), range(1,b.GetNbinsY()+1), range(1,b.GetNbinsZ()+1)):
                data_sub_syst.SetBinError(bx, by, bz, hypot(data_sub_syst.GetBinError(bx, by, bz), syst * b.GetBinContent(bx, by, bz)))
    report['data_sub']      = data_sub
    report['data_sub_syst'] = data_sub_syst

def makeEff(mca,cut,idplot,xvarplot,returnSeparatePassFail=False,notDoProfile="auto",mainOptions=None):
    import copy
    is2D = (":" in xvarplot.expr.replace("::","--"))
    options = copy.copy(idplot.opts)
    options.update(xvarplot.opts)
    mybins = copy.copy(xvarplot.bins)
    if notDoProfile == "auto":
        notDoProfile = not is2D
    if notDoProfile == False and returnSeparatePassFail == False:
        if is2D: options['Profile2D']=True
        else:    options['Profile1D']=True
    else:
        if xvarplot.bins[0] == "[":
            mybins += "*[-0.5,0.5,1.5]"
        else:
            mybins += ",2,-0.5,1.5"
    pspec = PlotSpec("%s_vs_%s"  % (idplot.name, xvarplot.name), 
                     "%s:%s" % (idplot.expr,xvarplot.expr),
                     mybins,
                     options) 
    report = mca.getPlots(pspec,cut,makeSummary=True)
    if mainOptions.weightNumerator:
        pspec_num = PlotSpec("%s_vs_%s_fornum"  % (idplot.name, xvarplot.name), 
                             "%s:%s" % (idplot.expr,xvarplot.expr),
                             mybins,
                             options) 
        pspec_num.extracut ='(%s)'%mainOptions.weightNumerator
        report_num = mca.getPlots(pspec_num,cut,makeSummary=True)
        if 'signal' in report_num and 'background' in report_num:
            report_num['total'] = mergePlots(pspec.name+"_total", [ report_num[s] for s in ('signal','background') ] )
        if 'data' in report_num and 'background' in report_num:
            makeDataSub(report_num, mca)
        
    

    if 'signal' in report and 'background' in report:
        report['total'] = mergePlots(pspec.name+"_total", [ report[s] for s in ('signal','background') ] )
    if 'data' in report and 'background' in report:
        makeDataSub(report, mca)
    if mainOptions.weightNumerator:
        if notDoProfile and not returnSeparatePassFail:
            if is2D: report = dict([(title, effFromH3D(hist,mainOptions, customNum=report_num[title], name=title)) for (title, hist) in report.iteritems()])
            else:    report = dict([(title, effFromH2D(hist,mainOptions, customNum=report_num[title], name=title)) for (title, hist) in report.iteritems()])
    else: 
        if notDoProfile and not returnSeparatePassFail:
            if is2D: report = dict([(title, effFromH3D(hist,mainOptions)) for (title, hist) in report.iteritems()])
            else:    report = dict([(title, effFromH2D(hist,mainOptions)) for (title, hist) in report.iteritems()])
    return report

def styleEffsByProc(effmap,procs,mca):
    allprocs = mca.listSignals(True)+mca.listBackgrounds(True)+mca.listOptionsOnlyProcesses()
    effs = []
    for proc in procs:
        if proc not in effmap: continue
        eff = effmap[proc]
        if not eff: continue
        if proc in allprocs:
            eff.SetLineColor(mca.getProcessOption(proc,"FillColor",SAFE_COLOR_LIST[len(effs)]))
            eff.SetFillColor(mca.getProcessOption(proc,"FillColor",SAFE_COLOR_LIST[len(effs)]))
            eff.SetMarkerColor(mca.getProcessOption(proc,"FillColor",SAFE_COLOR_LIST[len(effs)]))
            eff.SetMarkerStyle(mca.getProcessOption(proc,"MarkerStyle",20))
            eff.SetMarkerSize(mca.getProcessOption(proc,"MarkerSize",1.6)*0.8)
            eff.SetLineWidth(4)
            effs.append((mca.getProcessOption(proc,"Label",proc),eff))
            if mca.getProcessOption(proc,'DrawOption'):
                eff.DrawOption = mca.getProcessOption(proc,'DrawOption')
        else:
            eff.SetLineColor(SAFE_COLOR_LIST[len(effs)])
            eff.SetMarkerColor(SAFE_COLOR_LIST[len(effs)])
            eff.SetMarkerStyle(20)
            eff.SetMarkerSize(1.6*0.8)
            eff.SetLineWidth(4)
            effs.append((proc,eff))
    return effs

if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser(usage="%prog [options] mc.txt cuts.txt plotfile.txt")
    addMCEfficiencyOptions(parser)
    (options, args) = parser.parse_args()
    options.globalRebin = 1
    options.allowNegative = True # with the fine bins used in ROCs, one otherwise gets nonsensical results
    mca  = MCAnalysis(args[0],options)
    procs = mca.listProcesses()
    cut = CutsFile(args[1],options).allCuts()
    ids   = PlotFile(args[2],options).plots()
    xvars = PlotFile(args[3],options).plots()
    outname  = options.out if options.out else (args[2].replace(".txt","")+".root")
    if os.path.dirname(outname) != "":
        dirname = os.path.dirname(outname)
        if not os.path.exists(dirname):
            os.system("mkdir -p "+dirname)
            if os.path.exists("/afs/cern.ch"): os.system("cp /afs/cern.ch/user/g/gpetrucc/php/index.php "+os.path.dirname(outname))
    outfile  = ROOT.TFile(outname,"RECREATE")
    ROOT.gROOT.ProcessLine(".x tdrstyle.cc")
    ROOT.gStyle.SetErrorX(0.5)
    ROOT.gStyle.SetOptStat(0)
    effplots = [ (y,x,makeEff(mca,cut,y,x,returnSeparatePassFail=options.normEffUncToLumi,mainOptions=options)) for y in ids for x in xvars ]
    for (y,x,pmap) in effplots:
        for proc in procs + [ "total", "signal", "background", "data_sub" ]:
            if (proc not in pmap) or not pmap[proc]: continue
            eff = pmap[proc]
            #eff.Print()
#            PrintHisto(eff)
            if options.xcut and eff.ClassName() != "TGraphAsymmErrors":
                ax = eff.GetXaxis()
                for b in xrange(1,eff.GetNbinsX()+1):
                    if ax.GetBinCenter(b) < options.xcut[0] or ax.GetBinCenter(b) > options.xcut[1]:
                        eff.SetBinContent(b,0)
                        eff.SetBinError(b,0)

            if options.normEffUncToLumi:
                assert (("TH3" in eff.ClassName()) or ("TH2" in eff.ClassName()))
                is1d = "TH3" not in eff.ClassName()
                #eff.Print()
                #print 'is1d is ',is1d
                binsfail = []
                binspass = []
                if is1d:
                    binsfail = [eff.GetBin(i1,1) for i1 in range(1,eff.GetNbinsX()+1)]
                    binspass = [eff.GetBin(i1,2) for i1 in range(1,eff.GetNbinsX()+1)]
                else:
                    binsfail = [eff.GetBin(i1,i2,1) for i1 in range(1,eff.GetNbinsX()+1) for i2 in range(1,eff.GetNbinsY()+1)]
                    binspass = [eff.GetBin(i1,i2,2) for i1 in range(1,eff.GetNbinsX()+1) for i2 in range(1,eff.GetNbinsY()+1)]

                for bin in binspass+binsfail:
                    eff.SetBinError(bin,sqrt(eff.GetBinContent(bin)))

                outfile.WriteTObject(eff)
                effratio = eff.ProjectionX("_px") if is1d else eff.Project3D("yx")
                effratio.Reset()
                for b1 in xrange(len(binsfail)):
                    passing = eff.GetBinContent(binspass[b1])
                    failing = eff.GetBinContent(binsfail[b1])
                    bx = ROOT.Long(0)
                    by = ROOT.Long(0)
                    bz = ROOT.Long(0)
                    eff.GetBinXYZ(binspass[b1],bx,by,bz)
                    if is1d:
                        ratiobin = effratio.FindBin(eff.GetXaxis().GetBinCenter(bx))
                    else:
                        ratiobin = effratio.FindBin(eff.GetXaxis().GetBinCenter(bx),eff.GetYaxis().GetBinCenter(by))
                    effratio.SetBinContent(ratiobin,passing/(passing+failing))
                    effratio.SetBinError(ratiobin,sqrt(passing*failing*((passing+failing)**(-3))))
                pmap[proc] = effratio
            eff.SetName("_".join([y.name,x.name,proc]))
            outfile.WriteTObject(eff)
    if len(procs)>=1 and "cut" in options.groupBy:
        for x in xvars:
            for y,ex,pmap in effplots:
                if ex != x: continue
                myname = outname.replace(".root","_%s_%s.root" % (y.name,x.name))
                procsToStack = options.compare.split(",") if options.compare else procs
                effs = styleEffsByProc(pmap,procsToStack,mca)
                if len(effs) == 0: continue
                stackEffs(myname,x,effs,options)
    if "process" in options.groupBy:
        for proc in procs:
            for x in xvars:
                effs = []
                myname = outname.replace(".root","_%s_%s.root" % (proc,x.name))
                for y,ex,pmap in effplots:
                    if ex != x: continue
                    eff = pmap[proc]
                    if not eff: continue
                    eff.SetLineColor(y.getOption("MarkerColor",SAFE_COLOR_LIST[len(effs)]))
                    eff.SetMarkerColor(y.getOption("MarkerColor",SAFE_COLOR_LIST[len(effs)]))
                    eff.SetMarkerStyle(y.getOption("MarkerStyle",33))
                    eff.SetMarkerSize(y.getOption("MarkerSize",1.4)*0.8)
                    eff.SetLineWidth(4)
                    effs.append((y.getOption("Title",y.name),eff))
                if len(effs) == 0: continue
                stackEffs(myname,x,effs,options)
    outfile.Close()


