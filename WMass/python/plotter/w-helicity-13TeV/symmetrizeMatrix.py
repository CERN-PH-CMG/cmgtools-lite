import ROOT, datetime
from array import array

ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)

ROOT.gStyle.SetPalette(1)

date = datetime.date.today().isoformat()

from optparse import OptionParser
parser = OptionParser(usage='%prog [options] ')
parser.add_option('-i','--infile', dest='infile', default='', type='string', help='file with fitresult')
parser.add_option('-o','--outdir', dest='outdir', default='', type='string', help='outdput directory to save the matrix')
parser.add_option(     '--suffix', dest='suffix', default='', type='string', help='suffix for the correlation matrix')
parser.add_option(     '--Ybins' , dest='Ybins' , default='', type='string', help='binning in Y')
parser.add_option(     '--dc'    , dest='dc'    , default='', type='string', help='the corresponding datacard (for the rates)')
(options, args) = parser.parse_args()

##infile = ROOT.TFile('/afs/cern.ch/work/e/emanuele/wmass/fit/CMSSW_8_1_0/src/multidimfit.root','read')
infile = ROOT.TFile(options.infile, 'read')


if 'multidimfit' in options.infile:
    fitresult = infile.Get('fit_mdf')
else:
    fitresult = infile.Get('fit_s')

h2_corr = fitresult.correlationHist()

c = ROOT.TCanvas()

h2_corr.Draw('colz')
for ext in ['png', 'pdf']:
    c.SaveAs('{od}/corrMatrix_{date}_{suff}_original.{ext}'.format(od=options.outdir, date=date, suff=options.suffix, ext=ext))

bins = {}
labels = []

for ix in range(1,h2_corr.GetXaxis().GetNbins()+1):
    labels.append(h2_corr.GetXaxis().GetBinLabel(ix))

h2_new = h2_corr.Clone('correlationMatrix_symmetric')
h2_new.Reset()

## some more ROOT "magic"
parlist = fitresult.floatParsFinal()
l_params = list(parlist.at(i).GetName() for i in range(len(parlist)))

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
    c.SaveAs('{od}/corrMatrix_{date}_{suff}_symmetric.{ext}'.format(od=options.outdir, date=date, suff=options.suffix, ext=ext))

if options.Ybins:
    ybins = list(float(i) for i in options.Ybins.split(','))
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

    if not len(ybins)-1 == sorted_rap: 
        print 'SOMETHING WENT TERRIBLY WRONG'

    ## get the rates and processes from the datacard. they're necessarily in the same order
    dcfile = open(options.dc, 'r')
    dclines = dcfile.readlines()
    procline = list(line for line in dclines if line.startswith('process')); procline = procline[0]; procs = procline.split()
    rateline = list(line for line in dclines if line.startswith('rate'   )); rateline = rateline[0]; rates = rateline.split()
    
    arr_val = array('f', [])
    arr_ehi = array('f', [])
    arr_elo = array('f', [])
    arr_rap = array('f', [])
    arr_rlo = array('f', [])
    arr_rhi = array('f', [])

    totalrate = 0.
    for p in sorted_rap:
        tmp_procname = '_'.join(p.split('_')[1:-1])
        totalrate += float(rates[procs.index(tmp_procname)])
    #totalrate=1.

    for ip,p in enumerate(sorted_rap):
        tmp_par = fitresult.floatParsFinal().find(p) if p in l_sorted_new else fitresult.constPars().find(p)
        tmp_procname = '_'.join(p.split('_')[1:-1])
        tmp_rate = float(rates[procs.index(tmp_procname)])
        arr_val.append(tmp_rate/totalrate*tmp_par.getVal())
        arr_ehi.append(tmp_rate/totalrate*abs(tmp_par.getAsymErrorHi()))
        arr_elo.append(tmp_rate/totalrate*abs(tmp_par.getAsymErrorLo()))
        arr_rap.append((ybins[ip]+ybins[ip+1])/2.)
        arr_rlo.append(abs(ybins[ip]-arr_rap[-1]))
        arr_rhi.append(abs(ybins[ip]-arr_rap[-1]))

    graph = ROOT.TGraphAsymmErrors(len(arr_val), arr_rap, arr_val, arr_rlo, arr_rhi, arr_elo, arr_ehi)
    graph.SetTitle('W^{+}: Y_{W}')
    graph.SetFillColor(ROOT.kBlue+1)
    graph.SetFillStyle(3001)
    #graph.GetXaxis().SetRangeUser(ybins[0],ybins[-1])
    graph.GetXaxis().SetRangeUser(-4.,4.)
    graph.GetXaxis().SetTitle('Y_{W}')
    graph.GetYaxis().SetTitle('N_{events}/N_{total}')
    c2 = ROOT.TCanvas()
    graph.Draw('a2')
    for ext in ['png', 'pdf']:
        c2.SaveAs('{od}/rapidityDistribution_{date}_{suff}.{ext}'.format(od=options.outdir, date=date, suff=options.suffix, ext=ext))

    
    

    
    
