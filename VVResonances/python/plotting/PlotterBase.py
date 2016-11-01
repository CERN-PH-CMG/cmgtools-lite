import ROOT
class PlotterBase(object):

    def __init__(self):
        self.fillstyle=1001
        self.linestyle=1
        self.linecolor=1
        self.linewidth=2
        self.fillcolor=ROOT.kOrange-3
        self.markerstyle=20
        self.corrFactors=[]

    def addCorrectionFactor(self,value,model):
        corr=dict()
        corr['value']=value
        corr['model']=model
        self.corrFactors.append(corr)

    def setLineProperties(self,linestyle,linecolor,linewidth):
        self.linestyle=linestyle
        self.linecolor=linecolor
        self.linewidth=linewidth 

    def setFillProperties(self,fillstyle,fillcolor):
        self.fillstyle=fillstyle
        self.fillcolor=fillcolor

    def setMarkerProperties(self,markerstyle):
        self.markerstyle=markerstyle

    def drawTH2(self,var,cuts,lumi,binsx,minx,maxx,binsy,miny,maxy,titlex = "",unitsx = "",titley="",unitsy="", drawStyle = "COLZ"):
        return None

    def drawTH3(self,var,cuts,lumi,binsx,minx,maxx,binsy,miny,maxy,binsz,minz,maxz,titlex = "",unitsx = "",titley="",unitsy="", drawStyle = "COLZ"):
        return None

    def drawTH1(self,var,cuts,lumi,bins,min,max,titlex = "",units = "",drawStyle = "HIST"):
        return None

    def makeDataSet(self,var,cut,maxN):
        return None



    def drawTH2Keys(self,var,cuts,binsx,minx,maxx,binsy,miny,maxy):
        print 'making  Keys dataset'
        data=self.makeDataSet(var,cuts,-1)
        print 'dataset created with entries=',data.numEntries()

        varx=var.split(',')[0]
        vary=var.split(',')[1]

        data.get().find(varx).setMax(maxx)
        data.get().find(varx).setMin(minx)

        data.get().find(vary).setMax(maxy)
        data.get().find(vary).setMin(miny)

        argset=ROOT.RooArgList()
        argset.add(data.get().find(varx))
        argset.add(data.get().find(vary))
        keys=ROOT.RooNDKeysPdf("keys","keys",argset,data)

        histo=self.drawTH2(vary+":"+varx,cuts,"1",binsx,minx,maxx,binsy,miny,maxy)
        for i in range(1,histo.GetNbinsX()+1):
            for j in range(1,histo.GetNbinsY()+1):
                bin=histo.GetBin(i,j)
                x=histo.GetXaxis().GetBinCenter(i)
                y=histo.GetYaxis().GetBinCenter(j)
                argset.find(varx).setVal(x)
                argset.find(vary).setVal(y)
                histo.SetBinContent(bin,keys.getVal())

        #histo=keys.createHistogram(var,binsx,binsy)
#        import pdb;pdb.set_trace()

        return histo

    def drawTH2KeysFast(self,var,cuts,binsx,minx,maxx,binsy,miny,maxy,BINSCALE =5):
        histo=self.drawTH2(var,cuts,"1",binsx*BINSCALE,minx,maxx,binsy*BINSCALE,miny,maxy)

        varx=var.split(':')[1]
        vary=var.split(':')[0]

        w=ROOT.RooWorkspace("w")
        w.factory(varx+"[{x},{X}]".format(x=minx,X=maxx))
        w.factory(vary+"[{y},{Y}]".format(y=miny,Y=maxy))
        w.factory("weight[-1e+15,1e+15]")

        datahist=ROOT.RooDataHist("data","data",ROOT.RooArgList(w.var(varx),w.var(vary)),histo)
        
        dataset = ROOT.RooDataSet("dataset","dataset",ROOT.RooArgSet(w.var(varx),w.var(vary),w.var("weight")),"weight")
        
        for i in range(0,datahist.numEntries()):
            line=datahist.get(i)
            dataset.add(line,datahist.weight())
            

        keys=ROOT.RooNDKeysPdf("keys","keys",ROOT.RooArgList(w.var(varx),w.var(vary)),dataset)       
        return keys.createHistogram(varx+','+vary,binsx,binsy)

    

