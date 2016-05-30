#!/usr/bin/env python
import os, glob, sys, math
from array import array
from ROOT import *
def GetContours(g, color, style):
    contours = [1.0]
    g.GetHistogram().SetContour(1,array('d',contours));
    g.Draw("cont z list"); 
    contLevel = g.GetContourList(1.0);
    max_points = -1
    for cont in contLevel:
        n_points = cont.GetN()
        if n_points > max_points:
            max_points = n_points
            cont.SetLineColor(color)
            cont.SetLineStyle(style)
            cont.SetLineWidth(5)
            out = cont
        
            #cont.Draw("same")

    return out


def getxsecGlu():
    xsecGlu = {} # dict for xsecs 
    xsecFile = "../../../../../SUSYAnalysis/python/tools/glu_xsecs_13TeV.txt"

    with open(xsecFile,"r") as xfile:                            
        lines = xfile.readlines() 
        print 'Found %i lines in %s' %(len(lines),xsecFile)
        for line in lines:
            if line[0] == '#': continue
            (mGo,xsec,err) = line.split()
            xsecGlu[int(mGo)] = (float(xsec),float(err))
            #print 'Importet', mGo, xsec, err, 'from', line 
    return xsecGlu

if __name__ == "__main__":

    ## remove '-b' option
    if '-b' in sys.argv:
        sys.argv.remove('-b')
        _batchMode = True

    if len(sys.argv) > 1:
        pattern = sys.argv[1]
        print '# pattern is', pattern
    else:
        print "No pattern given!"
        exit(0)

    ## Create Yield Storage
    
#    pattern = "datacardsABCD_2p1bins_fullscan2"
#    os.chdir(pattern)
    dirList = glob.glob('T1tttt*')
    samples = [x[x.find('/')+1:] for x in dirList]    
    xsecGlu = getxsecGlu()
    if 1==1:
        fileList = glob.glob(pattern+'/limitOutput/*root')
        hexp = TH2F('hexp','hexp', 81,-12.5, 2012.5, 81, -12.5, 2012.5)
        hexpdown = TH2F('hexpdown','hexpdown', 81,-12.5, 2012.5, 81, -12.5, 2012.5)
        hexpup = TH2F('hexpup','hexpup', 81,-12.5, 2012.5, 81, -12.5, 2012.5)
        hobs = TH2F('hobs','hobs', 81,-12.5, 2012.5, 81, -12.5, 2012.5)
        vmx=[]; vmy = []; vxsec = []; vobs = [];  vobsup = []; vobsdown = []; vexp = []; vup = []; vdown = []; vlim = [];
        for x in fileList:
            mGo = int(x[x.find('_mGo')+4:x.find('_mLSP')])
            mLSP = int(x[x.find('_mLSP')+5:x.find('.As')])
            f = TFile.Open(x, 'read')
            t = f.Get('limit')
            xsec = xsecGlu[mGo][0]
            theorySys = xsecGlu[mGo][1]
            #print theorySys
            rExp = 0
            rObs = 0
            rExp1SigmaDown = 0
            rExp1SigmaUp = 0
            factor = 1.0
            if mGo < 1400:
                factor = 100.0
            for entry in t:
                q = entry.quantileExpected
                if q == 0.5: rExp = entry.limit/factor
                if q == -1: rObs = entry.limit/factor
                if q < 0.4 and q > 0.14 : rExp1SigmaDown = entry.limit/factor
                if q < 0.14 : rExp2SigmaDown = entry.limit/factor
                if q > 0.6 and q < 0.9 : rExp1SigmaUp = entry.limit/factor
                if q > 0.9 : rExp2SigmaUp = entry.limit/factor

            hexp.Fill(mGo,mLSP,rExp)
            hexpdown.Fill(mGo,mLSP,rExp1SigmaDown)
            hexpup.Fill(mGo,mLSP,rExp1SigmaUp)
            hobs.Fill(mGo,mLSP,rObs)
            vmx.append(mGo)
            vmy.append(mLSP)
            vxsec.append(xsec)
            vlim.append(xsec * rObs)
            vobs.append(rObs)
            vobsup.append(rObs*(1+theorySys/100.0))
            vobsdown.append(rObs*(1-theorySys/100.0))
            vexp.append(rExp)
            vup.append(rExp1SigmaUp)
            vdown.append(rExp1SigmaDown)
            f.Close()

        hexp.SaveAs(pattern+'/testexp_'+pattern+'.root')
        hobs.SaveAs(pattern+'/testobs_'+pattern+'.root')
        aexp = array("d", vexp) 
        alim = array("d", vlim) 
        aup = array("d", vup) 
        adown = array("d", vdown) 
        aobs = array("d", vobs) 
        aobsup = array("d", vobsup) 
        aobsdown = array("d", vobsdown) 
        amx = array("d", vmx) 
        amy = array("d", vmy) 

        glim = TGraph2D("glim", "Cross-section limt", len(vlim), amx, amy, alim)
        gexp = TGraph2D("gexp", "Expected Limit", len(vexp), amx, amy, aexp)
        gup = TGraph2D("gup", "Expected Limit 1sigma up", len(vup), amx, amy, aup)
        gdown = TGraph2D("gdown", "Expected Limit 1sigma down", len(vdown), amx, amy, adown)
        gobs = TGraph2D("gobs", "Observed Limit", len(vobs), amx, amy, aobs)
        gobsup = TGraph2D("gobsup", "theory 1sigma up", len(vobsup), amx, amy, aobsup)
        gobsdown = TGraph2D("gobsdown", "theory 1sigma down", len(vobsdown), amx, amy, aobsdown)
        c = TCanvas("c","c",800,600)
        
        xmin = min(vmx)
        xmax = max(vmx)
        ymin = min(vmy)
        ymax = max(vmy)
        bin_size = 12.5;
        nxbins = max(1, min(500, (math.ceil((xmax-xmin)/bin_size))))
        nybins = max(1, min(500, (math.ceil((ymax-ymin)/bin_size))))
        glim.SetNpx(int(nxbins))
        glim.SetNpy(int(nybins))
        
        
        cexp = GetContours(gexp, 2,1)
        cup = GetContours(gup,2,2)
        cdown = GetContours(gdown,2,2)
        cobs = GetContours(gobs,1,1)
        cobsup = GetContours(gobsup,1,2)
        cobsdown = GetContours(gobsdown,1,2)

        hlim = glim.GetHistogram()
        hlim.SetTitle(";m_{gluino} [GeV];m_{LSP} [GeV]");
        hlim.Draw("colz")
        cexp.Draw("same")
        cup.Draw("same")
        cdown.Draw("same")
        cobs.Draw("same")
        cobsup.Draw("same")
        cobsdown.Draw("same")
        flimit = TFile(pattern+"/limit_scan.root","recreate")
        #ONLY do for T5tttt
        hlim.SetBinContent(11,37,0.27)
        hlim.SetBinError(11,37,0.27)
        hlim.Write("hXsec_exp_corr");
        cobs.Write("graph_smoothed_Obs");
        cobsup.Write("graph_smoothed_ObsP");
        cobsdown.Write("graph_smoothed_ObsM");
        cexp.Write("graph_smoothed_Exp");
        cup.Write("graph_smoothed_ExpP");
        cdown.Write("graph_smoothed_ExpM");
        hexp.Write("hexp")
        hexpup.Write("hexpup")
        hexpdown.Write("hexpdown")
        hobs.Write("hobs")
        c.SaveAs(pattern+'/canvas_'+pattern+'.root')


    
