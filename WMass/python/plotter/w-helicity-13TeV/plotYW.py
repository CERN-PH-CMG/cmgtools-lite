#!/bin/env python
# USAGE: python plotYW.py --type toys --infile toys_wplus.root -y cards_el/binningYW.txt -C plus -o plots --xsecfile Wel_plus_shapes_xsec.root [--normxsec]

import ROOT, datetime, array, os, math, re
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")

import utilities
utilities = utilities.util()


class valueClass:
    def __init__(self, name):
        self.name = name

        self.pol = 'left' if 'left' in self.name else 'right' if 'right' in self.name else 'long'
        self.isleft  = self.pol == 'left'
        self.isright = self.pol == 'right'
        self.islong  = self.pol == 'long'

        self.charge = 'plus' if 'plus' in name else 'minus'
        self.ch     = '+' if 'plus' in name else '-'

        self.color  = ROOT.kAzure+8 if self.isleft else ROOT.kOrange+7 if self.isright else ROOT.kGray+1
        self.colorf = ROOT.kAzure+3 if self.isleft else ROOT.kOrange+9 if self.isright else ROOT.kGray+3

        ## here all the arrays that will contain the values and errors etc.
        self.val       = array.array('f', []); self.ehi       = array.array('f', []); self.elo       = array.array('f', []);
        self.val_fit   = array.array('f', []); self.ehi_fit   = array.array('f', []); self.elo_fit   = array.array('f', []);
        self.relv      = array.array('f', []); self.relhi     = array.array('f', []); self.rello     = array.array('f', []);
        self.relv_fit  = array.array('f', []); self.relhi_fit = array.array('f', []); self.rello_fit = array.array('f', []);
        self.rap       = array.array('f', []); self.rlo       = array.array('f', []); self.rhi       = array.array('f', []);

    def makeGraphs(self):
        self.graph = ROOT.TGraphAsymmErrors(len(self.val), self.rap, self.val, self.rlo, self.rhi, self.elo, self.ehi)
        self.graph.SetName('graph'+self.pol)
        self.graph_rel= ROOT.TGraphAsymmErrors(len(self.relv), self.rap, self.relv, self.rlo, self.rhi, self.rello, self.relhi)
        self.graph_rel.SetName('graph'+self.pol+'_rel')

        self.graph_fit = ROOT.TGraphAsymmErrors(len(self.val_fit), self.rap, self.val_fit, self.rlo, self.rhi, self.elo_fit, self.ehi_fit)
        self.graph_fit.SetName('graph'+self.pol+'_fit')
        self.graph_fit_rel = ROOT.TGraphAsymmErrors(len(self.relv_fit), self.rap, self.relv_fit, self.rlo, self.rhi, self.rello_fit, self.relhi_fit)
        self.graph_fit_rel.SetName('graph'+self.pol+'_fit_rel')
    
        self.graphStyle()
        self.makeMultiGraphRel()

    def makeMultiGraphRel(self):
        self.mg = ROOT.TMultiGraph()
        self.mg.SetTitle('W^{{{ch}}}: {p}'.format(ch=self.ch,p=self.pol))
        self.mg.Add(self.graph_rel,'P2')
        self.mg.Add(self.graph_fit_rel)

    def graphStyle(self):
        if not self.graph:
            print 'ERROR: this struct has no graphs!!!'
            sys.exit()
        self.graph.SetLineColor(self.color)
        self.graph.SetFillColor(self.color)
        self.graph.SetFillStyle(3002)
    
        self.graph_fit.SetLineWidth(2)
        self.graph_fit.SetLineColor(self.colorf)
    
        self.graph_rel.SetLineWidth(5)
        self.graph_rel.SetLineColor(self.color)
        self.graph_rel.SetFillColor(self.color)
        self.graph_rel.SetFillStyle(3002)
        self.graph_fit_rel.SetLineWidth(2)
        self.graph_fit_rel.SetLineColor(self.colorf)
        

NPDFs = 60

