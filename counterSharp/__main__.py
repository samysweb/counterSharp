import logging
from pycparser import c_parser
import sys

from .source import SourceManager
from .util import Config
from .cbmc import CBMCManager

logger = logging.getLogger(__name__)

def main():
	config = Config(sys.argv[1:])
	sourceManager = SourceManager(config)
	sourceManager.parse()
	sourceManager.process()
	sourceManager.storeTemp()
	#cbmc = CBMCManager(sourceManager)
	#cbmc.obtainCNF()
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