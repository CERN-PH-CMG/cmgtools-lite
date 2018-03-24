#!/usr/bin/env python
# may use as: cat w-helicity-13TeV/wmass_e/zee_catlist.txt | xargs -i python w-helicity-13TeV/wmass_e/wmass_plots.py plots/testZskim {} > runplots.sh
# may use as: cat w-helicity-13TeV/wmass_e/wgen_catlist.txt | xargs -i python w-helicity-13TeV/wmass_e/wmass_plots.py plots/gen {} > runplots.sh
import sys
import re
import os

ODIR=sys.argv[1]

FASTTEST=''
#FASTTEST='--max-entries 1000 '

dowhat = "plots" 
#dowhat = "dumps" 
#dowhat = "yields" 

TREES = "-F Friends '{P}/friends/tree_Friend_{cname}.root' "
TREESONLYSKIMW = "-P /eos/cms/store/group/dpg_ecal/comm_ecal/localreco/TREES_1LEP_80X_V3_WENUSKIM_V5_TINY"
TREESONLYSKIMZ = "-P /eos/cms/store/group/dpg_ecal/comm_ecal/localreco/TREES_1LEP_80X_V3_ZEESKIM_V6"
TREESONLYFULL  = "-P /eos/cms/store/group/dpg_ecal/comm_ecal/localreco/TREES_1LEP_80X_V3"

def base(selection,useSkim=True):

    if 'wenu' in selection: TREESONLYSKIM=TREESONLYSKIMW
    if 'wgen' in selection: TREESONLYSKIM=TREESONLYSKIMW
    elif 'zee' in selection: TREESONLYSKIM=TREESONLYSKIMZ
    else:
        raise RuntimeError, 'Unknown selection'

    CORE=' '.join([TREES,TREESONLYSKIM if useSkim else TREESONLYFULL])
    if 'cmsphys06' in os.environ['HOSTNAME']: CORE = CORE.replace('/eos/cms/store/group/dpg_ecal/comm_ecal/localreco/','/data1/emanuele/wmass/')

    CORE+=" -f -j 8 -l 35.9 --s2v "+FASTTEST
    if dowhat == "plots": CORE+=" --lspam '#bf{CMS} #it{Preliminary}' --legendWidth 0.20 --legendFontSize 0.035 "
    if selection != "wgen":
        CORE+=" --showRatio --maxRatioRange 0.75 1.25 --fixRatioRange "

    if selection=='wenu':
        GO="%s w-helicity-13TeV/wmass_e/mca-80X-wenu-helicity.txt w-helicity-13TeV/wmass_e/wenu_80X.txt "%CORE
        GO="%s -W 'puw2016_nTrueInt_36fb(nTrueInt)*trgSF_We(LepGood1_pdgId,LepGood1_pt,LepGood1_eta,2)*leptonSF_We(LepGood1_pdgId,LepGood1_pt,LepGood1_eta)'"%GO
        GO="%s --AP --xp 'Wplus.*,Wminus.*' "%GO
        if dowhat in ["plots","ntuple"]: GO+=" w-helicity-13TeV/wmass_e/wenu_plots.txt "
    elif selection=='wgen':
        GO="%s w-helicity-13TeV/wmass_e/mca-80X-wenu-helicity.txt w-helicity-13TeV/wmass_e/wenu_80X.txt "%CORE
        GO="%s -p Wplus_long,Wplus_left,Wplus_right --plotmode=nostack "%GO
        #GO="%s --sP wplus_mtwtk,wplus_etal1,wplus_ptl1,wplus_etal1gen,wplus_ptl1gen,wplus_wy,wplus_wpt "%GO
        GO="%s --sP wplus_wy "%GO
        if dowhat in ["plots","ntuple"]: GO+=" w-helicity-13TeV/wmass_e/wenu_plots.txt "        
    elif selection=='zee':
        GO="%s w-helicity-13TeV/wmass_e/mca-80X-skims.txt w-helicity-13TeV/wmass_e/skim_zee.txt "%CORE
        GO="%s -W 'puw2016_nTrueInt_36fb(nTrueInt)*trgSF_We(LepGood1_pdgId,LepGood1_pt,LepGood1_eta,2)*leptonSF_We(LepGood1_pdgId,LepGood1_pt,LepGood1_eta)*leptonSF_We(LepGood2_pdgId,LepGood2_pt,LepGood2_eta)' --sp 'Z' "%GO
        if dowhat in ["plots","ntuple"]: GO+=" w-helicity-13TeV/wmass_e/zee_plots.txt "
    else:
        raise RuntimeError, 'Unknown selection'

    return GO

def procs(GO,mylist):
    return GO+' '+" ".join([ '-p %s'%l for l in mylist ])
def sigprocs(GO,mylist):
    return procs(GO,mylist)+' --showIndivSigs --noStackSig'
def runIt(GO,name,plots=[],noplots=[]):
    if   dowhat == "plots":  print 'python mcPlots.py',"--pdir %s/%s"%(ODIR,name),GO,' '.join(['--sP \'%s\''%p for p in plots]),' '.join(['--xP \'%s\''%p for p in noplots])
    elif dowhat == "yields": print 'echo %s; python mcAnalysis.py'%name,GO
    elif dowhat == "dumps":  print 'echo %s; python mcDump.py'%name,GO
    elif dowhat == "ntuple": print 'echo %s; python mcNtuple.py'%name,GO
