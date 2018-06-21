#!/bin/env python
# USAGE: ./plotYsystFromToys.py -C plus binningYW.txt Wel_plus_ws.root toys_BFGS2_wplus_el_normonly.root

import ROOT, datetime, array, os, math
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")

import utilities
utilities = utilities.util()

NPDFs = 60

def translateWStoTF(pname):
    if not 'r_' in pname:
        return pname

    if 'Wplus' in pname or 'Wminus' in pname:
        pnew = pname.replace('r_','')
        pnew = pnew.split('_')
        pnew.insert(-2, 'mu' )#if 'Wmu' in options.tensorflow else 'el')
        pnew = '_'.join(pnew)
        return pnew

    return -1

def getFromToys(infile):
    _dict = {}
    
    f = ROOT.TFile(infile, 'read')
    tree = f.Get('fitresults')
    lok  = tree.GetListOfLeaves()
    
    for p in lok:
        if '_err'   in p.GetName(): continue
        if '_minos' in p.GetName(): continue
        if '_gen'   in p.GetName(): continue
        if '_In'    in p.GetName(): continue
        
        tmp_hist = ROOT.TH1F(p.GetName(),p.GetName(), 1000, -3., 3.)
        tree.Draw(p.GetName()+'>>'+p.GetName())
        mean = tmp_hist.GetMean()
        err  = tmp_hist.GetRMS()
        _dict[p.GetName()] = (mean, mean+err, mean-err)

    return _dict

def getFromScans(indir):
    _dict = {}
    
    for sd in os.listdir(indir):

        if 'jobs' in sd: continue

        par = translateWStoTF(sd) ## parameter name different than in TF
        f = ROOT.TFile(indir+'/'+sd+'/scan_'+sd+'.root', 'read')
        tree = f.Get('fitresults')

        vals = []
        for ev in tree:
            vals.append( [getattr(ev, par), 2.*ev.nllval  ] )
        vals = sorted(vals)
        lvals = vals[:len(vals)/2]
        rvals = vals[len(vals)/2:]

        graph = ROOT.TGraph(len(vals), array.array('d', [x[1] for x in vals]), array.array('d', [y[0] for y in vals]) )

        best = graph.Eval(0.)
        lgraph = ROOT.TGraph(len(lvals), array.array('d', [x[1] for x in lvals]), array.array('d', [y[0] for y in lvals]) )
        rgraph = ROOT.TGraph(len(rvals), array.array('d', [x[1] for x in rvals]), array.array('d', [y[0] for y in rvals]) )
        sol1  = lgraph.Eval(1.)
        sol2  = rgraph.Eval(1.)

        _dict[par] = (best, sol1, sol2)

    return _dict


