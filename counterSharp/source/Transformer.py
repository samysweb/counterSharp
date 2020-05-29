import logging
import pycparser
import os

from pycparser import c_generator

from .transforms import GlobalVarTransformVisitor, AssertTransformVisitor, AssumeTransformVisitor

logger = logging.getLogger(__name__)

"""
Transforms input C files into CBMC input C files
Source Code transformation of
- asserts
- assumes
- returns
- function calls
"""
class Transformer:
	sourceTransformations = [
		GlobalVarTransformVisitor,
		AssertTransformVisitor,
		AssumeTransformVisitor
	]

	def __init__(self, configParam, inputFileParam):
		self.config = configParam
		self.inputFile = inputFileParam
		includeHeaders = os.path.dirname(__file__)+"/../pycparser/fake_libc_include/"
		self.ast = pycparser.parse_file(self.inputFile, use_cpp=True, cpp_args='-I'+includeHeaders)
		# self.ast.show(showcoord=True)
	
	def process(self):
		for Transformation in Transformer.sourceTransformations:
			t = Transformation(self.config)
			t.visit(self.ast)
		generator = c_generator.CGenerator()
		print(generator.visit(self.ast))
		# self.ast.show(showcoord=True)
		