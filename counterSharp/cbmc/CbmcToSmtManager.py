import subprocess
import re
import logging
import signal
import tempfile

from .CbmcManager import CbmcManager

logger = logging.getLogger(__name__)

class CbmcToSmtManager(CbmcManager):
	UnwindStartVal = 2

	def __init__(self, configParam, sourceManagerParam):
		super().__init__(configParam, sourceManagerParam)
	
	def exportDimacs(self):
		with tempfile.NamedTemporaryFile("w+") as outfile:
			cmd = ["cbmc", "--verbosity", "4", "--smt2", "--outfile", outfile.name, "--function", self.config.function, "--slice-formula", "--unwind", str(self.genericUnwindDepth)] + self.getSpecificUnwind()
			cmd.extend(self.config.cbmcArgs)
			inputSymbols = self.sourceManager.getInputSymbols()
			# NOTE(steuber): The following could be optimized with some fancy string algorithm probably...
			needles=[]
			for s in inputSymbols:
				#"c __CPROVER__start::i!0#2 ""
				#needles.append("c __CPROVER__start::"+s.name+"!0#2 ")
				needles.append("|__CPROVER__start::"+s.name+"!0@1#2|")
				#needles.append("c "+self.config.function+"::"+s.name+"!0@1#1 ")
			
			if inputSymbols is None:
				raise Exception("No input variables for function found")
			# confidence
			curCmd = cmd + ["--no-assertions", "--no-assumptions", "--unwinding-assertions"]  + self.fileListParam
			stdout = self.runCbmc(curCmd)
			self.writeSmtFile(outfile, needles, self.config.confidenceFile)
			# assume/assert hit/miss
			for i in range(0,len(self.config.computeOutputs)):
				curCmd = cmd + ["--property", self.config.function+".assertion."+str(i+1)] + self.fileListParam
				stdout = self.runCbmc(curCmd)
				self.writeSmtFile(outfile, needles, self.config.computeOutputs[i][1])
	
	def writeSmtFile(self, smtfile, inputNeedles, outputFile):
		if smtfile is None:
			logger.info("Did not write file %s: State not reachable"%(outputFile))
		smtfile.seek(0)
		inputLiterals = []
		projectionVars = []
		for line in smtfile:
			for n in inputNeedles:
				if line.startswith("(define-fun "+n+""):
					projectionVars.append(n)
		with open(outputFile,"w") as outputF:
			smtfile.seek(0)
			printedProjections = False
			for line in smtfile:
				if line.startswith("(check-sat)") and not printedProjections:
					for p in projectionVars:
						print("(project-on "+p+")", file=outputF)
					printedProjections=True
					print("(count-sat)", file=outputF)
				elif not line.startswith("(get-value"):
					print(line,file=outputF)