
#!/usr/bin/env python
import sys
import numpy as np
import random as rd
out = ''
SMS = 'T1tttt'

from yieldClass import *
from ROOT import *
def printDataCard(yds, ydsObs, ydsSysSig):
    folder = 'datacards_'+ out +'/'
    if not os.path.exists(folder): os.makedirs(folder) 
    bins = sorted(yds.keys())

    sampNames = [x.name for x in yds[bins[0]]]
    nSamps = len(sampNames)
    for x in sampNames:
        if "Scan_m" in x: signalName = x

    precision = 4
    
    try:                                                                                                                     
        os.stat(folder + signalName )                                                                                
    except:                                                                                                                  
        os.mkdir(folder + signalName )
    iproc = { key: i+1 for (i,key) in enumerate(sorted(reversed(sampNames)))}
    iproc.update({signalName: 0})
    
    for i,bin in enumerate(bins):
        datacard = open(folder + signalName + '/' +bin + '.card.txt', 'w'); 
        datacard.write("## Datacard for binfile %s (signal %s)\n"%(bin,signalName))
        
            #datacard.write("shapes *        * ../common/%s.input.root x_$PROCESS x_$PROCESS_$SYSTEMATIC\n" % binName)
        datacard.write('##----------------------------------\n')
        datacard.write('bin         %s\n' % bin)
        obs = sum(yd.val for yd in ydsObs[bin])
        datacard.write('observation %s\n' % obs)
        datacard.write('##----------------------------------\n')
        klen = len(sampNames)
        kpatt = " %%%ds "  % klen
        fpatt = " %%%d.%df " % (klen,3)
        datacard.write('##----------------------------------\n')
        datacard.write('bin'+ ( ' ' * 32) +(" ".join([kpatt % bin     for p in sampNames]))+"\n")
        datacard.write('process'+ ( ' ' * 30)  +(" ".join([kpatt % p          for p in sampNames]))+"\n")
        datacard.write('process'+ ( ' ' * 30)  +(" ".join([kpatt % iproc[p]    for p in sampNames]))+"\n")
        datacard.write('rate'+ ( ' ' * 35)  +(" ".join([fpatt % yd.val for yd in yds[bin]]))+"\n")
        #            datacard.write('##----------------------------------\n')
#        datacard.write('Lumi lnN' + (' ' * 33) +  " ".join([kpatt % numToBar(1.0+0.05) for yd in yds[bin]]) + '\n')
        '''for i,yd in enumerate(yds[bin]):
            before = '       -  ' * i
            after = '       -  ' * (nSamps - i - 1)
            datacard.write('MCstats' + yd.name + ' lnN  ' + (' ' * (28-len(yd.name)))  + before + " ".join([kpatt % numToBar(1.0+(yd.err/(yd.val+0.01))) ]) +  after +"\n")        
        '''
        for i, yd in enumerate(ydsSigSys[bin]):
            before = '       -  ' * (nSamps - i - 1)
            sys = yd.name[yd.name.find('Scan_') + 5:yd.name.find('_mGo')]
            datacard.write(sys + ' lnN  ' + (' ' * (28))  + before + " ".join([kpatt % numToBar(1 + yd.val) ]) +"\n")
    return 1


def readSystFile():
    systDict = {}
    with open('sysTable_ICHEP.dat',"r") as xfile:
#    with open('sysTable_few.dat',"r") as xfile:
        lines = xfile.readlines()
        systs = lines[0].replace(' ','').replace('\n','').split('|') 
        print systs
        for line in lines[1:]:
            values = line.replace(' ','').replace('\n','').split('|')            
            binMB = values[0]
            binSB = values[1]
            singleSysts = {}
            for val, syst in zip(values[2:],systs[2:]):
                singleSysts[(binSB,syst)] = val
            systDict[binMB] =  singleSysts

    return systDict

