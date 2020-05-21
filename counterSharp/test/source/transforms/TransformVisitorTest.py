from counterSharp.util import Config

import unittest

class TransformVisitorTest(unittest.TestCase):
	def setUp(self):
		self.config=Config(["--assertMissVar", "assertMissVar", "--assumeMissVar", "assumeMissVar", "file.c"])