if __name__ == "__main__":

    from optparse import OptionParser
    parser = OptionParser(usage='%prog ybinfile workspace.root toys.root [options] ')
    parser.add_option('-i', '--infile'      , dest='infile'   , default=''            , type='string', help='workspace converted from datacard')
    parser.add_option('-y', '--ybinfile'    , dest='ybinfile' , default=''            , type='string', help='file with the yw binning')

    parser.add_option('-t', '--type'        , dest='type'     , default='toys'        , type='string', help='run the plot from which postfit? toys/scans/hessian')
    parser.add_option(      '--toyfile'     , dest='toyfile'  , default=''            , type='string', help='file that has the toys')
    parser.add_option(      '--scandir'     , dest='scandir'  , default=''            , type='string', help='directory with all the scans')
    parser.add_option(      '--hessfile'    , dest='hessfile' , default=''            , type='string', help='file that contains the hessian errors in a dictionary')

    parser.add_option('-C', '--charge'      , dest='charge'   , default='plus,minus'  , type='string', help='process given charge. default is both')
    parser.add_option('-o', '--outdir'      , dest='outdir'   , default='.'           , type='string', help='outdput directory to save the plots')
    parser.add_option(      '--suffix'      , dest='suffix'   , default=''            , type='string', help='suffix for the correlation matrix')
    (options, args) = parser.parse_args()


    if not os.path.isdir(options.outdir):
        os.system('mkdir {od}'.format(od=options.outdir))
        os.system('cp /afs/cern.ch/user/m/mdunser/index.php {od}'.format(od=options.outdir))

    if options.ybinfile:
        ybinfile = options.ybinfile
    else:
        ybinfile = os.path.dirname(os.path.abspath(options.infile))+'/binningYW.txt'


    ## get the central values and uncertainties depending on the type given:

    ## if --type=toys   , we expect a toyfile
    ## if --type=scans  , we expect a scan directory
    ## if --type=hessian, we expect a hessian file

    if   options.type == 'toys':
        valuesAndErrors = getFromToys(options.infile)
    elif options.type == 'scans':
        valuesAndErrors = getFromScans(options.infile)
    elif options.type == 'hessian':
        tmp = eval(open(options.infile,'r').read())
        valuesAndErrors = {}
        for i,j in tmp.items():
            valuesAndErrors[i] = (j[0], j[0]-j[1], j[0]+j[1])
    else:
        print 'ERROR: none of your types is supported. specify either "toys", "scans", or "hessian"'
        sys.exit()


    ybinfile = open(ybinfile, 'r')
    ybins = eval(ybinfile.read())
    ybinfile.close()

    ## calculate the bin widths for the rapidity bins
    ybinwidths = {}
    for k,v in ybins.items():
        tmplist = list(abs(i - v[v.index(i)+1]) for i in v[:-1])
        ybinwidths[k] = [float('{n:.2f}'.format(n=i)) for i in tmplist]


    charges = options.charge.split(',')
    for charge in charges:

        ##file_pdfs = os.environ['CMSSW_BASE']+'/src/CMGTools/WMass/data/pdfs_prefit/pdf_variations_prefit.root'
        base = "/afs/cern.ch/work/e/emanuele/wmass/heppy/CMSSW_8_0_25/"
        file_pdfs = base+'/src/CMGTools/WMass/data/pdfs_prefit/pdf_variations_prefit.root'
        ## this gets the pdf central variation binned in the correct format
        nominal = utilities.getRebinned(ybins,charge,file_pdfs, 0)
        
        shape_syst = {}
        for pol in ['left','right','long']:
            histos = []
            for ip in xrange(1,NPDFs+1):
                #print "Loading polarization %s, histograms for pdf %d" % (pol,ip)
                ## this gets the pdf variations after correctly rebinning the YW
                pdf = utilities.getRebinned(ybins,charge,file_pdfs,ip)
                histos.append(pdf[pol])
            shape_syst[pol] = histos

        systematics = {}
        for pol in ['left','right','long']:
            #print "===> Running pol = ",pol
            systs=[]
            for iy,y in enumerate(ybinwidths['{ch}_{pol}'.format(ch=charge,pol=pol if not pol=='long' else 'right')]):
                #print "\tBin iy=%d,y=%f = " % (iy,y)
                nom = nominal[pol][iy]
                totUp=0
                for ip,pdf in enumerate(shape_syst[pol]):
                    # debug
                    relsyst = abs(nom-pdf[iy])/nom
                    if relsyst>0.20:
                        print "SOMETHING WENT WRONG WITH THIS PDF: %d HAS RELATIVE SYST = %f. SKIPPING !" % (ip,relsyst)
                    else:
                        totUp += math.pow(relsyst*nom,2)
                totUp = math.sqrt(totUp)
                print "Rel systematic for Y bin %d = +/-%.3f" % (iy,totUp/nom)
                systs.append(totUp)
            systematics[pol]=systs


        ## this is where the ugly stuff starts
        arr_val   = array.array('f', [])
        arr_ehi   = array.array('f', [])
        arr_elo   = array.array('f', [])
        arr_relv  = array.array('f', [])
        arr_relhi = array.array('f', [])
        arr_rello = array.array('f', [])
        arr_val_fit   = array.array('f', [])
        arr_ehi_fit   = array.array('f', [])
        arr_elo_fit   = array.array('f', [])
        arr_relv_fit  = array.array('f', [])
        arr_relhi_fit = array.array('f', [])
        arr_rello_fit = array.array('f', [])
        arr_rap   = array.array('f', [])
        arr_rlo   = array.array('f', [])
        arr_rhi   = array.array('f', [])


        for pol in ['left','right']:
            cp = '{ch}_{pol}'.format(ch=charge,pol=pol)

            arr_val       = array.array('f', []); arr_ehi       = array.array('f', []); arr_elo       = array.array('f', []);
            arr_val_fit   = array.array('f', []); arr_ehi_fit   = array.array('f', []); arr_elo_fit   = array.array('f', []);
            arr_relv      = array.array('f', []); arr_relhi     = array.array('f', []); arr_rello     = array.array('f', []);
            arr_relv_fit  = array.array('f', []); arr_relhi_fit = array.array('f', []); arr_rello_fit = array.array('f', []);
            arr_rap       = array.array('f', []); arr_rlo       = array.array('f', []); arr_rhi       = array.array('f', []);

            for iy,y in enumerate(ybinwidths['{ch}_{pol}'.format(ch=charge,pol=pol)]):
                parname = 'W{charge}_{pol}_W{charge}_{pol}_mu_Ybin_{iy}'.format(charge=charge,pol=pol,iy=iy)
                print 'at parameter name', parname

                ## old arr_val.append(nominal[pol][iy]/ybinwidths[cp][iy])
                ## old arr_ehi.append(systematics[pol][iy]/ybinwidths[cp][iy])
                ## old arr_elo.append(systematics[pol][iy]/ybinwidths[cp][iy]) # symmetric for the expected

                arr_relv. append(1.);
                arr_rello.append(systematics[pol][iy]/nominal[pol][iy])
                arr_relhi.append(systematics[pol][iy]/nominal[pol][iy]) # symmetric for the expected
                
                ## old arr_val_fit.append(fitval[parname]/ybinwidths[cp][iy])
                ## old arr_ehi_fit.append(fiterr[parname]/ybinwidths[cp][iy])
                ## old arr_elo_fit.append(fiterr[parname]/ybinwidths[cp][iy]) ## forced to be symmetric for now

                ## old print "par = ",parname," expected = ",nominal[pol][iy]," fitted = ",fitval[parname]

                ## old # renormalize the theo to the fitted ones (should match when running on the expected)
                ## old arr_ehi[-1] = arr_ehi[-1]/arr_val[-1]*arr_val_fit[-1]
                ## old arr_elo[-1] = arr_elo[-1]/arr_val[-1]*arr_val_fit[-1]
                ## old arr_val[-1] = arr_val_fit[-1]

                ## old arr_relv_fit .append(fitval[parname]/nominal[pol][iy])
                ## old arr_rello_fit.append(fiterr[parname]/nominal[pol][iy])
                ## old arr_relhi_fit.append(fiterr[parname]/nominal[pol][iy]) ## forced to be symmetric for now

                fitmean = valuesAndErrors[parname][0]
                arr_relv_fit .append(valuesAndErrors[parname][0])
                arr_rello_fit.append(abs(fitmean-valuesAndErrors[parname][1]))
                arr_relhi_fit.append(abs(fitmean-valuesAndErrors[parname][2]))

                arr_rap.append((ybins[cp][iy]+ybins[cp][iy+1])/2.)
                arr_rlo.append(abs(ybins[cp][iy]-arr_rap[-1]))
                arr_rhi.append(abs(ybins[cp][iy]-arr_rap[-1]))

            if 'left' in pol:
                print 'left {ch}: {i}'.format(ch=charge, i=sum(arr_val))
                #graphLeft      = ROOT.TGraphAsymmErrors(len(arr_val), arr_rap, arr_val, arr_rlo, arr_rhi, arr_elo, arr_ehi)
                graphLeft_rel  = ROOT.TGraphAsymmErrors(len(arr_relv), arr_rap, arr_relv, arr_rlo, arr_rhi, arr_rello, arr_relhi)
                #graphLeft     .SetName('graphLeft')
                graphLeft_rel .SetName('graphLeft_rel')
                #graphLeft_fit      = ROOT.TGraphAsymmErrors(len(arr_val_fit), arr_rap, arr_val_fit, arr_rlo, arr_rhi, arr_elo_fit, arr_ehi_fit)
                graphLeft_fit_rel  = ROOT.TGraphAsymmErrors(len(arr_relv_fit), arr_rap, arr_relv_fit, arr_rlo, arr_rhi, arr_rello_fit, arr_relhi_fit)
                #graphLeft_fit     .SetName('graphLeft_fit')
                graphLeft_fit_rel .SetName('graphLeft_fit_rel')
            else:
                print 'right {ch}: {i}'.format(ch=charge, i=sum(arr_val))
                #graphRight      = ROOT.TGraphAsymmErrors(len(arr_val), arr_rap, arr_val, arr_rlo, arr_rhi, arr_elo, arr_ehi)
                graphRight_rel  = ROOT.TGraphAsymmErrors(len(arr_relv), arr_rap, arr_relv, arr_rlo, arr_rhi, arr_rello, arr_relhi)
                #graphRight     .SetName('graphRight')
                graphRight_rel .SetName('graphRight_rel')
                #graphRight_fit      = ROOT.TGraphAsymmErrors(len(arr_val_fit), arr_rap, arr_val_fit, arr_rlo, arr_rhi, arr_elo_fit, arr_ehi_fit)
                graphRight_fit_rel  = ROOT.TGraphAsymmErrors(len(arr_relv_fit), arr_rap, arr_relv_fit, arr_rlo, arr_rhi, arr_rello_fit, arr_relhi_fit)
                #graphRight_fit     .SetName('graphRight_fit')
                graphRight_fit_rel .SetName('graphRight_fit_rel')

        c2 = ROOT.TCanvas('foo','', 800, 800)
        c2.GetPad(0).SetTopMargin(0.05)
        c2.GetPad(0).SetBottomMargin(0.15)
        c2.GetPad(0).SetLeftMargin(0.16)

        ## these are the colors...
        colorL = ROOT.kAzure+8
        colorR = ROOT.kOrange+7
        colorLf = ROOT.kAzure+3
        colorRf = ROOT.kOrange+9

        ## the four graphs exist now. now starting to draw them
        ## ===========================================================
        leg = ROOT.TLegend(0.60, 0.60, 0.85, 0.80)
        leg.SetFillStyle(0)
        leg.SetBorderSize(0)
