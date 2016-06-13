
import ROOT
import os




cuts={}

cuts['common'] = '(HLT_MU||HLT_ELE)&&Flag_goodVertices&&Flag_CSCTightHaloFilter&&Flag_HBHENoiseFilter&&Flag_HBHENoiseIsoFilter&&Flag_eeBadScFilter&&lnujj_nOtherLeptons==0'
cuts['mu'] = 'abs(lnujj_l1_l_pdgId)==13'
cuts['e'] = 'abs(lnujj_l1_l_pdgId)==11'
cuts['HP'] = 'lnujj_l2_tau2/lnujj_l2_tau1<0.6'
cuts['LP'] = 'lnujj_l2_tau2/lnujj_l2_tau1>0.6&&lnujj_l2_tau2/lnujj_l2_tau1<0.75'
cuts['nob'] = 'lnujj_nMediumBTags==0'
cuts['b'] = 'lnujj_nMediumBTags>0'

leptons=['mu','e']
purities=['HP','LP']
categories=['nob','b']


WWTemplate="BulkGravToWWToWlepWhad_narrow"
BRWW=2*2.*0.322*0.6760

WZTemplate="WprimeToWZ_narrow"
BRWZ=1

WHTemplate="WprimeToWhToWlephbb"
BRWH=0.577*0.322


dataTemplate="SingleMuon,SingleElectron"
topTemplate="TTJets."
topTemplateExt="TTJets.,TTJets_ext"

WJetsTemplate="WJetsToLNu_HT"



minMJJ=40.0
maxMJJ=160.0

minMVV=600.0
maxMVV=4600.0


binsMJJ=40
binsMVV=100


cuts['acceptance']= "lnujj_LV_mass>{minMVV}&&lnujj_LV_mass<{maxMVV}&&lnujj_l2_pruned_mass>{minMJJ}&&lnujj_l2_pruned_mass<{maxMJJ}".format(minMVV=minMVV,maxMVV=maxMVV,minMJJ=minMJJ,maxMJJ=maxMJJ)                
cuts['acceptanceMJJ']= "lnujj_l2_pruned_mass>{minMJJ}&&lnujj_l2_pruned_mass<{maxMJJ}".format(minMJJ=minMJJ,maxMJJ=maxMJJ)                



def makeSignalShapes(filename,template):
    for l in leptons:
        for p in purities:
            cut='&&'.join([cuts['common'],cuts[l],cuts[p]])
            rootFile=filename+"_"+l+"_"+p+".root"
            cmd='vvSignalParam2D.py -s "{template}" -c "{cut}"  -o "{rootFile}" -V "lnujj_LV_mass"  -v "lnujj_l2_pruned_mass"  -m {minMJJ} -M {maxMJJ}  samples'.format(template=template,cut=cut,rootFile=rootFile,minMJJ=minMJJ,maxMJJ=maxMJJ)
            os.system(cmd)
            jsonFile=filename+"_"+l+"_"+p+".json"
            cmd='vvMakeJSON.py  -o "{jsonFile}" -g "MEAN:pol1,SIGMA:pol2,ALPHA1:pol3,N1:pol0,ALPHA2:pol4,N2:pol0,mean:pol4,sigma:pol4,alpha:pol3,n:pol0,slope:pol4,f:pol4"  {rootFile}  '.format(jsonFile=jsonFile,rootFile=rootFile)
            os.system(cmd)


def makeSignalYields(filename,template,branchingFraction):
    for lepton in leptons:
        for purity in purities:
            for region in categories:
                cut = "&&".join([cuts[lepton],cuts[purity],cuts['common'],cuts[region],cuts['acceptance']])
                #Signal yields
                yieldFile=filename+"_"+lepton+"_"+purity+"_"+region+"_yield"
                cmd='vvMakeSignalYields.py -s {template} -c "{cut}" -o {output} -V "lnujj_LV_mass" -m {minMVV} -M {maxMVV} -f "pol7" -b {BR} samples'.format(template=template, cut=cut, output=yieldFile,minMVV=minMVV,maxMVV=maxMVV,BR=branchingFraction)
                os.system(cmd)



