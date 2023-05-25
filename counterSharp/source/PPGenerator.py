import re

from pycparser.c_generator import CGenerator
from pycparser import c_ast

from .visitors.transforms import TransformVisitor

class PPGenerator(CGenerator):
	def __init__(self, nameParam, fileHandleParam):
		super().__init__()
		self.name = nameParam
		self.fileHandle = fileHandleParam
		self.lineNum = 0
	
	def visit(self, node):
		if node is not None:
			pos = node.coord
			if pos is not None and not "pycparser/fake_libc_include" in pos.file:
				# Omit content from global inclusions
				prefix = ""
				while (pos.line >= self.lineNum):
					curLine = self.fileHandle.readline().strip()
					if len(curLine)>0:
						for inc in re.finditer(r'\#include\s?[<][^>]+[>]', curLine):
							prefix+=inc[0]+"\n"
						for inc in re.finditer(r'\#include\s?["][^"]+["]', curLine):
							print("WARNING: Local inclusions are only supported if all global inclusions are in the main file!")
							prefix+="\n" # We keep the inclusion of local files
					self.lineNum+=1
				return prefix+(str(super().visit(node)))
			elif isinstance(node, c_ast.FileAST) or pos == TransformVisitor.TransformCoord:
				return str(super().visit(node))
			else:
				return ""
		else:
			return ""
