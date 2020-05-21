from pycparser import c_ast

from .TransformVisitorTest import TransformVisitorTest

from counterSharp.source.transforms import GlobalVarTransformVisitor

class GlobalVarTransformVisitorTest(TransformVisitorTest):

	def test_assumeAssert(self):
		ast = c_ast.FileAST([c_ast.Node()])
		v = GlobalVarTransformVisitor(self.config)
		v.visit(ast)
		self.assertIsInstance(ast.ext[0],c_ast.Decl)
		self.assertIsInstance(ast.ext[1],c_ast.Decl)
		if ast.ext[0].name==self.config.assertMissVar:
			assertDecl = ast.ext[0]
			assumeDecl = ast.ext[1]
			self.assertEqual(ast.ext[1].name, self.config.assumeMissVar)
		else:
			self.assertEqual(ast.ext[0].name, self.config.assumeMissVar)
			self.assertEqual(ast.ext[1].name, self.config.assertMissVar)
			assertDecl = ast.ext[1]
			assumeDecl = ast.ext[0]
		self.assertEqual(assertDecl.type.declname, self.config.assertMissVar)
		self.assertEqual(assumeDecl.type.declname, self.config.assumeMissVar)
		self.assertEqual(assertDecl.init.value, '\0')
		self.assertEqual(assumeDecl.init.value, '\0')
		