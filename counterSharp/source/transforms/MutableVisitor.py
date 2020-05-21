class MutableVisitor(object):
	_method_cache = None

	def visit(self, node, parents=[]):
		""" Visit a node.
		"""

		if self._method_cache is None:
			self._method_cache = {}
		
		if node is None:
			return

		visitor = self._method_cache.get(node.__class__.__name__, None)
		if visitor is None:
			method = 'visit_' + node.__class__.__name__
			visitor = getattr(self, method, None)
			if visitor is None:
				raise Exception("Missing method %s" % (method))
			self._method_cache[node.__class__.__name__] = visitor

		return visitor(node, parents)

	def visit_ArrayDecl(self, node, parents):
		parents.append(node)
		res = self.visit(node.type,parents)
		if res is not None:
			node.type=res
		res = self.visit(node.dim,parents)
		if res is not None:
			node.dim=res
		parents.pop()

	def visit_ArrayRef(self, node, parents):
		parents.append(node)
		res = self.visit(node.name,parents)
		if res is not None:
			node.name=res
		res = self.visit(node.subscript,parents)
		if res is not None:
			node.subscript=res
		parents.pop()

	def visit_Assignment(self, node, parents):
		parents.append(node)
		res = self.visit(node.lvalue,parents)
		if res is not None:
			node.lvalue=res
		res = self.visit(node.rvalue,parents)
		if res is not None:
			node.rvalue=res
		parents.pop()

	def visit_BinaryOp(self, node, parents):
		parents.append(node)
		res = self.visit(node.left,parents)
		if res is not None:
			node.left=res
		res = self.visit(node.right,parents)
		if res is not None:
			node.right=res
		parents.pop()

	def visit_Case(self, node, parents):
		parents.append(node)
		res = self.visit(node.expr,parents)
		if res is not None:
			node.expr=res
		if node.stmts is not None:
			for i in range(0,len(node.stmts)):
				res = self.visit(node.stmts[i],parents)
				if res is not None:
					node.stmts[i]=res
		parents.pop()

	def visit_Cast(self, node, parents):
		parents.append(node)
		res = self.visit(node.to_type,parents)
		if res is not None:
			node.to_type=res
		res = self.visit(node.expr,parents)
		if res is not None:
			node.expr=res
		parents.pop()

	def visit_Compound(self, node, parents):
		parents.append(node)
		if node.block_items is not None:
			for i in range(0,len(node.block_items)):
				res = self.visit(node.block_items[i],parents)
				if res is not None:
					node.block_items[i]=res
		parents.pop()

	def visit_CompoundLiteral(self, node, parents):
		parents.append(node)
		res = self.visit(node.type,parents)
		if res is not None:
			node.type=res
		res = self.visit(node.init,parents)
		if res is not None:
			node.init=res
		parents.pop()

	def visit_Decl(self, node, parents):
		parents.append(node)
		res = self.visit(node.type,parents)
		if res is not None:
			node.type=res
		res = self.visit(node.init,parents)
		if res is not None:
			node.init=res
		res = self.visit(node.bitsize,parents)
		if res is not None:
			node.bitsize=res
		parents.pop()

	def visit_DeclList(self, node, parents):
		parents.append(node)
		if node.decls is not None:
			for i in range(0,len(node.decls)):
				res = self.visit(node.decls[i],parents)
				if res is not None:
					node.decls[i]=res
		parents.pop()

	def visit_Default(self, node, parents):
		parents.append(node)
		if node.stmts is not None:
			for i in range(0,len(node.stmts)):
				res = self.visit(node.stmts[i],parents)
				if res is not None:
					node.stmts[i]=res
		parents.pop()

	def visit_DoWhile(self, node, parents):
		parents.append(node)
		res = self.visit(node.cond,parents)
		if res is not None:
			node.cond=res
		res = self.visit(node.stmt,parents)
		if res is not None:
			node.stmt=res
		parents.pop()

	def visit_Enum(self, node, parents):
		parents.append(node)
		res = self.visit(node.values,parents)
		if res is not None:
			node.values=res
		parents.pop()

	def visit_Enumerator(self, node, parents):
		parents.append(node)
		res = self.visit(node.value,parents)
		if res is not None:
			node.value=res
		parents.pop()

	def visit_EnumeratorList(self, node, parents):
		parents.append(node)
		if node.enumerators is not None:
			for i in range(0,len(node.enumerators)):
				res = self.visit(node.enumerators[i],parents)
				if res is not None:
					node.enumerators[i]=res
		parents.pop()

	def visit_ExprList(self, node, parents):
		parents.append(node)
		if node.exprs is not None:
			for i in range(0,len(node.exprs)):
				res = self.visit(node.exprs[i],parents)
				if res is not None:
					node.exprs[i]=res
		parents.pop()

	def visit_FileAST(self, node, parents):
		parents.append(node)
		if node.ext is not None:
			for i in range(0,len(node.ext)):
				res = self.visit(node.ext[i],parents)
				if res is not None:
					node.ext[i]=res
		parents.pop()

	def visit_For(self, node, parents):
		parents.append(node)
		res = self.visit(node.init,parents)
		if res is not None:
			node.init=res
		res = self.visit(node.cond,parents)
		if res is not None:
			node.cond=res
		res = self.visit(node.next,parents)
		if res is not None:
			node.next=res
		res = self.visit(node.stmt,parents)
		if res is not None:
			node.stmt=res
		parents.pop()

	def visit_FuncCall(self, node, parents):
		parents.append(node)
		res = self.visit(node.name,parents)
		if res is not None:
			node.name=res
		res = self.visit(node.args,parents)
		if res is not None:
			node.args=res
		parents.pop()

	def visit_FuncDecl(self, node, parents):
		parents.append(node)
		res = self.visit(node.args,parents)
		if res is not None:
			node.args=res
		res = self.visit(node.type,parents)
		if res is not None:
			node.type=res
		parents.pop()

	def visit_FuncDef(self, node, parents):
		parents.append(node)
		res = self.visit(node.decl,parents)
		if res is not None:
			node.decl=res
		res = self.visit(node.body,parents)
		if res is not None:
			node.body=res
		if node.param_decls is not None:
			for i in range(0,len(node.param_decls)):
				res = self.visit(node.param_decls[i],parents)
				if res is not None:
					node.param_decls[i]=res
		parents.pop()

	def visit_If(self, node, parents):
		parents.append(node)
		res = self.visit(node.cond,parents)
		if res is not None:
			node.cond=res
		res = self.visit(node.iftrue,parents)
		if res is not None:
			node.iftrue=res
		res = self.visit(node.iffalse,parents)
		if res is not None:
			node.iffalse=res
		parents.pop()

	def visit_InitList(self, node, parents):
		parents.append(node)
		if node.exprs is not None:
			for i in range(0,len(node.exprs)):
				res = self.visit(node.exprs[i],parents)
				if res is not None:
					node.exprs[i]=res
		parents.pop()

	def visit_Label(self, node, parents):
		parents.append(node)
		res = self.visit(node.stmt,parents)
		if res is not None:
			node.stmt=res
		parents.pop()

	def visit_NamedInitializer(self, node, parents):
		parents.append(node)
		res = self.visit(node.expr,parents)
		if res is not None:
			node.expr=res
		if node.name is not None:
			for i in range(0,len(node.name)):
				res = self.visit(node.name[i],parents)
				if res is not None:
					node.name[i]=res
		parents.pop()

	def visit_ParamList(self, node, parents):
		parents.append(node)
		if node.params is not None:
			for i in range(0,len(node.params)):
				res = self.visit(node.params[i],parents)
				if res is not None:
					node.params[i]=res
		parents.pop()

	def visit_PtrDecl(self, node, parents):
		parents.append(node)
		res = self.visit(node.type,parents)
		if res is not None:
			node.type=res
		parents.pop()

	def visit_Return(self, node, parents):
		parents.append(node)
		res = self.visit(node.expr,parents)
		if res is not None:
			node.expr=res
		parents.pop()

	def visit_Struct(self, node, parents):
		parents.append(node)
		if node.decls is not None:
			for i in range(0,len(node.decls)):
				res = self.visit(node.decls[i],parents)
				if res is not None:
					node.decls[i]=res
		parents.pop()

	def visit_StructRef(self, node, parents):
		parents.append(node)
		res = self.visit(node.name,parents)
		if res is not None:
			node.name=res
		res = self.visit(node.field,parents)
		if res is not None:
			node.field=res
		parents.pop()

	def visit_Switch(self, node, parents):
		parents.append(node)
		res = self.visit(node.cond,parents)
		if res is not None:
			node.cond=res
		res = self.visit(node.stmt,parents)
		if res is not None:
			node.stmt=res
		parents.pop()

	def visit_TernaryOp(self, node, parents):
		parents.append(node)
		res = self.visit(node.cond,parents)
		if res is not None:
			node.cond=res
		res = self.visit(node.iftrue,parents)
		if res is not None:
			node.iftrue=res
		res = self.visit(node.iffalse,parents)
		if res is not None:
			node.iffalse=res
		parents.pop()

	def visit_TypeDecl(self, node, parents):
		parents.append(node)
		res = self.visit(node.type,parents)
		if res is not None:
			node.type=res
		parents.pop()

	def visit_Typedef(self, node, parents):
		parents.append(node)
		res = self.visit(node.type,parents)
		if res is not None:
			node.type=res
		parents.pop()

	def visit_Typename(self, node, parents):
		parents.append(node)
		res = self.visit(node.type,parents)
		if res is not None:
			node.type=res
		parents.pop()

	def visit_UnaryOp(self, node, parents):
		parents.append(node)
		res = self.visit(node.expr,parents)
		if res is not None:
			node.expr=res
		parents.pop()

	def visit_Union(self, node, parents):
		parents.append(node)
		if node.decls is not None:
			for i in range(0,len(node.decls)):
				res = self.visit(node.decls[i],parents)
				if res is not None:
					node.decls[i]=res
		parents.pop()

	def visit_While(self, node, parents):
		parents.append(node)
		res = self.visit(node.cond,parents)
		if res is not None:
			node.cond=res
		res = self.visit(node.stmt,parents)
		if res is not None:
			node.stmt=res
		parents.pop()
	
	def visit_Break(self, node, parents):
		return

	def visit_Constant(self, node, parents):
		return
	
	def visit_Continue(self, node, parents):
		parents.append(node)
		return
	
	def visit_EllipsisParam(self, node, parents):
		return
	
	def visit_EmptyStatement(self, node, parents):
		return
	
	def visit_Goto(self, node, parents):
		return
	
	def visit_ID(self, node, parents):
		return
	
	def visit_IdentifierType(self, node, parents):
		return
	
	def visit_Pragma(self, node, parents):
		return