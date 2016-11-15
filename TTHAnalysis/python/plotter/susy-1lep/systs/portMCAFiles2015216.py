#!/usr/bin/env python
from CMGTools.TTHAnalysis.plotter.mcAnalysis import *

class ReplaceLogic:
    def __init__(self, replaceComponent="", specificReplaceWeight=["old","old"], commentOut=False):
        self.nC=replaceComponent
        if len(specificReplaceWeight)!=2:
            print "invalid specificReplaceWeight, exiting"
            exit()
        self.oW=specificReplaceWeight[0]
        self.nW=specificReplaceWeight[1]
        self.co=commentOut


collectGlobalReplacements = []
#add here and then just execute all of them in the replacement part
#globalReplacements

replaceScaleFactorGlobal=["0.94","TriggEff"]
#replaceScaleFactorGlobal=["xsec*lepSF*0.94*btagSF","xsec*1"]
#replaceScaleFactorGlobal=["xsec*lepSF*TopPtWeight*0.94*btagSF","xsec*1*TopPtWeight"]
#replaceScaleFactorGlobal=["lepSF*0.94*btagSF*TopPtWeight","1*TopPtWeight"]
assert len(replaceScaleFactorGlobal)==2
replacenGenLepStuff=["ngenTau+ngenLep"," Sum$(abs(genTau_grandmotherId)==6&&abs(genTau_motherId)==24)+Sum$(abs(genLep_grandmotherId)==6&&abs(genLep_motherId)==24)"]
assert len(replacenGenLepStuff)==2

componentDict={}
# "#" means no change
componentDict["TTJets_LO"]=ReplaceLogic(commentOut=True)
componentDict["TTJets_DiLepton"]=ReplaceLogic(replaceComponent="TTJets_DiLept")
componentDict["TTJets_SingleLepton"]=ReplaceLogic(replaceComponent="TTJets_SingleLeptFromT;TTJets_SingleLeptFromTbar",specificReplaceWeight=["2*",""])
componentDict["TTJets_LO_HT600to800"]=ReplaceLogic(replaceComponent="TTJets_HT-600to800")
componentDict["TTJets_LO_HT800to1200"]=ReplaceLogic(replaceComponent="TTJets_HT-800to1200")
componentDict["TTJets_LO_HT1200to2500"]=ReplaceLogic(replaceComponent="TTJets_HT-1200to2500")
componentDict["TTJets_LO_HT2500toInf"]=ReplaceLogic(replaceComponent="TTJets_HT-2500toInf")

componentDict["WJetsToLNu_HT100to200"]=ReplaceLogic(replaceComponent="WJetsToLNu_HT-100To200",commentOut=True)
componentDict["WJetsToLNu_HT200to400"]=ReplaceLogic(replaceComponent="WJetsToLNu_HT-200To400")
componentDict["WJetsToLNu_HT400to600"]=ReplaceLogic(replaceComponent="WJetsToLNu_HT-400To600")
componentDict["WJetsToLNu_HT600to800"]=ReplaceLogic(replaceComponent="WJetsToLNu_HT-600To800")
componentDict["WJetsToLNu_HT800to1200"]=ReplaceLogic(replaceComponent="WJetsToLNu_HT-800To1200")
componentDict["WJetsToLNu_HT1200to2500"]=ReplaceLogic(replaceComponent="WJetsToLNu_HT-1200To2500")
componentDict["WJetsToLNu_HT2500toInf"]=ReplaceLogic(replaceComponent="WJetsToLNu_HT-2500ToInf")


componentDict["TToLeptons_tch_amcatnlo"]=ReplaceLogic(replaceComponent="ST_t-channel_antitop_4f_leptonDecays_13TeV-powheg-pythia8;ST_t-channel_antitop_4f_leptonDecays_13TeV-powheg-pythia8") #use the antitop sample twice, change to POWHEG
componentDict["TToLeptons_sch"]=ReplaceLogic(replaceComponent="ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8")
componentDict["T_tWch"]=ReplaceLogic(replaceComponent="ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8")
componentDict["TBar_tWch"]=ReplaceLogic(replaceComponent="ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8")

componentDict["DYJetsToLL_M50_HT100to200"]=ReplaceLogic(replaceComponent="DYJetsToLL_M-50_HT-100to200")
componentDict["DYJetsToLL_M50_HT200to400"]=ReplaceLogic(replaceComponent="DYJetsToLL_M-50_HT-200to400")
componentDict["DYJetsToLL_M50_HT400to600"]=ReplaceLogic(replaceComponent="DYJetsToLL_M-50_HT-400to600")
componentDict["DYJetsToLL_M50_HT600toInf"]=ReplaceLogic(replaceComponent="DYJetsToLL_M-50_HT-600toInf")


