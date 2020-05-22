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
			CondCheckTransformVisitorTest.FunctionIdent,
			None
			)
		self.assertRaises(TransformationException, self.v.visit, ast)

	def test_correctCallResultsInDifference(self):
		ast = c_ast.FuncCall(
			CondCheckTransformVisitorTest.FunctionIdent,
			c_ast.ExprList([
				c_ast.Constant("int",0)
			])
			)
		ast1 = c_ast.Compound([ast])
		self.v.visit(ast1)
		self.assertNotEqual(ast1.block_items[0],ast)
	
	# TODO(steuber): Test for assertion in expression list
	# TODO(steuber): Test for correct conversion

		