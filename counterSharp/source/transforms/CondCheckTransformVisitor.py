import logging

from pycparser import c_ast

from .TransformationException import TransformationException
from .TransformVisitor import TransformVisitor

logger = logging.getLogger(__name__)

"""
Transforms function call AST node into condition check for a given function identifier and status variable identifier
"""
class CondCheckTransformVisitor(TransformVisitor):

	ResultVarCount=0

	def __init__(self, configParam, functionIdentifierParam, statusVarIdentifierParam):
		self.config = configParam
		self.functionIdentifier = functionIdentifierParam
		self.statusVarIdentifier = statusVarIdentifierParam

	def visit_FuncCall(self, node, parents):
		if node.name.name != self.functionIdentifier:
			parents.append(node)
			res = self.visit(node.args,parents)
			if res is not None:
				node.args=res
			parents.pop()
			return None
		# Node is a condition check
		parent = parents[-1]
		if not isinstance(parent, c_ast.Compound)\
			and not isinstance(parent, c_ast.Case)\
			and not isinstance(parent, c_ast.Default)\
			and not isinstance(parent, c_ast.Label):
			# Invalid positioning for condition check
			raise TransformationException("Call to %s cannot be used as expression!" % (self.functionIdentifier), node.coord)
		if node.args is None or node.args.exprs is None:
			raise TransformationException("Call to %s: Expected 1 parameter, but got 0" % (self.functionIdentifier), node.coord)
		if len(node.args.exprs) != 1:
			raise TransformationException("Call to %s: Expected 1 parameter, but got %d" % (self.functionIdentifier, len(node.args.exprs)), node.coord)
		return self.buildCheck(node, parents)

	def buildCheck(self, node, parents):
		curType=None
		for curN in parents[::-1]:
			if isinstance(curN, c_ast.FuncDef):
				curType = curN.decl.type.type
				break
		if curType is None:
			raise TransformationException("Call to %s outside function definition" % (self.functionIdentifier), node.coord)
		varName = self.config.resultVar+str(CondCheckTransformVisitor.ResultVarCount)
		CondCheckTransformVisitor.ResultVarCount+=1
		compoundStmts = [
			c_ast.Assignment('=',
				c_ast.ID(self.statusVarIdentifier,coord=CondCheckTransformVisitor.TransformCoord),
				c_ast.Constant('int', 1, coord=CondCheckTransformVisitor.TransformCoord),
				coord=CondCheckTransformVisitor.TransformCoord),
		]
		if isinstance(curType, c_ast.TypeDecl) and isinstance(curType.type, c_ast.IdentifierType) and "void" in curType.type.names:
			compoundStmts.append(c_ast.Return(None))
		else:
			compoundStmts.append(c_ast.Decl(
					varName,
					[], [], [],
					c_ast.TypeDecl(varName, [], curType,
						coord=CondCheckTransformVisitor.TransformCoord),
					None,
					None,
					coord=CondCheckTransformVisitor.TransformCoord))
			compoundStmts.append(c_ast.Return(c_ast.ID(varName,coord=CondCheckTransformVisitor.TransformCoord),coord=CondCheckTransformVisitor.TransformCoord))
		tCompound = c_ast.Compound(compoundStmts)
		ifStmt = c_ast.If(node.args.exprs[0],tCompound,c_ast.EmptyStatement(coord=CondCheckTransformVisitor.TransformCoord),coord=CondCheckTransformVisitor.TransformCoord)
		return ifStmt