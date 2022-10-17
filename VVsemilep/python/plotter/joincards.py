import sys, re

torun = ['%s=%s'%(x.split('/')[-1].split('.')[0],x) for x in sys.argv[3:]]
print 'echo Will join to %s these cards:'%(sys.argv[2],), torun

print 'combineCards.py %s > %s.txt'%(' '.join([x for x in torun]), sys.argv[2] )

if sys.argv[1]=="standard":
    print 'text2workspace.py -o %s.root %s.txt'%(sys.argv[2],sys.argv[2])
elif sys.argv[1]=="unconstrained_all":
    print "text2workspace.py -o %s.root %s.txt \
           -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel --PO verbose \
           --PO 'map=.*/ttH.*:r_ttH[1,-5,10]' \
           --PO 'map=.*/TTW:r_TTW[1,0,6]' \
           --PO 'map=.*/TTZ:r_TTZ[1,0,6]' \
           --PO 'map=.*2lss_mm.*/fakes_data:r_fakes_mu[0,4]' \
           --PO 'map=.*2lss_ee.*/fakes_data:r_fakes_el[0,4]' \
           --PO 'map=.*2lss_em.*/fakes_data:r_fakes_em=expr::r_fakes_em(\"0.45*@0+0.55*@1\",r_fakes_mu,r_fakes_el)' \
           --PO 'map=.*2lss_1tau.*/fakes_data:r_fakes_em=expr::r_fakes_em(\"0.45*@0+0.55*@1\",r_fakes_mu,r_fakes_el)' \
           --PO 'map=.*3l.*/fakes_data:r_fakes_em=expr::r_fakes_em(\"0.45*@0+0.55*@1\",r_fakes_mu,r_fakes_el)' \
    "%(sys.argv[2],sys.argv[2])
elif sys.argv[1]=="unconstrained_ttZ":
    print "text2workspace.py -o %s.root %s.txt \
           -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel --PO verbose \
           --PO 'map=.*/ttH.*:r_ttH[1,-5,10]' \
           --PO 'map=.*/TTZ:r_TTZ[1,0,6]' \
    "%(sys.argv[2],sys.argv[2])
elif sys.argv[1]=="2l_3l_relative":
    print "text2workspace.py -o %s.root %s.txt \
           -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel --PO verbose \
           --PO 'map=.*2lss.*/ttH.*:r_ttH_2lss[1,-5,10]' \
           --PO 'map=none:dr_3l[-5,10]' \
           --PO 'map=.*3l.*/ttH:r_ttH_3l=sum::r_ttH_3l(r_ttH_2lss,dr_3l)' \
    "%(sys.argv[2],sys.argv[2])
elif sys.argv[1]=="2l_3l_relative_unconstrained":
    print "text2workspace.py -o %s.root %s.txt \
           -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel --PO verbose \
           --PO 'map=.*2lss.*/ttH.*:r_ttH_2lss[1,-5,10]' \
           --PO 'map=none:dr_3l[-5,10]' \
           --PO 'map=.*3l.*/ttH:r_ttH_3l=sum::r_ttH_3l(r_ttH_2lss,dr_3l)' \
           --PO 'map=.*/TTW:r_TTW[1,0,6]' \
           --PO 'map=.*/TTZ:r_TTZ[1,0,6]' \
           --PO 'map=.*2lss_mm.*/fakes_data:r_fakes_mu[0,4]' \
           --PO 'map=.*2lss_ee.*/fakes_data:r_fakes_el[0,4]' \
           --PO 'map=.*2lss_em.*/fakes_data:r_fakes_em=expr::r_fakes_em(\"0.45*@0+0.55*@1\",r_fakes_mu,r_fakes_el)' \
           --PO 'map=.*2lss_1tau.*/fakes_data:r_fakes_em=expr::r_fakes_em(\"0.45*@0+0.55*@1\",r_fakes_mu,r_fakes_el)' \
           --PO 'map=.*3l.*/fakes_data:r_fakes_em=expr::r_fakes_em(\"0.45*@0+0.55*@1\",r_fakes_mu,r_fakes_el)' \
    "%(sys.argv[2],sys.argv[2])
else:
    raise RuntimeError

print "echo standard fit \# combine %s.root -M MaxLikelihoodFit --saveShapes --saveWithUncertainties --setPhysicsModelParameterRanges r=-5,20 --setPhysicsModelParameters r=1 --customStartingPoint"%(sys.argv[2].split('/')[-1])
print "echo p-value on variable X \# combine %s.root -M HybridNew --testStat=PL --singlePoint 0 --rule=CLsplusb --redefineSignalPOIs X --freq -T 150 --fork 12 -i 10 --clsAcc 0"%(sys.argv[2].split('/')[-1])
print "echo multi-dim fit \# combine %s.root -M MultiDimFit --algo=singles"%(sys.argv[2].split('/')[-1])
print "echo limit obs. \(exp.\) \# combine %s.root -M Asymptotic \(-t -1 --expectSignal 1\)"%(sys.argv[2].split('/')[-1])
print "echo impacts 1 \# combineTool.py -M Impacts -d %s.root -m 125 --robustFit 1 --rMin -5 --rMax 10 --doInitialFit"%(sys.argv[2].split('/')[-1])
print "echo impacts 2 \# combineTool.py -M Impacts -d %s.root -m 125 --robustFit 1 --rMin -5 --rMax 10 --doFits --parallel 12"%(sys.argv[2].split('/')[-1])
print "echo impacts 3 \# combineTool.py -M Impacts -d %s.root -m 125 -o impacts.json"%(sys.argv[2].split('/')[-1])
print "echo impacts 4 \# plotImpacts.py -i impacts.json -o impacts --per-page 20 --unblind"


### for i in `cat catlist.txt | grep 2lss`; do python postFitPlots.py ttH-multilepton/mca-2lss-mcdata-frdata.txt ttH-multilepton/mca-2lss-mcdata-frdata.txt local/2lss_SR_data_frdata_b${i}/all/2lss_3l_plots.root kinMVA_2lss_bins combineUnblMar01/fits/standard/mlfit.root ttH_$i --lspam '#bf{CMS} #it{Preliminary}' --showMCError; done
### 
### for i in `cat catlist.txt | grep 3l`; do python postFitPlots.py ttH-multilepton/mca-3l-mcdata-frdata.txt ttH-multilepton/mca-3l-mcdata-frdata.txt local/3l_SR_data_frdata_b${i}/2lss_3l_plots.root kinMVA_3l_bins combineUnblMar01/fits/standard/mlfit.root ttH_$i --lspam '#bf{CMS} #it{Preliminary}' --showMCError; done

