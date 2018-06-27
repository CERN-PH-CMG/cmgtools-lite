import optparse, subprocess, ROOT, datetime, math, array, copy, os
import numpy as np

doPUreweighting = True
doPUandSF = False

def submitFRrecursive(ODIR, name, cmd, dryRun=False):
    outdir=ODIR+"/jobs/"
    if not os.path.isdir(outdir): 
        os.system('mkdir -p '+outdir)
    os.system('cp ${{HOME}}/index.php {od}/../'.format(od=outdir))
    os.system('cp ${{HOME}}/index.php {od}/../../'.format(od=outdir))
    os.system('cp ${{HOME}}/resubFRs.py {od}/../../'.format(od=outdir))
    srcfile = outdir+name+".sh"
    logfile = outdir+name+".log"
    srcfile_op = open(srcfile,"w")
    srcfile_op.write("#! /bin/sh\n")
    srcfile_op.write("ulimit -c 0\n")
    srcfile_op.write("cd {cmssw};\neval $(scramv1 runtime -sh);\ncd {d};\n".format( 
            d = os.getcwd(), cmssw = os.environ['CMSSW_BASE']))
    srcfile_op.write(cmd+'\n')
    os.system("chmod a+x "+srcfile)
    bsubcmd = "bsub -q 1nd -o {logfile} {srcfile}\n".format(d=os.getcwd(), logfile=logfile, srcfile=srcfile)
    if dryRun: 
        print "[DRY-RUN]: ", bsubcmd
    else: os.system(bsubcmd)

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
            #if(scale > 1.0):
            #   scale = 1.0
            #   scaleerr = 0.0
    if  not reterr:
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
        if not type(friends)==list: friends = [friends]
        for f in friends:
            cmd += ' -F Friends {friends}/tree_Friend_{{cname}}.root'.format(friends=f)
    # cmd += ' --mcc ttH-multilepton/mcc-eleIdEmu2.txt '
    cmd += ' -W puw*LepGood_effSF[0]*LepGood_effSF[1]' 
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
    if doPUreweighting: cmd += ' -W new_puwts_HLT_Mu17_prescaled_2016(nTrueInt)'#new_puwts2016(nTrueInt)'#puWeight' # ' ## adding pu weight

    if doPUandSF and not '-W ' in extraopts: cmd += ' -W puw*LepGood_effSF[0]*LepGood_effSF[1]'

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
    if doPUandSF and not '-W ' in extraopts: cmd += ' -W puw*LepGood_effSF[0]*LepGood_effSF[1]' ##_get_muonSF_trgIsoID(LepGood_pdgId[0],LepGood_pt[0],LepGood_eta[0],0)' ## adding pu weight
    if doPUreweighting: cmd += ' -W new_puwts_HLT_Mu17_prescaled_2016(nTrueInt)'#puWeight' #new_puwts2016(nTrueInt) ' ## adding pu weight
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

