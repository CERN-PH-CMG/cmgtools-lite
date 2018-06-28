import ROOT, datetime, array, os


## usage:
## python symmetrizeMatrix.py --infile multidimfit.root --outdir ~/www/private/w-helicity-13TeV/correlationMatrices/ --suffix <suffix>  --dc <input_datacard>

def getScales(ybins, charge, pol, infile, returnError = False):
    histo_file = ROOT.TFile(infile, 'READ')

    histo_gen  = histo_file.Get('w{ch}_wy_W{ch}_{pol}'     .format(ch=charge, pol=pol))
    histo_reco = histo_file.Get('w{ch}_wy_reco_W{ch}_{pol}'.format(ch=charge, pol=pol))

    scales = []
    errors = []
    numhist = ROOT.TH1F('num','num', 1, 0., 1.)
    denhist = ROOT.TH1F('den','den', 1, 0., 1.)
    for iv, val in enumerate(ybins[:-1]):
        errnum = ROOT.Double()
        errden = ROOT.Double()
        istart = histo_gen.FindBin(val)
        iend   = histo_gen.FindBin(ybins[iv+1])
        num = histo_gen .IntegralAndError(istart, iend-1, errnum) ## do not include next bin
        den = histo_reco.IntegralAndError(istart, iend-1, errden) ## do not include next bin
        numhist.SetBinContent(1, num); numhist.SetBinError(1, errnum)
        denhist.SetBinContent(1, den); denhist.SetBinError(1, errden)
        numhist.Divide(denhist)
        tmp_ratio = numhist.GetBinContent(1) #num/den
        scales.append(tmp_ratio)
        ## make the errors relative to the central value
        errors.append(numhist.GetBinError(1)/tmp_ratio)

    if returnError:
        return errors
    
    return scales

