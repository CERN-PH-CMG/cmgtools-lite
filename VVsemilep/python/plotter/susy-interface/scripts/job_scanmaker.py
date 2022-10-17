import os, copy, ROOT

## DO NOT TOUCH: THIS IS GOING TO BE CHANGED BY THE BATCH SUBMISSION
name     = "THENAME"
sig      = "THESIGNAL"
mass1    = "THEMASS1"
mass2    = "THEMASS2"
offset   = int("THEOFFSET")
file     = "THEFILE"
xs       = THEXS
q2file   = "THEQ2FILE"
q2syntax = "THEQ2SYNTAX"
wstr     = "THEWEIGHTSTR"
frfiles  = THEFRFILES
thejec   = "THEJEC" # name of the jec in the systs file
themet   = "THEMET" # name of the met in the systs file
q2acc    = "THEQ2ACC" # name of the q2acc in the systs file
frjec    = THEFRJEC # central, jecUp, jecDn
wvjec    = THEWVJEC # central, jecUp, jecDn
frmet    = THEFRMET # pfMET, genMET
wvmet    = THEWVMET # pfMET, genMET
wVars    = THEWEIGHTVARS
bkgdir   = "THEBKGDIR"
mcadir   = "THEMCADIR"
outdir   = "THEOUTDIR"
themca   = "THEMCA"
thesyst  = "THESYST"
#first    = "THECMDFIRST"
#second   = "THECMDSECOND"
thebase  = "THEBASE"

## ---------

def cmd(cmd):
	print cmd
	os.system(cmd)

def cp(location, destination):
	cmd("cp " + location + " " + destination)

def mkdir(path):
	if os.path.isdir(path): return
	cmd("mkdir -p " + path)

def makeFakeRate(thefrfiles, more = [], index = 0):
	myfrfiles = copy.deepcopy(thefrfiles)
	if len(more) > 0 and index > 0:
		if more[0]:
			myfrfiles = [x if x != more[0] else more[index] for x in myfrfiles]
		else:
			myfrfiles.append(more[index])
	myfrfiles = filter(None, myfrfiles)
	if len(myfrfiles) == 0: return ""
	return ", FakeRate=\"" + "\,".join(myfrfiles) + "\""

def div(num, den):
	if den==0: return 1
	return float(num)/den