def printABCDCard(yds, ydsObs, ydsKappa, ydsSigSys):
    systDict = readSystFile()
    folder = 'datacardsABCD_' + out + '/'
    if not os.path.exists(folder): os.makedirs(folder) 
    bins = sorted(yds.keys())
    
    catNames = [x.cat for x in yds[bins[0]] ]
    sampNames = [x.name.replace('background','data') for x in (yds[bins[0]]) ]
    sampUniqueNames = list(set(sampNames))
    for x in sampNames:
        if "Scan_m" in x: signalName = x
     
    mGlu = signalName[signalName.find('_mGo') + 4:signalName.find('_mLSP')]
    factor = 1.0
    if float(mGlu) < 1400:
        factor = 100.0
    catUniqueNames = [x.cat for x in ydsObs[bins[0]] ]
    nSamps = len(sampNames)

    precision = 4
    
    
    try:                                                                                                              
        os.stat(folder + signalName )                                                                                
    except:                                                                                                                  
        os.mkdir(folder + signalName ) 

    #print sampUniqueNames
    iproc = { key: i+1 for (i,key) in enumerate(sorted(reversed(sampUniqueNames)))}
    iproc.update({signalName: 0})
    #print iproc
    rd.seed(5)
    for i,bin in enumerate(bins):
        obs0 = False
        if 'LT1_HT2i_NB2_NJ9i' in bin:
            obs0 = True
        datacard = open(folder+ signalName+ '/' +bin + '.card.txt', 'w'); 
        datacard.write("## Datacard for bin %s (signal %s)\n"%(bin,signalName))
        datacard.write("imax 4  number of channels \n")
        datacard.write("jmax 1  number of processes -1 \n")
        datacard.write("kmax *  number of nuisance parameters (sources of systematical uncertainties) \n")
        
        klen = len(sampNames)
        kpatt = " %%%ds "  % klen
        fpatt = " %%%d.%df " % (klen,5)
        datacard.write('##----------------------------------\n')
        #observation

        datacard.write('bin'+ ( ' ' * 32) +(" ".join([kpatt % cat.replace('_predict','')     for cat in catUniqueNames]))+"\n")
        np.random.seed(42546)
        ##########ATTENENTION###############
        #####Randomly adding 0.3 to the observation remove for real data#############
        #datacard.write('observation'+ ( ' ' * 32) +(" ".join([kpatt % str(round(yd.val+rd.choice([0.3,0]))) if 'SR_MB' in yd.cat else str(round(yd.val))  for yd in ydsObs[bin]]))+"\n")
        datacard.write('observation'+ ( ' ' * 32) +(" ".join([kpatt % str(0.1) if obs0 and 'CR_MB' in yd.cat else str(round(yd.val))   for yd in ydsObs[bin]]))+"\n")


        datacard.write('##----------------------------------\n')
        datacard.write('##----------------------------------\n')
        datacard.write('bin'+ ( ' ' * 32) +(" ".join(([kpatt % (cat.replace('_predict',''))     for cat in catNames])))+"\n")
        datacard.write('process'+ ( ' ' * 30)  +(" ".join([kpatt % p          for p in sampNames]))+"\n")
        datacard.write('process'+ ( ' ' * 30)  +(" ".join([kpatt % iproc[p]    for p in sampNames]))+"\n")

        datacard.write('rate'+ ( ' ' * 37)  +(" ".join([fpatt % float(yd.val/factor) if type(yd) != int and 'Scan' in yd.name else '   1     '  for yd in yds[bin]]))+"\n")


        before = '       -  ' * (4)
        after = '       -  ' * (3)

        #flag to do proper signal uncertainties from pickle file
        doSigSyst = True

        #hard code for now some values for uncertainties that are flat on the normalization
        #Trigger 1 (2015) | 2 (ICHEP)
        #PU      5 (2015) | per bin (ICHEP)
        #Lep SF  5 (2015) | 5 (ICHEP)
        #Lumi    2.7 (2015) | 6.7 (ICHEP)

        if doSigSyst:
            #ICHEP
            fixedSyst = [('XtrigSyst',1.02), ('XlepSFSyst',1.05), ('XlumiSyst',1.067)]
            #2015 data
            
           #fixedSyst = [('XtrigSyst',1.01), ('XpuSyst', 1.05), ('XlepSFSyst',1.05), ('XlumiSyst',1.027)] 
            
            for sys in fixedSyst:
                datacard.write(sys[0] + ' lnN  ' + (' ' * (28))  + before + 4*" ".join([kpatt % numToBar(sys[1])]) + "\n")
        
            #statistical uncertainty write out all bins
            datacard.write('XXstatSys_SR_MB'+bin+' lnN '+ ( ' ' * 17)  +(" ".join([fpatt % float(1+yd.err/max(yd.val,0.0001)) if type(yd) != int and 'Scan' in yd.name and 'SR_MB' in yd.cat else '   -     '  for yd in yds[bin]]))+"\n")
            datacard.write('XXstatSys_CR_MB'+bin+' lnN '+ ( ' ' * 17)  +(" ".join([fpatt % float(1+yd.err/max(yd.val,0.0001)) if type(yd) != int and 'Scan' in yd.name and 'CR_MB' in yd.cat else '   -     '  for yd in yds[bin]]))+"\n")
            datacard.write('XXstatSys_SR_SB'+bin+' lnN '+ ( ' ' * 17)  +(" ".join([fpatt % float(1+yd.err/max(yd.val,0.0001)) if type(yd) != int and 'Scan' in yd.name and 'SR_SB' in yd.cat else '   -     '  for yd in yds[bin]]))+"\n")
            datacard.write('XXstatSys_CR_SB'+bin+' lnN '+ ( ' ' * 17)  +(" ".join([fpatt % float(1+yd.err/max(yd.val,0.0001)) if type(yd) != int and 'Scan' in yd.name and 'CR_SB' in yd.cat else '   -     '  for yd in yds[bin]]))+"\n")

           
            for yd in ydsSigSys[bin]:
                datacard.write('X'+yd.name[yd.name.find("Scan_")+5:yd.name.find('mGo')-1] + ' lnN  ' + (' ' * (28))  + before + " ".join([kpatt % numToBar(1 + yd.val)]) + after + "\n")

        #If we don't do you signal systematics just assing 20% flat
        else:
            datacard.write('sigSyst lnN  ' + (' ' * (28))  + before + " 1.2 " + after + "\n")

        #for bin LT1_HT2i_NB2_NJ9i write out additonal uncertainty (need to remove this for next iteration)
        if obs0:
            datacard.write('ALT1_HT2i_NB2_NJ9i_100percent lnN '+ ( ' ' * 32) +(" ".join(([kpatt % 1.98 if ('CR_MB','data') == (x.replace('_predict',''),y) else '    -   ' for (x,y) in zip(catNames,sampNames)])))+"\n")
        
        #Background systematics as lnN on region A
        for syst in systDict[bin]:
            datacard.write('A'+syst[1]+' lnN '+ ( ' ' * 32) +(" ".join(([kpatt % systDict[bin][syst] if ('SR_MB','data') == (x.replace('_predict',''),y) else '    -   ' for (x,y) in zip(catNames,sampNames)])))+"\n")




        #Write out paramters for ABCD method based on rate params in the higgs tool
        params = ('kappa','beta','delta')
        addParam = ''
        betaQCDname= ''
        deltaQCDname= ''
        for yd,p in zip(ydsKappa[bin], params):
            Val = yd.val
            Err = yd.err
            Name = yd.name
            SB = yd.sbname
            MB = yd.mbname
            Label = yd.label

            if 'QCD' in yd.name: name = p+yd.name +'_'+ Label 
            if Val > 0.01 and p == 'beta' and obs0==False:
                addParam = addParam+p
                betaQCDname = Name+'_'+Label
                datacard.write(name + ' param ' + valToBar(Val) +' ' + valToBar(Err) + '  \n')
            elif Val > 0.01 and p == 'delta':
                addParam = addParam + p
                deltaQCDname = Name+'_'+Label
                datacard.write(name + ' param ' + valToBar(Val) +' ' + valToBar(Err) + '  \n')
            elif p == 'kappa':
                name = p+'_'+ bin
                datacard.write(name + ' param ' + valToBar(Val) +' ' + valToBar(Err) + '\n')

        betaName = ''; gammaName = ''; deltaName = '';
        params = ('alpha','beta','gamma','delta')
        for yd,p in zip(ydsObs[bin], params):
            if p == 'beta': betaName = yd.label
            if p == 'gamma': gammaName = yd.label
            if p == 'delta': deltaName = yd.label



        formula = '(@0*@1/@2*@3)'
        paramIn = 'beta_' + betaName + ',gamma_' + gammaName + ',delta_' + deltaName + ',kappa_' + bin
        if 'beta' in addParam and 'delta' in addParam: 
            formula = formula.replace('@0','(@0-@4)').replace('@2','(@2-@5)')
            paramIn = paramIn +',beta' + betaQCDname + ',delta' + deltaQCDname
        elif addParam == 'beta':
            formula = formula.replace('@0','(@0-@4)')
            paramIn = paramIn +',beta' + betaQCDname
        elif addParam == 'delta': 
            formula = formula.replace('@2','(@2-@4)')
            paramIn = paramIn +',delta' + deltaQCDname

            
        for yd,p in zip(ydsObs[bin], params):
            postFix = bin + '_' + yd.cat
            if p == 'alpha':
                datacard.write(p + '_' + yd.label + ' rateParam ' +yd.cat.replace('_predict','') + ' ' + yd.name.replace('background','data') + ' ' + formula + ' ' + paramIn + '\n')
            else:
                datacard.write(p + '_' + yd.label + ' rateParam ' +yd.cat.replace('_predict','') + ' ' + yd.name.replace('background','data')  + ' ' + str(round(yd.val)) + ' [0,'+str(round(yd.val*3))+'] \n')


                
    return 1 

