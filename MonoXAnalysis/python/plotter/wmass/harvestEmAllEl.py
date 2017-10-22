import CombineHarvester.CombineTools.ch as ch
import CombineHarvester.CombinePdfs.morphing as morphing
import ROOT
import sys, glob,datetime,os,re

Iamdebugging = True
# import some parameters from wmass_parameters.py, they are also used by other scripts
from wmass_parameters import *

if Iamdebugging:
    print "mass_id_down, mass_id_up = %s,%s" % (mass_id_down,mass_id_up)    

if len(sys.argv) < 2:
    print "----- WARNING -----"
    print "Too few arguments: need at list cards folder name (absolute afs path). E.g.: /afs/blabla/python/plotter/cards/<whatever_you_chose>/"
    print "-------------------"
    quit()


class WMassFitMaker:
    def __init__(self,mwrange,mwcentral,npoints,bindir,options=None):
        self.mwrange = mwrange
        self.mwcentral = mwcentral
        self.npoints = npoints
        self.bindir = bindir
        self.options = options


    def harvestEm(self,channel='wenu',charge='both'):
        cmb = ch.CombineHarvester()

        # Read all the cards.
        # CH stores metadata about each object (Observation, Process, Systematic),
        # this is extracted from the card names with some regex
        for card in glob.glob(self.bindir+('/%s_mass*.txt' % channel)):
            cmb.QuickParseDatacard(card, """%s_mass(?<MASS>\d+)_$CHANNEL.card.txt""" % channel)

        # Need a unqiue bin name for each plus/minus,pt and eta combination
        # We extracted this part of the datacard name into the channel variable above,
        # so can just copy it and override the specific bin name that was in all the cards
        cmb.ForEachObj(lambda obj: obj.set_bin(obj.channel()))

        # We'll have three copies of the observation, one for each mass point.
        # Filter all but one copy.
        cmb.FilterObs(lambda obj: obj.mass() != '%d' % self.mwcentral)

        # Create workspace to hold the morphing pdfs and the mass
        w = ROOT.RooWorkspace('morph', 'morph')
        mass = w.factory('mw[{mwrange}]'.format(mwrange=self.mwrange))

        # BuildRooMorphing will dump a load of debug plots here
        debug = ROOT.TFile(self.bindir+'/debug.root', 'RECREATE')

        # Run for each bin,process combination (only for signal!)
        for b in cmb.bin_set():
            for p in cmb.cp().bin([b]).signals().process_set():
                morphing.BuildRooMorphing(w, cmb, b, p, mass, verbose=True, file=debug)

        # Just to be safe
        mass.setConstant(True)

        # Now the workspace is copied into the CH instance and the pdfs attached to the processes
        # (this relies on us knowing that BuildRooMorphing will name the pdfs in a particular way)
        cmb.AddWorkspace(w, True)
        cmb.cp().process(['W']).ExtractPdfs(cmb, 'morph', '$BIN_$PROCESS_morph', '')

        # Adjust the rateParams a bit - we currently have three for each bin (one for each mass),
        # but we only want one. Easiest to drop the existing ones completely and create new ones
        cmb.syst_type(['rateParam'], False)
        cmb.cp().process(['W']).AddSyst(cmb, 'norm_$BIN', 'rateParam', ch.SystMap()(1.00))

        # Have to set the range by hand
        for sys in cmb.cp().syst_type(['rateParam']).syst_name_set():
            cmb.GetParameter(sys).set_range(0.5, 1.5)

        # Print the contents of the model
        cmb.PrintAll()

        # Write out the cards, one per bin
        outdir=self.bindir+'/wenu_cards_morphed_{charge}'.format(charge=charge)
        writer = ch.CardWriter('$TAG/$BIN.txt', '$TAG/shapes.root')
        writer.SetVerbosity(1)
        writer.WriteCards(outdir, cmb)

    def combineCards(self, input_dcs,target_dc):
        ## running combineCards to make the combined plus+minus datacard                        
        if os.path.isfile(target_dc):  
            print 'removing existing combined datacard first!'
            os.system('rm {dc}'.format(dc=target_dc) )
        #dcs = os.listdir(subdir+"/wenu_cards_morphed_both/")  # what's the purpose of this line?
        print 'running combineCards.py'
        combineCardsCmd = 'combineCards.py {dcs} >& {target_dc}'.format(dcs=input_dcs, target_dc=target_dc)
        print combineCardsCmd
        ## run combineCards and make the workspace                                                                            
        os.system(combineCardsCmd )
        print 'running text2workspace'
        t2wCmd = 'text2workspace.py {target_dc} '.format(subdir=subdir, target_dc=target_dc)
        print t2wCmd
        os.system(t2wCmd)

    def run(self, workspaces):
        if len(workspaces)<1:
            print "ERROR: no workspaces passed. Doint nothing."
            return

        date = datetime.date.today().isoformat()

        combineCmds = {}
        for m,ws in enumerate(workspaces):
            print "===> RUN FIT FOR WORKSPACE: ",ws
            # name = re.search('\S+eta\_(\S+)\/wenu\S+',ws)
            name = re.search('\S+eta\_(\S+)\/wenu\S+',ws)
            if name==None: 
                name="comb"
            else:
                name=name.group(1)
            if self.options.debug:
                print "In run() function: name = " + str(name)
            ## constructing the command                                                                                                                                     
            combine_base  = 'combine -t -1 -M MultiDimFit --setPhysicsModelParameters mw={central},r=1 --setPhysicsModelParameterRanges mw={mwrange} '.format(central=self.mwcentral,mwrange=self.mwrange)
            combine_base += ' --redefineSignalPOIs=mw --algo grid --points {npoints} {target_ws} '.format(npoints=self.npoints, target_ws=ws)

            saveNuisances = ''
            saveNuisances += ' --saveSpecifiedNuis {vs}'.format(vs=','.join('CMS_We_pdf'+str(i) for i in range(1,27)))
            saveNuisances += ','
            saveNuisances += '{vs} '.format(vs=','.join(['CMS_W_ptw','CMS_We_elescale']))

            combineCmds["nominal"] = combine_base + ' -n {date}_{name} {sn} '.format(date=date,name=name,sn=saveNuisances)
            for nuisgroup in self.options.freezeNuisanceGroups:
                nuisgroup_name = nuisgroup.split(",")[0]
                nuisgroup_friendlyName = nuisgroup.split(",")[0]
                if (len(nuisgroup.split(",")) > 1):
                    nuisgroup_friendlyName = nuisgroup.split(",")[1]
                combineCmds["no%s" % nuisgroup_friendlyName] = combine_base + ' -n {date}_{name}_no{uncfr} --freezeNuisanceGroups {unc} '.format(date=date,name=name,uncfr=nuisgroup_friendlyName,unc=nuisgroup_name)
            for nuis in self.options.freezeNuisances:
                nuis_name = nuis.split(",")[0]
                nuis_friendlyName = nuis.split(",")[0]
                if (len(nuis.split(",")) > 1):
                    nuis_friendlyName = nuis.split(",")[1]
                combineCmds["no%s" % nuis_friendlyName] = combine_base + ' -n {date}_{name}_no{uncfr} --freezeNuisances {unc} '.format(date=date,name=name,uncfr=nuis_friendlyName,unc=nuis_name)

            keys = combineCmds.keys()
            keys.sort()
            
            for key in keys:
                #print "%s: %s" % (key, combineCmds.get(key))
                cmd = combineCmds.get(key)
                if runBatch:
                    cmd += ' --job-mode lxbatch --split-points 10 --sub-opts="-q 8nh" --task-name {name}_{uncset}'.format(name=name,uncset=key)
                cmd = 'combineTool.py ' + ' '.join(cmd.split()[1:])
                print '-- running combine command ------------------------------'
                print '---   ' + str(key) + ': -----------------------------'
                print cmd
                os.system(cmd)

            # another possibility
            # for key,cmd in combineCmds.iteritems():
            #     if runBatch:
            #         cmd += ' --job-mode lxbatch --split-points 10 --sub-opts="-q 8nh" --task-name {name}_{uncset}'.format(name=name,uncset=key)
            #     cmd = 'combineTool.py ' + ' '.join(cmd.split()[1:])
            #     print '-- running combine command ------------------------------'
            #     print '---   ' + str(key) + ': -----------------------------'
            #     print cmd
            #     os.system(cmd)