if __name__ == "__main__":

    ROOT.gROOT.SetBatch()
    ROOT.gStyle.SetOptStat(0)

    ROOT.gStyle.SetPalette(1)

    date = datetime.date.today().isoformat()

    from optparse import OptionParser
    parser = OptionParser(usage='%prog [options] ')
    parser.add_option('-i','--infile', dest='infile', default='', type='string', help='file with fitresult')
    parser.add_option('-o','--outdir', dest='outdir', default='', type='string', help='outdput directory to save the matrix')
    parser.add_option(     '--suffix', dest='suffix', default='', type='string', help='suffix for the correlation matrix')
    parser.add_option(     '--dc'    , dest='dc'    , default='', type='string', help='the corresponding datacard (for the rates)')
    parser.add_option(     '--sf'    , dest='scaleFile'    , default='', type='string', help='path of file with the scaling/unfolding')
    (options, args) = parser.parse_args()

    ##infile = ROOT.TFile('/afs/cern.ch/work/e/emanuele/wmass/fit/CMSSW_8_1_0/src/multidimfit.root','read')
    infile = ROOT.TFile(options.infile, 'read')

    if 'multidimfit' in options.infile:
        fitresult = infile.Get('fit_mdf')
    else:
        fitresult = infile.Get('fit_s')

    h2_corr = fitresult.correlationHist()

    c = ROOT.TCanvas()

    ## some more ROOT "magic"
    parlist = fitresult.floatParsFinal()
    l_params = list(parlist.at(i).GetName() for i in range(len(parlist)))

    ## pretty dumb check if we're dealing with W+ or W-
    nplus  = len(list(p for p in l_params if 'plus'  in p))
    nminus = len(list(p for p in l_params if 'minus' in p))
    charge = 'plus' if nplus > nminus else 'minus'

    print 'assuming this is W {ch}'.format(ch=charge)

    ## ======================================
    ## saving the original correlation matrix
    h2_corr.Draw('colz')
    for ext in ['png', 'pdf']:
        c.SaveAs('{od}/corrMatrix_{date}_{suff}_{ch}_original.{ext}'.format(od=options.outdir, date=date, suff=options.suffix, ch=charge, ext=ext))

    h2_new = h2_corr.Clone('correlationMatrix_symmetric')
    h2_new.Reset()
    ## ======================================


    hel_pars = list(p for p in l_params if 'norm_W' in p)
    long_par = list(a for a in l_params if 'long' in a)
    rest     = list(p for p in l_params if p not in hel_pars and p not in long_par)
    pars_r   = list(p for p in hel_pars if 'right' in p)
    pars_r = sorted(pars_r, key = lambda x: int(x.split('_')[-2]))
    pars_l   = list(p for p in hel_pars if 'left' in p)
    pars_l = sorted(pars_l, key = lambda x: int(x.split('_')[-2]), reverse=True )

    l_sorted_new = pars_r + pars_l + long_par + rest

    for il,l in enumerate(l_sorted_new):
        new_l = l.lstrip('norm_').replace('right','WR').replace('left','WL').replace('Ybin_','')
        if 'Ybin' in l:
            name_l = l.split('_')[1:]
            new_l  = name_l[0].replace('plus','+').replace('minus','-')+' '+name_l[-4]
            new_l += ' bin'+(name_l[-2] if 'left' in l else name_l[-1])
        h2_new.GetXaxis().SetBinLabel(il+1, new_l)
        h2_new.GetYaxis().SetBinLabel(il+1, new_l)
        for il2,l2 in enumerate(l_sorted_new):
            binx = h2_corr.GetXaxis().FindBin(l)
            biny = h2_corr.GetYaxis().FindBin(l2)
            new_l2 = l2.lstrip('norm_').replace('right','WR ').replace('left','WL ')
            h2_new.SetBinContent(il+1, il2+1, h2_corr.GetBinContent(binx, biny))

    h2_new.Draw('colz')
    for ext in ['png', 'pdf']:
        c.SaveAs('{od}/corrMatrix_{date}_{suff}_{ch}_symmetric.{ext}'.format(od=options.outdir, date=date, suff=options.suffix, ch=charge, ext=ext))

    ## =======================================================
    ## == MAKING THE RAPIDITY DISTRIBUTIONS ==================
    ## =======================================================

    if options.dc:
        ## assuming the datacard and the binningYW.txt file are in the same directory
        ybinfile = open(options.dc.replace(os.path.basename(options.dc),'binningYW.txt'), 'r')
        ybinline = ybinfile.readlines()[0]
        ybins = list(float(i) for i in ybinline.split())
        ybinfile.close()

        ## calculate the bin widths for the rapidity bins
        ybinswidths = list(abs(i - ybins[ybins.index(i)+1]) for i in ybins[:-1])

        plist2 = fitresult.constPars()
        lpars2 = list(plist2.at(i).GetName() for i in range(len(plist2)))

        hel_pars2 = list(p for p in lpars2 if 'norm_W' in p)
        long_par2 = list(a for a in lpars2 if 'long' in a)
        rest      = list(p for p in lpars2 if p not in hel_pars2 and p not in long_par2)
        rpars2    = list(p for p in hel_pars2 if 'right' in p)
        rpars2    = sorted(rpars2, key = lambda x: int(x.split('_')[-2]))
        lpars2    = list(p for p in hel_pars2 if 'left' in p)
        lpars2    = sorted(lpars2, key = lambda x: int(x.split('_')[-2]), reverse=True )

        sorted_rap = rpars2 + pars_r + pars_l + lpars2

        if not len(ybins)-1 == len(sorted_rap):
            print 'SOMETHING WENT TERRIBLY WRONG'

        ## get the rates and processes from the datacard. they're necessarily in the same order
        dcfile = open(options.dc, 'r')
        dclines = dcfile.readlines()
        procline = list(line for line in dclines if line.startswith('process')); procline = procline[0]; procs = procline.split()
        rateline = list(line for line in dclines if line.startswith('rate'   )); rateline = rateline[0]; rates = rateline.split()

        arr_val   = array.array('f', [])
        arr_ehi   = array.array('f', [])
        arr_elo   = array.array('f', [])
        arr_relv  = array.array('f', [])
        arr_relhi = array.array('f', [])
        arr_rello = array.array('f', [])
        arr_rap   = array.array('f', [])
        arr_rlo   = array.array('f', [])
        arr_rhi   = array.array('f', [])


        totalrate = 0.
        fitAbsoluteRates = False
        for p in sorted_rap:
            tmp_procname = '_'.join(p.split('_')[1:-1])
            if float(rates[procs.index(tmp_procname)]) > 1: # means that the rates are SFs wrt the expected ones
                print 'I FIGURE YOU FIT RELATIVE RATES (i.e. rate parameters around 1.0)!'
                totalrate += float(rates[procs.index(tmp_procname)])
            else: 
                print 'I FIGURE YOU FIT ABSOLUTE RATES (i.e. big numbers)!'
                fitAbsoluteRates = True
        if fitAbsoluteRates:
            for ip,p in enumerate(sorted_rap):
                tmp_par = fitresult.floatParsFinal().find(p) if p in l_sorted_new else fitresult.constPars().find(p)
                totalrate += tmp_par.getVal()

        #totalrate=1.
        #sys.exit()

        for ip,p in enumerate(sorted_rap):
            tmp_par = fitresult.floatParsFinal().find(p) if p in l_sorted_new else fitresult.constPars().find(p)
            tmp_procname = '_'.join(p.split('_')[1:-1])
            if fitAbsoluteRates:
                arr_val.append(tmp_par.getVal()/totalrate/ybinswidths[ip])
                arr_ehi.append(abs(tmp_par.getAsymErrorHi())/totalrate/ybinswidths[ip])
                arr_elo.append(abs(tmp_par.getAsymErrorLo() if tmp_par.hasAsymError() else tmp_par.getAsymErrorHi())/totalrate/ybinswidths[ip])

                tmp_par_init = fitresult.floatParsFinal().find(p) if p in l_sorted_new else fitresult.constPars().find(p)
                arr_relv .append(tmp_par.getVal()/tmp_par_init.getVal())
                arr_rello.append(abs(tmp_par.getAsymErrorHi())/tmp_par_init.getVal())
                arr_relhi.append(abs(tmp_par.getAsymErrorLo() if tmp_par.hasAsymError() else tmp_par.getAsymErrorHi())/tmp_par_init.getVal())
            else:
                tmp_rate = float(rates[procs.index(tmp_procname)])
                arr_val.append(tmp_rate/totalrate/ybinwidths[ip]*tmp_par.getVal())
                arr_ehi.append(tmp_rate/totalrate/ybinwidths[ip]*abs(tmp_par.getAsymErrorHi()))
                arr_elo.append(tmp_rate/totalrate/ybinwidths[ip]*abs(tmp_par.getAsymErrorLo() if tmp_par.hasAsymError() else tmp_par.getAsymErrorHi()))

                arr_relv .append(tmp_par.getVal())
                arr_rello.append(abs(tmp_par.getAsymErrorHi()))
                arr_relhi.append(abs(tmp_par.getAsymErrorLo() if tmp_par.hasAsymError() else tmp_par.getAsymErrorHi()))

            arr_rap.append((ybins[ip]+ybins[ip+1])/2.)
            arr_rlo.append(abs(ybins[ip]-arr_rap[-1]))
            arr_rhi.append(abs(ybins[ip]-arr_rap[-1]))

        graph     = ROOT.TGraphAsymmErrors(len(arr_val), arr_rap, arr_val, arr_rlo, arr_rhi, arr_elo, arr_ehi)
        graph.SetTitle('W {ch}: Y_{{W}}'.format(ch=charge))
        graph.SetFillColor(ROOT.kBlue+1)
        graph.SetFillStyle(3001)
        #graph.GetXaxis().SetRangeUser(ybins[0],ybins[-1])
        graph.GetXaxis().SetRangeUser(-4.,4.)
        graph.GetXaxis().SetTitle('Y_{W}')
        graph.GetYaxis().SetTitle('N_{events}/N_{total}')
        c2 = ROOT.TCanvas()
        graph.Draw('a2')
        for ext in ['png', 'pdf']:
            c2.SaveAs('{od}/rapidityDistribution_{date}_{suff}_{ch}.{ext}'.format(od=options.outdir, date=date, suff=options.suffix, ch=charge, ext=ext))

        graph_rel = ROOT.TGraphAsymmErrors(len(arr_val), arr_rap, arr_relv, arr_rlo, arr_rhi, arr_rello, arr_relhi)
        graph_rel.SetTitle('W {ch}: Y_{{W}}'.format(ch=charge))
        graph_rel.SetMarkerStyle(20)
        graph_rel.SetMarkerColor(ROOT.kBlack)
        graph_rel.SetMarkerSize(0.8)
        graph_rel.SetFillColor(ROOT.kBlue+1)
        graph_rel.SetFillStyle(3003)
        graph_rel.GetXaxis().SetRangeUser(-4.,4.)
        graph_rel.GetYaxis().SetRangeUser(0.97,1.03)
        graph_rel.GetXaxis().SetTitle('Y_{W}')
        graph_rel.GetYaxis().SetTitle('rate par. fit value')
        graph_rel.Draw('Pa5')
        for ext in ['png', 'pdf']:
            c2.SaveAs('{od}/rapidityDistribution_{date}_{suff}_{ch}_relative.{ext}'.format(od=options.outdir, date=date, suff=options.suffix, ch=charge, ext=ext))

        ## some "unfolding" stuff first
        if options.scaleFile:
            arr_scales_left  = array.array('f', getScales(ybins, charge, 'left' , options.scaleFile))
            arr_scales_right = array.array('f', getScales(ybins, charge, 'right', options.scaleFile))
        else:
            arr_scales_left = [1. for y in ybins[1:]]
            arr_scales_right = [1. for y in ybins[1:]]

        arr_val_scaled_left  = []
        arr_val_scaled_right = []

        for i in range(len(arr_scales_left)):
            arr_val_scaled_left .append(arr_scales_left[i] *arr_val[i])
            arr_val_scaled_right.append(arr_scales_right[i]*arr_val[i])

        arr_val_scaled_left  = array.array('f', arr_val_scaled_left )
        arr_val_scaled_right = array.array('f', arr_val_scaled_right)


        c3 = ROOT.TCanvas('foo','',800,800)
        half = len(arr_val)/2
        graph_right = ROOT.TGraphAsymmErrors(half, arr_rap[half:], arr_val_scaled_right[:half][::-1], arr_rlo[half:], arr_rhi[half:], arr_elo[:half][::-1], arr_ehi[:half][::-1])
        graph_left  = ROOT.TGraphAsymmErrors(half, arr_rap[half:], arr_val_scaled_left[half:], arr_rlo[half:], arr_rhi[half:], arr_elo[half:], arr_ehi[half:])
        graph_left .SetFillColor(ROOT.kAzure+8 )
        graph_right.SetFillColor(ROOT.kOrange+7)
        graph_left .GetXaxis().SetRangeUser(0.,3.0)
        graph_right.GetXaxis().SetRangeUser(0.,3.0)

        leg = ROOT.TLegend(0.70, 0.70, 0.90, 0.90)
        leg.SetFillStyle(0)
        leg.SetBorderSize(0)

        ymax = 6.0

        mg = ROOT.TMultiGraph()
        mg.Add(graph_right)
        mg.Add(graph_left )
        leg.AddEntry(graph_left , 'W^{{{ch}}} left' .format(ch='+' if charge == 'plus' else '-'), 'f')
        leg.AddEntry(graph_right, 'W^{{{ch}}} right'.format(ch='+' if charge == 'plus' else '-'), 'f')
        mg.Draw('Pa5')
        mg.GetXaxis().SetRangeUser(0.0,ymax)
        mg.GetXaxis().SetTitle('|Y_{W}|')
        mg.GetXaxis().SetTitleSize(0.06)
        mg.GetXaxis().SetLabelSize(0.04)
        mg.GetYaxis().SetTitleSize(0.06)
        mg.GetYaxis().SetLabelSize(0.04)
        mg.GetYaxis().SetTitle('N_{events}/N_{total}')
        mg.GetYaxis().SetTitleOffset(1.2)
        c3.GetPad(0).SetTopMargin(0.05)
        c3.GetPad(0).SetBottomMargin(0.15)
        c3.GetPad(0).SetLeftMargin(0.16)

        leg.Draw('same')

        for ext in ['png', 'pdf']:
            c3.SaveAs('{od}/rapidityDistribution_{date}_{suff}_{ch}_absRapLeftRight.{ext}'.format(od=options.outdir, date=date, suff=options.suffix, ch=charge, ext=ext))

    
