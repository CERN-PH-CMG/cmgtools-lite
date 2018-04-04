import optparse, subprocess, ROOT, datetime, math, array, copy, os
import numpy as np

#doPUreweighting = True
doPUandSF = False

def printAggressive(s):
    print '='.join('' for i in range(len(s)+1))
    print s
    print '='.join('' for i in range(len(s)+1))

def readScaleFactor(path, process, reterr = False):
    infile = open(path,'r')
    lines = infile.readlines()
    
    for line in lines:
        if 'Process {proc} scaled by'.format(proc=process) in line:
            scale = float(line.split()[4])
            scaleerr = float(line.split()[-1])
    if not reterr:
        return scale
    else:
        return scale, scaleerr

def readFakerate(path, process):
    infile = open(path,'r')
    lines = infile.readlines()
    index = 999
    for ind,line in enumerate(lines):
        if process in line and '===' in line:
            index = ind
    frs = []; errs = []
    for il, line in enumerate(lines):
        if il < index+3: continue
        if len(line)==1: break
        frs.append(float(line.split()[2]))
        down = float(line.split()[3].replace('--','-'))
        up   = float(line.split()[4].replace('++','+'))
        errs.append( (abs(down)+abs(up))/2.)
    ##fr  = float(lines[index+3].split()[2])
    ##err = (abs(float(lines[index+3].split()[3])) + abs(float(lines[index+3].split()[4])) )/2.
    print('this is frs:', frs)
    return frs, errs

def runCards(trees, friends, targetdir, fmca, fcut, fsyst, plotbin, enabledcuts, disabledcuts, processes, scaleprocesses, extraopts = ''):

    if not type(trees)==list: trees = [trees]
    treestring = ' '.join(' -P '+ t for t in list(trees))

    cmd  = ' makeShapeCardsSusy.py --s2v -f -j 6 -l {lumi} --od {td} {trees} {fmca} {fcut}'.format(lumi=lumi, td=targetdir, trees=treestring, fmca=fmca, fcut=fcut)
    cmd += ' {plotvar} {binning}'.format(plotvar=plotbin.split()[0], binning=plotbin.split()[1])
    if friends:
        cmd += ' --Fs {friends}'.format(friends=friends)
    cmd += ' --mcc ttH-multilepton/mcc-eleIdEmu2.txt '
    cmd += ' -W puw2016_nTrueInt_36fb(nTrueInt) ' 
    cmd += ' -p '+','.join(processes)
    cmd += ''.join(' -E ^'+cut for cut in enabledcuts )
    cmd += ''.join(' -X ^'+cut for cut in disabledcuts)
    if scaleprocesses:
        for proc,scale in scaleprocesses.items():
            cmd += ' --scale-process {proc} {scale} '.format(proc=proc, scale=scale)
    cmd += ' {fsyst} '.format(fsyst=fsyst)
    if extraopts:
        cmd += ' '+extraopts

#example command
#python makeShapeCardsSusy.py --s2v -P /afs/cern.ch/work/e/efascion/DPStrees/TREES_110816_2muss/ --Fs /afs/cern.ch/work/e/efascion/public/friendsForDPS_110816/ -l 12.9 dps-ww/final_mca.txt dps-ww/cutfinal.txt finalMVA_DPS 10,0.,1.0  --od dps-ww/cards -p DPSWW,WZ,ZZ,WWW,WpWpJJ,Wjets  -W 0.8874 --asimov dps-ww/syst.txt
    print '============================================================================================='
    print 'running: python', cmd
    print '============================================================================================='
    subprocess.call(['python']+cmd.split())#+['/dev/null'],stderr=subprocess.PIPE)
    