def makeResults(onlyEE = False,onlyMM = True, splitsign =False, splitCharge = False): #sfdate, onlyMM = True, splitCharge = True):
#def runCards(trees, friends, targetdir, fmca, fcut, fsyst, plotbin, enabledcuts, disabledcuts, processes, scaleprocesses, extraopts = ''):
#python makeShapeCardsSusy.py --s2v -P /afs/cern.ch/work/e/efascion/DPStrees/TREES_110816_2muss/ --Fs /afs/cern.ch/work/e/efascion/public/friendsForDPS_110816/ -l 12.9 dps-ww/final_mca.txt dps-ww/cutfinal.txt finalMVA_DPS 10,0.,1.0  --od dps-ww/cards -p DPSWW,WZ,ZZ,WWW,WpWpJJ,Wjets  -W 0.8874 --asimov dps-ww/syst.txt
    
    #sfs = calculateScalefactors(False, sfdate)

    targetcarddir = 'cards_{date}{pf}_MuMu_Signalscaled'.format(date=date, pf=('-'+postfix if postfix else '') )
    trees     = '/eos/user/m/mdunser/dps-13TeV-combination/TREES_latest/'
    friends = [trees+'/friends_jet_pu_lepSF/', trees+'/friends_latest_bdt/']
    targetdir = '/eos/user/a/anmehta/www/{date}{pf}MuMu_tauveto/'.format(date=date, pf=('-'+postfix if postfix else '') ) 
    #fcut   = 'dpsww13TeV/dps2016/results/cuts_results_MVA_tight_WP.txt' #cuts_results.txt'#'#
    fplots = 'dpsww13TeV/dps2016/results/plots.txt'
    fsyst  = 'dpsww13TeV/dps2016/results/syst.txt'


    print '=========================================='
    print 'run results for MUMU'
    print '=========================================='
    print 'confirm the binning of 1D BDT histogram'
    print '=========================================='

    if splitCharge: 
        loop = [ ['minusminus'], ['plusplus']]
    elif splitsign:
        loop = [ ['SS'], ['OS']]
    else:
        loop = [ [] ]

    print 'did i split the charge? %i' %splitCharge



    processes      = ['DPSWW', 'WZ', 'ZZ', 'WG_wg', 'rares','fakes_data','data']#'DY',
    processesCards = ['data', 'DPSWW', 'WZ', 'ZZ', 'WG_wg', 'rares', 'fakes_data', 'WZamcatnlo', 'DPSWW_alt']

    binningBDT   = ' Binnumberset1D(BDT_DPS_fakes,BDT_DPS_WZ) 15,1.0,16.0'
    nbinspostifx = '_15bins'
    #fmca   = 'dpsww13TeV/dps2016/results/mumuelmu_mca_v1.txt'#elmu_mca_v1.txt'#
    #fmca_elmu='dpsww13TeV/dps2016/results/elmu_mca_v1.txt'
    for bdt in ['wz']:
        for ich,ch in enumerate(loop):
            #if not ich: continue
            if onlyMM:
                fmca   = 'dpsww13TeV/dps2016/results/mumuelmu_mca_v1.txt'
                fcut   = 'dpsww13TeV/dps2016/results/cuts_results_MVA_tight_WP1.txt'
                enable    = ['trigmumu','mumu'] + ch
                state='mumu'
            elif onlyEE:
                fmca='dpsww13TeV/dps2016/results/elel_mca.txt'
                fcut   = 'dpsww13TeV/dps2016/results/cuts_results_DY.txt'
                enable= ['trigelel','elel'] + ch
                state='elel'
            else:
                enable    = ['trigelmu','elmu'] + ch
                fmca='dpsww13TeV/dps2016/results/elmu_mca_v1.txt'
                fcut   = 'dpsww13TeV/dps2016/results/cuts_results_MVA_tight_WP.txt'
                state='elmu'
            disable   = []
            fittodata = []#'DPSWW', 'WZ', 'ZZ', 'WG_wg', 'rares', 'fakes_data']
            scalethem = {}#'DPSWW':'{sf:.3f}'.format(sf=0.50)}#'WZ': '{sf:.3f}'.format(sf=1.04),
                         #'ZZ': '{sf:.3f}'.format(sf=1.21)}
                         
            mumusf = 0.95
            extraopts = '--showIndivSigs'.format(sf=mumusf) # --plotmode=norm -W {sf:.3f}
            #drawvars=['mcMatchId1','mcMatchId2']#N','pt_mcMatchId2','pt_mcMatchId1',
            drawvars=['pt1']#mll','met','mtl1met','mtl2met','mtll']
            if splitCharge or splitsign:
                makeplots  = ['{}_{}{}'.format(a, state,ch[0])  for a in drawvars]
            else:
                makeplots  = ['{}_{}'.format(a, state)  for a in drawvars]

            #makeplots = ['lepMVA1_mumu','lepMVA2_mumu']
            #makeplots = ['BDTforCombine_mumu{ch}{nbins}'.format(ch=(ch[0] if ch else ''),nbins=nbinspostifx)] 
            #makeplots = ['BDTforCombine_elmu{ch}{nbins}'.format(ch=(ch[0] if ch else ''),nbins=nbinspostifx),'BDTfakes_BDTWZ_elmu{ch}_20bins'.format(ch=(ch[0] if ch else '')),'BDT_wz_elmu{ch}_20bins'.format(ch=(ch[0] if ch else '')),'BDT_fakes_elmu{ch}_20bins'.format(ch=(ch[0] if ch else '')),
            #            makeplots=['pt_eta_elel_OS','pt_eta_elel_OS','mll_elel']

            #makeplots=['pt_mu_elmu','nVert_elmu']#'pt_el_elmu',]#'pt2_mumu','eta1_mumu','eta2_mumu','phi1_mumu','phi2_mumu']#'lepMVA1_mumu','lepMVA2_mumu']
            #makeplots=['pt1_mumu']
            #makeplots=['met_elmu','pt1_elmu','nVert_elmu','mt1_elmu','mt2_elmu','dphiLep_elmu','pt2_elmu','eta_sum_elmu','dphilll2_elmu']
            #makeplots=['pt1_el_elmu','pt1_mu_elmu','pt2_el_elmu','pt2_mu_elmu']#etaprod_elmu','mt1_elmu','met_elmu','mt2ll_elmu','mtll_elmu','dphil2met_elmu','mll_elmu','BDT_wz_elmu_20bins','BDT_fakes_elmu_20bins']
            #makeplots=['pt1_mumu{ch}'.format(ch=(ch[0] if ch else '')),'met_mumu{ch}'.format(ch=(ch[0] if ch else ''))]#'nVert_mumu{ch}'.format(ch=(ch[0] if ch else '')),'mt1_mumu{ch}'.format(ch=(ch[0] if ch else '')),'mt2_mumu{ch}'.format(ch=(ch[0] if ch else '')),'dphiLep_mumu{ch}'.format(ch=(ch[0] if ch else '')),'pt2_mumu{ch}'.format(ch=(ch[0] if ch else '')),'eta_sum_mumu{ch}'.format(ch=(ch[0] if ch else '')),'dphilll2_mumu{ch}'.format(ch=(ch[0] if ch else '')),'etaprod_mumu{ch}'.format(ch=(ch[0] if ch else '')),'mt1_mumu{ch}'.format(ch=(ch[0] if ch else '')),'mt2ll_mumu{ch}'.format(ch=(ch[0] if ch else '')),'mtll_mumu{ch}'.format(ch=(ch[0] if ch else '')),'dphil2met_mumu{ch}'.format(ch=(ch[0] if ch else '')),'mll_mumu{ch}'.format(ch=(ch[0] if ch else ''))]#,'BDT_wz_mumu{ch}_20bins'.format(ch=(ch[0] if ch else '')),'BDT_fakes_mumu_{ch}20bins'.format(ch=(ch[0] if ch else ''))]

            runplots(trees, friends, targetdir, fmca, fcut, fplots, enable, disable, processes, scalethem, fittodata, makeplots, True, extraopts)
            ## ==================================
            ## running datacards
            ## ==================================
            #extraoptscards = ' -W {sf:.3f} -o mumu{ch} -b mumu{ch} '.format(sf=mumusf, ch=(ch[0] if ch else ''))
            extraoptscards = ' -o elmu{ch} -b elmu{ch} '.format(ch=(ch[0] if ch else ''))
            #runCards(trees, friends, targetcarddir, fmca, fcut, fsyst , binningBDT, enable, disable, processesCards, scalethem, extraoptscards)
            