##
## following commented snippet is not needed anymore
##
            ## running combine once with the systematics and once without                        
            # print '-- running combine command ------------------------------'
            # print '---     with uncertainties: -----------------------------'
            # print run_combine_allUnc
            # os.system(run_combine_allUnc)

            # print '---     without PDF uncertainties: --------------------------'
            # print run_combine_noPdf
            # os.system(run_combine_noPdf )

            # print '---     without PTW uncertainties: --------------------------'
            # print run_combine_noPtW
            # os.system(run_combine_noPtW )

            # print '---     without electron energy scale uncertainties: --------------------------'
            # print run_combine_noEScale
            # os.system(run_combine_noEScale )

            # impactBase = 'combineTool.py -M Impacts -n {date}_eta_{name} -d {target_ws} -m {mass}'.format(mass=m,date=date,name=name, target_ws=ws)
            # impactBase += ' --setPhysicsModelParameters mw={central},r=1  --redefineSignalPOIs=mw --setPhysicsModelParameterRanges mw={mwrange} -t -1 '.format(central=central,mwrange=mwrange)
            # impactInitial = impactBase+'  --robustFit 1 --doInitialFit '
            # impactFits    = impactBase+'  --robustFit 1 --doFits '
            # impactJSON    = impactBase+'  -o impacts_eta_{name}.json '.format(name=name)
            # impactPlot    = 'plotImpacts.py -i impacts_eta_{name}.json -o impacts_eta_{name} --transparent'.format(name=name)

            # os.system(impactInitial)
            # os.system(impactFits   )
            # os.system(impactJSON   )
            # os.system(impactPlot   )


