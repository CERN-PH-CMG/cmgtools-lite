blinded = False

# LT bins
binsLT = {}
binsLT['LTi'] = ('250 < LT','$\geq$ 250')
binsLT['LT1'] = ('250 < LT && LT < 350','[250, 350]')
binsLT['LT2'] = ('350 < LT && LT < 450','[350, 450]')
binsLT['LT3'] = ('450 < LT && LT < 600','[450, 600]')
binsLT['LT2i'] = ('350 < LT','$\geq$ 350')
binsLT['LT3i'] = ('450 < LT','$\geq$ 450')
binsLT['LT4i'] = ('600 < LT','$\geq$ 600')

binsLT['DLLT1'] = ('250 < DL_ST[2] && DL_ST[2] < 350','[250, 350]')
binsLT['DLLT2'] = ('350 < DL_ST[2] && DL_ST[2] < 450','[350, 450]')
binsLT['DLLT3'] = ('450 < DL_ST[2] && DL_ST[2] < 600','[450, 600]')
binsLT['DLLT3i'] = ('450 < DL_ST[2]','$\geq$ 450')
binsLT['DLLT4i'] = ('600 < DL_ST[2]','$\geq$ 600')

DLLTDict = {}
DLLTDict['LT1']  = 'DLLT1'
DLLTDict['LT2']  = 'DLLT2'
DLLTDict['LT3']  = 'DLLT3'
DLLTDict['LT3i'] = 'DLLT3i'
DLLTDict['LT4i'] = 'DLLT4i'


# HT bins
binsHT = {}
binsHT['HT0i'] = ('500 < HT','$\geq$ 500')
binsHT['HT0'] = ('500 < HT && HT < 750','[500, 750]')
binsHT['HT1'] = ('750 < HT && HT < 1250','[750, 1250]')
binsHT['HT1i'] = ('750 < HT','$\geq$ 750')
binsHT['HT2i'] = ('1250 < HT','$\geq$ 1250')
binsHT['HT01'] = ('500 < HT && HT < 1250','[500, 1250]')

##binsHT for dilepton study (HT recalculated ([2] option for now))
binsHT['DLHT0i'] = ('500 < DL_HT[2]','$\geq$ 500')
binsHT['DLHT0'] = ('500 < DL_HT[2] && DL_HT[2] < 750','[500, 750]')
binsHT['DLHT1'] = ('750 < DL_HT[2] && DL_HT[2] < 1250','[750, 1250]')
binsHT['DLHT1i'] = ('750 < DL_HT[2]','$\geq$ 750')
binsHT['DLHT2i'] = ('1250 < DL_HT[2]','$\geq$ 1250')
binsHT['DLHT01'] = ('500 < DL_HT[2] && DL_HT[2] < 1250','[500, 1250]')

DLHTDict = {}
DLHTDict['HT0i'] = 'DLHT0i'
DLHTDict['HT0']  = 'DLHT0'
DLHTDict['HT1']  = 'DLHT1'
DLHTDict['HT1i'] = 'DLHT1i'
DLHTDict['HT2i'] = 'DLHT2i'
DLHTDict['HT01'] = 'DLHT01'




# NB bins
binsNB = {}
binsNB['NB0'] = ('nBJet == 0','$=$ 0')
binsNB['NB1'] = ('nBJet == 1','$=$ 1')
binsNB['NB2'] = ('nBJet == 2','$=$ 2')
binsNB['NB12'] = ('nBJet == 2','[1,2]')
binsNB['NB0i'] = ('nBJet >= 0','$\geq$ 0')
binsNB['NB1i'] = ('nBJet >= 1','$\geq$ 1')
binsNB['NB2i'] = ('nBJet >= 2','$\geq$ 2')
binsNB['NB3i'] = ('nBJet >= 3','$\geq$ 3')

