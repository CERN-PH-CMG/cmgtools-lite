import ROOT, datetime, array, os, math
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True

from mergeCardComponentsAbsY import mirrorShape

def getRebinned(ybins, charge, infile):
    histo_file = ROOT.TFile(infile, 'READ')

    histos = {}
    for pol in ['left','right','long']:
        histo = histo_file.Get('w{ch}_wy_W{ch}_{pol}'.format(ch=charge, pol=pol))
        conts = []
        for iv, val in enumerate(ybins[:-1]):
            err = ROOT.Double()
            istart = histo.FindBin(val)
            iend   = histo.FindBin(ybins[iv+1])
            val = histo.IntegralAndError(istart, iend-1, err) ## do not include next bin
            if 'pdfs' not in infile: print "pol = %s; ist,ie,val = %d,%d,%f" % (pol,istart,iend,val)
            conts.append(2*val) ## input files are not abs(Y)
        histos[pol] = conts
    return histos

NPDFs = 60

if __name__ == "__main__":

    from optparse import OptionParser
    parser = OptionParser(usage='%prog inputdir ybinfile [options] ')
    parser.add_option('-C','--charge', dest='charge', default='plus,minus', type='string', help='process given charge. default is both')
    parser.add_option('-o','--outdir', dest='outdir', default='.', type='string', help='outdput directory to save the matrix')
    (options, args) = parser.parse_args()

    inputdir = args[0]
    ybinfile = args[1]

    print "Taking histos from dir: %s" % inputdir

    ybinfile = open(ybinfile, 'r')
    ybinline = ybinfile.readlines()[0]
    ybins = list(float(i) for i in ybinline.split())
    ybinfile.close()

    ## calculate the bin widths for the rapidity bins
    ybinwidths = list(abs(i - ybins[ybins.index(i)+1]) for i in ybins[:-1])

    charges = options.charge.split(',')
    for charge in charges:

        file_nom = '{dir}/wgen_nosel_{charge}_nominal.root'.format(dir=inputdir,charge=charge)
        nominal = getRebinned(ybins,charge,file_nom)
        
        print "Now getting histograms from %s (will take some time)..." % inputdir
        shape_syst = {}
        for pol in ['left','right','long']:
            histos = []
            for ip in xrange(NPDFs):
                print "Loading polarization %s, histograms for pdf %d" % (pol,ip)
                filepdf = '{dir}/wgen_nosel_{charge}_pdfs_pdf{ipdf}.root'.format(dir=inputdir,charge=charge,ipdf=ip)
                pdf = getRebinned(ybins,charge,'{dir}/wgen_nosel_{charge}_pdfs_pdf{ipdf}.root'.format(dir=inputdir,charge=charge,ipdf=ip))
                hnom = nominal[pol]; hpdf = pdf[pol]
                histos.append(hpdf)
            shape_syst[pol] = histos
        
        systematics = {}
        for pol in ['left','right','long']:
            # print "===> Running pol = ",pol
            systs=[]
            for iy,y in enumerate(ybinwidths):
                # print "\tBin iy=%d,y=%f = " % (iy,y)
                nom = nominal[pol][iy]
                totUp=0
                for pdf in shape_syst[pol]:
                    totUp += pow(nom-pdf[iy],2)
                    # print "\t\tUp = %f; Dn = %f" % (totUp,totDn)
                totUp=math.sqrt(totUp)
                print "Rel systematic for Y bin %d = +/-%.3f" % (iy,totUp/nom)
                systs.append(totUp)
            systematics[pol]=systs

        arr_val   = array.array('f', [])
        arr_ehi   = array.array('f', [])
        arr_elo   = array.array('f', [])
        arr_relv  = array.array('f', [])
        arr_relhi = array.array('f', [])
        arr_rello = array.array('f', [])
        arr_rap   = array.array('f', [])
        arr_rlo   = array.array('f', [])
        arr_rhi   = array.array('f', [])

        for pol in ['left','right']:
            totalrate = 0.
            for iy,y in enumerate(ybinwidths):
                totalrate += nominal[pol][iy]

        for pol in ['left','right']:

            arr_val   = array.array('f', []); arr_ehi   = array.array('f', []); arr_elo   = array.array('f', []);
            arr_relv  = array.array('f', []); arr_relhi = array.array('f', []); arr_rello = array.array('f', []);
            arr_rap   = array.array('f', []); arr_rlo   = array.array('f', []); arr_rhi   = array.array('f', []);

            for iy,y in enumerate(ybinwidths):
                arr_val.append(nominal[pol][iy]/totalrate/ybinwidths[iy])
                arr_ehi.append(systematics[pol][iy]/totalrate/ybinwidths[iy])
                arr_elo.append(systematics[pol][iy]/totalrate/ybinwidths[iy]) # symmetric for the expected

                arr_relv. append(1.);
                arr_rello.append(systematics[pol][iy]/nominal[pol][iy])
                arr_relhi.append(systematics[pol][iy]/nominal[pol][iy]) # symmetric for the expected

                arr_rap.append((ybins[iy]+ybins[iy+1])/2.)
                arr_rlo.append(abs(ybins[iy]-arr_rap[-1]))
                arr_rhi.append(abs(ybins[iy]-arr_rap[-1]))

            if 'left' in pol:
                print 'left {ch}: {i}'.format(ch=charge, i=sum(arr_val))
                graphLeft      = ROOT.TGraphAsymmErrors(len(arr_val), arr_rap, arr_val, arr_rlo, arr_rhi, arr_elo, arr_ehi)
                graphLeft_rel  = ROOT.TGraphAsymmErrors(len(arr_relv), arr_rap, arr_relv, arr_rlo, arr_rhi, arr_rello, arr_relhi)
                graphLeft     .SetName('graphLeft')
                graphLeft_rel .SetName('graphLeft_rel')
            else:
                print 'right {ch}: {i}'.format(ch=charge, i=sum(arr_val))
                graphRight      = ROOT.TGraphAsymmErrors(len(arr_val), arr_rap, arr_val, arr_rlo, arr_rhi, arr_elo, arr_ehi)
                graphRight_rel  = ROOT.TGraphAsymmErrors(len(arr_relv), arr_rap, arr_relv, arr_rlo, arr_rhi, arr_rello, arr_relhi)
                graphRight     .SetName('graphRight')
                graphRight_rel .SetName('graphRight_rel')

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

        date = datetime.date.today().isoformat()
        for ext in ['png', 'pdf']:
            c2.SaveAs('{od}/genAbsY_pdfs_{date}_{ch}.{ext}'.format(od=options.outdir, date=date, ch=charge, ext=ext))

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
            c2.SaveAs('{od}/genAbsY_pdfs_{date}_{ch}_relative.{ext}'.format(od=options.outdir, date=date, ch=charge, ext=ext))