from optparse import OptionParser
parser = OptionParser(usage="%prog /afs/path/to/datacard/in/CMSSW_8_0_25/ [options]")
# add options
parser.add_option("--freezeNuisances",dest="freezeNuisances",action="append", default=[],help="append a nuisance parameter to freeze when doing the fit. Can pass two names separated by comma: the first is the nuisance name in the datacard, the second a user friendly name for recording (if not given, use the first name)")
parser.add_option("--freezeNuisanceGroups",dest="freezeNuisanceGroups",action="append", default=[],help="append a group of nuisance parameters to freeze when doing the fit. Can pass two names separated by comma: the first is the nuisance name in the datacard, the second a user friendly name for recording (if not given, use the first name)")
parser.add_option("--step", dest="step", type="string", default=None, help="Specify which step to do: available options are runHarvest, combineCards, runFit. This option is mandatory.")
parser.add_option("-d", "--debug", dest="debug", action="store_true", default=False, help="if True, print some info on stdout (default is False)")
(options, args) = parser.parse_args()

if options.debug:
    print "mass_id_down, mass_id_up = %s,%s" % (mass_id_down,mass_id_up)

card_dir = str(args[0])  # it should be the absolute path to CMSSW_8_0_25 release
if not card_dir.endswith("/"):
    card_dir = card_dir + "/"
if not "CMSSW_8_0_25" in str(args[0]) or not str(args[0]).startswith("/afs/"):
    print "### WARNING ###"    
    print "The path to datacard folder is expected to be inside a CMSSW_8_0_25 release and the absolute path should be passed. Did you type the right full path?"
    print "Quitting ..."
    quit()


