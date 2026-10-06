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

# ---------------------------------------------------------------------------------#
	# TIPOS DE RECORRIDO (TP3)
	# preorder: raiz, izquierda, derecha
	def preorder(self, nodo):
		lista = []
		if nodo is None:
			return lista
		else:
			return self.preorder_recursivo(nodo, lista)

	def preorder_recursivo(self, nodo, lista):
		if nodo is None:
			return
		lista.append(nodo.valor)
		self.preorder_recursivo(nodo.izquierda, lista)
		self.preorder_recursivo(nodo.derecha, lista)
		return lista

	# inorder: izquierda, raiz, derecha.
	# Sobre este arbol (ordenado por name) el inorder da la lista completa
	# ordenada alfabeticamente "gratis", sin volver a ordenar.
	def inorder(self, nodo):
		lista = []
		if nodo is None:
			return lista
		else:
			return self.inorder_recursivo(nodo, lista)

	def inorder_recursivo(self, nodo, lista):
		if nodo is None:
			return
		self.inorder_recursivo(nodo.izquierda, lista)
		lista.append(nodo.valor)
		self.inorder_recursivo(nodo.derecha, lista)
		return lista

	# postorder: izquierda, derecha, raiz
	def postorder(self, nodo):
		lista = []
		if nodo is None:
			return lista
		else:
			return self.postorder_recursivo(nodo, lista)

	def postorder_recursivo(self, nodo, lista):
		if nodo is None:
			return
		self.postorder_recursivo(nodo.izquierda, lista)
		self.postorder_recursivo(nodo.derecha, lista)
		lista.append(nodo.valor)
		return lista