def submitIt(GO,name,plots=[],noplots=[],opts=None):
    outdir=ODIR+"/jobs/"
    if not os.path.isdir(outdir): os.mkdir(outdir)
    srcfile = outdir+name+".sh"
    logfile = outdir+name+".log"
    srcfile_op = open(srcfile,"w")
    srcfile_op.write("#! /bin/sh\n")
    srcfile_op.write("ulimit -c 0\n")
    srcfile_op.write("cd {cmssw};\neval $(scramv1 runtime -sh);\ncd {dir};\n".format( 
            dir = os.getcwd(), cmssw = os.environ['CMSSW_BASE']))
    srcfile_op.write("python mcPlots.py "+" --pdir %s/%s "%(ODIR,name)+GO+' '.join(['--sP \'%s\''%p for p in plots])+' '.join(['--xP \'%s\''%p for p in noplots])+'\n')
    os.system("chmod a+x "+srcfile)
    cmd = "bsub -q 8nh -o {dir}/{logfile} {dir}/{srcfile}\n".format(dir=os.getcwd(), logfile=logfile, srcfile=srcfile)
    if opts.dryRun: print "[DRY-RUN]: ", cmd
    else: os.system(cmd)
def add(GO,opt):
    return '%s %s'%(GO,opt)
def remove(GO,opt):
    return GO.replace(opt,'')
def swapcharge(GO,charge):
    return GO.replace('plus',charge)
def setwide(x):
    x2 = add(x,'--wide')
    x2 = x2.replace('--legendWidth 0.35','--legendWidth 0.20')
    return x2
def fulltrees(x,selection):
    if 'wenu' in selection: TREESONLYSKIM=TREESONLYSKIMW
    elif 'zee' in selection: TREESONLYSKIM=TREESONLYSKIMZ
    else:
        raise RuntimeError, 'Unknown selection'
    return x.replace(TREESONLYSKIM,TREESONLYFULL)

allow_unblinding = True

if __name__ == '__main__':

    from optparse import OptionParser
    parser = OptionParser(usage="%prog outdir what [options] ")
    parser.add_option("--dry-run", dest="dryRun",    action="store_true", default=False, help="Do not run the job, only print the command");
    parser.add_option("-q", "--queue",    dest="queue",     type="string", default=None, help="Run jobs on lxbatch instead of locally");
    (options, args) = parser.parse_args()

    torun = sys.argv[2]

    if (not allow_unblinding) and '_data' in torun and (not any([re.match(x.strip()+'$',torun) for x in ['.*_appl.*','cr_.*']])): raise RuntimeError, 'You are trying to unblind!'

    x=""
    if 'zee' in torun:
        x = base('zee')
        if '_incl' in torun: x = add(x," --sP 'etal1,etal2' ")
        if '_ebeb' in torun: x = add(x,"-A alwaystrue ebeb 'max(abs(LepGood1_eta),abs(LepGood2_eta))<1.44'  --sP 'zmass,zmass_corr' ")
        if '_notebeb' in torun: x = add(x,"-A alwaystrue notebeb 'max(abs(LepGood1_eta),abs(LepGood2_eta))>1.57' --sP 'zmass,zmass_corr' ")
        if '_gg' in torun: x = add(x,"-A alwaystrue goldgold 'min(LepGood1_r9,LepGood2_r9)>0.94' --sP 'zmass,zmass_corr' ")
        if '_notgg' in torun: x = add(x,"-A alwaystrue notgoldgold 'min(LepGood1_r9,LepGood2_r9)<0.94' --sP 'zmass,zmass_corr' ")
        #if '_w_reweight' in torun and dowhat=="plots": x = add(x,"--sP 'z_mll,pt1,pt2,ptZ,scaledptZ,costheta_cs,phi_cs,sumAiPi,y_vs_ctheta,y_vs_phi,y_vs_sumAiPi' ")
        #if '_genpt' in torun: x = add(x,"--sP 'gen_ptv,gen_scaledptv' --xp 'data' -p 'Z' ")
    elif 'wenu' in torun:
        x = base('wenu')
    elif 'wgen' in torun:
        x = base('wgen')
        if 'plus' in torun: x = swapcharge(x,'plus')
        elif 'minus' in torun: x = swapcharge(x,'minus')
        if 'nosel' in torun:
             x = add(x," -U 'alwaystrue' ")
        if 'fullsel' in torun:
            x = add(x," -W 'puw2016_nTrueInt_36fb(nTrueInt)*trgSF_We(LepGood1_pdgId,LepGood1_pt,LepGood1_eta,2)*leptonSF_We(LepGood1_pdgId,LepGood1_pt,LepGood1_eta)' ")
        if torun.endswith('pdfs'):
            for i in xrange(60):
                wgt = 'hessWgt[%d]/genWeight' % i
                output = '%s/%s_pdf%i.root' % (ODIR,torun,i)
                xw = x
                xw = add(xw," -W '{wgt}' -o {output}".format(wgt=wgt,output=output))
                submitIt( xw,'%s_%s' % (torun,i), opts=options )

    plots = [] # if empty, to all the ones of the txt file
    if not torun.endswith('pdfs'): 
        if options.queue: submitIt(x,'%s'%torun,plots,opts=options)
        else: runIt(x,'%s'%torun,plots)
