#!/usr/bin/env python
import sys, os, pickle
import ROOT

_treepath = None
_allfiles = []

def get_file_or_copy_local(url, copy_local=True):
    if os.path.exists(url):
        return url
    if not os.path.exists('%s.url'%url):
        raise RuntimeError('File not found: %s'%url)

    url = open('%s.url'%url, 'r').read().strip()
    if not copy_local:
        return url

    else:
        from LepMVAEfficiencies.runLepTnPFriendMaker import cacheLocally
        return cacheLocally(url, os.environ.get('TMPDIR', '/tmp'))

def load_dataset(name, trainclass, addw=1, path=None, friends=[]):
    if not path:
        path = _treepath
        if not path:
            raise RuntimeError('No default tree path set')

    fileloc = get_file_or_copy_local(
                os.path.join(path, name, 'treeProducerSusyMultilepton/tree.root'))
    print 'Using %s' % fileloc
    infile = ROOT.TFile.Open(fileloc)
    _allfiles.append(infile) # Dirty trick to keep the files and trees in memory

    tree = infile.Get('tree')

    # Check if tree was loaded
    try: tree.GetName()
    except ReferenceError:
        raise RuntimeError("'tree' not found in %s" % fileloc)

    for friend in friends:
        friendloc = get_file_or_copy_local(os.path.join(path, friend, 'evVarFriend_%s.root' % name))
        print "Adding friend from", friendloc
        tree.AddFriend('sf/t', friendloc)

    pckfile = os.path.join(path, name, "skimAnalyzerCount/SkimReport.pck")
    pckobj  = pickle.load(open(pckfile,'r'))
    counters = dict(pckobj)
    weight = 1.0*addw/(counters['Sum Weights'])
    print ('Added %s dataset, category %s, with weight %f/%f' %
             (name, trainclass, addw, counters['Sum Weights']))

    return tree, weight

def train_single(allcuts, variables, dsets, fOutName, options):
    datasets = []
    for name, trainclass, addw in dsets:
        tree, weight = load_dataset(name, trainclass, addw,
                                    path=options.treepath,
                                    friends=options.friends)
        datasets.append((name, trainclass, tree, weight))

    fOut = ROOT.TFile(fOutName+'.root',"recreate")
    fOut.cd()
    factory = ROOT.TMVA.Factory(options.training, fOut, "!V:!Color:Transformations=I")
    dataloader = ROOT.TMVA.DataLoader('dataset')

    for cut in options.addcuts:
        allcuts += cut

    dl = ROOT.TMVA.DataLoader("dataset_%s"%fOutName)

    dl.AddSpectator("iF0 := iLepFO_Recl[0]","F") # do not remove this!
    dl.AddSpectator("iF1 := iLepFO_Recl[1]","F") # do not remove this!
    dl.AddSpectator("iF2 := iLepFO_Recl[2]","F") # do not remove this!

    ## Add the variables
    for var in variables:
        dl.AddVariable(var, 'F')

    ## Add the datasets
    for name,trainclass,tree,weight in datasets:
        dl.AddTree(tree, trainclass, weight)

    fOut.cd()
    for trainclass in set([x[1] for x in dsets]):
        dl.SetWeightExpression("prescaleFromSkim*genWeight*xsec", trainclass)

    ## Start the training
    nTrain_Signal = int(dl.DataInput().GetSignalEntries()*0.8)
    nTrain_Background = int(dl.DataInput().GetBackgroundEntries()*0.8)
    nTest_Background = dl.DataInput().GetBackgroundEntries()-nTrain_Background
    nTest_Signal = dl.DataInput().GetSignalEntries()-nTrain_Signal
    dl.PrepareTrainingAndTestTree(allcuts, "!V:nTrain_Signal=%d:nTest_Signal=%d:nTrain_Background=%d:nTest_Background=%d:ScaleWithPreselEff"%(nTrain_Signal,nTest_Signal,nTrain_Background,nTest_Background))
    factory.BookMethod(dl,ROOT.TMVA.Types.kBDT, 'BDTG',
                            ':'.join([
                                '!H',
                                '!V',
                                'NTrees=200',
                                'BoostType=Grad',
                                'Shrinkage=0.10',
                                '!UseBaggedGrad',
                                'nCuts=200',
                                'nEventsMin=100',
                                'NNodesMax=5',
                                'MaxDepth=8',
                                'NegWeightTreatment=PairNegWeightsGlobal',
                                'CreateMVAPdfs',
                                ]))
    factory.TrainAllMethods()
    factory.TestAllMethods()
    factory.EvaluateAllMethods()

    fOut.Close()