##binsNb for dilepton study (all nb>=1,2,3 collapsed to nB>=1), ignoring NB0 for now
DLnBDict = {}
DLnBDict['NB1']   = 'NB1i' 
DLnBDict['NB2']   = 'NB1i' 
DLnBDict['NB1i']   = 'NB1i' 
DLnBDict['NB2i']   = 'NB1i' 
DLnBDict['NB3i']   = 'NB1i' 

###binsNb for dilepton study don't change anything for now...
#DLnBDict = {}
#DLnBDict['NB0']   = 'NB0' 
#DLnBDict['NB1']   = 'NB1' 
#DLnBDict['NB2']   = 'NB2' 
#DLnBDict['NB0i']   = 'NB0i' 
#DLnBDict['NB1i']   = 'NB1i' 
#DLnBDict['NB2i']   = 'NB2i' 
#DLnBDict['NB3i']   = 'NB3i' 


# NJ Bins
binsNJ = {}
binsNJ['NJ34'] = ('3 <= nJets30Clean && nJets30Clean <= 4','[3, 4]')
binsNJ['NJ4i'] = ('4 <= nJets30Clean','$\geq$ 4')
binsNJ['NJ45'] = ('4 <= nJets30Clean && nJets30Clean <= 5','[4, 5]')
binsNJ['NJ45f9'] = ('4 <= nJets30Clean && nJets30Clean <= 5','[4, 5]')
binsNJ['NJ45f6'] = ('4 <= nJets30Clean && nJets30Clean <= 5','[4, 5]')
binsNJ['NJ68'] = ('6 <= nJets30Clean && nJets30Clean <= 8','[6, 8]')
binsNJ['NJ9i'] = ('9 <= nJets30Clean','$\geq$ 9')
binsNJ['NJ5'] = ('nJets30Clean == 5','[5]')
binsNJ['NJ4f5'] = ('nJets30Clean == 4','[4]')

##binsNJ for dilepton study (now taken from the friend trees for variant [2])
binsNJ['DLNJ34'] = ('3 <= DL_nJets30Clean[2] && DL_nJets30Clean[2] <= 4','[3, 4]')
binsNJ['DLNJ4i'] = ('4 <= DL_nJets30Clean[2]','$\geq$ 4')
binsNJ['DLNJ45'] = ('4 <= DL_nJets30Clean[2] && DL_nJets30Clean[2] <= 5','[4, 5]')
binsNJ['DLNJ45f9'] = ('4 <= DL_nJets30Clean[2] && DL_nJets30Clean[2] <= 5','[4, 5]')
binsNJ['DLNJ45f6'] = ('4 <= DL_nJets30Clean[2] && DL_nJets30Clean[2] <= 5','[4, 5]')
binsNJ['DLNJ68'] = ('6 <= DL_nJets30Clean[2] && DL_nJets30Clean[2] <= 8','[6, 8]')
binsNJ['DLNJ9i'] = ('9 <= DL_nJets30Clean[2]','$\geq$ 9')
binsNJ['DLNJ5'] = ('DL_nJets30Clean[2] == 5','[5]')
binsNJ['DLNJ4f5'] = ('DL_nJets30Clean[2] == 4','[4]')

DLnJDict = {}
DLnJDict['NJ34']   = 'DLNJ34'  
DLnJDict['NJ4i']   = 'DLNJ4i' 
DLnJDict['NJ45f9'] = 'DLNJ45f9'
DLnJDict['NJ45f6'] = 'DLNJ45f6'
DLnJDict['NJ68']   = 'DLNJ68' 
DLnJDict['NJ9i']   = 'DLNJ9i' 





## Signal/Control region (wrt dPhi)
binsSR = {}
# blind data
#binsSR['SR'] = ('isSR == 1','$\delta \phi > $ x')
#unblind now
binsSR['SR'] = ('abs(isSR) == 1','$\delta \phi > $ x')
binsCR = {}
binsCR['CR'] = ('isSR == 0','$\delta \phi < $ x')
binsCR['DLCR'] = ('nLep == 2','nLep=2')

