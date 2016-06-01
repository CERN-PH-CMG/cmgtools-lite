from CMGTools.TTHAnalysis.treeReAnalyzer import *
import ROOT
import itertools
import PhysicsTools.Heppy.loadlibs
import pickle

# Directory for SFs
sfdir = "../python/tools/SFs/"

print 80*"#"
print "Initializing Btag SF"

# Basing on macro from Vienna
# https://github.com/HephySusySW/Workspace/blob/74X-master/RA4Analysis/cmgPostProcessing/btagEfficiency.py

# legacy 2012 BtagSFs
import PhysicsTools.Heppy.physicsutils.BTagSF

# Cuts for jets
minJpt = 30
maxJeta = 2.4
btagWP = 0.890

# pt, eta bins
ptBorders = [30, 40, 50, 60, 70, 80, 100, 120, 160, 210, 260, 320, 400, 500, 670]
ptBins = []
etaBins = [[0,0.8], [0.8,1.6], [ 1.6, 2.4]]

for i in range(len(ptBorders)-1):
    ptBins.append([ptBorders[i], ptBorders[i+1]])
    if i == len(ptBorders)-2:
        ptBins.append([ptBorders[i+1], -1])

def partonName (parton):
    if parton==5:  return 'b'
    if parton==4:  return 'c'
    return 'other'

### SF ROOT file
sfFname = sfdir+"btagSF_CSVv2.csv"

# load SFs from csv file
calib = ROOT.BTagCalibration("csvv2", sfFname)

# SF readers (from CMSSW)
sfReaders = { "Comb" : {}, "Mu" : {} }

sfReaders["Comb"]["Up"]      = ROOT.BTagCalibrationReader(calib, 1, "comb", "up")
sfReaders["Comb"]["Central"] = ROOT.BTagCalibrationReader(calib, 1, "comb", "central")
sfReaders["Comb"]["Down"]    = ROOT.BTagCalibrationReader(calib, 1, "comb", "down")
sfReaders["Mu"]["Up"]        = ROOT.BTagCalibrationReader(calib, 1, "mujets", "up")
sfReaders["Mu"]["Central"]   = ROOT.BTagCalibrationReader(calib, 1, "mujets", "central")
sfReaders["Mu"]["Down"]      = ROOT.BTagCalibrationReader(calib, 1, "mujets", "down")


def getSF2015(parton, pt, eta):

    flav = 2 # flavour for reader
    ptlim = 1000 # limit of pt range
    sftype = "Comb" # meas type of SF

    if abs(parton)==5: #SF for b
        flav = 0; ptlim = 669.9; sftype = "Mu"
    elif abs(parton)==4: #SF for c
        flav = 1; ptlim = 669.9; sftype = "Mu"
    else: # SF for light flavours
        flav = 2; ptlim = 999.9; sftype = "Comb"

    # read SFs
    sf   = sfReaders[sftype]["Central"].eval(flav, eta, min(pt,ptlim))
    sf_d = sfReaders[sftype]["Down"].eval(flav, eta, min(pt,ptlim))
    sf_u = sfReaders[sftype]["Up"].eval(flav, eta, min(pt,ptlim))

    # double uncertainty for out-of-range pt
    if pt > ptlim:
        # derived from c + 2*(d-c) = 2*d - c = d + (d-c)
        sf_d += sf_d - sf
        sf_u += sf_u - sf

    return {"SF":sf, "SF_down":sf_d,"SF_up":sf_u}

# MC eff  -- precomputed
bTagEffFile = sfdir+"btagMCeff.pck"
try:
  mcEffDict = pickle.load(file(bTagEffFile))
except IOError:
  print 'Unable to load MC efficiency file!'
  mcEffDict = False

print 80*"#"
print "Loaded btag mcEffDict with keys:", mcEffDict.keys()

def getMCEff(parton, pt, eta, mcEff, year = 2015):
    for ptBin in ptBins:
        if pt>=ptBin[0] and (pt<ptBin[1] or ptBin[1]<0):
            for etaBin in etaBins:
                if abs(eta)>=etaBin[0] and abs(eta)<etaBin[1]:
                    if year == 2015: res=getSF2015(parton, pt, eta)
                    else: res=getSF(parton, pt, eta, year)
                    if abs(parton)==5:                  res["mcEff"] = mcEff[tuple(ptBin)][tuple(etaBin)]["b"]
                    if abs(parton)==4:                  res["mcEff"] = mcEff[tuple(ptBin)][tuple(etaBin)]["c"]
                    if abs(parton)>5 or abs(parton)<4:  res["mcEff"] = mcEff[tuple(ptBin)][tuple(etaBin)]["other"]
                    return res
    return {} #empty if not found

