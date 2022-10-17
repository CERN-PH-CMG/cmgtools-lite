import os
from functions import *


class Init():
	def __init__(self, path):
		self.path = path
		self.load()
	def identify(self, module, args, options):
		if not module or len(args)==0: return False
		if getattr(self, "module", None) != module: return False
		for i in range(len(args)):
			if getattr(self, "arg"+str(i), None) != args[i]: return False
		for key, val in options.__dict__.iteritems():
			if key=="pretend": continue
			if type(val) is list or type(val) is tuple:
				opt = getattr(self, "opt_"+key, [])
				# an artifact of reading and writing empty lists
				if not (type(opt) is list or type(opt) is tuple):
					if opt: opt = [opt]
					else  : opt = []
				if not compareLists(opt, val): return False
			else:
				opt = getattr(self, "opt_"+key, "")
				if opt != str(val): return False
		return True
	def load(self):
		if not os.path.exists(self.path): return
		for line in [l.strip("\n") for l in open(self.path,"r").readlines()]:
			if line[0]=="#" or len(line.strip())==0: continue
			sl = [s.strip() for s in line.split(":")]
			if sl[1].count(";")>0: setattr(self, sl[0], sl[1].split(";"))
			else                 : setattr(self, sl[0], sl[1]           )
	def set(self, module, args, options):
		self.module = module
		for i in range(len(args)):
			setattr(self, "arg"+str(i), args[i])
		for key, val in options.__dict__.iteritems():
			setattr(self, "opt_"+key, val)
	def write(self):
		if os.path.exists(self.path): cmd("rm "+self.path)
		f = open(self.path, "w")
		for key, val in self.__dict__.iteritems():
			if key=="pretend": continue
			if type(val) is list or type(val) is tuple:
				val = splitList(val)
				f.write(key +" : "+ ";".join([str(e) for e in val]) +"\n")
				continue
			f.write(key +" : "+ str(val) +"\n")
		f.close()