def simplePlot():
    print '=========================================='
    print 'running simple plots'
    print '=========================================='
    trees     = ['/eos/user/m/mdunser/w-helicity-13TeV/trees/wz3lnu/']
    friends   = '/eos/user/m/mdunser/w-helicity-13TeV/trees/trees_all_skims/friends/'
    targetdir = '/eos/user/v/vmariani/www/bdt_weight_applied_pythia/' 

    fmca      = 'dpsww13TeV/dps2016/simple/mca_simple.txt' #'dpsww13TeV/dps2016/mca-wmu-weight.txt' 
    fcut      = 'dpsww13TeV/dps2016/simple/cuts_simple.txt'
    fplots    = 'dpsww13TeV/dps2016/simple/plots.txt'

    enable    = []
    disable   = ['trigger2mu']#'muonTightIso'
    processes = ['WWherw', 'WZ', 'WWCUETPM8']# 'WZ', 'WWCUETPM8', 'WWCP5'
    fittodata = []
    scalethem = {}
    extraopts = '--plotmode=norm' #--ratioNums WWherw,WWCP5,WWCUETPM8 --ratioDen WWherw --maxRatioRange 0.8 1.2 --fixRatioRange' #'--plotmode=norm' #--ratioNums WWherw,WZ --ratioDen WWherw --maxRatioRange 0.8 1.2 --fixRatioRange
    makeplots = ['BDT_WZ', 'BDT_fakes', 'BDT_WZ_times_fakes', 'BDT_WZ_fakes_2D'] 
    #makeplots = ['ptl1', 'ptl2', 'etal1', 'etal2', 'phil1', 'phil2', 'pfmet', 'etaprod', 'etasum', 'ml1l2', 'mtl1pf', 'mtl1l2', 'mt2davis', 'dphil1l2', 'dphil2pf', 'dphilll2', 'nVert']#['BDT_WZ', 'BDT_fakes', 'BDT_WZ_times_fakes', 'BDT_WZ_fakes_2D']#['ptl1', 'ptl2', 'etal1', 'etal2', 'phil1', 'phil2', 'pfmet', 'etaprod', 'etasum', 'ml1l2', 'mtl1pf', 'mtl1l2', 'mt2davis', 'dphil1l2', 'dphil2pf', 'dphilll2', 'nVert']
    showratio = True
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
    ## in order to calculate the fakerates (and submit the jobs to the batch) one has to run (i think):

    ##  python runDPS.py --fr --recalculate --submitFR

    ## this here is the usual stuff, but the paths are still wrong. we need to find the 1l skims that have mvaTTH inside

    trees     = '/eos/user/m/mdunser/dps-13TeV-combination/TREES_fr_2016/'
    #friends  ='/afs/cern.ch/work/a/anmehta/work/Test/Test2/CMSSW_8_0_25/src/CMGTools/DPS13TeV/python/postprocessing/JetCleaning_1lskim_DblEl_friendsJune07_All/'
    friends   = trees+'/friends/'
    targetdir = '/eos/user/a/anmehta/www/{date}{pf}Muon_fakerates_redefinedLoose/'.format(date=date, pf=('-'+postfix if postfix else '') )
    ## accordingly we have to change the mca file here. we also need to adapt the cuts file here.
    ## also the tight cut should now be 0.9 if we are moving to what the tHq people use
    fmca   = 'dpsww13TeV/dps2016/New_FRfast/mca_fr.txt' 
    fcut   = 'dpsww13TeV/dps2016/New_FRfast/cuts_fr.txt'
    fplots = 'dpsww13TeV/dps2016/New_FRfast/plots.txt'       
    ftight = 'dpsww13TeV/dps2016/New_FRfast/tightCut.txt'    

    ## we need datasets in our mca that are called QCD, WandZ, and the data. WandZ should be a combo of W+jets and Z+jets
    processes = ['QCD', 'WandZ','data']
    compprocs = ['QCD', 'WandZ','data','data_sub']
    fittodata = ['QCD', 'WandZ']

    ## these are the plots that are made. a scale factor is derived from the first plot in this list. in this case MT
    makeplots = ['mtl1pf','pfmet','rho','nVert','l1mvaTTH','ptl1','etal1','pfmet']#'nJetAll','nJet40','nJet30','nJet25','lep_jet_dphi'
    
    ## copy the pT binning here from the xvars.txt file which is in dpsww13TeV/dps2016/FRfast/xvars.txt
    binning = [20,23,26,29,32,35,38,41,45,50,55,65,100]
    ## we need/want a bit more granular binning in eta for the fakerates. those should then be pretty accurate
    #    binningeta = [-2.5,-2.0,-1.5,-1.0,-0.5,0.,0.5,1.0,1.5,2.0,2.5]
    binningeta = [0.,0.5,1.0,1.5,2.0,2.5]
    ## now we construct the 2D histograms for the FR (and prompt rate) for data and MC
    h_name  = 'fakerate_mu'; h_title = 'fakerates muons'
    ##we are computing FR from data and QCD MC
    h_fakerate_data = ROOT.TH2F(h_name+'_data',h_title+' - data', len(binning)-1, array.array('f',binning), len(binningeta)-1, array.array('f',binningeta))
    h_fakerate_mc   = ROOT.TH2F(h_name+'_qcd' ,h_title+' - qcd' , len(binning)-1, array.array('f',binning), len(binningeta)-1, array.array('f',binningeta))
    h_fakerate_data .Sumw2()
    h_fakerate_mc   .Sumw2()
    h_fakerate_data .GetZaxis().SetRangeUser(0.01,0.45)
    h_fakerate_mc   .GetZaxis().SetRangeUser(0.01,0.45)
    h_fakerate_data .GetXaxis().SetTitle('p_{T} #mu'); h_fakerate_data .GetYaxis().SetTitle('#eta #mu')
    h_fakerate_mc   .GetXaxis().SetTitle('p_{T} #mu'); h_fakerate_mc   .GetYaxis().SetTitle('#eta #mu')

    ## here's the prompt rate.
    h_name  = 'promptrate_mu'; h_title = 'promptrates muons'
    h_promptrate_data = ROOT.TH2F(h_name+'_data',h_title+' - data', len(binning)-1, array.array('f',binning), len(binningeta)-1, array.array('f',binningeta))
    h_promptrate_mc   = ROOT.TH2F(h_name+'_qcd' ,h_title+' - qcd' , len(binning)-1, array.array('f',binning), len(binningeta)-1, array.array('f',binningeta))
    h_promptrate_data .Sumw2()
    h_promptrate_mc   .Sumw2()
    h_promptrate_data .GetZaxis().SetRangeUser(0.5,1.00)
    h_promptrate_mc   .GetZaxis().SetRangeUser(0.5,1.00)
    h_promptrate_data .GetXaxis().SetTitle('p_{T} #mu'); h_promptrate_data .GetYaxis().SetTitle('#eta #mu')
    h_promptrate_mc   .GetXaxis().SetTitle('p_{T} #mu'); h_promptrate_mc   .GetYaxis().SetTitle('#eta #mu')

    ## add MT cut to the eff plot!
    fakerates = {}; promptrates = {}
    scales = {}
    printAggressive('STARTING FAKE RATES...!')

    ## now we loop on all the bins in eta of the lepton
    for j,eta in enumerate(binningeta[:-1]):

        ## we make a string that identifies each of the bins uniquely and make subdirectories for each
        etastring = 'To'.join(str(i).replace('-','m').replace('.','p') for i in [eta, binningeta[j+1]] )
        tmp_td = targetdir+'/'+etastring

        ## this is some weird recursive magic to submit this to the batch. one needs a valid voms proxy
        ## and such to run this on batch. it submits one job per bin in eta. each would take about
        ## an hour i guess? depends a lot on priorities etc. though
        if opts.submitFR:
            abspath = os.path.abspath('.')
            tmp_cmd = 'python '+abspath+'/runDPS.py --fr --recalculate --doBin {j}'.format(j=j)
            submitFRrecursive(tmp_td, 'frjob_{j}'.format(j=j), tmp_cmd)
            continue
        if opts.doBin > -1:
            if not j == opts.doBin: continue
        ## end weird magic

        ## now those are the usual options for runplots. we run first the plots of MT (and whatever else is in the list above)
        ## from the MT plot on LOOSE leptons, we get a scale factor for the WandZ which we apply to the subtraction afterwards
        scalethem = {}
        enable    = []
        ## the cut that is in the cut-file which we want to disable should then be mvaTTH > 0.9
        disable   = ['muonTightMVA']
        newplots = [('mu_'+plot) for plot in makeplots]
        ## the next lines add options: the first one adds the eta cuts for the eta bin we are in
        extraopts = ' -A alwaystrue ETA{eta} abs(LepGood1_eta)>={e1}&&abs(LepGood1_eta)<{e2} '.format(eta=etastring, e1=eta, e2=binningeta[j+1]) ## no whitespaces in the cutstring here!!
        
        ## the next line would add pileup and lepton SFs. but we don't have them yet...
        ## include at least the lepton SFs later (not super important though)
        extraopts+= ''# -W 1. '.format(wgt=pileupandSFs)

        ## now if recalculate is set to true it will run the plots for the WandZ scale factor
        if recalculate: runplots(trees, friends, tmp_td, fmca, fcut, fplots, enable, disable, processes, scalethem, fittodata, newplots, True, extraopts)
        printAggressive('DONE MAKING THE PLOTS TO DERIVE THE EWK SCALE FACTORS!')

        scales['qcd_{eta}'  .format(eta=etastring)] = readScaleFactor(tmp_td+'/mu_{plot}.txt'.format(plot=makeplots[0]), 'QCD')
        scales['wandz_{eta}'.format(eta=etastring)] = readScaleFactor(tmp_td+'/mu_{plot}.txt'.format(plot=makeplots[0]), 'WandZ')
        #scales['top_{eta}'.format(eta=etastring)] = readScaleFactor(tmp_td+'/mu_{plot}.txt'.format(plot=makeplots[0]), 'Top')
        #scales['dy_{eta}'.format(eta=etastring)] = readScaleFactor(tmp_td+'/mu_{plot}.txt'.format(plot=makeplots[0]), 'DY')

        ## IMPORTANT
        ## now we enable the MT < 40 GeV cut, and disable again the tight mvaTTH cut
        enable  = ['mtl1pf40max']
        disable = ['muonTightMVA']
        ##why do we scale QCD. we need to subtract contributions from EWK processes only ??
        scalethem = {'QCD'  : scales['qcd_{eta}'  .format(eta=etastring)],
                     'WandZ': scales['wandz_{eta}'.format(eta=etastring)]
                     #            'Top': scales['top_{eta}'.format(eta=etastring)],
                     #'DY': scales['dy_{eta}'.format(eta=etastring)],
                     }

        ## this file has the pT binning that we want for the FR
        fxvar  = 'dpsww13TeV/dps2016/New_FRfast/xvars.txt'

        ## this now remakes the plots with the MT cut included after scaling the QCD and the WandZ
        printAggressive('SCALING THE PROCESSES BY FACTORS')
        print scalethem
        if recalculate: runplots(trees, friends, tmp_td+'/mTCutIncluded/', fmca, fcut, fplots, enable, disable, processes, scalethem, [], newplots, True, extraopts) ## don't fit to data anymore  #here1
        extraopts += ' --ratioRange 0 2 --sp QCD '##we calculate ratios (in the ratio plot) w.r.t QCD sample

        ## runefficiencies now produces the actual FR numbers (and PR which is taken from the WandZ)
        ## the numbers are read from the output and filled into the proper dictionary and histograms
        if recalculate: runefficiencies(trees, friends, tmp_td+'/fr_mu_{eta}'.format(eta=etastring), fmca, fcut, ftight, fxvar, enable, disable, scalethem,compprocs, True, extraopts) #here2
        fakerates['fr_mu_qcd_{eta}'.format(eta=etastring)] = readFakerate(tmp_td+'/fr_mu_{eta}.txt'.format(eta=etastring),'QCD')
        fakerates['fr_mu_dat_{eta}'.format(eta=etastring)] = readFakerate(tmp_td+'/fr_mu_{eta}.txt'.format(eta=etastring),'Data - EWK') 
        
        promptrates['fr_mu_qcd_{eta}'.format(eta=etastring)] = readFakerate(tmp_td+'/fr_mu_{eta}.txt'.format(eta=etastring),'WandZ')
        promptrates['fr_mu_dat_{eta}'.format(eta=etastring)] = readFakerate(tmp_td+'/fr_mu_{eta}.txt'.format(eta=etastring),'WandZ')

        print len(binning), binning
        print len(fakerates['fr_mu_dat_{eta}'.format(eta=etastring)][0]), fakerates['fr_mu_dat_{eta}'.format(eta=etastring)][0]
        for i in range(len(fakerates['fr_mu_dat_{eta}'.format(eta=etastring)][0])):
            h_fakerate_data.SetBinContent(i+1,j+1, fakerates['fr_mu_dat_{eta}'.format(eta=etastring)][0][i])
            h_fakerate_data.SetBinError  (i+1,j+1, fakerates['fr_mu_dat_{eta}'.format(eta=etastring)][1][i])
            h_fakerate_mc  .SetBinContent(i+1,j+1, fakerates['fr_mu_qcd_{eta}'.format(eta=etastring)][0][i])
            h_fakerate_mc  .SetBinError  (i+1,j+1, fakerates['fr_mu_qcd_{eta}'.format(eta=etastring)][1][i])
            h_promptrate_data.SetBinContent(i+1,j+1, promptrates['fr_mu_dat_{eta}'.format(eta=etastring)][0][i])
            h_promptrate_data.SetBinError  (i+1,j+1, promptrates['fr_mu_dat_{eta}'.format(eta=etastring)][1][i])
            h_promptrate_mc  .SetBinContent(i+1,j+1, promptrates['fr_mu_qcd_{eta}'.format(eta=etastring)][0][i])
            h_promptrate_mc  .SetBinError  (i+1,j+1, promptrates['fr_mu_qcd_{eta}'.format(eta=etastring)][1][i])


    ## ok from here on all the work is already done and the rest is only filling stuff into the histograms and 
    ## varying stuff etc.

    ## it also saves all the histograms then as root, pdf, and png files


    if not opts.submitFR and opts.doBin < 0:
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
        outfile = ROOT.TFile(targetdir+'/fakerateMap_mu_{date}{pf}.root'.format(date=date,pf=('_'+postfix if postfix else '')),'RECREATE')
        h_fakerate_data.Write()
        h_fakerate_mc  .Write()
        h_fakerate_data_frUp.Write()
        h_fakerate_mc_frUp  .Write()
        h_fakerate_data_frDn.Write()
        h_fakerate_mc_frDn  .Write()
        outfile.Close()

        outfile = ROOT.TFile(targetdir+'/promptrateMap_mu_{date}{pf}.root'.format(date=date,pf=('_'+postfix if postfix else '')),'RECREATE')
        h_promptrate_data.Write()
        h_promptrate_mc  .Write()
        #        h_promptrate_data_frUp.Write()
        #       h_promptrate_mc_frUp  .Write()
        #      h_promptrate_data_frDn.Write()
        #     h_promptrate_mc_frDn  .Write()
        outfile.Close()
        
        print scales
        print fakerates
        print promptrates

        h_fr_smoothed_data = ROOT.TH2F('fakerates_smoothed_data'  ,' fakerates - smoothed data'  , len(binningeta)-1, array.array('f',binningeta), 2, array.array('f',[0., 1., 2.]))
        h_pr_smoothed_data = ROOT.TH2F('promptrates_smoothed_data',' promptrates - smoothed data', len(binningeta)-1, array.array('f',binningeta), 3, array.array('f',[0., 1., 2.,3.]))
        #h_fr_smoothed_mc   = ROOT.TH2F(h_name+'_qcd' ,h_title+' - qcd' , len(binning)-1, array.array('f',binning), len(binningeta)-1, array.array('f',binningeta))


        ## ok and from here on out, what it does is to look at the output files, get the graph of the fakerate
        ## as a function of pT, then fits this graph with a pol0 and a pol1 and takes the one with the smaller
        ## chi2/ndf and puts it in a 2D histogram again which has the offset and the slope (instead of the value
        ## of the actual FR) stored.

        for j,eta in enumerate(binningeta[:-1]):


            print 'GETTING AND FITTING THE FR FROM', etastring

            etastring = 'To'.join(str(i).replace('-','m').replace('.','p') for i in [eta, binningeta[j+1]] )
            tmp_td = targetdir+'/'+etastring

            graph_file= ROOT.TFile(tmp_td+'/fr_mu_{eta}'.format(eta=etastring), 'read')

            mg = ROOT.TMultiGraph(); pols = []
            legfr= ROOT.TLegend(0.62,0.55,0.78, 0.82)
            legfr.SetHeader('#eta (#mu) -- {eta}'.format(eta=etastring))
            legfr.SetFillColor(0)
            legfr.SetShadowColor(0)
            legfr.SetLineColor(0)
            legfr.SetTextFont(42)
            legfr.SetTextSize(0.035)


            for rate in ['pr', 'fr']:

                pol0 = ROOT.TF1("{r}_pol0_{eta}".format(r=rate,eta=etastring), "[0]        ", 20., 45.)
                pol1 = ROOT.TF1("{r}_pol1_{eta}".format(r=rate,eta=etastring), "[1]*x + [0]", 20., 45.)
                errf= ROOT.TF1("{r}_errf_{eta}".format(r=rate,eta=etastring), "[0]*TMath::Erf((x-[1])/[2])", 20., 100.)
                
                if rate == 'fr':
                    graph = graph_file.Get('muonTightId_pt_fine_binned_data_sub')
                    pol0.SetLineColor(ROOT.kGreen); pol0.SetLineWidth(2)
                    pol1.SetLineColor(ROOT.kRed-3); pol1.SetLineWidth(2)
                    #legfr.AddEntry(graph,"Fake Ratio","P")
                    #legfr.AddEntry(pol1,"Pol1","l")
                    #graph.SetTitle(";p_{T}#mu;Ratios");
                    #graph.GetXaxis().SetTitle("p_{T}#mu");
                    #pol0.SetParLimits(1, 0.1, 0.4)
                    #pol1.SetParLimits(1, -0.1  , 0.1)
                    #pol1.SetParLimits(0,  0.1  , 1.1)

                else:
                    graph = graph_file.Get('muonTightId_pt_fine_binned_WandZ')
                    graph.SetLineColor(ROOT.kRed); 
                    graph.SetMarkerColor(ROOT.kRed);
                    graphPR = graph.Clone()
                    #pol0.SetLineColor(ROOT.kBlue)   ; pol0.SetLineWidth(2)
                    #pol1.SetLineColor(ROOT.kAzure-3); pol1.SetLineWidth(2)
                    errf.SetLineColor(ROOT.kCyan); errf.SetLineWidth(2)
                    errf.SetParameter(0, 2.1);
                    errf.SetParameter(1, 2.1);
                    errf.SetParameter(2, 1.52);
                    ERRF=errf.Clone()
                    #pol0.SetParLimits(1, 0.1, 1.1)
                    #pol1.SetParLimits(1, -0.1  , 0.1)
                    #pol1.SetParLimits(0,  0.1  , 1.1)
                    

                mg.Add(copy.deepcopy(graph))

                if rate == 'fr':
                    graph.Fit("{r}_pol0_{eta}".format(r=rate,eta=etastring), "M", "", 20., 45.)
                    graph.Fit("{r}_pol1_{eta}".format(r=rate,eta=etastring), "M", "", 20., 45.)
                    
                    pol0_chi2 = pol0.GetChisquare(); pol0_ndf = pol0.GetNDF()
                    pol1_chi2 = pol1.GetChisquare(); pol1_ndf = pol1.GetNDF()
                    rchi2_0 = pol0_chi2/pol0_ndf
                    rchi2_1 = pol1_chi2/pol1_ndf
                    bestfunc = pol0 if rchi2_0 < rchi2_1 else pol1
                    worstfun = pol0 if rchi2_0 > rchi2_1 else pol1
                    print '{r} and {eta}: chi2 of pol0 = {chi0}/{ndf0} = {red0}'.format(r=rate,eta=etastring,chi0=pol0_chi2,ndf0=pol0_ndf, red0=rchi2_0)
                    print '{r} and {eta}: chi2 of pol1 = {chi1}/{ndf1} = {red1}'.format(r=rate,eta=etastring,chi1=pol1_chi2,ndf1=pol1_ndf, red1=rchi2_1)

                if rate == 'pr':
                    graph.Fit("{r}_errf_{eta}".format(r=rate,eta=etastring), "M", "", 20., 100.)
                    #graph.Fit("{r}_pol1_{eta}".format(r=rate,eta=etastring), "M", "", 20., 100.)
                    #pol1_chi2 = pol1.GetChisquare(); pol1_ndf = pol1.GetNDF()
                    errf_chi2 = errf.GetChisquare(); errf_ndf = errf.GetNDF()
                    #rchi2_1 = pol1_chi2/pol1_ndf
                    rchi2_0 = errf_chi2/errf_ndf
                    bestfunc = errf #if rchi2_0 < rchi2_1 else pol1
                    worstfun = '' #if rchi2_0 > rchi2_1 else pol1


                    print '{r} and {eta}: chi2 of errf = {chi0}/{ndf0} = {red0}'.format(r=rate,eta=etastring,chi0=errf_chi2,ndf0=errf_ndf, red0=rchi2_0)
                    #print '{r} and {eta}: chi2 of pol1 = {chi1}/{ndf1} = {red1}'.format(r=rate,eta=etastring,chi1=pol1_chi2,ndf1=pol1_ndf, red1=rchi2_1)

                print 'the better function is {func}'.format(func=bestfunc.GetName())

                #print '{eta}: compared to {func}         .   value={val:.3f}'.format(eta=eta, func = worstfun.GetName(), val=worstfun.GetChisquare()/worstfun.GetNDF())
                
                etabin = j+1 #if eta == 'barrel' else 2
                
                if rate == 'fr':
                    h_fr_smoothed_data.SetBinContent(etabin, 1, bestfunc.GetParameter(0))
                    h_fr_smoothed_data.SetBinError  (etabin, 1, bestfunc.GetParError (0))

                    h_fr_smoothed_data.SetBinContent(etabin, 2, bestfunc.GetParameter(1) if bestfunc.GetNpar() > 1 else 0.)
                    h_fr_smoothed_data.SetBinError  (etabin, 2, bestfunc.GetParError (1) if bestfunc.GetNpar() > 1 else 0.)
                    #pols.append(copy.deepcopy(pol0))
                    pols.append(copy.deepcopy(pol1))
                else:
                    h_pr_smoothed_data.SetBinContent(etabin, 1, bestfunc.GetParameter(0))
                    h_pr_smoothed_data.SetBinError  (etabin, 1, bestfunc.GetParError (0))

                    h_pr_smoothed_data.SetBinContent(etabin, 2, bestfunc.GetParameter(1) if bestfunc.GetNpar() > 1 else 0.)
                    h_pr_smoothed_data.SetBinError  (etabin, 2, bestfunc.GetParError (1) if bestfunc.GetNpar() > 1 else 0.)

                    h_pr_smoothed_data.SetBinContent(etabin, 3, bestfunc.GetParameter(2) if bestfunc.GetNpar() > 2 else 0.)
                    h_pr_smoothed_data.SetBinError  (etabin, 3, bestfunc.GetParError (2) if bestfunc.GetNpar() > 2 else 0.)

                    pols.append(copy.deepcopy(errf)) ##here
                    #pols.append(copy.deepcopy(pol1))

                mg.Add(copy.deepcopy(graph))

            #graph.Draw('ape')
            mg.Draw('ape')
            mg.GetYaxis().SetRangeUser(0., 1.0)
            mg.GetXaxis().SetTitle("p_{T}#mu")
            mg.GetYaxis().SetTitle("Ratios")
            legfr.AddEntry(graph,"Fake Ratio","P")
            legfr.AddEntry(pol1,"Pol1","l")
            legfr.AddEntry(graphPR,"Prompt Ratio","P")
            legfr.AddEntry(ERRF,"Errf","l")
            legfr.Draw("same")
            #            canv.BuildLegend();
            for p in pols:
                p.Draw('same')
            ##pol1.Draw('same')
            canv.SaveAs(targetdir+'fakeAndPromptRate_fit_data_{eta}.png'.format(eta=etastring))
            canv.SaveAs(targetdir+'fakeAndPromptRate_fit_data_{eta}.pdf'.format(eta=etastring))
        
        h_fr_smoothed_data.Draw("colz text45 e")
        h_fr_smoothed_data.GetZaxis().SetRangeUser(-0.05, 0.45)
        h_fr_smoothed_data.GetXaxis().SetTitle('#eta_{#mu}')
        h_fr_smoothed_data.GetXaxis().SetTitleSize(0.045)
        h_fr_smoothed_data.GetXaxis().SetLabelSize(0.05)
        h_fr_smoothed_data.GetYaxis().SetLabelSize(0.08)
        h_fr_smoothed_data.GetYaxis().SetBinLabel(1, 'offset')
        h_fr_smoothed_data.GetYaxis().SetBinLabel(2, 'slope')
        canv.SaveAs(targetdir+'fakerate_smoothed_data_{date}.png'.format(date=date))
        canv.SaveAs(targetdir+'fakerate_smoothed_data_{date}.pdf'.format(date=date))

        h_pr_smoothed_data.Draw("colz text45 e")
        #h_pr_smoothed_data.GetZaxis().SetRangeUser(0.00, 1.0)
        h_pr_smoothed_data.GetXaxis().SetTitle('#eta_{#mu}')
        h_pr_smoothed_data.GetXaxis().SetTitleSize(0.045)
        h_pr_smoothed_data.GetXaxis().SetLabelSize(0.035)
        h_pr_smoothed_data.GetYaxis().SetLabelSize(0.035)
        h_pr_smoothed_data.GetYaxis().SetBinLabel(1, 'Plateau')
        h_pr_smoothed_data.GetYaxis().SetBinLabel(2, 'Edge')
        h_pr_smoothed_data.GetYaxis().SetBinLabel(3, 'Resolution')
        canv.SaveAs(targetdir+'promptrate_smoothed_data_{date}.png'.format(date=date))
        canv.SaveAs(targetdir+'promptrate_smoothed_data_{date}.pdf'.format(date=date))
        
        outfile = ROOT.TFile(targetdir+'/fakerate_promptrate_mu_smoothed_data{pf}.root'.format(date=date,pf=('_'+postfix if postfix else '')),'RECREATE')

        h_fr_smoothed_data.Write()
        h_pr_smoothed_data.Write()
        outfile.Close()
    

        #python mcEfficiencies.py -f -j 4 -l $TRIGLUMI --s2v -P $ELFRTREES dps-ww/elFR/mca_elFR.txt dps-ww/elFR/cuts_elFR.txt dps-ww/elFR/tightCut.txt dps-ww/elFR/xvar${pt}.txt --sp QCD --scale-process QCD $QCDSCALE --scale-process WandZ $WZSCALE -o ~/www/private/dps-ww/${DATE}-elFR${POSTFIX}/${eta}_${pt}/fr_el_${eta}_${pt} --groupBy cut --compare QCD,data,data_sub,total,WandZ --showRatio --ratioRange 0 3 --mcc ttH-multilepton/mcc-eleIdEmu2.txt -X pt${negpt} -X eta${negeta} -X lepMVAtight ;# --sP lpt${pt} # -E mtw1 


