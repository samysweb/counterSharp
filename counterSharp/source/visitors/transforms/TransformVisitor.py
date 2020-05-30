import logging

from pycparser.plyparser import Coord

from .MutableVisitor import MutableVisitor

logger = logging.getLogger(__name__)

class TransformVisitor(MutableVisitor):
	TransformCoord=Coord("COUNTERSHARP",0,0)
	def __init__(self, configParam):
		self.config = configParam