def makeBackgroundShapes(name,filename,template,addCut=""):
    for l in leptons:
        for p in purities:
            if addCut=='':
                cut='&&'.join([cuts['common'],cuts[p],cuts[l]])
            else:
                cut='&&'.join([cuts['common'],cuts[p],cuts[l],addCut])
                
            mvvFile=filename+"_MVV_"+name+"_"+l+"_"+p
            cmd='vvMakeBackgroundMVVConditionalShapes.py -s "{template}" -c "{cut}"  -o "{rootFile}" -v "lnujj_LV_mass" -V "lnujj_l2_pruned_mass"  -b 100  -x {minMVV} -X {maxMVV}   -B 8 -y {minMJJ} -Y {maxMJJ}   samples'.format(template=template,cut=cut,rootFile=mvvFile,minMVV=minMVV,maxMVV=maxMVV,minMJJ=minMJJ,maxMJJ=maxMJJ)
            os.system(cmd)




            if addCut=='':
                cut='&&'.join([cuts['common'],cuts[p],cuts[l],cuts['acceptance']])
            else:
                cut='&&'.join([cuts['common'],cuts[p],cuts[l],addCut,cuts['acceptance']])


            if p=="HP":
                function='erfexp'
#                if name.find('top')!=-1:
#                    function='erfexpCB'
                    
            if p=="LP":
                function='erfexp'
                if name.find('top')!=-1:
                    function='expo'

            rootFile="tmp.root"
            cmd='vvMakeData.py -s "{samples}"  -c "{cut}"  -o "{rootFile}" -v "lnujj_l2_pruned_mass" -b "{bins}" -m "{mini}" -M "{maxi}"  -n "{name}"  -d 0 samples'.format(samples=template,cut=cut,rootFile=rootFile,bins=binsMJJ,mini=minMJJ,maxi=maxMJJ,name=name)
            os.system(cmd)
            
            jsonFile=filename+"_MJJ_"+name+"_"+l+"_"+p
            cmd='vvSimpleFit.py -o {jsonFile} -i {histo} -f {function} {rootFile}'.format(jsonFile=jsonFile,rootFile=rootFile,histo=name,function=function)
            os.system(cmd)

def makeBackgroundShapesPerCat(name,filename,template,addCut=""):
    for l in leptons:
        for p in purities:
            for c in categories:

                if addCut=='':
                    cut='&&'.join([cuts['common'],cuts[p],cuts[l],cuts[c]])
                else:
                    cut='&&'.join([cuts['common'],cuts[p],cuts[l],cuts[c],addCut])
                
                mvvFile=filename+"_MVV_"+name+"_"+l+"_"+p+"_"+c
                cmd='vvMakeBackgroundMVVConditionalShapes.py -s "{template}" -c "{cut}"  -o "{rootFile}" -v "lnujj_LV_mass" -V "lnujj_l2_pruned_mass"  -b 100  -x {minMVV} -X {maxMVV}   -B 8 -y {minMJJ} -Y {maxMJJ}   samples'.format(template=template,cut=cut,rootFile=mvvFile,minMVV=minMVV,maxMVV=maxMVV,minMJJ=minMJJ,maxMJJ=maxMJJ)
                os.system(cmd)




                if addCut=='':
                    cut='&&'.join([cuts['common'],cuts[p],cuts[l],cuts[c],cuts['acceptance']])
                else:
                    cut='&&'.join([cuts['common'],cuts[p],cuts[l],addCut,cuts[c],cuts['acceptance']])


                if p=="HP":
                    function='erfexp'
                    
                if p=="LP":
                    function='expo'

                rootFile="tmp.root"
                cmd='vvMakeData.py -s "{samples}"  -c "{cut}"  -o "{rootFile}" -v "lnujj_l2_pruned_mass" -b "{bins}" -m "{mini}" -M "{maxi}"  -n "{name}"  -d 0 samples'.format(samples=template,cut=cut,rootFile=rootFile,bins=binsMJJ,mini=minMJJ,maxi=maxMJJ,name=name)
                os.system(cmd)
            
                jsonFile=filename+"_MJJ_"+name+"_"+l+"_"+p+"_"+c
                cmd='vvSimpleFit.py -o {jsonFile} -i {histo} -f {function} {rootFile}'.format(jsonFile=jsonFile,rootFile=rootFile,histo=name,function=function)
                os.system(cmd)




