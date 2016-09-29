#!/usr/bin/env python
import sys, os, pickle
import ROOT

_treepath = None

def cacheLocally(infile, tmpDir='/tmp/'):
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
        return cacheLocally(url, os.environ.get('TMPDIR', '/tmp'))

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


def train(allcuts, variables, dsets, fOutName, options):
    datasets = []
    for name, trainclass, addw in dsets:
        tree, weight = load_dataset(name, trainclass, addw)
        datasets.append((name, trainclass, tree, weight))

    fOut = ROOT.TFile(fOutName,"recreate")
    fOut.cd()
    factory = ROOT.TMVA.Factory(options.training, fOut, "!V:!Color:Transformations=I")

    for cut in options.addcuts:
        allcuts += cut

    factory.AddSpectator("iF0 := iF_Recl[0]","F") # do not remove these
    factory.AddSpectator("iF1 := iF_Recl[1]","F")
    factory.AddSpectator("iF2 := iF_Recl[2]","F")

    ## Add the variables
    for var in variables:
        factory.AddVariable(var, 'F')

    ## Add the datasets
    for name,trainclass,tree,weight in datasets:
        factory.AddTree(tree, trainclass, weight)

    fOut.cd()
    for trainclass in set([x[1] for x in dsets]):
        factory.SetWeightExpression("genWeight*xsec", trainclass)

    ## Start the training
    factory.PrepareTrainingAndTestTree(allcuts, "!V")
    factory.BookMethod(ROOT.TMVA.Types.kBDT, 'BDTG',
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


def main(args, options):
    global _treepath
    _treepath = options.treepath

    read_dset_config(_treepath)

    allcuts = ROOT.TCut('1')
    allcuts += "nLepFO_Recl>=3"
    allcuts += "abs(mZ1_Recl-91.2)>10"
    allcuts += "LepGood_conePt[iF_Recl[0]]>20"
    allcuts += "LepGood_conePt[iF_Recl[1]]>10"
    allcuts += "LepGood_conePt[iF_Recl[2]]>10"
    allcuts += "nJet25_Recl >= 2"
    allcuts += "nBJetLoose25_Recl >= 1"
    allcuts += "maxEtaJet25 >= 0"

    variables = [
        "max_Lep_eta := max(abs(LepGood_eta[iF_Recl[0]]),abs(LepGood_eta[iF_Recl[1]]))",
        "numJets_float := nJet25_Recl",
        "maxEtaJet25 := maxEtaJet25",
        # "MT_met_lep1 := MT_met_lep1",
    ]

    dsets = []
    dsets.append(('THQ',                                 'Signal', 3.))
    if options.training.lower() == 'ttv':
        # dsets.append(('TTWToLNu',                        'Background', 1))
        # dsets.append(('TTZToLLNuNu',                     'Background', 1))
        dsets.append(('TTW_LO',                          'Background', 1))
        dsets.append(('TTZ_LO',                          'Background', 1))
    elif options.training.lower() == 'tt':
        dsets.append(('TTJets_DiLepton',                 'Background', 0.1))
        dsets.append(('TTJets_DiLepton_ext_skim3l',      'Background', 0.9))
        dsets.append(('TTJets_SingleLeptonFromT',        'Background', 0.1))
        dsets.append(('TTJets_SingleLeptonFromTbar',     'Background', 0.1))
        dsets.append(('TTJets_SingleLeptonFromT_ext',    'Background', 0.9))
        dsets.append(('TTJets_SingleLeptonFromTbar_ext', 'Background', 0.9))
    else:
        print "Please choose either 'ttv' or 'tt' for -T option"
        return 1

    train(allcuts=allcuts,
          variables=variables,
          dsets=dsets,
          fOutName='thq_mva.root',
          options=options)

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

    if not options.output:
        options.output = 'thq_training_%s.root' % options.training

    if not options.treepath:
        parser.print_help()
        sys.exit(-1)

    sys.exit(main(args, options))
