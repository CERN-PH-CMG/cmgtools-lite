## addWeight = adds another factor to the weight expression in the fake rate file
## replace   = string replacement of any occurrence in the string

## the template MCA file
mcafile = "susy-ewkino/3l/mca_ewkino.txt"

## dictionaries giving replacements (search for key, replace by value, give {label} to write "Up" or "Dn", put "0" as key for single statement)
jecDict = {"nJet30_Mini"       : "nJet30_jec{label}_Mini"       , \
           "htJet30j_Mini"     : "htJet30j_jec{label}_Mini"     , \
           "nBJetMedium25_Mini": "nBJetMedium25_jec{label}_Mini"}
ewkDict = {"FR_wpsMiX4mrE2_el_QCDEl_ptJIMIX4_mvaSusy_sMi": "FR_wpsMiX4mrE2_el_QCDEl_ptJIMIX4_mvaSusy_sMi", \
           "FR_wpsMiX4mrE2_mu_QCDMu_ptJIMIX4_mvaSusy_sMi": "FR_wpsMiX4mrE2_mu_QCDMu_ptJIMIX4_mvaSusy_sMi"} 
bTagLightDict = {"0": "btagMediumSF_Light{label}_Mini/btagMediumSF_Mini"}
bTagBCDict    = {"0": "btagMediumSF_BC{label}_Mini/btagMediumSF_Mini"}

## the systematic variations to be applied
## parameters: name, longname, list of processes, fakerate file to vary, action (replace or addWeight), the dictionary
var = [
       Variation("jec"      , "JEC"            , ["prompt", "sig"]             , "fakerate_standard", "replace"  , jecDict      ), 
       Variation("ewk"      , "EWK SUBTRACTION", ["fakeappl_data", "promptsub"], "fakerate_fakeappl", "replace"  , ewkDict      ), 
       Variation("bTagLight", "BTAG LIGHT"     , ["prompt", "sig"]             , "fakerate_standard", "addWeight", bTagLightDict), 
       Variation("bTagBC"   , "BTAG CB"        , ["prompt", "sig"]             , "fakerate_standard", "addWeight", bTagBCDict   ), 
      ]




## --------------- do not touch beyond this line ---------------

class Variation:
	def __init__(self, name, longname, tags, frfile, action, theDict = {}):
		self.name     = name
		self.longname = longname.upper()
		self.tags     = tags
		self.frfile   = frfile
		self.action   = action
		self.theDict  = theDict
	def match(self, line):
		for t in self.tags:
			if line.find(t) > -1: return True
		return False
	def getFakeRateFiles(self, line):
		if line.find("FakeRate") == -1: return []
		FakeRateString = line[line.find("FakeRate=\"")+10:]
		FakeRateString = FakeRateString[0:FakeRateString.find(",")-1]
		return FakeRateString.split(",")
	def apply(self, line, label = "Up")
		oldfakerates = self.getFakeRateFiles(line)
		newfakerates = makeFakeRateFiles(oldfakerates,label)
		oldfakerates = "\,".join(oldfakerates)
		newfakerates = "\,".join(newfakerates)
		sl = line.split(":")
		newline = sl[0].strip() + "_" + self.name + label + "  :" + ":".join(sl[1:]) 
		newline = newline.replace("FakeRate=\"" + oldfakerates + "\"", "FakeRate=\"" + newfakerates + "\"")
		return newline
	def makeFakeRateFiles(self, files, label):
		if len(files) == 0: return []
		newfiles = []
		for frf in files:
			if frf.find(frfile) == -1: newfiles.append(frf); continue
			new = frf.replace(frfile + "_central", frfile + "_" + label)
			self.makeFakeRate(frf, new, label)
			newfiles.append(new)
		return newfiles			
	def makeFakeRate(self, old, new, label = "Up"):
		ff = open(old, "r")
		theLines = ff.readlines()
		ff.close()
		ff = open(new, "w")
		ff.write("".join(self.applyOnFakeRate(theLines, label)))
		ff.close()
	def applyOnFakeRate(self, lines, label = "Up"):
		if self.action == "replace":
			newlines = []
			for l in lines:
				nl  = l
				for k,v in self.theDict.iteritems()
					nl = nl.replace(k, v.format(label=label))
				newlines.append(nl)
			return newlines
		if self.action == "addWeight":
			newlines = []
			for l in lines:
				nl = l
				sl = l.strip().split(":")
				if sl[0].strip() == "weight": 
					sl[1] = sl[1].strip() += "*" + self.theDict["0"]
					nl = ":".join(sl)
				newlines.append(nl)
			return newlines
		return lines


f = open(mcafile, "r")
mca = f.readlines()
f.close()

f = open(mcafile.rstrip(".txt") + "_withAutomSyst.txt", "w")
f.write("".join(mca))

for v in vars:
	for d in ["Up", "Dn"]:
		f.write("\n\n")
		f.write("## AUTOMATIC SYSTEMATIC VARIATION: " + v.longname + "\n")
		f.write("## ===========================================================\n")
	
		for line in mca:
			if not v.match(line): continue			
			f.write(v.apply(line, d))

f.close()

