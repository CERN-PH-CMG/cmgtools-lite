import ROOT
ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")
from CMGTools.VVResonances.statistics.DataCardMaker import DataCardMaker
cmd='combineCards.py '



for lepton in ['e','mu']:
    for purity in ['HP','LP']:
        for category in ['nob','b']:
            card=DataCardMaker(lepton,purity,'13TeV',12900,category)
            cat='_'.join([category,lepton,purity,'13TeV'])
            cmd=cmd+" "+cat+'=datacard_'+cat+'.txt '
         
            #WW signal-MVV
            card.addMVVSignalParametricShape("XWW_MVV","MLNuJ","LNuJJ_XWW_MVV_"+lepton+".json",{'CMS_scale_j':1,'CMS_scale_MET':1.0},{'CMS_res_j':1.0,'CMS_res_MET':1.0})
            card.addMJJSignalParametricShape("Wqq","MJ","LNuJJ_XWW_MJJ_"+purity+".json",{'CMS_scale_prunedj_0':1,'CMS_scale_prunedj_1':'MH'},{'CMS_res_prunedj_0':1.0,'CMS_res_prunedj_1':'MH'})
            card.product("XWW","Wqq","XWW_MVV")
            card.addParametricYield("XWW",0,"LNuJJ_XWW_"+lepton+"_"+purity+"_"+category+"_yield.json")
#            card.addParametricYieldWithCrossSection("XWW",0,"LNuJJ_XWW_"+lepton+"_"+purity+"_"+category+"_yield.json",'sigma_hvt.json','sigma0','BRWW')

            #WZ signal-MVV