def runefficiencies(trees, friends, targetdir, fmca, fcut, ftight, fxvar, enabledcuts, disabledcuts, scaleprocesses, compareprocesses, showratio, extraopts = ''):
    
    if not type(trees)==list: trees = [trees]
    treestring = ' '.join(' -P '+ t for t in list(trees))
    cmd  = ' mcEfficiencies.py --s2v -f -j 6 -l {lumi} -o {td} {trees} {fmca} {fcut} {ftight} {fxvar}'.format(lumi=lumi, td=targetdir, trees=treestring, fmca=fmca, fcut=fcut, ftight=ftight, fxvar=fxvar)
    if friends:
        #cmd += ' --Fs {friends}'.format(friends=friends)
        #cmd += ' -F mjvars/t {friends}/friends_evVarFriend_{{cname}}.root --FMC sf/t {friends}/friends_sfFriend_{{cname}}.root  '.format(friends=friends)
        cmd += ' -F Friends {friends}/tree_Friend_{{cname}}.root'.format(friends=friends)
    # not needed here cmd += ' --mcc ttH-multilepton/mcc-eleIdEmu2.txt --mcc dps-ww/mcc-tauveto.txt '
    ## cmd += ' --obj treeProducerWMassEle ' ## the tree is called 'treeProducerWMassEle' not 'tree'
    cmd += ' --groupBy cut '
    ## if doPUreweighting: cmd += ' -W puw_8TeV_nVert_dataWjets(nVert) ' ## adding pu weight
    # if doPUreweighting: cmd += ' -W puWeight ' ## adding pu weight
    if doPUandSF and not '-W ' in extraopts: cmd += ' -W puWeight*LepGood_effSF[0] '
    cmd += ''.join(' -E ^'+cut for cut in enabledcuts )
    cmd += ''.join(' -X ^'+cut for cut in disabledcuts)
    cmd += ' --compare {procs}'.format(procs=(','.join(compareprocesses)  ))
    if scaleprocesses:
        for proc,scale in scaleprocesses.items():
            cmd += ' --scale-process {proc} {scale} '.format(proc=proc, scale=scale)
    showrat   = ''
    if showratio:
        showrat = ' --showRatio '
    cmd += showrat
    if extraopts:
        cmd += ' '+extraopts

    print 'running: python', cmd
    subprocess.call(['python']+cmd.split())#+['/dev/null'],stderr=subprocess.PIPE)


def runplots(trees, friends, targetdir, fmca, fcut, fplots, enabledcuts, disabledcuts, processes, scaleprocesses, fitdataprocess, plotlist, showratio, extraopts = '', invertedcuts = []):
    
    if not type(trees)==list: trees = [trees]
    treestring = ' '.join(' -P '+ t for t in list(trees))
    cmd  = ' mcPlots.py --s2v -f -j 6 -l {lumi} --pdir {td} {trees} {fmca} {fcut} {fplots}'.format(lumi=lumi, td=targetdir, trees=treestring, fmca=fmca, fcut=fcut, fplots=fplots)
    if friends:
        if not type(friends)==list: friends = [friends]
        for f in friends:
            cmd += ' -F Friends {friends}/tree_Friend_{{cname}}.root'.format(friends=f)
    cmd += ''.join(' -E ^'+cut for cut in enabledcuts )
    cmd += ''.join(' -X ^'+cut for cut in disabledcuts)
    cmd += ' --sP '+','.join(plot for plot in plotlist)
    cmd += ' -p '+','.join(processes)
    if invertedcuts:
        cmd += ''.join(' -I ^'+cut for cut in invertedcuts )
    if doPUandSF and not '-W ' in extraopts: cmd += ' -W puWeight*LepGood_effSF[0] ' ##_get_muonSF_trgIsoID(LepGood_pdgId[0],LepGood_pt[0],LepGood_eta[0],0)' ## adding pu weight
    cmd += ' -o '+targetdir+'/'+'_AND_'.join(plot for plot in plotlist)+'.root'
    if fitdataprocess:
        cmd+= ' --fitData '
        cmd+= ''.join(' --flp '+proc for proc in fitdataprocess)
    if scaleprocesses:
        for proc,scale in scaleprocesses.items():
            cmd += ' --scale-process {proc} {scale} '.format(proc=proc, scale=scale)
    showrat   = ''
    if showratio:
        showrat = ' --showRatio '
    cmd += showrat
    if extraopts:
        cmd += ' '+extraopts

    print 'running: python', cmd
    subprocess.call(['python']+cmd.split())#+['/dev/null'],stderr=subprocess.PIPE)

