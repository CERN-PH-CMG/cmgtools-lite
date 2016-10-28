
import ROOT
import os




cuts={}


cuts['common'] = '(((HLT2_MU||HLT2_ELE||HLT2_ISOMU||HLT2_ISOELE||HLT2_MET120)&&run>2000)+(run<2000)*lnujj_sf)*(Flag_goodVertices&&Flag_CSCTightHaloFilter&&Flag_HBHENoiseFilter&&Flag_HBHENoiseIsoFilter&&Flag_eeBadScFilter&&lnujj_nOtherLeptons==0&&lnujj_l2_softDrop_mass>0&&lnujj_LV_mass>600&&Flag_badChargedHadronFilter&&Flag_badMuonFilter&&(abs(lnujj_l1_l_pdgId)==11||(abs(lnujj_l1_l_pdgId)==13&&lnujj_l1_l_relIso04<0.1)))'


cuts['mu'] = '(abs(lnujj_l1_l_pdgId)==13)'
cuts['e'] = '(abs(lnujj_l1_l_pdgId)==11)'
cuts['HP'] = '(lnujj_l2_tau2/lnujj_l2_tau1<0.6)'
cuts['LP'] = '(lnujj_l2_tau2/lnujj_l2_tau1>0.6&&lnujj_l2_tau2/lnujj_l2_tau1<0.75)'
cuts['nob'] = '(lnujj_nMediumBTags==0)*lnujj_btagWeight'
cuts['b'] = '(lnujj_nMediumBTags>0)*lnujj_btagWeight'


leptons=['mu','e']
purities=['HP','LP']
categories=['nob','b']


WWTemplate="BulkGravToWWToWlepWhad_narrow"
BRWW=2.*0.327*0.6760


WZTemplate="WprimeToWZToWlepZhad_narrow"
BRWZ=0.327*0.6991

WHTemplate="WprimeToWhToWlephbb"
BRWH=0.577*0.327


dataTemplate="SingleMuon,SingleElectron"
topTemplate="TTJets."


WJetsTemplate="WJetsToLNu_HT"

SMWWTemplate='WWTo1L1Nu2Q'
SMWZTemplate='WZTo1L1Nu2Q'



minMJJ=40.0
maxMJJ=160.0

minMVV=600.0
maxMVV=4800.0


binsMJJ=60
binsMVV=200


cuts['acceptance']= "(lnujj_LV_mass>{minMVV}&&lnujj_LV_mass<{maxMVV}&&lnujj_l2_softDrop_mass>{minMJJ}&&lnujj_l2_softDrop_mass<{maxMJJ})".format(minMVV=minMVV,maxMVV=maxMVV,minMJJ=minMJJ,maxMJJ=maxMJJ)                
cuts['acceptanceMJJ']= "(lnujj_l2_softDrop_mass>{minMJJ}&&lnujj_l2_softDrop_mass<{maxMJJ})".format(minMJJ=minMJJ,maxMJJ=maxMJJ)                


def makeSignalShapesMVV(filename,template):
    for l in leptons:
        cut='*'.join([cuts['common'],cuts[l],cuts['acceptanceMJJ']])
        rootFile=filename+"_MVV_"+l+".root"
        cmd='vvMakeSignalMVVShapes.py -s "{template}" -c "{cut}"  -o "{rootFile}" -V "lnujj_LV_mass"  samples'.format(template=template,cut=cut,rootFile=rootFile,minMJJ=minMJJ,maxMJJ=maxMJJ)
        os.system(cmd)
        jsonFile=filename+"_MVV_"+l+".json"
        print 'Making JSON'
        cmd='vvMakeJSON.py  -o "{jsonFile}" -g "MEAN:pol1,SIGMA:pol2,ALPHA1:pol3,N1:pol0,ALPHA2:pol4,N2:pol0" -m 800 -M 5000  {rootFile}  '.format(jsonFile=jsonFile,rootFile=rootFile)
        os.system(cmd)