#            card.addMVVSignalParametricShape("XWZ_MVV","MLNuJ","LNuJJ_XWZ_MVV_"+lepton+".json",{'CMS_scale_j':1,'CMS_scale_MET':1.0},{'CMS_res_j':1.0,'CMS_res_MET':1.0})
#            card.addMJJSignalParametricShape("Zqq","MJ","LNuJJ_XWZ_MJJ_"+purity+".json",{'CMS_scale_prunedj_0':1,'CMS_scale_prunedj_1':'MH'},{'CMS_res_prunedj_0':1.0,'CMS_res_prunedj_1':'MH'})
#            card.product("XWZ","Zqq","XWZ_MVV")
#            card.addParametricYield("XWZ",0,"LNuJJ_XWZ_"+lepton+"_"+purity+"_"+category+"_yield.json")



            #W+jets
            rootFile="LNuJJ_MVVHist_Wjets_"+lepton+"_"+purity+".root"
            card.addHistoShapeFromFile("Wjets",["MLNuJ","MJ"],rootFile,"histo",["slopeSyst_Wjets_"+lepton,"widthSyst_Wjets_"+lepton,"meanSyst0_Wjets_"+lepton,"meanSyst1_Wjets_"+lepton,"slopeSystMJJ_Wjets_"+purity,"widthSystMJJ_Wjets_"+purity,"meanSystMJJ_Wjets_"+purity],False,2)       
            card.addFixedYieldFromFile("Wjets",1,"LNuJJ_"+lepton+"_"+purity+"_"+category+".root","Wjets")


            #TOP RES
            card.addMJJSignalParametricShapeCB("WqqTop","MJ","LNuJJ_MJJ_topRes_"+purity+".json",{'CMS_scale_prunedj_0':1,'CMS_scale_prunedj_1':'MLNuJ'},{'CMS_res_prunedj_0':1.0,'CMS_res_prunedj_1':'MLNuJ'},"MLNuJ")

            rootFile="LNuJJ_MVVHist_topRes_"+lepton+"_"+category+".root"
            card.addHistoShapeFromFile("topRes_MVV",["MLNuJ"],rootFile,"histo",["slopeSyst_topRes_"+lepton+"_"+category,"widthSyst_topRes_"+lepton+"_"+category,"meanSyst_topRes_"+lepton+"_"+category],False,2)       
            card.conditionalProduct("topRes","WqqTop","MLNuJ","topRes_MVV")
            card.addFixedYieldFromFile("topRes",2,"LNuJJ_"+lepton+"_"+purity+"_"+category+".root","topRes")



            #SM WW
            card.addMJJSignalParametricShape("WqqVV","MJ","LNuJJ_XWW_MJJ_"+purity+".json",{'CMS_scale_prunedj_0':1,'CMS_scale_prunedj_1':'MH'},{'CMS_res_prunedj_0':1.0,'CMS_res_prunedj_1':'MH'},"MLNuJ")

            rootFile="LNuJJ_MVVHist_WW_"+lepton+"_"+category+".root"
            card.addHistoShapeFromFile("WW_MVV",["MLNuJ"],rootFile,"histo",[],False,2)       
            card.conditionalProduct("WW","WqqVV","MLNuJ","WW_MVV")
            card.addFixedYieldFromFile("WW",3,"LNuJJ_"+lepton+"_"+purity+"_"+category+".root","WW")

            #SM WZ RES
            card.addMJJSignalParametricShape("ZqqVV","MJ","LNuJJ_XWZ_MJJ_"+purity+".json",{'CMS_scale_prunedj_0':1,'CMS_scale_prunedj_1':'MH'},{'CMS_res_prunedj_0':1.0,'CMS_res_prunedj_1':'MH'},"MLNuJ")

            rootFile="LNuJJ_MVVHist_WZ_"+lepton+"_"+category+".root"
            card.addHistoShapeFromFile("WZ_MVV",["MLNuJ"],rootFile,"histo",[],False,2)       
            card.conditionalProduct("WZ","ZqqVV","MLNuJ","WZ_MVV")
            card.addFixedYieldFromFile("WZ",4,"LNuJJ_"+lepton+"_"+purity+"_"+category+".root","WZ")

            #TOP NONRES
            rootFile="LNuJJ_MVVHist_topNonRes_"+lepton+"_"+purity+"_"+category+".root"
            if purity=="HP":
                card.addHistoShapeFromFile("topNonRes",["MLNuJ","MJ"],rootFile,"histo",["slopeSyst_topNonRes_"+lepton+"_"+category,"widthSyst_topNonRes_"+lepton+"_"+category,"meanSyst0_topNonRes_"+lepton+"_"+category,"meanSyst1_topNonRes_"+lepton+"_"+category,"slopeSystMJJ_topNonRes_"+purity,"widthSystMJJ_topNonRes_"+purity,"meanSystMJJ_topNonRes_"+purity],False,2)       
            else:
                card.addHistoShapeFromFile("topNonRes",["MLNuJ","MJ"],rootFile,"histo",["slopeSyst_topNonRes_"+lepton+"_"+category,"widthSyst_topNonRes_"+lepton+"_"+category,"meanSyst0_topNonRes_"+lepton+"_"+category,"meanSyst1_topNonRes_"+lepton+"_"+category,"slopeSystMJJ_topNonRes_"+purity],False,2)       

            card.addFixedYieldFromFile("topNonRes",5,"LNuJJ_"+lepton+"_"+purity+"_"+category+".root","topNonRes")

            #DATA
            card.importBinnedData("LNuJJ_"+lepton+"_"+purity+"_"+category+".root","data",["MLNuJ","MJ"])


            #####
            #####SYSTEMATICS

            #luminosity
            card.addSystematic("CMS_lumi","lnN",{'XWW':1.04,'XWZ':1.04,'WW':1.04,'WZ':1.04,'Wjets':1.04,'topRes':1.04,'topNonRes':1.04})

            #lepton efficiency
            card.addSystematic("CMS_eff_"+lepton,"lnN",{'XWW':1.02,'XWZ':1.02,'WW':1.02,'WZ':1.02,'Wjets':1.02,'topRes':1.02,'topNonRes':1.02})


            #W+jets cross section in acceptance-dominated by pruned mass
            card.addSystematic("CMS_Wjets_sigma","lnN",{'Wjets':1.3})
            card.addSystematic("CMS_VV_sigma","lnN",{'WW':1.3,'WZ':1.3})

            if category=='b':
                card.addSystematic("CMS_Wbb_sigma","lnN",{'Wjets':1.5})


            #Tau21_fake    
            if purity=='HP':
                card.addSystematic("CMS_tau21_fake","lnN",{'Wjets':1+0.37})
            if purity=='LP':
                card.addSystematic("CMS_tau21_fake","lnN",{'Wjets':1-0.42})
                

            #Top cross section    
            card.addSystematic("CMS_top_sigma","lnN",{'topRes':1.3,'topNonRes':1.3})
            #Top activity in the event     
            card.addSystematic("CMS_top_activity","lnN",{'topRes':1.9,'topNonRes':0.1})

            #tau21 
            if purity=='HP':
                card.addSystematic("CMS_tau21_eff","lnN",{'topRes':1+0.13,'XWW':1+0.13,'XWZ':1+0.13,'WW':1+0.13,'WZ':1+0.13})
                card.addSystematic("CMS_tau21_fakeTop","lnN",{'topNonRes':1+0.25})

            if purity=='LP':
                card.addSystematic("CMS_tau21_eff","lnN",{'topRes':1-0.94,'XWW':1-0.94,'XWZ':1-0.94,'WW':1-0.94,'WZ':1-0.94})
                card.addSystematic("CMS_tau21_fakeTop","lnN",{'topNonRes':1-0.53})


            if category=='b':
                card.addSystematic("CMS_btag_eff","lnN",{'topRes':1.18,'topNonRes':1.18})
                card.addSystematic("CMS_btag_fake","lnN",{'Wjets':1.3,'XWW':1.3,'XWZ':1.3 ,'WW':1.3,'WZ':1.3})
            else:
                card.addSystematic("CMS_btag_eff","lnN",{'topRes':0.70,'topNonRes':0.70})
                card.addSystematic("CMS_btag_fake","lnN",{'Wjets':0.98,'XWW':0.98,'XWZ':0.98,'WW':0.98,'WZ':0.98})
               
            #pruned mass scale    
            card.addSystematic("CMS_scale_j","param",[0.0,0.02])
            card.addSystematic("CMS_res_j","param",[0.0,0.05])
            card.addSystematic("CMS_scale_prunedj_0","param",[0.0,0.1])
            card.addSystematic("CMS_res_prunedj_0","param",[0.0,0.2])
            card.addSystematic("CMS_scale_prunedj_1","param",[0.0,4e-6])
            card.addSystematic("CMS_res_prunedj_1","param",[0.0,1e-5])
            card.addSystematic("CMS_scale_MET","param",[0.0,0.02])
            card.addSystematic("CMS_res_MET","param",[0.0,0.01])



            card.addSystematic("slopeSyst_Wjets_"+lepton,"param",[0.0,0.333])
            card.addSystematic("meanSyst0_Wjets_"+lepton,"param",[0.0,0.333])
            card.addSystematic("meanSyst1_Wjets_"+lepton,"param",[0.0,0.333])
            card.addSystematic("widthSyst_Wjets_"+lepton,"param",[0.0,0.333])

            card.addSystematic("slopeSystMJJ_Wjets_"+purity,"param",[0.0,0.333])
            card.addSystematic("meanSystMJJ_Wjets_"+purity,"param",[0.0,0.333])
            card.addSystematic("widthSystMJJ_Wjets_"+purity,"param",[0.0,0.333])

            card.addSystematic("slopeSyst_topNonRes_"+lepton+"_"+category,"param",[0.0,0.333])
            card.addSystematic("meanSyst0_topNonRes_"+lepton+"_"+category,"param",[0.0,0.333])
            card.addSystematic("meanSyst1_topNonRes_"+lepton+"_"+category,"param",[0.0,0.333])
            card.addSystematic("widthSyst_topNonRes_"+lepton+"_"+category,"param",[0.0,0.333])

            card.addSystematic("slopeSystMJJ_topNonRes_"+purity,"param",[0.0,0.333])
            if purity=='HP':
                card.addSystematic("meanSystMJJ_topNonRes_"+purity,"param",[0.0,0.333])
                card.addSystematic("widthSystMJJ_topNonRes_"+purity,"param",[0.0,0.333])

            card.addSystematic("slopeSyst_topRes_"+lepton+"_"+category,"param",[0.0,0.333])
            card.addSystematic("meanSyst_topRes_"+lepton+"_"+category,"param",[0.0,0.333])
            card.addSystematic("widthSyst_topRes_"+lepton+"_"+category,"param",[0.0,0.333])


            card.makeCard()

#make combined cards



print cmd
            
