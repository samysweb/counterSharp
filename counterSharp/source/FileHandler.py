import logging
import pycparser
import os
import tempfile

from pycparser import c_generator

from .PPGenerator import PPGenerator
from .visitors import InputFinder
from .visitors.transforms import GlobalVarTransformVisitor, AssertTransformVisitor, AssumeTransformVisitor, ReturnTransformVisitor, FunctionCallTransformVisitor

logger = logging.getLogger(__name__)

"""
Transforms input C files into CBMC input C files
Source Code transformation of
- asserts
- assumes
- returns
- function calls
"""
class FileHandler:
	sourceTransformations = [
		GlobalVarTransformVisitor,
		AssertTransformVisitor,
		AssumeTransformVisitor,
		ReturnTransformVisitor,
		FunctionCallTransformVisitor
	]

	def __init__(self, configParam, inputFileParam):
		self.config = configParam
		self.inputFile = inputFileParam
		if not os.path.isfile(self.inputFile):
			raise FileNotFoundError(self.inputFile)
		includeHeaders = os.path.dirname(__file__)+"/../pycparser/fake_libc_include/"
		self.ast = pycparser.parse_file(self.inputFile, use_cpp=True, cpp_args='-I'+includeHeaders)
	
	def process(self):
		for Transformation in FileHandler.sourceTransformations:
			t = Transformation(self.config)
			t.visit(self.ast)
		self.findInputs()
	
	def findInputs(self):
		finder = InputFinder(self.config)
		finder.visit(self.ast)
		self.inputVars = finder.getInputVars()

	def storeTemp(self):
		with open(self.inputFile,"r") as inputHandle:
			generator = PPGenerator(self.inputFile, inputHandle)
			with tempfile.NamedTemporaryFile("w", delete=False, suffix=".c") as f:
				self.tempFileName = f.name
				print(generator.visit(self.ast),file=f)
	
	def delTemp(self):
		os.unlink(self.fileName)
		