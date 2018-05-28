import ROOT, itertools, datetime, math, copy, os
from array import array


## usage:  python templatesRoofit.py --infile /eos/user/m/mdunser/W_NLO_amcatnlo_newDefinitionFinalFix.root --nlo --outdir ~/www/private/w-helicity-13TeV/cosThetaFits/2018-02-28/
## usage:  python templatesRoofit.py --infile /eos/user/m/mdunser/W_LO_madgraph_finalDressing_extOnly.root        --outdir ~/www/private/w-helicity-13TeV/cosThetaFits/2018-02-28/

def formatHisto(hist):
    hist.GetXaxis().SetTitleOffset(1.02)
    hist.GetXaxis().SetTitleSize(0.06)
    hist.GetXaxis().SetLabelSize(0.06)

    hist.GetYaxis().SetTitleOffset(1.02)
    hist.GetYaxis().SetTitleSize(0.06)
    hist.GetYaxis().SetLabelSize(0.06)

    hist.GetZaxis().SetLabelSize(0.06)

def symmetrizeFractions(fractionR, fractionL, fraction0, nsmooth=0):
    ## symmetrize the fractions
    newcontents = {}
    nbinsY = fractionR.GetXaxis().GetNbins()
    nbinsZ = fractionR.GetYaxis().GetNbins()

    fractionR_sym = fractionR.Clone(fractionR.GetName()+'_sym')
    fractionL_sym = fractionL.Clone(fractionL.GetName()+'_sym')
    fraction0_sym = fraction0.Clone(fraction0.GetName()+'_sym')
    fractionR_sym.Reset()
    fractionL_sym.Reset()
    fraction0_sym.Reset()

    ## careful here, this symmetrization makes f0 flat in Y

    for iy in range(1,nbinsY+1):
        for iz in range(1,nbinsZ+1):
            newcontents[('R', iy, iz)] = 1./2.*sum( fractionR.GetBinContent(i, iz) for i in [iy, nbinsY+1-iy] )
            newcontents[('L', iy, iz)] = 1./2.*sum( fractionL.GetBinContent(i, iz) for i in [iy, nbinsY+1-iy] )
            newcontents[('0', iy, iz)] = 1./nbinsY*sum( fraction0.GetBinContent(i, iz) for i in range(1,nbinsZ+1) )
    for iy in range(1,nbinsY+1):
        for iz in range(1,nbinsZ+1):
            fractionR_sym.SetBinContent(iy, iz, newcontents[('R', iy, iz)])
            fractionL_sym.SetBinContent(iy, iz, newcontents[('L', iy, iz)])
            fraction0_sym.SetBinContent(iy, iz, newcontents[('0', iy, iz)])
    
    for i in range(nsmooth):
        fractionR.Smooth()
        fractionL.Smooth()
        fraction0.Smooth()

    return [fractionR_sym, fractionL_sym, fraction0_sym]

def saveCanv(c, name):
    c.SaveAs(name+'.pdf')
    c.SaveAs(name+'.png')

from optparse import OptionParser
parser = OptionParser(usage='%prog [options] cards/card*.txt')
parser.add_option('--roofit' , dest='doRooFit' , default=False, action='store_true', help='Use fancy RooFit generic pdf fitting instead of simple chi2.')
parser.add_option('--generic', dest='doGeneric', default=True , action='store_true', help='Use generic pdf instead of whatever else')
parser.add_option('--nlo'    , dest='doNLO'    , default=False, action='store_true', help='Use the amc@nlo sample.')
parser.add_option('--bins-atlas', dest='atlasBins'    , default=False, action='store_true', help='Use the binning of the ATLAS paper.')
parser.add_option('-i','--infile', dest='infile', default='', type='string', help='Specify the input file. should be a single (big) friendtree.')
parser.add_option('-o','--outdir', dest='outdir', default='', type='string', help='Specify the output directory for the plots. It makes a lot of plots.')
(options, args) = parser.parse_args()


ROOT.gROOT.SetBatch()

nlostring = 'NLO' if options.doNLO else 'LO'


if not (options.outdir or options.infile):
    raise RuntimeError, 'You have to give an input file and an output directory!'

plotsdir = '{od}/chi2_muEl/{nlo}/'.format(od=options.outdir,nlo=nlostring)

if not os.path.isdir(plotsdir):
    os.system('mkdir -p {pd}'.format(pd=plotsdir))
    os.system('cp ~/index.php {pd}/'.format(pd=plotsdir))

maxYW = 6.

## some tree specific things. we need the name of the 
## variables of the W in the tree

var_wy  = 'abs(genw_y)'
var_wpt = 'genw_pt'
var_wch = 'genw_charge'
var_dec = 'genw_decayId'
##var_cos = 'genw_costcs'
#var_cos = 'genw_cost2d'
var_cos = 'genw_costcm'

## weightstring
gen_weight = '(weightGen/abs(weightGen))'

## get the tree from the file

if os.path.isfile(options.infile):
    infile = ROOT.TFile(options.infile, 'read')
    tree = infile.Get('Friends')
