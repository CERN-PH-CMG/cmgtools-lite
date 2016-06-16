import ROOT
ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")
from CMGTools.VVResonances.statistics.DataCardMaker import DataCardMaker
cmd='combineCards.py '



for purity in ['HP','LP']:
    for category in ['WW','WZ','ZZ']:
        card=DataCardMaker('dijet',purity,'13TeV',2630,category)
        cat='_'.join([category,'dijet',purity,'13TeV'])
        cmd=cmd+" "+cat+'=datacard_'+cat+'.txt '
         

        #WW signal-MVV
        card.addMVVSignalParametricShape("XWW","MVV","JJ_XWW.json",{'CMS_scale_j':1,'CMS_scale_MET':1.0},{'CMS_res_j':1.0,'CMS_res_MET':1.0})
        card.addParametricYield("XWW",0,"JJ_XWW_"+purity+"_"+category+"_yield.json")


        #QCD function
        card.addMVVBackgroundShapeQCD("QCD","MVV",logTerm=False)
        card.addFloatingYield("QCD",1,1000,mini=0,maxi=1e+9)
        card.importBinnedData("JJ_"+purity+"_"+category+".root","data",["MVV"])

            #####
            #####SYSTEMATICS

        #luminosity 
        card.addSystematic("CMS_lumi","lnN",{'XWW':1.04})

        #Tagging efficiency correlated between signal and top in each purity
        if purity=='HP':
            card.addSystematic("CMS_tau21","lnN",{'XWW':0.5})
        else:    
            card.addSystematic("CMS_tau21","lnN",{'XWW':1.5})



        #parametric systs    

        card.addSystematic("CMS_scale_j","param",[0.0,0.02])
        card.addSystematic("CMS_res_j","param",[0.0,0.05])
        card.addSystematic("CMS_scale_MET","param",[0.0,0.02])
        card.addSystematic("CMS_res_MET","param",[0.0,0.01])

        card.makeCard()

#make combined cards
print cmd
            
