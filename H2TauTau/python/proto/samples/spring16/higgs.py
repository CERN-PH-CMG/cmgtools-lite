import copy
import re 
from CMGTools.RootTools.yellowreport.YRParser import yrparser13TeV
# from CMGTools.H2TauTau.proto.samples.sampleShift import sampleShift
from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator

creator = ComponentCreator()

HiggsGGH125 = creator.makeMCComponent('HiggsGGH125', '/GluGluHToTauTau_M125_13TeV_powheg_pythia8/RunIISpring16MiniAODv1-PUSpring16_80X_mcRun2_asymptotic_2016_v3-v1/MINIAODSIM', 'CMS', '.*root', 1.0)
# HiggsGGH130 = creator.makeMCComponent('HiggsGGH130', '/GluGluHToTauTau_M130_13TeV_powheg_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM', 'CMS', '.*root', 1.0)

# HiggsVBF120 = creator.makeMCComponent('HiggsVBF125', '/VBFHToTauTau_M120_13TeV_powheg_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM', 'CMS', '.*root', 1.0)
HiggsVBF125 = creator.makeMCComponent('HiggsVBF125', '/VBFHToTauTau_M125_13TeV_powheg_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM', 'CMS', '.*root', 1.0)
# HiggsVBF130 = creator.makeMCComponent('HiggsVBF125', '/VBFHToTauTau_M130_13TeV_powheg_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM', 'CMS', '.*root', 1.0)




HiggsTTH125 = creator.makeMCComponent('HiggsTTH125', '/ttHToTT_M125_13TeV_powheg_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM', 'CMS', '.*root', 1.0)


#############

mc_higgs_vbf = [
    HiggsVBF125,
    # HiggsVBFtoWW125,
]

mc_higgs_ggh = [
    HiggsGGH125,
    # HiggsGGHtoWW125,
]

mc_higgs_vh = [
    # HiggsVH125,
    # HiggsVHtoWW125
]

mc_higgs_tth = [
    HiggsTTH125
]

mc_higgs = copy.copy(mc_higgs_vbf)
mc_higgs.extend(mc_higgs_ggh)

mc_higgs.extend(mc_higgs_vh)
mc_higgs.extend(mc_higgs_tth)


pattern = re.compile('Higgs(\D+)(\d+)')
for h in mc_higgs:
    m = pattern.match( h.name )
    process = m.group(1)
    
    isToWW = False 
    isInclusive = False
    if 'toWW' in process :
        process = process.replace('toWW', '')
        isToWW = True
    if 'Inclusive' in process:
        process = process.replace('Inclusive', '')
        isInclusive = True
          
    mass = float(m.group(2))
    xSection = 0.
    try:
        if process == 'VH':
            xSection += yrparser13TeV.get(mass)['WH']['sigma']
            xSection += yrparser13TeV.get(mass)['ZH']['sigma']
        else:
            xSection += yrparser13TeV.get(mass)[process]['sigma']
    except KeyError:
        print 'Higgs mass', mass, 'not found in cross section tables. Interpolating linearly at +- 1 GeV...'
        if process=='VH':
            xSection += 0.5 * (yrparser13TeV.get(mass-1.)['WH']['sigma'] + xSection + yrparser13TeV.get(mass+1.)['WH']['sigma'])
            xSection += 0.5 * (yrparser13TeV.get(mass-1.)['ZH']['sigma'] + yrparser13TeV.get(mass+1.)['ZH']['sigma'])
        else:
            xSection += 0.5 * (yrparser13TeV.get(mass-1.)[process]['sigma'] + yrparser13TeV.get(mass+1.)[process]['sigma'])

    if isToWW :
        br = yrparser13TeV.get(mass)['H2B']['WW']
    elif isInclusive:
        br = 1.
    else :
        br = yrparser13TeV.get(mass)['H2F']['tautau']
      
    h.xSection = xSection*br
    h.branchingRatio = br
    print h.name, 'sigma*br =', h.xSection, 'sigma =', xSection, 'br =', h.branchingRatio