def makeSignalShapesMJJ(filename,template):
    for p in purities:
        cut='*'.join([cuts['common'],cuts[p],"(lnujj_LV_mass>600)"])
        rootFile=filename+"_MJJ_"+p+".root"
        cmd='vvMakeSignalMJJShapes.py -s "{template}" -c "{cut}"  -o "{rootFile}" -V "lnujj_l2_softDrop_mass"  samples'.format(template=template,cut=cut,rootFile=rootFile,minMJJ=minMJJ,maxMJJ=maxMJJ)
        os.system(cmd)
        jsonFile=filename+"_MJJ_"+p+".json"
        cmd='vvMakeJSON.py  -o "{jsonFile}" -g "mean:pol4,sigma:pol4,alpha:pol3,n:pol0,slope:pol4,f:pol4" -m 800 -M 5000  {rootFile}  '.format(jsonFile=jsonFile,rootFile=rootFile)
        os.system(cmd)


def makeSignalYields(filename,template,branchingFraction):
    for lepton in leptons:
        for purity in purities:
            for region in categories:
                cut = "*".join([cuts[lepton],cuts[purity],cuts['common'],cuts[region],cuts['acceptance']])
                #Signal yields
                yieldFile=filename+"_"+lepton+"_"+purity+"_"+region+"_yield"
                cmd='vvMakeSignalYields.py -s {template} -c "{cut}" -o {output} -V "lnujj_LV_mass" -m {minMVV} -M {maxMVV} -f "pol6" -b {BR} -x 800 samples'.format(template=template, cut=cut, output=yieldFile,minMVV=minMVV,maxMVV=maxMVV,BR=branchingFraction)
                os.system(cmd)




def makeBackgroundShapesMVVNoP(name,filename,template,addCut=""):
    for l in leptons:
        if addCut=='':
            cut='*'.join([cuts['common'],cuts[l]])
        else:
            cut='*'.join([cuts['common'],cuts[l],addCut])
                
        mvvFile=filename+"_MVV_"+name+"_"+l
        cmd='vvMakeBackgroundMVVConditionalShapes.py -s "{template}" -c "{cut}"  -o "{rootFile}" -v "lnujj_LV_mass" -V "lnujj_l2_softDrop_mass"  -b 200  -x {minMVV} -X {maxMVV}   -B 12 -y {minMJJ} -Y {maxMJJ}   samples'.format(template=template,cut=cut,rootFile=mvvFile,minMVV=minMVV,maxMVV=maxMVV,minMJJ=minMJJ-12,maxMJJ=maxMJJ+12)
        os.system(cmd)

        #And now the histogrammed versions
def makeBackgroundShapesHisto(name,filename):
    for l in leptons:
        for p in purities:               
            mvvFile=filename+"_MVV_"+name+"_"+l
            mjjFile=filename+"_MJJ_"+name+"_"+p+".json"
            rootFile=filename+"_MVVHist_"+name+"_"+l+"_"+p+".root"
            cmd="vvPDFToHisto.py -n histo -s 'slopeSyst_{name}:1.0:0.2' -m 'meanSyst0_{name}:1.0:0.2,meanSyst1_{name}:mjj:1e-3' -w 'widthSyst_{name}:1.0:0.2' -S 'slopeSystMJJ_{name2}:1.0:0.3' -M 'meanSystMJJ_{name2}:1.0:0.3' -W 'widthSystMJJ_{name2}:1.0:0.3'   -j {mjjFile} -o '{rootFile}' -b {binsMVV} -x {minMVV} -X {maxMVV} -B {binsMJJ} -y {minMJJ} -Y {maxMJJ} {mvvFile}.json".format(name=name+"_"+l,name2=name+"_"+p,rootFile=rootFile,binsMVV=binsMVV,minMVV=minMVV,maxMVV=maxMVV,binsMJJ=binsMJJ,minMJJ=minMJJ,maxMJJ=maxMJJ,mvvFile=mvvFile,mjjFile=mjjFile) 
            os.system(cmd)


