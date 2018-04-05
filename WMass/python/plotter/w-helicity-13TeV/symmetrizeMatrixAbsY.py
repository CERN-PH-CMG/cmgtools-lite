import ROOT, datetime, array, os
import re

## usage:
## python symmetrizeMatrix.py --infile multidimfit.root --outdir ~/www/private/w-helicity-13TeV/correlationMatrices/ --suffix <suffix>  --dc <input_datacard>

def getScales(ybins, charge, pol, infile, doNLO=True, returnError=False):
    histo_file = ROOT.TFile(infile, 'READ')

    histlist = list(i.GetName() for i in histo_file.GetListOfKeys())

    chs = 'W{ch}'.format(ch=charge)

    if doNLO:
        name_gen  = [i for i in histlist if chs in i and pol in i and not 'LO' in i and not 'reco' in i]
        name_reco = [i for i in histlist if chs in i and pol in i and not 'LO' in i and     'reco' in i]
    else:
        name_gen  = [i for i in histlist if chs in i and pol in i and     'LO' in i and not 'reco' in i]
        name_reco = [i for i in histlist if chs in i and pol in i and     'LO' in i and     'reco' in i]

    if not name_gen or not name_reco:
        print 'DID NOT FIND THE HISTOGRAMS IN THE SCALEFILE for {nlo}'.format(nlo='NLO' if doNLO else 'LO')
        print 'Will continue without LO-NLO uncertainty...'
        a = []
        return a
    else:
        name_gen  = name_gen [0]
        name_reco = name_reco[0]

    histo_gen  = histo_file.Get(name_gen )
    histo_reco = histo_file.Get(name_reco)

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

    date = datetime.date.today().isoformat()

    from optparse import OptionParser
    parser = OptionParser(usage='%prog [options] ')
    parser.add_option('-i','--infile', dest='infile', default='', type='string', help='file with fitresult')
    parser.add_option('-o','--outdir', dest='outdir', default='', type='string', help='outdput directory to save the matrix')
    parser.add_option(     '--suffix', dest='suffix', default='', type='string', help='suffix for the correlation matrix')
    parser.add_option(     '--dc'    , dest='dc'    , default='', type='string', help='the corresponding datacard (for the rates)')
    parser.add_option(     '--sf'    , dest='scaleFile'    , default='', type='string', help='path of file with the scaling/unfolding')
    parser.add_option(     '--no-date-name', dest="noDateInName", action="store_true", default=False, help="Do not append date in output name (by default it does)")
    (options, args) = parser.parse_args()

    if options.noDateInName:
        date = ""

    if not os.path.isdir(options.outdir):
        os.system('mkdir -p {od}'.format(od=options.outdir))
    os.system('cp {pf} {od}'.format(pf='/afs/cern.ch/user/g/gpetrucc/php/index.php',od=options.outdir))

    ##infile = ROOT.TFile('/afs/cern.ch/work/e/emanuele/wmass/fit/CMSSW_8_1_0/src/multidimfit.root','read')
    infile = ROOT.TFile(options.infile, 'read')

    if 'multidimfit' in options.infile:
        fitresult = infile.Get('fit_mdf')
    else:
        fitresult = infile.Get('fit_s')

    h2_corr = fitresult.correlationHist()

    c = ROOT.TCanvas("c","",1200,800)
    ROOT.gStyle.SetPalette(55)
    ROOT.gStyle.SetNumberContours(40); # default is 20 (values on palette go from -1 to 1)

    c.SetLeftMargin(0.09)
    c.SetRightMargin(0.11)
    c.SetBottomMargin(0.15)

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
    pars_r = sorted(pars_r, key = lambda x: int(x.split('_')[-1]), reverse=True)
    pars_l   = list(p for p in hel_pars if 'left' in p)
    pars_l = sorted(pars_l, key = lambda x: int(x.split('_')[-1]), reverse=False)

    l_sorted_new = pars_r + pars_l + long_par + rest
    print "######################################"
    print "fitresult.floatParsFinal(): " + str(l_params)
    print "######################################"

    helicities = ["right", "left", "long"]

    for il,l in enumerate(l_sorted_new):

        #####################
        ### remove CMS_Blabla if any 
        new_l = l.replace('CMS_We_','')
        new_l = new_l.replace('CMS_','')
        ### make some names shorter
        if any(h in l for h in helicities):    
            chargeID = ""
            helID    = ""
            ### Evaluate charge  
            if 'plus' in l:
                chargeID = "+"
            elif 'minus' in l:
                chargeID = "-"
            ### evaluate helicity
            if 'left' in l:
                helID = "L"
            elif 'right' in l:
                helID = "R"
            elif 'long' in l:
                helID = "0"
            ### evaluate some specific parameters
            if l.startswith("norm"):
                new_l = "W%s%s" % (helID, chargeID)
            elif l.startswith("eff_unc"):
                new_l = "#deltaeff W%s%s" % (helID, chargeID)
            elif l.startswith("lumi"):
                new_l = "lumi W%s%s" % (helID, chargeID)

            ### evaluate rapidity bin
            if 'Ybin_' in l:
                regex = re.compile('Ybin_'+'([0-9]*)')
                regexp_out = regex.findall(l)
                if len(regexp_out):
                    YbinNumber = "Y%d" % int(regexp_out[0])
                    #print "bin: " + str(YbinNumber)   
                    new_l = new_l + " " + YbinNumber
        #####################

        h2_new.GetXaxis().SetBinLabel(il+1, new_l)
        h2_new.GetYaxis().SetBinLabel(il+1, new_l)
        h2_new.GetYaxis().SetLabelSize(0.025)
        for il2,l2 in enumerate(l_sorted_new):
            binx = h2_corr.GetXaxis().FindBin(l)
            biny = h2_corr.GetYaxis().FindBin(l2)
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
        ybinwidths = list(abs(i - ybins[ybins.index(i)+1]) for i in ybins[:-1])

        plist2 = fitresult.constPars()
        lpars2 = list(plist2.at(i).GetName() for i in range(len(plist2)))
        print "######################################"
        print "fitresult.constPars(): " + str(lpars2)
        print "######################################"

        hel_pars2 = list(p for p in lpars2 if 'norm_W' in p)
        long_par2 = list(a for a in lpars2 if 'long' in a)
        rest      = list(p for p in lpars2 if p not in hel_pars2 and p not in long_par2)
        rpars2    = list(p for p in hel_pars2 if 'right' in p)
        rpars2    = sorted(rpars2, key = lambda x: int(x.split('_')[-1]), reverse=True)
        lpars2    = list(p for p in hel_pars2 if 'left' in p)
        lpars2    = sorted(lpars2, key = lambda x: int(x.split('_')[-1]), reverse=False)

        sorted_rap = rpars2 + pars_r + pars_l + lpars2

        tmp_pars_l = pars_l
        pars_l = pars_l + lpars2
        pars_r = list(reversed(pars_r)) + list(reversed(rpars2))

        if not  (2 * (len(ybins)-1)) == len(sorted_rap):
            print 'SOMETHING WENT TERRIBLY WRONG'
            print "len(ybins)-1 = %d;   len(sorted_rap) = %d" % (len(ybins)-1, len(sorted_rap))

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


        ###########################################################
        ### Names in datacard are like Wplus_right_Wplus_el_Ybin_9, but fit_mdf->Print() shows norm_Wplus_right_Wplus_Ybin_9
        ### Need a temporary patch to remove el from names copied from datacard, if they begin with 'norm_' .
        tmp_procs = []
        channel_mu1_el2 = 0
        for process in procs:
            ### electron case
            if '_el_Ybin' in process:
                channel_mu1_el2 = 2
                tmp_procs.append(process.replace('_el_Ybin','_Ybin'))
            ### muon case
            elif '_mu_Ybin' in process:
                tmp_procs.append(process.replace('_mu_Ybin','_Ybin'))
                channel_mu1_el2 = 1
            else:
                tmp_procs.append(process)
        procs = tmp_procs

        if channel_mu1_el2 == 1:
            print "Assuming you are working with muons"
        elif channel_mu1_el2 == 2:
            print "Assuming you are working with electrons"

        totalrate = 0.
        fitAbsoluteRates = False
        for p in sorted_rap:
            tmp_procname = '_'.join(p.split('_')[1:])
            if float(rates[procs.index(tmp_procname)]) > 1: # means that the rates are SFs wrt the expected ones
                #print 'I FIGURE YOU FIT RELATIVE RATES (i.e. rate parameters around 1.0)!'
                totalrate += float(rates[procs.index(tmp_procname)])
            else: 
                #print 'I FIGURE YOU FIT ABSOLUTE RATES (i.e. big numbers)!'
                fitAbsoluteRates = True
        if fitAbsoluteRates:
            for ip,p in enumerate(sorted_rap):
                tmp_par = fitresult.floatParsFinal().find(p) if p in l_sorted_new else fitresult.constPars().find(p)
                totalrate += tmp_par.getVal()

        ## ybinwidths = list(reversed(ybinwidths)) + ybinwidths
        ## ybins = list(-1.*i for i in reversed(ybins[1:])) + ybins

        for pol in [pars_l, pars_r]:
            arr_val   = array.array('f', []); arr_ehi   = array.array('f', []); arr_elo   = array.array('f', []);
            arr_relv  = array.array('f', []); arr_relhi = array.array('f', []); arr_rello = array.array('f', []);
            arr_rap   = array.array('f', []); arr_rlo   = array.array('f', []); arr_rhi   = array.array('f', []);
            ## for the reco thing...
            arr_valReco   = array.array('f', []); arr_ehiReco   = array.array('f', []); arr_eloReco   = array.array('f', []);

            for ip,p in enumerate(pol):

                tmp_par = fitresult.floatParsFinal().find(p) if p in l_sorted_new else fitresult.constPars().find(p)
                tmp_procname = '_'.join(p.split('_')[1:])

                if fitAbsoluteRates:
                    arr_val.append(tmp_par.getVal()/totalrate/ybinwidths[ip])
                    arr_ehi.append(abs(tmp_par.getAsymErrorHi())/totalrate/ybinwidths[ip])
                    arr_elo.append(abs(tmp_par.getAsymErrorLo() if tmp_par.hasAsymError() else tmp_par.getAsymErrorHi())/totalrate/ybinwidths[ip])

                    #tmp_par_eff =  fitresult.constPars().find(p.replace('norm_','eff_'))  # won't work anymore since '_el_' is in efficiency parameter but not in p 
                    tmp_par_eff_name = p.replace('norm_','eff_')
                    if channel_mu1_el2 > 0:
                        print "WARNING: getting name of efficiency parameter: we are adding 'us_%s_Ybin' to 'us_Ybin' " % "el" if channel_mu1_el2 == 2 else "mu" 
                        print "before " + tmp_par_eff_name
                        if channel_mu1_el2 == 2 and not '_el_Ybin' in tmp_par_eff_name:                        
                            tmp_par_eff_name = tmp_par_eff_name.replace('us_Ybin','us_el_Ybin')
                        elif channel_mu1_el2 == 1 and not '_mu_Ybin' in tmp_par_eff_name:
                            tmp_par_eff_name = tmp_par_eff_name.replace('us_Ybin','us_mu_Ybin')
                        print "after " + tmp_par_eff_name
                    #print "ip, p, eff_par = %d %s %s" % (ip, str(p), str(tmp_par_eff_name))
                    tmp_par_eff =  fitresult.constPars().find(tmp_par_eff_name)
                    tmp_eff = tmp_par_eff.getVal()
                    arr_valReco.append(tmp_par.getVal()/totalrate/ybinwidths[ip]*tmp_eff)
                    arr_ehiReco.append(abs(tmp_par.getAsymErrorHi())/totalrate/ybinwidths[ip]*tmp_eff)
                    arr_eloReco.append(abs(tmp_par.getAsymErrorLo() if tmp_par.hasAsymError() else tmp_par.getAsymErrorHi())/totalrate/ybinwidths[ip]*tmp_eff)

                    tmp_par_init = fitresult.floatParsInit().find(p) if p in l_sorted_new else fitresult.constPars().find(p)
                    arr_relv .append(tmp_par.getVal()/tmp_par_init.getVal())
                    arr_rello.append(abs(tmp_par.getAsymErrorLo())/tmp_par_init.getVal() if tmp_par.hasAsymError() else abs(tmp_par.getAsymErrorHi())/tmp_par_init.getVal())
                    arr_relhi.append(abs(tmp_par.getAsymErrorHi())/tmp_par_init.getVal())
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

            if 'left' in pol[0]:
                print 'left {ch}: {i}'.format(ch=charge, i=sum(arr_val))
                graphLeft      = ROOT.TGraphAsymmErrors(len(arr_val), arr_rap, arr_val, arr_rlo, arr_rhi, arr_elo, arr_ehi)
                graphLeft_rel  = ROOT.TGraphAsymmErrors(len(arr_relv), arr_rap, arr_relv, arr_rlo, arr_rhi, arr_rello, arr_relhi)
                graphLeft_reco = ROOT.TGraphAsymmErrors(len(arr_valReco), arr_rap, arr_valReco, arr_rlo, arr_rhi, arr_eloReco, arr_ehiReco)
                graphLeft     .SetName('graphLeft')
                graphLeft_rel .SetName('graphLeft_rel')
                graphLeft_reco.SetName('graphLeft_reco')
            else:
                print 'right {ch}: {i}'.format(ch=charge, i=sum(arr_val))
                graphRight      = ROOT.TGraphAsymmErrors(len(arr_val), arr_rap, arr_val, arr_rlo, arr_rhi, arr_elo, arr_ehi)
                graphRight_rel  = ROOT.TGraphAsymmErrors(len(arr_relv), arr_rap, arr_relv, arr_rlo, arr_rhi, arr_rello, arr_relhi)
                graphRight_reco = ROOT.TGraphAsymmErrors(len(arr_valReco), arr_rap, arr_valReco, arr_rlo, arr_rhi, arr_eloReco, arr_ehiReco)
                graphRight     .SetName('graphRight')
                graphRight_rel .SetName('graphRight_rel')
                graphRight_reco.SetName('graphRight_reco')

        c2 = ROOT.TCanvas('foo','', 800, 800)
        c2.GetPad(0).SetTopMargin(0.05)
        c2.GetPad(0).SetBottomMargin(0.15)
        c2.GetPad(0).SetLeftMargin(0.16)

        ## these are the colors...
        colorL = ROOT.kAzure+8
        colorR = ROOT.kOrange+7

        ## the four graphs exist now. now starting to draw them
        ## ===========================================================
        leg = ROOT.TLegend(0.60, 0.60, 0.85, 0.80)
        leg.SetFillStyle(0)
        leg.SetBorderSize(0)
        leg.AddEntry(graphLeft , 'W^{{{ch}}} left' .format(ch='+' if charge == 'plus' else '-'), 'f')
        leg.AddEntry(graphRight, 'W^{{{ch}}} right'.format(ch='+' if charge == 'plus' else '-'), 'f')

        graphLeft.SetTitle('W {ch}: Y_{{W}}'.format(ch=charge))
        graphLeft.SetFillColor(colorL)
        graphRight.SetFillColor(colorR)

        mg = ROOT.TMultiGraph()
        mg.Add(graphLeft)
        mg.Add(graphRight)

        mg.Draw('Pa2')
        mg.GetXaxis().SetRangeUser(0.,6.)
        mg.GetXaxis().SetTitle('|Y_{W}|')
        mg.GetYaxis().SetTitle('dN/dy')
        mg.GetXaxis().SetTitleSize(0.06)
        mg.GetXaxis().SetLabelSize(0.04)
        mg.GetYaxis().SetTitleSize(0.06)
        mg.GetYaxis().SetLabelSize(0.04)
        mg.GetYaxis().SetTitleOffset(1.2)

        leg.Draw('same')

        for ext in ['png', 'pdf']:
            c2.SaveAs('{od}/rapidityDistribution_{date}_{suff}_{ch}.{ext}'.format(od=options.outdir, date=date, suff=options.suffix, ch=charge, ext=ext))


        ## make the reco plot as well, for good measure
        ## ========================================================

        c2.Clear()
        leg.Clear()

        leg.AddEntry(graphLeft_reco , 'W^{{{ch}}} left (reco)' .format(ch='+' if charge == 'plus' else '-'), 'f')
        leg.AddEntry(graphRight_reco, 'W^{{{ch}}} right (reco)'.format(ch='+' if charge == 'plus' else '-'), 'f')

        graphLeft_reco .SetTitle('W {ch}: Y_{{W}}'.format(ch=charge))
        graphLeft_reco .SetFillColor(colorL)
        graphRight_reco.SetFillColor(colorR)

        mgReco = ROOT.TMultiGraph()
        mgReco.Add(graphLeft_reco)
        mgReco.Add(graphRight_reco)

        mgReco.Draw('Pa2')
        mgReco.GetXaxis().SetRangeUser(0.,6.)
        mgReco.GetXaxis().SetTitle('|Y_{W}|')
        mgReco.GetYaxis().SetTitle('dN/dy (reco)')
        mgReco.GetXaxis().SetTitleSize(0.06)
        mgReco.GetXaxis().SetLabelSize(0.04)
        mgReco.GetYaxis().SetTitleSize(0.06)
        mgReco.GetYaxis().SetLabelSize(0.04)
        mgReco.GetYaxis().SetTitleOffset(1.2)

        leg.Draw('same')

        for ext in ['png', 'pdf']:
            c2.SaveAs('{od}/rapidityDistribution_RECO_{date}_{suff}_{ch}.{ext}'.format(od=options.outdir, date=date, suff=options.suffix, ch=charge, ext=ext))



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
        padUp.SetBottomMargin(0.15)

        graphLeft_rel.SetTitle('W^{{{ch}}}: left'.format(ch='+' if charge=='plus' else '-'))
        graphLeft_rel.SetFillColor(colorL)
        graphRight_rel.SetTitle('W^{{{ch}}}: right'.format(ch='+' if charge=='plus' else '-'))
        graphRight_rel.SetFillColor(colorR)

        graphLeft_rel.GetXaxis().SetRangeUser(0., 3.)
        graphLeft_rel.GetYaxis().SetRangeUser(0.97, 1.033)
        graphRight_rel.GetXaxis().SetRangeUser(0., 3.)
        graphRight_rel.GetYaxis().SetRangeUser(0.97, 1.033)

        graphRight_rel.GetXaxis().SetTitle('|Y_{W}|')

        graphLeft_rel .GetXaxis().SetTitleSize(0.06)
        graphLeft_rel .GetXaxis().SetLabelSize(0.06)
        graphLeft_rel .GetYaxis().SetTitleSize(0.06)
        graphLeft_rel .GetYaxis().SetLabelSize(0.06)
        graphRight_rel.GetXaxis().SetTitleSize(0.06)
        graphRight_rel.GetXaxis().SetLabelSize(0.06)
        graphRight_rel.GetYaxis().SetTitleSize(0.06)
        graphRight_rel.GetYaxis().SetLabelSize(0.06)

        graphLeft_rel.Draw('Pa2')
        line.Draw("Lsame");
        padUp.RedrawAxis("sameaxis");

        padDown = c2.cd(2)
        padDown.SetTickx(1)
        padDown.SetTicky(1)
        padDown.SetGridy(1)
        padDown.SetBottomMargin(0.15)
        graphRight_rel.Draw('pa2')
        line.Draw("Lsame");
        padDown.RedrawAxis("sameaxis");

        for ext in ['png', 'pdf']:
            c2.SaveAs('{od}/rapidityDistribution_{date}_{suff}_{ch}_relative.{ext}'.format(od=options.outdir, date=date, suff=options.suffix, ch=charge, ext=ext))

        ### sys.exit()

        ### 

        ### graph     = ROOT.TGraphAsymmErrors(len(arr_val), arr_rap, arr_val, arr_rlo, arr_rhi, arr_elo, arr_ehi)
        ### graph.SetTitle('W {ch}: Y_{{W}}'.format(ch=charge))
        ### graph.SetFillColor(ROOT.kBlue+1)
        ### graph.SetFillStyle(3001)
        ### #graph.GetXaxis().SetRangeUser(ybins[0],ybins[-1])
        ### graph.GetXaxis().SetRangeUser(-4.,4.)
        ### graph.GetXaxis().SetTitle('Y_{W}')
        ### graph.GetYaxis().SetTitle('N_{events}/N_{total}')
        ### c2 = ROOT.TCanvas()
        ### graph.Draw('a2')
        ### for ext in ['png', 'pdf']:
        ###     c2.SaveAs('{od}/rapidityDistribution_{date}_{suff}_{ch}.{ext}'.format(od=options.outdir, date=date, suff=options.suffix, ch=charge, ext=ext))

        ### graph_rel = ROOT.TGraphAsymmErrors(len(arr_val), arr_rap, arr_relv, arr_rlo, arr_rhi, arr_rello, arr_relhi)
        ### graph_rel.SetTitle('W {ch}: Y_{{W}}'.format(ch=charge))
        ### graph_rel.SetMarkerStyle(20)
        ### graph_rel.SetMarkerColor(ROOT.kBlack)
        ### graph_rel.SetMarkerSize(0.8)
        ### graph_rel.SetFillColor(ROOT.kBlue+1)
        ### graph_rel.SetFillStyle(3003)
        ### graph_rel.GetXaxis().SetRangeUser(-4.,4.)
        ### graph_rel.GetYaxis().SetRangeUser(0.97,1.03)
        ### graph_rel.GetXaxis().SetTitle('Y_{W}')
        ### graph_rel.GetYaxis().SetTitle('rate par. fit value')
        ### graph_rel.Draw('Pa5')
        ### for ext in ['png', 'pdf']:
        ###     c2.SaveAs('{od}/rapidityDistribution_{date}_{suff}_{ch}_relative.{ext}'.format(od=options.outdir, date=date, suff=options.suffix, ch=charge, ext=ext))

        ### ## some "unfolding" stuff first
        ### if options.scaleFile:
        ###     arr_scales_left  = array.array('f', getScales(ybins, charge, 'left' , options.scaleFile))
        ###     arr_scales_right = array.array('f', getScales(ybins, charge, 'right', options.scaleFile))
        ### else:
        ###     arr_scales_left = [1. for y in ybins[1:]]
        ###     arr_scales_right = [1. for y in ybins[1:]]

        ### arr_val_scaled_left  = []
        ### arr_val_scaled_right = []

        ### for i in range(len(arr_scales_left)):
        ###     arr_val_scaled_left .append(arr_scales_left[i] *arr_val[i])
        ###     arr_val_scaled_right.append(arr_scales_right[i]*arr_val[i])

        ### arr_val_scaled_left  = array.array('f', arr_val_scaled_left )
        ### arr_val_scaled_right = array.array('f', arr_val_scaled_right)


        ### c3 = ROOT.TCanvas('foo','',800,800)
        ### half = len(arr_val)/2
        ### graph_right = ROOT.TGraphAsymmErrors(half, arr_rap[half:], arr_val_scaled_right[:half][::-1], arr_rlo[half:], arr_rhi[half:], arr_elo[:half][::-1], arr_ehi[:half][::-1])
        ### graph_left  = ROOT.TGraphAsymmErrors(half, arr_rap[half:], arr_val_scaled_left[half:], arr_rlo[half:], arr_rhi[half:], arr_elo[half:], arr_ehi[half:])
        ### graph_left .SetFillColor(ROOT.kAzure+8 )
        ### graph_right.SetFillColor(ROOT.kOrange+7)
        ### graph_left .GetXaxis().SetRangeUser(0.,3.0)
        ### graph_right.GetXaxis().SetRangeUser(0.,3.0)

        ### leg = ROOT.TLegend(0.20, 0.20, 0.5, 0.35)
        ### leg.SetFillStyle(0)
        ### leg.SetBorderSize(0)

        ### ymax = 6.0

        ### mg = ROOT.TMultiGraph()
        ### mg.Add(graph_right)
        ### mg.Add(graph_left )
        ### leg.AddEntry(graph_left , 'W^{{{ch}}} left' .format(ch='+' if charge == 'plus' else '-'), 'f')
        ### leg.AddEntry(graph_right, 'W^{{{ch}}} right'.format(ch='+' if charge == 'plus' else '-'), 'f')
        ### mg.Draw('Pa5')
        ### mg.GetXaxis().SetRangeUser(0.0,ymax)
        ### mg.GetXaxis().SetTitle('|Y_{W}|')
        ### mg.GetXaxis().SetTitleSize(0.06)
        ### mg.GetXaxis().SetLabelSize(0.04)
        ### mg.GetYaxis().SetTitleSize(0.06)
        ### mg.GetYaxis().SetLabelSize(0.04)
        ### mg.GetYaxis().SetTitle('N_{events}/N_{total}')
        ### mg.GetYaxis().SetTitleOffset(1.2)
        ### c3.GetPad(0).SetTopMargin(0.05)
        ### c3.GetPad(0).SetBottomMargin(0.15)
        ### c3.GetPad(0).SetLeftMargin(0.16)

        ### leg.Draw('same')

        ### for ext in ['png', 'pdf']:
        ###     c3.SaveAs('{od}/rapidityDistribution_{date}_{suff}_{ch}_absRapLeftRight.{ext}'.format(od=options.outdir, date=date, suff=options.suffix, ch=charge, ext=ext))

    
