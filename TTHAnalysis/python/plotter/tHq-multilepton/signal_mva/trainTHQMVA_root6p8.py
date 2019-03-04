#!/usr/bin/env python
import sys, os, pickle
import ROOT

def cache_locally(infile, tmpDir='/tmp/'):
    tmpfile = os.path.join(tmpDir, os.path.basename(infile))

    # Copy locally if it's not there already
    if not os.path.exists(tmpfile):
        xrcmd = "xrdcp %s %s" % (infile, tmpfile)
        print " transferring to %s" % tmpDir
        os.system(xrcmd)
        print "... copied successfully"

    infile = tmpfile
    return infile

def get_file_or_copy_local(url, copy_local=True):
    if os.path.exists(url):
        return url
    if not os.path.exists('%s.url'%url):
        raise RuntimeError('File not found: %s'%url)

    url = open('%s.url'%url, 'r').read().strip()
    if not copy_local:
        return url

    else:
        return cache_locally(url, os.environ.get('TMPDIR', '/tmp'))

_dsets = {}
def read_dset_config(filename):
    global _dsets
    with open(filename, 'r') as infile:
        for line in infile:
            line = line.strip()
            if line.startswith('#'): continue
            name, treefile, friendlist = line.split(';')
            name = name.strip()
            treefile = treefile.strip()
            friendlist = friendlist.strip()
            friends = friendlist.split(',')
            friends = [f.strip() for f in friends]

            _dsets[name] = {'tree':treefile, 'friends': friends}

_allfiles = []
def load_dataset(name, trainclass, addw=1):
    global _allfiles

    fileloc = get_file_or_copy_local(
                os.path.join(_dsets[name]['tree'], 'treeProducerSusyMultilepton/tree.root'))
    print 'Using %s' % fileloc
    infile = ROOT.TFile.Open(fileloc)
    _allfiles.append(infile) # Dirty trick to keep the files and trees in memory

    tree = infile.Get('tree')

    # Check if tree was loaded
    try: tree.GetName()
    except ReferenceError:
        raise RuntimeError("'tree' not found in %s" % fileloc)

    for friend in _dsets[name]['friends']:
        friendloc = get_file_or_copy_local(os.path.join(friend, 'evVarFriend_%s.root' % name))
        print "Adding friend from", friendloc
        tree.AddFriend('sf/t', friendloc)

    pckfile = os.path.join(_dsets[name]['tree'], "skimAnalyzerCount/SkimReport.pck")
    pckobj  = pickle.load(open(pckfile,'r'))
    counters = dict(pckobj)
    weight = 1.0*addw/(counters['Sum Weights'])
    print ('Added %s dataset, category %s, with weight %f/%f' %
             (name, trainclass, addw, counters['Sum Weights']))

    return tree, weight

# Define the selections:
CUTS = {}
CUTS['3l'] = ROOT.TCut('1')
CUTS['3l'] += "nLepFO_Recl>=3"
CUTS['3l'] += "abs(mZ1_Recl-91.2)>10"
CUTS['3l'] += "LepGood_conePt[iLepFO_Recl[0]]>20"
CUTS['3l'] += "LepGood_conePt[iLepFO_Recl[1]]>10"
CUTS['3l'] += "LepGood_conePt[iLepFO_Recl[2]]>10"
#CUTS['3l'] += "nJet25_Recl >= 2"
CUTS['3l'] += "nBJetLoose25_Recl >= 1"
CUTS['3l'] += "maxEtaJet25 >= 0"

CUTS['2lss'] = ROOT.TCut('1')
CUTS['2lss'] += "nLepFO_Recl>=2"
CUTS['2lss'] += "nLepTight_Recl<=2"
CUTS['2lss'] += "LepGood_charge[iLepFO_Recl[0]]*LepGood_charge[iLepFO_Recl[1]] > 0"
CUTS['2lss'] += "LepGood_conePt[iLepFO_Recl[0]]>20"
CUTS['2lss'] += "LepGood_conePt[iLepFO_Recl[1]]>10"
#CUTS['2lss'] += "nJet25_Recl >= 2"
CUTS['2lss'] += "nBJetLoose25_Recl >= 1"
CUTS['2lss'] += "maxEtaJet25 >= 0"

