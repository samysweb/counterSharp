from pycparser import c_ast

from .TransformVisitorTest import TransformVisitorTest

from counterSharp.source.transforms import CondCheckTransformVisitor
from counterSharp.source.transforms import TransformationException

class CondCheckTransformVisitorTest(TransformVisitorTest):
	FunctionIdent = "myTestAssertion"
	VarIdent = "myTestIdent"
	def setUp(self):
		super().setUp()
		self.v = CondCheckTransformVisitor(
			self.config,
			CondCheckTransformVisitorTest.FunctionIdent,
			CondCheckTransformVisitorTest.VarIdent
		)

	def test_noParams(self):
		ast = c_ast.FuncCall(
			c_ast.ID(name=CondCheckTransformVisitorTest.FunctionIdent),
			None
			)
		self.assertRaises(TransformationException, self.v.visit, ast)

	"""
	Check cond check transform works if appearing in compound, case, default or label
	"""
	def test_correctCallResultsInDifference(self):
		ast = c_ast.FuncCall(
			c_ast.ID(name=CondCheckTransformVisitorTest.FunctionIdent),
			c_ast.ExprList([
				c_ast.Constant("int",0)
			])
			)
		# Compound
		ast1 = c_ast.Compound([ast])
		self.v.visit(ast1)
		self.assertNotEqual(ast1.block_items[0],ast)
		# Case
		ast1 = c_ast.Case(c_ast.Constant("int",0),[ast])
		self.v.visit(ast1)
		self.assertNotEqual(ast1.stmts[0],ast)
		# Default
		ast1 = c_ast.Default([ast])
		self.v.visit(ast1)
		self.assertNotEqual(ast1.stmts[0],ast)
		# Label
		ast1 = c_ast.Label("Test",ast)
		self.v.visit(ast1)
		self.assertNotEqual(ast1.stmt,ast)
	
	"""
	Check Cond Transform in detail
	"""
	def test_correctCallDetails(self):
		condExpr = c_ast.Constant("int",0)
		ast = c_ast.FuncCall(
			c_ast.ID(name=CondCheckTransformVisitorTest.FunctionIdent),
			c_ast.ExprList([condExpr])
			)
		# Compound
		ast1 = c_ast.Compound([ast])
		self.v.visit(ast1)
		# If Statement
		self.assertIsInstance(ast1.block_items[0],c_ast.If)
		ifStmt = ast1.block_items[0]
		self.assertEquals(ifStmt.cond, condExpr)
		ifStmtContent = ifStmt.iftrue
		# Assignment
		self.assertIsInstance(ifStmtContent.block_items[0], c_ast.Assignment)
		self.assertEquals(ifStmtContent.block_items[0].op, "=")
		# Assigned identifier
		self.assertIsInstance(ifStmtContent.block_items[0].lvalue, c_ast.ID)
		self.assertEquals(ifStmtContent.block_items[0].lvalue.name,CondCheckTransformVisitorTest.VarIdent)
		# Assigned constant
		self.assertIsInstance(ifStmtContent.block_items[0].rvalue, c_ast.Constant)
		self.assertEquals(ifStmtContent.block_items[0].rvalue.type,"int")
		self.assertEquals(ifStmtContent.block_items[0].rvalue.value,1)
		# Goto statement
		self.assertIsInstance(ifStmtContent.block_items[1], c_ast.Goto)
		self.assertEquals(ifStmtContent.block_items[1].name, self.config.gotoLabel)
	
	def test_assertInExpressionList(self):
		ast = c_ast.ExprList([
			c_ast.FuncCall(
			c_ast.ID(name=CondCheckTransformVisitorTest.FunctionIdent),
			c_ast.ExprList([
				c_ast.Constant("int",0)
			])
			)
		])
		self.assertRaises(TransformationException, self.v.visit, ast)

		