def numToBar(num):
    r = num
    if type(num) == float and abs(num - 1.0) < 0.001:
        r = '   -  '
    else: r = '%1.3f' % num
    return r

def valToBar(num):
    r = '%1.3f' % num
    return r

if __name__ == "__main__":

    ## remove '-b' option
    if '-b' in sys.argv:
        sys.argv.remove('-b')
        _batchMode = True

    if len(sys.argv) > 1:
        out = sys.argv[1]
        print '# out is', out
    else:
        print "No output folder name given!!"
        exit(0)

    ## Create Yield Storage
    ydsSys = YieldStore("lepYields") 
    storeDict = True

    #Define Signal pickle file
    pckname = "pickles/"+SMS+"_sigSysts_2016_all.pckz"
    if storeDict == True and os.path.exists(pckname):

        print "#Loading saved yields from pickle!"

        import cPickle as pickle
        import gzip

        ydsSys = pickle.load( gzip.open( pckname, "rb" ) )
#        print [name for name in ydsSys.samples if ("syst" in name and "mGo1500_mLSP1000" in name)]
 
    yds6 = YieldStore("lepYields")
    yds9 = YieldStore("lepYields")
    pattern = "test12p9/*/merged/LT*NJ68.*"
    yds6.addFromFiles(pattern,("lep","sele")) 
    pattern = "test12p9/*/merged/LT*NJ9i.*"
    yds9.addFromFiles(pattern,("lep","sele"))


    