def doMetVariation(infile, outfile, sig, jec, met, wVars):
	global mass1, mass2, q2file, q2syntax, q2acc
	## Q2ACC
	if q2file:
		f       = ROOT.TFile.Open(q2file, "read")
		dmass1=mass1; dmass2=mass2
		if dmass1 == "127": dmass1="150" # FIXME: something TChiNeuWH dependent!
		if dmass1 == "150" and dmass2=="24": dmass2="1"
		theq2Up = f.Get(q2syntax.replace("[m1]",dmass1).replace("[m2]",dmass2).replace("[var]","Up")).Clone()
		theq2Dn = f.Get(q2syntax.replace("[m1]",dmass1).replace("[m2]",dmass2).replace("[var]","Dn")).Clone()
		q2UpFull = copy.deepcopy(theq2Up)
		q2DnFull = copy.deepcopy(theq2Dn)
	## retrieve all histograms
	f = ROOT.TFile.Open(infile, "read")
	pfMET  = f.Get("x_sig_{s}_pfMET" .format(s=sig))
	genMET = f.Get("x_sig_{s}_genMET".format(s=sig))
	jecUp  = f.Get("x_sig_{s}_{j}_Up".format(s=sig, j=jec))
	jecDn  = f.Get("x_sig_{s}_{j}_Dn".format(s=sig, j=jec))
	wvHist = {}
	for key, vals in wVars.iteritems():
		wvHist[key + "Up"] = f.Get("x_sig_{s}_{j}_Up".format(s=sig, j=key))
		wvHist[key + "Dn"] = f.Get("x_sig_{s}_{j}_Dn".format(s=sig, j=key))
	final  = pfMET.Clone("x_sig_{s}"       .format(s=sig))
	metUp  = pfMET.Clone("x_sig_{s}_{m}_Up".format(s=sig, m=met))
	metDn  = pfMET.Clone("x_sig_{s}_{m}_Dn".format(s=sig, m=met))
	if q2file:
		q2Up   = pfMET.Clone("x_sig_{s}_{q}_Up".format(s=sig, q=q2acc))
		q2Dn   = pfMET.Clone("x_sig_{s}_{q}_Dn".format(s=sig, q=q2acc))
	## change naming and stuff
	final.Reset()
	metUp.Reset()
	metDn.Reset()
	## build the q2 variation
	if q2file:
		q2Up .Reset()
		q2Dn .Reset()
		for bin in range(1,q2Up.GetNbinsX()+1): 
			q2Up.SetBinContent(bin, q2UpFull.GetBinContent(bin+offset))
			q2Dn.SetBinContent(bin, q2DnFull.GetBinContent(bin+offset))
	## do the correction
	for bin in range(1,final.GetNbinsX()+1):
		diff = abs(pfMET.GetBinContent(bin)-genMET.GetBinContent(bin))/2
		avg  = float(pfMET.GetBinContent(bin)+genMET.GetBinContent(bin))/2
		sf   = div(avg, pfMET.GetBinContent(bin))
		final   .SetBinContent(bin, avg     )
		final   .SetBinError  (bin, diff    )
		if q2file:
			q2Up    .SetBinContent(bin, avg * q2Up.GetBinContent(bin)/100.*sf)
			q2Dn    .SetBinContent(bin, avg * q2Dn.GetBinContent(bin)/100.*sf)
		metUp   .SetBinContent(bin, avg+diff)
		metDn   .SetBinContent(bin, avg-diff)
		jecUp   .SetBinContent(bin, jecUp   .GetBinContent(bin)*sf)
		jecDn   .SetBinContent(bin, jecDn   .GetBinContent(bin)*sf)
		for key, vals in wVars.iteritems():
			wvHist[key + "Up"].SetBinContent(bin, wvHist[key + "Up"].GetBinContent(bin)*sf)
			wvHist[key + "Dn"].SetBinContent(bin, wvHist[key + "Dn"].GetBinContent(bin)*sf)
	## write all to output file
	ff = ROOT.TFile.Open(outfile, "recreate")
	ff.cd()
	final   .Write()
	if q2file:
		q2Up    .Write()
		q2Dn    .Write()
	metUp   .Write()
	metDn   .Write()
	jecUp   .Write()
	jecDn   .Write()
	for key, vals in wVars.iteritems():
		wvHist[key + "Up"].Write()
		wvHist[key + "Dn"].Write()
	ff.Close()

def plugFiles(dirs):
	return " ".join(["--infile {d}".format(d=thedir) for thedir in dirs])

def makeWeight(wstr, wvar):
	if not wvar: return wstr
	if wvar == "1": return wstr
	return "("+wstr+")*"+wvar

cmdbase = thebase.replace("{","[[").replace("}","]]")
cmdbase = cmdbase.replace("[[[","{").replace("]]]","}")
#cmdbase = "python {sc} {{MCA}} {FIRST} {{SYSTS}} --od {{OUTDIR}} ".format(sc=script, FIRST=first)
mcabase = "sig_{{name}} : {file} : {xs} : {{ws}} ; Label=\"{{name}}\"{{FRfiles}}".format(file=file, xs=xs)

short = mass1 + "_" + mass2
accdir = outdir + "/acc/" + short
mpsdir = outdir + "/mps/" + short
mkdir(mcadir)
mkdir(outdir)
mkdir(accdir)
mkdir(mpsdir)