def makeResults(onlyMM = True, splitCharge = True): #sfdate, onlyMM = True, splitCharge = True):
#def runCards(trees, friends, targetdir, fmca, fcut, fsyst, plotbin, enabledcuts, disabledcuts, processes, scaleprocesses, extraopts = ''):
#python makeShapeCardsSusy.py --s2v -P /afs/cern.ch/work/e/efascion/DPStrees/TREES_110816_2muss/ --Fs /afs/cern.ch/work/e/efascion/public/friendsForDPS_110816/ -l 12.9 dps-ww/final_mca.txt dps-ww/cutfinal.txt finalMVA_DPS 10,0.,1.0  --od dps-ww/cards -p DPSWW,WZ,ZZ,WWW,WpWpJJ,Wjets  -W 0.8874 --asimov dps-ww/syst.txt
    
    #sfs = calculateScalefactors(False, sfdate)

    targetcarddir = 'cards/{date}{pf}/'.format(date=date, pf=('-'+postfix if postfix else '') )
    trees     = '/eos/user/m/mdunser/dps-13TeV-combination/TREES_latest/'
    friends = [trees+'/friends/', trees+'/friends_bdt/']
    #    targetdir = '/afs/cern.ch/user/m/mdunser/www/private/dps-ww-combination/results/{date}{pf}/'.format(date=date, pf=('-'+postfix if postfix else '') )
    targetdir = '/eos/user/a/anmehta/www/{date}{pf}Complete_newbinning/'.format(date=date, pf=('-'+postfix if postfix else '') )
    fcut   = 'dpsww13TeV/dps2016/results/cuts_results.txt'#mumuelmu_mca.txt'
    fplots = 'dpsww13TeV/dps2016/results/plots.txt'
    fsyst  = 'dpsww13TeV/dps2016/results/syst.txt'


    print '=========================================='
    print 'run results for MUMU'
    print '=========================================='

    if splitCharge: 
        loop = [ ['plusplus'], ['minusminus']]
    else:
        loop = [ [] ]

    print 'did i split the charge?'

    processes      = ['data', 'DPSWW', 'WZ', 'ZZ', 'WG_wg', 'rares', 'fakes_data']
    processesCards = ['data', 'DPSWW', 'WZ', 'ZZ', 'WG_wg', 'rares', 'fakes_data', 'WZamcatnlo']#, 'DPSWW_alt']

    binningBDT   = ' (BDT_DPS_WZ*BDT_DPS_fakes) 20,0.,1. '
    nbinspostifx = '_20bins'

    fmca   = 'dpsww13TeV/dps2016/results/mumuelmu_mca.txt'
    
    for ich,ch in enumerate(loop):
        #if not ich: continue
        enable    = ['trigmumu', 'mumu'] + ch
        disable   = []
        fittodata = []
        scalethem = {'WZ': '{sf:.3f}'.format(sf=1.04),
                     'ZZ': '{sf:.3f}'.format(sf=1.21)}
        mumusf = 0.95
        extraopts = ' -W {sf:.3f} --showIndivSigs'.format(sf=mumusf)# --plotmode=norm
        #        makeplots = ['BDTfakes_BDTWZ_mumu','BDT_wz_mumu',
        makeplots = ['BDT_wz_mumu'+(ch[0] if ch else '')+nbinspostifx]
#        makeplots=['BDT_wz_mumuplusplus_20bins','BDT_wz_mumuminusminus_20bins','BDT_fakes_mumuplusplus_20bins','BDT_fakes_mumuminusminus_20bins','BDTfakes_BDTWZ_mumuminusminus_20bins','BDTfakes_BDTWZ_mumuplusplus_20bins']
        runplots(trees, friends, targetdir, fmca, fcut, fplots, enable, disable, processes, scalethem, fittodata, makeplots, True, extraopts)
        ## ==================================
        ## running datacards
        ## ==================================
        ####    foobar extraoptscards = ' -W {sf:.3f} -o mumu{ch} -b mumu{ch} '.format(sf=mumusf, ch=(ch[0] if ch else ''))
        ####    foobar runCards(trees, friends, targetcarddir, fmca, fcut, fsyst , binningBDT, enable, disable, processesCards, scalethem, extraoptscards)


def simplePlot():
    print '=========================================='
    print 'running simple plots'
    print '=========================================='
    trees     = ['/eos/user/m/mdunser/w-helicity-13TeV/trees/trees_all_skims/']
    friends   = '/afs/cern.ch/work/a/anmehta/work/TestingWW2/CMSSW_8_0_25/src/CMGTools/DPS13TeV/python/postprocessing/Full_Singlemu_friends_v1//'
    targetdir = '/eos/user/a/anmehta/www/{date}{pf}SingleMuComplete/'.format(date=date, pf=('-'+postfix if postfix else '') )
    fmca      = 'dpsww13TeV/dps2016/simple/mca_simple.txt'
    fcut      = 'dpsww13TeV/dps2016/simple/cuts_simple.txt'
    fplots    = 'dpsww13TeV/dps2016/simple/plots.txt'
    enable    = []
    disable   = []
    processes = ['WZ','WW',]
    fittodata = []
    scalethem = {}
    extraopts = '' #--maxRatioRange 0.8 1.2 --fixRatioRange ' #'--plotmode=norm '
    makeplots = ['BDT_fakes','BDT_WZ','BDT_WZXBDT_fakes','BDTfakes_BDTWZ'] #weightLongPlus', 'weightLeftPlus', 'weightRightPlus'] #'mtl1tk', 'etal1', 'ptl1']#'nVert', 'ptl1', 'etal1', 'mtl1tk', 'mtl1pf', 'tkmet', 'pfmet']
    showratio = False
    runplots(trees, friends, targetdir, fmca, fcut, fplots, enable, disable, processes, scalethem, fittodata, makeplots, showratio, extraopts)
    