# Define the variables to be used:
VARIABLES = {}
VARIABLES['3l'] = [
    ("nJet25_Recl", "I"),
    ("nJetEta1", "I"),
    ("maxEtaJet25", "F"),
    ("dEtaFwdJetBJet", "F"),
    ("dEtaFwdJetClosestLep", "F"),
    ("dPhiHighestPtSSPair", "F"),
    ("Lep3Pt := LepGood_conePt[iLepFO_Recl[2]]", "F"),
    ("minDRll", "F"),
    ("lepCharge := LepGood_charge[iLepFO_Recl[0]]+LepGood_charge[iLepFO_Recl[1]]+LepGood_charge[iLepFO_Recl[2]]", "I"),
    ("dEtaFwdJet2BJet","F"),
    ("fwdJetPt25","F"),
]
VARIABLES['2lss'] = [
    ("nJet25_Recl", "I"),
    ("nJetEta1", "I"),
    ("maxEtaJet25", "F"),
    ("dEtaFwdJetBJet", "F"),
    ("dEtaFwdJetClosestLep", "F"),
    ("dPhiHighestPtSSPair", "F"),
    ("Lep2Pt := LepGood_conePt[iLepFO_Recl[1]]", "F"),
    ("minDRll", "F"),
    ("lepCharge := LepGood_charge[iLepFO_Recl[0]]+LepGood_charge[iLepFO_Recl[1]]", "I"),
    ("dEtaFwdJet2BJet","F"),
    ("fwdJetPt25","F"),
]

def train(cuts, variables, dsets, options):
    datasets = []
    for name, trainclass, addw in dsets:
        tree, weight = load_dataset(name, trainclass, addw)
        datasets.append((name, trainclass, tree, weight))

    fOut = ROOT.TFile(options.output,"recreate")
    fOut.cd()
    factory = ROOT.TMVA.Factory(options.training, fOut,
                                ':'.join([
                                    "!V",
                                    "Color",
                                    "Transformations=I",
                                    "AnalysisType=Classification"]))

    dataloader = ROOT.TMVA.DataLoader("dataset")


    for cut in options.addcuts:
        cuts += cut

    dataloader.AddSpectator("iF0 := iLepFO_Recl[0]","F") # do not remove these
    dataloader.AddSpectator("iF1 := iLepFO_Recl[1]","F")
    dataloader.AddSpectator("iF2 := iLepFO_Recl[2]","F")

    ## Add the variables
    for var, type_ in variables:
        dataloader.AddVariable(var, type_)

    ## Add the datasets
    for name,trainclass,tree,weight in datasets:
        dataloader.AddTree(tree, trainclass, weight)

    fOut.cd()
    for trainclass in set([x[1] for x in dsets]):
        dataloader.SetWeightExpression("genWeight*xsec", trainclass)

    ## Start the training
    # Check http://tmva.sourceforge.net/docu/TMVAUsersGuide.pdf
    dataloader.PrepareTrainingAndTestTree(cuts, "!V") # check options
    factory.BookMethod(dataloader, ROOT.TMVA.Types.kBDT, 'BDTG',
                               ':'.join([
                               '!H', # print help
                               '!V', # verbose
                               'NTrees=200', # default is 200
                               'BoostType=Grad',
                               #'AdaBoostBeta=0.50',
                               'Shrinkage=0.10', # for gradient boosting
                               #'!UseBaggedGrad',
                               'nCuts=40', # scanning steps
                               'MaxDepth=4', # maximum decision tree depth
                               'NegWeightTreatment=PairNegWeightsGlobal',
                               'CreateMVAPdfs',
                               # 'VarTransform=G,D',
                               ]))

    layoutString = ROOT.TString("Layout=TANH|128,TANH|128,TANH|128,LINEAR")

     # Training strategies.
    training0 = ROOT.TString("LearningRate=1e-1,Momentum=0.9,Repetitions=1,"
                       "ConvergenceSteps=20,BatchSize=256,TestRepetitions=10,"
                       "WeightDecay=1e-4,Regularization=L2,"
                       "DropConfig=0.0+0.5+0.5+0.5, Multithreading=True")
    training1 = ROOT.TString("LearningRate=1e-2,Momentum=0.9,Repetitions=1,"
                       "ConvergenceSteps=20,BatchSize=256,TestRepetitions=10,"
                       "WeightDecay=1e-4,Regularization=L2,"
                       "DropConfig=0.0+0.0+0.0+0.0, Multithreading=True")
    training2 = ROOT.TString("LearningRate=1e-3,Momentum=0.0,Repetitions=1,"
                       "ConvergenceSteps=20,BatchSize=256,TestRepetitions=10,"
                       "WeightDecay=1e-4,Regularization=L2,"
                       "DropConfig=0.0+0.0+0.0+0.0, Multithreading=True")
    trainingStrategyString = ROOT.TString("TrainingStrategy=")
    #trainingStrategyString = ""
    vertical = ROOT.TString("|")
    #trainingStrategyString += training0 + "|" + training1 + "|" + training2
    trainingStrategyString += training0 + vertical + training1 + vertical + training2

     # General Options.
    dnnOptions = ROOT.TString("!H:V:ErrorStrategy=CROSSENTROPY:VarTransform=N:"
                         "WeightInitialization=XAVIERUNIFORM")
    dnnOptions.Append(":")
    dnnOptions.Append(layoutString)
    dnnOptions.Append(":") 
    dnnOptions.Append(trainingStrategyString)

    #cpuOptions = ROOT.TString(dnnOptions + ":Architecture=CPU")
    cpuOptions = ""
    arc = ROOT.TString(":Architecture=CPU")
    cpuOptions = dnnOptions + arc

    #factory.BookMethod(dataloader, ROOT.TMVA.Types.kDNN, 'DNN_CPU', cpuOptions)



    factory.TrainAllMethods()
    factory.TestAllMethods()
    factory.EvaluateAllMethods()

    fOut.Close()