else:
    tree = ROOT.TChain('Friends')
    rootlist = list( i for i in os.listdir(options.infile) if '.root' in i)
    for i,f in enumerate(rootlist):
        if i > 9: continue
        print 'adding file', f
        tree.Add(options.infile+'/'+f)


## first build the quantiles in both rapidity and pT


if not options.atlasBins:
    ## make the quantiles for YW
    ## ===================================
    print('FILLING FOR THE W-rapidity QUANTILES')
    
    nqy = 15
    h_tmp_wy  = ROOT.TH1F('h_tmp_wy','quantile calculation Yw', 1000, 0., maxYW)
    tree.Draw(var_wy+'>>h_tmp_wy', '('+var_wch + ' > 0 && abs(genw_decayId)==14 )*'+gen_weight)
    xqy = array('d', [i/float(nqy)+1./float(nqy) for i in range(nqy)])
    yqy = array('d', [1. for i in range(nqy)])
    foobar = h_tmp_wy.GetQuantiles(nqy,yqy,xqy);
    
    yqnewy = array('d', [0.] + [float('{a:.3f}'.format(a=i)) for i in yqy])
    
    wrap_nbins = len(yqnewy)-1
    wrap_bins = array('d', yqnewy)
    
    ## make the quantiles for W-pT
    ## ===================================
    
    print('FILLING FOR THE W-pT QUANTILES')
    nq =  20 ## number of quantiles
    h_tmp_wpt = ROOT.TH1F('h_tmp_wpt','quantile calculation', 1000, 0., 100.)
    tree.Draw(var_wpt+'>>h_tmp_wpt', '(abs(genw_decayId)==14 || abs(genw_decayId)== 12) *'+gen_weight)
    xq = array('d', [i/float(nq)+1./float(nq) for i in range(int(nq))])
    yq = array('d', [1 for i in range(nq)])
    h_tmp_wpt.GetQuantiles(nq,yq,xq);
    
    
    yqnew = array('d', [0.] + [float('{a:.3f}'.format(a=i)) for i in yq])
    hnew = ROOT.TH1F('h_wpt_quantiles', 'wpt rebinned', len(yq), yqnew)
    
    wpt_nbins = nq
    wpt_bins = yqnew

else:
    wrap_bins   = array('d', [0.20*i for i in range(15)] + [3., 3.25, 3.5, 3.75, 4., 4.25, 4.5, 5., 6.])
    wrap_nbins  = len(wrap_bins)-1
    wpt_bins  = array('d', range(11) + [12., 14., 16., 18., 20., 25., 30., 35., 40., 50., 60., 70., 100.])
    wpt_nbins = len(wpt_bins)-1

print('this is the YW binning', wrap_bins)
print('these are the w-pt quantiles: ', wpt_bins)

## ===================================
## finished with the quantile production. we now have wpt_bins and wrap_bins

## first we need a bunch of histograms in which we store the weights
## as a function of cos(theta)* and the helicity fractions :

cost_nbins =  50
cost_bins = array('d', [2*i/float(cost_nbins)-1 for i in range(cost_nbins+1)])

h3_rapVsCMvsWPtPlus  = ROOT.TH3D('h3_rapVsCMvsWPtPlus' ,'h3_rapVsCMvsWPtPlus' , cost_nbins, cost_bins, wrap_nbins, wrap_bins, wpt_nbins, wpt_bins); h3_rapVsCMvsWPtPlus .Sumw2()
h3_rapVsCMvsWPtMinus = ROOT.TH3D('h3_rapVsCMvsWPtMinus','h3_rapVsCMvsWPtMinus', cost_nbins, cost_bins, wrap_nbins, wrap_bins, wpt_nbins, wpt_bins); h3_rapVsCMvsWPtMinus.Sumw2()

h3_rapVsCMvsWPtPlus .GetXaxis().SetTitle('cos #theta'); h3_rapVsCMvsWPtPlus .GetYaxis().SetTitle('Y_{W}'); h3_rapVsCMvsWPtPlus .GetZaxis().SetTitle('W-p_{T}')
h3_rapVsCMvsWPtMinus.GetXaxis().SetTitle('cos #theta'); h3_rapVsCMvsWPtMinus.GetYaxis().SetTitle('Y_{W}'); h3_rapVsCMvsWPtMinus.GetZaxis().SetTitle('W-p_{T}')

nbinsX = h3_rapVsCMvsWPtPlus.GetXaxis().GetNbins()
nbinsY = h3_rapVsCMvsWPtPlus.GetYaxis().GetNbins()
nbinsZ = h3_rapVsCMvsWPtPlus.GetZaxis().GetNbins()

