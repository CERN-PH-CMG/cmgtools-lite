import ROOT


class RooPlotter(object):
    def __init__(self,filename):
        self.fIN=ROOT.TFile(filename)
        self.w=self.fIN.Get("w")
        self.contributions=[]


    def fix(self,var,val):
        self.w.var(var).setVal(val)
        self.w.var(var).setConstant(1)

    def prefit(self,model="s",minos=0,weighted=False,verbose=0):
        self.fitResult = self.w.pdf("model_"+model).fitTo(self.w.data("data_obs"),ROOT.RooFit.NumCPU(8),ROOT.RooFit.SumW2Error(weighted),ROOT.RooFit.Minos(minos),ROOT.RooFit.Verbose(verbose),ROOT.RooFit.Save(1))

    def fitToy(self,model,toyFile,toy):
        self.fT=ROOT.TFile(toyFile)
        self.toydata = self.fT.Get("toy_"+str(toy))
        self.fitResult = self.w.pdf("model_"+model).fitTo(self.toydata,ROOT.RooFit.NumCPU(8))

        
    def addContribution(self,contrib,signal,description,linewidth,lineStyle,lineColor,fillStyle,fillColor,suffix=""):
        self.contributions.append({'name':contrib,'signal':signal,'description':description,'linewidth':linewidth,'linestyle':lineStyle,'linecolor':lineColor,'fillstyle':fillStyle,'fillcolor':fillColor,'suffix':suffix}) 


    def drawStack(self,var,varDesc,cat,cut="",blinded=False,log=False):
        self.canvas=ROOT.TCanvas("c")
        self.canvas.cd()
        #make frame
        self.frame=self.w.var(var).frame()
        #plot data 
        if cut !="":
            dataset=self.w.data("data_obs").reduce(cut)
        else:
            dataset=self.w.data("data_obs").reduce("CMS_channel==CMS_channel::"+cat)

        dataset.plotOn(self.frame,ROOT.RooFit.Cut("CMS_channel==CMS_channel::"+cat),ROOT.RooFit.Name("datapoints"),ROOT.RooFit.Invisible())

        #OK now stack for each curve add all the others
       
        errorVisualized=False

        for i in range(0,len(self.contributions)):
            data = self.contributions[i]
            print 'Plotting ',data['name']
            names=[]
            for j in range(i,len(self.contributions)):
                if self.contributions[j]['signal']:
                    names.append('shapeSig_'+self.contributions[j]['name']+"_"+cat+self.contributions[j]['suffix'])
                else:
                    names.append('shapeBkg_'+self.contributions[j]['name']+"_"+cat+self.contributions[j]['suffix'])

            self.w.pdf("model_s").plotOn(self.frame,ROOT.RooFit.Slice(self.w.cat("CMS_channel"),cat),ROOT.RooFit.Components(",".join(names)),ROOT.RooFit.ProjWData(ROOT.RooArgSet(self.w.var("MLNuJ")),dataset),ROOT.RooFit.Name(data['name']),ROOT.RooFit.Invisible())
            curve=self.frame.getCurve(data['name'])
            curve.SetLineColor(data['linecolor'])
            curve.SetLineWidth(data['linewidth'])
            curve.SetLineStyle(data['linestyle'])
            curve.SetFillColor(data['fillcolor'])
            curve.SetFillStyle(data['fillstyle'])

        
        self.frame.SetXTitle(varDesc)
        self.frame.SetYTitle("Events")

        #legend
        self.legend = ROOT.TLegend(0.62,0.6,0.92,0.90,"","brNDC")
	self.legend.SetBorderSize(0)
	self.legend.SetLineColor(1)
	self.legend.SetLineStyle(1)
	self.legend.SetLineWidth(1)
	self.legend.SetFillColor(0)
	self.legend.SetFillStyle(0)
	self.legend.SetTextFont(42)

        for c in self.contributions:
            name=c['name']
            desc=c['description']
            curve=self.frame.getCurve(name)
            self.legend.AddEntry(curve,desc,"f")
           


        self.frame.SetTitle("")    
        self.frame.SetLabelSize(0.04,"X")    
        self.frame.SetLabelSize(0.04,"Y")    
        self.frame.SetTitleSize(0.05,"X")    
        self.frame.SetTitleSize(0.05,"Y")    
        self.frame.SetTitleOffset(0.90,"X")    
        self.frame.SetTitleOffset(0.93,"Y")    

        if log:
            self.frame.GetYaxis().SetRangeUser(1e-1,1e+4)
        self.frame.Draw()       
        for c in self.contributions:
            name=c['name']
            curve=self.frame.getCurve(name)
            curve.Draw("Fsame")
            curve.Draw("Lsame")


        if not blinded:
            hist=self.frame.getHist("datapoints")
            hist.Draw("Psame")

        self.legend.Draw()    
        if log:
            self.canvas.SetLogy(1)
        self.canvas.RedrawAxis()
        self.canvas.Update()

        

    
    

        
        
        