## first loop on pfMET and genMET, and the JEC
if len(frmet)==2:
	f = open(mcadir + "/mca_acc_"+name+".txt", "w")
	f.write(mcabase.format(name=sig+"_pfMET"           , ws=wstr                      , FRfiles=makeFakeRate(frfiles,frmet, 0)) + "\n")
	f.write(mcabase.format(name=sig+"_genMET"          , ws=makeWeight(wstr, wvmet[1]), FRfiles=makeFakeRate(frfiles,frmet, 1)) + "\n")
	if len(frjec)==3:
		f.write(mcabase.format(name=sig+"_"+thejec+"_Up"   , ws=makeWeight(wstr, wvjec[1]), FRfiles=makeFakeRate(frfiles,frjec, 1)) + "\n")
		f.write(mcabase.format(name=sig+"_"+thejec+"_Dn"   , ws=makeWeight(wstr, wvjec[2]), FRfiles=makeFakeRate(frfiles,frjec, 2)) + "\n")
	for k,vals in wVars.iteritems():
		f.write(mcabase.format(name=sig+"_"+k+"_Up", ws=makeWeight(wstr,vals[0]), FRfiles=makeFakeRate(frfiles)) + "\n")
		f.write(mcabase.format(name=sig+"_"+k+"_Dn", ws=makeWeight(wstr,vals[1]), FRfiles=makeFakeRate(frfiles)) + "\n")
	f.close()
	mybase = cmdbase.format(MCA=mcadir + "/mca_acc_"+name+".txt", SYS="", O=outdir + "/acc/"+short)
	cmd(mybase.replace("[[","{").replace("]]","}") + " --asimov")
	
	
	## get central value of acceptance 
	doMetVariation(accdir + "/common/SR.input.root", accdir + "/acc_SR.input.root", sig, thejec, themet, wVars)


## prepare the proper job
cp(themca, mcadir + "/mca_full_"+name+".txt")
f = open(mcadir + "/mca_full_"+name+".txt", "a")
f.write(mcabase.format(name=sig+"+"              , ws=wstr, FRfiles=makeFakeRate(frfiles, frjec, 0)) + "\n")
if len(frjec)==3:
	f.write(mcabase.format(name=sig+"_"+thejec+"_Up+", ws=wstr, FRfiles=makeFakeRate(frfiles, frjec, 1)) + ",SkipMe=True\n")
	f.write(mcabase.format(name=sig+"_"+thejec+"_Dn+", ws=wstr, FRfiles=makeFakeRate(frfiles, frjec, 2)) + ",SkipMe=True\n")
if len(frmet)==2:
	f.write(mcabase.format(name=sig+"_"+themet+"_Up+", ws=wstr, FRfiles=makeFakeRate(frfiles, frmet, 0)) + ",SkipMe=True\n")
	f.write(mcabase.format(name=sig+"_"+themet+"_Dn+", ws=wstr, FRfiles=makeFakeRate(frfiles, frmet, 0)) + ",SkipMe=True\n")
for k,vals in wVars.iteritems():
	f.write(mcabase.format(name=sig+"_"+k+"_Up+", ws=makeWeight(wstr,vals[0]), FRfiles=makeFakeRate(frfiles)) + ",SkipMe=True\n")
	f.write(mcabase.format(name=sig+"_"+k+"_Dn+", ws=makeWeight(wstr,vals[1]), FRfiles=makeFakeRate(frfiles)) + ",SkipMe=True\n")
if q2file:
	f.write(mcabase.format(name=sig+"_"+q2acc+"_Up+", ws=wstr, FRfiles=makeFakeRate(frfiles, frjec, 1)) + ",SkipMe=True\n")
	f.write(mcabase.format(name=sig+"_"+q2acc+"_Dn+", ws=wstr, FRfiles=makeFakeRate(frfiles, frjec, 2)) + ",SkipMe=True\n")
f.close()

## run the proper job, which is actually just making the cards
mybase = cmdbase.format(MCA=mcadir + "/mca_full_"+name+".txt", SYS=thesyst, O=outdir+"/mps/"+short)
cmd(mybase.replace("[[","{").replace("]]","}") + " --ip x " + plugFiles([bkgdir+"/common/SR.input.root", accdir+"/acc_SR.input.root"]))

