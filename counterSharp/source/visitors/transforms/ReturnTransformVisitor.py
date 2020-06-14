import logging

from pycparser import c_ast

from .TransformVisitor import TransformVisitor

logger = logging.getLogger(__name__)

class ReturnTransformVisitor(TransformVisitor):
	def __init__(self, configParam):
		super().__init__(configParam)
	def visit_FuncDef(self, node, parents):
		isCheckedFunction = (node.decl.name==self.config.function)
		v = ReturnStmtTransformVisitor(self.config, isCheckedFunction)
		v.visit(node.body,[])
		if not v.foundReturn:
			assertStmt = c_ast.FuncCall(
				c_ast.ID("__CPROVER_assert", coord=ReturnTransformVisitor.TransformCoord),
				c_ast.ExprList(
					[c_ast.Constant('int', "0", coord=ReturnTransformVisitor.TransformCoord),c_ast.Constant('string', "\"\"", coord=ReturnTransformVisitor.TransformCoord)]
				, coord=ReturnTransformVisitor.TransformCoord)
				, coord=ReturnTransformVisitor.TransformCoord)
			stmtList = []
			if isCheckedFunction:
				stmtList.append(assertStmt)
			stmtList.append(c_ast.Return(None, coord=ReturnTransformVisitor.TransformCoord))
			compoundStmt = c_ast.Compound(stmtList, coord=ReturnTransformVisitor.TransformCoord)
			label = c_ast.Label(self.config.returnLabel, compoundStmt,
				coord=ReturnTransformVisitor.TransformCoord)
			node.body.block_items.append(label)
		return None

class ReturnStmtTransformVisitor(TransformVisitor):
	def __init__(self, config, isCheckedFunction):
		super().__init__(config)
		self.foundReturn = False
		self.isCheckedFunction=isCheckedFunction
	def visit_Return(self, node, parents):
		assertStmt = c_ast.FuncCall(
			c_ast.ID("__CPROVER_assert", coord=ReturnTransformVisitor.TransformCoord),
			c_ast.ExprList(
				[c_ast.Constant('int', "0", coord=ReturnTransformVisitor.TransformCoord),c_ast.Constant('string', "\"\"", coord=ReturnTransformVisitor.TransformCoord)]
			, coord=ReturnTransformVisitor.TransformCoord)
			, coord=ReturnTransformVisitor.TransformCoord)
		stmtList = []
		if self.isCheckedFunction:
			stmtList.append(assertStmt)
		stmtList.append(node)
		compoundStmt = c_ast.Compound(stmtList, coord=ReturnTransformVisitor.TransformCoord)
		if not self.foundReturn:
			self.foundReturn = True
			return c_ast.Label(self.config.returnLabel, compoundStmt,
				coord=ReturnTransformVisitor.TransformCoord)
		else:
			return compoundStmt