############ METHOD 1b ##################
## https://twiki.cern.ch/twiki/bin/view/CMS/BTagSFMethods#1b_Event_reweighting_using_scale

# get MC efficiencies and scale factors for all jets of one event, uses getMCEff
def getMCEfficiencyForBTagSF(event, mcEff, onlyLightJetSystem = False, isFastSim = False):

    # jets from event collection
    cjets = [j for j in Collection(event,"Jet","nJet")]
    cjets30 = [j for j in Collection(event,"Jet","nJet") if (j.pt > minJpt and abs(j.eta) < maxJeta and j.id)]

    jets = [] # list of jets for bTagSF

    for jet in cjets30:
       jPt     = jet.pt
       jEta    = jet.eta
       # hadronFlavour is recommended by BTAG POG
       jParton = jet.hadronFlavour if hasattr(jet,"hadronFlavour") else jet.mcFlavour
       #if hasattr(jet,"hadronFlavour"):
       #    print jParton, jet.hadronFlavour, jet.mcFlavour
       #jParton = jet.mcFlavour

       if jPt <= minJpt or abs(jEta) >=maxJeta or (not jet.id): continue

       if onlyLightJetSystem:
           if jet.btagCSV > btagWP: continue
           jParton=1

       jets.append([jParton, jPt, jEta])

    # set jParton to 4 for a random jet
    if onlyLightJetSystem and len(jets)>0:
        nc = randint(0, len(jets)-1)
        jets[nc][0] = 4

    # append corresp. jet bTag MC eff
    for jet in jets:
        jParton, jPt, jEta = jet
        r = getMCEff(jParton, jPt, jEta, mcEff, 2015) #getEfficiencyAndMistagRate(jPt, jEta, jParton )
        jet.append(r)

    if len(jets) != len(cjets30):
        print "!! Different number of jets:", len(jets), 'vs', len(cjets)
        return 0

    # Compute and apply the SFs

    #effNames = ['','SF','SF_b_Up','SF_b_Down','SF_light_Up','SF_light_Down']
    #mcEffs = {name:tuple() for name in effNames}

    mceffs = tuple()
    mceffs_SF = tuple()
    mceffs_SF_b_Up = tuple()
    mceffs_SF_b_Down = tuple()
    mceffs_SF_light_Up = tuple()
    mceffs_SF_light_Down = tuple()

    for jParton, jPt, jEta, r in jets:
        if isFastSim:
            fsim_SF = ROOT.getFastSimCorr(partonName(abs(jParton)),jPt,"mean",jEta)
            fsim_SF_up = ROOT.getFastSimCorr(partonName(abs(jParton)),jPt,"up",jEta)
            fsim_SF_down = ROOT.getFastSimCorr(partonName(abs(jParton)),jPt,"down",jEta)
        else:
            fsim_SF = 1.
            fsim_SF_up = 1.
            fsim_SF_down = 1.
        mceffs += (r["mcEff"],)
        mceffs_SF += (r["mcEff"]*r["SF"]*fsim_SF,)
        if abs(jParton)==5 or abs(jParton)==4:
            mceffs_SF_b_Up   += (r["mcEff"]*r["SF_up"]*fsim_SF_up,)
            mceffs_SF_b_Down += (r["mcEff"]*r["SF_down"]*fsim_SF_down,)
            mceffs_SF_light_Up   += (r["mcEff"]*r["SF"],)
            mceffs_SF_light_Down += (r["mcEff"]*r["SF"],)
        else:
            mceffs_SF_b_Up   += (r["mcEff"]*r["SF"],)
            mceffs_SF_b_Down += (r["mcEff"]*r["SF"],)
            mceffs_SF_light_Up   += (r["mcEff"]*r["SF_up"]*fsim_SF_up,)
            mceffs_SF_light_Down += (r["mcEff"]*r["SF_down"]*fsim_SF_down,)

    return {"mceffs":mceffs, "mceffs_SF":mceffs_SF, "mceffs_SF_b_Up":mceffs_SF_b_Up, "mceffs_SF_b_Down":mceffs_SF_b_Down, "mceffs_SF_light_Up":mceffs_SF_light_Up, "mceffs_SF_light_Down":mceffs_SF_light_Down}
    #return mcEffs