if not options.step:
    print "### WARNING ###"    
    print "You forgot option --step <arg>, where <arg> can be runHarvest, combineCards, runFit. Please try again"
    quit()

#card_dir = 'cards/' + str(args[0]) + '/'
subdirs = [x[0] for x in os.walk(card_dir)]

#mwrange='0,30'
# values from wmass_parameters.py
mwrange='%d,%d' % (mass_id_down,mass_id_up)
npoints = n_mass_id
central = mass_id_central

runBatch   = False # not needed, running in local is faster at the moment
justHadd   = False # actually not implemented
runHarvest = False
combineCards = False
runFit = False
if options.step == "runHarvest":
    runHarvest = True
elif options.step == "combineCards":
    combineCards = True
elif options.step == "runFit":
    runFit = True
else:
    print "### ERROR ###"
    print " step = %s is not a valid option. Choice is among runHarvest, combineCards, runFit. Please try again" % str(options.step)
    quit()

input_dcs_alleta = ""
workspaces = []
for isub, subdir in enumerate(subdirs):
    if options.debug: 
        print "### subdir"
        print str(subdir)
    if subdir == subdirs[0]: continue
    if 'wenu_cards_morphed' in subdir: continue
    name = subdir.split('/')[-1]
    if not 'eta_' in name: continue
    if options.debug:
        print "subdir was accepted"
    print '--------------------------------------------------------------------'
    print '- running for {mode} -----------------------------------------------'.format(mode=name)
    print '- in subdirectory {subdir} -----------------------------------------'.format(subdir=subdir)
    print '--------------------------------------------------------------------'

    fit = WMassFitMaker(mwrange,central,npoints,subdir, options)

    if runHarvest:
        ## run the combine harvester which combines all the datacards etc. 
        fit.harvestEm()

    target_dc = '{subdir}/wenu_cards_morphed_both/morphed_datacard_channel.txt'.format(subdir=subdir)
    target_ws = target_dc.replace('txt','root')
    workspaces.append(target_ws)

    if combineCards:
        dcs = os.listdir(subdir+"/wenu_cards_morphed_both/")
        input_dcs=" ".join(["%s=%s" % (os.path.splitext(dc)[0],subdir+"/wenu_cards_morphed_both/"+dc) for dc in dcs if "txt" in dc])
        input_dcs_alleta += " "+input_dcs

        if options.debug:
            print ""
            print "input datacards --> input_dcs = " + str(input_dcs)
            print "target datacard --> target_dc = " + str(target_dc)
            print ""

        fit.combineCards(input_dcs,target_dc)

comb_dir = card_dir+'comb'
if not os.path.exists(comb_dir): 
    os.mkdir(comb_dir)
comb_dc = comb_dir+"/morphed_datacard_comb.txt"
comb_ws = comb_dc.replace('txt','root')
workspaces.append(comb_ws)        

if combineCards:
    if options.debug:
        print ""
        print ""
        print "Now the final step to combine datacards"
        print "input datacards --> input_dcs_alleta = " + str(input_dcs_alleta)
        print "target datacard --> comb_dc          = " + str(comb_dc)
        print ""
        print ""
    fit.combineCards(input_dcs_alleta,comb_dc)

