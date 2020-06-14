import logging
import os
import subprocess

logger = logging.getLogger(__name__)

class ApproxMCManager:
	def __init__(self, configParam, cbmcParam):
		self.config = configParam
		self.cbmc = cbmcParam
	
	def run(self):
		# Count assume miss paths
		with open(self.config.assumeMissFile,"w") as f:
			print("c Assume Miss",file=f)
			print("c ind "+(" ".join(self.cbmc.inputLiterals))+" 0",file=f)
			print("p cnf %d %d"%(self.cbmc.dimacsVars,(self.cbmc.dimacsClauses+1)), file=f)
			for c in self.cbmc.dimacs:
				if len(c.strip())!=0:
					print(c, file=f)
			print("c One Assume Variable must be true",file=f)
			print(" ".join(self.cbmc.assumeMissLiterals)+" 0", file=f)
			print("c All Assert Variables must be false", file=f)
			for l in self.cbmc.assertMissLiterals:
				print("-%s 0"%(l), file=f)
		
		# Count assume hit paths
		with open(self.config.assumeHitFile,"w") as f:
			print("c Assume Hit", file=f)
			print("c ind "+(" ".join(self.cbmc.inputLiterals))+" 0",file=f)
			print("p cnf %d %d"%(self.cbmc.dimacsVars,(self.cbmc.dimacsClauses+1)), file=f)
			for c in self.cbmc.dimacs:
				if len(c.strip())!=0:
					print(c, file=f)
			print("c All Assume Variables must be false", file=f)
			for l in self.cbmc.assumeMissLiterals:
				print("-%s 0"%(l), file=f)

		# Count assert miss paths
		with open(self.config.assertMissFile,"w") as f:
			print("c Assert Miss", file=f)
			print("c ind "+(" ".join(self.cbmc.inputLiterals))+" 0",file=f)
			print("p cnf %d %d"%(self.cbmc.dimacsVars,(self.cbmc.dimacsClauses+1)), file=f)
			for c in self.cbmc.dimacs:
				if len(c.strip())!=0:
					print(c, file=f)
			print("c All Assume Variables must be false", file=f)
			for l in self.cbmc.assumeMissLiterals:
				print("-%s 0"%(l), file=f)
			print("c One Assert Variable must be true",file=f)
			print(" ".join(self.cbmc.assertMissLiterals)+" 0", file=f)
		
		# Count assert miss paths
		with open(self.config.assertHitFile,"w") as f:
			print("c Assert Hit", file=f)
			print("c ind "+(" ".join(self.cbmc.inputLiterals))+" 0",file=f)
			print("p cnf %d %d"%(self.cbmc.dimacsVars,(self.cbmc.dimacsClauses+1)), file=f)
			for c in self.cbmc.dimacs:
				if len(c.strip())!=0:
					print(c, file=f)
			print("c All Assume Variables must be false", file=f)
			for l in self.cbmc.assumeMissLiterals:
				print("-%s 0"%(l), file=f)
			print("c All Assert Variables must be false", file=f)
			for l in self.cbmc.assertMissLiterals:
				print("-%s 0"%(l), file=f)

			