# get the tag weights for the efficiencies calculated with getMCEfficiencyForBTagSF
def getTagWeightDict(effs, maxNBtagsForWeight):
    zeroTagWeight = 1.
    for e in effs:
        zeroTagWeight*=(1-e)
    tagWeight={}
    for i in range(min(len(effs), maxNBtagsForWeight)+1):
        tagWeight[i]=zeroTagWeight
        twfSum = 0.
        for tagged in itertools.combinations(effs, i):
            twf=1.
            for fac in [x/(1-x) for x in tagged]:
                twf*=fac
            twfSum+=twf
#            print "tagged",tagged,"twf",twf,"twfSum now",twfSum
        tagWeight[i]*=twfSum
#    print "tagWeight",tagWeight,"\n"
    for i in range(maxNBtagsForWeight+1):
        if not tagWeight.has_key(i):
            tagWeight[i] = 0.
    return tagWeight

############ METHOD 1a ##################
## https://twiki.cern.ch/twiki/bin/view/CMS/BTagSFMethods#1a_Event_reweighting_using_scale

# To be implemented
def getBTagWeight(event, mcEff, isFastSim = False):

    # jets from event collection: central w pt > 30 GeV
    cjets30 = [j for j in Collection(event,"Jet","nJet") if (j.pt > minJpt and abs(j.eta) < maxJeta and j.id)]
    jets = [] # list of jets for bTagSF

    for jet in cjets30:
       jPt     = jet.pt
       jEta    = jet.eta
       jParton = jet.hadronFlavour if hasattr(jet,"hadronFlavour") else jet.mcFlavour

       if jPt <= minJpt or abs(jEta) >=maxJeta or (not jet.id): continue

       isBtagged = False
       jPt     = jet.pt
       jEta    = jet.eta
       jParton = jet.hadronFlavour if hasattr(jet,"hadronFlavour") else jet.mcFlavour
       jBTagCSV = jet.btagCSV

       if jBTagCSV > btagWP: isBtagged = True
       jets.append([jParton, jPt, jEta, isBtagged])

    PMC = 1.
    PData = 1.
    PData_b_up = 1.
    PData_b_down = 1.
    PData_l_up = 1.
    PData_l_down = 1.

    for jParton, jPt, jEta, isBtagged in jets:
        r = getMCEff(jParton, jPt, jEta, mcEff, 2015)#getEfficiencyAndMistagRate(jPt, jEta, jParton )
        if isFastSim:
            fsim_SF = ROOT.getFastSimCorr(partonName(abs(jParton)),jPt,"mean",jEta)
            fsim_SF_up = ROOT.getFastSimCorr(partonName(abs(jParton)),jPt,"up",jEta)
            fsim_SF_down = ROOT.getFastSimCorr(partonName(abs(jParton)),jPt,"down",jEta)
        else:
            fsim_SF = 1.
            fsim_SF_up = 1.
            fsim_SF_down = 1.
        if isBtagged:
            PMC *= r['mcEff']
            PData *= r['mcEff']*r['SF']
            if abs(jParton)==5 or abs(jParton)==4:
                PData_b_up *= r['mcEff']*r['SF_up']
                PData_b_down *= r['mcEff']*r['SF_down']
                PData_l_up *= r['mcEff']*r['SF']
                PData_l_down *= r['mcEff']*r['SF']
            else:
                PData_b_up *= r['mcEff']*r['SF']
                PData_b_down *= r['mcEff']*r['SF']
                PData_l_up *= r['mcEff']*r['SF_up']
                PData_l_down *= r['mcEff']*r['SF_down']
        else:
            PMC *= (1. - r['mcEff'])
            PData *= (1. - r['mcEff']*r['SF'])
            if abs(jParton)==5 or abs(jParton)==4:
                PData_b_up *=   (1 - r['mcEff']*r['SF_up'])
                PData_b_down *= (1 - r['mcEff']*r['SF_down'])
                PData_l_up *=   (1 - r['mcEff']*r['SF'])
                PData_l_down *= (1 - r['mcEff']*r['SF'])
            else:
                PData_b_up *=   (1 - r['mcEff']*r['SF'])
                PData_b_down *= (1 - r['mcEff']*r['SF'])
                PData_l_up *=   (1 - r['mcEff']*r['SF_up'])
                PData_l_down *= (1 - r['mcEff']*r['SF_down'])
            #PData_up *= (1 - r['mcEff']*r['SF_up'])
            #PData_down *= (1 - r['mcEff']*r['SF_down'])
    #res = {'w':PData/PMC, 'w_b_up':PData_b_up/PMC, 'w_b_down':PData_b_down/PMC, 'w_l_up':PData_l_up/PMC, 'w_l_down':PData_l_down/PMC}
    #return res
    return {'btagSF':PData/PMC, 'btagSF_b_up':PData_b_up/PMC, 'btagSF_b_down':PData_b_down/PMC, 'btagSF_l_up':PData_l_up/PMC, 'btagSF_l_down':PData_l_down/PMC}

