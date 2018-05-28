import ROOT,os
from array import array

## USAGE:
## python templatesMoments.py --outdir ~/www/private/w-helicity-13TeV/angularCoefficients/2018-03-23/ --infile /eos/user/m/mdunser/w-helicity-13TeV/trees/TREES_latest_1muskim/friends/  --nlo  --bins-fractions fractions.root -c a7
## if you want to run all coefficients, remove the -c option. but this might take a while

def formatHisto(hist):
    hist.GetXaxis().SetTitleOffset(1.02)
    hist.GetXaxis().SetTitleSize(0.06)
    hist.GetXaxis().SetLabelSize(0.06)

    hist.GetYaxis().SetTitleOffset(1.02)
    hist.GetYaxis().SetTitleSize(0.06)
    hist.GetYaxis().SetLabelSize(0.06)

    hist.GetZaxis().SetLabelSize(0.06)

def symmetrizeCoefficients(dic):
    newdic = {}

    for key,val in dic.items():
        newcontents = {}
        nbinsY = val.GetXaxis().GetNbins()
        nbinsZ = val.GetYaxis().GetNbins()

        val_sym = val.Clone(val.GetName()+'_sym')
        val_sym.Reset()

        for iy in range(1,nbinsY+1):
            for iz in range(1,nbinsZ+1):
                newcontents[(key, iy, iz)] = 1./2.*sum( val.GetBinContent(i, iz) for i in [iy, nbinsY+1-iy] )

        for iy in range(1,nbinsY+1):
            for iz in range(1,nbinsZ+1):
                val_sym.SetBinContent(iy, iz, newcontents[(key, iy, iz)])
        newdic[key] = val_sym

    return newdic


from optparse import OptionParser
parser = OptionParser(usage='%prog [options] cards/card*.txt')
parser.add_option('--nlo'    , dest='doNLO'    , default=False, action='store_true', help='Use the amc@nlo sample.')
parser.add_option('--bins-atlas', dest='atlasBins'    , default=False, action='store_true', help='Use the binning of the ATLAS paper.')
parser.add_option('--bins-fractions', dest='fractionsBins'    , default='', type='string', help='Use the bins from a specified input file.')
parser.add_option('-v', dest='verbose'    , default=False, action='store_true', help='Save all the bin-by-bin distributions (it\'s a lot of them...')
parser.add_option('-i','--infile', dest='infile', default='', type='string', help='Specify the input file. should be a single (big) friendtree.')
parser.add_option('-o','--outdir', dest='outdir', default='', type='string', help='Specify the output directory for the plots. It makes a lot of plots.')
parser.add_option('-c','--coefficient', dest='coefficient', default='', type='string', help='Specify the exact angular coefficient you want to run.')
(options, args) = parser.parse_args()


if options.coefficient:
    print('RUNNING ON ONLY', options.coefficient)

ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)

nlostring = 'NLO' if options.doNLO else 'LO'


if not (options.outdir or options.infile):
    raise RuntimeError( 'You have to give an input file and an output directory!')

plotsdir = '{od}/moments_muEl/{nlo}/'.format(od=options.outdir,nlo=nlostring)

if not os.path.isdir(plotsdir):
    os.system('mkdir -p {pd}'.format(pd=plotsdir))
    os.system('cp ~/index.php {pd}/'.format(pd=plotsdir))

maxYW = 6.

var_wy  = 'genw_y'
var_wpt = 'genw_pt'
var_wch = 'genw_charge'
var_dec = 'genw_decayId'
var_cos = 'genw_costcs'
var_phi = 'genw_phics'

## weightstring
gen_weight = '(weightGen/abs(weightGen))'

if os.path.isfile(options.infile):
    infile = ROOT.TFile(options.infile, 'read')
    tree = infile.Get('Friends')
else:
    tree = ROOT.TChain('Friends')
    rootlist = list( i for i in os.listdir(options.infile) if '.root' in i)
    for f in rootlist:
        tree.Add(options.infile+'/'+f)



if not options.atlasBins and not options.fractionsBins:
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

elif options.atlasBins:
    wrap_bins   = array('d', [0.5*i for i in range(7)])
    wrap_nbins  = len(wrap_bins)-1
    wpt_bins  = array('d', [0., 20., 35., 50., 70., 100.])
    wpt_nbins = len(wpt_bins)-1

