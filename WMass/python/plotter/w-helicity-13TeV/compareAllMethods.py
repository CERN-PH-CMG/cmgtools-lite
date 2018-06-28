import ROOT, os, datetime, re, operator, math, copy
import utilities
import array


utilities = utilities.util()


def fitToys(hist, color=ROOT.kGreen+1):
    hist.Fit('gaus')
    hist.SetLineColor(color)
    f = hist.GetFunction('gaus')
    f.SetLineColor(color)
    cen = f.GetParameter(1)
    sig = f.GetParameter(2)

    return (hist, cen, sig)

def getCleanedGraph(infile, par, norm, n_iter, treename='limit'):
    f = ROOT.TFile(infile,'read')
    tree = f.Get(treename)
    vals = []
    normval = norm if norm else 1.
    for ev in tree:
        ## ##if 2.*ev.deltaNLL > 15: continue
        ## if norm == 1. and abs(getattr(ev, par) - norm) > 0.07: continue
        ## if abs(2.*ev.deltaNLL) < 0.0001: continue
        if treename=='limit':
            vals.append( [getattr(ev, par)/normval, 2.*ev.deltaNLL] )
        else:
            vals.append( [getattr(ev, par)/normval, 2.*ev.nllval] )
    vals = sorted(vals)

    n_iter = int(n_iter)
    
    graph = ROOT.TGraph(len(vals), array.array('d', [x[0] for x in vals]), array.array('d', [y[1] for y in vals]) )

    utilities.graphStyle(graph, rangeY=[-1., 4.] )

    return graph


def noOffsetGraph(graph, func):
    newgraph = graph.Clone(graph.GetName()+'_noOffset')
    utilities.graphStyle(newgraph, color=ROOT.kMagenta+1)
    minpoint = -1.*func.GetParameter(1) / (2.*func.GetParameter(2))
    fmin = func.Eval(minpoint)

    print 'found minimum at', fmin
    
    for ip in range(1,newgraph.GetN()+1):
        x, y = ROOT.Double(), ROOT.Double()
        newgraph.GetPoint(ip, x, y)
        newgraph.SetPoint(ip, x, y-fmin)

    return newgraph
        
_basedir = '/afs/cern.ch/work/m/mdunser/public/cmssw/w-helicity-13TeV/CMSSW_8_0_25/src/CMGTools/WMass/python/plotter/cards/simple_dpsww/'


pars = [
    'rares_norm',
    'WZ_norm',
    'mumu_fakes',
    'lumi_13TeV_2016',
    'WG_norm',
    'ZZ_norm',
    'mumu_fakes1',
    'mumu_fakes2',
    'WG_shape1',
    'WG_shape2',
    'ZZ_shape1',
    'ZZ_shape2',
    'signal_shape',
    'WZ_shapeUnc',
    'rares_shape1',
    'rares_shape2'
]


