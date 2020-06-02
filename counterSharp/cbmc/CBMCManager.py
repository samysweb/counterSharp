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
		print(self.dimacs)
	
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