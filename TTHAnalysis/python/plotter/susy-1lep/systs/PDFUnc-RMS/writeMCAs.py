#!/usr/bin/env python
#import re, sys, os, os.path

import glob, os, sys, math


### ./makeBinYields.py --mca ../systs/PDFUnc-RMS/mca-MC_syst_PDFUnc-RMS_1a_allSF.txt -P ../systs/PDFUnc-RMS/links -F sf/t ../systs/PDFUnc-RMS/links/Friends/DileptonPreapproval/evVarFriend_{cname}.root -l 2.2 --grid -v 2 --od lumi22fb_DlMakeBinYields/PDFUnc-RMS --syst -b
#Following recipe from
#https://indico.cern.ch/event/459797/contribution/2/attachments/1181555/1710844/mcaod-Nov4-2015.pdf
#i.e.:
#MC Replicas: Make a distribution of the observable under the (eg 100) MC replicas and either take the RMS as the uncertainty or propagate the full distribution for non-gaussian cases


#PDFUnc-RMS

firstPart = """
### ./makeBinYields.py --mca ../systs/PDFUnc-RMS/mca-MC_syst_PDFUnc-RMS_1a_allSF.txt -P ../systs/PDFUnc-RMS/links -F sf/t ../systs/PDFUnc-RMS/links/Friends/DileptonPreapproval/evVarFriend_{cname}.root -l 2.2 --grid -v 2 --od lumi22fb_DlMakeBinYields/PDFUnc-RMS --syst -b
#Following recipe from
#https://indico.cern.ch/event/459797/contribution/2/attachments/1181555/1710844/mcaod-Nov4-2015.pdf
#i.e.:
#MC Replicas: Make a distribution of the observable under the (eg 100) MC replicas and either take the RMS as the uncertainty or propagate the full distribution for non-gaussian cases
### CENTRAL
# TTJets
TTJets  : TTJets_LO             : xsec*lepSF*TopPtWeight*0.94*btagSF : ngenTau+ngenLep == 0 && lheHTIncoming <= 600 && HT < 1250;
TTJets  : TTJets_DiLepton               : xsec*lepSF*TopPtWeight*0.94*btagSF : lheHTIncoming <= 600;
TTJets  : TTJets_SingleLepton           : 2*xsec*lepSF*TopPtWeight*0.94*btagSF : lheHTIncoming <= 600;
TTJets  : TTJets_LO_HT600to800          : xsec*lepSF*TopPtWeight*0.94*btagSF ;
TTJets  : TTJets_LO_HT800to1200         : xsec*lepSF*TopPtWeight*0.94*btagSF ;
TTJets  : TTJets_LO_HT1200to2500        : xsec*lepSF*TopPtWeight*0.94*btagSF ;
TTJets  : TTJets_LO_HT2500toInf         : xsec*lepSF*TopPtWeight*0.94*btagSF ;
# WJets
WJets   : WJetsToLNu_HT100to200         : xsec*lepSF*TopPtWeight*0.94*btagSF ;
WJets   : WJetsToLNu_HT200to400         : xsec*lepSF*TopPtWeight*0.94*btagSF ;
WJets   : WJetsToLNu_HT400to600         : xsec*lepSF*TopPtWeight*0.94*btagSF ;
WJets   : WJetsToLNu_HT600to800         : xsec*lepSF*TopPtWeight*0.94*btagSF ;
WJets   : WJetsToLNu_HT800to1200        : xsec*lepSF*TopPtWeight*0.94*btagSF ;
WJets   : WJetsToLNu_HT1200to2500       : xsec*lepSF*TopPtWeight*0.94*btagSF ;
WJets   : WJetsToLNu_HT2500toInf        : xsec*lepSF*TopPtWeight*0.94*btagSF ;
# Single Top
SingleTop       : TToLeptons_tch_amcatnlo       : xsec*lepSF*TopPtWeight*0.94*btagSF ;
SingleTop       : TToLeptons_sch                : xsec*lepSF*TopPtWeight*0.94*btagSF ;
SingleTop       : T_tWch                        : xsec*lepSF*TopPtWeight*0.94*btagSF ;
SingleTop       : TBar_tWch                     : xsec*lepSF*TopPtWeight*0.94*btagSF ;
# DY
DY      : DYJetsToLL_M50_HT100to200     : xsec*lepSF*TopPtWeight*0.94*btagSF ;
DY      : DYJetsToLL_M50_HT200to400     : xsec*lepSF*TopPtWeight*0.94*btagSF ;
DY      : DYJetsToLL_M50_HT400to600     : xsec*lepSF*TopPtWeight*0.94*btagSF ;
DY      : DYJetsToLL_M50_HT600toInf     : xsec*lepSF*TopPtWeight*0.94*btagSF ;
# TTV
TTV     : TTWToLNu                      : xsec*lepSF*TopPtWeight*0.94*btagSF ;
TTV     : TTWToQQ                       : xsec*lepSF*TopPtWeight*0.94*btagSF ;
TTV     : TTZToLLNuNu                   : xsec*lepSF*TopPtWeight*0.94*btagSF ;
TTV     : TTZToQQ                       : xsec*lepSF*TopPtWeight*0.94*btagSF ;
"""