if __name__ == "__main__":

    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetPaintTextFormat('.3f')

    date = datetime.date.today().isoformat()

    from optparse import OptionParser
    parser = OptionParser(usage='%prog [options] ')
    parser.add_option('-m', '--mode'           , dest='mode'     , default=''   , type='string', help='mode: combine or tensorflow')
    parser.add_option('-t', '--type'           , dest='type'     , default=''   , type='string', help='type: hessian, scans, or toys')
    parser.add_option(      '--pars'           , dest='pars'     , default=''   , type='string', help='comma separated list of regexp parameters to run. default is all parameters!')
    parser.add_option(      '--webdir'         , dest='webdir'     , default=''   , type='string', help='web directory to save the likelihood scans')
    (options, args) = parser.parse_args()

    ## all the necessary objects
    file_tf_hessians = ROOT.TFile(_basedir+'/hessian/hessian_tensorflow.root' , 'read')
    file_tf_toys     = ROOT.TFile(_basedir+'/toys/toys_tensorflow_10k.root'   , 'read')
    file_cb_hessians = ROOT.TFile(_basedir+'/hessian/multidimfit_combine.root', 'read')
    file_cb_toys     = ROOT.TFile(_basedir+'/toys/toys_combine_25k.root'      , 'read')
    dir_cb_scans    = _basedir+'/scans/'
    dir_tf_scans    = _basedir+'/scans/'
    
    obj_tf_hessians  = file_tf_hessians .Get('fitresults')
    obj_tf_toys      = file_tf_toys     .Get('fitresults')
    obj_cb_hessians  = file_cb_hessians .Get('fit_mdf')
    obj_cb_toys      = file_cb_toys     .Get('limit')
    ## =============================


    parameters = []
    all_parameters = []
    pois_regexps = list(options.pars.split(','))

    for i in range(len(pars)):
        tmp_name = pars[i] #.GetName()
        if '_In' in tmp_name: ## those are the input parameters
            continue
        if tmp_name in ['CMS_th1x', 'r']: ## don't want those
            continue
        all_parameters.append(tmp_name)
        for poi in pois_regexps:
            if re.match(poi, tmp_name): 
                parameters.append(pars[i])#.GetName())


    if options.webdir:
        ROOT.gROOT.SetBatch()

    for par in pars:

        vals_errs = []

        print 'getting the hessian errors'
        for ev in obj_tf_hessians:
            unc_tf_hessian   = getattr(obj_tf_hessians, par)
            unc_tf_hessian_e = getattr(obj_tf_hessians, par+'_err')
        unc_tf_hessian_g = ROOT.TGraphAsymmErrors(1, array.array('d', [unc_tf_hessian]), 
                                                     array.array('d', [0]),
                                                     array.array('d', [abs(unc_tf_hessian_e)]),  
                                                     array.array('d', [abs(unc_tf_hessian_e)]),  
                                                     array.array('d',[0]), array.array('d',[0]))
        utilities.graphStyle(unc_tf_hessian_g,style=24,color=ROOT.kRed-2)

        print 'from combine'
        unc_cb_hessian     = obj_cb_hessians.floatParsFinal().find(par).getVal()
        unc_cb_hessian_ehi = obj_cb_hessians.floatParsFinal().find(par).getAsymErrorHi()
        unc_cb_hessian_elo = obj_cb_hessians.floatParsFinal().find(par).getAsymErrorLo()
        unc_cb_hessian_g = ROOT.TGraphAsymmErrors(1, array.array('d', [unc_cb_hessian]), 
                                                     array.array('d', [1]),
                                                     array.array('d', [abs(unc_cb_hessian_ehi)]),  
                                                     array.array('d', [abs(unc_cb_hessian_ehi)]),  
                                                     array.array('d',[0]), array.array('d',[0]))
        utilities.graphStyle(unc_cb_hessian_g,style=23,color=ROOT.kRed-3)


        print 'getting toys from tensorflow'
        unc_tf_toys    = ROOT.TH1F(par+'_tf_toys_hist', 'toys for '+par, 100, -3., 3.)
        obj_tf_toys.Draw(par+'>>'+unc_tf_toys.GetName())
        unc_tf_toys.Scale(1./unc_tf_toys.Integral())
        unc_tf_toys_h, unc_tf_toys_cen, unc_tf_toys_sig = fitToys(unc_tf_toys, ROOT.kBlue-1)
        unc_tf_toys_g = ROOT.TGraphAsymmErrors(1, array.array('d', [unc_tf_toys_cen]), 
                                                  array.array('d', [2]),
                                                  array.array('d', [abs(unc_tf_toys_sig)]),  
                                                  array.array('d', [abs(unc_tf_toys_sig)]),  
                                                  array.array('d',[0]), array.array('d',[0]))
        utilities.graphStyle(unc_tf_toys_g,style=22,color=ROOT.kBlue-1)

        print 'getting toys from combine'
        unc_cb_toys    = ROOT.TH1F(par+'_cb_toys_hist', 'toys from combine for '+par   , 100, -3., 3.)
        obj_cb_toys.Draw('trackedParam_'+par+'>>'+unc_cb_toys.GetName())
        unc_cb_toys.Scale(1./unc_cb_toys.Integral())
        unc_cb_toys_h, unc_cb_toys_cen, unc_cb_toys_sig = fitToys(unc_cb_toys, ROOT.kGreen+1)
        unc_cb_toys_g = ROOT.TGraphAsymmErrors(1, array.array('d', [unc_cb_toys_cen]), 
                                                  array.array('d', [3]),
                                                  array.array('d', [abs(unc_cb_toys_sig)]),  
                                                  array.array('d', [abs(unc_cb_toys_sig)]),  
                                                  array.array('d',[0]), array.array('d',[0]))
        utilities.graphStyle(unc_cb_toys_g,style=21,color=ROOT.kGreen+1)

        print 'getting the graph for combine scans'
        ##get the graph from the offset
        cb_scan_graph = getCleanedGraph(dir_cb_scans+par+'/scan_'+par+'.root', par, norm=1., n_iter=0)# tmp_val, n_iter=5)
        cb_scan_graph.Draw('ap')

        ## graph with offest
        cb_scan_graph.Fit('pol2', 'rob')
        cb_scan_fit = cb_scan_graph.GetFunction('pol2')

        (cb_scan_cen, cb_scan_err1, cb_scan_err2) = utilities.solvePol2(cb_scan_fit.GetParameter(2), cb_scan_fit.GetParameter(1), cb_scan_fit.GetParameter(0)-1)
        vals_errs.append( ['combine, scans     ', cb_scan_cen, cb_scan_err1, cb_scan_err2])
        cb_scan_graph_nooffset = noOffsetGraph(copy.deepcopy(cb_scan_graph), cb_scan_fit)
        ggg = cb_scan_graph_nooffset.GetFunction('pol2'); ggg.SetLineColor(ROOT.kMagenta+2)
        cb_scan_graph_nooffset.Draw('ap')

        cb_scan_g = ROOT.TGraphAsymmErrors(1, array.array('d', [cb_scan_cen]), 
                                                  array.array('d', [4]),
                                                  array.array('d', [abs(cb_scan_err1)]),  
                                                  array.array('d', [abs(cb_scan_err2)]),  
                                                  array.array('d',[0]), array.array('d',[0]))
        utilities.graphStyle(cb_scan_g, color=ROOT.kMagenta+2)

        print 'getting the graph for tensorflow scans'
        ##get the graph from the offset
        tf_scan_graph = getCleanedGraph(dir_tf_scans+'/fitresults_'+par+'.root', par, norm=1., n_iter=0, treename='fitresults')# tmp_val, n_iter=5)
        tf_scan_graph.Draw('ap')

        ## graph with offest
        tf_scan_graph.Fit('pol2', 'rob')
        tf_scan_fit = tf_scan_graph.GetFunction('pol2')

        (tf_scan_cen, tf_scan_err1, tf_scan_err2) = utilities.solvePol2(tf_scan_fit.GetParameter(2), tf_scan_fit.GetParameter(1), tf_scan_fit.GetParameter(0)-1)
        vals_errs.append( ['combine, scans     ', tf_scan_cen, tf_scan_err1, tf_scan_err2])
        tf_scan_graph_nooffset = noOffsetGraph(copy.deepcopy(tf_scan_graph), tf_scan_fit)
        fff = tf_scan_graph_nooffset.GetFunction('pol2'); fff.SetLineColor(ROOT.kAzure+4)
        utilities.graphStyle(tf_scan_graph_nooffset, style=22, color=ROOT.kAzure+1)
        tf_scan_graph_nooffset.Draw('ap')

        tf_scan_g = ROOT.TGraphAsymmErrors(1, array.array('d', [tf_scan_cen]), 
                                                  array.array('d', [5]),
                                                  array.array('d', [abs(tf_scan_err1)]),  
                                                  array.array('d', [abs(tf_scan_err2)]),  
                                                  array.array('d',[0]), array.array('d',[0]))
        utilities.graphStyle(tf_scan_g, style=26, color=ROOT.kAzure+1)

        c4 = ROOT.TCanvas('foo', 'bar', 1200, 350)
        c4.Divide(3,1)

        c4.cd(1)
        unc_tf_toys_h.GetXaxis().SetTitle('toys')
        unc_tf_toys_h.Draw('')
        unc_cb_toys_h.Draw('same')
    
        c4.cd(2)
        mg = ROOT.TMultiGraph()
        mg.SetTitle('scans for '+par)
        mg.Add(cb_scan_graph_nooffset)
        mg.Add(tf_scan_graph_nooffset)
        mg.Draw('ap')

        xmin=-2;xmax=2.
        mg.GetYaxis().SetRangeUser(-0.1, 2.)
        mg.GetXaxis().SetRangeUser(xmin,xmax)
        mg.GetXaxis().SetTitle(par)
        mg.SetTitle('scans of '+par)

        tmp_line = ROOT.TLine(xmin, 1., xmax, 1.)
        tmp_line.SetLineStyle(3); tmp_line.SetLineWidth(2);
        tmp_line.Draw('same')
        tmp_line0 = ROOT.TLine(xmin, 0., xmax, 0.)
        tmp_line0.SetLineStyle(1); tmp_line0.SetLineWidth(2);
        tmp_line0.Draw('same')

        #valhist = ROOT.TH1F('valhist', 'values for '+par, len(vals_errs), 0., len(vals_errs))
        #for i,(n,x0,x1,x2) in enumerate(vals_errs):
        #    valhist.SetBinContent(i+1, x0)

        c4.cd(3)
        #valgraph.Draw('ap')
        mg2 = ROOT.TMultiGraph()
        mg2.SetTitle('values and uncertainties')
        mg2.Add(unc_tf_hessian_g)
        mg2.Add(unc_cb_hessian_g)
        mg2.Add(unc_tf_toys_g)
        mg2.Add(unc_cb_toys_g)
        mg2.Add(cb_scan_g)
        mg2.Add(tf_scan_g)

        mg2.Draw('ap')
        ymin = -1; ymax = 6
        mg2.GetYaxis().SetRangeUser(ymin,ymax)
        mg2.GetXaxis().SetRangeUser(-2.,2.)
        tmp_line1 = ROOT.TLine(0, ymin, 0., ymax)
        tmp_line1.SetLineStyle(3); tmp_line.SetLineWidth(2);
        tmp_line1.Draw('same')
        #mg2.Draw('ap')

        lat = ROOT.TLatex()
        lat.SetTextSize(0.03)
        lat.DrawLatex(mg2.GetXaxis().GetXmin()+0.03, 0.25, 'hessian tensorflow')
        lat.DrawLatex(mg2.GetXaxis().GetXmin()+0.03, 1.25, 'hessian combine')
        lat.DrawLatex(mg2.GetXaxis().GetXmin()+0.03, 2.25, 'toys tensorflow')
        lat.DrawLatex(mg2.GetXaxis().GetXmin()+0.03, 3.25, 'toys combine')
        lat.DrawLatex(mg2.GetXaxis().GetXmin()+0.03, 4.25, 'scan tensorflow')
        lat.DrawLatex(mg2.GetXaxis().GetXmin()+0.03, 5.25, 'scan combine')

        if options.webdir:
            if not os.path.isdir(options.webdir):
                os.system('mkdir -p '+options.webdir)
            os.system('cp /afs/cern.ch/user/g/gpetrucc/php/index.php '+options.webdir)
            c4.SaveAs(options.webdir+'/'+par+'.pdf')
            c4.SaveAs(options.webdir+'/'+par+'.png')
    

