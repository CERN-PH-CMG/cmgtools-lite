import gzip, pickle
import ROOT as r 
import numpy as np 
import math 
r.gROOT.SetBatch(True)

def fillROOTHistoWithStupidHisto(roothist, stupid_hist):
    axis1 = stupid_hist.axes()[0].name
    bins1 = stupid_hist.axis(axis1).edges()
    axis2 = stupid_hist.axes()[1].name
    bins2 = stupid_hist.axis(axis2).edges()
    
    thehist=r.TH2F(roothist, '', len(bins1)-1, bins1, len(bins2)-1, bins2 )
    matrix=stupid_hist.values()[()]
    for iy, ix in np.ndindex(matrix.shape):
        thebin=thehist.GetBin(iy+1,ix+1)
        thehist.SetBinContent(thebin, matrix[iy,ix])
    thehist.GetXaxis().SetTitle(axis1)
    thehist.GetYaxis().SetTitle(axis2)
    thehist.Draw("colz text")
    return thehist

def hypoth(a,b):
    return math.sqrt(a**2+b**2)


for year in '2016APV,2016,2017,2018'.split(','): 
    with gzip.open('/work/sesanche/EFT_analysis/tmp/topcoffea/topcoffea/data/triggerSF/triggerSF_%s.pkl.gz'%year) as fin: hin = pickle.load(fin)

    tf=r.TFile.Open("triggerScaleFactors_%s.root"%year,'recreate')

    for chan in hin:
        for subchan in hin[chan]:
            hin[chan][subchan]['hdn']
            den_data=fillROOTHistoWithStupidHisto('data_den_%s_%s'%(chan,subchan), hin[chan][subchan]['hdd'])
            num_data=fillROOTHistoWithStupidHisto( 'data_num_%s_%s'%(chan,subchan), hin[chan][subchan]['hdn'])
    
            den_mc=fillROOTHistoWithStupidHisto('mc_den_%s_%s'%(chan,subchan), hin[chan][subchan]['hmd'])
            num_mc=fillROOTHistoWithStupidHisto( 'mc_num_%s_%s'%(chan,subchan), hin[chan][subchan]['hmn'])
            
            data_eff=r.TEfficiency( num_data, den_data)
            mc_eff  =r.TEfficiency( num_mc, den_mc)
    
            sf=num_mc.Clone('sf_%s_%s'%(chan,subchan))
            sf.Reset()
            for i in range(den_data.GetXaxis().GetNbins()):
                for j in range(den_data.GetYaxis().GetNbins()):
                    thebin=den_data.GetBin(i+1,j+1)
                    sf.SetBinContent( thebin, data_eff.GetEfficiency(thebin)/mc_eff.GetEfficiency(thebin) if mc_eff.GetEfficiency(thebin) else 0 )
                    dataerr=max(data_eff.GetEfficiencyErrorUp(thebin), data_eff.GetEfficiencyErrorLow(thebin))
                    mcerr=max(mc_eff.GetEfficiencyErrorUp(thebin), mc_eff.GetEfficiencyErrorLow(thebin))
                    sf.SetBinError  ( thebin, hypoth( dataerr/mc_eff.GetEfficiency(thebin), mcerr*data_eff.GetEfficiency(thebin)/mc_eff.GetEfficiency(thebin)**2) if mc_eff.GetEfficiency(thebin) else 0  )
    
            tf.WriteTObject( sf, 'sf_%s_%s'%(chan,subchan))