def makeBackgroundShapesHistoWithCat(name,filename):
    for l in leptons:
        for p in purities:               
            for c in categories:               
                mvvFile=filename+"_MVV_"+name+"_"+l+"_"+c
                mjjFile=filename+"_MJJ_"+name+"_"+p+".json"
                rootFile=filename+"_MVVHist_"+name+"_"+l+"_"+p+"_"+c+".root"
                cmd="vvPDFToHisto.py -n histo -s 'slopeSyst_{name}:1.0:0.2' -m 'meanSyst0_{name}:1.0:0.2,meanSyst1_{name}:mjj:1e-3' -w 'widthSyst_{name}:1.0:0.2' -S 'slopeSystMJJ_{name2}:1.0:0.3' -M 'meanSystMJJ_{name2}:1.0:0.3' -W 'widthSystMJJ_{name2}:1.0:0.1'   -j {mjjFile} -o '{rootFile}' -b {binsMVV} -x {minMVV} -X {maxMVV} -B {binsMJJ} -y {minMJJ} -Y {maxMJJ} {mvvFile}.json".format(name=name+"_"+l+"_"+c,name2=name+"_"+p,rootFile=rootFile,binsMVV=binsMVV,minMVV=minMVV,maxMVV=maxMVV,binsMJJ=binsMJJ,minMJJ=minMJJ,maxMJJ=maxMJJ,mvvFile=mvvFile,mjjFile=mjjFile) 
                os.system(cmd)



def makeBackgroundShapesMJJ(name,filename,template,addCut=""):
    for l in leptons:
        for p in purities:
            if addCut=='':
                cut='*'.join([cuts['common'],cuts[p],cuts[l],cuts['acceptance']])
            else:
                cut='*'.join([cuts['common'],cuts[p],cuts[l],addCut,cuts['acceptance']])
            if p=="HP":
                function='erfexp'
#                if name.find('top')!=-1:
#                    function='erfexpCB'
                    
            if p=="LP":
                function='erfexp'
                if name.find('top')!=-1:
                    function='expo'

            rootFile="tmp.root"
            cmd='vvMakeData.py -s "{samples}"  -c "{cut}"  -o "{rootFile}" -v "lnujj_l2_softDrop_mass" -b "{bins}" -m "{mini}" -M "{maxi}"  -n "{name}"  -d 0 samples'.format(samples=template,cut=cut,rootFile=rootFile,bins=binsMJJ,mini=minMJJ,maxi=maxMJJ,name=name)
            os.system(cmd)
            
            jsonFile=filename+"_MJJ_"+name+"_"+l+"_"+p
            cmd='vvSimpleFit.py -o {jsonFile} -i {histo} -f {function} {rootFile}'.format(jsonFile=jsonFile,rootFile=rootFile,histo=name,function=function)
            os.system(cmd)

def makeBackgroundShapesMJJNoL(name,filename,template,addCut=""):
    for p in purities:
        if addCut=='':
            cut='*'.join([cuts['common'],cuts[p],cuts['acceptance']])
        else:
            cut='*'.join([cuts['common'],cuts[p],addCut,cuts['acceptance']])
        if p=="HP":
            function='erfexp'
#                if name.find('top')!=-1:
#                    function='erfexpCB'
                    
        if p=="LP":
            function='erfexp'
            if name.find('top')!=-1:
                function='expo'

        rootFile="tmp.root"
        cmd='vvMakeData.py -s "{samples}"  -c "{cut}"  -o "{rootFile}" -v "lnujj_l2_softDrop_mass" -b "{bins}" -m "{mini}" -M "{maxi}"  -n "{name}"  -d 0 samples'.format(samples=template,cut=cut,rootFile=rootFile,bins=binsMJJ,mini=minMJJ,maxi=maxMJJ,name=name)
        os.system(cmd)
            
        jsonFile=filename+"_MJJ_"+name+"_"+p
        cmd="vvSimpleFit.py -t Mj -o {jsonFile} -i {histo} -f {function} {rootFile}".format(jsonFile=jsonFile,rootFile=rootFile,histo=name,function=function)
        os.system(cmd)



