from pycparser import c_ast

class InputFinder(c_ast.NodeVisitor):
	def __init__(self, configParam):
		self.config = configParam
		self.inputVars = []
	
	def visit_FuncDef(self, node):
		if node.decl.name==self.config.function:
			assert(isinstance(node.decl.type, c_ast.FuncDecl))
			if node.decl.type.args is not None:
				for p in node.decl.type.args.params:
					self.inputVars.append(p)

	
	def getInputVars(self):
		return self.inputVars