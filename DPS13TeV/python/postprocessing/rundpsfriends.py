import os

td = '/eos/user/m/mdunser/dps-13TeV-combination/TREES_latest/'
n =  150000

baseCmd = 'python postproc_batch.py -N {n}  -q 8nh --log friends_log --friend '.format(n=n)
#cmdJet = baseCmd+' {td} {od}  -I CMGTools.DPS13TeV.postprocessing.examples.jetReCleaner jetReCleaner '                  .format(td=td,od=td+'/friends/')
#cmdBDT = baseCmd+' {td} {od}  -I CMGTools.DPS13TeV.postprocessing.examples.bdtWeigthsDPS_WZ_and_fakes BDT_WZ_and_fakes '.format(td=td,od=td+'/friends_bdt_new2/')

cmdJet = baseCmd+' {td} {od} '.format(td=td,od=td+'/friends/')
cmdBDT = baseCmd+' {td} {od} '.format(td=td,od=td+'/friends_bdt_new2/')

dss_wmass = []
dss_multi = []

for d in os.listdir(td):
    if 'friend' in d: continue
    if '.root'  in d: continue
    for sd in os.listdir(td+'/'+d):
        if 'treeProducerSusyMultilepton' in sd:
            dss_multi.append(d)
        if 'treeProducerWMass' in sd:
            dss_wmass.append(d)

#cmdJet += ' -d '+' -d '.join(dss)
cmdBDT_multi = cmdBDT+' --tree treeProducerSusyMultilepton  -d '+' -d '.join(dss_multi)
cmdBDT_wmass = cmdBDT+' -d '+' -d '.join(dss_wmass)

#os.system(cmdJet)
#os.system(cmdBDT)
print cmdBDT_multi
print ''
print cmdBDT_wmass
