
import ROOT
import os




cuts={}

cuts['common'] = '((HLT_HT800||HLT_HT900)&&Flag_goodVertices&&Flag_CSCTightHaloFilter&&Flag_HBHENoiseFilter&&Flag_HBHENoiseIsoFilter&&Flag_eeBadScFilter&&jj_nOtherLeptons==0)'
cuts['HP'] = '(jj_l1_tau2/jj_l1_tau1<0.45&&jj_l2_tau2/jj_l2_tau1<0.45)'
cuts['LP'] = '((jj_l1_tau2/jj_l1_tau1<0.45&&jj_l2_tau2/jj_l2_tau1>0.45&&jj_l2_tau2/jj_l2_tau1<0.75)||(jj_l2_tau1/jj_l2_tau1<0.45&&jj_l1_tau2/jj_l1_tau1>0.45&&jj_l1_tau2/jj_l1_tau1<0.75))'
cuts['WW'] = '(jj_l1_pruned_mass>65&&jj_l1_pruned_mass<85&&jj_l2_pruned_mass>65&&jj_l2_pruned_mass<85)'
cuts['WZ'] = '((jj_l1_pruned_mass>65&&jj_l1_pruned_mass<85&&jj_l2_pruned_mass>85&&jj_l2_pruned_mass<105)||(jj_l2_pruned_mass>65&&jj_l2_pruned_mass<85&&jj_l1_pruned_mass>85&&jj_l1_pruned_mass<105))'
cuts['ZZ'] = '(jj_l1_pruned_mass>85&&jj_l1_pruned_mass<105&&jj_l2_pruned_mass>85&&jj_l2_pruned_mass<105)'

purities=['HP','LP']
categories=['WW','WZ','ZZ']


WWTemplate="BulkGravToWW_narrow"
BRWW=1
WZTemplate="WprimeToWZ_narrow"
BRWZ=1

dataTemplate="JetHT"



minMJJ=40.0
maxMJJ=105.0

minMVV=1000.0
maxMVV=5000.0


binsMJJ=40
binsMVV=120



def makeSignalShapes(filename,template):

    cut='&&'.join([cuts['common']])
    rootFile=filename+".root"
    cmd='vvSignalParam2D.py -s "{template}" -c "{cut}"  -o "{rootFile}" -V "jj_LV_mass"  -v "jj_l2_pruned_mass"  -m {minMJJ} -M {maxMJJ}  samples'.format(template=template,cut=cut,rootFile=rootFile,minMJJ=minMJJ,maxMJJ=maxMJJ)
    os.system(cmd)
    jsonFile=filename+".json"
    cmd='vvMakeJSON.py  -o "{jsonFile}" -g "MEAN:pol1,SIGMA:pol2,ALPHA1:pol3,N1:pol0,ALPHA2:pol4,N2:pol0,mean:pol4,sigma:pol4,alpha:pol3,n:pol0,slope:pol4,f:pol4"  -m 1000 -M 5000 {rootFile}  '.format(jsonFile=jsonFile,rootFile=rootFile)
    os.system(cmd)


def makeSignalYields(filename,template,branchingFraction):
    for purity in purities:
        for region in categories:
            cut = "&&".join([cuts[purity],cuts['common'],cuts[region]])
                #Signal yields
            yieldFile=filename+"_"+purity+"_"+region+"_yield"
            cmd='vvMakeSignalYields.py -s {template} -c "{cut}" -o {output} -V "jj_LV_mass" -m {minMVV} -M {maxMVV} -f "pol3" -b {BR} -x 1000.0 samples'.format(template=template, cut=cut, output=yieldFile,minMVV=minMVV,maxMVV=maxMVV,BR=branchingFraction)
            os.system(cmd)



def makeNormalizations(name,filename,template,data=0,addCut=''):
    for purity in purities:
        for region in categories:
            rootFile=filename+"_"+purity+"_"+region+".root"
            if addCut=='':
                cut='&&'.join([cuts['common'],cuts[purity],cuts[region]])
            else:
                cut='&&'.join([cuts['common'],cuts[purity],cuts[region],addCut])
            cmd='vvMakeData.py -s "{samples}" -d {data} -c "{cut}"  -o "{rootFile}" -v "jj_LV_mass" -b "{BINS}" -m "{MINI}" -M "{MAXI}" -f {factor} -n "{name}"  samples'.format(samples=template,cut=cut,rootFile=rootFile,BINS=binsMVV,MINI=minMVV,MAXI=maxMVV,factor=1.0,name=name,data=data)
            os.system(cmd)


              


#makeSignalShapes("JJ_XWW",WWTemplate)
#makeSignalYields("JJ_XWW",WWTemplate,BRWW)
makeNormalizations("data","JJ",dataTemplate,1)