elif options.fractionsBins:
    ffile = ROOT.TFile(options.fractionsBins, 'read')
    hist = ffile.Get('fractionL_plus')
    ptbins = []
    ywbins = []
    for i in range(1,hist.GetXaxis().GetNbins()+2):
        ywbins.append(hist.GetXaxis().GetBinLowEdge(i))
    for i in range(1,hist.GetYaxis().GetNbins()+2):
        ptbins.append(hist.GetYaxis().GetBinLowEdge(i))
    wrap_bins = array('d', ywbins)
    wrap_nbins  = len(wrap_bins)-1
    wpt_bins  = array('d', ptbins)
    wpt_nbins = len(wpt_bins)-1


print('this is the YW binning:', wrap_bins)
print('this is the w-pt binninq: ', wpt_bins)
term_const = '(1.+{cost}^2)'.format(cost=var_cos)
term_a0    = '(1.-3.*{cost}^2)'                                        .format (cost=var_cos)
term_a1    = 'TMath::Sin(2.*TMath::ACos({cost})) * TMath::Cos({phi})'  .format (cost=var_cos,phi=var_phi)
term_a2    = 'TMath::Sin(TMath::ACos({cost}))^2*TMath::Cos(2.*{phi})'  .format (cost=var_cos,phi=var_phi)
term_a3    = 'TMath::Sin(TMath::ACos({cost}))*TMath::Cos({phi})'       .format (cost=var_cos,phi=var_phi)
term_a4    = '{cost}'                                                  .format (cost=var_cos)
term_a5    = 'TMath::Sin(TMath::ACos({cost}))^2 * TMath::Sin(2.*{phi})'.format (cost=var_cos,phi=var_phi)
term_a6    = 'TMath::Sin(2.*TMath::ACos({cost})) * TMath::Sin({phi})'  .format (cost=var_cos,phi=var_phi)
term_a7    = 'TMath::Sin(TMath::ACos({cost})) * TMath::Sin({phi})'     .format (cost=var_cos,phi=var_phi)
allterms  = {'const': term_const, 'a0': term_a0, 'a1': term_a1, 'a2': term_a2, 'a3': term_a3, 'a4': term_a4, 'a5': term_a5, 'a6': term_a6, 'a7': term_a7}
prefactor = {'const': [1., 0.] , 'a0': [10./3., 2./3.], 'a1': [5., 0.], 'a2': [10., 0.], 'a3': [4., 0.], 'a4': [4., 0.], 'a5': [5., 0.], 'a6': [5., 0.], 'a7': [4., 0.]}

arg_nbins =  50
arg_bins = array('d', [2*i/float(arg_nbins)-1 for i in range(arg_nbins+1)])

lat = ROOT.TLatex(); lat.SetNDC(); lat.SetTextSize(0.05)
c = ROOT.TCanvas()
c.SetLeftMargin  (0.15)
c.SetRightMargin (0.15)
c.SetBottomMargin(0.15)

all_2d = {}

