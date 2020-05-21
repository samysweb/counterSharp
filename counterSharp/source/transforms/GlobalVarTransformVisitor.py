import logging

from pycparser import c_ast

from .TransformVisitor import TransformVisitor

logger = logging.getLogger(__name__)

class GlobalVarTransformVisitor(TransformVisitor):
	def visit_FileAST(self, node, parents):
		node.ext.insert(0,
			c_ast.Decl(
				self.config.assertMissVar,
				[], [], [],
				c_ast.TypeDecl(self.config.assertMissVar, [], c_ast.IdentifierType(['char'])),
				c_ast.Constant('char','\0'),
				None,
				coord=GlobalVarTransformVisitor.TransformCoord)
		)

		node.ext.insert(0,
			c_ast.Decl(
				self.config.assumeMissVar,
				[], [], [],
				c_ast.TypeDecl(self.config.assumeMissVar, [], c_ast.IdentifierType(['char'])),
				c_ast.Constant('char','\0'),
				None,
				coord=GlobalVarTransformVisitor.TransformCoord)
		)