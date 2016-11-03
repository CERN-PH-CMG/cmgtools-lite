from CMGTools.VVResonances.plotting.TreePlotter import *



class EventSampler(object):
    def __init__(self,tag,luminosity,randomizer,filename,cut,normalizationSyst=0.00001,scaleInfo ={} ,smearingInfo={}):
        plotter=TreePlotter(filename+'.root','tree')
        plotter.setupFromFile(filename+'.pck')
        plotter.addCorrectionFactor('genWeight','tree')
        plotter.addCorrectionFactor('xsec','tree')
        plotter.addCorrectionFactor('puWeight','tree')
        histo = plotter.drawTH1("0.5",cut,str(luminosity),1,0,1)
        self.scaleInfo=scaleInfo
        self.smearingInfo=smearingInfo
        self.random=randomizer
        self.cache=ROOT.TFile("cache_"+filename.split('/')[1]+"_"+tag+".root","RECREATE")
        self.cache.cd()
        self.tree=plotter.tree.CopyTree(cut)
        self.entries = self.tree.GetEntries()
        self.integral=histo.Integral()
        if self.integral>100:
            self.normalizationStat=ROOT.TF1("poisson","TMath::Poisson(x,{mean})".format(mean=self.integral),0,10*self.integral)
        else:
            self.normalizationStat=ROOT.TF1("poisson","TMath::Poisson(x,{mean})".format(mean=self.integral),0,500)
        if normalizationSyst>0.01:    
            self.normalizationSyst=ROOT.TF1("gauss","TMath::Gaus(x,0.0,{sigma})".format(sigma=normalizationSyst),-10,10)
        else:
            self.normalizationSyst=None


    def randomEvent(self):
        i = int(self.random.Rndm()*self.entries)
        self.tree.GetEntry(i)


        
    def makeHistogram2D(self,varx,vary,binsx,minx,maxx,binsy,miny,maxy):
        h=ROOT.TH2D("tmpH","tmpH",binsx,minx,maxx,binsy,miny,maxy)
        #find statistical term


        if self.normalizationSyst==None:
            events=(self.normalizationStat.GetRandom())
        else:
            events=(self.normalizationStat.GetRandom()*(1+self.normalizationSyst.GetRandom()))
        print 'Events',events

        events=int(events)    
        for i in range(0,events):
            self.randomEvent()
            x=getattr(self.tree,varx)[0]
            y=getattr(self.tree,vary)[0]
#            print  'event',x,y
            if varx in self.scaleInfo.keys():
                x=x*(1+self.scaleInfo[varx])
            if varx in self.smearingInfo.keys():
                x=x*(1+self.random.Gaus(0.0,self.smearingInfo(varx)))
            if vary in self.scaleInfo.keys():
                y=y*(1+self.scaleInfo[vary])
            if vary in self.smearingInfo.keys():
                y=y*(1+self.random.Gaus(0.0,self.smearingInfo(vary)))
            weight=self.tree.genWeight
            if weight>0:
                h.Fill(x,y)
            else:
                h.Fill(x,y,-1.0)
        return h    
                
        

        
    
    

