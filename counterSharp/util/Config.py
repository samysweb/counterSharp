import argparse
import logging


class Config:
	def __init__(self, args):
		parser = argparse.ArgumentParser()
		# Debug flag
		parser.add_argument('-d', dest='debug', action='store_true')
		# Function to parse
		parser.add_argument('--function', dest='function',action='store',nargs=1,default='main',required=False)
		# Name of internal assume and assert variables
		parser.add_argument('--assertMissVar', dest='assertMissVar', action='store',nargs=1,default='__counterSharp_assertMiss',required=False)
		parser.add_argument('--assumeMissVar', dest='assumeMissVar', action='store',nargs=1,default='__counterSharp_assumeMiss',required=False)
		parser.add_argument('--assertFunction', dest='assertFunction', action='store',nargs=1,default='__counterSharp_assert',required=False)

		# C Input Files
		parser.add_argument('inputfiles', nargs='*',)
		
		args = parser.parse_args(args)
		self.debug = args.debug

		self.function = args.function
		
		self.assertMissVar = args.assertMissVar
		self.assumeMissVar = args.assumeMissVar
		self.assertFunction = args.assertFunction

		self.inputFiles = args.inputfiles
		if self.debug:
			logging.basicConfig(format='[%(name)s] %(levelname)s: %(message)s', level=logging.DEBUG)
		else:
			logging.basicConfig(format='[%(name)s] %(levelname)s: %(message)s', level=logging.DEBUG)
		self.logger = logging.getLogger(__name__)
		self.logger.debug("Input files: "+str(self.inputFiles))

		
	
		