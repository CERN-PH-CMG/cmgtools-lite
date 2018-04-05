import ROOT

wmfile = ROOT.TFile('/afs/cern.ch/user/m/mdunser/www/private/w-helicity-13TeV/helicityTemplates/2017-12-07/wminus_etaPtY.root','read')
wpfile = ROOT.TFile('/afs/cern.ch/user/m/mdunser/www/private/w-helicity-13TeV/helicityTemplates/2017-12-07/wplus_etaPtY.root' ,'read')

histos = []

h3_wm_l = wmfile.Get('wminus_etaPtY_Wm_left' ); histos.append(h3_wm_l)
h3_wm_r = wmfile.Get('wminus_etaPtY_Wm_right'); histos.append(h3_wm_r)
h3_wm_0 = wmfile.Get('wminus_etaPtY_Wm_long' ); histos.append(h3_wm_0)
                                                              
h3_wp_l = wpfile.Get('wplus_etaPtY_Wp_left' ); histos.append(h3_wp_l)
h3_wp_r = wpfile.Get('wplus_etaPtY_Wp_right'); histos.append(h3_wp_r)
h3_wp_0 = wpfile.Get('wplus_etaPtY_Wp_long' ); histos.append(h3_wp_0)

maxhistm = h3_wm_l
maxhistp = h3_wp_r

nbins_yw = h3_wm_l.GetNbinsZ()

ROOT.gStyle.SetOptStat(0)
##ROOT.gStyle.SetPadRightMargin(ROOT.gStyle.GetPadRightMargin()*0.8)
ROOT.gStyle.SetPadRightMargin(0.15)
canv = ROOT.TCanvas()
ROOT.gROOT.SetBatch()


for h3 in histos:
    print 'at histo', h3.GetName()
    for ibin in range(1,nbins_yw+1):
        h3.GetZaxis().SetRange(ibin, ibin)
        h2_tmp = h3.Project3D('yx')
        isp = 'plus' in h3.GetName()
        pol = h3.GetName().split('_')[-1]
        ymin = h3.GetZaxis().GetBinLowEdge(ibin)
        ymax = h3.GetZaxis().GetBinUpEdge(ibin)

        title_tmp = '{ch} {pol}: {ymin:.2f} < Y_{{W}} < {ymax:.2f}'.format(ch = ('W^{+}' if isp else 'W^{-}'), ymin=ymin, ymax=ymax, pol=pol)
        h2_tmp.SetTitle(title_tmp)
        name_tmp = 'w{ch}_{pol}_bin{ibin}'.format(ch='plus' if isp else 'minus', ibin=ibin, pol=pol)
        h2_tmp.GetXaxis().SetTitle('#eta^{lep}')
        h2_tmp.GetYaxis().SetTitle('p_{T}^{lep}')

        h2_tmp.GetXaxis().SetTitleOffset(0.70)
        h2_tmp.GetYaxis().SetTitleOffset(0.70)

        ##(maxhistp if isp else maxhistm).GetZaxis().SetRange(ibin, ibin)
        ##h2_max_tmp = (maxhistp if isp else maxhistm).Project3D('yx')
    
        ##zmax = (h2_max_tmp).GetMaximum()
    
        ##h2_tmp.GetZaxis().SetRangeUser(0., zmax*1.0)

        h2_tmp.Draw('colz')
        canv.SaveAs('/afs/cern.ch/user/m/mdunser/www/private/w-helicity-13TeV/templatesForMarco/{name}.pdf'.format(name=name_tmp))