def makeBackgroundShapesMJJPerCat(name,filename,template,addCut=""):
    for p in purities:
        for c in categories:
            if addCut=='':
                cut='*'.join([cuts['common'],cuts[p],cuts[c],cuts['acceptance']])
            else:
                cut='*'.join([cuts['common'],cuts[p],addCut,cuts[c],cuts['acceptance']])


            if p=="HP":
                function='erfexp'
                
            if p=="LP":
                function='expo'

            rootFile="tmp.root"
            cmd='vvMakeData.py -s "{samples}"  -c "{cut}"  -o "{rootFile}" -v "lnujj_l2_softDrop_mass" -b "{bins}" -m "{mini}" -M "{maxi}"  -n "{name}"  -d 0 samples'.format(samples=template,cut=cut,rootFile=rootFile,bins=binsMJJ,mini=minMJJ,maxi=maxMJJ,name=name)
            os.system(cmd)
            
            jsonFile=filename+"_MJJ_"+name+"_"+p+"_"+c
            cmd='vvSimpleFit.py -o {jsonFile} -i {histo} -f {function} {rootFile}'.format(jsonFile=jsonFile,rootFile=rootFile,histo=name,function=function)
            os.system(cmd)


def makeBackgroundShapesMVVPerCat(name,filename,template,addCut=""):
    for l in leptons:
        for c in categories:

            if addCut=='':
                cut='*'.join([cuts['common'],cuts[l],cuts[c]])
            else:
                cut='*'.join([cuts['common'],cuts[l],cuts[c],addCut])
                
            mvvFile=filename+"_MVV_"+name+"_"+l+"_"+c
            cmd='vvMakeBackgroundMVVConditionalShapes.py -s "{template}" -c "{cut}"  -o "{rootFile}" -v "lnujj_LV_mass" -V "lnujj_l2_softDrop_mass"  -b 500  -x {minMVV} -X {maxMVV}   -B 10 -y {minMJJ} -Y {maxMJJ}   samples'.format(template=template,cut=cut,rootFile=mvvFile,minMVV=minMVV,maxMVV=maxMVV,minMJJ=minMJJ-15,maxMJJ=maxMJJ+15)
#                cmd='vvMakeBackgroundMVVConditionalShapesErfPowSim.py -s "{template}" -c "{cut}"  -o "{rootFile}" -v "lnujj_LV_mass" -V "lnujj_l2_softDrop_mass"  -b 500  -x {minMVV} -X {maxMVV}   -B 120 -y {minMJJ} -Y {maxMJJ}   samples'.format(template=template,cut=cut,rootFile=mvvFile,minMVV=minMVV,maxMVV=maxMVV,minMJJ=minMJJ,maxMJJ=maxMJJ)
            os.system(cmd)

def makeBackgroundShapesPerCat(name,filename,template,addCut=""):
    for l in leptons:
        for p in purities:
            for c in categories:

                if addCut=='':
                    cut='*'.join([cuts['common'],cuts[p],cuts[l],cuts[c]])
                else:
                    cut='*'.join([cuts['common'],cuts[p],cuts[l],cuts[c],addCut])
                
                mvvFile=filename+"_MVV_"+name+"_"+l+"_"+p+"_"+c
                cmd='vvMakeBackgroundMVVConditionalShapes.py -s "{template}" -c "{cut}"  -o "{rootFile}" -v "lnujj_LV_mass" -V "lnujj_l2_softDrop_mass"  -b 100  -x {minMVV} -X {maxMVV}   -B 8 -y {minMJJ} -Y {maxMJJ}   samples'.format(template=template,cut=cut,rootFile=mvvFile,minMVV=minMVV,maxMVV=maxMVV,minMJJ=minMJJ,maxMJJ=maxMJJ)
#                cmd='vvMakeBackgroundMVVConditionalShapesErfPowSim.py -s "{template}" -c "{cut}"  -o "{rootFile}" -v "lnujj_LV_mass" -V "lnujj_l2_softDrop_mass"  -b 500  -x {minMVV} -X {maxMVV}   -B 120 -y {minMJJ} -Y {maxMJJ}   samples'.format(template=template,cut=cut,rootFile=mvvFile,minMVV=minMVV,maxMVV=maxMVV,minMJJ=minMJJ,maxMJJ=maxMJJ)

                os.system(cmd)




                if addCut=='':
                    cut='*'.join([cuts['common'],cuts[p],cuts[l],cuts[c],cuts['acceptance']])
                else:
                    cut='*'.join([cuts['common'],cuts[p],cuts[l],addCut,cuts[c],cuts['acceptance']])


                if p=="HP":
                    function='erfexp'
                    
                if p=="LP":
                    function='expo'

                rootFile="tmp.root"
                cmd='vvMakeData.py -s "{samples}"  -c "{cut}"  -o "{rootFile}" -v "lnujj_l2_softDrop_mass" -b "{bins}" -m "{mini}" -M "{maxi}"  -n "{name}"  -d 0 samples'.format(samples=template,cut=cut,rootFile=rootFile,bins=binsMJJ,mini=minMJJ,maxi=maxMJJ,name=name)
                os.system(cmd)
            
                jsonFile=filename+"_MJJ_"+name+"_"+l+"_"+p+"_"+c
                cmd='vvSimpleFit.py -o {jsonFile} -i {histo} -f {function} {rootFile}'.format(jsonFile=jsonFile,rootFile=rootFile,histo=name,function=function)
                os.system(cmd)