def fakesDataMC():
    print '=========================================='
    print 'running fake closure/validation plots'
    print '=========================================='
    trees     = ['/eos/cms/store/group/phys_tracking/elisabetta/WSkims/']
    friends   = '/eos/user/m/mdunser/w-helicity-13TeV/friends/friends_SFs_2017-12-01/'
    targetdir = '/afs/cern.ch/user/m/mdunser/www/private/w-helicity-13TeV/fakes-dataMC/{date}{pf}/'.format(date=date, pf=('-'+postfix if postfix else '') )
    fmca      = 'w-helicity-13TeV/wmass_mu/FRfast/mca_fr_closure.txt'
    fcut      = 'w-helicity-13TeV/wmass_mu/FRfast/cuts_fr_closure.txt'
    fplots    = 'w-helicity-13TeV/wmass_mu/FRfast/plots.txt'

    enable    = []
    disable   = []
    processes = ['data', 'WandZ', 'fakes_data', 'Top', 'DiBosons']
    fittodata = []
    scalethem = {}
    extraopts = ' '# --maxRatioRange 0. 2. --fixRatioRange  '
    makeplots = ['nVert']#'ptl1', 'etal1', 'tkmetcoarse', 'mtl1tkcoarse']
    showratio = True
    runplots(trees, friends, targetdir, fmca, fcut, fplots, enable, disable, processes, scalethem, fittodata, makeplots, showratio, extraopts)
    
def dyComparison():
    print '=========================================='
    print 'running checks on DY '
    print '=========================================='
    trees     = ['/eos/cms/store/group/phys_tracking/elisabetta/WSkims/']
    friends   = '/eos/user/m/mdunser/w-helicity-13TeV/friends/friends_SFs_pu_awayJet-2017-12-11/'#2017-12-01/'
    targetdir = '/afs/cern.ch/user/m/mdunser/www/private/w-helicity-13TeV/dy-dataMC/{date}{pf}/'.format(date=date, pf=('-'+postfix if postfix else '') )
    fmca      = 'w-helicity-13TeV/wmass_mu/dy/mca.txt'
    fcut      = 'w-helicity-13TeV/wmass_mu/dy/cuts.txt'
    fplots    = 'w-helicity-13TeV/wmass_mu/dy/plots.txt'

    enable    = []
    disable   = []
    processes = ['data', 'Z']## very small:, 'Top', 'DiBosons']
    fittodata = []
    scalethem = {}
    extraopts = ' -W LepGood_effSF[0]*LepGood_effSF[1] --maxRatioRange 0.8 1.2 --fixRatioRange '# --maxRatioRange 0. 2. --fixRatioRange  '
    makeplots = ['rho', 'nVert']#'etal2']#, 'ptl1', 'etal1', 'ptl2', 'mll']#'etal2', 'nVert', 'mll', 'tkmet', 'pfmet']
    showratio = True
    runplots(trees, friends, targetdir, fmca, fcut, fplots, enable, disable, processes, scalethem, fittodata, makeplots, showratio, extraopts)
    
def fakeShapes():
    print '=========================================='
    print 'running fake shape plots'
    print '=========================================='
    trees     = ['/afs/cern.ch/work/m/mdunser/public/wHelicityTrees/TREES_1LEP_53X_V2/']
    friends   = '/eos/cms/store/cmst3/group/susy/emanuele/wmass/trees/TREES_1LEP_53X_V2/'
    targetdir = '/afs/cern.ch/user/m/mdunser/www/private/w-helicity-8TeV/fakes-sanity/{date}{pf}/'.format(date=date, pf=('-'+postfix if postfix else '') )
    fmca      = 'w-helicity/FR/mca_fr_closure.txt'
    fcut      = 'w-helicity/FR/cuts_fr_closure.txt'
    fplots    = 'w-helicity/FR/plots_fr_closure.txt'

    enable    = []
    disable   = ['muonTightIso']
    invert    = []
    processes = ['data', 'wjets', 'qcd', 'singleTop', 'ttjets', 'diboson', 'dyjets']
    fittodata = ['qcd']
    scalethem = {}
    extraopts = ' --maxRatioRange 0. 2. '
    makeplots = ['l1reliso03',]# 'mtl1tk', 'pfmet', 'ptl1', 'etal1']
    showratio = True
    runplots(trees, friends, targetdir, fmca, fcut, fplots, enable, disable, processes, scalethem, fittodata, makeplots, showratio, extraopts, invert)



