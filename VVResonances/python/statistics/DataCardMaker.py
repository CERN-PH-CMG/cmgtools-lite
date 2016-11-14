import ROOT
ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")
import json


class DataCardMaker:
    def __init__(self,finalstate,category,period,luminosity=1.0,physics="LJ"):
        self.physics=physics
        self.finalstate=finalstate
        self.category=category
        self.period=period
        self.contributions=[]
        self.systematics=[]

        self.tag=self.physics+"_"+finalstate+"_"+category+"_"+period
        self.rootFile = ROOT.TFile("datacardInputs_"+self.tag+".root","RECREATE")
        self.rootFile.cd()
        self.w=ROOT.RooWorkspace("w","w")
        self.luminosity=luminosity
        self.w.factory(self.physics+"_"+period+"_lumi["+str(luminosity)+"]")
        if period=='8TeV':
            self.sqrt_s=8000.0
        if period=='13TeV':
            self.sqrt_s=13000.0


    def addSystematic(self,name,kind,values,addPar = ""):
        self.systematics.append({'name':name,'kind':kind,'values':values })


    def addMVVSignalParametricShape(self,name,variable,jsonFile,scale ={},resolution={}):
        self.w.factory("MH[2000]")
        self.w.var("MH").setConstant(1)

        scaleStr='0'
        resolutionStr='0'

        scaleSysts=[]
        resolutionSysts=[]
        for syst,factor in scale.iteritems():
            self.w.factory(syst+"[0,-0.1,0.1]")
            scaleStr=scaleStr+"+{factor}*{syst}".format(factor=factor,syst=syst)
            scaleSysts.append(syst)
        for syst,factor in resolution.iteritems():
            self.w.factory(syst+"[0,-0.5,0.5]")
            resolutionStr=resolutionStr+"+{factor}*{syst}".format(factor=factor,syst=syst)
            resolutionSysts.append(syst)

        MVV=variable
        self.w.factory(variable+"[0,13000]")


        f=open(jsonFile)
        info=json.load(f)

        SCALEVar="_".join(["MEAN",name,self.tag])
        self.w.factory("expr::{name}('({param})*(1+{vv_syst})',MH,{vv_systs})".format(name=SCALEVar,param=info['MEAN'],vv_syst=scaleStr,vv_systs=','.join(scaleSysts)))

        SIGMAVar="_".join(["SIGMA",name,self.tag])
        self.w.factory("expr::{name}('({param})*(1+{vv_syst})',MH,{vv_systs})".format(name=SIGMAVar,param=info['SIGMA'],vv_syst=resolutionStr,vv_systs=','.join(resolutionSysts)))

        ALPHA1Var="_".join(["ALPHA1",name,self.tag])
        self.w.factory("expr::{name}('MH*0+{param}',MH)".format(name=ALPHA1Var,param=info['ALPHA1']))

        ALPHA2Var="_".join(["ALPHA2",name,self.tag])
        self.w.factory("expr::{name}('MH*0+{param}',MH)".format(name=ALPHA2Var,param=info['ALPHA2']))

        N1Var="_".join(["N1",name,self.tag])
        self.w.factory("expr::{name}('MH*0+{param}',MH)".format(name=N1Var,param=info['N1']))

        N2Var="_".join(["N2",name,self.tag])
        self.w.factory("expr::{name}('MH*0+{param}',MH)".format(name=N2Var,param=info['N2']))

        pdfName="_".join([name,self.tag])
        vvMass = ROOT.RooDoubleCB(pdfName,pdfName,self.w.var(MVV),self.w.function(SCALEVar),self.w.function(SIGMAVar),self.w.function(ALPHA1Var),self.w.function(N1Var),self.w.function(ALPHA2Var),self.w.function(N2Var))
        getattr(self.w,'import')(vvMass, ROOT.RooCmdArg())
        f.close()





    def addMJJSignalParametricShape(self,name,variable,jsonFile,scale ={},resolution={},varToReplace="MH"):
        self.w.factory("MH[2000]")
        self.w.var("MH").setConstant(1)

        scaleStr='0'
        resolutionStr='0'

        scaleSysts=[]
        resolutionSysts=[]
        for syst,factor in scale.iteritems():
            self.w.factory(syst+"[0,-0.1,0.1]")
            scaleStr=scaleStr+"+{factor}*{syst}".format(factor=factor,syst=syst)
            scaleSysts.append(syst)
        for syst,factor in resolution.iteritems():
            self.w.factory(syst+"[0,-0.5,0.5]")
            resolutionStr=resolutionStr+"+{factor}*{syst}".format(factor=factor,syst=syst)
            resolutionSysts.append(syst)

        MJJ=variable
        self.w.factory(variable+"[0,1000]")


        f=open(jsonFile)
        info=json.load(f)

        SCALEVar="_".join(["mean",name,self.tag])
        self.w.factory("expr::{name}('({param})*(1+{vv_syst})',MH,{vv_systs})".format(name=SCALEVar,param=info['mean'],vv_syst=scaleStr,vv_systs=','.join(scaleSysts)).replace("MH",varToReplace))

        SIGMAVar="_".join(["sigma",name,self.tag])
        self.w.factory("expr::{name}('({param})*(1+{vv_syst})',MH,{vv_systs})".format(name=SIGMAVar,param=info['sigma'],vv_syst=resolutionStr,vv_systs=','.join(resolutionSysts)).replace("MH",varToReplace))

        ALPHAVar="_".join(["alpha",name,self.tag])
        self.w.factory("expr::{name}('MH*0+{param}',MH)".format(name=ALPHAVar,param=info['alpha']).replace("MH",varToReplace))

        NVar="_".join(["n",name,self.tag])
        self.w.factory("expr::{name}('MH*0+{param}',MH)".format(name=NVar,param=info['n']).replace("MH",varToReplace))

        pdfName="_".join([name+"peak",self.tag])
        vvMass = ROOT.RooCBShape(pdfName,pdfName,self.w.var(MJJ),self.w.function(SCALEVar),self.w.function(SIGMAVar),self.w.function(ALPHAVar),self.w.function(NVar))
        getattr(self.w,'import')(vvMass, ROOT.RooCmdArg())


        SLOPEVar="_".join(["slope",name,self.tag])
        self.w.factory("expr::{name}('MH*0+{param}',MH)".format(name=SLOPEVar,param=info['slope']).replace("MH",varToReplace))

        FVar="_".join(["f",name,self.tag])
        self.w.factory("expr::{name}('MH*0+{param}',MH)".format(name=FVar,param=info['f']).replace("MH",varToReplace))

        pdfName2="_".join([name+"bkg",self.tag])

        self.w.factory("RooExponential::{name}({var},{SLOPE})".format(name=pdfName2,var=MJJ,SLOPE=SLOPEVar).replace("MH",varToReplace))

        pdfName3="_".join([name,self.tag])
        self.w.factory("SUM::{name}({f}*{PDF1},{PDF2})".format(name=pdfName3,f=FVar,PDF1=pdfName,PDF2=pdfName2))

        f.close()



    def addMJJSignalParametricShapeCB(self,name,variable,jsonFile,scale ={},resolution={},varToReplace="MH"):
        self.w.factory("MH[2000]")
        self.w.var("MH").setConstant(1)

        scaleStr='0'
        resolutionStr='0'

        scaleSysts=[]
        resolutionSysts=[]
        for syst,factor in scale.iteritems():
            self.w.factory(syst+"[0,-0.1,0.1]")
            scaleStr=scaleStr+"+{factor}*{syst}".format(factor=factor,syst=syst)
            scaleSysts.append(syst)
        for syst,factor in resolution.iteritems():
            self.w.factory(syst+"[0,-0.5,0.5]")
            resolutionStr=resolutionStr+"+{factor}*{syst}".format(factor=factor,syst=syst)
            resolutionSysts.append(syst)

        MJJ=variable
        self.w.factory(variable+"[0,1000]")


        f=open(jsonFile)
        info=json.load(f)

        SCALEVar="_".join(["mean",name,self.tag])
        self.w.factory("expr::{name}('({param})*(1+{vv_syst})',MH,{vv_systs})".format(name=SCALEVar,param=info['mean'],vv_syst=scaleStr,vv_systs=','.join(scaleSysts)).replace("MH",varToReplace))

        SIGMAVar="_".join(["sigma",name,self.tag])
        self.w.factory("expr::{name}('({param})*(1+{vv_syst})',MH,{vv_systs})".format(name=SIGMAVar,param=info['sigma'],vv_syst=resolutionStr,vv_systs=','.join(resolutionSysts)).replace("MH",varToReplace))

        ALPHA1Var="_".join(["alpha1",name,self.tag])
        self.w.factory("expr::{name}('MH*0+{param}',MH)".format(name=ALPHA1Var,param=info['alpha1']).replace("MH",varToReplace))

        N1Var="_".join(["n1",name,self.tag])
        self.w.factory("expr::{name}('MH*0+{param}',MH)".format(name=N1Var,param=info['n1']).replace("MH",varToReplace))

        ALPHA2Var="_".join(["alpha2",name,self.tag])
        self.w.factory("expr::{name}('MH*0+{param}',MH)".format(name=ALPHA2Var,param=info['alpha2']).replace("MH",varToReplace))

        N2Var="_".join(["n2",name,self.tag])
        self.w.factory("expr::{name}('MH*0+{param}',MH)".format(name=N2Var,param=info['n2']).replace("MH",varToReplace))

        pdfName="_".join([name,self.tag])
        vvMass = ROOT.RooDoubleCB(pdfName,pdfName,self.w.var(MJJ),self.w.function(SCALEVar),self.w.function(SIGMAVar),self.w.function(ALPHA1Var),self.w.function(N1Var),self.w.function(ALPHA2Var),self.w.function(N2Var))
        getattr(self.w,'import')(vvMass, ROOT.RooCmdArg())
        f.close()


    def addMJJTopShapeCB(self,name,variable,jsonFile,scale ={},resolution={},varToReplace="MH",uncertainties=[0,0,0,0],newTag=""):
        self.w.factory("MH[2000]")
        self.w.var("MH").setConstant(1)


        if newTag !="":
            tag=newTag
        else:
            tag=name+"_"+self.tag

        scaleStr='0'
        resolutionStr='0'

        scaleSysts=[]
        resolutionSysts=[]
        for syst,factor in scale.iteritems():
            self.w.factory(syst+"[0,-0.1,0.1]")
            scaleStr=scaleStr+"+{factor}*{syst}".format(factor=factor,syst=syst)
            scaleSysts.append(syst)
        for syst,factor in resolution.iteritems():
            self.w.factory(syst+"[0,-0.5,0.5]")
            resolutionStr=resolutionStr+"+{factor}*{syst}".format(factor=factor,syst=syst)
            resolutionSysts.append(syst)

        MJJ=variable
        self.w.factory(variable+"[0,1000]")


        f=open(jsonFile)
        info=json.load(f)

        SCALEVar="_".join(["mean",name,self.tag])
        self.w.factory("expr::{name}('({param})*(1+{vv_syst})',MH,{vv_systs})".format(name=SCALEVar,param=info['mean'],vv_syst=scaleStr,vv_systs=','.join(scaleSysts)).replace("MH",varToReplace))

        SIGMAVar="_".join(["sigma",name,self.tag])
        self.w.factory("expr::{name}('({param})*(1+{vv_syst})',MH,{vv_systs})".format(name=SIGMAVar,param=info['sigma'],vv_syst=resolutionStr,vv_systs=','.join(resolutionSysts)).replace("MH",varToReplace))

        ALPHAVar1="_".join(["alpha1",name,self.tag])
        self.w.factory("expr::{name}('MH*0+{param}',MH)".format(name=ALPHAVar1,param=info['alpha1']).replace("MH",varToReplace))

        NVar1="_".join(["n1",name,self.tag])
        self.w.factory("expr::{name}('MH*0+{param}',MH)".format(name=NVar1,param=info['n1']).replace("MH",varToReplace))

        ALPHAVar2="_".join(["alpha2",name,self.tag])
        self.w.factory("expr::{name}('MH*0+{param}',MH)".format(name=ALPHAVar2,param=info['alpha2']).replace("MH",varToReplace))

        NVar2="_".join(["n2",name,self.tag])
        self.w.factory("expr::{name}('MH*0+{param}',MH)".format(name=NVar2,param=info['n2']).replace("MH",varToReplace))


        pdfName1="_".join([name,self.tag,'CB'])
        vvMass = ROOT.RooDoubleCB(pdfName1,pdfName1,self.w.var(MJJ),self.w.function(SCALEVar),self.w.function(SIGMAVar),self.w.function(ALPHAVar1),self.w.function(NVar1),self.w.function(ALPHAVar2),self.w.function(NVar2))
        getattr(self.w,'import')(vvMass, ROOT.RooCmdArg())



        p0="_".join(["c0",tag])
        p0Syst="_".join(["syst_c0",tag])

        if uncertainties[0] !=0:
            self.w.factory("{name}[-5,5]".format(name=p0Syst))
            self.w.factory("expr::{name}('({p0})*(1+{syst})',{syst})".format(name=p0,p0=info['c_0'],syst=p0Syst))

            self.addSystematic(p0Syst,"param",[0.0,uncertainties[0]])
            p0VAR = self.w.function(p0)

        else:
            self.w.factory("{name}[{val}]".format(name=p0,val=info['c_0']))
            p0VAR = self.w.var(p0)


        p1="_".join(["c1",tag])
        p1Syst="_".join(["syst_c1",tag])

        if uncertainties[1] !=0:
            self.w.factory("{name}[-5,5]".format(name=p1Syst))
            self.w.factory("expr::{name}('({p1})*(1+{syst})',{syst})".format(name=p1,p1=info['c_1'],syst=p1Syst))
            self.addSystematic(p1Syst,"param",[0.0,uncertainties[1]])
            p1VAR = self.w.function(p0)
        else:
            self.w.factory("{name}[{val}]".format(name=p1,val=info['c_1']))
            p1VAR = self.w.var(p1)

        p2="_".join(["c2",tag])
        p2Syst="_".join(["syst_c2",tag])

        if uncertainties[2] !=0:
            self.w.factory("{name}[-5,5]".format(name=p2Syst))
            self.w.factory("expr::{name}('({p2})*(1+{syst})',{syst})".format(name=p2,p2=info['c_2'],syst=p2Syst))
            self.addSystematic(p2Syst,"param",[0.0,uncertainties[2]])
            p2VAR = self.w.function(p2)
        else:
            self.w.factory("{name}[{val}]".format(name=p2,val=info['c_2']))
            p2VAR = self.w.var(p2)

        pdfName2="_".join([name,self.tag,'Erf'])
        erfexp = ROOT.RooErfExpPdf(pdfName2,pdfName2,self.w.var(MJJ),p0VAR,p1VAR,p2VAR)
        getattr(self.w,'import')(erfexp, ROOT.RooCmdArg())


        fR="_".join(["fR",tag])
        fRSyst="_".join(["syst_fR",tag])

        if uncertainties[3] !=0:
            self.w.factory("{name}[-0.5,0.5]".format(name=fRSyst))
            self.w.factory("expr::{name}('({fR})*(1+{syst})',{syst})".format(name=fR,fR=info['fR'],syst=fRSyst))
            self.addSystematic(fRSyst,"param",[0.0,uncertainties[3]])
            fRVAR = self.w.function(fR)
        else:
            self.w.factory("{name}[{val}]".format(name=fR,val=info['fR']))
            fRVAR = self.w.var(fR)



        pdfName="_".join([name,self.tag])
        self.w.factory("SUM::{name}({fR}*{name}_Erf,{name}_CB)".format(name=pdfName,fR=fR))
        f.close()





    def addHistoShapeFromFile(self,name,observables,filename,histoname,systematics=[],conditional = False,order=0,newTag=""):
        varset=ROOT.RooArgSet()
        varlist=ROOT.RooArgList()
        varPointers=[]
        for var in observables:
            self.w.factory(var+"[0,10000]")
            varPointers.append(self.w.var(var))
            varset.add(self.w.var(var))
            varlist.add(self.w.var(var))

        if newTag !="":
            tag=newTag
        else:
            tag=name+"_"+self.tag


        FR=ROOT.TFile(filename)

        #Load PDF
        histo=FR.Get(histoname)


        if len(systematics)>0:
            histName="_".join([name+"NominalHIST",tag])
            pdfName="_".join([name+"Nominal",self.tag])
        else:
            histName="_".join([name+"HIST",tag])
            pdfName="_".join([name,self.tag])

        roohist = ROOT.RooDataHist(histName,histName,varlist,histo)
        pdf=ROOT.RooHistPdf(pdfName,pdfName,varset,roohist,order)
        getattr(self.w,'import')(roohist, ROOT.RooCmdArg())
        getattr(self.w,'import')(pdf, ROOT.RooCmdArg())
        #Load SYstematics
        coeffList=ROOT.RooArgList()
        pdfList=ROOT.RooArgList(self.w.pdf(pdfName))

        for syst in systematics:
            self.w.factory(syst+"[-1,1]")
            coeffList.add(self.w.var(syst))

            for variation in ["Up","Down"]:
                histo=FR.Get(histoname+"_"+syst+variation)
                print 'loaded',histoname+"_"+syst+variation
                histName="_".join([name+"_"+syst+variation+"HIST",tag])
                roohist = ROOT.RooDataHist(histName,histName,varlist,histo)

                pdfName="_".join([name+"_"+syst+variation,self.tag])
                pdf=ROOT.RooHistPdf(pdfName,pdfName,varset,roohist,order)

                getattr(self.w,'import')(roohist, ROOT.RooCmdArg())
                getattr(self.w,'import')(pdf, ROOT.RooCmdArg())
                pdfList.add(self.w.pdf(pdfName))

        pdfName="_".join([name,self.tag])
        if len(systematics)>0:
            if len(observables)==1:
                total=ROOT.FastVerticalInterpHistPdf(pdfName,pdfName,self.w.var(observables[0]),pdfList, coeffList)
            elif len(observables)==2:
                total=ROOT.FastVerticalInterpHistPdf2D(pdfName,pdfName,self.w.var(observables[0]),self.w.var(observables[1]),conditional,pdfList, coeffList)
            getattr(self.w,'import')(total, ROOT.RooCmdArg())

    def addQuarkGluonTerm(self,name,observables,filename,histoname,systematics,jsonFile,fractionSysts,conditional = True,newTag=""):
          self.addHistoShapeFromFile(name+"quark",observables,filename,histoname+"_quark",systematics,conditional,newTag)
          self.addHistoShapeFromFile(name+"gluon",observables,filename,histoname+"_gluon",systematics,conditional,newTag)
          pdfName="_".join([name,self.tag])
          pdfName1="_".join([name+"quark",self.tag])
          pdfName2="_".join([name+"gluon",self.tag])

          #load json file
          f=open(jsonFile)
          info=json.load(f)
          param="("+info['quarkFraction'].replace("MVV",observables[0])+")*(1.0"

          systNames=[]
          for syst,factor in fractionSysts.iteritems():
              systNames.append(syst)
              self.w.factory(syst+"[0,-1,1]")
              param=param+"+{factor}*{syst}".format(factor=factor,syst=syst)

          param=param+")"

          systNames.append(observables[0])
          systStr=','.join(systNames)

          fname="_".join(["quarkGluonFraction",self.tag])
          self.w.factory("expr::{name}('{formula}',{deps})".format(name=fname,formula=param,deps=systStr))
          self.w.factory("SUM::{name}({f}*{name1},{name2})".format(name=pdfName,name1=pdfName1,name2=pdfName2,f=fname))


    def addMJJParametricBackgroundShapeErfExp(self,name,variable,jsonFile,systP0={},systP1={},systP2={}):

        MJJ=variable
        self.w.factory(MJJ+"[0,10000]")
        f=open(jsonFile)
        info=json.load(f)


        p0Systs=[]
        p1Systs=[]
        p2Systs=[]

        p0SystStr='0'
        p1SystStr='0'
        p2SystStr='0'

        for syst,factor in systP0.iteritems():
            self.w.factory(syst+"[0,-0.5,0.5]")
            p0SystStr+="+{factor}*{syst}".format(factor=factor,syst=syst)
            p0Systs.append(syst)
        for syst,factor in systP1.iteritems():
            self.w.factory(syst+"[0,-0.5,0.5]")
            p1SystStr+="+{factor}*{syst}".format(factor=factor,syst=syst)
            p1Systs.append(syst)
        for syst,factor in systP2.iteritems():
            self.w.factory(syst+"[0,-0.5,0.5]")
            p2SystStr+="+{factor}*{syst}".format(factor=factor,syst=syst)
            p2Systs.append(syst)



        p0="_".join(["p0",name,self.tag])
        self.w.factory("expr::{name}('({param})*(1+{vv_syst})',{vv_systs})".format(name=p0,param=info['c_0'],vv_syst=p0SystStr,vv_systs=','.join(p0Systs)))

        p1="_".join(["p1",name,self.tag])
        self.w.factory("expr::{name}('({param})*(1+{vv_syst})',{vv_systs})".format(name=p1,param=info['c_1'],vv_syst=p1SystStr,vv_systs=','.join(p1Systs)))

        p2="_".join(["p2",name,self.tag])
        self.w.factory("expr::{name}('({param})*(1+{vv_syst})',{vv_systs})".format(name=p2,param=info['c_2'],vv_syst=p2SystStr,vv_systs=','.join(p2Systs)))

        pdfName="_".join([name,self.tag])
        erfexp = ROOT.RooErfExpPdf(pdfName,pdfName,self.w.var(MJJ),self.w.function(p0),self.w.function(p1),self.w.function(p2))
        getattr(self.w,'import')(erfexp, ROOT.RooCmdArg())
        f.close()






    def addMJJParametricBackgroundShapeExpo(self,name,variable,jsonFile,systP0={}):

        MJJ=variable
        self.w.factory(MJJ+"[0,10000]")

        f=open(jsonFile)
        info=json.load(f)

        p0Systs=[]
        p0SystStr='0'
        for syst,factor in systP0.iteritems():
            self.w.factory(syst+"[0,-0.5,0.5]")
            p0SystStr+="+{factor}*{syst}".format(factor=factor,syst=syst)
            p0Systs.append(syst)

        p0="_".join(["p0",name,self.tag])
        self.w.factory("expr::{name}('({param})*(1+{vv_syst})',{vv_systs})".format(name=p0,param=info['c_0'],vv_syst=p0SystStr,vv_systs=','.join(p0Systs)))


        pdfName="_".join([name,self.tag])
        self.w.factory("RooExponential::{name}({x},{slope})".format(name=pdfName,x=MJJ,slope=p0))
        f.close()


    def addMJJFloatingBackgroundShapeErfExp(self,name,variable,newTag=""):
        MJJ=variable
        self.w.factory(MJJ+"[0,1000]")

        if newTag !="":
            tag=newTag
        else:
            tag=name+"_"+self.tag


        p0="_".join(["c_0",tag])
        self.w.factory(p0+"[-0.03,-10,10]")
        p1="_".join(["c_1",tag])
        self.w.factory(p1+"[50,40,160]")
        p2="_".join(["c_2",tag])
        self.w.factory(p2+"[20,1,200]")

        pdfName="_".join([name,self.tag])
        bernsteinPDF = ROOT.RooErfExpPdf(pdfName,pdfName,self.w.var(MJJ),self.w.var(p0),self.w.var(p1),self.w.var(p2))
        getattr(self.w,'import')(bernsteinPDF, ROOT.RooCmdArg())

    def addMJJFloatingBackgroundShapeBifur(self,name,variable,newTag=""):
        MJJ=variable
        self.w.factory(MJJ+"[0,1000]")

        if newTag !="":
            tag=newTag
        else:
            tag=name+"_"+self.tag


        p0="_".join(["c_0",tag])
        self.w.factory(p0+"[60,40,160]")
        p1="_".join(["c_1",tag])
        self.w.factory(p1+"[20,1,200]")
        p2="_".join(["c_2",tag])
        self.w.factory(p2+"[20,1,200]")


        pdfName="_".join([name,self.tag])
        self.w.factory("RooBifurGauss::{name}({var},{p0},{p1},{p2})".format(name=pdfName,var=MJJ,p0=p0,p1=p1,p2=p2))



    def addMJJFloatingBackgroundShapeExpo(self,name,variable,newTag=""):
        MJJ=variable
        self.w.factory(MJJ+"[0,10000]")

        if newTag !="":
            tag=newTag
        else:
            tag=name+"_"+self.tag


        p0="_".join(["c_0",tag])

        self.w.factory(p0+"[-10,0]")

        pdfName="_".join([name,self.tag])
        self.w.factory("RooExponential::{name}({var},{p0})".format(name=pdfName,var=MJJ,p0=p0))





    def addMVVBackgroundShapeQCD(self,name,variable,logTerm=False,newTag="",preconstrains={}):

        MVV=variable
        self.w.factory(MVV+"[0,10000]")


        if newTag !="":
            tag=newTag
        else:
            tag=name+"_"+self.tag



        p0="_".join(["p0",tag])
        if "p0" in preconstrains.keys():
            val = preconstrains['p0']['val']
            err = preconstrains['p0']['err']
            self.addSystematic(p0,"param",[val,err])
        else:
            val = 15.0
        self.w.factory("{name}[{val},10,60]".format(name=p0,val=val))

        p1="_".join(["p1",tag])
        if "p1" in preconstrains.keys():
            val = preconstrains['p1']['val']
            err = preconstrains['p1']['err']
            self.addSystematic(p1,"param",[val,err])
        else:
            val = 0.001
        self.w.factory("{name}[{val},0,5]".format(name=p1,val=val))


        p2="_".join(["p2",tag])
        if "p2" in preconstrains.keys():
            val = preconstrains['p2']['val']
            err = preconstrains['p2']['err']
            self.addSystematic(p2,"param",[val,err])
        else:
            val = 0.001



        if logTerm:
            self.w.factory("{name}[{val},0,1000]".format(name=p2,val=val))
        else:
            self.w.factory("{name}[0]".format(name=p2))

        pdfName="_".join([name,self.tag])
        qcd = ROOT.RooQCDPdf(pdfName,pdfName,self.w.var(MVV),self.w.var(p0),self.w.var(p1),self.w.var(p2))
        getattr(self.w,'import')(qcd, ROOT.RooCmdArg())



    def addMVVBackgroundShapePow(self,name,variable,newTag="",preconstrains={}):

        MVV=variable
        self.w.factory(MVV+"[0,13000]")

        if newTag !="":
            tag=newTag
        else:
            tag=name+"_"+self.tag

        p0="_".join(["p0",tag])
        if "p0" in preconstrains.keys():
            val = preconstrains['p0']['val']
            err = preconstrains['p0']['err']
            self.addSystematic(p0,"param",[val,err])
        else:
            val = -4
        self.w.factory("{name}[{val},-100,0]".format(name=p0,val=val))

        pdfName="_".join([name,self.tag])
        qcd = ROOT.RooPower(pdfName,pdfName,self.w.var(MVV),self.w.var(p0))
        getattr(self.w,'import')(qcd, ROOT.RooCmdArg())



    def addMVVBackgroundShapeErfPow(self,name,variable,newTag="",preconstrains={}):

        MVV=variable
        self.w.factory(MVV+"[0,13000]")

        if newTag !="":
            tag=newTag
        else:
            tag=name+"_"+self.tag

        p0="_".join(["p0",tag])
        if "p0" in preconstrains.keys():
            val = preconstrains['p0']['val']
            err = preconstrains['p0']['err']
            self.addSystematic(p0,"param",[val,err])
        else:
            val = -0.1
        self.w.factory("{name}[{val},-20,0]".format(name=p0,val=val))


        p1="_".join(["p1",tag])
        if "p1" in preconstrains.keys():
            val = preconstrains['p1']['val']
            err = preconstrains['p1']['err']
            self.addSystematic(p1,"param",[val,err])
        else:
            val = 700
        self.w.factory("{name}[{val},0,2000]".format(name=p1,val=val))


        p2="_".join(["p2",tag])
        if "p2" in preconstrains.keys():
            val = preconstrains['p2']['val']
            err = preconstrains['p2']['err']
            self.addSystematic(p2,"param",[val,err])
        else:
            val = 1000
        self.w.factory("{name}[{val},0,5000]".format(name=p2,val=val))


        pdfName="_".join([name,self.tag])
        qcd = ROOT.RooErfPowPdf(pdfName,pdfName,self.w.var(MVV),self.w.function(p0),self.w.function(p1),self.w.function(p2))

        getattr(self.w,'import')(qcd, ROOT.RooCmdArg())



    def addParametricMVVBKGShapeErfPow(self,name,MVV,MJJ,jsonFile,newTag="",systs0={},systs1={},systs2={},pdfTag=""):

        syst0Str='0'
        syst1Str='0'
        syst2Str='0'


        systsV0=[]
        systsV1=[]
        systsV2=[]

        for syst,factor in systs0.iteritems():
            self.w.factory(syst+"[0,-0.1,0.1]")
            syst0Str+="+{factor}*{syst}".format(factor=factor,syst=syst)
            systsV0.append(syst)

        for syst,factor in systs1.iteritems():
            self.w.factory(syst+"[0,-0.1,0.1]")
            syst1Str+="+{factor}*{syst}".format(factor=factor,syst=syst)
            systsV1.append(syst)

        for syst,factor in systs2.iteritems():
            self.w.factory(syst+"[0,-0.1,0.1]")
            syst2Str+="+{factor}*{syst}".format(factor=factor,syst=syst)
            systsV2.append(syst)



        self.w.factory(MVV+"[0,13000]")
        self.w.factory(MJJ+"[0,1000]")

        if newTag !="":
            tag=newTag
        else:
            tag=name+"_"+self.tag


        f=open(jsonFile)
        info=json.load(f)

        p0="_".join(["p0",name,tag])
        if syst0Str.find(MJJ)!=-1 or str(info['p0']).find('mjj')!=-1:
            self.w.factory("expr::{name}('({param})*(1+0*{MJJ}+{syst})',{MJJ},{systs})".format(name=p0,param=str(info['p0']).replace("mjj",MJJ),MJJ=MJJ,syst=syst0Str,systs=','.join(systsV0)))
        else:
            self.w.factory("expr::{name}('({param})*(1+{syst})',{systs})".format(name=p0,param=str(info['p0']).replace("mjj",MJJ),syst=syst0Str,systs=','.join(systsV0)))


        p1="_".join(["p1",name,tag])
        if syst1Str.find(MJJ)!=-1 or str(info['p1']).find('mjj')!=-1:
            self.w.factory("expr::{name}('({param})*(1+0*{MJJ}+{syst})',{MJJ},{systs})".format(name=p1,param=str(info['p1']).replace("mjj",MJJ),MJJ=MJJ,syst=syst1Str,systs=','.join(systsV1)))
        else:
            self.w.factory("expr::{name}('({param})*(1+{syst})',{systs})".format(name=p1,param=str(info['p1']).replace("mjj",MJJ),syst=syst1Str,systs=','.join(systsV1)))



        p2="_".join(["p2",name,tag])
        if syst2Str.find(MJJ)!=-1 or str(info['p2']).find('mjj')!=-1:
            self.w.factory("expr::{name}('({param})*(1+0*{MJJ}+{syst})',{MJJ},{systs})".format(name=p2,param=str(info['p2']).replace("mjj",MJJ),MJJ=MJJ,syst=syst2Str,systs=','.join(systsV2)))
        else:
            self.w.factory("expr::{name}('({param})*(1+{syst})',{systs})".format(name=p2,param=str(info['p2']).replace("mjj",MJJ),syst=syst2Str,systs=','.join(systsV2)))

        if pdfTag=="":
            pdfName="_".join([name,self.tag])
        else:
            pdfName="_".join([name,pdfTag])

        erfexp = ROOT.RooErfPowPdf(pdfName,pdfName,self.w.var(MVV),self.w.function(p0),self.w.function(p1),self.w.function(p2))
        getattr(self.w,'import')(erfexp, ROOT.RooCmdArg())



    def addParametricMVVBKGShapePow(self,name,MVV,MJJ,jsonFile,newTag="",systs0={}):
        syst0Str='0'
        systsV0=[]
        for syst,factor in systs0.iteritems():
            self.w.factory(syst+"[0,-0.1,0.1]")
            syst0Str+="+{factor}*{syst}".format(factor=factor,syst=syst)
            systsV0.append(syst)

        self.w.factory(MVV+"[0,13000]")
        self.w.factory(MJJ+"[0,1000]")

        if newTag !="":
            tag=newTag
        else:
            tag=name+"_"+self.tag


        f=open(jsonFile)
        info=json.load(f)



        p0="_".join(["p0",name,tag])
        self.w.factory("expr::{name}('({param})*(1+0*{MJJ}+{syst})',{MJJ},{systs})".format(name=p0,param=info['p0'].replace("mjj",MJJ),MJJ=MJJ,syst=syst0Str,systs=','.join(systsV0)))

        pdfName="_".join([name,self.tag])
        qcd = ROOT.RooPower(pdfName,pdfName,self.w.var(MVV),self.w.function(p0))
        getattr(self.w,'import')(erfexp, ROOT.RooCmdArg())




    def sum(self,name,pdf1,pdf2,sumVar,sumVarExpr=""):
        pdfName="_".join([name,self.tag])
        pdfName1="_".join([pdf1,self.tag])
        pdfName2="_".join([pdf2,self.tag])
        if sumVarExpr=='':
            self.w.factory(sumVar+"[0,1]")
        else:
            self.w.factory("expr::"+sumVar+"("+sumVarExpr+")")
        self.w.factory("SUM::{name}({f}*{name1},{name2})".format(name=pdfName,name1=pdfName1,f=sumVar,name2=pdfName2))


    def conditionalProduct(self,name,pdf1,varName,pdf2,tag1="",tag2=""):
        pdfName="_".join([name,self.tag])

        if tag1=="":
            pdfName1="_".join([pdf1,self.tag])
        else:
            pdfName1="_".join([pdf1,tag1])
        if tag2=="":
            pdfName2="_".join([pdf2,self.tag])
        else:
            pdfName2="_".join([pdf2,tag2])

        self.w.factory("PROD::{name}({name1}|{x},{name2})".format(name=pdfName,name1=pdfName1,x=varName,name2=pdfName2))

    def product(self,name,pdf1,pdf2):
        pdfName="_".join([name,self.tag])
        pdfName1="_".join([pdf1,self.tag])
        pdfName2="_".join([pdf2,self.tag])
        self.w.factory("PROD::{name}({name1},{name2})".format(name=pdfName,name1=pdfName1,name2=pdfName2))





    def envelope(self,name,pdfs):
        catName = "envelope_"+name+"_"+self.tag
        pdfName="_".join([name,self.tag])

        pdfList=[]
        pdfArgList = ROOT.RooArgList()
        for p in pdfs:
            pdfList.append(p+"_"+self.tag)
            pdfArgList.add(self.w.pdf(p+"_"+self.tag))

        pdfStr = ','.join(pdfList)
        self.w.factory("{cat}[{list}]".format(cat=catName,list=pdfStr))
        multiPDF = ROOT.RooMultiPdf(pdfName,pdfName,self.w.cat(catName),pdfArgList)
        getattr(self.w,'import')(multiPDF)
        self.addSystematic(catName,"discrete","")

    def conditionalDoubleProduct(self,name,pdf1,pdf2,varName,pdf3):
        pdfName="_".join([name,self.tag])
        pdfName1="_".join([pdf1,self.tag])
        pdfName2="_".join([pdf2,self.tag])
        pdfName3="_".join([pdf3,self.tag])
        self.w.factory("PROD::{name}({name1}|{x},{name2}|{x},{name3})".format(name=pdfName,name1=pdfName1,x=varName,name2=pdfName2,name3=pdfName3))


    def product(self,name,pdf1,pdf2):
        pdfName="_".join([name,self.tag])
        pdfName1="_".join([pdf1,self.tag])
        pdfName2="_".join([pdf2,self.tag])
        self.w.factory("PROD::{name}({name1},{name2})".format(name=pdfName,name1=pdfName1,name2=pdfName2))

    def addParametricYield(self,name,ID,jsonFile):
        f=open(jsonFile)
        info=json.load(f)

        pdfName="_".join([name,self.tag])
        pdfNorm="_".join([name,self.tag,"norm"])
        self.w.factory("expr::{name}('({param})*{lumi}',MH,{lumi})".format(name=pdfNorm,param=info['yield'],lumi=self.physics+"_"+self.period+"_lumi"))
        f.close()
        self.contributions.append({'name':name,'pdf':pdfName,'ID':ID,'yield':1.0})


    def addParametricYieldWithCrossSection(self,name,ID,jsonFile,jsonFileCS,sigmaStr,BRStr):
        ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")
        from array import array
        #first load cross section
        fCS=open(jsonFileCS)
        info=json.load(fCS)
        xArr=[]
        yArr=[]

        for m in sorted(map(float,info.keys())):
            xArr.append(float(m))
            #I know this is stupid
            yArr.append(float(info[str(int(m))][sigmaStr])*float(info[str(int(m))][BRStr]))


        pdfSigma="_".join([name,self.tag,"sigma"])
        spline=ROOT.RooSpline1D(pdfSigma,pdfSigma,self.w.var("MH"),len(xArr),array('d',xArr),array('d',yArr))
        getattr(self.w,'import')(spline, ROOT.RooCmdArg())
        fCS.close()

        f=open(jsonFile)
        info=json.load(f)
        pdfName="_".join([name,self.tag])
        pdfNorm="_".join([name,self.tag,"norm"])
        self.w.factory("expr::{name}('({param})*{lumi}*({sigma})',MH,{lumi},{sigma})".format(name=pdfNorm,param=info['yield'],lumi=self.physics+"_"+self.period+"_lumi",sigma=pdfSigma))
        f.close()
        self.contributions.append({'name':name,'pdf':pdfName,'ID':ID,'yield':1.0})



    def addFloatingYield(self,name,ID,events,mini=0,maxi=1e+9,constant=False):
        pdfName="_".join([name,self.tag])
        pdfNorm="_".join([name,self.tag,"norm"])
        self.w.factory("{name}[{val},{mini},{maxi}]".format(name=pdfNorm,val=events,mini=mini,maxi=maxi))
        if constant:
            self.w.var(pdfNorm).setConstant(1)
        self.contributions.append({'name':name,'pdf':pdfName,'ID':ID,'yield':1.0})


    def addConstrainedYield(self,name,ID,events,nuisance,uncertainty):
        pdfName="_".join([name,self.tag])
        self.contributions.append({'name':name,'pdf':pdfName,'ID':ID,'yield':events})
        self.addSystematic(nuisance,"lnN",{name:1+uncertainty})

    def addConstrainedYieldFromFile(self,name,ID,filename,histoName,nuisance,uncertainty):
        pdfName="_".join([name,self.tag])

        f=ROOT.TFile(filename)
        histogram=f.Get(histoName)
        events=histogram.Integral()*self.luminosity
        self.contributions.append({'name':name,'pdf':pdfName,'ID':ID,'yield':events})
        self.addSystematic(nuisance,"lnN",{name:1+uncertainty})

    def addFixedYieldFromFile(self,name,ID,filename,histoName):
        pdfName="_".join([name,self.tag])
        f=ROOT.TFile(filename)
        histogram=f.Get(histoName)
        events=histogram.Integral()*self.luminosity
        self.contributions.append({'name':name,'pdf':pdfName,'ID':ID,'yield':events})





    def makeCard(self):

        f = open("datacard_"+self.tag+'.txt','w')
        f.write('imax 1\n')
        f.write('jmax {n}\n'.format(n=len(self.contributions)-1))
        f.write('kmax *\n')
        f.write('-------------------------\n')
        for c in self.contributions:
            f.write('shapes {name} {channel} {file}.root w:{pdf}\n'.format(name=c['name'],channel=self.tag,file="datacardInputs_"+self.tag,pdf=c['pdf']))
        f.write('shapes {name} {channel} {file}.root w:{name}\n'.format(name="data_obs",channel=self.tag,file="datacardInputs_"+self.tag))
        f.write('-------------------------\n')
        f.write('bin '+self.tag+'\n')
        f.write('observation  -1\n')
        f.write('-------------------------\n')
        f.write('bin\t')

        for shape in self.contributions:
            f.write(self.tag+'\t')
        f.write('\n')

        #Sort the shapes by ID

        shapes = sorted(self.contributions,key=lambda x: x['ID'])
        #print names
        f.write('process\t')
        for shape in shapes:
            f.write(shape['name']+'\t')
        f.write('\n')

        #Print ID
        f.write('process\t')
        for shape in shapes:
            f.write(str(shape['ID'])+'\t')
        f.write('\n')

        #print rates
        f.write('rate\t')
        for shape in shapes:
            f.write(str(shape['yield'])+'\t')
        f.write('\n')


        #Now systematics
        for syst in self.systematics:
            if syst['kind'] == 'param':
                f.write(syst['name']+'\t'+'param\t' +str(syst['values'][0])+'\t'+str(syst['values'][1])+'\n')

            elif syst['kind'] == 'discrete':
                f.write(syst['name']+'\t'+'discrete\n')

            elif syst['kind'] == 'lnN':
                f.write(syst['name']+'\t'+ 'lnN\t' )
                for shape in shapes:
                    has=False
                    for name,v in syst['values'].iteritems():
                        if shape['name']==name:
                            f.write(str(v)+'\t' )
                            has=True
                            break;
                    if not has:
                            f.write('-\t' )
                f.write('\n' )
            elif syst['kind'] == 'lnU':
                f.write(syst['name']+'\t'+ 'lnU\t' )
                for shape in shapes:
                    has=False
                    for name,v in syst['values'].iteritems():
                        if shape['name']==name:
                            f.write(str(v)+'\t' )
                            has=True
                            break;
                    if not has:
                            f.write('-\t' )
                f.write('\n' )


        f.close()


        self.rootFile.cd()
        self.w.Write()
        self.rootFile.Close()




    def importBinnedData(self,filename,histoname,poi,name = "data_obs",scale=1):
        f=ROOT.TFile(filename)
        histogram=f.Get(histoname)
        histogram.Scale(scale)
        cList = ROOT.RooArgList()
        for i,p in enumerate(poi):
            cList.add(self.w.var(p))
            if i==0:
                axis=histogram.GetXaxis()
            elif i==1:
                axis=histogram.GetYaxis()
            elif i==2:
                axis=histogram.GetZaxis()
            else:
                print 'Asking for more than 3 D . ROOT doesnt support that, use unbinned data instead'
                return
            mini=axis.GetXmin()
            maxi=axis.GetXmax()
            bins=axis.GetNbins()
            self.w.var(p).setMin(mini)
            self.w.var(p).setMax(maxi)
            self.w.var(p).setBins(bins)
        dataHist=ROOT.RooDataHist(name,name,cList,histogram)

        getattr(self.w,'import')(dataHist, ROOT.RooCmdArg())