## project pT versus rapidity for the fractions
fractionR_plus = h3_rapVsCMvsWPtPlus.Project3D('zy').Clone('fractionR_plus'); fractionR_plus.SetTitle('W^{+}: fractions R'); fractionR_plus.Reset(); formatHisto(fractionR_plus)
fractionL_plus = h3_rapVsCMvsWPtPlus.Project3D('zy').Clone('fractionL_plus'); fractionL_plus.SetTitle('W^{+}: fractions L'); fractionL_plus.Reset(); formatHisto(fractionL_plus)
fraction0_plus = h3_rapVsCMvsWPtPlus.Project3D('zy').Clone('fraction0_plus'); fraction0_plus.SetTitle('W^{+}: fractions 0'); fraction0_plus.Reset(); formatHisto(fraction0_plus)

fractionR_minus = h3_rapVsCMvsWPtMinus.Project3D('zy').Clone('fractionR_minus'); fractionR_minus.SetTitle('W^{-}:fractions R'); fractionR_minus.Reset(); formatHisto(fractionR_minus)
fractionL_minus = h3_rapVsCMvsWPtMinus.Project3D('zy').Clone('fractionL_minus'); fractionL_minus.SetTitle('W^{-}:fractions L'); fractionL_minus.Reset(); formatHisto(fractionL_minus)
fraction0_minus = h3_rapVsCMvsWPtMinus.Project3D('zy').Clone('fraction0_minus'); fraction0_minus.SetTitle('W^{-}:fractions 0'); fraction0_minus.Reset(); formatHisto(fraction0_minus)

## done making the histograms


## we also need the three analytic helicity fraction functions

ana_r = ROOT.TF1('ana_r', '3./8.*(1+x)^2')
ana_l = ROOT.TF1('ana_l', '3./8.*(1-x)^2')
ana_0 = ROOT.TF1('ana_0', '3./4*(TMath::Sqrt(1-x*x))^2')

## done making the functions

lat = ROOT.TLatex(); lat.SetNDC(); lat.SetTextSize(0.03)

