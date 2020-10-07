import os
import ROOT as r 
from root_numpy import tree2array
import pandas



import argparse
import ROOT

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--idir',      help='Folder to convert to csv', default='./temp')
args = parser.parse_args()

def load_data(file, vars):
    try: tfile = r.TFile.Open(file)
    except: raise 
    
    try: ttree = tfile.Get('Friends')
    except: raise
    print('Opened tree')
    arr = tree2array(ttree)
    print('Loaded tree in array')
    
    thedf = pandas.DataFrame(arr, columns=vars)
    print(thedf.head())
    thedf = thedf[thedf['Hreco_nLeps']==2]
    thedf = thedf[thedf['Hreco_nJets']>5]
    return thedf

thevars = [
    'nLeps',
    'nJets',
    'Lep0_pt', 'Lep0_eta', 'Lep0_phi', 'Lep0_m',
    'Lep1_pt', 'Lep1_eta', 'Lep1_phi', 'Lep1_m',
    'Lep2_pt', 'Lep2_eta', 'Lep2_phi', 'Lep2_m',
    'DeltaRl0l1',
    'DeltaRl0j0', 'DeltaRl0j1', 'DeltaRl0j2', 'DeltaRl0j3', 'DeltaRl0j4', 'DeltaRl0j5', 
    'DeltaRl1j0', 'DeltaRl1j1', 'DeltaRl1j2', 'DeltaRl1j3', 'DeltaRl1j4', 'DeltaRl1j5', 
    'DeltaRj0j0', 'DeltaRj0j1', 'DeltaRj0j2', 'DeltaRj0j3', 'DeltaRj0j4', 'DeltaRj0j5', 
    'DeltaRj1j0', 'DeltaRj1j1', 'DeltaRj1j2', 'DeltaRj1j3', 'DeltaRj1j4', 'DeltaRj1j5', 
    'DeltaRj2j0', 'DeltaRj2j1', 'DeltaRj2j2', 'DeltaRj2j3', 'DeltaRj2j4', 'DeltaRj2j5', 
    'DeltaRj3j0', 'DeltaRj3j1', 'DeltaRj3j2', 'DeltaRj3j3', 'DeltaRj3j4', 'DeltaRj3j5', 
    'DeltaRj4j0', 'DeltaRj4j1', 'DeltaRj4j2', 'DeltaRj4j3', 'DeltaRj4j4', 'DeltaRj4j5', 
    'DeltaRj5j0', 'DeltaRj5j1', 'DeltaRj5j2', 'DeltaRj5j3', 'DeltaRj5j4', 'DeltaRj5j5', 
    'Jet0_pt','Jet0_eta','Jet0_phi','Jet0_m','Jet0_btagdiscr',#'Jet1_mass',
    'Jet1_pt','Jet1_eta','Jet1_phi','Jet1_m','Jet1_btagdiscr',#'Jet1_mass',
    'Jet2_pt','Jet2_eta','Jet2_phi','Jet2_m','Jet2_btagdiscr',#'Jet2_mass',
    'Jet3_pt','Jet3_eta','Jet3_phi','Jet3_m','Jet3_btagdiscr',#'Jet2_mass',
    'Jet4_pt','Jet4_eta','Jet4_phi','Jet4_m','Jet4_btagdiscr',#'Jet2_mass',
    'Jet5_pt','Jet5_eta','Jet5_phi','Jet5_m','Jet5_btagdiscr',#'Jet2_mass',
    'Jet6_pt','Jet6_eta','Jet6_phi','Jet6_m','Jet6_btagdiscr',#'Jet2_mass',
    'HadTop_pt','HadTop_eta','HadTop_phi','HadTop_m',
    'TopScore',
    'met','met_phi',
    'HTXS_Higgs_pt','HTXS_Higgs_y',
    'Hgen_vis_pt',
    'Hgen_tru_pt',
    'evt_tag'
]

thevars = [ 'Hreco_%s'%i for i in thevars]

mydir = args.idir

for f in os.listdir(mydir):
    print('Converting ', f)
    data = load_data("%s/%s" %(mydir, f),  thevars)
    c = f.replace('.root', '.csv')
    data.to_csv("%s/%s" %(mydir, c), index=False)
