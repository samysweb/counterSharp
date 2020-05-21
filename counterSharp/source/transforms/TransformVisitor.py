import logging

from pycparser import c_ast

logger = logging.getLogger(__name__)

class TransformVisitor(c_ast.NodeVisitor):
	TransformCoord="COUNTERSHARP"
	def __init__(self, configParam):
		self.config = configParam