def main(args, options):
    read_dset_config(options.treepath)

    # Define the signal and background datasets
    dsets = []
    dsets.append(('THQ',    'Signal', 1.))
    if options.training == 'ttv':
        dsets.append(('TTW_LO', 'Background', 1.))
        dsets.append(('TTZ_LO', 'Background', 1.))
    elif options.training == 'tt':
        #dsets.append(('TTJets_DiLepton_part1', 'Background', 0.5))
        #dsets.append(('TTJets_DiLepton_part2', 'Background', 0.5))
        dsets.append(('TTLep_pow_part1', 'Background', 1.))
        dsets.append(('TTLep_pow_part2', 'Background', 1.))
        dsets.append(('TTLep_pow_part3', 'Background', 1.))
        dsets.append(('TTLep_pow_part4', 'Background', 1.))
        dsets.append(('TTLep_pow_part5', 'Background', 1.))
        if options.channel == '2lss':
            #dsets.append(('TTJets_SingleLeptonFromT',        'Background', 1))
            #dsets.append(('TTJets_SingleLeptonFromTbar',     'Background', 1))
            dsets.append(('TTSemi_pow',     'Background', 1.))

    train(cuts=CUTS[options.channel],
          variables=VARIABLES[options.channel],
          dsets=dsets, options=options)

    return 0


if __name__ == '__main__':
    from optparse import OptionParser
    usage = """
    %prog [options]
    """
    parser = OptionParser(usage="%prog [options] OUTFILE")
    parser.add_option("-T","--training", dest="training",
                      type="string", default="ttv",
                      help=('Select which training to run (ttv or tt)'))
    parser.add_option("-C","--channel", dest="channel",
                      type="string", default="3l",
                      help=('Select which channel to run (3l or 2lss)'))
    parser.add_option("-P","--treepath", dest="treepath",
                      type="string", default='treepaths.txt',
                      help='File with minitree locations and friend trees')
    parser.add_option("-o","--output", dest="output",
                      type="string", default=None)
    parser.add_option("-F","--friend", dest="friends",
                      type="string", default=[], action="append")
    parser.add_option("-c","--cut", dest="addcuts",
                      type="string", default=[], action="append")
    (options, args) = parser.parse_args()

    try:
        assert(options.training in ['ttv', 'tt'])
        assert(options.channel in ['3l', '2lss'])
    except AssertionError:
        print "Unknown training or channel, choose a combination of ('ttv', 'tt') and ('3l', '2lss')"
        sys.exit(-1)

    if not options.output:
        options.output = 'thq_training_%s_%s.root' % (options.training, options.channel)

    if not options.treepath:
        parser.print_help()
        sys.exit(-1)

    sys.exit(main(args, options))