def makeTopShapes2(name,filename,template,addCut=""):

    for p in purities:
        if p=='HP':
            if addCut=='':
                cut='*'.join([cuts['common'],cuts[p]])
            else:
                cut='*'.join([cuts['common'],cuts[p],addCut])
        else:
            if addCut=='':
                cut='*'.join([cuts['common']])
            else:
                cut='*'.join([cuts['common'],addCut])
                       
        mjjFile=filename+"_MJJ_"+name+"_"+p
        cmd='vvMakeTopMJJConditionalShapesFromTruth.py -s "{template}" -c "{cut}"  -o "{rootFile}" -v "lnujj_l2_softDrop_mass" -V "lnujj_LV_mass"  -b 20  -x {minMJJ} -X {maxMJJ}  -i "LNuJJ_XWW_MJJ_{purity}.json"   samples'.format(template=template,cut=cut,rootFile=mjjFile,minMJJ=minMJJ,maxMJJ=maxMJJ,purity=p)
        os.system(cmd)



    for l in leptons:    
#        for p in purities:
        for c in categories:
            if addCut=='':
                cut='*'.join([cuts['common'],cuts[l],cuts[c]])
            else:
                cut='*'.join([cuts['common'],addCut,cuts[l],cuts[c]])

            rootFile="tmp.root"
            cmd='vvMakeData.py -s "{samples}"  -c "{cut}"  -o "{rootFile}" -v "lnujj_LV_mass" -b "{bins}" -m "{mini}" -M "{maxi}"  -n "{name}"  -d 0 samples'.format(samples=template,cut=cut,rootFile=rootFile,bins=100,mini=600,maxi=maxMVV,name=name)
            os.system(cmd)
                
            jsonFile=filename+"_MVV_"+name+"_"+l+"_"+c
            cmd='vvSimpleFit.py -o {jsonFile} -i {histo} -f erfpow {rootFile}'.format(jsonFile=jsonFile,rootFile=rootFile,histo=name)
            os.system(cmd)

            rootFile=filename+"_MVVHist_"+name+"_"+l+"_"+c+".root"
            cmd="vvPDFToHisto1D.py -n histo -s 'slopeSyst_{name}:1.0:0.1' -m 'meanSyst_{name}:1.0:0.1' -w 'widthSyst_{name}:1.0:0.1' -o '{rootFile}' -b {binsMVV} -x {minMVV} -X {maxMVV}  {mvvFile}.json".format(name=name+"_"+l+"_"+c,rootFile=rootFile,binsMVV=binsMVV,minMVV=minMVV,maxMVV=maxMVV,mvvFile=jsonFile) 
            os.system(cmd)



def makeTopShapes(name,filename,template,addCut=""):

    for p in purities:
        if p=='HP':
            if addCut=='':
                cut='*'.join([cuts['common'],cuts[p]])
            else:
                cut='*'.join([cuts['common'],cuts[p],addCut])
        else:
            if addCut=='':
                cut='*'.join([cuts['common']])
            else:
                cut='*'.join([cuts['common'],addCut])
                       
        mjjFile=filename+"_MJJ_"+name+"_"+p
        cmd='vvMakeTopMJJConditionalShapes.py -s "{template}" -c "{cut}"  -o "{rootFile}" -v "lnujj_l2_softDrop_mass" -V "lnujj_LV_mass"  -b 20  -x {minMJJ} -X {maxMJJ}  samples'.format(template=template,cut=cut,rootFile=mjjFile,minMJJ=minMJJ,maxMJJ=maxMJJ)
        os.system(cmd)


    for l in leptons:    
