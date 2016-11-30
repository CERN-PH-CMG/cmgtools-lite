import os
import time
import numpy as np
from array import array

from ROOT import TFile, TTree, TTreeFormula

from sklearn.externals import joblib

from CMGTools.H2TauTau.proto.plotter.Samples import createSampleLists
from CMGTools.H2TauTau.proto.plotter.Variables import getVars

def ensure_dir(f):
    print 'ensure dir', f
    d = os.path.dirname(f)
    if not os.path.exists(d):
        ensure_dir(d)
    if not os.path.exists(f):
        os.mkdir(f)

analysis_dir = '/data1/steggema/mt/051016/MuTauMC/'

train_vars = getVars([
    'mt', 'l2_mt', 'n_jets', 'met_pt', 'pthiggs', 'vbf_mjj', 'vbf_deta', 'vbf_n_central', 'l2_pt', 'l1_pt','mvis', 'l1_eta', 'l2_eta', 'delta_phi_l1_l2', 'delta_eta_l1_l2', 'pt_l1l2', 'delta_phi_j1_met', 'pzeta_disc', 'jet1_pt', 'jet1_eta'
])
split_var = train_vars[10]

mva_name = 'mva'

clf0 = joblib.load('GradientBoostingClassifier_clf_0_0jet.pkl')
clf1 = joblib.load('GradientBoostingClassifier_clf_1_0jet.pkl')

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


    file_out_name = file_name.replace('MuTauMC', 'MuTauMVA')

    if file_out_name == file_name:
        print 'Error, identical file names', file_out_name, file_name
        raise RuntimeError('Exiting...')

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

    for var in train_vars:
        if var.drawname != var.name:
            var.formula = TTreeFormula('formula'+var.name, var.drawname, tree_in)
            var.formula.GetNdata()

    t_start = time.time()


    for i_ev, event in enumerate(tree_in):

        if i_ev % 10000 == 0:
            print 'Event', i_ev
            t_current = time.time()
            print 'Time', t_current- t_start
            t_start = t_current

        split_var_val = split_var.formula.EvalInstance() if hasattr(split_var, 'formula') else getattr(event, split_var.name)

        if int(split_var_val * 1000) % 2 == 0:
            clf = clf0
        else:
            clf = clf1

        inputs = []
        for var in train_vars:
            val = var.formula.EvalInstance() if hasattr(var, 'formula') else getattr(event, var.name)
            inputs.append(val)
            
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

