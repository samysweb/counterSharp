import subprocess
import re
import logging

logger = logging.getLogger(__name__)

class CBMCManager:
	UnwindStartVal = 2

	def __init__(self, configParam, sourceManagerParam):
		self.sourceManager = sourceManagerParam
		self.fileListParam = self.sourceManager.getTempFiles()
		self.config = configParam
		self.genericUnwindDepth = CBMCManager.UnwindStartVal
		self.specificUnwindDepth = {}
	
	def run(self):
		self.findUnwindDepth()
		self.exportDimacs()
	
	def exportDimacs(self):
		cmd = ["cbmc", "--verbosity", "0", "--function", self.config.function, "--dimacs", "--unwind", str(self.genericUnwindDepth)] + self.getSpecificUnwind()
		cmd.extend(self.config.cbmcArgs)
		cmd.extend(self.fileListParam)
		curRun = subprocess.run(cmd, capture_output=True)
		self.dimacs = curRun.stdout.decode('ascii').split("\n")
		instanceData = self.dimacs[0].split(" ")
		assert(instanceData[0]=="p")
		self.dimacsVars = int(instanceData[2])
		self.dimacsClauses = int(instanceData[3])
		self.dimacs = self.dimacs[1:]
		inputSymbols = self.sourceManager.getInputSymbols()
		if inputSymbols is None:
			raise Exception("No input variables for function found")
		# REGEX_NORMAL_STR = R"(^c (c::)?(.*?)::(.*?)::(.*?)!(\d*)@(\d*)#(\d*) (.*)$)";
		# REGEX_SHORT_STR = R"(^c (\d*) (c::)?(.*?)::(.*?)::(.*?)!(\d*)@(\d*)#(\d*)$)";
		# r(^c (c::)?(.*?)::(.*?)::(.*?)!(\d*)@(\d*)#(\d*) (.*)$)
		# function_name::[unknown::]variable_name!thread_name@rec_depth#time vars...
		needles=[]
		for s in inputSymbols:
			needles.append("c "+self.config.function+"::"+s.name+"!0@1#1")
		# NOTE(steuber): Could be optimized with some fancy string algorithm...
		self.inputLiterals = []
		self.assertMissLiterals = []
		self.assumeMissLiterals = []
		for line in self.dimacs:
			for n in needles:
				if line.startswith(n):
					self.inputLiterals.extend([
						x.strip() for x in line.split(" ")[2:] if x != "FALSE" and x != "TRUE"
					])
				if line.startswith("c "+self.config.assertMissVar+"#"):
					x = line.split(" ")[2].strip()
					if x != "FALSE" and x != "TRUE":
						self.assertMissLiterals.append(x)
				if line.startswith("c "+self.config.assumeMissVar+"#"):
					x = line.split(" ")[2].strip()
					if x != "FALSE" and x != "TRUE":
						self.assumeMissLiterals.append(x)
		if len(self.inputLiterals)==0:
			raise Exception("No unfixed input literals found in DIMACS")
		if len(self.assertMissLiterals)==0:
			logger.warning("No unfixed assertMiss literals found. If asserts have been defined this is worrying...")
		if len(self.assumeMissLiterals)==0:
			logger.warning("No unfixed assumeMiss literals found. If assumes have been defined this is worrying...")
		
	
	def findUnwindDepth(self):
		baseCmd = ["cbmc", "--verbosity", "4", "--function", self.config.function, "--no-assertions", "--no-assumptions"]
		maxVal = self.genericUnwindDepth
		while True:
			runCmd = baseCmd + ["--unwind", str(self.genericUnwindDepth), "--unwinding-assertions"] + self.getSpecificUnwind() + self.fileListParam
			logger.debug(" ".join(runCmd))
			curRun = subprocess.run(runCmd, capture_output=True)
			if curRun.returncode == 0:
				# No more refinement necessary
				break
			if len(curRun.stderr)>0:
				# CBMC failed
				raise Exception("CBMC threw error: "+str(curRun.stderr))
			resultLines = curRun.stdout.decode('ascii').split("\n** Results:\n")[1].split("\n")
			nonBoundedLoop = False
			for l in resultLines:
				# Check for loop bound failures
				if len(l.strip()) == 0:
					# Only evaluate until empty line
					break
				reResult = re.match(r'\[([^\.]+).unwind.([^\.]+)\] .*: FAILURE$', l.strip())
				if reResult is not None:
					nonBoundedLoop=True
					loopIdent = reResult[1]+"."+reResult[2]
					if loopIdent in self.specificUnwindDepth:
						self.specificUnwindDepth[loopIdent]*=2
					else:
						self.specificUnwindDepth[loopIdent]=2*self.genericUnwindDepth
					if self.specificUnwindDepth[loopIdent]>maxVal:
						maxVal = self.specificUnwindDepth[loopIdent]
			if not nonBoundedLoop:
				self.genericUnwindDepth=maxVal
	
	def getSpecificUnwind(self):
		res = ["--unwindset"]
		param2=[]
		for loopIdent, val in self.specificUnwindDepth.items():
			param2.append(loopIdent+":"+str(val))
		res.append(",".join(param2))
		return res
			

	# Unwinding till bound assertion fulfilled:
	# First round: cbmc --function [xyz] --unwind 2 --unwinding-assertions --no-assertions --no-assumptions [files]
	# ith round: cbmc --function [xyz] --unwind [2^i*n] --unwindset [loopid0]:j ... --unwindset [loopidn]:k --unwinding-assertions --no-assertions --no-assumptions [files]