if options.doRooFit:
    ## name the bins and make a cut for each bin. needed later for slicing the
    ## roodataset
    
    bins = {}
    
    for ( (irap, rap), (ipt, pt) , ch) in itertools.product(enumerate(wrap_bins),enumerate(wpt_bins), ['minus','plus']):
        _bin = (irap, ipt, ch)
        if rap == wrap_bins[-1] or pt == wpt_bins[-1]  : continue
        bins[_bin] = 'abs(genw_y) >= {ylo} && abs(genw_y) < {yhi} && genw_pt >= {plo} && genw_pt < {phi} && genw_charge {wch}'.format(ylo=rap, yhi=wrap_bins[irap+1], plo=pt, phi=wpt_bins[ipt+1], wch = '>0' if ch == 'plus' else '<0')
    
    #print(bins)
    #sys.exit()
    
    
    ## moving on to some more roofit specific things in
    ## defining the roorealvars we want to load from the tree
    
    # Define W variables
    wy  = ROOT.RooRealVar(var_wy ,'wy'  , 0., maxYW  )
    wpt = ROOT.RooRealVar(var_wpt,'wpt' ,  0., 100.)
    wch = ROOT.RooRealVar(var_wch,'wch' , -2., 2.  )
    cos = ROOT.RooRealVar(var_cos,'cos #theta^{*}' , -1., 1.  )
    dec = ROOT.RooRealVar(var_dec,'decay id of w'  , 10 , 18  )

    argset = ROOT.RooArgSet(wy, wpt, wch, cos, dec)
    
    ## import the variables into a dataset. note that there is a W+ cut
    ## applied here
    
    if options.doNLO:
        genw = ROOT.RooRealVar('weightGen','gen weight' , -225995., 225995.  )
        wfor = ROOT.RooFormulaVar('weight', 'event weight', gen_weight, ROOT.RooArgList(genw) )
        argset.add(genw)
        ds1 = ROOT.RooDataSet('ds1','ds1', argset, ROOT.RooFit.Import(tree), ROOT.RooFit.Cut('genw_decayId == 14') )
        wvar = ds1.addColumn(wfor)
        ds = ROOT.RooDataSet('ds','ds', ds1, ds1.get(), '',  wvar.GetName() )
        ds.Print()
    else:
        ds = ROOT.RooDataSet('ds','ds', argset, ROOT.RooFit.Import(tree), ROOT.RooFit.Cut('genw_decayId == 14') )
        ds.Print()
    
    
    ## make the rooworkspace which will have all the objects
    
    w = ROOT.RooWorkspace('w')
    getattr(w,'import')(ds)
    
    ## for plotting 
    c1 = ROOT.TCanvas()
    
    ## foobar getattr(w, 'import')(f_f0)
    ## foobar getattr(w, 'import')(f_fL)
    ## foobar getattr(w, 'import')(f_fR)
    
    ## here we start looping on the bins in rapidity and pT of the W
    ## we make a roodataset for each cut (a .reduce from the original)
    ## we make pdf for each bin, with parameters fL and f0 and a n
    ## normalization parameter for each of the bins. then we fit the bin
    
    for (ib,( (irap, ipt, ch) , cut)) in enumerate(bins.items()):  ## a lot of unpacking. but it works
        name = '{irap}_{ipt}_{wch}'.format(irap=irap, ipt=ipt, wch=ch)
    
        #if ib: continue
        #if not name == '0_17': continue
        # if not ipt < 3: continue
        print('at bin number {i}: {n}'.format(i=ib, n=name))
    
        ## slice the roodataset with the specific cut and import it into the workspace
        ds_tmp = ds.reduce(ROOT.RooFit.Name('ds_'+name), ROOT.RooFit.Cut(cut) )
        getattr(w,'import')(ds_tmp)
    
        if options.doGeneric:
            ## make the three parameters for each bin
            w.factory('norm_{n}[1.,0.,1e6]'.format(n=name)) ## could probably give a smarter initial value and ranges here
            w.factory('fL_{n}[0.7,0.,1.]'  .format(n=name))
            w.factory('f0_{n}[0.1,0.,1.]'  .format(n=name))
    
            ## making a RooGenericPdf
            ## =====================================
            ## construct the pdf-string for each bin and import into workspace
            model_str  = 'EXPR::helicityFractions_'+name
            ## model_str += '("norm_{n}*( (1.-fL_{n}-f0_{n}) * 3./8.*(1+{x})^2  + fL_{n} * 3./8.*(1-{x})^2 + f0_{n} * 3./4*(TMath::Sqrt(1-{x}*{x}))^2 )"'.format(n=name, x=var_cos)
            ## model_str += ',{{{x},norm_{n},fL_{n},f0_{n}}} )'.format(n=name, x=var_cos)
            model_str += '("( (1.-fL_{n}-f0_{n}) * 3./8.*(1+{x})^2  + fL_{n} * 3./8.*(1-{x})^2 + f0_{n} * 3./4*(TMath::Sqrt(1-{x}*{x}))^2 )"'.format(n=name, x=var_cos)
            model_str += ',{{{x},fL_{n},f0_{n}}} )'.format(n=name, x=var_cos)
    
            w.factory(model_str)
        else:
            ##tmp_func_f0 = ROOT.RooGenericPdf('func_f0_'+name,'func_f0_'+name, '3./4.*(TMath::Sqrt(1-{x}*{x}))^2'.format(x=var_cos), ROOT.RooArgList(cos))
            ##tmp_func_fL = ROOT.RooGenericPdf('func_fL_'+name,'func_fL_'+name, '3./8.*(1-{x})^2'                 .format(x=var_cos), ROOT.RooArgList(cos))
            ##tmp_func_fR = ROOT.RooGenericPdf('func_fR_'+name,'func_fR_'+name, '3./8.*(1+{x})^2'                 .format(x=var_cos), ROOT.RooArgList(cos))
            ##tmp_f0 = ROOT.RooRealVar('f0_'+name, 'f0 in bin '+name, 0.1, 0., 1.); getattr(w, 'import')(tmp_f0)
            ##tmp_fL = ROOT.RooRealVar('fL_'+name, 'fL in bin '+name, 0.7, 0., 1.); getattr(w, 'import')(tmp_fL)
            ##tmp_fR = ROOT.RooRealVar('fR_'+name, 'fR in bin '+name, 0.2, 0., 1.); getattr(w, 'import')(tmp_fR)
            ##tmp_f_all = ROOT.RooAddPdf('helicityFractions_'+name, 'helicityFractions_'+name, ROOT.RooArgList(tmp_func_f0, tmp_func_fL, tmp_func_fR), ROOT.RooArgList(tmp_f0, tmp_fL), 1) ## recursive version
    
            tmp_f0 = ROOT.RooRealVar('f0_'+name, 'f0 in bin '+name, 0., 1e6); getattr(w, 'import')(tmp_f0)
            tmp_fL = ROOT.RooRealVar('fL_'+name, 'fL in bin '+name, 0., 1e6); getattr(w, 'import')(tmp_fL)
            tmp_fR = ROOT.RooRealVar('fR_'+name, 'fR in bin '+name, 0., 1e6); getattr(w, 'import')(tmp_fR)
    
            gen_tmp_func_f0 = ROOT.RooGenericPdf('gen_func_f0_'+name,'gen_func_f0_'+name, '(3./4.*(TMath::Sqrt(1-{x}*{x}))^2)'.format(x=var_cos), ROOT.RooArgList(cos))
            gen_tmp_func_fL = ROOT.RooGenericPdf('gen_func_fL_'+name,'gen_func_fL_'+name, '(3./8.*(1-{x})^2)'                 .format(x=var_cos), ROOT.RooArgList(cos))
            gen_tmp_func_fR = ROOT.RooGenericPdf('gen_func_fR_'+name,'gen_func_fR_'+name, '(3./8.*(1+{x})^2)'                 .format(x=var_cos), ROOT.RooArgList(cos))
    
            tmp_func_f0 = ROOT.RooExtendPdf('func_f0_'+name,'func_f0_'+name, gen_tmp_func_f0, tmp_f0)
            tmp_func_fL = ROOT.RooExtendPdf('func_fL_'+name,'func_fL_'+name, gen_tmp_func_fL, tmp_fL)
            tmp_func_fR = ROOT.RooExtendPdf('func_fR_'+name,'func_fR_'+name, gen_tmp_func_fR, tmp_fR)
            tmp_f_all = ROOT.RooAddPdf('helicityFractions_'+name, 'helicityFractions_'+name, ROOT.RooArgList(tmp_func_f0, tmp_func_fL, tmp_func_fR))##, ROOT.RooArgList(tmp_f0, tmp_fL, tmp_fR), 1)
            getattr(w, 'import')(tmp_f_all)
    
        ## fit the thing!
        w.pdf('helicityFractions_'+name).fitTo( w.data(ds_tmp.GetName()) )#, ROOT.RooFit.Strategy(2)) #, ROOT.RooFit.Extended(1) )
        ## w.pdf('helicityFractions_'+name).chi2FitTo( w.data(ds_tmp.GetName()).binnedClone(), ROOT.RooFit.Verbose(1) )
        if options.doGeneric:
            f0 = w.var('f0_{n}'.format(n=name)).getValV()
            fL = w.var('fL_{n}'.format(n=name)).getValV()
            fR = 1. - f0 - fL
        else:
            ## f0 = w.var('f0_{n}'.format(n=name)).getValV()
            ## fL_param = w.var('fL_{n}'.format(n=name)).getValV()
            ## fR = (1.-f0)*(1.-fL_param)
            ## fL = (1.-f0)*fL_param
            n0 = w.var('f0_{n}'.format(n=name)).getValV()
            nL = w.var('fL_{n}'.format(n=name)).getValV()
            nR = w.var('fR_{n}'.format(n=name)).getValV()
            f0 = n0/(n0+nL+nR)
            fL = nL/(n0+nL+nR)
            fR = nR/(n0+nL+nR)
            
        ## fill the histogram of the fractions. get the correct bin number first
        bin_yw = irap+1
        bin_pt = ipt +1
        fractionR.SetBinContent(bin_yw, bin_pt, fR); fractionR.SetBinError(bin_yw, bin_pt, 0.) ## no errors yet
        fractionL.SetBinContent(bin_yw, bin_pt, fL); fractionL.SetBinError(bin_yw, bin_pt, 0.) ## no errors yet
        fraction0.SetBinContent(bin_yw, bin_pt, f0); fraction0.SetBinError(bin_yw, bin_pt, 0.) ## no errors yet
    
        for bin_cos in range(1, h3_weightsR.GetNbinsX()+1):
            ## get the bin center and set the roorealvar to it
            tmp_cos = h3_weightsR.GetXaxis().GetBinCenter(bin_cos)
            w.var(var_cos).setVal(tmp_cos)
            ## evaluate the fitted function:
            tmp_cos_fit = w.pdf('helicityFractions_'+name).getVal(ROOT.RooArgSet(cos))
            ## print('this is the fit evaluation at costheta {cos:.3f}: {foo:.3f}'.format(cos=tmp_cos,foo=tmp_cos_fit))
            ## evaluate the 3 analytic functions
            tmp_cos_ana_r = ana_r.Eval(tmp_cos)
            tmp_cos_ana_l = ana_l.Eval(tmp_cos)
            tmp_cos_ana_0 = ana_0.Eval(tmp_cos)
    
            h3_weightsR.SetBinContent(bin_cos, bin_yw, bin_pt, tmp_cos_ana_r/tmp_cos_fit); #h3_weightsR.SetBinError(jx, bin_yw, bin_pt, tmp_wr.GetBinError(jx))
            h3_weightsL.SetBinContent(bin_cos, bin_yw, bin_pt, tmp_cos_ana_l/tmp_cos_fit); #h3_weightsL.SetBinError(jx, bin_yw, bin_pt, tmp_wl.GetBinError(jx))
            h3_weights0.SetBinContent(bin_cos, bin_yw, bin_pt, tmp_cos_ana_0/tmp_cos_fit); #h3_weights0.SetBinError(jx, bin_yw, bin_pt, tmp_w0.GetBinError(jx))
        
    
        ## do some drawing (of the function and the data)
        c1.Clear()
        frame_cos_tmp = cos.frame(ROOT.RooFit.Title('bin: {n}'.format(n=name)))
        w.data(ds_tmp.GetName()).plotOn(frame_cos_tmp, ROOT.RooFit.Binning(cost_nbins))
        w.pdf ('helicityFractions_{n}'.format(n=name)).plotOn(frame_cos_tmp)
        frame_cos_tmp.Draw()
        lat.DrawLatex(0.45, 0.85, 'f0: {f0:.4f}'.format(f0=f0) )
        lat.DrawLatex(0.45, 0.80, 'fL: {fL:.4f}'.format(fL=fL) )
        lat.DrawLatex(0.45, 0.75, 'fR: {fR:.4f}'.format(fR=fR) )
        c1.SaveAs('plotsRoofit/MLfit_muOnly/{nlo}/cosTheta_roofit_newDef_{n}.pdf'.format(n=name,nlo=nlostring))
        c1.SaveAs('plotsRoofit/MLfit_muOnly/{nlo}/cosTheta_roofit_newDef_{n}.png'.format(n=name,nlo=nlostring))