#    yds6.showStats()
#    yds9.showStats()

    ####SELECT DATA OR MC### (turn into options for the commandline at some point)
    useMC = False
    prefix =  'data'
    if useMC:
        prefix = 'background'

    readSystFile()
    for mGo in range(600, 2000, 25):
       for mLSP in range(0,1200,25):

#    for mGo in range(1400, 1550, 50):
#        for mLSP in range(50,150,50):
            for ydIn in (yds6, yds9):
                print "making datacards for "+str(mGo)+ ' '+str(mLSP)
                signal = SMS+'_Scan_mGo'+str(mGo)+'_mLSP'+str(mLSP)
                cat = 'SR_MB'
                sampsObs = [('background',cat),]
                ydsObs = ydIn.getMixDict(sampsObs)
                sampsBkg = [('TTsemiLep',cat),('TTdiLep',cat),('TTV',cat), ('SingleT',cat), ('WJets',cat), ('DY',cat), ('QCD',cat),]
                sampsSig = [(signal ,cat),]
                samps = sampsBkg + sampsSig
                ydsSig = ydIn.getMixDict(sampsSig)
                if type(ydsSig.values()[0][0]) == int:
                    print "signal not available will skip"
                    continue
                
                yds = ydIn.getMixDict(samps)

                
                cats = ('SR_MB', 'CR_MB', 'SR_SB','CR_SB')
                catsNoSR = ('CR_MB', 'SR_SB','CR_SB')
                
                sampsABCDbkg = [(prefix,cat) for cat in catsNoSR]
                sampsABCDbkg.insert(0,(prefix,'SR_MB'))


                sampsABCDsig = [(SMS+'_Scan_mGo'+str(mGo)+'_mLSP'+str(mLSP),cat) for cat in cats]

                cat = 'SR_MB'
                #select all uncertainites we have in the pickle file
                sampsABCDSigSys = [(SMS+'_Scan_JEC_syst_mGo'+str(mGo)+'_mLSP'+str(mLSP), 'SR_MB'),
                                   (SMS+'_Scan_ISR_syst_mGo'+str(mGo)+'_mLSP'+str(mLSP), 'SR_MB'),
                                   (SMS+'_Scan_btagHF_syst_mGo'+str(mGo)+'_mLSP'+str(mLSP), 'SR_MB'), 
                                   (SMS+'_Scan_btagLF_syst_mGo'+str(mGo)+'_mLSP'+str(mLSP), 'SR_MB'),
                                   (SMS+'_Scan_Scale-Env_syst_mGo'+str(mGo)+'_mLSP'+str(mLSP), 'SR_MB'),
                                   (SMS+'_Scan_MET_syst_mGo'+str(mGo)+'_mLSP'+str(mLSP), 'SR_MB'), 
                                  ]
                #print sampsABCDSigSys
                sampsABCD = sampsABCDbkg + sampsABCDsig
                
                ydsABCD = ydIn.getMixDict(sampsABCD)
                ydsObsABCD = ydIn.getMixDict(sampsABCDbkg)

                ydsKappa = ydIn.getMixDict([('EWK','Kappa'), (prefix+'_QCDpred','CR_MB'), (prefix+'_QCDpred','CR_SB') ])
                ydsABCDSigSys = ydsSys.getMixDict(sampsABCDSigSys)
                
                printABCDCard(ydsABCD, ydsObsABCD, ydsKappa, ydsABCDSigSys)
                