def makeFakeRatesFast(recalculate):
    trees     = ['/eos/cms/store/group/phys_tracking/elisabetta/WSkims/']
    friends   = '/eos/user/m/mdunser/w-helicity-13TeV/friends/friends_SFs_pu_awayJet-2017-12-11/'
    targetdir = '/afs/cern.ch/user/m/mdunser/www/private/w-helicity-13TeV/fakerates/{date}{pf}/'.format(date=date, pf=('-'+postfix if postfix else '') )

    fmca   = 'w-helicity-13TeV/wmass_mu/FRfast/mca_fr.txt' 
    fcut   = 'w-helicity-13TeV/wmass_mu/FRfast/cuts_fr.txt'
    fplots = 'w-helicity-13TeV/wmass_mu/FRfast/plots.txt'       
    ftight = 'w-helicity-13TeV/wmass_mu/FRfast/tightCut.txt'    
    processes = ['data', 'QCD', 'WandZ']
    compprocs = ['QCD', 'data', 'data_sub', 'WandZ']#, 'total']
    fittodata = ['QCD', 'WandZ']
    makeplots = ['mtl1tk', 'reliso03'] ## the first plot here is the one from which the scale factors are derived!!!
    
    binning = [25,27,30,33,35,37,39,41,43,45,55,100] ## from xvars.txt
    binningeta = [0,1.2,2.4]
    #binning = [25,30,35,40,50,100] ## from xvars.txt
    h_name  = 'fakerate_mu'; h_title = 'fakerates muons'

    h_fakerate_data = ROOT.TH2F(h_name+'_data',h_title+' - data', len(binning)-1, array.array('f',binning), len(binningeta)-1, array.array('f',binningeta))
    h_fakerate_mc   = ROOT.TH2F(h_name+'_qcd' ,h_title+' - qcd' , len(binning)-1, array.array('f',binning), len(binningeta)-1, array.array('f',binningeta))
    h_fakerate_data .Sumw2()
    h_fakerate_mc   .Sumw2()
    h_fakerate_data .GetZaxis().SetRangeUser(0.01,0.45)
    h_fakerate_mc   .GetZaxis().SetRangeUser(0.01,0.45)
    h_fakerate_data .GetXaxis().SetTitle('p_{T} mu'); h_fakerate_data .GetYaxis().SetTitle('#eta mu')
    h_fakerate_mc   .GetXaxis().SetTitle('p_{T} mu'); h_fakerate_mc   .GetYaxis().SetTitle('#eta mu')

    h_name  = 'promptrate_mu'; h_title = 'promptrates muons'
    h_promptrate_data = ROOT.TH2F(h_name+'_data',h_title+' - data', len(binning)-1, array.array('f',binning), len(binningeta)-1, array.array('f',binningeta))
    h_promptrate_mc   = ROOT.TH2F(h_name+'_qcd' ,h_title+' - qcd' , len(binning)-1, array.array('f',binning), len(binningeta)-1, array.array('f',binningeta))
    h_promptrate_data .Sumw2()
    h_promptrate_mc   .Sumw2()
    h_promptrate_data .GetZaxis().SetRangeUser(0.5,1.00)
    h_promptrate_mc   .GetZaxis().SetRangeUser(0.5,1.00)
    h_promptrate_data .GetXaxis().SetTitle('p_{T} mu'); h_promptrate_data .GetYaxis().SetTitle('#eta mu')
    h_promptrate_mc   .GetXaxis().SetTitle('p_{T} mu'); h_promptrate_mc   .GetYaxis().SetTitle('#eta mu')

    ## add MT cut to the eff plot!
    fakerates = {}; promptrates = {}
    scales = {}
    printAggressive('STARTING FAKE RATES...!')
    for j,eta in enumerate(['barrel', 'endcap']):
        #if not j == 1: continue
        scalethem = {}
        etastring = '{eta}'.format(eta=eta)
        enable    = [eta]
        disable   = ['muonTightIso']
        newplots = [('mu_'+eta+'_'+plot) for plot in makeplots]
        extraopts = ''
        if recalculate: runplots(trees, friends, targetdir, fmca, fcut, fplots, enable, disable, processes, scalethem, fittodata, newplots, True, extraopts)
        printAggressive('DONE MAKING THE PLOTS TO DERIVE THE EWK SCALE FACTORS!')
        scales['qcd_{eta}'  .format(eta=etastring)] = readScaleFactor(targetdir+'/mu_{eta}_{plot}.txt'.format(eta=etastring, plot=makeplots[0]), 'QCD')
        scales['wandz_{eta}'.format(eta=etastring)] = readScaleFactor(targetdir+'/mu_{eta}_{plot}.txt'.format(eta=etastring, plot=makeplots[0]), 'WandZ')
        enable  = [eta, 'pfmet15max', 'mtl1tk40max']
        disable = ['muonTightIso']
        scalethem = {'QCD'  : scales['qcd_{eta}'  .format(eta=etastring)],
                     'WandZ': scales['wandz_{eta}'.format(eta=etastring)]}
        fxvar  = 'w-helicity-13TeV/FRfast/xvars.txt'
        ## reproduce plots with MT and MET included
        printAggressive('SCALING THE PROCESSES BY FACTORS')
        print scalethem
        if recalculate: runplots(trees, friends, targetdir+'/mtMetCutsIncluded/', fmca, fcut, fplots, enable, disable, processes, scalethem, [], newplots, True, extraopts) ## don't fit to data anymore
        extraopts = ' --ratioRange 0 2 --sp QCD '
        if recalculate: runefficiencies(trees, friends, targetdir+'/fr_mu_{eta}'.format(eta=etastring), fmca, fcut, ftight, fxvar, enable, disable, scalethem, compprocs, True, extraopts)
        fakerates['fr_mu_qcd_{eta}'.format(eta=etastring)] = readFakerate(targetdir+'/fr_mu_{eta}.txt'.format(eta=etastring),'QCD')
        fakerates['fr_mu_dat_{eta}'.format(eta=etastring)] = readFakerate(targetdir+'/fr_mu_{eta}.txt'.format(eta=etastring),'Data - EWK')

        promptrates['fr_mu_qcd_{eta}'.format(eta=etastring)] = readFakerate(targetdir+'/fr_mu_{eta}.txt'.format(eta=etastring),'WandZ')
        promptrates['fr_mu_dat_{eta}'.format(eta=etastring)] = readFakerate(targetdir+'/fr_mu_{eta}.txt'.format(eta=etastring),'WandZ')

        for i in range(len(fakerates['fr_mu_qcd_{eta}'.format(eta=etastring)][0])):
            h_fakerate_data.SetBinContent(i+1,j+1, fakerates['fr_mu_dat_{eta}'.format(eta=etastring)][0][i])
            h_fakerate_data.SetBinError  (i+1,j+1, fakerates['fr_mu_dat_{eta}'.format(eta=etastring)][1][i])
            h_fakerate_mc  .SetBinContent(i+1,j+1, fakerates['fr_mu_qcd_{eta}'.format(eta=etastring)][0][i])
            h_fakerate_mc  .SetBinError  (i+1,j+1, fakerates['fr_mu_qcd_{eta}'.format(eta=etastring)][1][i])
            h_promptrate_data.SetBinContent(i+1,j+1, promptrates['fr_mu_dat_{eta}'.format(eta=etastring)][0][i])
            h_promptrate_data.SetBinError  (i+1,j+1, promptrates['fr_mu_dat_{eta}'.format(eta=etastring)][1][i])
            h_promptrate_mc  .SetBinContent(i+1,j+1, promptrates['fr_mu_qcd_{eta}'.format(eta=etastring)][0][i])
            h_promptrate_mc  .SetBinError  (i+1,j+1, promptrates['fr_mu_qcd_{eta}'.format(eta=etastring)][1][i])

    h_fakerate_data_frUp = h_fakerate_data.Clone(h_fakerate_data.GetName()+'_frUp')
    h_fakerate_mc_frUp   = h_fakerate_mc  .Clone(h_fakerate_mc  .GetName()+'_frUp')
    h_fakerate_data_frUp.Scale(1.1)
    h_fakerate_mc_frUp  .Scale(1.1)

    h_fakerate_data_frDn = h_fakerate_data.Clone(h_fakerate_data.GetName()+'_frDn')
    h_fakerate_mc_frDn   = h_fakerate_mc  .Clone(h_fakerate_mc  .GetName()+'_frDn')
    h_fakerate_data_frDn.Scale(0.9)
    h_fakerate_mc_frDn  .Scale(0.9)

    ROOT.gROOT.SetBatch()
    ROOT.gStyle.SetOptStat(0)
    canv = ROOT.TCanvas()
    #canv.SetLogx()
    ROOT.gStyle.SetPaintTextFormat(".3f")
    h_fakerate_data.Draw('colz text45 e')
    canv.SaveAs(targetdir+'fakerate_mu_data_{date}.png'.format(date=date))
    canv.SaveAs(targetdir+'fakerate_mu_data_{date}.pdf'.format(date=date))
    h_fakerate_mc  .Draw('colz text45 e')
    canv.SaveAs(targetdir+'fakerate_mu_qcd_{date}.png'.format(date=date))
    canv.SaveAs(targetdir+'fakerate_mu_qcd_{date}.pdf'.format(date=date))
    h_promptrate_data.Draw('colz text45 e')
    canv.SaveAs(targetdir+'promptrate_mu_data_{date}.png'.format(date=date))
    canv.SaveAs(targetdir+'promptrate_mu_data_{date}.pdf'.format(date=date))
    h_promptrate_mc  .Draw('colz text45 e')
    canv.SaveAs(targetdir+'promptrate_mu_qcd_{date}.png'.format(date=date))
    canv.SaveAs(targetdir+'promptrate_mu_qcd_{date}.pdf'.format(date=date))
    outfile = ROOT.TFile('w-helicity-13TeV/wmass_mu/fakerateMap_mu_{date}{pf}.root'.format(date=date,pf=('_'+postfix if postfix else '')),'RECREATE')
    h_fakerate_data.Write()
    h_fakerate_mc  .Write()
    h_fakerate_data_frUp.Write()
    h_fakerate_mc_frUp  .Write()
    h_fakerate_data_frDn.Write()
    h_fakerate_mc_frDn  .Write()
    outfile.Close()

    outfile = ROOT.TFile('w-helicity-13TeV/wmass_mu/promptrateMap_mu_{date}{pf}.root'.format(date=date,pf=('_'+postfix if postfix else '')),'RECREATE')
    h_promptrate_data.Write()
    h_promptrate_mc  .Write()
    #h_promptrate_data_frUp.Write()
    #h_promptrate_mc_frUp  .Write()
    #h_promptrate_data_frDn.Write()
    #h_promptrate_mc_frDn  .Write()
    outfile.Close()
    
    print scales
    print fakerates
    print promptrates

    h_fr_smoothed_data = ROOT.TH2F('fakerates_smoothed_data',' fakerates - smoothed data', len(binningeta)-1, array.array('f',binningeta), 2, array.array('f',[0., 1., 2.]))
    #h_fr_smoothed_mc   = ROOT.TH2F(h_name+'_qcd' ,h_title+' - qcd' , len(binning)-1, array.array('f',binning), len(binningeta)-1, array.array('f',binningeta))

    for eta in ['barrel', 'endcap']:
        graph_file= ROOT.TFile(targetdir+'/fr_mu_{eta}'.format(eta=eta), 'read')
        graph= graph_file.Get('muonTightIso_pt_fine_binned_data_sub')

        pol0 = ROOT.TF1("pol0_{eta}".format(eta=eta), "[0]        ", 25., 50.)
        pol1 = ROOT.TF1("pol1_{eta}".format(eta=eta), "[1]*x + [0]", 25., 50.)

        pol0.SetLineColor(ROOT.kGreen); pol0.SetLineWidth(2)
        pol1.SetLineColor(ROOT.kRed-3); pol1.SetLineWidth(2)

        #pol0.SetParameter(1, graph.Eval(25.))
        #pol1.SetParameter(1, graph.Eval(25.)); pol1.SetParameter(2, 0.)

        pol0.SetParLimits(1, 0.1, 0.4)
        pol1.SetParLimits(1, -0.1  , 0.0)
        pol1.SetParLimits(0,  0.1  , 1.1)

        graph.Fit("pol0_{eta}".format(eta=eta), "M", "", 25., 50.)
        graph.Fit("pol1_{eta}".format(eta=eta), "M", "", 30., 45.)
        #graph.Fit("pol0", "M", "", 25., 50.)
        #graph.Fit("pol1", "M", "", 25., 50.)

        pol0_chi2 = pol0.GetChisquare(); pol0_ndf = pol0.GetNDF()
        pol1_chi2 = pol1.GetChisquare(); pol1_ndf = pol1.GetNDF()

        rchi2_0 = pol0_chi2/pol0_ndf
        rchi2_1 = pol1_chi2/pol1_ndf

        bestfunc = pol0 if rchi2_0 < rchi2_1 else pol1
        worstfun = pol0 if rchi2_0 > rchi2_1 else pol1

        print '{eta}: chi2 of pol0 = {chi0}/{ndf0} = {red0}'.format(eta=eta,chi0=pol0_chi2,ndf0=pol0_ndf, red0=rchi2_0)
        print '{eta}: chi2 of pol1 = {chi1}/{ndf1} = {red1}'.format(eta=eta,chi1=pol1_chi2,ndf1=pol1_ndf, red1=rchi2_1)

        print 'the better function is {func}'.format(func=bestfunc.GetName())

        #print '{eta}: compared to {func}         .   value={val:.3f}'.format(eta=eta, func = worstfun.GetName(), val=worstfun.GetChisquare()/worstfun.GetNDF())
        
        etabin = 1 if eta == 'barrel' else 2
        
        h_fr_smoothed_data.SetBinContent(etabin, 1, bestfunc.GetParameter(0))
        h_fr_smoothed_data.SetBinError  (etabin, 1, bestfunc.GetParError (0))

        h_fr_smoothed_data.SetBinContent(etabin, 2, bestfunc.GetParameter(1) if bestfunc.GetNpar() > 1 else 0.)
        h_fr_smoothed_data.SetBinError  (etabin, 2, bestfunc.GetParError (1) if bestfunc.GetNpar() > 1 else 0.)

        graph.Draw('ape')
        graph.GetYaxis().SetRangeUser(0., 0.5)
        pol0.Draw('same')
        pol1.Draw('same')
        canv.SaveAs(targetdir+'fakerate_fit_data_{eta}.png'.format(eta=eta))
        canv.SaveAs(targetdir+'fakerate_fit_data_{eta}.pdf'.format(eta=eta))
    
    h_fr_smoothed_data.Draw("colz text")
    canv.SaveAs(targetdir+'fakerate_smoothed_data_{date}.png'.format(date=date))
    canv.SaveAs(targetdir+'fakerate_smoothed_data_{date}.pdf'.format(date=date))
    
    outfile = ROOT.TFile('w-helicity-13TeV/wmass_mu/fakerateSmoothed_mu_{date}{pf}.root'.format(date=date,pf=('_'+postfix if postfix else '')),'RECREATE')
    h_fr_smoothed_data.Write()
    outfile.Close()
    

        #python mcEfficiencies.py -f -j 4 -l $TRIGLUMI --s2v -P $ELFRTREES dps-ww/elFR/mca_elFR.txt dps-ww/elFR/cuts_elFR.txt dps-ww/elFR/tightCut.txt dps-ww/elFR/xvar${pt}.txt --sp QCD --scale-process QCD $QCDSCALE --scale-process WandZ $WZSCALE -o ~/www/private/dps-ww/${DATE}-elFR${POSTFIX}/${eta}_${pt}/fr_el_${eta}_${pt} --groupBy cut --compare QCD,data,data_sub,total,WandZ --showRatio --ratioRange 0 3 --mcc ttH-multilepton/mcc-eleIdEmu2.txt -X pt${negpt} -X eta${negeta} -X lepMVAtight ;# --sP lpt${pt} # -E mtw1 