if runFit:
    fit.run(workspaces)

    # for m,ws in enumerate(workspaces):
    #     print "===> RUN FIT FOR WORKSPACE: ",ws
    #     name = re.search('\S+eta\_(\S+)\/wenu\S+',ws).group(1)
    #     if name==None: name="comb"
    #     ## constructing the command
    #     combine_base  = 'combine -t -1 -M MultiDimFit --setPhysicsModelParameters mw={central},r=1 --setPhysicsModelParameterRanges mw={mwrange} '.format(central=central,mwrange=mwrange)
    #     combine_base += ' --redefineSignalPOIs=mw --algo grid --points {npoints} {target_ws} '.format(npoints=npoints, target_ws=ws)

    #     saveNuisances = ''
    #     saveNuisances += ' --saveSpecifiedNuis {vs} '.format(vs=','.join('CMS_We_pdf'+str(i) for i in range(1,27)))

    #     date = datetime.date.today().isoformat()

    #     run_combine_allUnc = combine_base + ' -n {date}_{name} {sn} '.format(date=date,name=name,sn=saveNuisances)
    #     run_combine_noPdf  = combine_base + ' -n {date}_{name}_noPDFUncertainty --freezeNuisanceGroups pdfUncertainties '.format(date=date,name=name)
    #     run_combine_noPtW  = combine_base + ' -n {date}_{name}_noPTWUncertainty --freezeNuisances CMS_W_ptw '.format(date=date,name=name)
    #     run_combine_noEScale  = combine_base + ' -n {date}_{name}_noEScaleUncertainty --freezeNuisances CMS_We_elescale '.format(date=date,name=name)

    #     if runBatch:
    #         run_combine_allUnc += ' --job-mode lxbatch --split-points 10 --sub-opts="-q 8nh" --task-name {name}                  '.format(name=name)
    #         run_combine_noPdf  += ' --job-mode lxbatch --split-points 10 --sub-opts="-q 8nh" --task-name {name}_noPDFUncertainty '.format(name=name)
    #         run_combine_noPtW  += ' --job-mode lxbatch --split-points 10 --sub-opts="-q 8nh" --task-name {name}_noPtWUncertainty '.format(name=name)
    #         run_combine_noEScale  += ' --job-mode lxbatch --split-points 10 --sub-opts="-q 8nh" --task-name {name}_noEScaleUncertainty '.format(name=name)
    #         run_combine_allUnc  = 'combineTool.py ' + ' '.join(run_combine_allUnc.split()[1:])
    #         run_combine_noPdf   = 'combineTool.py ' + ' '.join(run_combine_noPdf .split()[1:])
    #         run_combine_noPtW   = 'combineTool.py ' + ' '.join(run_combine_noPtW .split()[1:])
    #         run_combine_noEScale   = 'combineTool.py ' + ' '.join(run_combine_noEScale .split()[1:])

    
    #     ## running combine once with the systematics and once without 
    #     print '-- running combine command ------------------------------'
    #     print '---     with uncertainties: -----------------------------'
    #     print run_combine_allUnc
    #     os.system(run_combine_allUnc)

    #     print '---     without PDF uncertainties: --------------------------'
    #     print run_combine_noPdf
    #     os.system(run_combine_noPdf )

    #     print '---     without PTW uncertainties: --------------------------'
    #     print run_combine_noPtW
    #     os.system(run_combine_noPtW )

    #     print '---     without electron energy scale uncertainties: --------------------------'
    #     print run_combine_noEScale
    #     os.system(run_combine_noEScale )

    #     # impactBase = 'combineTool.py -M Impacts -n {date}_eta_{name} -d {target_ws} -m {mass}'.format(mass=m,date=date,name=name, target_ws=ws)
    #     # impactBase += ' --setPhysicsModelParameters mw={central},r=1  --redefineSignalPOIs=mw --setPhysicsModelParameterRanges mw={mwrange} -t -1 '.format(central=central,mwrange=mwrange)
    #     # impactInitial = impactBase+'  --robustFit 1 --doInitialFit '
    #     # impactFits    = impactBase+'  --robustFit 1 --doFits '
    #     # impactJSON    = impactBase+'  -o impacts_eta_{name}.json '.format(name=name)
    #     # impactPlot    = 'plotImpacts.py -i impacts_eta_{name}.json -o impacts_eta_{name} --transparent'.format(name=name)

    #     # os.system(impactInitial)
    #     # os.system(impactFits   )
    #     # os.system(impactJSON   )
    #     # os.system(impactPlot   )    



