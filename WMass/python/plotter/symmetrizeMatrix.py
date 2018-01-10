import ROOT

ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)

ROOT.gStyle.SetPalette(1)

infile = ROOT.TFile('multidimfit.root', 'read')

fitresult = infile.Get('fit_mdf')

h2_corr = fitresult.correlationHist()

c = ROOT.TCanvas()

h2_corr.Draw('colz')
c.SaveAs('./correlationMatrix_FR1p01_otherbkgnuis_original.pdf')
c.SaveAs('./correlationMatrix_FR1p01_otherbkgnuis_original.png')

bins = {}
labels = []

for ix in range(1,h2_corr.GetXaxis().GetNbins()+1):
    labels.append(h2_corr.GetXaxis().GetBinLabel(ix))

h2_new = h2_corr.Clone('correlationMatrix_FR1p01_otherbkgnuis')
h2_new.Reset()

#l_sorted = sorted(labels, key = lambda x: int(x.split('_')[-1]) if not (x =='Wpt' or x =='longNuisance') else x[-1] )
#l_sorted_new  = [l for l in l_sorted if '_right_' in l]
#l_sorted_new += [l for l in l_sorted if '_left_' in l]
#l_sorted_new += [l for l in l_sorted if '_long_' in l]
#l_sorted_new += ['CMS_We_FRe_norm', 'CMS_We_VV', 'CMS_We_lepEff','lumi_8TeV', 'norm_long_Wp_el']
#l_sorted_new += ['longNuisance']


l_sorted_new = [
'norm_Wp_right_Wp_el_Ybin_3_12',
'norm_Wp_right_Wp_el_Ybin_4_11',
'norm_Wp_right_Wp_el_Ybin_5_10',
'norm_Wp_right_Wp_el_Ybin_6_9',
'norm_Wp_right_Wp_el_Ybin_7_8',
'norm_Wp_left_Wp_el_Ybin_7_8',
'norm_Wp_left_Wp_el_Ybin_6_9',
'norm_Wp_left_Wp_el_Ybin_5_10',
'norm_Wp_left_Wp_el_Ybin_4_11',
'norm_Wp_left_Wp_el_Ybin_3_12',
'CMS_We_FRe_norm',
'CMS_We_VV',
'CMS_We_elescale',
'CMS_We_lepEff',
'lumi_8TeV',   
'norm_long_Wp_el'   ]


for il,l in enumerate(l_sorted_new):
    new_l = l.lstrip('norm_').replace('right','WR').replace('left','WL').replace('Ybin_','')
    new_l = new_l.replace('Wp_WL_Wp','WpL')
    new_l = new_l.replace('Wp_WR_Wp','WpR')
    new_l = new_l.replace('Wp_WL_Wp','WpL')
    new_l = new_l.replace('Wp_WR_Wp','WpR')
    #print(new_l)
    h2_new.GetXaxis().SetBinLabel(il+1, new_l)
    h2_new.GetYaxis().SetBinLabel(il+1, new_l)
    for il2,l2 in enumerate(l_sorted_new):
        binx = h2_corr.GetXaxis().FindBin(l)
        biny = h2_corr.GetYaxis().FindBin(l2)
        new_l2 = l2.lstrip('norm_').replace('right','WR ').replace('left','WL ')
        h2_new.SetBinContent(il+1, il2+1, h2_corr.GetBinContent(binx, biny))

h2_new.Draw('colz')
c.SaveAs('./correlationMatrix_FR1p01_otherbkgnuis_new.pdf')
c.SaveAs('./correlationMatrix_FR1p01_otherbkgnuis_new.png')


#print(labels)
#print(h2_corr.GetXaxis().GetBinLabel(1))
#print(h2_corr.GetYaxis().GetBinLabel(1))



#fit_mdf->correlationHist()->Draw("colz")
