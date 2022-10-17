from ROOT import TFile, TTree, TCanvas, TH1F, kBlack, kBlue, kRed, kGreen, TLegend, gROOT

gROOT.SetBatch()

thevars = {'Wmass': [200, 0., 200.],
           'pTHvis': [200, 0., 200.], 
           'visHmass': [200, 0., 200.],
       }

f_new_constr = TFile.Open('/nfs/user/pvischia/tth/v6/NanoTrees_TTH_091019_v6pre_skim2lss_tight/2016//6_higgsDiffRecoTTH/TTHnobb_fxfx_Friend.root'                  , 'read')  
f_new_nocons = TFile.Open('/nfs/user/pvischia/tth/v6/NanoTrees_TTH_091019_v6pre_skim2lss_tight/2016//6_higgsDiffRecoTTH_noWmassConstraint/TTHnobb_fxfx_Friend.root', 'read')
f_old_constr = TFile.Open('/nfs/user/elfaham/104X/v6/2016/2lss_diff_NoTop-tagged/TTHnobb_fxfx_Friend.root'                                                   , 'read') 
f_old_derekk = TFile.Open('/home/ucl/cp3/dcransha/ttHdiff/attempt1/CMSSW_10_4_0/src/CMGTools/TTHAnalysis/macros/diff/2lss_diff_Top-tagged/fullSuite/2016/TTHnobb_fxfx_Friend_DefaultModule_NoTopMediumBottomVeto_2016.root', 'read')

t_new_constr = f_new_constr.Get('Friends')
t_new_nocons = f_new_nocons.Get('Friends')
t_old_constr = f_old_constr.Get('Friends')
t_old_derekk = f_old_derekk.Get('Friends')

print('t_new_constr ', t_new_constr.GetEntries())
print('t_new_nocons ', t_new_nocons.GetEntries())
print('t_old_constr ', t_old_constr.GetEntries())
print('t_old_derekk ', t_old_derekk.GetEntries())


t_new_diff = f_new_constr.Get('Friends')
t_new_diff.AddFriend('alt=Friends', '/home/ucl/cp3/dcransha/ttHdiff/attempt1/CMSSW_10_4_0/src/CMGTools/TTHAnalysis/macros/diff/2lss_diff_Top-tagged/fullSuite/2016/TTHnobb_fxfx_Friend_DefaultModule_NoTopMediumBottomVeto_2016.root')

for var, ranges in thevars.items():
    nbins, xlow, xhigh = ranges
    print(var, nbins, xlow, xhigh)
    c = TCanvas(var,var)
    c.cd()
    h_new_constr = TH1F('h%s_new_constr'%var, var, nbins, xlow, xhigh)
    h_new_nocons = TH1F('h%s_new_nocons'%var, var, nbins, xlow, xhigh)
    h_old_constr = TH1F('h%s_old_constr'%var, var, nbins, xlow, xhigh)
    h_old_derekk = TH1F('h%s_old_derekk'%var, var, nbins, xlow, xhigh)
    
    t_new_constr.Draw('Hreco_%s>>h%s_new_constr'%(var,var))
    t_new_nocons.Draw('Hreco_%s>>h%s_new_nocons'%(var,var))
    t_old_constr.Draw('Hreco_%s>>h%s_old_constr'%(var,var))
    t_old_derekk.Draw('Hreco_%s>>h%s_old_derekk'%(var,var))

    h_new_constr.Draw('hist')
    h_new_nocons.Draw('hist same')
    h_old_constr.Draw('hist same')
    h_old_derekk.Draw('hist same')

    h_new_constr.SetLineWidth(2)
    h_new_nocons.SetLineWidth(2)
    h_old_constr.SetLineWidth(2)
    h_old_derekk.SetLineWidth(2)

    h_new_constr.SetLineColor(kBlack)
    h_new_nocons.SetLineColor(kBlue)
    h_old_constr.SetLineColor(kRed)
    h_old_derekk.SetLineColor(kGreen+2)
    
    leg = TLegend(0.7,0.8, 0.9,0.9)
    leg.AddEntry(h_new_constr, 'New, with W constraint', 'l')
    leg.AddEntry(h_new_nocons, 'New, with no W constraint', 'l')
    leg.AddEntry(h_old_constr, 'Hesham, with W constraint', 'l')
    leg.AddEntry(h_old_derekk, 'Derek, with W constraint', 'l')
    leg.Draw()

    c.Print('compold/%s.png'%var)


    h_diff = TH1F('h%sdiff'%var, var, 100, -5, 5)
    t_new_diff.Draw('Hreco_%s-alt.Hreco_%s>>h%sdiff'%(var,var,var))
    h_diff.Draw('hist')
    h_diff.SetLineWidth(2)
    h_diff.SetLineColor(kBlack)
    h_diff.SetTitle('%s(new)-%s(old)'%(var,var))
    c.Print('compold/%s_diff.png'%var)
