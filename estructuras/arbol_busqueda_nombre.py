class Nodo ():
	def __init__(self,valor):
		self.valor = valor
		self.izquierda = None
		self.derecha = None


class Arbol():
	# crea el arbol sin ningun nodo
	def __init__(self):
		self.raiz = None
	
	# si la raiz es None, crea un nodo con el valor y lo asigna a la raiz.
	def agregar(self,valor):
		if self.raiz == None:
			self.raiz = Nodo(valor)
		#si la raiz no es None, llama a la funcion recursiva
		else:
			self._agregar_recursivo(self.raiz, valor)
	
	# asigna los valores a derecha o izquierda 
	def _agregar_recursivo(self, nodo, valor):
		# si el name es menor (en el alfabeto) que el del nodo actual.
		if valor.name.lower() < nodo.valor.name.lower():
			# verifica si es None lo agrega a la izquierda.
			if nodo.izquierda is None:
				nodo.izquierda = Nodo(valor)
			# si no, llama a recursivo con el nodo de la izquierda
			else:
				self._agregar_recursivo(nodo.izquierda, valor)
		# si el name es mayor o igual (en el alfabeto) que el del nodo actual.
		else:
			# verifica si en None lo agrega a la derecha.
			if nodo.derecha is None:
				nodo.derecha = Nodo(valor)
			# si no, llama a recursivo con el nodo de la derecha.
			else:
				self._agregar_recursivo(nodo.derecha, valor)
# ---------------------------------------------------------------------------------#
	# si la raiz en None retorna None, si no llama a buscar recursivo.
	def buscar(self, name):
		if self.raiz is None:
			return None
		else:
			return self._buscar_recursivo(self.raiz, name)

	# funcion recursiva que busca un nombre en el arbol.
	def _buscar_recursivo(self, nodo, name):
		#si el nodo en None retorna None.
		if nodo is None: 
			return None
		# si el name del nodo es igual a name  retorna el valor. (game completo)
		if nodo.valor.name.lower() == name.lower():
			return nodo.valor
		# si el name es menor que el name del nodo.
		elif name.lower() < nodo.valor.name.lower():
			# llama a la funcion recursiva con el nodo de la izquierda.
			return self._buscar_recursivo(nodo.izquierda, name)
		else:
			# si es mayor llama a la funcion recursiva con el nodo de la derecha.
			return self._buscar_recursivo(nodo.derecha, name)