#        for p in purities:
        for c in categories:
            if addCut=='':
                cut='*'.join([cuts['common'],cuts[l],cuts[c]])
            else:
                cut='*'.join([cuts['common'],addCut,cuts[l],cuts[c]])

            rootFile="tmp.root"
            cmd='vvMakeData.py -s "{samples}"  -c "{cut}"  -o "{rootFile}" -v "lnujj_LV_mass" -b "{bins}" -m "{mini}" -M "{maxi}"  -n "{name}"  -d 0 samples'.format(samples=template,cut=cut,rootFile=rootFile,bins=100,mini=600,maxi=maxMVV,name=name)
            os.system(cmd)
                
            jsonFile=filename+"_MVV_"+name+"_"+l+"_"+c
            cmd='vvSimpleFit.py -o {jsonFile} -i {histo} -f erfpow {rootFile}'.format(jsonFile=jsonFile,rootFile=rootFile,histo=name)
            os.system(cmd)

            rootFile=filename+"_MVVHist_"+name+"_"+l+"_"+c+".root"
            cmd="vvPDFToHisto1D.py -n histo -s 'slopeSyst_{name}:1.0:0.1' -m 'meanSyst_{name}:1.0:0.1' -w 'widthSyst_{name}:1.0:0.1' -o '{rootFile}' -b {binsMVV} -x {minMVV} -X {maxMVV}  {mvvFile}.json".format(name=name+"_"+l+"_"+c,rootFile=rootFile,binsMVV=binsMVV,minMVV=minMVV,maxMVV=maxMVV,mvvFile=jsonFile) 
            os.system(cmd)





def makeVVShapes(name,filename,template,addCut=""):
    for l in leptons:    
        for c in categories:
            if addCut=='':
                cut='*'.join([cuts['common'],cuts[l],cuts[c]])
            else:
                cut='*'.join([cuts['common'],addCut,cuts[l],cuts[c]])

            rootFile="tmp.root"
            cmd='vvMakeData.py -s "{samples}"  -c "{cut}"  -o "{rootFile}" -v "lnujj_LV_mass" -b "{bins}" -m "{mini}" -M "{maxi}"  -n "{name}"  -d 0 samples'.format(samples=template,cut=cut,rootFile=rootFile,bins=100,mini=600,maxi=maxMVV,name=name)
            os.system(cmd)
                
            jsonFile=filename+"_MVV_"+name+"_"+l+"_"+c
            cmd='vvSimpleFit.py -o {jsonFile} -i {histo} -f erfpow {rootFile}'.format(jsonFile=jsonFile,rootFile=rootFile,histo=name)
            os.system(cmd)

            rootFile=filename+"_MVVHist_"+name+"_"+l+"_"+c+".root"
            cmd="vvPDFToHisto1D.py -n histo -s 'slopeSyst_{name}:1.0:0.1' -m 'meanSyst_{name}:1.0:0.1' -w 'widthSyst_{name}:1.0:0.1' -o '{rootFile}' -b {binsMVV} -x {minMVV} -X {maxMVV}  {mvvFile}.json".format(name=name+"_"+l+"_"+c,rootFile=rootFile,binsMVV=binsMVV,minMVV=minMVV,maxMVV=maxMVV,mvvFile=jsonFile) 
            os.system(cmd)
def makeNormalizations(name,filename,template,data=0,addCut='',factor=1):
    for lepton in leptons:
        for purity in purities:
            for region in categories:
                rootFile=filename+"_"+lepton+"_"+purity+"_"+region+".root"
                if addCut=='':
                    cut='*'.join([cuts['common'],cuts[purity],cuts[lepton],cuts[region],cuts['acceptance']])
                else:
                    cut='*'.join([cuts['common'],cuts[purity],cuts[lepton],cuts[region],addCut,cuts['acceptance']])
                cmd='vvMakeData.py -s "{samples}" -d {data} -c "{cut}"  -o "{rootFile}" -v "lnujj_LV_mass,lnujj_l2_softDrop_mass" -b "{BINS},{bins}" -m "{MINI},{mini}" -M "{MAXI},{maxi}" -f {factor} -n "{name}"  samples'.format(samples=template,cut=cut,rootFile=rootFile,BINS=binsMVV,bins=binsMJJ,MINI=minMVV,MAXI=maxMVV,mini=minMJJ,maxi=maxMJJ,factor=factor,name=name,data=data)
                os.system(cmd)




