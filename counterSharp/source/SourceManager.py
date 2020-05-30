from enum import Enum
import logging
import os
import tempfile

import pycparser
from pycparser.c_generator import CGenerator

from .FileHandler import FileHandler

logger = logging.getLogger(__name__)

class SMState:
	"""
	Source Manager has been initialized
	"""
	INIT=1
	"""
	C files have been succesfully parsed
	"""
	PARSED=2
	"""
	C files have successfully been processed (AST transformations)
	"""
	PROCESSED=3
	"""
	C files have successfully been stored in temporary files
	"""
	STORED=4
	"""
	C files were successfully deleted
	"""
	DELETED=5

class InvalidSMStateException(Exception):
	pass

class SourceManager:
	def __init__(self, config):
		self.config = config
		self.sourceFiles = config.inputFiles
		self.state = SMState.INIT
		self.fileHandlers=[]
		
	
	def parse(self):
		if not self.state == SMState.INIT:
			raise InvalidSMStateException()
		includeHeaders = os.path.dirname(__file__)+"/../pycparser/fake_libc_include/"
		self.parsedFiles = {}
		generator = CGenerator()
		for file in self.sourceFiles:
			# TODO(steuber): Check if files exist
			self.fileHandlers.append(FileHandler(self.config, file))
		self.state = SMState.PARSED
	
	def process(self):
		if not self.state == SMState.PARSED:
			raise InvalidSMStateException()
		
		for f in self.fileHandlers:
			f.process()
		
		self.state = SMState.PROCESSED
		
	
	def storeTemp(self):
		if not self.state == SMState.PROCESSED:
			raise InvalidSMStateException()
		for f in self.fileHandlers:
			f.storeTemp()
		self.state = SMState.STORED
		if self.config.debug:
			for f in self.fileHandlers:
				logger.debug(f.tempFileName)
	
	def deleteTemp(self):
		if not self.state == SMState.STORED:
			raise InvalidSMStateException()
		for f in self.fileHandlers:
			f.deleteTemp()
		self.state = SMState.DELETED