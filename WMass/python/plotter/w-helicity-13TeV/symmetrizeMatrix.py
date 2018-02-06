import ROOT, datetime

ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)

ROOT.gStyle.SetPalette(1)

date = datetime.date.today().isoformat()

from optparse import OptionParser
parser = OptionParser(usage='%prog [options] ')
parser.add_option('-i','--infile', dest='infile', default='', type='string', help='file with fitresult')
parser.add_option('-o','--outdir', dest='outdir', default='', type='string', help='outdput directory to save the matrix')
parser.add_option(     '--suffix', dest='suffix', default='', type='string', help='suffix for the correlation matrix')
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
pars_l   = list(p for p in hel_pars if 'left' in p)
pars_l = sorted(pars_l, key = lambda x: int(x.split('_')[-2]) )
pars_r   = list(p for p in hel_pars if 'right' in p)
pars_r = sorted(pars_r, key = lambda x: int(x.split('_')[-2]), reverse=True)

l_sorted_new = pars_l + pars_r + long_par + rest

for il,l in enumerate(l_sorted_new):
    new_l = l.lstrip('norm_').replace('right','WR').replace('left','WL').replace('Ybin_','')
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

