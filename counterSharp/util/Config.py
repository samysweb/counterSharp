import argparse
import logging


class Config:
	def __init__(self, args):
		parser = argparse.ArgumentParser()

		parser.add_argument('--amm', dest='assumeMissFile', action='store', required=True,help="Name of the assume miss dimacs file")
		parser.add_argument('--amh', dest='assumeHitFile', action='store', required=True,help="Name of the assume hit dimacs file")
		parser.add_argument('--asm', dest='assertMissFile', action='store', required=True,help="Name of the assert miss dimacs file")
		parser.add_argument('--ash', dest='assertHitFile', action='store', required=True,help="Name of the assert hit dimacs file")
		parser.add_argument('--con', dest='confidenceFile', action='store', required=True,help="Name of the confidence file (counts the number of inputs missing the bounds")

		# Debug flag
		parser.add_argument('-d', dest='debug', action='store_true')
		# Function to parse
		parser.add_argument('--function', dest='function',action='store',nargs=1,default='main',required=False)
		# Name of internal assume and assert variables
		parser.add_argument('--assertMissVar', dest='assertMissVar', action='store',nargs=1,default='__counterSharp_assertMiss',required=False)
		parser.add_argument('--assumeMissVar', dest='assumeMissVar', action='store',nargs=1,default='__counterSharp_assumeMiss',required=False)
		parser.add_argument('--assertFunction', dest='assertFunction', action='store',nargs=1,default='__counterSharp_assert',required=False)
		parser.add_argument('--assumeFunction', dest='assumeFunction', action='store',nargs=1,default='__counterSharp_assume',required=False)
		parser.add_argument('--returnLabel', dest='returnLabel', action='store', nargs=1, default='__counterSharp_end', required=False)
		parser.add_argument('--cbmcArg', dest='cbmcArgs', action='append', required=False)
		parser.add_argument('--unwindDepth', dest='unwindDepth', action='store', required=False)

		# C Input Files
		parser.add_argument('inputfiles', nargs='*',)
		
		args = parser.parse_args(args)

		self.debug = args.debug

		self.function = args.function[0]
		# TODO(steuber): Make configurable
		self.returnVal = "__counterSharp_returnVal"
		self.assertMissVar = args.assertMissVar
		self.assumeMissVar = args.assumeMissVar
		self.assertFunction = args.assertFunction
		self.assumeFunction = args.assumeFunction
		self.returnLabel = args.returnLabel
		self.cbmcArgs = args.cbmcArgs if args.cbmcArgs is not None else []
		self.unwindDepth = args.unwindDepth if args.unwindDepth is not None else -1

		# Properties for which DIMACS files should be computed
		self.computeOutputs = []
		self.computeOutputs.append(([(self.assertMissVar, "0"),(self.assumeMissVar, "0",)], args.assertHitFile))
		self.computeOutputs.append(([(self.assertMissVar, "1"),(self.assumeMissVar, "0",)], args.assertMissFile))
		self.computeOutputs.append(([(self.assumeMissVar, "0")], args.assumeHitFile))
		self.computeOutputs.append(([(self.assumeMissVar, "1")], args.assumeMissFile))
		self.confidenceFile = args.confidenceFile

		self.inputFiles = args.inputfiles
		if self.debug:
			logging.basicConfig(format='[%(name)s] %(levelname)s: %(message)s', level=logging.DEBUG)
		else:
			logging.basicConfig(format='[%(name)s] %(levelname)s: %(message)s', level=logging.DEBUG)
		self.logger = logging.getLogger(__name__)
		self.logger.debug("Input files: "+str(self.inputFiles))

		
	
		