def train_2d(fOutName, training, options):
    allcuts = ROOT.TCut('1')
    if '2lss' in training:
        allcuts += "nLepFO_Recl>=2"
        allcuts += "LepGood_conePt[iLepFO_Recl[0]]>25"
        allcuts += "LepGood_conePt[iLepFO_Recl[1]]>15"
        allcuts += "LepGood_charge[iLepFO_Recl[0]] == LepGood_charge[iLepFO_Recl[1]]"
        allcuts += "(nBJetLoose25_Recl >= 2 || nBJetMedium25_Recl >= 1)"
        allcuts += "nJet25_Recl >= 4"
    elif '3l' in training:
        allcuts += "nLepFO_Recl>=3"
        allcuts += "abs(mZ1_Recl-91.2)>10"
        allcuts += "LepGood_conePt[iLepFO_Recl[0]]>25"
        allcuts += "LepGood_conePt[iLepFO_Recl[1]]>15"
        allcuts += "LepGood_conePt[iLepFO_Recl[2]]>15"
        allcuts += "(nJet25_Recl >= 4 || (met_pt*0.00397 + mhtJet25_Recl*0.00265 - 0.184 > 0.0 + 0.1*(mZ1_Recl > 0)))"
        allcuts += "nBJetLoose25_Recl >= 2"

    variables = [ # Common variables
        "max_Lep_eta := max(abs(LepGood_eta[iLepFO_Recl[0]]),abs(LepGood_eta[iLepFO_Recl[1]]))",
        "numJets_float := nJet25_Recl",
        "mindr_lep1_jet := mindr_lep1_jet",
        "mindr_lep2_jet := mindr_lep2_jet",
        "MT_met_lep1 := MT_met_lep1",
    ]
    
    dsets = []
    if '3l' in training and 'mem' in training:
        if not 'skim_3l_2j_2b1B' in options.treepath: raise RuntimeError
        dsets += [('TTHnobb_pow_train1', 'Signal', 7.971808)]
        dsets += [('TTHnobb_pow_train2', 'Signal', 7.971808)]
        dsets += [('TTHnobb_pow_train3', 'Signal', 7.971808)]
    else:
        dsets += [('TTHnobb_pow', 'Signal', 1)]

    if '2lss' in training and 'ttw' in training:
        variables += ["LepGood_conePt[iLepFO_Recl[1]] := LepGood_conePt[iLepFO_Recl[1]]"]
        dsets += [('TTW_LO', 'Background', 1)]

    if '2lss' in training and 'ttv' in training:
        variables += [
            "LepGood_conePt[iLepFO_Recl[1]] := LepGood_conePt[iLepFO_Recl[1]]",
            "LepGood_conePt[iLepFO_Recl[0]] := LepGood_conePt[iLepFO_Recl[0]]"
        ]
        dsets += [
            ('TTW_LO', 'Background', 1),
            ('TTZ_LO', 'Background', 1),
        ]
    if '2lss' in training and 'ttbar' in training:
        variables += [
#            "met := min(met_pt, 400)",
#            "avg_dr_jet : = avg_dr_jet",
        ]
        dsets += [
            ('TTJets_SingleLeptonFromT',        'Background', 1.0),
            ('TTJets_SingleLeptonFromTbar',     'Background', 1.0),
        ]


    if '3l' in training and 'ttw' in training:
        variables += ["LepGood_conePt[iLepFO_Recl[2]] := LepGood_conePt[iLepFO_Recl[2]]"]
        dsets += [('TTW_LO', 'Background', 1)]
    if '3l' in training and 'ttv' in training:
        variables += [
            "LepGood_conePt[iLepFO_Recl[2]] := LepGood_conePt[iLepFO_Recl[2]]",
            "LepGood_conePt[iLepFO_Recl[0]] := LepGood_conePt[iLepFO_Recl[0]]"
        ]
        if "mem" in training:
            if not 'skim_3l_2j_2b1B' in options.treepath: raise RuntimeError
            dsets += [
                ('TTW_LO_train1', 'Background', 2.918363),
                ('TTW_LO_train2', 'Background', 2.918363),
                ('TTW_LO_train3', 'Background', 2.918363),
                ('TTZ_LO_train1', 'Background', 4.096574),
                ('TTZ_LO_train2', 'Background', 4.096574),
                ('TTZ_LO_train3', 'Background', 4.096574),
                ]
        else:
            dsets += [
                ('TTW_LO', 'Background', 1),
                ('TTZ_LO', 'Background', 1),
                ]
    if '3l' in training and 'ttbar' in training:
        variables += [
#            "mhtJet25 := mhtJet25_Recl",
#            "avg_dr_jet : = avg_dr_jet",
        ]
        if "mem" in training:
            if not 'skim_3l_2j_2b1B' in options.treepath: raise RuntimeError
            dsets += [
                ('TTJets_DiLepton_part1_train1',           'Background', 16156033.0/(16156033.0+987698.0)),
                ('TTJets_DiLepton_part2_train1',           'Background', 987698.0/(16156033.0+987698.0)),
                ('TTJets_SingleLeptonFromT_train1',        'Background', 1.0),
                ('TTJets_SingleLeptonFromTbar_train1',     'Background', 1.0),
                ('TTLep_pow_part1_train3',                 'Background', 1166830868.59/(1166830868.59+1169106139.83)),
                ('TTLep_pow_part2_train3',                 'Background', 1169106139.83/(1166830868.59+1169106139.83)),
                ('TTSemi_pow_train3',                      'Background', 1.0),
            ]
        else:
            dsets += [
                ('TTJets_DiLepton_part1',            'Background', 16156033.0/(16156033.0+987698.0)),
                ('TTJets_DiLepton_part2',            'Background', 987698.0/(16156033.0+987698.0)),
                ('TTJets_SingleLeptonFromT',        'Background', 1.0),
                ('TTJets_SingleLeptonFromTbar',     'Background', 1.0),
            ]

    if 'bdtv8_bestchoice' in training:
        variables += [
            'BDTv8_eventReco_mvaValue := max(-0.2,BDTv8_eventReco_mvaValue)',
            "BDTv8_eventReco_bJet_fromHadTop_CSV := max(-0.2,BDTv8_eventReco_bJet_fromHadTop_CSV)",
            "BDTv8_eventReco_HadTop_pT := max(-10,BDTv8_eventReco_HadTop_pT)",
            "BDTv8_eventReco_HadTop_mass := max(-10,BDTv8_eventReco_HadTop_mass)",
            ]
    if 'bdtv8_onlymass' in training:
        variables += [
            'BDTv8_eventReco_mvaValue := max(-0.2,BDTv8_eventReco_mvaValue)',
            "BDTv8_eventReco_HadTop_mass := max(-10,BDTv8_eventReco_HadTop_mass)",
            ]
    if 'bdtv8_value' in training:
        variables += [
            'BDTv8_eventReco_mvaValue := max(-1.1,BDTv8_eventReco_mvaValue)',
            ]
    if 'bdtrTT_value' in training:
        variables += [
            'BDTrTT_eventReco_mvaValue := max(-1.1,BDTrTT_eventReco_mvaValue)',
            ]
    if 'bdthttTT_value' in training:
        variables += [
            'BDThttTT_eventReco_mvaValue := max(-1.1,BDThttTT_eventReco_mvaValue)',
            ]
    if 'bdtv8_reco' in training:
        variables += [
            "BDTv8_eventReco_bJet_fromLepTop_CSV := max(-1.1,BDTv8_eventReco_bJet_fromLepTop_CSV)",
            "BDTv8_eventReco_bJet_fromHadTop_CSV := max(-1.1,BDTv8_eventReco_bJet_fromHadTop_CSV)",
            "BDTv8_eventReco_qJet1_fromW_fromHadTop_CSV := max(-1.1,BDTv8_eventReco_qJet1_fromW_fromHadTop_CSV)",
            "BDTv8_eventReco_HadTop_pT := BDTv8_eventReco_HadTop_pT",
            "BDTv8_eventReco_W_fromHadTop_mass := BDTv8_eventReco_W_fromHadTop_mass",
            "BDTv8_eventReco_HadTop_mass := BDTv8_eventReco_HadTop_mass",
            "BDTv8_eventReco_W_fromHiggs_mass := BDTv8_eventReco_W_fromHiggs_mass",
            "BDTv8_eventReco_LepTop_HadTop_dR := BDTv8_eventReco_LepTop_HadTop_dR",
            ]
    if 'hadtopsimple' in training:
        variables += [
            "HadTopSimple_bJet_fromHadTop_CSV := max(-1.1,bJet_fromHadTop_CSV)",
            "HadTopSimple_lJet_fromHadTop_CSV2 := max(-1.1,lJet_fromHadTop_CSV2)",
            "HadTopSimple_HadTop_Mass := HadTop_Mass",
            "HadTopSimple_HadTop_Pt := HadTop_Pt",
            "HadTopSimple_W_fromHadTop_Mass := W_fromHadTop_Mass",
            "HadTopSimple_bJet_notFromHadTop_CSV := max(-1.1,bJet_notFromHadTop_CSV)"
            ]
    if 'memlogs' in training:
        variables += [
            "MEM_TTHvsTTW := max(-10.,min(50.,log(MEM_TTH)-log(MEM_TTW)))",
            "MEM_TTHvsTTZ := max(-10.,min(50.,log(MEM_TTH)-log(MEM_TTLL)))",
            ]
    if 'memvars' in training:
        variables += [
            "MEM_TTH := max(-100.,min(10.,log(MEM_TTH)))",
            "MEM_TTW := max(-100.,min(10.,log(MEM_TTW)))",
            "MEM_TTZ := max(-100.,min(10.,log(MEM_TTLL)))",
            ]
    if 'memfixvars' in training:
        variables += [
            "MEM_TTH := min(0,log(max(3.72e-44,MEM_TTH)))",
            "MEM_TTW := min(0,log(max(3.72e-44,MEM_TTW)))",
            "MEM_TTZ := min(0,log(max(3.72e-44,MEM_TTLL)))",
            ]
    if 'memlr' in training:
        if 'ttv' in training:
            variables += [
                "MEM_LR_ttHttV := -log((0.00389464*MEM_TTLL*(MEM_TTLL<1) + 3.12221e-14*MEM_TTW*(MEM_TTW<1)) / (0.00389464*MEM_TTLL*(MEM_TTLL<1) + 3.12221e-14*MEM_TTW*(MEM_TTW<1)+9.99571e-05*(MEM_TTH_mean*(MEM_TTH_mean<1))))"
                ]
        if 'ttbar' in training:
            variables += [
                "MEM_LR_ttHttbar := -log((MEM_TTbarfl*(MEM_TTbarfl<1)+MEM_TTbarsl*(MEM_TTbarsl<1)) / (MEM_TTH_mean*(MEM_TTH_mean<1)))"
                ]
    if 'hj_value_v8' in training:
        variables += [
            'BDTv8_eventReco_Hj_score := max(-1.1,BDTv8_eventReco_Hj_score)',
#            'BDTv8_eventReco_Hjj_score := max(-1.1,BDTv8_eventReco_Hjj_score)',
            ]
    if 'hj_value_rTT' in training:
        variables += [
            'BDTrTT_eventReco_Hj_score := max(-1.1,BDTrTT_eventReco_Hj_score)',
            ]
    if 'hj_value_httTT' in training:
        variables += [
            'BDThttTT_eventReco_Hj_score := max(-1.1,BDThttTT_eventReco_Hj_score)',
            ]

    outname = fOutName+'_'+training
    train_single(allcuts, variables, dsets, outname, options)