### variable DeltaPhi cuts
'''
dPhiCuts = {}# "SR":{}, "CR":{}}

dPhiCuts['NJ6']['LT1']['SR'] = ('dPhi > 1','$\delta \phi > $ x')
dPhiCuts['NJ6']['LT1']['CR'] = ('dPhi < 1','$\delta \phi < $ x')
'''

def getSRcut(nj_bin, lt_bin, sr_bin, blinded):

    dPhiCut = "dPhi "
    cutLbl = "$\delta \phi "

    if "SR" in sr_bin:
        dPhiCut += " > "
        cutLbl += " > $ "
    elif "CR" in sr_bin:
        dPhiCut += " < "
        cutLbl += " < $ "

    '''
    if "Few" in nj_bin: cuts = { "LT1": 1.0, "LT2": 0.75, "LT3i": 0.75 }
    elif "9" in nj_bin: cuts = { "LT1": 1.0, "LT2": 0.75, "LT3i": 0.75 }
    elif "6" in nj_bin: cuts = { "LT1": 1.0, "LT2": 0.75, "LT3": 0.75, "LT4i": 0.5 }
    elif "5" in nj_bin: cuts = { "LT1": 1.0, "LT2": 0.75, "LT3i": 0.75 }
    else:
        print "Unknown SR!", nj_bin, lt_bin
        return 0
    '''
    ## DPhi Cuts for LT bins
    cuts = { "LT1": 1.0, "LT2": 0.75, "LT3": 0.75, "LT4": 0.5 }

    for bin in cuts:
        if bin in lt_bin:
            cut = cuts[bin]; break
    else:
        print "No cut found for", nj_bin, lt_bin
        cut = 0

    if blinded and ('68' in nj_bin or '9i' in nj_bin) and "SR" in sr_bin:
        cut = 99.0

    dPhiCut += str(cut)
    cutLbl += str(cut)

    #print nj_bin, lt_bin, sr_bin, dPhiCut, cutLbl

    return (dPhiCut,cutLbl)

################
# MAKE CUT LISTS
################

### QCD
cutQCD = {}

for nj_bin in ['NJ34']:#,'NJ45']:
    nj_cut = binsNJ[nj_bin][0]
    ltbins = ['LT1','LT2','LT3','LT4i']

    for lt_bin in ltbins:
        lt_cut = binsLT[lt_bin][0]

        for ht_bin in ['HT0i']:
            ht_cut = binsHT[ht_bin][0]

            for nb_bin in ['NB0']:
                nb_cut = binsNB[nb_bin][0]

                binname = "%s_%s_%s_%s" %(lt_bin,ht_bin,nb_bin,nj_bin)
                cutQCD[binname] = [("base",lt_bin,lt_cut),("base",ht_bin,ht_cut),("base",nb_bin,nb_cut),("base",nj_bin,nj_cut)]

cutQCDsyst = {}

for lt_bin in ['LTi']:
    lt_cut = binsLT[lt_bin][0]

    for nj_bin in ['NJ34','NJ45','NJ68','NJ9i']:
        nj_cut = binsNJ[nj_bin][0]

        htbins = []

        if nj_bin in ['NJ34']:
            htbins += ['HT0i']
        elif nj_bin in ['NJ45','NJ68']:
            htbins += ['HT0','HT1','HT2i']
        elif nj_bin in ['NJ9i']:
            htbins += ['HT01','HT2i']

        for ht_bin in htbins:
            ht_cut = binsHT[ht_bin][0]

            for nb_bin in ['NB0i','NB0','NB1','NB2i']:
                nb_cut = binsNB[nb_bin][0]

                binname = "%s_%s_%s_%s" %(lt_bin,ht_bin,nb_bin,nj_bin)
                cutQCDsyst[binname] = [("base",lt_bin,lt_cut),("base",ht_bin,ht_cut),("base",nb_bin,nb_cut),("base",nj_bin,nj_cut)]


### Inclusive NB,NJ,HT
cutIncl = {}