if __name__ == "__main__":

    from optparse import OptionParser
    parser = OptionParser(usage='%prog ybinfile workspace.root toys.root [options] ')
    parser.add_option('-i', '--infile'      , dest='infile'   , default=''            , type='string', help='workspace converted from datacard')
    parser.add_option('-y', '--ybinfile'    , dest='ybinfile' , default=''            , type='string', help='file with the yw binning')

    parser.add_option('-t', '--type'        , dest='type'     , default='toys'        , type='string', help='run the plot from which postfit? toys/scans/hessian')
    parser.add_option(      '--toyfile'     , dest='toyfile'  , default=''            , type='string', help='file that has the toys')
    parser.add_option(      '--scandir'     , dest='scandir'  , default=''            , type='string', help='directory with all the scans')
    parser.add_option(      '--hessfile'    , dest='hessfile' , default=''            , type='string', help='file that contains the hessian errors in a dictionary')
    parser.add_option(      '--xsecfile'    , dest='xsecfile' , default=None          , type='string', help='file that contains the expected x sections with variations')
    parser.add_option('-C', '--charge'      , dest='charge'   , default='plus,minus'  , type='string', help='process given charge. default is both')
    parser.add_option('-o', '--outdir'      , dest='outdir'   , default='.'           , type='string', help='outdput directory to save the plots')
    parser.add_option(      '--suffix'      , dest='suffix'   , default=''            , type='string', help='suffix for the correlation matrix')
    parser.add_option('-n', '--normxsec'    , dest='normxsec' , default=False         , action='store_true',   help='if given, plot the differential xsecs normalized to the total xsec')
    (options, args) = parser.parse_args()


    if not os.path.isdir(options.outdir):
        os.system('mkdir {od}'.format(od=options.outdir))
        if os.path.exists("/afs/cern.ch"): os.system("cp /afs/cern.ch/user/g/gpetrucc/php/index.php {od}".format(od=options.outdir))

    if options.ybinfile:
        ybinfile = options.ybinfile
    else:
        ybinfile = os.path.dirname(os.path.abspath(options.infile))+'/binningYW.txt'


    ## get the central values and uncertainties depending on the type given:

    ## if --type=toys   , we expect a toyfile
    ## if --type=scans  , we expect a scan directory
    ## if --type=hessian, we expect a hessian file

    if   options.type == 'toys':
        valuesAndErrors = utilities.getFromToys(options.infile)
    elif options.type == 'scans':
        valuesAndErrors = utilities.getFromScans(options.infile)
    elif options.type == 'hessian':
        tmp = eval(open(options.infile,'r').read())
        valuesAndErrors = {}
        for i,j in tmp.items():
            valuesAndErrors[i] = (j[0], j[0]-j[1], j[0]+j[1])
    else:
        print 'ERROR: none of your types is supported. specify either "toys", "scans", or "hessian"'
        sys.exit()

    channel = 'mu' if any(re.match(param,'.*_mu_Ybin_.*') for param in valuesAndErrors.keys()) else 'el'
    print "From the list of parameters it seems that you are plotting results for channel ",channel

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
        xsec_nominal = utilities.getXSecFromShapes(ybins,charge,options.xsecfile,channel, 0)

        shape_syst = {}
        value_syst = {}
        for pol in ['left','right', 'long']:
            histos = []
            values = []
            for ip in xrange(1,NPDFs+1):
                # print "Loading polarization %s, histograms for pdf %d" % (pol,ip)
                ## this gets the pdf variations after correctly rebinning the YW
                pdf = utilities.getRebinned(ybins,charge,file_pdfs,ip)
                xsec_pdf = utilities.getXSecFromShapes(ybins,charge,options.xsecfile,channel,ip)
                histos.append(pdf[pol])
                values.append(xsec_pdf[pol])
            shape_syst[pol] = histos
            value_syst[pol] = values

        systematics = {}
        xsec_systematics = {}
        for pol in ['left','right', 'long']:
            #print "===> Running pol = ",pol
            systs=[]
            xsec_systs=[]
            for iy,y in enumerate(ybinwidths['{ch}_{pol}'.format(ch=charge,pol=pol if not pol=='long' else 'right')]):
                #print "\tBin iy=%d,y=%f = " % (iy,y)
                nom = nominal[pol][iy]
                xsec_nom = xsec_nominal[pol][iy]
                totUp=0; xsec_totUp=0
                for ip,pdf in enumerate(shape_syst[pol]):
                    xsec_pdf = value_syst[pol][ip]
                    # debug
                    relsyst = abs(nom-pdf[iy])/nom
                    xsec_relsyst = abs(xsec_nom-xsec_pdf[iy])/xsec_nom if xsec_nom else 0.0
                    if relsyst>0.20:
                        print "SOMETHING WENT WRONG WITH THIS PDF: %d HAS RELATIVE SYST = %f. SKIPPING !" % (ip,relsyst)
                    else:
                        totUp += math.pow(relsyst*nom,2)
                    xsec_totUp += math.pow(xsec_relsyst*xsec_nom,2)
                totUp = math.sqrt(totUp)
                xsec_totUp = math.sqrt(xsec_totUp)
                # print "Rel systematic for Y bin %d = +/-%.3f" % (iy,totUp/nom)
                # print "\tRel systematic on xsec for Y bin %d = +/-%.3f" % (iy,xsec_totUp/xsec_nom if xsec_nom else 0.)
                systs.append(totUp)
                xsec_systs.append(xsec_totUp)
            systematics[pol]=systs
            xsec_systematics[pol]=xsec_systs

        allValues = {}
        for pol in ['left','right', 'long']:
            cp = '{ch}_{pol}'.format(ch=charge,pol=pol)
            MAXYFORNORM = ybins[cp][-2] # exclude the outermost bin which has huge error due to acceptance
            normsigma = sum([xsec_nominal[pol][iy] for iy,y in enumerate(ybins[cp][:-1]) if abs(y)<MAXYFORNORM])
            print "total xsec up to |Y|<{maxy} = {sigma:.3f} (pb)".format(maxy=MAXYFORNORM,sigma=normsigma)

            tmp_val = valueClass('values_'+charge+'_'+pol)

            for iy,y in enumerate(ybinwidths['{ch}_{pol}'.format(ch=charge,pol=pol)]):
                parname = 'W{charge}_{pol}_W{charge}_{pol}_{ch}_Ybin_{iy}'.format(charge=charge,pol=pol,ch=channel,iy=iy)

                tmp_val.val.append(xsec_nominal[pol][iy]/ybinwidths[cp][iy])
                tmp_val.ehi.append(xsec_systematics[pol][iy]/ybinwidths[cp][iy])
                tmp_val.elo.append(xsec_systematics[pol][iy]/ybinwidths[cp][iy]) # symmetric for the expected
                if options.normxsec:
                    tmp_val.val[-1] = tmp_val.val[-1]/normsigma
                    tmp_val.ehi[-1] = tmp_val.ehi[-1]/normsigma
                    tmp_val.elo[-1] = tmp_val.elo[-1]/normsigma

                tmp_val.relv. append(1.);
                tmp_val.rello.append(systematics[pol][iy]/nominal[pol][iy])
                tmp_val.relhi.append(systematics[pol][iy]/nominal[pol][iy]) # symmetric for the expected
                
                if options.normxsec:
                    xsec_fit = utilities.getNormalizedXsecFromToys(ybins,charge,pol,channel,iy,options.infile,MAXYFORNORM)
                else:
                    xsec_parname = parname+'_pmaskedexp'
                    xsec_fit = valuesAndErrors[xsec_parname]
                
                tmp_val.val_fit.append(xsec_fit[0]/ybinwidths[cp][iy])
                tmp_val.elo_fit.append(abs(xsec_fit[0]-xsec_fit[1])/ybinwidths[cp][iy])
                tmp_val.ehi_fit.append(abs(xsec_fit[0]-xsec_fit[2])/ybinwidths[cp][iy])

                units = '' if options.normxsec else '(pb)'
                print "par = {parname}, expected sigma = {sigma:.3f} {units}   fitted = {val:.3f} + {ehi:.3f} - {elo:.3f} {units}".format(parname=parname,
                                                                                                                                          sigma=tmp_val.val[-1],units=units,
                                                                                                                                          val=tmp_val.val_fit[-1],ehi=tmp_val.ehi_fit[-1],elo=tmp_val.elo_fit[-1])

                if options.normxsec:
                    rfit = tuple([xs/xsec_nominal[pol][iy]*normsigma for xs in xsec_fit]) # rescale the fit xsec by the expected xsec in that bin
                else:
                    rfit = valuesAndErrors[parname] # r values: contain all the common norm uncertainties (lumi, eff...)

                tmp_val.relv_fit .append(rfit[0])
                tmp_val.rello_fit.append(abs(rfit[0]-rfit[1]))
                tmp_val.relhi_fit.append(abs(rfit[0]-rfit[2]))

                tmp_val.rap.append((ybins[cp][iy]+ybins[cp][iy+1])/2.)
                tmp_val.rlo.append(abs(ybins[cp][iy]-tmp_val.rap[-1]))
                tmp_val.rhi.append(abs(ybins[cp][iy]-tmp_val.rap[-1]))

                tmp_val.makeGraphs()

                allValues[pol] = tmp_val


        c2 = ROOT.TCanvas('foo','', 800, 800)
        c2.GetPad(0).SetTopMargin(0.05)
        c2.GetPad(0).SetBottomMargin(0.15)
        c2.GetPad(0).SetLeftMargin(0.16)

        ## the four graphs exist now. now starting to draw them
        ## ===========================================================
        leg = ROOT.TLegend(0.60, 0.60, 0.85, 0.90)
        leg.SetFillStyle(0)
        leg.SetBorderSize(0)
        leg.AddEntry(allValues['left'] .graph     , 'W^{{{ch}}} left (PDF systs)' .format(ch='+' if charge == 'plus' else '-') , 'f')
        leg.AddEntry(allValues['left'] .graph_fit , 'W^{{{ch}}} left (fit)' .format(ch='+' if charge == 'plus' else '-')       , 'pl')
        leg.AddEntry(allValues['right'].graph     , 'W^{{{ch}}} right (PDF systs)'.format(ch='+' if charge == 'plus' else '-') , 'f')
        leg.AddEntry(allValues['right'].graph_fit , 'W^{{{ch}}} right (fit)'.format(ch='+' if charge == 'plus' else '-')       , 'pl')
        leg.AddEntry(allValues['long'] .graph     , 'W^{{{ch}}} long (PDF systs)'.format(ch='+' if charge == 'plus' else '-') , 'f')
        leg.AddEntry(allValues['long'] .graph_fit , 'W^{{{ch}}} long (fit)'.format(ch='+' if charge == 'plus' else '-')       , 'pl')

        allValues['left'].graph.SetTitle('W {ch}: Y_{{W}}'.format(ch=charge))
            
        mg = ROOT.TMultiGraph()
        mg.Add(allValues['left'] .graph,'P2')
        mg.Add(allValues['right'].graph,'P2')
        mg.Add(allValues['long'] .graph,'P2')
        mg.Add(allValues['left'] .graph_fit)
        mg.Add(allValues['right'].graph_fit)
        mg.Add(allValues['long'] .graph_fit)
 
        mg.Draw('Pa')
        mg.GetXaxis().SetRangeUser(0.,6.)
        mg.GetXaxis().SetTitle('|Y_{W}|')
        if options.normxsec: 
            mg.GetYaxis().SetTitle('d#sigma/dy/#sigma_{tot}')
        else: 
            mg.GetYaxis().SetTitle('d#sigma/dy (pb)')
        mg.GetXaxis().SetTitleSize(0.06)
        mg.GetXaxis().SetLabelSize(0.04)
        mg.GetYaxis().SetTitleSize(0.06)
        mg.GetYaxis().SetLabelSize(0.04)
        mg.GetYaxis().SetTitleOffset(1.2)
 
        leg.Draw('same')

        date = datetime.date.today().isoformat()
        normstr = 'norm' if options.normxsec else ''
        for ext in ['png', 'pdf']:
            c2.SaveAs('{od}/genAbsY{norm}_pdfs_{date}_{ch}{suffix}_{t}.{ext}'.format(od=options.outdir, norm=normstr, date=date, ch=charge, suffix=options.suffix, ext=ext,t=options.type))

        ## now make the relative error plot:
        ## ======================================

        c2.Clear()
        c2.Divide(1,3)

        line = ROOT.TF1("horiz_line","1",0.0,3.0);
        line.SetLineColor(ROOT.kBlack);
        line.SetLineWidth(2);

        padUp = c2.cd(1)
        padUp.SetTickx(1)
        padUp.SetTicky(1)
        padUp.SetGridy(1)
        padUp.SetLeftMargin(0.15)
        padUp.SetBottomMargin(0.10)

        yaxtitle = '#frac{d#sigma/dy/#sigma_{tot}}{d#sigma^{exp}/dy/#sigma^{exp}_{tot}}' if options.normxsec else '#frac{dN/dy}{dN^{exp}/dy}'

        allValues['left'].mg.Draw('Pa')
        allValues['left'].mg.GetXaxis().SetRangeUser(0., 3.)
        allValues['left'].mg.GetYaxis().SetRangeUser(0.85, 1.15)
        allValues['left'].mg.GetXaxis().SetTitleSize(0.06)
        allValues['left'].mg.GetXaxis().SetLabelSize(0.06)
        allValues['left'].mg.GetYaxis().SetTitleSize(0.06)
        allValues['left'].mg.GetYaxis().SetLabelSize(0.06)
        allValues['left'].mg.GetYaxis().SetTitle(yaxtitle)

        leg.Draw('same')
        line.Draw("Lsame");
        padUp.RedrawAxis("sameaxis");

        padMiddle = c2.cd(2)
        padMiddle.SetTickx(1)
        padMiddle.SetTicky(1)
        padMiddle.SetGridy(1)
        padMiddle.SetLeftMargin(0.15)
        padMiddle.SetBottomMargin(0.15)
        allValues['right'].mg.Draw('pa')
        allValues['right'].mg.GetXaxis().SetRangeUser(0., 3.)
        allValues['right'].mg.GetYaxis().SetRangeUser(0.85, 1.15)
        allValues['right'].mg.GetXaxis().SetTitle('|Y_{W}|')
        allValues['right'].mg.GetXaxis().SetTitleSize(0.06)
        allValues['right'].mg.GetXaxis().SetLabelSize(0.06)
        allValues['right'].mg.GetYaxis().SetTitleSize(0.06)
        allValues['right'].mg.GetYaxis().SetLabelSize(0.06)
        allValues['right'].mg.GetYaxis().SetTitle(yaxtitle)
        line.Draw("Lsame");
        padMiddle.RedrawAxis("sameaxis");

        padDown = c2.cd(3)
        padDown.SetTickx(1)
        padDown.SetTicky(1)
        padDown.SetGridy(1)
        padDown.SetLeftMargin(0.15)
        padDown.SetBottomMargin(0.15)
        allValues['long'].mg.Draw('pa')
        allValues['long'].mg.GetXaxis().SetRangeUser(0., 3.)
        allValues['long'].mg.GetYaxis().SetRangeUser(0.85, 1.15)
        allValues['long'].mg.GetXaxis().SetTitle('|Y_{W}|')
        allValues['long'].mg.GetXaxis().SetTitleSize(0.06)
        allValues['long'].mg.GetXaxis().SetLabelSize(0.06)
        allValues['long'].mg.GetYaxis().SetTitleSize(0.06)
        allValues['long'].mg.GetYaxis().SetLabelSize(0.06)
        allValues['long'].mg.GetYaxis().SetTitle(yaxtitle)
        line.Draw("Lsame");
        padDown.RedrawAxis("sameaxis");

        for ext in ['png', 'pdf']:
            c2.SaveAs('{od}/genAbsY{norm}_pdfs_{date}_{ch}{suffix}_relative_{t}.{ext}'.format(od=options.outdir, norm=normstr, date=date, ch=charge, suffix=options.suffix, ext=ext,t=options.type))