def main(args, options):
    global _treepath
    _treepath = options.treepath

    if len(options.training):
        train_2d(args[0], options.training.lower(), options)
    else:
        train_2d(args[0], '2lss_ttv',   options)
        train_2d(args[0], '2lss_ttv_hj_value_v8',   options)
        train_2d(args[0], '2lss_ttv_hj_value_rTT',   options)
        train_2d(args[0], '2lss_ttv_hj_value_httTT',   options)
        train_2d(args[0], '2lss_ttbar', options)
        train_2d(args[0], '2lss_ttbar_bdtv8_value', options)
        train_2d(args[0], '2lss_ttbar_bdtrTT_value', options)
        train_2d(args[0], '2lss_ttbar_bdthttTT_value', options)
        train_2d(args[0], '3l_ttv',     options)
#        train_2d(args[0], '3l_ttv_memlr',     options)
        train_2d(args[0], '3l_ttbar',   options)
#        train_2d(args[0], '3l_ttbar_memlr',   options)


if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser(usage="%prog [options] OUTFILE")
    parser.add_option("-T","--training", dest="training",
                      type="string", default="",
                      help=('Either "MultiClassICHEP16" or "2lss_ttw",'
                            '"3l_ttbar", etc. Default will run all 2D trainings'))
    parser.add_option("-P","--treepath", dest="treepath",
                      type="string", default=None)
    parser.add_option("-F","--friend", dest="friends",
                      type="string", default=[], action="append")
    parser.add_option("-c","--cut", dest="addcuts",
                      type="string", default=[], action="append")
    (options, args) = parser.parse_args()

    if not len(args) or not options.treepath:
        parser.print_help()
        sys.exit(-1)

    main(args, options)