for nj_bin in ['NJ4i']:#,'NJ45']:
    nj_cut = binsNJ[nj_bin][0]
    ltbins = ['LTi','LT1','LT2','LT3','LT4i']

    for lt_bin in ltbins:
        lt_cut = binsLT[lt_bin][0]

        for ht_bin in ['HT0i']:
            ht_cut = binsHT[ht_bin][0]

            for nb_bin in ['NB0i']:
                nb_cut = binsNB[nb_bin][0]

                binname = "%s_%s_%s_%s" %(lt_bin,ht_bin,nb_bin,nj_bin)
                cutIncl[binname] = [("base",lt_bin,lt_cut),("base",ht_bin,ht_cut),("base",nb_bin,nb_cut),("base",nj_bin,nj_cut)]

### Bins for Rcs plots vs HT/LT

cutLTbinsSR = {}
cutLTbinsCR = {}

for nj_bin in ['NJ45f6','NJ68']:
    nj_cut = binsNJ[nj_bin][0]

    ltbins = ['LT1','LT2','LT3','LT4i']

    for lt_bin in ltbins:
        lt_cut = binsLT[lt_bin][0]

        nbbins = ['NB0','NB1i']

        '''
        # Match NB bins
        if lt_bin in ['LT1','LT2','LT3','LT4i']:
        nbbins += ['NB1'] # NB1 present in all NJ,LT bins
        if lt_bin in ['LT4i']:
        nbbins += ['NB2i'] # NB2i present in all NJ,LT bins

        if lt_bin in ['LT1','LT2','LT3']:
        # Signal region binning
        if nj_bin in ['NJ68']:
        nbbins += ['NB2','NB3i']
        # Side band  binning
        if nj_bin in ['NJ45f6']:
        nbbins += ['NB2i']
        '''

        for nb_bin in nbbins:
            nb_cut = binsNB[nb_bin][0]

            # split to SR/CR
            for sr_bin in ['SR']:
                sr_cut = binsSR[sr_bin][0]

                binname = "%s_%s_%s_%s" %(lt_bin,nb_bin,nj_bin,sr_bin)
                cutLTbinsSR[binname] = [("base",lt_bin,lt_cut),("base",nb_bin,nb_cut),("base",nj_bin,nj_cut),("base",sr_bin,sr_cut)]

            for cr_bin in ['CR']:
                cr_cut = binsCR[cr_bin][0]

                binname = "%s_%s_%s_%s" %(lt_bin,nb_bin,nj_bin,cr_bin)
                cutLTbinsCR[binname] = [("base",lt_bin,lt_cut),("base",nb_bin,nb_cut),("base",nj_bin,nj_cut),("base",cr_bin,cr_cut)]



### REAL SEARCH BINS (also for RCS)
cutDict = {}
cutDictf9 = {}

cutDictSR = {}
cutDictCR = {}
cutDictDLCR = {}

cutDictSRf9 = {}
cutDictCRf9 = {}
cutDictDLCRf9 = {}

cutDictNJ45f6 = {}
cutDictNJ45f9 = {}
cutDictNJ68 = {}
cutDictNJ9i = {}