else:
    print('FILLING THE 3D HISTOGRAM!!')
    tree.Draw(var_wpt+':'+var_wy+':'+var_cos+'>>h3_rapVsCMvsWPtPlus' , '('+var_wch + ' > 0 && (genw_decayId == 14 || genw_decayId == 12) )* '+gen_weight, '')
    tree.Draw(var_wpt+':'+var_wy+':'+var_cos+'>>h3_rapVsCMvsWPtMinus', '('+var_wch + ' < 0 && (genw_decayId == 14 || genw_decayId == 12) )* '+gen_weight, '')
    
    ## END FILLING WPT YW CM HISTOGRAM
    ## ======================================
    
    ## f_wr = ROOT.TF1('f_analytic_wr', '3./8.*(1+x)^2'              , -1., 1.)
    ## f_wl = ROOT.TF1('f_analytic_wl', '3./8.*(1-x)^2'              , -1., 1.)
    ## f_w0 = ROOT.TF1('f_analytic_w0', '3./4*(TMath::Sqrt(1-x*x))^2', -1., 1.)
    
    ## build normalized templates of CM for each of the helicities
    nfills = int(1e7)
    h_ana_wr = ROOT.TH1F('h_analytic_wr', 'h_analytic_wr', cost_nbins, -1., 1.); h_ana_wr.FillRandom(ana_r.GetName(), nfills); h_ana_wr.Scale(1./nfills);
    h_ana_wl = ROOT.TH1F('h_analytic_wl', 'h_analytic_wl', cost_nbins, -1., 1.); h_ana_wl.FillRandom(ana_l.GetName(), nfills); h_ana_wl.Scale(1./nfills);
    h_ana_w0 = ROOT.TH1F('h_analytic_w0', 'h_analytic_w0', cost_nbins, -1., 1.); h_ana_w0.FillRandom(ana_0.GetName(), nfills); h_ana_w0.Scale(1./nfills);
    h_ana_wr .GetXaxis().SetTitle('cos #theta')
    h_ana_wl .GetXaxis().SetTitle('cos #theta')
    h_ana_w0 .GetXaxis().SetTitle('cos #theta')

    c = ROOT.TCanvas()
    nfits = 0
    badfits = {}
    allfits = {}

    ROOT.gStyle.SetOptStat(0)

    for iy in range(1,nbinsY+1):
        for iz in range(1,nbinsZ+1):
            for wch in ['plus', 'minus']:
                nfits += 1
                #if nfits > 2: continue
                c.Clear()
                pos = wch == 'plus'
                name = '{iy}_{iz}_{ch}'.format(iy=iy-1,iz=iz-1,ch=wch)
                print('at bin {n}'.format(n=name))
                c.SetName ('canv_'+name)
                c.SetTitle('canv_'+name)
                h3_rapVsCMvsWPt = h3_rapVsCMvsWPtPlus if wch == 'plus' else h3_rapVsCMvsWPtMinus
                h_cm = h3_rapVsCMvsWPt.ProjectionX(name, iy if iy else 1, iy if iy else nbinsY, iz if iz else 1, iz if iz else nbinsZ)
                #h_cm.SetTitle('cosTheta_'+name)
                ylo = h3_rapVsCMvsWPt.GetYaxis().GetBinLowEdge(iy)
                yhi = h3_rapVsCMvsWPt.GetYaxis().GetBinUpEdge(iy)
                plo = h3_rapVsCMvsWPt.GetZaxis().GetBinLowEdge(iz)
                phi = h3_rapVsCMvsWPt.GetZaxis().GetBinUpEdge(iz)
                h_cm.SetTitle('{ch}: y_{{W}} #in [{ylo:.2f},{yhi:.2f}] , p_{{T}}^{{W}} #in [{plo:.2f},{phi:.2f}]'.format(ch='W^{+}' if wch == 'plus' else 'W^{-}', ylo=ylo,yhi=yhi,plo=plo,phi=phi) )
    
                fitterR = ROOT.TF1('helR_'+name,'[2] * ( (1.-[1]-[0])*{wr} + [1]*{wl} + [0]*{w0} )'.format(wr=ana_r.GetExpFormula(), wl=ana_l.GetExpFormula(), w0=ana_0.GetExpFormula()), -1., 1.)
                fitterL = ROOT.TF1('helL_'+name,'[2] * ( (1.-[1]-[0])*{wr} + [1]*{wl} + [0]*{w0} )'.format(wr=ana_r.GetExpFormula(), wl=ana_l.GetExpFormula(), w0=ana_0.GetExpFormula()), -1., 1.)
                fitter0 = ROOT.TF1('hel0_'+name,'[2] * ( (1.-[1]-[0])*{wr} + [1]*{wl} + [0]*{w0} )'.format(wr=ana_r.GetExpFormula(), wl=ana_l.GetExpFormula(), w0=ana_0.GetExpFormula()), -1., 1.)
    
                fitterR.SetParLimits(0, 0., 1.); fitterR.SetParLimits(1, 0., 1.)
                fitterL.SetParLimits(0, 0., 1.); fitterL.SetParLimits(1, 0., 1.)
                fitter0.SetParLimits(0, 0., 1.); fitter0.SetParLimits(1, 0., 1.)
    
                h_cm_norm = h_cm.Clone(h_cm.GetName()+'_norm')
                h_cm_norm.Scale(1./h_cm_norm.Integral())
    
                h_cm_norm.Fit(fitterR.GetName(), '', '', -1., 1.)
                h_cm_norm.Fit(fitterL.GetName(), '', '', -1., 1.)
                h_cm_norm.Fit(fitter0.GetName(), '', '', -1., 1.)
    
                f0 = fitterR.GetParameter(0)
                fL = fitterR.GetParameter(1)
                fR = 1.-fL-f0 #fitterR.GetParameter(0)
    
                # if f0 < 0.01: f0 = 0.01
    
                f0_err = fitterR.GetParError(0)
                fL_err = fitterR.GetParError(1)
                fR_err = math.sqrt(f0_err**2 + fL_err**2)

                print('fractions: \t fL: {fL:.4f} +- {fLe:.4f} \t fR: {fR:.4f} +- {fRe:.4f} \t f0: {f0:.4f} +- {f0e:.4f}'.format(fL=fL, fLe=fL_err, fR=fR, fRe=fR_err, f0=f0, f0e=f0_err))
                (fractionR_plus if pos else fractionR_minus).SetBinContent(iy, iz, fR); (fractionR_plus if pos else fractionR_minus).SetBinError(iy, iz, fR_err)
                (fractionL_plus if pos else fractionL_minus).SetBinContent(iy, iz, fL); (fractionL_plus if pos else fractionL_minus).SetBinError(iy, iz, fL_err)
                (fraction0_plus if pos else fraction0_minus).SetBinContent(iy, iz, f0); (fraction0_plus if pos else fraction0_minus).SetBinError(iy, iz, f0_err)
    
                lat.DrawLatex(0.45, 0.85, 'f0: {a1:.4f} +- {a2:.4f}'.format(a1=f0,a2=f0_err))
                lat.DrawLatex(0.45, 0.80, 'fL: {a1:.4f} +- {a2:.4f}'.format(a1=fL,a2=fL_err))
                lat.DrawLatex(0.45, 0.75, 'fR: {a1:.4f} +- {a2:.4f}'.format(a1=fR,a2=fR_err))
    
                chi2 = fitterR.GetChisquare(); ndf = fitterR.GetNDF(); 
                print('nev in the fitting: {n}'.format(n=h_cm.Integral()))
                if h_cm.Integral() < 1500.:
                    print('VERY FEW EVENTS!!!!')
                    print(name)
                    print('nev = {v}'.format(v=h_cm.Integral()))
                if chi2/ndf > 1.5:
                    print('VERY BAD FIT!!!!')
                    print(name)
                    print('chi2/ndf = {v}'.format(v=chi2/ndf))
                    badfits[name] = chi2/ndf
                allfits[name] = chi2/ndf
    
                lat.DrawLatex(0.45, 0.68, '#chi^{{2}}/ndf: {a1:.2f}/{a2} = {a3:.2f}'.format(a1=chi2, a2=ndf, a3=chi2/ndf))
                c.SaveAs('{pd}/cosTheta_chi2_{n}.pdf'.format(pd=plotsdir,n=name,nlo=nlostring))
                c.SaveAs('{pd}/cosTheta_chi2_{n}.png'.format(pd=plotsdir,n=name,nlo=nlostring))
    
    
    chi2dist = ROOT.TH1F('chi2', '#chi^{{2}} distribution - {n}'.format(n=('NLO' if options.doNLO else 'LO')), 50, 0., 5.); chi2dist.SetLineWidth(2); chi2dist.SetLineColor(ROOT.kAzure-2)
    chi2dist.GetXaxis().SetTitle('#chi^{2}')
    chi2dist.GetYaxis().SetTitle('# of fits')
    for n,chi2 in allfits.items():
        chi2dist.Fill( min(chi2, chi2dist.GetXaxis().GetBinCenter(chi2dist.GetXaxis().GetLast())) )
    chi2dist.Draw()
    lat.DrawLatex(0.7, 0.6, 'mean #chi^{{2}}: {m:.2f}'.format(m=chi2dist.GetMean()))
    
    c.SaveAs('{pd}/chi2_chi2.pdf'.format(pd=plotsdir,nlo=nlostring))
    c.SaveAs('{pd}/chi2_chi2.png'.format(pd=plotsdir,nlo=nlostring))

    
