#!/usr/bin/env python

## ELECTRONS
# e.g.: python  w-helicity-13TeV/skims.py w-helicity-13TeV/wmass_e/mca-80X-skims.txt w-helicity-13TeV/wmass_e/skim_wenu.txt  TREES_1LEP_80X_V3 /eos/cms/store/group/dpg_ecal/comm_ecal/localreco/TREES_1LEP_80X_V3_WENUSKIM_V2 -f w-helicity-13TeV/wmass_e/varsSkim_80X.txt
#       python  w-helicity-13TeV/skims.py w-helicity-13TeV/wmass_e/mca-80X-skims.txt w-helicity-13TeV/wmass_e/skim_zee.txt   TREES_1LEP_80X_V3 /eos/cms/store/group/dpg_ecal/comm_ecal/localreco/TREES_1LEP_80X_V3_ZEESKIM_V2  -f w-helicity-13TeV/wmass_e/varsSkim_80X.txt
#       python  w-helicity-13TeV/skims.py w-helicity-13TeV/wmass_e/mca-80X-skims.txt w-helicity-13TeV/wmass_e/skim_fr_el.txt TREES_1LEP_80X_V3 /eos/cms/store/group/dpg_ecal/comm_ecal/localreco/TREES_1LEP_80X_V3_FRELSKIM_V2 -f w-helicity-13TeV/wmass_e/varsSkim_80X_fr.txt

## MUONS
# DATA:
#       python  w-helicity-13TeV/skims.py w-helicity-13TeV/wmass_mu/skimming/mca-wmu-skim-bkg-data.txt w-helicity-13TeV/wmass_mu/skimming/skimCuts.txt /eos/user/m/mdunser/w-helicity-13TeV/trees/2017_12_12_legacy_singlemu/ /eos/user/m/mdunser/w-helicity-13TeV/trees/2017_12_12_legacy_singlemu/skims/ -f w-helicity-13TeV/wmass_mu/skimming/varsToKeep.txt --mo
# MC:  
#       python  w-helicity-13TeV/skims.py w-helicity-13TeV/wmass_mu/skimming/mca-wmu-skim-bkg-data.txt w-helicity-13TeV/wmass_mu/skimming/skimCuts.txt /eos/cms/store/group/dpg_ecal/comm_ecal/localreco/TREES_1LEP_80X_V3/ /eos/user/m/mdunser/w-helicity-13TeV/trees/TREES_2018-03-21_MC_1muskim/ -f w-helicity-13TeV/wmass_mu/skimming/varsToKeep.txt --mo

# SIGNAL:  
#       python  w-helicity-13TeV/skims.py w-helicity-13TeV/wmass_mu/skimming/mca-signal.txt w-helicity-13TeV/wmass_mu/skimming/signalCuts.txt /eos/cms/store/group/dpg_ecal/comm_ecal/localreco/TREES_1LEP_80X_V3_NoSkim5/ /eos/user/m/mdunser/w-helicity-13TeV/trees/TREES_2018-03-21_SIGNAL_1muskim/ -f w-helicity-13TeV/wmass_mu/skimming/varsToKeep.txt

# SIGNAL FRIENDS:  
#       python  w-helicity-13TeV/skims.py w-helicity-13TeV/wmass_mu/skimming/mca-signal.txt w-helicity-13TeV/wmass_mu/skimming/signalCuts.txt /eos/cms/store/group/dpg_ecal/comm_ecal/localreco/TREES_1LEP_80X_V3_NoSkim5/ /eos/user/m/mdunser/w-helicity-13TeV/trees/TREES_2018-03-21_SIGNAL_1muskim/ -f w-helicity-13TeV/wmass_mu/skimming/varsToKeep.txt

# add -q 8nh --log logs to run in batch 1 job/component (and --pretend to just check the command that will be run)

### FRIEND TREES ###
# then skim the friend trees, using the event lists saved from te previous step
# this is enough fast to be done interactively in series for all the datasets
# it's the same command as before, with --fo (--friend-only) option. Eventually may give a file with the list of variables to keep (as for the main trees)