#        leg.AddEntry(graphLeft , 'W^{{{ch}}} left (PDF systs)' .format(ch='+' if charge == 'plus' else '-'), 'f')
#        leg.AddEntry(graphLeft_fit , 'W^{{{ch}}} left (fit)' .format(ch='+' if charge == 'plus' else '-'), 'pl')
#        leg.AddEntry(graphRight, 'W^{{{ch}}} right (PDF systs)'.format(ch='+' if charge == 'plus' else '-'), 'f')
#        leg.AddEntry(graphRight_fit, 'W^{{{ch}}} right (fit)'.format(ch='+' if charge == 'plus' else '-'), 'pl')

###          graphLeft.SetTitle('W {ch}: Y_{{W}}'.format(ch=charge))
###          graphLeft.SetLineColor(colorL)
###          graphLeft.SetFillColor(colorL)
###          graphLeft.SetFillStyle(3002)
###          graphLeft_fit.SetLineWidth(2)
###          graphLeft_fit.SetLineColor(colorLf)
###          graphRight.SetLineColor(colorR)
###          graphRight.SetFillColor(colorR)
###          graphRight.SetFillStyle(3002)
###          graphRight_fit.SetLineWidth(2)
###          graphRight_fit.SetLineColor(colorRf)
###              
###          mg = ROOT.TMultiGraph()
###          mg.Add(graphLeft,'P2')
###          mg.Add(graphRight,'P2')
###          mg.Add(graphLeft_fit)
###          mg.Add(graphRight_fit)
###  
###          mg.Draw('Pa')
###          mg.GetXaxis().SetRangeUser(0.,6.)
###          mg.GetXaxis().SetTitle('|Y_{W}|')
###          mg.GetYaxis().SetTitle('dN/dy')
###          mg.GetXaxis().SetTitleSize(0.06)
###          mg.GetXaxis().SetLabelSize(0.04)
###          mg.GetYaxis().SetTitleSize(0.06)
###          mg.GetYaxis().SetLabelSize(0.04)
###          mg.GetYaxis().SetTitleOffset(1.2)
###  
###          leg.Draw('same')

        date = datetime.date.today().isoformat()
