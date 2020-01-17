import os, sys
nCores=8
submit = '{command}' 
submit = '''sbatch -c %d -p cpupower  --wrap '{command}' '''%nCores

if   'cmsco01.cern.ch' in os.environ['HOSTNAME']: ORIGIN="/data/peruzzi";
elif 'cmsphys10' in os.environ['HOSTNAME']:       ORIGIN="/data1/g/gpetrucc"; 
elif 'gpetrucc-vm2.cern.ch' in os.environ['HOSTNAME']:       ORIGIN="/data/gpetrucc"; 
elif 'fanae' in os.environ['HOSTNAME']:       ORIGIN="/pool/ciencias/HeppyTrees/EdgeZ/TTH/"; 
elif 'gae' in os.environ['HOSTNAME']:       ORIGIN="/pool/ciencias/HeppyTrees/EdgeZ/TTH/"; 
else: ORIGIN="/afs/cern.ch/work/p/peruzzi"; 


if len(sys.argv) < 3: 
    print 'Sytaxis is %s [outputdir] [year]  [other]'%sys.argv[0]
    raise RuntimeError 
OUTNAME=sys.argv[1]
YEAR=sys.argv[2]
OTHER=sys.argv[3:] if len(sys.argv) > 3 else ''

if   YEAR in '2016': LUMI="35.9"
elif YEAR in '2017': LUMI="41.4"
elif YEAR in '2018': LUMI="59.7"
else:
    raise RuntimeError("Wrong year %s"%YEAR)
nCores=32
submit = 'sbatch -c %d -p short  --wrap "{command}"'%nCores
#submit="{command}"

BCORE=" --s2v --tree NanoAOD ttH-multilepton/mca-2lss-mcdata-ttbar-trigger.txt "
BCORE="{BCORE} -L ttH-multilepton/functionsTTH.cc".format(BCORE=BCORE)

BASE="python mcEfficiencies.py {BCORE} --ytitle 'Trigger efficiency' ttH-multilepton/trigger-eff/cuts_trigger_eff.txt  ".format(BCORE=BCORE)
B0="{BASE} -P {ORIGIN}/NanoTrees_TTH_091019_v6pre/{YEAR}/ -P {ORIGIN}/NanoTrees_TTH_090120_v6_triggerFix/{YEAR} ttH-multilepton/trigger-eff/trigger_cuts.txt ttH-multilepton/2lss_3l_plots.txt --groupBy cut --year {YEAR} --Fs {{P}}/1_recl --Fs {{P}}/1_extraTriggersMET --mcc ttH-multilepton/lepchoice-ttH-FO.txt --split-factor=-1 --WA prescaleFromSkim -f -j {nCores}  ".format(BASE=BASE,YEAR=YEAR,ORIGIN=ORIGIN,nCores=nCores)
B0="{B0} --legend=BR --showRatio --ratioRange 0.9 1.05   --yrange 0.8 1.2 ".format(B0=B0)
B0="{B0} -o {OUTNAME}/triggers_{YEAR}.root".format(B0=B0,OUTNAME=OUTNAME,YEAR=YEAR)
B0="{B0} --pgroup MC:=TT,DY,SingleTop,WW --xp WJets  --sP lep1_conePt --sP lep2_conePt --sP lep1_eta --sP lep2_eta --sP era --sP tot_weight --sP dilep".format(B0=B0)
if '_ee' in OUTNAME:
    B0 += " -E ^ee "
if '_mm' in OUTNAME:
    B0 += " -E ^mm "
if '_em' in OUTNAME:
    B0 += " -E ^em "

if '_closure' in OUTNAME:
    B0 += ''' --weightNumerator 'triggerSF_ttH(LepGood1_pdgId, LepGood1_conePt, LepGood2_pdgId, LepGood2_conePt, 2, year)' '''
    
if '_3l' in OUTNAME:
    B0 = B0.replace("mca-2lss-mcdata-ttbar-trigger.txt","mca-3l-trigger.txt")
    B0 = B0.replace("MC:=TT,DY,SingleTop,WW", "")
    B0 = B0 + " -p data -p WZ "
    B0 = B0 + " -E ^trilep "
    B0 = B0.replace("--sP dilep", "--sP trilep")
print submit.format( command=B0 )
