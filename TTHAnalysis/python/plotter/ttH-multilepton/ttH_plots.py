#!/usr/bin/env python
import sys
import re

ODIR=sys.argv[1]

lumi = 2.16

def base(selection):

    CORE="-P /data/p/peruzzi/skim_2lss_3l_TREES_74X_140116_MiniIso_tauClean_Mor16lepMVA -F sf/t {P}/2_recleaner_v4_vetoCSVM/evVarFriend_{cname}.root -F sf/t {P}/4_kinMVA_trainMarcoJan27_v1_fix_reliso_conept/evVarFriend_{cname}.root"

    CORE+=" -l 2.26 --neg --s2v --tree treeProducerSusyMultilepton --mcc ttH-multilepton/lepchoice-ttH-FO.txt --mcc ttH-multilepton/ttH_2lss3l_triggerdefs.txt"
    CORE+=" -f -j 8 --lspam '#bf{CMS} #it{Preliminary}' --legendWidth 0.20 --legendFontSize 0.035 --showRatio --maxRatioRange 0 3  --showMCError --rebin 2"

    CORE+=" -W 'puw(nTrueInt)' "

    if selection=='2lss':
        GO="%s ttH-multilepton/mca-2lss-mc.txt ttH-multilepton/2lss_tight.txt ttH-multilepton/2lss_3l_plots.txt --xP 'lep3_.*' --xP '3lep_.*' --xP 'kinMVA_3l_.*' --xP 'kinMVA_input.*' "%CORE
    elif selection=='3l':
        GO="%s ttH-multilepton/mca-3l-mc.txt ttH-multilepton/3l_tight.txt ttH-multilepton/2lss_3l_plots.txt --xP '2lep_.*' --xP 'kinMVA_2lss_.*' --xP 'kinMVA_input.*' "%CORE
    else:
        raise RuntimeError, 'Unknown selection'

    return GO

def procs(GO,mylist):
    return GO+' '+" ".join([ '-p %s'%l for l in mylist ])
def sigprocs(GO,mylist):
    return procs(GO,mylist)+' --showIndivSigs --noStackSig'
def runIt(GO,name,plots=[],noplots=[]):
    print 'python mcPlots.py',"--pdir %s/%s"%(ODIR,name),GO,' '.join(['--sP %s'%p for p in plots]),' '.join(['--xP %s'%p for p in noplots]),' '.join(sys.argv[3:])
def add(GO,opt):
    return '%s %s'%(GO,opt)
def setwide(x):
    x2 = add(x,'--wide')
    x2 = x2.replace('--legendWidth 0.35','--legendWidth 0.20')
    return x2
def fulltrees(x):
    return x.replace('/data/p/peruzzi/skim_2lss_3l_TREES_74X_140116_MiniIso_tauClean_Mor16lepMVA','/data1/p/peruzzi/TREES_74X_140116_MiniIso_tauClean_Mor16lepMVA')

if __name__ == '__main__':

    torun = sys.argv[2]

    if 'data' in torun and not any([re.match(x,torun) for x in ['.*_appl.*','cr_.*']]): raise RuntimeError, 'You are trying to unblind!'

    if '2lss_' in torun:
        x = base('2lss')
        if '_appl' in torun: x = add(x,'-I TT')
        if '_1fo' in torun: x = add(x,"-A alwaystrue 1FO 'LepGood1_isTight+LepGood2_isTight==1'")
        if '_relax' in torun: x = add(x,'-X TT')
        if '_data' in torun: x = x.replace('mca-2lss-mc.txt','mca-2lss-mcdata.txt')

        if '_closure1lep' in torun:
            x = x.replace("--xP 'kinMVA_input.*'","--sP 'kinMVA_input.*'")
            x = add(x,"--AP --plotmode nostack --sP kinMVA_2lss_ttbar --sP kinMVA_2lss_ttV --sP lep1_conePt --sP lep2_conePt --sP lep1_pt --sP lep2_pt")
            x = procs(x,['TT_1lep','TT_frmc_tt','TT_frmc_qcd'])
            x = add(x,"--ratioDen TT_1lep --ratioNums TT_frmc_tt,TT_frmc_qcd")

        if '_fullclosure' in torun:
            x = x.replace('mca-2lss-mc.txt','mca-2lss-mc-mcfr.txt')
            x = add(x,"--sP kinMVA_2lss_ttbar --sP kinMVA_2lss_ttV --sP lep1_conePt --sP lep2_conePt --sP lep1_pt --sP lep2_pt")

        runIt(x,'%s/all'%torun)
        if '_flav' in torun:
            for flav in ['mm','ee','em']: runIt(add(x,'-E %s'%flav),'%s/%s'%(torun,flav))

    if '3l_' in torun:
        x = base('3l')
        if '_appl' in torun: x = add(x,'-I TTT')
        if '_relax' in torun: x = add(x,'-X TTT')
        if '_data' in torun: x = x.replace('mca-3l-mc.txt','mca-3l-mcdata.txt')
        runIt(x,'%s'%torun)

    if 'cr_3j' in torun:
        x = base('2lss')
        if '_data' in torun: x = x.replace('mca-2lss-mc.txt','mca-2lss-mcdata.txt')
        x = add(x,"-R 4j 3j 'nJet25==3' --rebin 2")
        plots = ['nJet25','nBJetLoose25','nBJetMedium25','met','metLD','htJet25j','mhtJet25','mtWmin','htllv','kinMVA_2lss_ttbar','kinMVA_2lss_ttV']
        runIt(x,'%s/all'%torun,plots)
        if '_flav' in torun:
            for flav in ['mm','ee','em']:
                runIt(add(x,'-E %s'%flav),'%s/%s'%(torun,flav),plots)
                if flav=='ee': runIt(add(x,'-E %s -X ee_metLD'%flav),'%s/%s_relaxMetLD'%(torun,flav),plots)

    if 'cr_ttbar' in torun:
        x = base('2lss')
        x = fulltrees(x)
        if '_data' in torun: x = x.replace('mca-2lss-mc.txt','mca-2lss-mcdata.txt')
        x = add(x,"-I same-sign -X 4j -X 2b1B -E 1B -E em")
        plots = ['met','metLD','nBJetLoose25','nJet25','nVert']
        runIt(x,'%s'%torun,plots)

    if 'cr_wz' in torun:
        x = base('3l')
        if '_data' in torun: x = x.replace('mca-3l-mc.txt','mca-3l-mcdata.txt')
        x = add(x,"-I 'Z veto' -X 4j -X 2b1B -E Bveto")
        plots = ['lep3_pt','metLD']
        runIt(x,'%s'%torun,plots)

    if 'cr_ttz' in torun:
        x = base('3l')
        if '_data' in torun: x = x.replace('mca-3l-mc.txt','mca-3l-mcdata.txt')
        plots = ['lep2_pt','met','nJet25']
        x = add(x,"-I 'Z veto' -X 2b1B -E 2b -E 1B")
        runIt(x,'%s'%torun,plots)
        x = add(x,"-E 4j")
        runIt(x,'%s_4j'%torun,plots)