## don't symmetrize for absY (fractionR_plus_sym  , fractionL_plus_sym , fraction0_plus_sym ) = symmetrizeFractions(copy.deepcopy(fractionR_plus ), copy.deepcopy(fractionL_plus ), copy.deepcopy(fraction0_plus ))
## don't symmetrize for absY (fractionR_minus_sym , fractionL_minus_sym, fraction0_minus_sym) = symmetrizeFractions(copy.deepcopy(fractionR_minus), copy.deepcopy(fractionL_minus), copy.deepcopy(fraction0_minus))

## ## this doesn't do anything
## for i in range(0):
##     fractionR_plus_sym .Smooth(1, 'k5b')
##     fractionL_plus_sym .Smooth(1, 'k5b')
##     fraction0_plus_sym .Smooth(1, 'k5b')
##     fractionR_minus_sym.Smooth(1, 'k5b')
##     fractionL_minus_sym.Smooth(1, 'k5b')
##     fraction0_minus_sym.Smooth(1, 'k5b')

    
date = datetime.date.today().isoformat()

fittype = 'MLroofit' if options.doRooFit else 'chi2'

c.SetLeftMargin  (0.15)
c.SetRightMargin (0.15)
c.SetBottomMargin(0.15)

fractionR_plus .GetZaxis().SetRangeUser(0., 0.5)
fractionR_minus.GetZaxis().SetRangeUser(0., 0.5)
fractionL_plus .GetZaxis().SetRangeUser(0., 0.8)
fractionL_minus.GetZaxis().SetRangeUser(0., 0.8)
fraction0_plus .GetZaxis().SetRangeUser(0., 0.4)
fraction0_minus.GetZaxis().SetRangeUser(0., 0.4)

