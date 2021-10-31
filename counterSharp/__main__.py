import logging
from pycparser import c_parser
import sys

from .source import SourceManager
from .util import Config
from .cbmc import CbmcManager, CbmcToSmtManager
from .approxmc import ApproxMCManager

logger = logging.getLogger(__name__)

def main():
	config = Config(sys.argv[1:])
	sourceManager = SourceManager(config)
	sourceManager.parse()
	sourceManager.process()
	sourceManager.storeTemp()
	if config.smt:
		cbmc = CbmcToSmtManager(config, sourceManager)
	else:
		cbmc = CbmcManager(config, sourceManager)
	cbmc.run()
	# approxmc = ApproxMCManager(config, cbmc)
	# approxmc.run()
	# TODO(steuber): Reactivate this...
	#sourceManager.delete()

if __name__ == '__main__':
	main()
	# parser = c_parser.CParser()
	# ast = parser.parse(text)
	# print("Before:")
	# ast.show(offset=2)

	# assign = ast.ext[0].body.block_items[0]
	# assign.lvalue.name = "y"
	# assign.rvalue.value = 2

	# print("After:")
	# ast.show(offset=2)