
#python susy-interface/accmaker.py 3l 3lA /mnt/t3nfs01/data01/shome/cheidegg/o/2016-07-13_ewkskims80X $WWW/heppy/2016-09-15_sigAcc20Vtx -l 12.9 -o below20 --flags '-A alwaystrue nVert "nVert<20" -X blinding --uf' -p TChiNeuSlepSneuFD_1000_1 -p TChiNeuSlepSneuFD_500_475 -p TChiNeuSlepSneuFD_300_100 -p TChiNeuWZ_250_100 -p TChiNeuWZ_200_100 -p TChiNeuWZ_400_1
#python susy-interface/accmaker.py 3l 3lA /mnt/t3nfs01/data01/shome/cheidegg/o/2016-07-13_ewkskims80X $WWW/heppy/2016-09-15_sigAcc20Vtx -l 12.9 -o above20 --flags '-A alwaystrue nVert "nVert>=20" -X blinding --uf' -p TChiNeuSlepSneuFD_1000_1 -p TChiNeuSlepSneuFD_500_475 -p TChiNeuSlepSneuFD_300_100 -p TChiNeuWZ_250_100 -p TChiNeuWZ_200_100 -p TChiNeuWZ_400_1
python susy-interface/accmaker.py 3l 3lF /mnt/t3nfs01/data01/shome/cheidegg/o/2016-07-13_ewkskims80X $WWW/heppy/2016-09-15_sigAcc20Vtx -l 12.9 -o below20 --flags '-A alwaystrue nVert "nVert<20" -X blinding --uf' -p TChiNeuSlepSneuTD_300_50 -p TChiNeuSlepSneuTD_200_175 -p TChiNeuSlepSneuTD_500_1
python susy-interface/accmaker.py 3l 3lF /mnt/t3nfs01/data01/shome/cheidegg/o/2016-07-13_ewkskims80X $WWW/heppy/2016-09-15_sigAcc20Vtx -l 12.9 -o above20 --flags '-A alwaystrue nVert "nVert>=20" -X blinding --uf' -p TChiNeuSlepSneuTD_300_50 -p TChiNeuSlepSneuTD_200_175 -p TChiNeuSlepSneuTD_500_1



