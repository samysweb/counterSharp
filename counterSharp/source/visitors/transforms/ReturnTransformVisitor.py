import logging

from pycparser import c_ast

from .TransformVisitor import TransformVisitor

logger = logging.getLogger(__name__)

class ReturnTransformVisitor(TransformVisitor):
	def visit_Return(self, node, parents):
		assertStmt = c_ast.FuncCall(
			c_ast.ID("__CPROVER_assert", coord=ReturnTransformVisitor.TransformCoord),
			c_ast.ExprList(
				[c_ast.Constant('int', "0", coord=ReturnTransformVisitor.TransformCoord),c_ast.Constant('string', "\"\"", coord=ReturnTransformVisitor.TransformCoord)]
			, coord=ReturnTransformVisitor.TransformCoord)
			, coord=ReturnTransformVisitor.TransformCoord)
		return c_ast.Compound([
			assertStmt,
			node
		], ReturnTransformVisitor.TransformCoord)