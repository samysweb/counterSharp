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
				c_ast.TypeDecl(self.config.assertMissVar, [], c_ast.IdentifierType(['char'],coord=GlobalVarTransformVisitor.TransformCoord),coord=GlobalVarTransformVisitor.TransformCoord),
				c_ast.Constant('int',"0",coord=GlobalVarTransformVisitor.TransformCoord),
				None,
				coord=GlobalVarTransformVisitor.TransformCoord)
		)

		node.ext.insert(0,
			c_ast.Decl(
				self.config.assumeMissVar,
				[], [], [],
				c_ast.TypeDecl(self.config.assumeMissVar, [], c_ast.IdentifierType(['char'],coord=GlobalVarTransformVisitor.TransformCoord),coord=GlobalVarTransformVisitor.TransformCoord),
				c_ast.Constant('int',"0",coord=GlobalVarTransformVisitor.TransformCoord),
				None,
				coord=GlobalVarTransformVisitor.TransformCoord)
		)