for nj_bin in ['NJ45f6','NJ68']:#binsNJ.iteritems():
    nj_cut = binsNJ[nj_bin][0]

    ltbins = ['LT1','LT2','LT3','LT4i']

    for lt_bin in ltbins:#binsLT.iteritems():
        lt_cut = binsLT[lt_bin][0]

        htbins = []

        if lt_bin in ['LT1']:
            htbins += ['HT0','HT1i']
        if lt_bin in ['LT2']:
            htbins += ['HT0','HT1i']
        if lt_bin in ['LT3','LT4i']:
            htbins += ['HT2i']
        if lt_bin in ['LT3','LT4i']:
            htbins += ['HT01']

        #for ht_bin,ht_cut in binsHT.iteritems():
        for ht_bin in htbins:
            ht_cut = binsHT[ht_bin][0]

            nbbins = []


            if nj_bin in ['NJ45f6'] and ht_bin not in ['HT2i']:
                nbbins += ['NB1','NB2i']
            if nj_bin in ['NJ45f6'] and ht_bin in ['HT2i']:
                nbbins += ['NB1i']
            if nj_bin in ['NJ68']:
                if lt_bin in ['LT1','LT2']:
                    nbbins += ['NB1','NB2','NB3i'] # NB1 present in all NJ,LT bins
                if lt_bin in ['LT3','LT4i']:
                    nbbins += ['NB1','NB2i'] # NB2i present in all NJ,LT bins

            # Match NB bins
            #if lt_bin in ['LT1','LT2','LT3','LT4i']:
            #    nbbins += ['NB0','NB1'] # NB1 present in all NJ,LT bins
            #if lt_bin in ['LT4i']:
            #    nbbins += ['NB2i'] # NB2i present in all NJ,LT bins

            #if lt_bin in ['LT1','LT2','LT3']:
            #    # Signal region binning
            #    if nj_bin in ['NJ68']:
            #        nbbins += ['NB2','NB3i']
            #    # Side band  binning
            #    if nj_bin in ['NJ45f6']:
            #        nbbins += ['NB2i']

            for nb_bin in nbbins:
                nb_cut = binsNB[nb_bin][0]

                binname = "%s_%s_%s_%s" %(lt_bin,ht_bin,nb_bin,nj_bin)
                cutDict[binname] = [("base",lt_bin,lt_cut),("base",ht_bin,ht_cut),("base",nb_bin,nb_cut),("base",nj_bin,nj_cut)]

                # split to SR/CR
                for sr_bin in ['SR']:
                    # use isSR var
                    #sr_cut = binsSR[sr_bin][0]
                    # use varying dPhi
                    sr_cut = getSRcut(nj_bin, lt_bin, sr_bin, blinded)[0]

                    binname = "%s_%s_%s_%s_%s" %(lt_bin,ht_bin,nb_bin,nj_bin,sr_bin)
                    cutDictSR[binname] = [("base",lt_bin,lt_cut),("base",ht_bin,ht_cut),("base",nb_bin,nb_cut),("base",nj_bin,nj_cut),("base",sr_bin,sr_cut)]

                for cr_bin in ['CR']:
                    # use isSR var
                    #cr_cut = binsCR[cr_bin][0]
                    # use varying dPhi
                    cr_cut = getSRcut(nj_bin, lt_bin, cr_bin, blinded)[0]
                    DLcr_bin = 'DL'+cr_bin
                    DLcr_cut = binsCR[DLcr_bin][0]

                    binname = "%s_%s_%s_%s_%s" %(lt_bin,ht_bin,nb_bin,nj_bin,cr_bin)
                    cutDictCR[binname] = [("base",lt_bin,lt_cut),("base",ht_bin,ht_cut),("base",nb_bin,nb_cut),("base",nj_bin,nj_cut),("base",cr_bin,cr_cut)]

                    DLbinname = "%s_%s_%s_%s_%s" %(lt_bin,ht_bin,nb_bin,nj_bin,DLcr_bin)
                    DLlt_cut = binsLT[DLLTDict[lt_bin]][0]
                    DLht_cut = binsHT[DLHTDict[ht_bin]][0]
                    DLnb_cut = binsNB[DLnBDict[nb_bin]][0]
                    DLnj_cut = binsNJ[DLnJDict[nj_bin]][0]
                    cutDictDLCR[DLbinname] = [("base",lt_bin,DLlt_cut),("base",ht_bin,DLht_cut),("base",nb_bin,DLnb_cut),("base",nj_bin,DLnj_cut),("base",DLcr_bin,DLcr_cut)]