def makeTopShapes(name,filename,template,addCut=""):

    for p in purities:
        if p=='HP':
            if addCut=='':
                cut='&&'.join([cuts['common'],cuts[p]])
            else:
                cut='&&'.join([cuts['common'],cuts[p],addCut])
        else:
            if addCut=='':
                cut='&&'.join([cuts['common']])
            else:
                cut='&&'.join([cuts['common'],addCut])
                       
        mjjFile=filename+"_MJJ_"+name+"_"+p
        cmd='vvMakeTopMJJConditionalShapes.py -s "{template}" -c "{cut}"  -o "{rootFile}" -v "lnujj_l2_pruned_mass" -V "lnujj_LV_mass"  -b 20  -x {minMJJ} -X {maxMJJ}   -B 5 -y {minMVV} -Y {maxMVV}   samples'.format(template=template,cut=cut,rootFile=mjjFile,minMVV=minMVV,maxMVV=2000,minMJJ=minMJJ,maxMJJ=maxMJJ)
        os.system(cmd)


    for l in leptons:    
        for p in purities:
            if addCut=='':
                cut='&&'.join([cuts['common'],cuts[p],cuts[l]])
            else:
                cut='&&'.join([cuts['common'],cuts[p],addCut,cuts[l]])

            rootFile="tmp.root"
            cmd='vvMakeData.py -s "{samples}"  -c "{cut}"  -o "{rootFile}" -v "lnujj_LV_mass" -b "{bins}" -m "{mini}" -M "{maxi}"  -n "{name}"  -d 0 samples'.format(samples=template,cut=cut,rootFile=rootFile,bins=100,mini=500,maxi=maxMVV,name=name)
            os.system(cmd)
            
            jsonFile=filename+"_MVV_"+name+"_"+l+"_"+p
            cmd='vvSimpleFit.py -o {jsonFile} -i {histo} -f erfpow {rootFile}'.format(jsonFile=jsonFile,rootFile=rootFile,histo=name)
            os.system(cmd)



#def makeTopShapesNew(name,filename,template,addCut=""):
#    for l in leptons:
#        for p in purities:
#            if addCut=='':
#                cut='&&'.join([cuts['common'],cuts[p],cuts[l]])
#            else:
#                cut='&&'.join([cuts['common'],cuts[p],addCut,cuts[l]])
#
#                
#            mjjFile=filename+"_MJJ_"+name+"_"+l+"_"+p
#            cmd='vvMakeTopMJJConditionalShapesSim.py -s "{template}" -c "{cut}"  -o "{rootFile}" -v "lnujj_l2_pruned_mass" -V "lnujj_LV_mass"  -b 40  -x {minMJJ} -X {maxMJJ}   -B 15 -y {minMVV} -Y {maxMVV}   samples'.format(template=template,cut=cut,rootFile=mjjFile,minMVV=minMVV,maxMVV=2000,minMJJ=minMJJ,maxMJJ=m#axMJJ)
#            os.system(cmd)






def makeNormalizations(name,filename,template,data=0,addCut=''):
    for lepton in leptons:
        for purity in purities:
            for region in categories:
                rootFile=filename+"_"+lepton+"_"+purity+"_"+region+".root"
                if addCut=='':
                    cut='&&'.join([cuts['common'],cuts[purity],cuts[lepton],cuts[region],cuts['acceptance']])
                else:
                    cut='&&'.join([cuts['common'],cuts[purity],cuts[lepton],cuts[region],addCut,cuts['acceptance']])
                cmd='vvMakeData.py -s "{samples}" -d {data} -c "{cut}"  -o "{rootFile}" -v "lnujj_LV_mass,lnujj_l2_pruned_mass" -b "{BINS},{bins}" -m "{MINI},{mini}" -M "{MAXI},{maxi}" -f {factor} -n "{name}"  samples'.format(samples=template,cut=cut,rootFile=rootFile,BINS=binsMVV,bins=binsMJJ,MINI=minMVV,MAXI=maxMVV,mini=minMJJ,maxi=maxMJJ,factor=1.0,name=name,data=data)
                os.system(cmd)




                   





#makeSignalShapes("LNuJJ_XWW",WWTemplate)
#makeSignalYields("LNuJJ_XWW",WWTemplate,BRWW)
#makeBackgroundShapes("Wjets_quark","LNuJJ",WJetsTemplate,"lnujj_l2_partonFlavour<21")
#makeBackgroundShapes("Wjets_gluon","LNuJJ",WJetsTemplate,"lnujj_l2_partonFlavour==21")
makeTopShapes("topRes","LNuJJ",topTemplateExt,"lnujj_l2_mergedVTruth&&lnujj_l2_nearestBDRTruth>0.8")
#makeBackgroundShapesPerCat("topNonRes","LNuJJ",topTemplateExt,"!(lnujj_l2_mergedVTruth&&lnujj_l2_nearestBDRTruth>0.8)")
#makeNormalizations("Wjets_quark","LNuJJ",WJetsTemplate,0,'lnujj_l2_partonFlavour<21')
#makeNormalizations("Wjets_gluon","LNuJJ",WJetsTemplate,0,'lnujj_l2_partonFlavour==21')
#makeNormalizations("topRes","LNuJJ",topTemplate,0,"lnujj_l2_mergedVTruth&&lnujj_l2_nearestBDRTruth>0.8")
#makeNormalizations("topNonRes","LNuJJ",topTemplate,0,"!(lnujj_l2_mergedVTruth&&lnujj_l2_nearestBDRTruth>0.8)")
#makeNormalizations("top","LNuJJ",topTemplate,0)
#makeNormalizations("data","LNuJJ",dataTemplate,1)

