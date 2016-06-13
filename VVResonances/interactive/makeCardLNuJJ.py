import ROOT
ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")
from CMGTools.VVResonances.statistics.DataCardMaker import DataCardMaker
cmd='combineCards.py '



for lepton in ['e','mu']:
    for purity in ['HP','LP']:
        for category in ['nob','b']:
            card=DataCardMaker(lepton,purity,'13TeV',2630,category)
            cat='_'.join([category,lepton,purity,'13TeV'])
            cmd=cmd+" "+cat+'=datacard_'+cat+'.txt '
         

            #WW signal-MVV
            card.addMVVSignalParametricShape("XWW_MVV","MLNuJ","LNuJJ_XWW_"+lepton+"_"+purity+".json",{'CMS_scale_j':1,'CMS_scale_MET':1.0},{'CMS_res_j':1.0,'CMS_res_MET':1.0})
            #WWsignal M-JJ
            card.addMJJSignalParametricShape("Wqq","MJ","LNuJJ_XWW_"+lepton+"_"+purity+".json",{'CMS_scale_prunedj_0':1,'CMS_scale_prunedj_1':'MH'},{'CMS_res_prunedj_0':1.0,'CMS_res_prunedj_1':'MH'})
            card.conditionalProduct("XWW","Wqq","MLNuJ","XWW_MVV")
            #parametric yield for signal
            card.addParametricYield("XWW",0,"LNuJJ_XWW_"+lepton+"_"+purity+"_"+category+"_yield.json")


            #W+jets - quark

            card.addMJJParametricBackgroundShapeErfExp("Wjets_quark_MJ","MJ","LNuJJ_MJJ_Wjets_quark_"+lepton+"_"+purity+".json",{'wMJJSlopeQ_'+lepton+"_"+purity:1.0},{'wMJJMeanQ_'+lepton+"_"+purity:1.0},{'wMJJSigmaQ_'+lepton+"_"+purity:1.0})
            card.addParametricMVVBKGShapeErfPow("Wjets_quark_MVV","MLNuJ","MJ","LNuJJ_MVV_Wjets_quark_"+lepton+"_"+purity+".json","",{'wSlope_'+lepton+"_"+purity:1.0},{'wMean0_'+lepton+"_"+purity:1.0,'wMean1_'+lepton+"_"+purity:'MJ'},{'wSigma_'+lepton+"_"+purity:1.0})            
            card.conditionalProduct("Wjets_quark","Wjets_quark_MVV","MJ","Wjets_quark_MJ")
            card.addFixedYieldFromFile("Wjets_quark",1,"LNuJJ_"+lepton+"_"+purity+"_"+category+".root","Wjets_quark")

            #W+jets - gluon
            card.addMJJParametricBackgroundShapeErfExp("Wjets_gluon_MJ","MJ","LNuJJ_MJJ_Wjets_gluon_"+lepton+"_"+purity+".json",{'wMJJSlopeG_'+lepton+"_"+purity:1.0},{'wMJJMeanG_'+lepton+"_"+purity:1.0},{'wMJJSigmaG_'+lepton+"_"+purity:1.0})
            card.addParametricMVVBKGShapeErfPow("Wjets_gluon_MVV","MLNuJ","MJ","LNuJJ_MVV_Wjets_gluon_"+lepton+"_"+purity+".json","",{'wSlope_'+lepton+"_"+purity:1.0},{'wMean0_'+lepton+"_"+purity:1.0,'wMean1_'+lepton+"_"+purity:'MJ'},{'wSigma_'+lepton+"_"+purity:1.0})            
            card.conditionalProduct("Wjets_gluon","Wjets_gluon_MVV","MJ","Wjets_gluon_MJ")
            card.addFixedYieldFromFile("Wjets_gluon",2,"LNuJJ_"+lepton+"_"+purity+"_"+category+".root","Wjets_gluon")



            #TOP RES
            card.addMJJSignalParametricShapeCB("WqqTop","MJ","LNuJJ_MJJ_topRes_"+purity+".json",{'CMS_scale_prunedj_0':1,'CMS_scale_prunedj_1':'MLNuJ'},{'CMS_res_prunedj_0':1.0,'CMS_res_prunedj_1':'MLNuJ'},"MLNuJ")
            card.addParametricMVVBKGShapeErfPow("topRes_MVV","MLNuJ","MJ","LNuJJ_MVV_topRes_"+lepton+"_"+purity+".json","",{'topResSlope_'+lepton+"_"+purity:1.0},{'topResMean_'+lepton+"_"+purity:1.0},{'topResSigma_'+lepton+"_"+purity:1.0})            
            card.conditionalProduct("topRes","WqqTop","MLNuJ","topRes_MVV")
            card.addFixedYieldFromFile("topRes",1,"LNuJJ_"+lepton+"_"+purity+"_"+category+".root","topRes")


            #TOP NONRES
            if purity=="HP":
                card.addMJJParametricBackgroundShapeErfExp("topNonRes_MJ","MJ","LNuJJ_MJJ_topNonRes_"+lepton+"_"+purity+"_"+category+".json",{'topMJJSlope_'+lepton+'_HP':1.0},{'topMJJMean_'+lepton+'_HP':1.0},{'topMJJSigma_'+lepton+'_HP':1.0})
            else:
                card.addMJJParametricBackgroundShapeExpo("topNonRes_MJ","MJ","LNuJJ_MJJ_topNonRes_"+lepton+"_"+purity+"_"+category+".json",{'topMJJSlope_'+lepton+'_LP':1.0})
            card.addParametricMVVBKGShapeErfPow("topNonRes_MVV","MLNuJ","MJ","LNuJJ_MVV_topNonRes_"+lepton+"_"+purity+"_"+category+".json","",{'topNonResSlope_'+lepton+"_"+purity:1.0},{'topNonResMean0_'+lepton+"_"+purity:1.0,'topNonResMean1_'+lepton+"_"+purity:'MJ'},{'topNonResSigma_'+lepton+"_"+purity:1.0}) 
            card.conditionalProduct("topNonRes","topNonRes_MVV","MJ","topNonRes_MJ")
            card.addFixedYieldFromFile("topNonRes",2,"LNuJJ_"+lepton+"_"+purity+"_"+category+".root","topNonRes")

            #DATA
            card.importBinnedData("LNuJJ_"+lepton+"_"+purity+"_"+category+".root","data",["MLNuJ","MJ"])


            #####
            #####SYSTEMATICS

            #luminosity
            card.addSystematic("CMS_lumi","lnN",{'XWW':1.04,'Wjets_quark':1.04,'Wjets_gluon':1.04,'topRes':1.04,'topNonRes':1.04})
            #lepton efficiency
            card.addSystematic("CMS_eff_"+lepton,"lnN",{'XWW':1.02,'Wjets_quark':1.02,'WJets_gluon':1.02,'topRes':1.02,'topNonRes':1.02})

            #W+jets cross section
            card.addSystematic("CMS_WJets_CS","lnN",{'Wjets_quark':1.2,'Wjets_gluon':1.2})
            card.addSystematic("CMS_WJets_QG_"+purity,"lnN",{'Wjets_quark':1.2,'Wjets_gluon':0.8})
            card.addSystematic("CMS_top_CS","lnN",{'topRes':1.2,'topNonRes':1.2})
            card.addSystematic("CMS_top_pt","lnN",{'topRes':1.2,'topNonRes':0.8})

            #Tagging efficiency correlated between signal and top in each purity
            if purity=='HP':
                card.addSystematic("CMS_tau21","lnN",{'XWW':0.8, 'topRes':0.8 })
            else:    
                card.addSystematic("CMS_tau21","lnN",{'XWW':1.2,'topRes':1.2})


            #Scale factor for the btagging
            if category=='nob':
                card.addSystematic("CMS_btag_eff","lnN",{'topRes':0.9,'topNonRes':0.9})
                card.addSystematic("CMS_btag_fakeRate","lnN",{'Wjets_quark':0.99,'Wjets_gluon':0.99,'XWW':0.99})
            else:    
                card.addSystematic("CMS_btag_eff","lnN",{'topRes':1.2,'topNonRes':1.2})
                card.addSystematic("CMS_btag_fakeRate","lnN",{'Wjets_quark':1.3,'Wjets_gluon':1.3,'XWW':1.3})

            #jet scale and resolution
               
            #pruned mass scale    
            card.addSystematic("CMS_scale_j","param",[0.0,0.02])
            card.addSystematic("CMS_res_j","param",[0.0,0.05])
            card.addSystematic("CMS_scale_prunedj_0","param",[0.0,0.1])
            card.addSystematic("CMS_res_prunedj_0","param",[0.0,0.2])
            card.addSystematic("CMS_scale_prunedj_1","param",[0.0,4e-6])
            card.addSystematic("CMS_res_prunedj_1","param",[0.0,1e-5])
            card.addSystematic("CMS_scale_MET","param",[0.0,0.02])
            card.addSystematic("CMS_res_MET","param",[0.0,0.01])

            card.addSystematic("topResSlope_"+lepton+"_"+purity,"param",[0.0,0.1])
            card.addSystematic("topResMean_"+lepton+"_"+purity,"param",[0.0,0.05])
            card.addSystematic("topResSigma_"+lepton+"_"+purity,"param",[0.0,0.1])
            card.addSystematic("topNonResSlope_"+lepton+"_"+purity,"param",[0.0,0.1])
            card.addSystematic("topNonResMean0_"+lepton+"_"+purity,"param",[0.0,0.05])
            card.addSystematic("topNonResMean1_"+lepton+"_"+purity,"param",[0.0,5e-4])
            card.addSystematic("topNonResSigma_"+lepton+"_"+purity,"param",[0.0,0.1])
            card.addSystematic("wSlope_"+lepton+"_"+purity,"param",[0.0,0.1])
            card.addSystematic("wMean0_"+lepton+"_"+purity,"param",[0.0,0.05])
            card.addSystematic("wMean1_"+lepton+"_"+purity,"param",[0.0,5e-4])
            card.addSystematic("wSigma_"+lepton+"_"+purity,"param",[0.0,0.1])

            card.addSystematic("wMJJSlopeQ_"+lepton+"_"+purity,"param",[0.0,0.1])
            card.addSystematic("wMJJMeanQ_"+lepton+"_"+purity,"param",[0.0,0.1])
            card.addSystematic("wMJJSigmaQ_"+lepton+"_"+purity,"param",[0.0,0.1])
            card.addSystematic("wMJJSlopeG_"+lepton+"_"+purity,"param",[0.0,0.1])
            card.addSystematic("wMJJMeanG_"+lepton+"_"+purity,"param",[0.0,0.1])
            card.addSystematic("wMJJSigmaG_"+lepton+"_"+purity,"param",[0.0,0.1])

            if purity=='HP':
                card.addSystematic("topMJJSlope_"+lepton+"_"+purity,"param",[0.0,0.1])
                card.addSystematic("topMJJMean_"+lepton+"_"+purity,"param",[0.0,0.1])
                card.addSystematic("topMJJSigma_"+lepton+"_"+purity,"param",[0.0,0.1])
            else:
                card.addSystematic("topMJJSlope_"+lepton+"_"+purity,"param",[0.0,0.1])

            card.makeCard()

#make combined cards



print cmd
            