### FIXME
for nj_bin in ['NJ45f9','NJ9i']:#binsNJ.iteritems():
    nj_cut = binsNJ[nj_bin][0]

    ltbins = ['LT1','LT2','LT3i']

    for lt_bin in ltbins:#binsLT.iteritems():
        lt_cut = binsLT[lt_bin][0]

        htbins = []


        ### FIXME
        if lt_bin in ['LT1']:
            htbins += ['HT0i','HT01','HT2i']
        if lt_bin in ['LT2','LT3i']:
            htbins += ['HT0i']
            #htbins += ['HT0','HT1','HT2i']

        #for ht_bin,ht_cut in binsHT.iteritems():
        for ht_bin in htbins:
            ht_cut = binsHT[ht_bin][0]

            nbbins = []

            # Match NB bins
            if nj_bin in ['NJ9i']:
                if lt_bin in ['LT1'] and not ht_bin in['HT0i']:
                    nbbins += ['NB1','NB2']


                if lt_bin in ['LT1'] and ht_bin in ['HT0i']:
                    nbbins += ['NB3i']

                if lt_bin in ['LT2']:
                    nbbins += ['NB1','NB2','NB3i']
                if lt_bin in ['LT3i']:
                    nbbins += ['NB1','NB2i']


            if nj_bin in ['NJ45f9']:
                if ht_bin in ['HT2i']:
                    nbbins += ['NB1i']
                else:
                    nbbins += ['NB1','NB2i']



            for nb_bin in nbbins:
                nb_cut = binsNB[nb_bin][0]

                binname = "%s_%s_%s_%s" %(lt_bin,ht_bin,nb_bin,nj_bin)

                cutDictf9[binname] = [("base",lt_bin,lt_cut),("base",ht_bin,ht_cut),("base",nb_bin,nb_cut),("base",nj_bin,nj_cut)]

# split to SR/CR

                for sr_bin in ['SR']:
                    # use isSR var
                    #sr_cut = binsSR[sr_bin][0]
                    # use varying dPhi
                    sr_cut = getSRcut(nj_bin, lt_bin, sr_bin, blinded)[0]

                    binname = "%s_%s_%s_%s_%s" %(lt_bin,ht_bin,nb_bin,nj_bin,sr_bin)
                    cutDictSRf9[binname] = [("base",lt_bin,lt_cut),("base",ht_bin,ht_cut),("base",nb_bin,nb_cut),("base",nj_bin,nj_cut),("base",sr_bin,sr_cut)]

                for cr_bin in ['CR']:
                    # use isSR var
                    #cr_cut = binsCR[cr_bin][0]
                    # use varying dPhi
                    cr_cut = getSRcut(nj_bin, lt_bin, cr_bin, blinded)[0]
                    DLcr_bin = 'DL'+cr_bin
                    DLcr_cut = binsCR[DLcr_bin][0]

                    binname = "%s_%s_%s_%s_%s" %(lt_bin,ht_bin,nb_bin,nj_bin,cr_bin)
                    cutDictCRf9[binname] = [("base",lt_bin,lt_cut),("base",ht_bin,ht_cut),("base",nb_bin,nb_cut),("base",nj_bin,nj_cut),("base",cr_bin,cr_cut)]

                    DLbinname = "%s_%s_%s_%s_%s" %(lt_bin,ht_bin,nb_bin,nj_bin,DLcr_bin)
                    DLlt_cut = binsLT[DLLTDict[lt_bin]][0]
                    DLht_cut = binsHT[DLHTDict[ht_bin]][0]
                    DLnb_cut = binsNB[DLnBDict[nb_bin]][0]
                    DLnj_cut = binsNJ[DLnJDict[nj_bin]][0]
                    cutDictDLCRf9[DLbinname] = [("base",lt_bin,DLlt_cut),("base",ht_bin,DLht_cut),("base",nb_bin,DLnb_cut),("base",nj_bin,DLnj_cut),("base",DLcr_bin,DLcr_cut)]



#####Dictionaries for data cross check from 4 to 5
cutDictf5 = {}
cutDictSRf5 = {}
cutDictCRf5 = {}


