import logging

from .MutableVisitor import MutableVisitor

logger = logging.getLogger(__name__)

class TransformVisitor(MutableVisitor):
	TransformCoord="COUNTERSHARP"
	def __init__(self, configParam):
		self.config = configParam