#        for ext in ['png', 'pdf']:
#            c2.SaveAs('{od}/genAbsY_pdfs_{date}_{ch}{suffix}_{t}.{ext}'.format(od=options.outdir, date=date, ch=charge, suffix=options.suffix, ext=ext,t='fromScans' if options.fromScans else 'fromToys'))

        ## now make the relative error plot:
        ## ======================================

        c2.Clear()
        c2.Divide(1,2)

        line = ROOT.TF1("horiz_line","1",0.0,3.0);
        line.SetLineColor(ROOT.kBlack);
        line.SetLineWidth(2);

        padUp = c2.cd(1)
        padUp.SetTickx(1)
        padUp.SetTicky(1)
        padUp.SetGridy(1)
        padUp.SetBottomMargin(0.10)

        graphLeft_rel.SetLineWidth(5)
        graphLeft_rel.SetLineColor(colorL)
        graphLeft_rel.SetFillColor(colorL)
        graphLeft_rel.SetFillStyle(3002)
        graphLeft_fit_rel.SetLineWidth(2)
        graphLeft_fit_rel.SetLineColor(colorLf)
        graphRight_rel.SetLineWidth(5)
        graphRight_rel.SetLineColor(colorR)
        graphRight_rel.SetFillColor(colorR)
        graphRight_rel.SetFillStyle(3002)
        graphRight_fit_rel.SetLineWidth(2)
        graphRight_fit_rel.SetLineColor(colorRf)

        mgLeft = ROOT.TMultiGraph()
        mgLeft.SetTitle('W^{{{ch}}}: left'.format(ch='+' if charge=='plus' else '-'))
        mgLeft.Add(graphLeft_rel,'P2')
        mgLeft.Add(graphLeft_fit_rel)
        mgRight = ROOT.TMultiGraph()
        mgRight.SetTitle('W^{{{ch}}}: right'.format(ch='+' if charge=='plus' else '-'))
        mgRight.Add(graphRight_rel,'P2')
        mgRight.Add(graphRight_fit_rel)

        mgLeft.Draw('Pa')
        mgLeft.GetXaxis().SetRangeUser(0., 3.)
        mgLeft.GetYaxis().SetRangeUser(0.85, 1.15)
        mgLeft.GetXaxis().SetTitleSize(0.06)
        mgLeft.GetXaxis().SetLabelSize(0.06)
        mgLeft.GetYaxis().SetTitleSize(0.06)
        mgLeft.GetYaxis().SetLabelSize(0.06)

        leg.Draw('same')
        line.Draw("Lsame");
        padUp.RedrawAxis("sameaxis");

        padDown = c2.cd(2)
        padDown.SetTickx(1)
        padDown.SetTicky(1)
        padDown.SetGridy(1)
        padDown.SetBottomMargin(0.15)
        mgRight.Draw('pa')
        mgRight.GetXaxis().SetRangeUser(0., 3.)
        mgRight.GetYaxis().SetRangeUser(0.85, 1.15)
        mgRight.GetXaxis().SetTitle('|Y_{W}|')
        mgRight.GetXaxis().SetTitleSize(0.06)
        mgRight.GetXaxis().SetLabelSize(0.06)
        mgRight.GetYaxis().SetTitleSize(0.06)
        mgRight.GetYaxis().SetLabelSize(0.06)
        line.Draw("Lsame");
        padDown.RedrawAxis("sameaxis");

        for ext in ['png', 'pdf']:
            c2.SaveAs('{od}/genAbsY_pdfs_{date}_{ch}{suffix}_relative_{t}.{ext}'.format(od=options.outdir, date=date, ch=charge, suffix=options.suffix, ext=ext,t=options.type))
