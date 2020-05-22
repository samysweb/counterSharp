import logging

from pycparser import c_ast

from .CondCheckTransformVisitor import CondCheckTransformVisitor

logger = logging.getLogger(__name__)

class AssertTransformVisitor(CondCheckTransformVisitor):

	def __init__(self, config):
		super().__init__(config, config.assertFunction, config.assertMissVar)