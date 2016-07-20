import os
import numpy as np
from array import array

from ROOT import TFile, TTree

from sklearn.externals import joblib

from CMGTools.H2TauTau.proto.plotter.Samples import createSampleLists

def ensure_dir(f):
    print 'ensure dir', f
    d = os.path.dirname(f)
    if not os.path.exists(d):
        ensure_dir(d)
    if not os.path.exists(f):
        os.mkdir(f)

analysis_dir = '/data1/steggema/mt/070416/TauMuSVFitMC/'
analysis_dir = '/data1/steggema/mt/070416/TauMuSVFitTESUp/'
analysis_dir = '/data1/steggema/mt/070416/TauMuSVFitTESDown/'

train_vars = [
    'mt',
    'n_jets',
    'met_pt',
    'pthiggs',
    'vbf_mjj',
    'vbf_deta',
    'vbf_n_central',
    'l2_pt',
    'l1_pt',
    'svfit_transverse_mass',
    'delta_phi_l1_l2',
    'delta_eta_l1_l2',
    'svfit_mass'
]

# clf0 = joblib.load('/afs/cern.ch/work/s/steggema/GradientBoostingClassifier_clf_0.pkl')
# clf1 = joblib.load('/afs/cern.ch/work/s/steggema/GradientBoostingClassifier_clf_1.pkl')

clf0_0jet = joblib.load('/afs/cern.ch/work/s/steggema/GradientBoostingClassifier_clf_0_0jet.pkl')
clf1_0jet = joblib.load('/afs/cern.ch/work/s/steggema/GradientBoostingClassifier_clf_1_0jet.pkl')
clf0_1jet = joblib.load('/afs/cern.ch/work/s/steggema/GradientBoostingClassifier_clf_0_1jet.pkl')
clf1_1jet = joblib.load('/afs/cern.ch/work/s/steggema/GradientBoostingClassifier_clf_1_1jet.pkl')
clf0_vbf = joblib.load('/afs/cern.ch/work/s/steggema/GradientBoostingClassifier_clf_0_vbf.pkl')
clf1_vbf = joblib.load('/afs/cern.ch/work/s/steggema/GradientBoostingClassifier_clf_1_vbf.pkl')


out_dict = {}

samples_mc, samples_data, samples, all_samples, sampleDict = createSampleLists(analysis_dir=analysis_dir)

trees_done = []

for sample in all_samples:
    name = sample.name
    print 'Sample', name

    file_name = '/'.join([sample.ana_dir, sample.dir_name, sample.tree_prod_name, 'tree.root'])
    file_in = TFile.Open(file_name)
    if not file_in:
        print 'WARNING, could not open file', file_name, 'continuing...'
        continue
    tree_in = file_in.Get(sample.tree_name)

    if file_name in trees_done or 'ggH' in name or 'bbH' in name:
        continue
    trees_done.append(file_name)


    file_out_name = file_name.replace('TauMuSVFitMC', 'TauMuSVFitMultiSepMVA').replace('TauMuSVFitTESUp', 'TauMuSVFitTESUpMultiSepMVA').replace('TauMuSVFitTESDown', 'TauMuSVFitTESDownMultiSepMVA')

    ensure_dir(file_out_name.replace('tree.root', ''))
    file_out = TFile(file_out_name, 'RECREATE')


    mva0_val = array('f', [0.])
    mva1_val = array('f', [0.])
    mva2_val = array('f', [0.])

    tree_out = TTree('tree', 'tree')

    mva0_name = 'mva0'
    tree_out.Branch(mva0_name, mva0_val, mva0_name+'/F')
    mva1_name = 'mva1'
    tree_out.Branch(mva1_name, mva1_val, mva1_name+'/F')
    mva2_name = 'mva2'
    tree_out.Branch(mva2_name, mva2_val, mva2_name+'/F')

    ave_mva = 0.

    for i_ev, event in enumerate(tree_in):

        if i_ev % 10000 == 0:
            print 'Event', i_ev

        split_var = event.delta_phi_l1_l2

        if int(split_var * 1000) % 2 == 0:
            clf = clf0_0jet
            if event.n_jets > 0.5:
                if event.vbf_mjj > 500. and event.vbf_deta > 3.5:
                    clf = clf0_vbf
                else:
                    clf = clf0_1jet
        else:
            clf = clf1_0jet
            if event.n_jets > 0.5:
                if event.vbf_mjj > 500. and event.vbf_deta > 3.5:
                    clf = clf1_vbf
                else:
                    clf = clf1_1jet

        inputs = []
        for var in train_vars:
            inputs.append(getattr(event, var))
        mva = clf.predict_proba(np.array(inputs).reshape(1, -1))
        mva0_val[0] = mva[0][0]
        mva1_val[0] = mva[0][1]
        mva2_val[0] = mva[0][2]
        tree_out.Fill()

        ave_mva += mva[0]

    print 'Average MVA value', ave_mva/float(tree_in.GetEntries())

    tree_out.AddFriend(tree_in)

    file_out.Write()
    file_out.Close()