def returnWeightSnippe(index):
    temp = """
### Var1
# TTJets
TTJets_PDFUnc-RMS{0} : TTJets_LO   : xsec*lepSF*TopPtWeight*0.94*btagSF*LHEweight_wgt[{0}]/LHEweight_wgt[0] : ngenTau+ngenLep == 0 && lheHTIncoming <= 600 && HT < 1250;
TTJets_PDFUnc-RMS{0} : TTJets_DiLepton   : xsec*lepSF*TopPtWeight*0.94*btagSF*LHEweight_wgt[{0}]/LHEweight_wgt[0] : lheHTIncoming <= 600;
TTJets_PDFUnc-RMS{0}	: TTJets_SingleLepton 		: 2*xsec*lepSF*TopPtWeight*0.94*btagSF*LHEweight_wgt[{0}]/LHEweight_wgt[0] : lheHTIncoming <= 600;
TTJets_PDFUnc-RMS{0}	: TTJets_LO_HT600to800		: xsec*lepSF*TopPtWeight*0.94*btagSF*LHEweight_wgt[{0}]/LHEweight_wgt[0] ;
TTJets_PDFUnc-RMS{0}	: TTJets_LO_HT800to1200 	: xsec*lepSF*TopPtWeight*0.94*btagSF*LHEweight_wgt[{0}]/LHEweight_wgt[0] ;
TTJets_PDFUnc-RMS{0}	: TTJets_LO_HT1200to2500 	: xsec*lepSF*TopPtWeight*0.94*btagSF*LHEweight_wgt[{0}]/LHEweight_wgt[0] ;
TTJets_PDFUnc-RMS{0}	: TTJets_LO_HT2500toInf 	: xsec*lepSF*TopPtWeight*0.94*btagSF*LHEweight_wgt[{0}]/LHEweight_wgt[0] ;
# WJets
WJets_PDFUnc-RMS{0}	: WJetsToLNu_HT100to200		: xsec*lepSF*TopPtWeight*0.94*btagSF*LHEweight_wgt[{0}]/LHEweight_wgt[0] ;
WJets_PDFUnc-RMS{0}	: WJetsToLNu_HT200to400 	: xsec*lepSF*TopPtWeight*0.94*btagSF*LHEweight_wgt[{0}]/LHEweight_wgt[0] ;
WJets_PDFUnc-RMS{0}	: WJetsToLNu_HT400to600 	: xsec*lepSF*TopPtWeight*0.94*btagSF*LHEweight_wgt[{0}]/LHEweight_wgt[0] ;
WJets_PDFUnc-RMS{0}	: WJetsToLNu_HT600to800 	: xsec*lepSF*TopPtWeight*0.94*btagSF*LHEweight_wgt[{0}]/LHEweight_wgt[0] ;
WJets_PDFUnc-RMS{0}	: WJetsToLNu_HT800to1200 	: xsec*lepSF*TopPtWeight*0.94*btagSF*LHEweight_wgt[{0}]/LHEweight_wgt[0] ;
WJets_PDFUnc-RMS{0}	: WJetsToLNu_HT1200to2500 	: xsec*lepSF*TopPtWeight*0.94*btagSF*LHEweight_wgt[{0}]/LHEweight_wgt[0] ;
WJets_PDFUnc-RMS{0}	: WJetsToLNu_HT2500toInf 	: xsec*lepSF*TopPtWeight*0.94*btagSF*LHEweight_wgt[{0}]/LHEweight_wgt[0] ;
# Single Top
SingleTop_PDFUnc-RMS{0}	: TToLeptons_tch_amcatnlo	: xsec*lepSF*TopPtWeight*0.94*btagSF*LHEweight_wgt[{0}]/LHEweight_wgt[0] ;
SingleTop_PDFUnc-RMS{0}	: TToLeptons_sch	 	: xsec*lepSF*TopPtWeight*0.94*btagSF*LHEweight_wgt[{0}]/LHEweight_wgt[0] ;
SingleTop_PDFUnc-RMS{0}	: T_tWch	 		: xsec*lepSF*TopPtWeight*0.94*btagSF*LHEweight_wgt[{0}]/LHEweight_wgt[0] ;
SingleTop_PDFUnc-RMS{0}	: TBar_tWch	 		: xsec*lepSF*TopPtWeight*0.94*btagSF*LHEweight_wgt[{0}]/LHEweight_wgt[0] ;
# DY
DY_PDFUnc-RMS{0}	: DYJetsToLL_M50_HT100to200	: xsec*lepSF*TopPtWeight*0.94*btagSF*LHEweight_wgt[{0}]/LHEweight_wgt[0] ;
DY_PDFUnc-RMS{0}	: DYJetsToLL_M50_HT200to400 	: xsec*lepSF*TopPtWeight*0.94*btagSF*LHEweight_wgt[{0}]/LHEweight_wgt[0] ;
DY_PDFUnc-RMS{0}	: DYJetsToLL_M50_HT400to600 	: xsec*lepSF*TopPtWeight*0.94*btagSF*LHEweight_wgt[{0}]/LHEweight_wgt[0] ;
DY_PDFUnc-RMS{0}	: DYJetsToLL_M50_HT600toInf 	: xsec*lepSF*TopPtWeight*0.94*btagSF*LHEweight_wgt[{0}]/LHEweight_wgt[0] ;
# TTV
TTV_PDFUnc-RMS{0}	: TTWToLNu			: xsec*lepSF*TopPtWeight*0.94*btagSF*LHEweight_wgt[{0}]/LHEweight_wgt[0] ;
TTV_PDFUnc-RMS{0}	: TTWToQQ 			: xsec*lepSF*TopPtWeight*0.94*btagSF*LHEweight_wgt[{0}]/LHEweight_wgt[0] ;
TTV_PDFUnc-RMS{0}	: TTZToLLNuNu 			: xsec*lepSF*TopPtWeight*0.94*btagSF*LHEweight_wgt[{0}]/LHEweight_wgt[0] ;
TTV_PDFUnc-RMS{0}	: TTZToQQ 			: xsec*lepSF*TopPtWeight*0.94*btagSF*LHEweight_wgt[{0}]/LHEweight_wgt[0] ;



""".format(index)
    return temp

f = open('mca-MC_syst_PDFUnc-RMS_1a_allSF.txt', 'w')
f.write(firstPart)
for i in range (9,110):
    f.write(returnWeightSnippe(i))
f.close()


split = 0
f = open('mca-MC_syst_PDFUnc-RMS_1a_allSF_{0}.txt'.format(split), 'w')
f.write(firstPart)
for i in range (9,110):
    if i%10==0:
        f.close()
        split += 1
        f = open('mca-MC_syst_PDFUnc-RMS_1a_allSF_{0}.txt'.format(split), 'w')
        f.write(firstPart)
    f.write(returnWeightSnippe(i))
f.close()


for i in range (0,split+1):
    print "./makeBinYields.py --mca ../systs/PDFUnc-RMS/mca-MC_syst_PDFUnc-RMS_1a_allSF_{split}.txt -P ../systs/PDFUnc-RMS/links -F sf/t ../systs/PDFUnc-RMS/links/Friends/DileptonPreapproval/evVarFriend_{cname}.root -l 2.2 --grid -v 2 --od lumi22fb_DlMakeBinYields/PDFUnc-RMS_{split} --syst -b".format(cname="{cname}",split=i)