def estimateSystematicsCorrelations(tau21factor,bfactor):
    print 'Estimate the effect of 10% of tau21 in the different categories'

    for sample in ["BulkGravToWWToWlepWhad_narrow_2000"]:
        for purity in purities:
            denom='*'.join([cuts['common'],cuts['acceptance']])           
            print 'Tau21 - Sample:',sample,purity
            cmd='vvEstimateSystematicsCorrelations.py -s "{sample}" -d "{denom}" -n "{num}" -v "lnujj_l2_tau2/lnujj_l2_tau1" -f {factor} samples'.format(sample=sample,denom=denom,num='*'.join([cuts[purity]]),factor=tau21factor)
            os.system(cmd)


            print 'btagged - Sample:',sample,purity
            cmd='vvEstimateSystematicsCorrelations.py -s "{sample}" -d "{denom}" -n "{num}" -v "lnujj_highestOtherBTag" -f {factor} samples'.format(sample=sample,denom=denom,num='lnujj_highestOtherBTag>0.8',factor=bfactor)
            os.system(cmd)

            print 'no-btagged - Sample:',sample,purity
            cmd='vvEstimateSystematicsCorrelations.py -s "{sample}" -d "{denom}" -n "{num}" -v "lnujj_highestOtherBTag" -f {factor} samples'.format(sample=sample,denom=denom,num='lnujj_nCentralJets==0||lnujj_highestOtherBTag<0.8',factor=bfactor)
            os.system(cmd)


    for sample in [WJetsTemplate]:
        for purity in purities:
            denom='*'.join([cuts['common'],cuts['acceptance']])
            print 'Sample:',sample,purity,'quarks'
            cmd='vvEstimateSystematicsCorrelations.py -s "{sample}" -d "{denom}" -n "{num}" -v "lnujj_l2_tau2/lnujj_l2_tau1" -f {factor} samples'.format(sample=sample,denom=denom,num='*'.join([cuts[purity]]),factor=tau21factor)
            os.system(cmd)

            print 'btagged - Sample:',sample,purity
            cmd='vvEstimateSystematicsCorrelations.py -s "{sample}" -d "{denom}" -n "{num}" -v "lnujj_highestOtherBTag" -f {factor} samples'.format(sample=sample,denom=denom,num='lnujj_highestOtherBTag>0.8',factor=bfactor)
            os.system(cmd)

            print 'no-btagged - Sample:',sample,purity
            cmd='vvEstimateSystematicsCorrelations.py -s "{sample}" -d "{denom}" -n "{num}" -v "lnujj_highestOtherBTag" -f {factor} samples'.format(sample=sample,denom=denom,num='lnujj_nCentralJets==0||lnujj_highestOtherBTag<0.8',factor=bfactor)
            os.system(cmd)



    for sample in [topTemplateExt]:
        for purity in purities:
            
            denom='*'.join([cuts['common'],cuts['acceptance'],'lnujj_l2_mergedVTruth&&lnujj_l2_nearestBDRTruth>0.8'])
            print 'Merged Top',purity
            print 'Sample:',sample
            cmd='vvEstimateSystematicsCorrelations.py -s "{sample}" -d "{denom}" -n "{num}" -v "lnujj_l2_tau2/lnujj_l2_tau1" -f {factor} samples'.format(sample=sample,denom=denom,num='*'.join([cuts[purity]]),factor=tau21factor)
            os.system(cmd)


            print 'btagged - Sample:',sample,purity
            cmd='vvEstimateSystematicsCorrelations.py -s "{sample}" -d "{denom}" -n "{num}" -v "lnujj_highestOtherBTag" -f {factor} samples'.format(sample=sample,denom=denom,num='lnujj_highestOtherBTag>0.8',factor=bfactor)
            os.system(cmd)

            print 'no-btagged - Sample:',sample,purity
            cmd='vvEstimateSystematicsCorrelations.py -s "{sample}" -d "{denom}" -n "{num}" -v "lnujj_highestOtherBTag" -f {factor} samples'.format(sample=sample,denom=denom,num='lnujj_nCentralJets==0||lnujj_highestOtherBTag<0.8',factor=bfactor)
            os.system(cmd)


            denom='*'.join([cuts['common'],cuts['acceptance'],'!(lnujj_l2_mergedVTruth&&lnujj_l2_nearestBDRTruth>0.8)'])
            print 'Other Top',purity
            print 'Sample:',sample
            cmd='vvEstimateSystematicsCorrelations.py -s "{sample}" -d "{denom}" -n "{num}" -v "lnujj_l2_tau2/lnujj_l2_tau1" -f {factor} samples'.format(sample=sample,denom=denom,num='*'.join([cuts[purity]]),factor=tau21factor)
            os.system(cmd)

            print 'btagged - Sample:',sample,purity
            cmd='vvEstimateSystematicsCorrelations.py -s "{sample}" -d "{denom}" -n "{num}" -v "lnujj_highestOtherBTag" -f {factor} samples'.format(sample=sample,denom=denom,num='lnujj_highestOtherBTag>0.8',factor=bfactor)
            os.system(cmd)

            print 'no-btagged - Sample:',sample,purity
            cmd='vvEstimateSystematicsCorrelations.py -s "{sample}" -d "{denom}" -n "{num}" -v "lnujj_highestOtherBTag" -f {factor} samples'.format(sample=sample,denom=denom,num='lnujj_nCentralJets==0||lnujj_highestOtherBTag<0.8',factor=bfactor)
            os.system(cmd)




