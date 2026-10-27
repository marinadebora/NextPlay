# NextPlay

**NextPlay** es una aplicación orientada a la recomendación de videojuegos. Su objetivo es ayudar a los usuarios a encontrar videojuegos que se adapten a sus intereses, preferencias y plataforma de juego.

La aplicación utiliza información obtenida de una API especializada en videojuegos. A partir de los datos disponibles, se desarrolló un archivo **JSON** que nos servirá como base de datos para la aplicación.

---
## Integrantes

> **Grupo 8**

- Carabajal Débora
- Ragonese Gianluca

---

## Instrucciones de ejecución

### 1. Clonar el repositorio

Para obtener el proyecto, clonar el repositorio desde GitHub:

```bash
git clone URL_DEL_REPOSITORIO
```
Luego, ingresar a la carpeta del proyecto:
```bash
cd NextPlay
```
### 2. Ejecutar la aplicación

No es necesario instalar dependencias adicionales.

Desde la carpeta del proyecto, ejecutar:
```bash
python main.py
```
### 3. Menú principal

Al iniciar la aplicación, se puede elegir entre la versión 1.0 (TP1/TP2), la versión 2.0 (TP3/TP4, con el árbol binario y el AVL integrados a la búsqueda y al filtro por rating) y la versión 3.0 (TP5, con el árbol general de categorías en el filtro por género y plataforma):
```bash
==== NextPlay ====
1. Versión 1.0
2. Versión 2.0
3. Versión 3.0
0. Salir
```
Las tres versiones comparten el mismo catálogo de juegos (`datos/VideoGames.JSON`) y el mismo menú de opciones:
```bash
=== NextPlay ===
1. Buscar videojuegos por nombre
2. Listar todos los videojuegos
3. Filtrar por genero / plataforma / rating minimo
4. Ver detalle de un videojuego
5. Comparar dos videojuegos
0. Salir
```

## Estructuras de datos (TP3 — árboles binarios de búsqueda)

A partir del TP3, el proyecto usa dos árboles binarios de búsqueda (`estructuras/`), cada uno con su propia **clave de ordenamiento**:

| Árbol | Archivo | Clave de ordenamiento | Dónde se usa |
|---|---|---|---|
| Por nombre | `estructuras/arbol_busqueda_nombre.py` | `name` (título del juego, alfabético) | Búsqueda exacta por nombre (versión 2, opción 1) y medición de TP2 (`algoritmos/medicion.py`) |
| Por rating | `estructuras/arbol_busqueda_rating.py` | `rating` (numérico) | Filtro por rating mínimo (versión 2, opción 3) |

Ambos árboles se construyen balanceados con `algoritmos/construir_arbol.py` (se ordena la lista de juegos por la clave elegida y se toma siempre el elemento del medio como raíz de cada subárbol), e implementan inserción, búsqueda y los 3 recorridos clásicos (`inorder`, `preorder`, `postorder`). El `inorder` del árbol por nombre devuelve el catálogo completo ordenado alfabéticamente sin necesidad de volver a ordenarlo.

La comparación de rendimiento del árbol por nombre contra la búsqueda secuencial del TP2 está en [`docs/06-analisis-complejidad.md`](./docs/06-analisis-complejidad.md).

## Estructuras de datos (TP4 — AVL)

El TP4 suma un **árbol AVL** (`estructuras/arbol_avl.py`), un árbol binario de búsqueda que se mantiene balanceado solo mientras se insertan juegos (factor de balance y las 4 rotaciones: izquierda-izquierda, derecha-derecha, izquierda-derecha y derecha-izquierda).

| Árbol | Archivo | Clave de ordenamiento | Dónde se usa |
|---|---|---|---|
| AVL por nombre | `estructuras/arbol_avl.py` | `name` (alfabético, sin distinguir mayúsculas) | Versión 2: búsqueda por nombre exacto (opción 1) y listado ordenado con `inorder` (opción 2) |

Se arma con `algoritmos/construir_arbol_avl.py`, insertando los juegos de a uno. El experimento que lo compara con el BST común (insertando los nombres ya ordenados, que degrada al BST en una lista enlazada) está en `algoritmos/experimento_balance.py`:

```bash
python -m algoritmos.experimento_balance
```

Los resultados, la explicación del AVL y la conclusión técnica están en [`docs/07-bst-vs-avl.md`](./docs/07-bst-vs-avl.md). Las pruebas del AVL están en `tests/test_avl.py`.

## Estructuras de datos (TP5 — árbol general)

El TP5 suma un **árbol general (n-ario)** de categorías (`estructuras/arbol_genral.py`). A diferencia de los árboles anteriores no se ordena por una clave: representa la jerarquía natural del catálogo, donde cada nodo puede tener cualquier cantidad de hijos.

```text
genres (o platform)
├── Action
│   ├── juego 1
│   └── juego 2
├── RPG
│   └── ...
└── ...
```

| Árbol | Archivo | Jerarquía | Dónde se usa |
|---|---|---|---|
| Por género | `estructuras/arbol_genral.py` (se arma con `algoritmos/construir_arbol_general.py`) | criterio `genres` → género → juegos | Versión 3: filtro por género (opción 3 → 1) |
| Por plataforma | el mismo, con criterio `platform` | criterio `platform` → plataforma → juegos | Versión 3: filtro por plataforma (opción 3 → 2) |

Un juego con más de un género (o plataforma) aparece bajo cada una de sus categorías. El árbol ofrece búsqueda de una categoría y los recorridos `preorder`, `postorder`, `inorder` y `por_nivel`. La explicación de la jerarquía, la complejidad de las operaciones, ejemplos de recorridos y la comparación con el filtro lineal están en [`docs/08-arbol-general.md`](./docs/08-arbol-general.md). Las pruebas están en `tests/test_arbol_general.py`.

## Estructura del repositorio

```text
proyecto/
├── algoritmos/
├── docs/
│   ├──capturas/
│   ├── 01-requerimientos.md
│   ├── 02-casos-de-uso.md
│   ├── 03-diagrama-clases.md
│   ├── 04-diagrama-datos.md
│   ├── 05-gestion-proyecto.md
│   ├── 06-analisis-complejidad.md
│   ├── 07-bst-vs-avl.md
│   ├── 08-arbol-general.md
│   └── 09-heap.md
├── estructuras/
├── datos/
├── modelos/
├── servicios/
├── tests/
├── ui/
├──.gitignore
├── main.py
└── README.md

```
## Documentación

- [Requerimientos](./docs/01-requerimientos.md)
- [Casos de uso](./docs/02-casos-de-uso.md)
- [Diagrama de clases](./docs/03-diagrama-clases.md)
- [Diagrama de datos](./docs/04-diagrama-datos.md)
- [Gestión del proyecto](./docs/05-gestion-proyecto.md)
- [Análisis de complejidad (árbol vs. búsqueda secuencial)](./docs/06-analisis-complejidad.md)
- [Desbalance del árbol y AVL (BST vs. AVL)](./docs/07-bst-vs-avl.md)
- [Árbol general de categorías (versión 3)](./docs/08-arbol-general.md)
- [Heap y Top-N (TP6)](./docs/09-heap.md)