if __name__ == '__main__':
    parser = optparse.OptionParser(usage='usage: %prog [opts] ', version='%prog 1.0')
    parser.add_option('--pf'        , '--postfix'    , dest='postfix'      , type='string'       , default=''    , help='postfix for running each module')
    parser.add_option('-d'          , '--date'       , dest='date'         , type='string'       , default=''    , help='run with specified date instead of today')
    parser.add_option('-l'          , '--lumi'       , dest='lumi'         , type='float'        , default=0.    , help='change lumi by hand')
    parser.add_option('--simple'    ,                  dest='simple'       , action='store_true' , default=False , help='make simple plot')
    parser.add_option('--sFR'       ,                  dest='sFR'          , action='store_true' , default=False , help='make simple FR plots')
    ## begin fake rate options
    parser.add_option('--fr'        , '--fakerates'  , dest='runFR'        , action='store_true' , default=False , help='run fakerates for muons')
    parser.add_option('--rec'       , '--recalculate', dest='recalculate'  , action='store_true' , default=False , help='recalculate fakerates')
    parser.add_option('--submitFR'  , '--submitFR'   , dest='submitFR'     , action='store_true' , default=False , help='submit the fakerates to the batch')
    parser.add_option('--doBin'     ,                  dest='doBin'        , type='int'          , default=-999  , help='submit exactly this bin of the FR calculation to the batch')
    ## end fake rate options
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
    lumi = 0.29 if not opts.lumi else opts.lumi##here 16.614
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
