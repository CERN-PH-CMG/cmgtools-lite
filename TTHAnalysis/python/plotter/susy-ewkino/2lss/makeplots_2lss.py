#!/usr/bin/env python
import sys,os
import re

ODIR=sys.argv[1]

dowhat = "plots" 
#dowhat = "dumps" 
#dowhat = "yields" 

def replaceInFile(path, search, replace):
    f = open(path, "r")
    lines = "".join(f.readlines())
    f.close()
    lines = lines.replace(search, replace)
    os.system("rm " + path)
    f = open(path, "w")
    f.write(lines)
    f.close()


def base(selection):
    
    CORE="-P /afs/cern.ch/user/f/folguera/workdir/trees/ewkino/8011_July12_skimmed/ -F sf/t {P}/2_recleaner_wpsViX4mrE2_ptJIMIX3/evVarFriend_{cname}.root"
    CORE+=" -F sf/t {P}/3_leptonJetReCleanerSusyEWK3L/evVarFriend_{cname}.root -F sf/t {P}/4_evtbtag_12fb_2lss/evVarFriend_{cname}.root"
    CORE+=" -f -j 8 -l 12.9 --s2v --tree treeProducerSusyMultilepton --mcc susy-ewkino/2lss/lepchoice-2lss-FO.txt --mcc susy-ewkino/mcc_triggerdefs.txt --neg"
    if dowhat == "plots":  CORE+=" --cms --legendWidth 0.20 --legendFontSize 0.035 --showRatio --maxRatioRange 0 3 --showMCError --legendHeader '2lss' "
    CORE+="-W 'puw2016_nInt_ICHEP(nTrueInt)*triggerSF_2lss_ewk(LepGood1_pt,LepGood2_pt,LepGood2_pdgId)*leptonSF_2lss_ewk(LepGood1_pdgId,LepGood1_pt,LepGood1_eta)*leptonSF_2lss_ewk(LepGood2_pdgId,LepGood2_pt,LepGood2_eta)*eventBTagSF' "

    GO="%s susy-ewkino/2lss/mca-2lss-mc.txt susy-ewkino/2lss/cuts_2lss.txt  "%CORE
    if dowhat == "plots": GO+=" susy-ewkino/2lss/plots_2lss.txt --xP 'nT_.*' "
    return GO

def procs(GO,mylist):
    return GO+' '+" ".join([ '-p %s'%l for l in mylist ])
def sigprocs(GO,mylist):
    return procs(GO,mylist)+' --showIndivSigs --noStackSig'
def runIt(GO,name,queue='',plots=[],noplots=[]):
    if   dowhat == "plots":  
        cmd = "python mcPlots.py --pdir {dir}/{name} {sel} ".format(dir = ODIR, name = name, sel = GO)
        cmd.join(['--sP %s '%p for p in plots])
        cmd.join(['--xP %s '%p for p in noplots])
        cmd.join(sys.argv[3:])
#        print 'echo python mcPlots.py',"--pdir %s/%s"%(ODIR,name),GO,' '.join(['--sP %s'%p for p in plots]),' '.join(['--xP %s'%p for p in noplots]),' '.join(sys.argv[3:])
        if 'q' in queue:
            if not os.path.exists("tmp/"): os.mkdir("tmp")
            script = "tmp/runplotter_"+name.replace('/','_')+".sh"
            os.system('cp {orig} {dest}'.format( orig = "runplotter.sh", dest = script))
            replaceInFile(script, "WORK=$1; shift", "WORK=\"" + os.getcwd() + "\"")
            replaceInFile(script, "SRC=$1; shift" , "SRC=\"" + os.getcwd().replace("/CMGTools/TTHAnalysis/python/plotter", "") + "\"")
            f = open(script, "a")
            f.write(cmd + "\n")
            f.close()
            basecmd = "bsub -q 8nh {workdir}/{runner}".format(workdir = os.getcwd(), runner=script)
            print basecmd
        else: 
            print cmd
                    
    elif dowhat == "yields": print 'echo %s; python mcAnalysis.py'%name,GO,' '.join(sys.argv[3:])
    elif dowhat == "dumps":  print 'echo %s; python mcDump.py'%name,GO,' '.join(sys.argv[3:])
    
def add(GO,opt):
    return '%s %s'%(GO,opt)
def setwide(x):
    x2 = add(x,'--wide')
    x2 = x2.replace('--legendWidth 0.35','--legendWidth 0.20')
    return x2

allow_unblinding = True
    

if __name__ == '__main__':
    
    torun = sys.argv[2]
    queue = ''
    if len(sys.argv)>3: queue = sys.argv[3]
    
    if (not allow_unblinding) and 'data' in torun and (not any([re.match(x.strip()+'$',torun) for x in ['.*_appl.*','cr_.*']])): raise RuntimeError, 'You are trying to unblind!'

    if '2lss_' in torun:
        x = base('2lss')
        if '_appl' in torun: 
            x = add(x,'-I ^TT ')
        if '_1fo' in torun:
            x = add(x,"-A alwaystrue 1FO 'LepGood1_isTight+LepGood2_isTight==1'")
            x = x.replace("--xP 'nT_.*'","")
        if '_2fo' in torun: 
            x = add(x,"-A alwaystrue 2FO 'LepGood1_isTight+LepGood2_isTight==0'")
        if '_relax' in torun: 
            x = add(x,'-X ^TT ')
        if '_data' in torun: 
            x = x.replace('mca-2lss-mc.txt','mca-2lss-mcdata.txt')
        if '_frdata' in torun:
            if not '_data' in torun: raise RuntimeError
            x = x.replace('mca-2lss-mcdata.txt','mca-2lss-mcdata-frdata.txt')
            x = add(x,'--plotgroup fakes_data+=promptsub')

        if '_flav' in torun:
            for flav in ['mm','ee','em']: runIt(add(x,'-E ^%s'%flav),'%sa/%s'%(torun.rstrip('_flav'),flav),queue)

        elif '_jet' in torun:
            runIt(add(x,'-E ^0j'),'%s/%s'%(torun.rstrip('_jet'),'0jet'),queue)
            runIt(add(x,'-E ^1j'),'%s/%s'%(torun.rstrip('_jet'),'1jet'),queue)
        elif '_SR' in torun:
            for sr in range(1,19): runIt(add(x,"-A alwaystrue SR 'SR_ewk_ss2l(nJet40,LepGood1_conePt,LepGood1_phi, LepGood2_conePt,LepGood2_phi, met_pt,met_phi)==%s'"%sr),'%s/%s'%(torun.rstrip('_SR'),"SR%s"%sr),queue)
        else:
            runIt(x,'%s'%torun,queue)

            