fractionR_plus .Draw('colz')
c.SaveAs('{pd}/fractionR_plus.pdf'.format(pd=plotsdir,nlo=nlostring))
c.SaveAs('{pd}/fractionR_plus.png'.format(pd=plotsdir,nlo=nlostring))
fractionL_plus .Draw('colz')
c.SaveAs('{pd}/fractionL_plus.pdf'.format(pd=plotsdir,nlo=nlostring))
c.SaveAs('{pd}/fractionL_plus.png'.format(pd=plotsdir,nlo=nlostring))
fraction0_plus .Draw('colz')
c.SaveAs('{pd}/fraction0_plus.pdf'.format(pd=plotsdir,nlo=nlostring))
c.SaveAs('{pd}/fraction0_plus.png'.format(pd=plotsdir,nlo=nlostring))
fractionR_minus.Draw('colz')
c.SaveAs('{pd}/fractionR_minus.pdf'.format(pd=plotsdir,nlo=nlostring))
c.SaveAs('{pd}/fractionR_minus.png'.format(pd=plotsdir,nlo=nlostring))
fractionL_minus.Draw('colz')
c.SaveAs('{pd}/fractionL_minus.pdf'.format(pd=plotsdir,nlo=nlostring))
c.SaveAs('{pd}/fractionL_minus.png'.format(pd=plotsdir,nlo=nlostring))
fraction0_minus.Draw('colz')
c.SaveAs('{pd}/fraction0_minus.pdf'.format(pd=plotsdir,nlo=nlostring))
c.SaveAs('{pd}/fraction0_minus.png'.format(pd=plotsdir,nlo=nlostring))