componentDict["TTWToLNu"]=ReplaceLogic(replaceComponent="TTWJetsToLNu")
componentDict["TTWToQQ"]=ReplaceLogic(replaceComponent="TTWJetsToQQ")
#componentDict["TTZToLLNuNu"]=ReplaceLogic(replaceComponent="TTZToLLNuNu")
componentDict["TTZToQQ"]=ReplaceLogic(replaceComponent="",commentOut=True)

#componentDict["QCD_HT300to500"]=ReplaceLogic(replaceComponent="")
#componentDict["QCD_HT500to700"]=ReplaceLogic(replaceComponent="")
#componentDict["QCD_HT700to1000"]=ReplaceLogic(replaceComponent="")
#componentDict["QCD_HT1000to1500"]=ReplaceLogic(replaceComponent="")
#componentDict["QCD_HT1500to2000"]=ReplaceLogic(replaceComponent="")
#componentDict["QCD_HT2000toInf"]=ReplaceLogic(replaceComponent="")

componentDict["SingleElectron_Run2015D_05Oct"]=ReplaceLogic(replaceComponent="SingleElectron_Run2016B_PromptReco_v2")
componentDict["SingleMuon_Run2015D_05Oct"]=ReplaceLogic(replaceComponent="SingleMuon_Run2016B_PromptReco_v2")
componentDict["SingleElectron_Run2015D_v4"]=ReplaceLogic(commentOut=True)
componentDict["SingleMuon_Run2015D_v4"]=ReplaceLogic(commentOut=True)


#componentDict[""]=ReplaceLogic(replaceComponent="")



class Process:
    def __init__(self, tty):
        self.tty = tty
    def doReplacements(self, line):
        #replace globalScaleFactor
        line=line.replace(replaceScaleFactorGlobal[0],replaceScaleFactorGlobal[1])
        #replace replacenGenLepStuff
        line=line.replace(replacenGenLepStuff[0],replacenGenLepStuff[1])
        #skip further steps if component name not in dictionary (i.e. change only weights)
        if self.tty._cname not in componentDict:
            return line
        #check for exact match of ._cname
        field = [f.strip() for f in line.split(':')]
        if len(field)>1 and field[1]!=self.tty._cname: return ""
#        print "going to replace something..."
        #comment out component
        if componentDict[self.tty._cname].co:
            print line
            line = (("#"+line).replace("\n","\n#"))[:-1]
        #replace component name
        splitComponents = componentDict[self.tty._cname].nC.split(";")
        if len(splitComponents)>1 and componentDict[self.tty._cname].nC!="":
            temp=""
            for split in splitComponents: temp=temp+line.replace(self.tty._cname,split)
            line=temp
        elif componentDict[self.tty._cname].nC!="": line = line.replace(self.tty._cname,componentDict[self.tty._cname].nC)
        #replace specificReplaceWeight
        if len(field)>2:
            line=line.replace(field[2],field[2].replace(componentDict[self.tty._cname].oW,componentDict[self.tty._cname].nW))
        return line
class ProcessSummary:
    def __init__(self):
        self.allProcesses = []
    def add(self, tty):
        self.allProcesses.append(Process(tty))
    def returnLines(self, line):
        for p in self.allProcesses:
            if p.tty._name in line and p.tty._cname in line:
                checkResult = p.doReplacements(line)
                if checkResult!="": return checkResult
                else: print "ambiguous match", p.tty._cname, line
        print "return unchanged line..."
        return line




if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser(usage="%prog [options] inputmca.txt outputmca.txt")
    addMCAnalysisOptions(parser)
    (options, args) = parser.parse_args()
    tty = MCAnalysis(args[0],options)
    print args[0]
    samples = args[0]
    fullFile = open(samples,'r')
    print args[1]
    outputMCA = args[1]
    outf = open(outputMCA, 'w')


    summary=ProcessSummary()
#    for line in fullFile: print line,
    for process in tty.listProcesses():
        print process
        for c in tty._allData[process]: summary.add(c)

#    for p in summary.allProcesses: print p
#        for c in tty._allData[process]: print c._cname,
#        print

    #    for i, line in enumerate(open(samples,'r')):
    #        print line,


    for line in fullFile:
        outf.write(summary.returnLines(line))