if __name__ == '__main__':
    parser = optparse.OptionParser(usage='usage: %prog [opts] ', version='%prog 1.0')
    parser.add_option('--pf'        , '--postfix'    , dest='postfix'      , type='string'       , default=''    , help='postfix for running each module')
    parser.add_option('-d'          , '--date'       , dest='date'         , type='string'       , default=''    , help='run with specified date instead of today')
    parser.add_option('-l'          , '--lumi'       , dest='lumi'         , type='float'        , default=0.    , help='change lumi by hand')
    parser.add_option('--simple'    ,                  dest='simple'       , action='store_true' , default=False , help='make simple plot')
    parser.add_option('--sFR'       ,                  dest='sFR'          , action='store_true' , default=False , help='make simple FR plots')
    parser.add_option('--fr'        , '--fakerates'  , dest='runFR'        , action='store_true' , default=False , help='run fakerates for muons')
    parser.add_option('--rec'        , '--recalculate'  , dest='recalculate'        , action='store_true' , default=False , help='recalculate fakerates')
    parser.add_option('--pr'        , '--promptrates', dest='runPR'        , action='store_true' , default=False , help='run promptrates for muons')
    parser.add_option('--fs'        , '--fakeshapes' , dest='fakeShapes'   , action='store_true' , default=False , help='run fake shapes')
    parser.add_option('--fc'        , '--fakeclosure', dest='fakeClosure'   , action='store_true' , default=False , help='run fake closure')
    parser.add_option('--fdm'       , '--fakesDataMC', dest='fakesDataMC'   , action='store_true' , default=False , help='run fakes data MC comparison')
    parser.add_option('--frp'       , '--fakerateplots', dest='fakeratePlots', type='string' , default='' , help='run fakerate plots and fitting')
    parser.add_option('--dy'        , '--dyComparison' , dest='dyComparison' , action='store_true' , default=False , help='make dy comparisons')
    parser.add_option('--results'   , '--makeResults'  , dest='results'      , action='store_true' , default=False , help='make results')
    (opts, args) = parser.parse_args()

    global date, postfix, lumi, date
    postfix = opts.postfix
    lumi = 36.0 if not opts.lumi else opts.lumi
    date = datetime.date.today().isoformat()
    if opts.date:
        date = opts.date

    if opts.simple:
        print 'making simple plots'
        simplePlot()
    if opts.sFR:
        print 'making simple FR plots'
        simpleFRPlot()
    if opts.runFR:
        print 'running the fakerates for muons'
        makeFakeRatesFast(opts.recalculate)
    if opts.runPR:
        print 'running the promptrates for muons'
        makePromptRates()
    if opts.fakeShapes:
        print 'running the fakeshapes for muons'
        fakeShapes()
    if opts.fakeClosure:
        print 'running the fakes closure for muons'
        fakeClosure()
    if opts.fakesDataMC:
        print 'running the fakes data-mc comparison'
        fakesDataMC()
    if opts.fakeratePlots:
        print 'running the fakerateplots and fitting'
        fakeratePlots(opts.fakeratePlots)
    if opts.dyComparison:
        print 'running the dy comparisons'
        dyComparison()
    if opts.results:
        print 'running results'
        makeResults()
