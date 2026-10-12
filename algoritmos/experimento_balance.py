"""TP4 - Experimentos de desbalance: BST comun vs AVL.

Que hace: arma los dos arboles insertando los juegos UNO POR UNO (con agregar)
en distintos ordenes y mide la altura, el tiempo de armado y el tiempo de
busqueda. La idea es provocar el caso malo del BST comun: si los nombres entran
ya ordenados, cada juego nuevo cuelga a la derecha del anterior y el arbol queda
como una lista enlazada (altura n, busqueda O(n)). El AVL, en cambio, rota
mientras inserta y mantiene la altura en O(log n).

Importante: NO se usa construir_arbol(), porque esa funcion ordena la lista y
arma el arbol partiendo por la mitad, o sea que el BST quedaria balanceado de
todas formas. Aca el desbalance se provoca justamente insertando con agregar().

Se ejecuta desde la raiz del proyecto (NextPlay):
python -m algoritmos.experimento_balance
"""
import math
import random
import sys
import time

from algoritmos.medicion import DATASETS
from servicios.index import cargar_juegos
from estructuras.arbol_busqueda_nombre import Arbol as ArbolBST
from estructuras.arbol_avl import Arbol as ArbolAVL

# Ordenes de insercion que se prueban.
ORDENES = ("ordenado A-Z", "ordenado Z-A", "aleatorio")


def ordenar_juegos(juegos, orden, semilla=42):
	"""Devuelve una copia de la lista de juegos en el orden de insercion pedido."""
	if orden == "ordenado A-Z":
		return sorted(juegos, key=lambda j: j.name.lower())
	if orden == "ordenado Z-A":
		return sorted(juegos, key=lambda j: j.name.lower(), reverse=True)
	copia = list(juegos)
	random.Random(semilla).shuffle(copia)
	return copia


def contar_rotaciones(arbol):
	"""Hace que el AVL cuente cuantas rotaciones simples se hacen.

	Una rotacion doble (izquierda-derecha o derecha-izquierda) son dos
	rotaciones simples seguidas, por eso se cuentan como 2.
	"""
	arbol.rotaciones = 0
	original_derecha = arbol.rotacion_derecha
	original_izquierda = arbol.rotacion_izquierda

	def rotacion_derecha(nodo):
		arbol.rotaciones += 1
		return original_derecha(nodo)

	def rotacion_izquierda(nodo):
		arbol.rotaciones += 1
		return original_izquierda(nodo)

	arbol.rotacion_derecha = rotacion_derecha
	arbol.rotacion_izquierda = rotacion_izquierda


def armar(clase_arbol, juegos):
	"""Inserta los juegos de a uno con agregar() y devuelve (arbol, segundos)."""
	arbol = clase_arbol()
	if clase_arbol is ArbolAVL:
		contar_rotaciones(arbol)
	inicio = time.perf_counter()
	for juego in juegos:
		arbol.agregar(juego)
	return arbol, time.perf_counter() - inicio


def tiempo_busqueda(arbol, nombres, repeticiones=3):
	"""Tiempo promedio de UNA busqueda (en segundos) sobre una lista de nombres."""
	inicio = time.perf_counter()
	for _ in range(repeticiones):
		for nombre in nombres:
			arbol.buscar(nombre)
	return (time.perf_counter() - inicio) / (repeticiones * len(nombres))


def experimento(cantidad_busquedas=100, semilla=42):
	"""Corre el experimento sobre los 3 catalogos y devuelve una fila por caso."""
	resultados = []
	limite_original = sys.getrecursionlimit()

	for tamaño, ruta in DATASETS.items():
		juegos = cargar_juegos(ruta)
		# El BST degenerado tiene tantos niveles como juegos, y agregar/buscar son
		# recursivas: hay que subir el limite de recursion de Python para que no falle.
		sys.setrecursionlimit(max(limite_original, len(juegos) + 1000))
		azar = random.Random(semilla)
		nombres = [j.name for j in azar.sample(juegos, min(cantidad_busquedas, len(juegos)))]

		for orden in ORDENES:
			en_orden = ordenar_juegos(juegos, orden, semilla)
			bst, t_armado_bst = armar(ArbolBST, en_orden)
			avl, t_armado_avl = armar(ArbolAVL, en_orden)

			resultados.append({
				"tamaño": tamaño,
				"orden": orden,
				"altura_ideal": math.ceil(math.log2(len(juegos) + 1)),
				"altura_bst": bst.altura(),
				"altura_avl": avl.altura(),
				"rotaciones_avl": avl.rotaciones,
				"armado_bst_ms": t_armado_bst * 1000,
				"armado_avl_ms": t_armado_avl * 1000,
				"busqueda_bst_ms": tiempo_busqueda(bst, nombres) * 1000,
				"busqueda_avl_ms": tiempo_busqueda(avl, nombres) * 1000,
			})

	sys.setrecursionlimit(limite_original)
	return resultados


def imprimir_tablas(resultados):
	"""Imprime los resultados como tablas Markdown (alturas y tiempos)."""
	print("### Altura final del arbol\n")
	print("| Catálogo | Orden de inserción | Altura ideal (log2) | Altura BST | Altura AVL | Rotaciones del AVL |")
	print("|---|---|---|---|---|---|")
	for f in resultados:
		print(f"| {f['tamaño']} | {f['orden']} | {f['altura_ideal']} | {f['altura_bst']} | {f['altura_avl']} | {f['rotaciones_avl']} |")

	print("\n### Tiempos (promedio por operación)\n")
	print("| Catálogo | Orden de inserción | Búsqueda BST | Búsqueda AVL | Armado BST (total) | Armado AVL (total) |")
	print("|---|---|---|---|---|---|")
	for f in resultados:
		print(
			f"| {f['tamaño']} | {f['orden']} "
			f"| {f['busqueda_bst_ms']:.5f} ms | {f['busqueda_avl_ms']:.5f} ms "
			f"| {f['armado_bst_ms']:.2f} ms | {f['armado_avl_ms']:.2f} ms |"
		)


if __name__ == "__main__":
	print("Insertando juegos de a uno en BST y AVL (puede tardar unos segundos)...\n")
	imprimir_tablas(experimento())
