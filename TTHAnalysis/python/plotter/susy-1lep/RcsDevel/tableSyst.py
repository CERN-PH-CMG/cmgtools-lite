import sys,os

#from makeYieldPlots import *
from makeYieldTables import *
#from yieldClass import *

if __name__ == "__main__":

    ## remove '-b' option

    pattern = "Syst"

    #BinMask LTX_HTX_NBX_NJX for canvas names
    basename = os.path.basename(pattern)
    mask = basename.replace("*","X_")

    # Define storage
    yds = YieldStore("Sele")
    yds9 = YieldStore("Sele")
    paths = []

    # Add files
    #old ntuples
#    btagPath = "Yields/systs/btag/test/merged/"; paths.append(btagPath)
#    puPath = "Yields/systs/PU/test/merged/"; paths.append(puPath)
#    wxsecPath = "Yields/systs/wXsec/test/merged/"; paths.append(wxsecPath)
#    tptPath = "Yields/systs/topPt/test/merged"; paths.append(tptPath)
#    dlConstPath = "Yields/systs/dilepConst/test/merged"; paths.append(dlConstPath)
#    dlSlopePath = "Yields/systs/dilepSlope/test/merged"; paths.append(dlSlopePath)


    tptPath = "YieldsJan15/systs/topPt/MC/allSF_noPU/meth1A/merged/"; paths.append(tptPath)
    puPath = "YieldsJan15/systs/PU/MC/allSF/meth1A/merged/"; paths.append(puPath)
    wxsecPath = "YieldsJan15/systs/wXsec/MC/allSF_noPU/meth1A/merged/"; paths.append(wxsecPath)
    dlConstPath = "YieldsJan15/systs/DLConst/merged"; paths.append(dlConstPath)
    dlSlopePath = "YieldsJan15/systs/DLSlope/merged"; paths.append(dlSlopePath)
    #jerPath = "Yields/systs/JER/merged"; paths.append(jerPath)                                                               #jerNoPath = "YieldsJan15/systs/JER_YesNo/merged"; paths.append(jerNoPath)
    btagPath = "YieldsJan15/systs/btag/hadFlavour/fixXsec/allSF_noPU/meth1A/merged/"; paths.append(btagPath)
    jecPath = "YieldsJan15/systs/JEC/MC/allSF_noPU/meth1A/merged/"; paths.append(jecPath)
    wpolPath = "YieldsJan15/systs/Wpol/MC/allSF_noPU/meth1A/merged/"; paths.append(wpolPath)
    ttvxsecPath = "YieldsJan15/systs/TTVxsec/MC/allSF_noPU/meth1A/merged/"; paths.append(ttvxsecPath)

    #jecPath = "Yields/systs/JEC/EWK/full/merged/"; paths.append(jecPath)

    for path in paths:
        yds.addFromFiles(path+'/*NJ68*',("lep","sele"))
        yds9.addFromFiles(path+'/*NJ9i*',("lep","sele"))

    systs = ["btagHF","btagLF","Wxsec","Wpol","TTVxsec","topPt","PU","JEC","DLSlope","DLConst"]#,"JEC"]
    systsprint = ["b-tag HF","b-tag LF","W xsec","W polar","TTV xsec","Top pT","PU","JES","dilep slope","dilep const"]#,"JEC"]

    # Sample and variable
    samp = "EWK"
    var = "Kappa"

    # canvs and hists
    hists = []
    canvs = []

    yds.showStats()

    f =  open('sysTable.tex','w')
    caption = 'Multi-b analysis: Systematic uncertainties on $\kappa$ for different sources'
    samps = [('EWK_'+syst+'_syst','Kappa')  for syst in systs]
    printSamps = [syst  for syst in systsprint]
    samps = [('EWK_'+syst+'_syst','Kappa')  for syst in systs]
    printLatexHeader(len(samps), f, caption)    
    label = '6,8 jet bins, relative uncertainties given in \%'

    yds.printLatexTable(samps, printSamps, label,f, True) 
    label = '9 jet bins, relative uncertainties given in \%'
    yds9.printLatexTable(samps, printSamps, label,f,True) 
    printLatexFooter(f, 0)
    f.close()
    
    f =  open('sysTable.dat','w')
    yds.printTable(samps, systs, label,f) 
    yds9.printTable(samps, systs, label,f) 
    f.close()
