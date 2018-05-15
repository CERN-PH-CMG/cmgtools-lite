export DATA=Fall17
export LABEL=ProdMay9

array=(
"crab_WJetsToLNu_LO_ProdMay9"
"crab_W1JetsToLNu_LO_ProdMay9"
"crab_W2JetsToLNu_LO_ProdMay9"
"crab_W3JetsToLNu_LO_ProdMay9"
"crab_W4JetsToLNu_LO_ProdMay9"
"crab_WW_ProdMay9"
"crab_WZ_ProdMay9"
"crab_ZZ_ProdMay9"
"crab_DYJetsToLL_M50_ProdMay9"
"crab_DYJetsToLL_M50_ext_ProdMay9"
"crab_DYJetsToLL_M50_LO_ProdMay9"
"crab_DYJetsToLL_M50_LO_ext_ProdMay9"
"crab_DYJetsToLL_M4to50_HT70to100_ProdMay9"
"crab_DYJetsToLL_M4to50_HT100to200_ProdMay9"
"crab_DYJetsToLL_M4to50_HT200to400_ProdMay9"
"crab_DYJetsToLL_M4to50_HT400to600_ProdMay9"
"crab_DYJetsToLL_M4to50_HT600toInf_ProdMay9"
"crab_DYJetsToLL_M50_HT100to200_ProdMay9"
"crab_DYJetsToLL_M50_HT200to400_ProdMay9"
"crab_DYJetsToLL_M50_HT400to600_ProdMay9"
"crab_DYJetsToLL_M50_HT600to800_ProdMay9"
"crab_DYJetsToLL_M50_HT800to1200_ProdMay9"
"crab_DYJetsToLL_M50_HT2500toInf_ProdMay9"
"crab_T_sch_lep_ProdMay9"
"crab_T_tch_ProdMay9"
"crab_TBar_tch_ProdMay9"
"crab_T_tWch_noFullyHad_ProdMay9"
"crab_TBar_tWch_noFullyHad_ProdMay9"
"crab_QCD_HT100to200_ProdMay9"
"crab_QCD_HT200to300_ProdMay9"
"crab_QCD_HT300to500_ProdMay9"
"crab_QCD_HT500to700_ProdMay9"
"crab_QCD_HT700to1000_ProdMay9"
"crab_QCD_HT1000to1500_ProdMay9"
"crab_QCD_HT1500to2000_ProdMay9"
"crab_QCD_HT2000toInf_ProdMay9"
"crab_TTGJets_ProdMay9"
"crab_TTWToLNu_fxfx_ProdMay9"
"crab_TTW_LO_ProdMay9"
"crab_TTZToLLNuNu_amc_ProdMay9"
"crab_TTZToLLNuNu_amc_psw_ProdMay9"
)

for i in "${array[@]}"; do
    crab resubmit --dir="$i"/"${i/${LABEL}}"${DATA}${LABEL}
done

