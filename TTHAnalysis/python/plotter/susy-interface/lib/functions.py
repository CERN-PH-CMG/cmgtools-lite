import sys, os, subprocess, datetime

def bash(cmd):
	#print cmd
	pipe = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
	back = pipe.stdout.read().rstrip("\n").strip()
	return back

def cleandir(path, cpIdx = True):
	if not os.path.isdir(path): return
	path = path.rstrip("/")
	cmd("rm -rf " + path + "/*")
	if cpIdx: cp("/afs/cern.ch/user/g/gpetrucc/php/index.php", path)

def cmd(cmd):
	#print cmd
	os.system(cmd)

def compareLists(list1, list2):
	if set(list1) == set(list2): return True
	return False

def cp(location, destination):
	cmd("cp " + location + " " + destination)

def factorial(array):
	return [prod(array[0:n]) for n in range(len(array))]

def getAllBins(bins):
	if not bins: return []
	separated = []
	if bins.find("[")>-1:
		values = [float(a) for a in bins.strip("[").strip("]").split(",")]
	else:
		steps, min, max = int(bins.split(",")[0]), float(bins.split(",")[1]), float(bins.split(",")[2])
		step = (max-min)/steps
		values = [min+step*i for i in range(0,steps+1)]
	return ["1,"+str(values[i])+","+str(values[i+1]) for i in range(0,len(values)-1)]

def getBinLength(bins):
	if not bins: return -1
	if bins.find("[")>-1:
		return int(bins.count(","))
	return int(bins.split(",")[0])

def getCut(firstCut, expr, bins):
	if not expr or not bins: return ""
	min, max = getMinMax(bins)
	return "-A {first} inSR '{EXPR}>={MIN} && {EXPR}<={MAX}'".format(first=firstCut, EXPR=expr, MIN=min, MAX=max)

def getMinMax(bins):
	if not bins: return -1, -1
	if bins.find("[")>-1:
		min,max = bins.split(",")[0].lstrip("["), bins.split(",")[-1].rstrip("]")
	else:
		min, max = bins.split(",")[1], bins.split(",")[2]
	return min, max

def getOffset(expr, bins):
	if not expr or not bins: return ""
	offset = 0
	if expr.find("-")>-1:
		offset += int(expr.split("-")[1].split(".")[0])
	if bins.find("[")>-1:
		offset += int(bins.split(",")[0].lstrip("[").split(".")[0])
	else:
		offset += int(bins.split(",")[1].split(".")[0])
	return str(offset)

def makeCombs(ncomb, steps, periods):
	cols = [[] for p in periods]
	ros  = []
	for i,p in enumerate(periods):
		for pack in range(0,ncomb/p):
			for num in range(0,p):
				cols[i].extend([num for s in range(steps[i])])
	for i in range(ncomb):
		row.append([cols[j][i] for j in range(len(cols))])
	return rows

def mkdir(path, cpIdx = True):
	if os.path.isdir(path): return
	cmd("mkdir -p " + path)
	if cpIdx and not os.path.exists(path.rstrip("/") + "/index.php"):
		cp("/afs/cern.ch/user/g/gpetrucc/php/index.php", path)

def mkcleandir(path, cpIdx = True):
	if os.path.isdir(path):
		cleandir(path, cpIdx)
		return
	mkdir(path, cpIdx)

def prod(array):
	return reduce(operator.mul, array, 1)

def replaceInFile(path, search, replace):
	f = open(path, "r")
	lines = "".join(f.readlines())
	f.close()
	lines = lines.replace(search, replace)
	os.system("rm " + path)
	f = open(path, "w")
	f.write(lines)
	f.close()

def splitList(thelist, separator = ";"):
	result = []
	for element in thelist:
		result.extend(element.split(";"))
	return result

def timestamp(readable = True):
	if readable:
		return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	return datetime.datetime.now().strftime("%y%m%d%H%M%S%f")
		

