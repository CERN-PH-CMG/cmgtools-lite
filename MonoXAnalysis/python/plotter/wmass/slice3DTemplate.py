#!/usr/bin/env python
import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True

class Template3DSlicer:
    def __init__(self,filename,xy='yx'):
        self.xy = xy
        self.tf = ROOT.TFile.Open(filename)
    def getTemplates(self,var="etaPtY",proc="W",suffixes=['right','left','long']):
        ret = { }
        for s in suffixes:
            hname = var+"_"+proc+"_"+s
            h = self.tf.Get(hname).Clone()
            h.SetDirectory(None)
            if 'z' not in self.xy:
                for b in xrange(1,h.GetZaxis().GetNbins()+1):
                    h.GetZaxis().SetRange(b,b)
                    h2d = h.Project3D("bin_"+str(b-1)+self.xy).Clone()
                    h2d.SetDirectory(None)
                    ret[proc+"_"+s+"_"+"bin_"+str(b-1)] = h2d
            else: 
                print "ERROR: binning variable should be the z one!"
        return ret
    def getXaxis(self,var,proc,suffix):
        hname = var+"_"+proc+"_"+suffix
        h = self.tf.Get(hname).Clone()
        return (h.GetXaxis().GetTitle(), h.GetXaxis().GetNbins(), h.GetXaxis().GetXmin(), h.GetXaxis().GetXmax())
    def getYaxis(self,var,proc,suffix):
        hname = var+"_"+proc+"_"+suffix
        h = self.tf.Get(hname).Clone()
        return (h.GetYaxis().GetTitle(), h.GetYaxis().GetNbins(), h.GetYaxis().GetXmin(), h.GetYaxis().GetXmax())
    def getXY(self,var,proc,suffix):
        xvar = self.getXaxis(var,proc,suffix)
        yvar = self.getYaxis(var,proc,suffix)
        return yvar[0]+":"+xvar[0]+" "+",".join(str(x) for x in xvar[1:])+","+",".join(str(y) for y in yvar[1:])

if __name__ == "__main__":
    testfile = "etaPtY.root"
    ts = Template3DSlicer(testfile,'yx')
    plots = ts.getTemplates("etaPtY","W",['right','left','long'])
    # c1 = ROOT.TCanvas("c1","",600,600)
    # for k,p in plots.iteritems():
    #     if p: 
    #         p.Draw("colz")
    #         c1.SaveAs(k+".png")

    print "Variable X = ", ts.getXaxis("etaPtY","W","long")
    print "Variable Y = ", ts.getYaxis("etaPtY","W","long")
    print "Variable 2D = ", ts.getXY("etaPtY","W","long")