for nj_bin in ['NJ4f5','NJ5']:#binsNJ.iteritems():
    nj_cut = binsNJ[nj_bin][0]

    ltbins = ['LT1','LT2','LT3i']

    for lt_bin in ltbins:#binsLT.iteritems():
        lt_cut = binsLT[lt_bin][0]

        htbins = []

        if lt_bin in ['LT1']:
            htbins += ['HT0','HT1i']
        if lt_bin in ['LT2', 'LT3i']:
            htbins += ['HT0','HT1i']


        #for ht_bin,ht_cut in binsHT.iteritems():
        for ht_bin in htbins:
            ht_cut = binsHT[ht_bin][0]

            nbbins = []


            if nj_bin in ['NJ4f5'] and ht_bin not in ['HT1i']:
                nbbins += ['NB1','NB2i']
            if nj_bin in ['NJ4f5'] and ht_bin in ['HT1i']:
                nbbins += ['NB1i']
            if nj_bin in ['NJ5']:
                if lt_bin in ['LT1','LT2']:
                    nbbins += ['NB1','NB2','NB3i'] # NB1 present in all NJ,LT bins
                if lt_bin in ['LT3i']:
                    nbbins += ['NB1','NB2i'] # NB2i present in all NJ,LT bins


            for nb_bin in nbbins:
                nb_cut = binsNB[nb_bin][0]
                binname = "%s_%s_%s_%s" %(lt_bin,ht_bin,nb_bin,nj_bin)
                cutDictf5[binname] = [("base",lt_bin,lt_cut),("base",ht_bin,ht_cut),("base",nb_bin,nb_cut),("base",nj_bin,nj_cut)]

                # split to SR/CR
                for sr_bin in ['SR']:
                    # use isSR var
                    #sr_cut = binsSR[sr_bin][0]
                    # use varying dPhi
                    sr_cut = getSRcut(nj_bin, lt_bin, sr_bin, blinded)[0]

                    binname = "%s_%s_%s_%s_%s" %(lt_bin,ht_bin,nb_bin,nj_bin,sr_bin)
                    cutDictSRf5[binname] = [("base",lt_bin,lt_cut),("base",ht_bin,ht_cut),("base",nb_bin,nb_cut),("base",nj_bin,nj_cut),("base",sr_bin,sr_cut)]

                for cr_bin in ['CR']:
                    # use isSR var
                    #cr_cut = binsCR[cr_bin][0]
                    # use varying dPhi
                    cr_cut = getSRcut(nj_bin, lt_bin, cr_bin, blinded)[0]

                    binname = "%s_%s_%s_%s_%s" %(lt_bin,ht_bin,nb_bin,nj_bin,cr_bin)
                    cutDictCRf5[binname] = [("base",lt_bin,lt_cut),("base",ht_bin,ht_cut),("base",nb_bin,nb_cut),("base",nj_bin,nj_cut),("base",cr_bin,cr_cut)]




#####Few bins for illustration
cutDictf68Few = {}
cutDictSRf68Few = {}
cutDictCRf68Few = {}

cutDictf9Few = {}
cutDictSRf9Few = {}
cutDictCRf9Few = {}