#makeSignalShapesMVV("LNuJJ_XWW",WWTemplate)
#makeSignalShapesMJJ("LNuJJ_XWW",WWTemplate)
#makeSignalShapesMVV("LNuJJ_XWZ",WZTemplate)
#makeSignalShapesMJJ("LNuJJ_XWZ",WZTemplate)
#makeSignalYields("LNuJJ_XWW",WWTemplate,BRWW)
#makeSignalYields("LNuJJ_XWZ",WZTemplate,BRWZ)


#makeBackgroundShapesMJJNoL("Wjets","LNuJJ",WJetsTemplate,"")
#makeBackgroundShapesMVVNoP("Wjets","LNuJJ",WJetsTemplate,"")
#makeBackgroundShapesHisto("Wjets","LNuJJ")

#makeTopShapes2("topRes","LNuJJ",topTemplate,"(lnujj_l2_mergedVTruth==1&&lnujj_l2_nearestBDRTruth>0.8)")


#makeBackgroundShapesMJJNoL("topNonRes","LNuJJ",topTemplate,"(!(lnujj_l2_mergedVTruth&&lnujj_l2_nearestBDRTruth>0.8))")
#makeBackgroundShapesMVVPerCat("topNonRes","LNuJJ",topTemplate,"(!(lnujj_l2_mergedVTruth&&lnujj_l2_nearestBDRTruth>0.8))")
#makeBackgroundShapesHistoWithCat("topNonRes","LNuJJ")

#makeVVShapes("WW","LNuJJ",SMWWTemplate)
#makeVVShapes("WZ","LNuJJ",SMWZTemplate)
makeNormalizations("Wjets","LNuJJ",WJetsTemplate,0,'',0.82)
makeNormalizations("topRes","LNuJJ",topTemplate,0,"lnujj_l2_mergedVTruth&&lnujj_l2_nearestBDRTruth>0.8")
makeNormalizations("topNonRes","LNuJJ",topTemplate,0,"!(lnujj_l2_mergedVTruth&&lnujj_l2_nearestBDRTruth>0.8)")
makeNormalizations("top","LNuJJ",topTemplate,0)
makeNormalizations("data","LNuJJ",dataTemplate,1)
makeNormalizations("WW","LNuJJ",SMWWTemplate,0)
makeNormalizations("WZ","LNuJJ",SMWZTemplate,0)

#estimateSystematicsCorrelations(1.2,1.1)
