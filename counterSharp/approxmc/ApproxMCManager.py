import logging
import os
import subprocess

logger = logging.getLogger(__name__)

class ApproxMCManager:
	def __init__(self, configParam, cbmcParam):
		self.config = configParam
		self.cbmc = cbmcParam
	
	def run(self):
		# Count assertion miss paths
		runCmd = ["approxmc", "--verb", "0"]
		logger.debug(" ".join(runCmd))
		curRun = subprocess.Popen(runCmd, stdin=subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
		curRun.stdin.write(("c ind "+(" ".join(self.cbmc.inputLiterals))+" 0\n").encode())
		curRun.stdin.write(("p cnf %d %d\n"%(self.cbmc.dimacsVars,(self.cbmc.dimacsClauses+1+len(self.cbmc.assumeMissLiterals)))).encode())
		for c in self.cbmc.dimacs:
			if len(c.strip())!=0:
				curRun.stdin.write((c+"\n").encode())
		curRun.stdin.write((" ".join(self.cbmc.assertMissLiterals)+" 0\n").encode())
		# No assume miss literals may be set
		for l in self.cbmc.assumeMissLiterals:
			curRun.stdin.write(("-%s 0\n"%(l)).encode())
		curRun.stdin.close()
		while curRun.returncode is None:
			curRun.poll()
		print(curRun.stdout.read().decode('ascii'))
		print(curRun.stderr.read().decode('ascii'))

		# Count assume miss paths
		runCmd = ["approxmc", "--verb", "0"]
		logger.debug(" ".join(runCmd))
		curRun = subprocess.Popen(runCmd, stdin=subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
		curRun.stdin.write(("c ind "+(" ".join(self.cbmc.inputLiterals))+" 0\n").encode())
		curRun.stdin.write(("p cnf %d %d\n"%(self.cbmc.dimacsVars,(self.cbmc.dimacsClauses+1))).encode())
		for c in self.cbmc.dimacs:
			if len(c.strip())!=0:
				curRun.stdin.write((c+"\n").encode())
		curRun.stdin.write((" ".join(self.cbmc.assumeMissLiterals)+" 0\n").encode())
		# No assert miss literals may be set
		for l in self.cbmc.assertMissLiterals:
			curRun.stdin.write(("-%s 0\n"%(l)).encode())
		curRun.stdin.close()
		while curRun.returncode is None:
			curRun.poll()
		print(curRun.stdout.read().decode('ascii'))
		print(curRun.stderr.read().decode('ascii'))

			