fractionLmR_plus = fractionL_plus .Clone('fractionLmR_plus')
fractionLmR_minus= fractionL_minus.Clone('fractionLmR_minus')
fractionLmR_plus .SetTitle('W^{+}: fractions L-R')
fractionLmR_minus.SetTitle('W^{-}: fractions L-R')
fractionLmR_plus .Add(fractionR_plus ,-1.)
fractionLmR_minus.Add(fractionR_minus,-1.)
fractionLmR_plus .GetZaxis().SetRangeUser(0., 0.8)
fractionLmR_minus.GetZaxis().SetRangeUser(0., 0.8)

fractionLmR_plus.Draw('colz')
c.SaveAs('{pd}/fractionLmR_plus.pdf'.format(pd=plotsdir,nlo=nlostring))
c.SaveAs('{pd}/fractionLmR_plus.png'.format(pd=plotsdir,nlo=nlostring))
fractionLmR_minus.Draw('colz')
c.SaveAs('{pd}/fractionLmR_minus.pdf'.format(pd=plotsdir,nlo=nlostring))
c.SaveAs('{pd}/fractionLmR_minus.png'.format(pd=plotsdir,nlo=nlostring))

## write the histograms into a file
outfile = ROOT.TFile('fractions_roofit_histos_{t}_{date}{nlo}_muEl_plusMinus.root'.format(t=fittype,date=date,nlo='_NLO' if options.doNLO else ''), 'recreate')

fractionR_plus.Write()
fractionL_plus.Write()
fraction0_plus.Write()
fractionR_minus.Write()
fractionL_minus.Write()
fraction0_minus.Write()

## fractionR_plus_sym .Write()
## fractionL_plus_sym .Write()
## fraction0_plus_sym .Write()
## fractionR_minus_sym.Write()
## fractionL_minus_sym.Write()
## fraction0_minus_sym.Write()

#h_tmp_wy.Write()

outfile.Close()