for nj_bin in ['NJ45f6','NJ68']:#binsNJ.iteritems():
    nj_cut = binsNJ[nj_bin][0]

    ltbins = ['LT1','LT2','LT3','LT4i']

    for lt_bin in ltbins:#binsLT.iteritems():
        lt_cut = binsLT[lt_bin][0]

        htbins = ['HT0i']
        #for ht_bin,ht_cut in binsHT.iteritems():
        for ht_bin in htbins:
            ht_cut = binsHT[ht_bin][0]

            nbbins = []
            if lt_bin in ['LT4i']:
                nbbins = ['NB1i']
            elif lt_bin in ['LT1']:
                if nj_bin in ['NJ45f6']:
                    nbbins = ['NB2i']
                else:
                    nbbins = ['NB3i']
            else:
                nbbins = ['NB2i']

            for nb_bin in nbbins:
                nb_cut = binsNB[nb_bin][0]
                binname = "%s_%s_%s_%s_Few" %(lt_bin,ht_bin,nb_bin,nj_bin)
                cutDictf68Few[binname] = [("base",lt_bin,lt_cut),("base",ht_bin,ht_cut),("base",nb_bin,nb_cut),("base",nj_bin,nj_cut)]
                #print binname
                # split to SR/CR
                for sr_bin in ['SR']:
                    # use isSR var
                    #sr_cut = binsSR[sr_bin][0]
                    # use varying dPhi
                    sr_cut = getSRcut(nj_bin, lt_bin, sr_bin, blinded)[0]

                    binname = "%s_%s_%s_%s_%s_Few" %(lt_bin,ht_bin,nb_bin,nj_bin,sr_bin)
                    cutDictSRf68Few[binname] = [("base",lt_bin,lt_cut),("base",ht_bin,ht_cut),("base",nb_bin,nb_cut),("base",nj_bin,nj_cut),("base",sr_bin,sr_cut)]

                for cr_bin in ['CR']:
                    # use isSR var
                    #cr_cut = binsCR[cr_bin][0]
                    # use varying dPhi
                    cr_cut = getSRcut(nj_bin, lt_bin, cr_bin, blinded)[0]

                    binname = "%s_%s_%s_%s_%s_Few" %(lt_bin,ht_bin,nb_bin,nj_bin,cr_bin)
                    cutDictCRf68Few[binname] = [("base",lt_bin,lt_cut),("base",ht_bin,ht_cut),("base",nb_bin,nb_cut),("base",nj_bin,nj_cut),("base",cr_bin,cr_cut)]


for nj_bin in ['NJ45f9','NJ9i']:#binsNJ.iteritems():
    nj_cut = binsNJ[nj_bin][0]

    ltbins = ['LT1','LT2i']

    for lt_bin in ltbins:#binsLT.iteritems():
        lt_cut = binsLT[lt_bin][0]

        htbins = ['HT0i']
        #for ht_bin,ht_cut in binsHT.iteritems():
        for ht_bin in htbins:
            ht_cut = binsHT[ht_bin][0]

            nbbins = []
            nbbins = ['NB1i']

            for nb_bin in nbbins:
                nb_cut = binsNB[nb_bin][0]
                binname = "%s_%s_%s_%s_Few" %(lt_bin,ht_bin,nb_bin,nj_bin)
                cutDictf9Few[binname] = [("base",lt_bin,lt_cut),("base",ht_bin,ht_cut),("base",nb_bin,nb_cut),("base",nj_bin,nj_cut)]

                # split to SR/CR
                for sr_bin in ['SR']:
                    # use isSR var
                    #sr_cut = binsSR[sr_bin][0]
                    # use varying dPhi
                    sr_cut = getSRcut(nj_bin, lt_bin, sr_bin, blinded)[0]

                    binname = "%s_%s_%s_%s_%s_Few" %(lt_bin,ht_bin,nb_bin,nj_bin,sr_bin)
                    cutDictSRf9Few[binname] = [("base",lt_bin,lt_cut),("base",ht_bin,ht_cut),("base",nb_bin,nb_cut),("base",nj_bin,nj_cut),("base",sr_bin,sr_cut)]

                for cr_bin in ['CR']:
                    # use isSR var
                    #cr_cut = binsCR[cr_bin][0]
                    # use varying dPhi
                    cr_cut = getSRcut(nj_bin, lt_bin, cr_bin, blinded)[0]

                    binname = "%s_%s_%s_%s_%s_Few" %(lt_bin,ht_bin,nb_bin,nj_bin,cr_bin)
                    cutDictCRf9Few[binname] = [("base",lt_bin,lt_cut),("base",ht_bin,ht_cut),("base",nb_bin,nb_cut),("base",nj_bin,nj_cut),("base",cr_bin,cr_cut)]
