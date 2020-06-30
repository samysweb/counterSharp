from pycparser import c_ast
from .TransformVisitor import TransformVisitor
from .TransformationException import TransformationException

class FunctionCallTransformVisitor(TransformVisitor):
	def __init__(self, config):
		super().__init__(config)
		self.funcCallFinder = FuncCallFinderVisitor()
		self.ifCheck = c_ast.If(
			cond=c_ast.BinaryOp(
				op='||',
				left=c_ast.BinaryOp(
					op='==',
					left=c_ast.ID(name=self.config.assertMissVar, coord=FunctionCallTransformVisitor.TransformCoord),
					right=c_ast.Constant(type='int',value=1, coord=FunctionCallTransformVisitor.TransformCoord),
					coord=FunctionCallTransformVisitor.TransformCoord
				),
				right=c_ast.BinaryOp(
					op='==',
					left=c_ast.ID(name=self.config.assumeMissVar, coord=FunctionCallTransformVisitor.TransformCoord),
					right=c_ast.Constant(type='int',value=1, coord=FunctionCallTransformVisitor.TransformCoord),
					coord=FunctionCallTransformVisitor.TransformCoord
				),
				coord=FunctionCallTransformVisitor.TransformCoord
			),
			iftrue=c_ast.Goto(self.config.returnLabel,
				coord=FunctionCallTransformVisitor.TransformCoord),
			iffalse=None,
			coord=FunctionCallTransformVisitor.TransformCoord
		)
	
	def visit_Compound(self, node, parents):
		parents.append(node)
		if node.block_items is not None:
			i=0
			while i < len(node.block_items):
				res = self.funcCallFinder.visit(node.block_items[i])
				if res:
					node.block_items.insert(i+1,self.ifCheck)
					i+=2
				else:
					self.visit(node.block_items[i])
					i+=1
		parents.pop()
		return None
	
	def treatStmtList(self, node, parents):
		parents.append(node)
		if node.stmts is not None:
			i=0
			while i < len(node.stmts):
				res = self.funcCallFinder.visit(node.stmts[i])
				if res:
					node.stmts.insert(i+1,self.ifCheck)
					i+=2
				else:
					self.visit(node.stmts[i])
					i+=1
		parents.pop()
		return None
	
	def visit_Case(self, node, parents):
		return self.treatStmtList(node, parents)
	
	def visit_Default(self, node, parents):
		return self.treatStmtList(node, parents)
	
	def treatSingleStmt(self, node, parents):
		parents.append(node)
		res = self.funcCallFinder.visit(node.stmt)
		if res:
			node.stmt = c_ast.Compound([
				node.stmt,
				self.ifCheck
			],
			coord=FunctionCallTransformVisitor.TransformCoord)
		else:
			self.visit(node.stmt)
		parents.pop()
		return None
	
	def visit_Label(self, node, parents):
		return self.treatSingleStmt(node,parents)
	
	def visit_While(self, node, parents):
		return self.treatSingleStmt(node,parents)
	
	def visit_For(self, node, parents):
		return self.treatSingleStmt(node,parents)
	
	def visit_DoWhile(self, node, parents):
		return self.treatSingleStmt(node,parents)
	
	def visit_If(self, node, parents):
		parents.append(node)
		res = self.funcCallFinder.visit(node.iftrue)
		if res:
			node.iftrue = c_ast.Compound([
				node.iftrue,
				self.ifCheck
			],
			coord=FunctionCallTransformVisitor.TransformCoord)
		else:
			self.visit(node.iftrue)
		if node.iffalse is not None:
			res = self.funcCallFinder.visit(node.iffalse)
			if res:
				node.iffalse = c_ast.Compound([
					node.iffalse,
					self.ifCheck
				],
				coord=FunctionCallTransformVisitor.TransformCoord)
			else:
				self.visit(node.iffalse)
		parents.pop()
		return None

class FuncCallFinderVisitor(c_ast.NodeVisitor):
	def __init__(self):
		self.argumentChecker = ArgumentCheckerVisitor()

	def visit_FuncCall(self, node):
		if node.args is not None:
			self.argumentChecker.visit(node.args)
		return True

	def visit_Compound(self, node):
		return False

	def visit_Case(self, node):
		return False
	
	def visit_Default(self, node):
		return False
	
	def visit_Label(self, node):
		return False
	
	def visit_While(self, node):
		return False
	
	def visit_For(self, node):
		return False
	
	def visit_DoWhile(self, node):
		return False
	
	def visit_If(self, node):
		return False
	
	def generic_visit(self, node):
		r = False
		for c in node:
			if self.visit(c):
				r = True
		return r

class ArgumentCheckerVisitor(c_ast.NodeVisitor):
	def visit_FuncCall(self, node):
		raise TransformationException("Found nested function call, cannot currently handle such constructs.",
										node.coord)
	# TODO(steuber): No nested function calls yet...