branches1a = [ 'btagSF_l_down', 'btagSF_l_up', 'btagSF_b_down', 'btagSF_b_up', 'btagSF']

# Flags
isFastSim = False # calc FastSim SFs
maxNBtagsForWeight = 2 # Max nBJet-1 to calculate the b-tag weight for

# Names of btag SF variations
sfnames = ['','_SF','_SF_b_Up','_SF_b_Down','_SF_light_Up','_SF_light_Down']
#sfnames = ['_SF']

# AutoDefine branches1b
branches1b = []
for name in sfnames:
    for i in range(1, maxNBtagsForWeight+2):
        branches1b.append('btagW_'+str(i)+'p'+name)
    for i in range(maxNBtagsForWeight+1):
        branches1b.append('btagW_'+str(i)+name)

print "Branches to save for bTag Weights (1b):"
print branches1b
print 80*"#"
print

def getSampKey(name):

    #if "TTJets" in name: return "TTJets"
    if "TT" in name: return "TTJets"
    elif "SingleT" in name: return "TTJets"
    elif "WJets" in name: return "WJets"
    elif "DY" in name: return "WJets"
    else: return "TTJets"

class EventVars1L_btagSF:
    def __init__(self):
        self.branches = branches1b + branches1a
        self.sample = "none" #default sample for mcEff

    def listBranches(self):
        return self.branches[:]

    def __call__(self,event,base):

        sample = getSampKey(self.sample)

        # output dict:
        ret = {}

        # don't run on data
        if event.isData: return ret

        # for signal use FastSim corrections
        if "T1tttt" in self.sample: isFastSim == True

        ################################################################
        ######### METHOD 1A ### ~SFs ###################################
        ################################################################

        btagSFs = getBTagWeight(event,mcEffDict[sample],isFastSim)
        for btagSF in btagSFs: ret[btagSF] = btagSFs[btagSF]

        ################################################################
        ######### METHOD 1B ### ~ Weights ##############################
        ################################################################

        # get nJets w pt > 30 and eta < 2.4
        cjets30 = [j for j in Collection(event,"Jet","nJet") if (j.pt > minJpt and abs(j.eta) < maxJeta and j.id)]

        # Get MC efficiencies for this event
        if sample in mcEffDict:
            mceff = getMCEfficiencyForBTagSF(event, mcEffDict[sample], isFastSim = isFastSim)
        else: return ret
        if not mceff: return ret

        # Fill weights into dict
        mcEffWs = {}
        for name in sfnames:
            #if name != "": sfname = "mceffs_" + name
            #else: sfname = "mceffs"
            sfname = "mceffs"+name

            # get weights for config
            #mcEffWs[sfname] = getTagWeightDict(mceff[sfname], maxNBtagsForWeight)
            mcEffW = getTagWeightDict(mceff[sfname], maxNBtagsForWeight)

            bW = 1
            # for inclusive Nb weights
            for i in range(1, maxNBtagsForWeight+2):
                ret['btagW_'+str(i)+'p'+name] = bW
            # weights for exclusive Nb
            for i in range(maxNBtagsForWeight+1):
                ret['btagW_'+str(i)+name] = bW*mcEffW[i]
                # weights for inclusive Nb
                for j in range(i+1, maxNBtagsForWeight+2):
                    ret['btagW_'+str(j)+'p'+name] -= bW*mcEffW[i] #prob. for >=j b-tagged jets

            # set W to 0 if nJets < maxConsBTW
            for i in range (len(cjets30)+1, maxNBtagsForWeight+1):
                ret['btagW_'+str(i)+name] = 0

        #print ret

        # return branches
        return ret

if __name__ == '__main__':
    from sys import argv
    file = ROOT.TFile(argv[1])
    tree = file.Get("tree")
    class Tester(Module):
        def __init__(self, name):
            Module.__init__(self,name,None)
            self.sf = EventVars1L()
        def analyze(self,ev):
            print "\nrun %6d lumi %4d event %d: leps %d" % (ev.run, ev.lumi, ev.evt, ev.nLepGood)
            print self.sf(ev)
    el = EventLoop([ Tester("tester") ])
    el.loop([tree], maxEvents = 50)