## ELECTRONS
#        python w-helicity-13TeV/skims.py w-helicity-13TeV/wmass_e/mca-80X-skims.txt w-helicity-13TeV/wmass_e/skim_wenu.txt TREES_1LEP_80X_V3 /eos/cms/store/group/dpg_ecal/comm_ecal/localreco/TREES_1LEP_80X_V3_WENUSKIM_V2 -f w-helicity-13TeV/wmass_e/varsSkim_80X_helicity_friends.txt --fo

import os, subprocess

if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser(usage="%prog [options] mc.txt cuts.txt treeDir outputDirSkims ")
    parser.add_option("-f", "--varfile",  dest="varfile", type="string", default=None, action="store",  help="File with the list of Branches to drop, as per TTree::SetBranchStatus")
    parser.add_option("--fo", "--friend-only",  dest="friendOnly", action="store_true", default=False,  help="Do not redo skim of the main trees, only of the friends")
    parser.add_option("--mo", "--main-only",  dest="mainOnly", action="store_true", default=False,  help="Do not make skim of the friend trees, only of the main")
    parser.add_option("--max-entries",     dest="maxEntries", default=1000000000, type="int", help="Max entries to process in each tree") 
    from CMGTools.WMass.plotter.skimTrees import addSkimTreesOptions
    addSkimTreesOptions(parser)
    (options, args) = parser.parse_args() 

    mcargs = args[:2]
    treeDir = args[2]
    outputDirSkims = args[3]

    outputDirFSkims = outputDirSkims+"/friends"

    if not options.friendOnly:
        if not os.path.exists(outputDirSkims):
            os.makedirs(outputDirSkims)
            os.makedirs(outputDirFSkims)
        else:
            print "The skim output dir ",outputDirSkims," exists. Will remove it and substitute with new one. \nDo you agree?[y/N]\n"
            if raw_input()!='y':
                print 'Aborting'
                exit()
            os.system("rm -rf "+outputDirSkims)
            os.makedirs(outputDirSkims)
            os.makedirs(outputDirFSkims)
        os.system('cp {vf} {od}'.format(od=outputDirSkims,vf=options.varfile))
        os.system('cp {sf} {od}'.format(od=outputDirSkims,sf=args[1])) ## this should work??
    else: print "Make only the friend trees in dir ",outputDirFSkims

    OPTS = ' --obj tree -P '+treeDir+' --s2v -j 4 -F Friends "{P}/friends/tree_Friend_{cname}.root" '
    OPTS += ' --max-entries %d ' % options.maxEntries 
    if options.pretend: OPTS += ' --pretend '
    if options.queue: OPTS += ' -q %s ' % options.queue
    if options.logdir: OPTS += ' --log %s ' % options.logdir

    varsToKeep = []; DROPVARS = ''
    if options.varfile!=None:
        with open(options.varfile) as f:
            varsToKeep = f.read().splitlines()
        DROPVARS = " --dropall --keep "+" --keep ".join(varsToKeep)
        OPTS += DROPVARS
    
    cmdSkim = "python skimTrees.py "+" ".join(mcargs)+" " + outputDirSkims + OPTS
    cmdFSkimEv = " python skimFTrees.py "+outputDirSkims+" "+treeDir+"/friends/ "+outputDirFSkims+' -f tree_Friend -t "Friends" ' + DROPVARS

    if not options.friendOnly:
        print "Now skimming the main trees, keeping the following vars:\n",varsToKeep
        print "This step may take time...\n"
        os.system(cmdSkim)
    if not options.queue and not options.mainOnly:
        print "Now skimming the event variables friend trees:\n"
        os.system(cmdFSkimEv)
        # print "Now skimming the fake rate friend trees:\n"
        # os.system(cmdFSkimFr)
        # print "Now skimming the trigger friend trees:\n"
        # os.system(cmdFSkimTg)

    print "VERY DONE\n"


