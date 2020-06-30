import copy
import logging

from pycparser import c_ast

from .TransformVisitor import TransformVisitor

logger = logging.getLogger(__name__)

class ReturnTransformVisitor(TransformVisitor):
	def __init__(self, configParam):
		super().__init__(configParam)

	def visit_FuncDef(self, node, parents):
		isCheckedFunction = (node.decl.name==self.config.function)
		if node.body.block_items is None:
			node.body.block_items = []
		# Insert variable for return value
		isVoidFun = True
		if not isinstance(node.decl.type.type.type,c_ast.IdentifierType) or node.decl.type.type.type.names[0]!="void":
			# Rename function's type...
			type = copy.deepcopy(node.decl.type.type)
			t = type
			while True:
				if hasattr(t,"declname"):
					t.declname=self.config.returnVal
				if hasattr(t,"type"):
					t=t.type
				else:
					break
			# Declare result variable...
			node.body.block_items.insert(0,
				c_ast.Decl(name=self.config.returnVal,
				quals=[],
				storage=[],
				funcspec=[],
				type=type,
				init=None,
				bitsize=None,
				coord=ReturnTransformVisitor.TransformCoord
				)
			)
			isVoidFun=False
		v = ReturnStmtTransformVisitor(self.config, isCheckedFunction)
		v.visit(node.body,[])
		if not v.foundReturn:
			stmtList = []
			if isCheckedFunction:
				stmtList.extend(assertStatementSequence(self.config,ReturnTransformVisitor.TransformCoord))
			if isVoidFun:
				stmtList.append(c_ast.Return(None, coord=ReturnTransformVisitor.TransformCoord))
			else:
				stmtList.append(c_ast.Return(c_ast.ID(name=self.config.returnVal,coord=ReturnTransformVisitor.TransformCoord), coord=ReturnTransformVisitor.TransformCoord))
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
		stmtListOuter = []
		if node.expr is not None:
			returnAssignment = c_ast.Assignment(
				op="=",
				lvalue=c_ast.ID(name=self.config.returnVal,coord=ReturnStmtTransformVisitor.TransformCoord),
				rvalue=node.expr,
				coord=ReturnStmtTransformVisitor.TransformCoord
			)
			stmtListOuter.append(returnAssignment)
		if not self.foundReturn:
			self.foundReturn = True
			stmtListInner = []
			if self.isCheckedFunction:
				stmtListInner.extend(assertStatementSequence(self.config,ReturnStmtTransformVisitor.TransformCoord))
			if node.expr is not None:
				stmtListInner.append(c_ast.Return(c_ast.ID(name=self.config.returnVal,coord=ReturnStmtTransformVisitor.TransformCoord), coord=ReturnStmtTransformVisitor.TransformCoord))
			else:
				stmtListInner.append(node)
			compoundStmt2 = c_ast.Compound(stmtListInner, coord=ReturnStmtTransformVisitor.TransformCoord)
			stmtListOuter.append(c_ast.Label(self.config.returnLabel, compoundStmt2,coord=ReturnStmtTransformVisitor.TransformCoord))
			compoundStmt = c_ast.Compound(stmtListOuter, coord=ReturnStmtTransformVisitor.TransformCoord)
			return compoundStmt
		else:
			stmtListOuter.append(c_ast.Goto(name=self.config.returnLabel,coord=ReturnStmtTransformVisitor.TransformCoord))
			return c_ast.Compound(stmtListOuter, coord=ReturnStmtTransformVisitor.TransformCoord)

def assertStatementBuilder(varName, value,coord):
	return c_ast.FuncCall(
			c_ast.ID("__CPROVER_assert", coord=coord),
			c_ast.ExprList(
				[c_ast.BinaryOp("!=",
					c_ast.ID(name=varName,coord=coord),
					c_ast.Constant('int', value, coord=coord)
					, coord=coord),
				c_ast.Constant('string', "\"\"", coord=coord)]
			, coord=coord)
			, coord=coord)

def assertStatementSequence(config,coord):
	res = []
	for var, val, _ in config.computeOutputs:
		res.append(assertStatementBuilder(var,val,coord))
	return res