for term,arg in sorted(allterms.items()) :
    if options.coefficient and not term == options.coefficient: 
        continue
    nx, x = arg_nbins, arg_bins
    ny, y = wrap_nbins, wrap_bins
    nz, z = wpt_nbins, wpt_bins
    if term == 'const': nx, x = arg_nbins, array('d', [2.+i/float(arg_nbins)-1 for i in range(arg_nbins+1)])
    if term == 'a0'   : nx, x = arg_nbins, array('d', [-2.+3.*i/float(arg_nbins)-0 for i in range(arg_nbins+1)])
    h3_argVsRapVsWPtPlus  = ROOT.TH3D('h3_{v}VsRapVsWPtPlus' .format(v=term),'h3_{v}VsRapVsWPtPlus' .format(v=term), nx, x, ny, y, nz, z); h3_argVsRapVsWPtPlus .Sumw2()
    h3_argVsRapVsWPtMinus = ROOT.TH3D('h3_{v}VsRapVsWPtMinus'.format(v=term),'h3_{v}VsRapVsWPtMinus'.format(v=term), nx, x, ny, y, nz, z); h3_argVsRapVsWPtMinus.Sumw2()
    print('filling for term', term)
    tree.Draw(var_wpt+':'+var_wy+':('+arg+')>>h3_{v}VsRapVsWPtPlus' .format(v=term), '('+var_wch + ' > 0 && (genw_decayId == 14 || genw_decayId == 12) )* '+gen_weight, '')
    tree.Draw(var_wpt+':'+var_wy+':('+arg+')>>h3_{v}VsRapVsWPtMinus'.format(v=term), '('+var_wch + ' < 0 && (genw_decayId == 14 || genw_decayId == 12) )* '+gen_weight, '')

    h2_rapVsWPtPlus  = h3_argVsRapVsWPtPlus .Project3D('zy')
    h2_rapVsWPtMinus = h3_argVsRapVsWPtMinus.Project3D('zy')
    formatHisto(h2_rapVsWPtPlus)
    formatHisto(h2_rapVsWPtMinus)

    nbinsX = h3_argVsRapVsWPtPlus.GetXaxis().GetNbins()
    nbinsY = h3_argVsRapVsWPtPlus.GetYaxis().GetNbins()
    nbinsZ = h3_argVsRapVsWPtPlus.GetZaxis().GetNbins()

    for iy in range(1,nbinsY+1):
        for iz in range(1,nbinsZ+1):
            for wch in ['plus', 'minus']:
                c.Clear()
                pos = wch == 'plus'
                name = '{iy}_{iz}_{ch}'.format(iy=iy-1,iz=iz-1,ch=wch)
                if options.verbose: 
                    print('at bin {n}'.format(n=name))
                c.SetName ('canv_'+name)
                c.SetTitle('canv_'+name)
                h3_argVsRapVsWPt = h3_argVsRapVsWPtPlus if wch == 'plus' else h3_argVsRapVsWPtMinus
                h_cm = h3_argVsRapVsWPt.ProjectionX(name, iy if iy else 1, iy if iy else nbinsY, iz if iz else 1, iz if iz else nbinsZ)
                #h_cm.SetTitle('cosTheta_'+name)
                ylo = h3_argVsRapVsWPt.GetYaxis().GetBinLowEdge(iy)
                yhi = h3_argVsRapVsWPt.GetYaxis().GetBinUpEdge(iy)
                plo = h3_argVsRapVsWPt.GetZaxis().GetBinLowEdge(iz)
                phi = h3_argVsRapVsWPt.GetZaxis().GetBinUpEdge(iz)
                h_cm.SetTitle('{arg}: W{ch}: y_{{W}} #in [{ylo:.2f},{yhi:.2f}] , p_{{T}}^{{W}} #in [{plo:.2f},{phi:.2f}]'.format(ch=wch, ylo=ylo,yhi=yhi,plo=plo,phi=phi,arg=term) )
                h_cm.GetXaxis().SetTitle(arg.replace(var_cos,'cos #theta^{*}').replace(var_phi, '#phi'))
    
                #h_cm_norm = h_cm.Clone(h_cm.GetName()+'_norm')
                #h_cm_norm.Scale(1./h_cm_norm.Integral())

                parameter = prefactor[term][0]*h_cm.GetMean() + prefactor[term][1]
    
                (h2_rapVsWPtPlus if pos else h2_rapVsWPtMinus).SetBinContent(iy, iz, parameter)

                h_cm.Draw()
                lat.DrawLatex(0.45, 0.68, '{term}: {par:.4f}'.format(term=term,par=parameter))
                if options.verbose:
                    c.SaveAs('{pd}/{term}_argument_{n}.pdf'.format(pd=plotsdir,n=name,term=term))
                    c.SaveAs('{pd}/{term}_argument_{n}.png'.format(pd=plotsdir,n=name,term=term))

    h2_rapVsWPtPlus.Draw('colz')
    c.SaveAs('{pd}/{term}_distribution_plus.pdf'.format(pd=plotsdir,n=name,term=term))
    c.SaveAs('{pd}/{term}_distribution_plus.png'.format(pd=plotsdir,n=name,term=term))
    h2_rapVsWPtMinus.Draw('colz')
    c.SaveAs('{pd}/{term}_distribution_minus.pdf'.format(pd=plotsdir,n=name,term=term))
    c.SaveAs('{pd}/{term}_distribution_minus.png'.format(pd=plotsdir,n=name,term=term))
    all_2d[term+'_plus' ] = h2_rapVsWPtPlus .Clone(term+'_plus' )
    all_2d[term+'_minus'] = h2_rapVsWPtMinus.Clone(term+'_minus')

outfilename = 'allAngularHistos.root' if not options.coefficient else options.coefficient+'CoefficientHistos.root'
outfile = ROOT.TFile('{od}/{ofn}'.format(od=plotsdir,ofn=outfilename),'RECREATE')

all_2d_sym = symmetrizeCoefficients(all_2d)

for key,value in all_2d.items():
    value.Write()
    all_2d_sym[key].Write()

outfile.Close()


