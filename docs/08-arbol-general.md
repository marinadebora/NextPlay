# TP5 — Árbol general de categorías (versión 3)

Este documento describe el árbol general (n-ario) que se incorporó en el TP5: qué jerarquía representa, cómo está implementado, qué complejidad tienen sus operaciones, cómo se recorre y dónde se usa en la aplicación.

Código involucrado:

| Archivo | Qué es |
|---|---|
| `estructuras/arbol_genral.py` | `Nodo` y `Arbol`: el árbol general, sus operaciones y sus recorridos. |
| `algoritmos/construir_arbol_general.py` | Arma el árbol a partir del catálogo y consulta una categoría. |
| `config/generos.py`, `config/plataformas.py` | Nombres de géneros y plataformas que ofrece el menú. |
| `ui/version3.py` | Versión 3 de la aplicación (el filtro por género/plataforma usa el árbol). |
| `tests/test_arbol_general.py` | Pruebas del árbol general. |

## 1. La jerarquía

Los videojuegos del catálogo ya vienen clasificados: cada juego tiene una lista de **géneros** y una lista de **plataformas**. Esa clasificación es una jerarquía natural del dominio, y se representa con un árbol por cada criterio:

```text
genres                         platform
├── Action                     ├── PC
│   ├── Half-Life: Source      │   ├── Half-Life: Source
│   └── Batman: Arkham Asylum  │   └── Age of Wonders III
├── RPG                        ├── Xbox One
│   ├── Age of Wonders III     │   └── Batman: Arkham Asylum
│   └── ...                    └── ...
└── ...
```

- **Nivel 0 (raíz):** el criterio de clasificación (`genres` o `platform`).
- **Nivel 1:** una categoría por cada valor distinto (Action, RPG, Indie... o PC, Xbox One...).
- **Nivel 2 (hojas):** los juegos que pertenecen a esa categoría.

Un juego con varios géneros aparece una vez bajo **cada** uno de ellos (por ejemplo, un juego `Action, RPG` cuelga de Action y de RPG). Los nodos son distintos, pero todos apuntan al mismo objeto `VideoJuego`.

### ¿Por qué un árbol general y no otra estructura?

- **No es un árbol binario ni un BST:** una categoría tiene tantos hijos como juegos pertenezcan a ella, no hay un máximo de dos. Y entre categorías no hay un orden natural (¿Action es "menor" que RPG?) que justifique ordenarlas como en un BST.
- **No alcanza con una lista plana:** la jerarquía raíz → categoría → juego es justamente lo que permite "explorar categorías" y recorrerla por niveles.
- **Utilidad real:** el filtro por género y por plataforma de la versión 3 resuelve la consulta sobre este árbol, en lugar de recorrer todo el catálogo.

## 2. Implementación

```python
class Nodo:
  valor     # texto (criterio o categoría) o un VideoJuego (hoja)
  hijos     # lista de nodos hijo, sin límite de cantidad

class Arbol:
  raiz        # Nodo con el criterio: "genres" o "platform"
  categorias  # diccionario {nombre de categoría: nodo de la categoría}
```

`agregar_hijo(juego)` toma las categorías del juego (según el criterio de la raíz), crea el nodo de cada categoría la primera vez que aparece y lo registra en el diccionario `categorias`; después cuelga un nodo hoja con el juego bajo cada una de sus categorías. El diccionario es un **índice auxiliar**: permite llegar al nodo de una categoría sin recorrer la lista de hijos de la raíz.

`construir_arbol_general(criterio, juegos)` crea el árbol y agrega los juegos de a uno.

## 3. Operaciones y complejidad

Se llama **n** a la cantidad de juegos del catálogo, **g** a la cantidad promedio de categorías por juego, **c** a la cantidad de categorías distintas y **k** a la cantidad de juegos de la categoría consultada. La cantidad total de nodos es **N = 1 + c + n·g**.

| Operación | Complejidad | Por qué |
|---|---|---|
| `agregar_hijo(juego)` | O(g) | por cada categoría del juego: una consulta al diccionario (O(1) en promedio) y un `append` |
| `construir_arbol_general` | O(n·g) | se agrega cada uno de los n juegos |
| `buscar_por_categoria(c)` | O(1) en promedio para llegar al nodo; O(k) para leer sus k juegos | acceso directo por el diccionario |
| Buscar una categoría sin el diccionario | O(c) | habría que revisar los hijos de la raíz uno por uno |
| `preorder`, `postorder`, `inorder`, `por_nivel` | O(N) | cada nodo se visita una vez |
| Espacio | O(N) = O(n·g) | un nodo por cada pertenencia juego-categoría |

Nota sobre los recorridos recursivos: cada llamada devuelve una lista que el padre copia con `extend`, así que en la práctica el costo es O(N·h), con h la altura del árbol. Como este árbol tiene altura 2 (tres niveles), h es una constante y queda O(N). `por_nivel` usa una cola (`deque`) para sacar el primer elemento en O(1).

### Comparación con el filtro lineal

El filtro lineal de la versión 1 (`servicios.index.filtrar`) recorre todo el catálogo para cada consulta: O(n). Medida de la consulta "juegos de un género" (promedio de 200 repeticiones, incluyendo armar la lista de resultados; valores de una sola máquina):

| Catálogo | Género | Juegos en la categoría | Filtro lineal | Árbol general |
|---|---|---|---|---|
| 120 juegos | Action | 87 | 0,0394 ms | 0,0017 ms |
| 980 juegos | Action | 634 | 0,3338 ms | 0,0100 ms |
| 8.980 juegos | Action | 4.745 | 3,5285 ms | 0,1003 ms |
| 8.980 juegos | Educational | 53 | 3,2976 ms | 0,0108 ms |

El filtro lineal siempre paga el recorrido del catálogo completo, aunque la categoría tenga pocos juegos; el árbol paga solo por los juegos que devuelve. A cambio, el árbol se construye una sola vez (con 8.980 juegos, unos 11 ms) y ocupa más memoria.

Tamaño real del árbol por género con el catálogo de 120 juegos: 15 categorías, 271 pertenencias (los 120 juegos tienen 271 géneros en total) y por lo tanto 1 + 15 + 271 = 287 nodos.

## 4. Recorridos

El árbol ofrece cuatro recorridos. Se muestran sobre un catálogo chico: los juegos A (`Action`, `RPG`), B (`Action`) y C (`RPG`).

```text
genres
├── Action
│   ├── A
│   └── B
└── RPG
    ├── A
    └── C
```

| Recorrido | Orden de visita | Resultado en el ejemplo |
|---|---|---|
| `preorder` | primero el nodo, después sus hijos de izquierda a derecha | `genres, Action, A, B, RPG, A, C` |
| `postorder` | primero los hijos, al final el nodo | `A, B, Action, A, C, RPG, genres` |
| `por_nivel` | nivel por nivel, de la raíz hacia abajo | `genres, Action, RPG, A, B, A, C` |
| `inorder` | primer hijo, luego el nodo, luego los hijos restantes | `A, Action, B, genres, A, RPG, C` |

Cuándo sirve cada uno:

- **`preorder`** muestra el árbol "como un índice": cada categoría seguida de sus juegos.
- **`postorder`** sirve cuando hay que procesar los hijos antes que el padre (por ejemplo, contar o liberar los juegos de una categoría antes de cerrarla).
- **`por_nivel`** muestra primero todas las categorías y después los juegos, útil para "explorar categorías" de arriba hacia abajo.
- **`inorder`** en un árbol general no tiene una definición única (en un binario es izquierda-raíz-derecha); acá se adoptó la convención de visitar el primer hijo, luego el nodo y luego el resto de los hijos, que coincide con el inorder clásico cuando cada nodo tiene a lo sumo dos hijos.

Todos devuelven una lista con los N valores del árbol (aquí, 7 en el ejemplo; 287 con el catálogo real por género).

## 5. Dónde se usa en la aplicación

En la **versión 3** (`python main.py` → opción 3), la opción 3 del menú ("Filtrar") ofrece:

1. **Por género:** el usuario elige un número del menú de géneros y la aplicación consulta el árbol por género.
2. **Por plataforma:** igual, con el árbol por plataforma.
3. **Por rating mínimo:** usa el BST por rating (TP3).

Las versiones 1 y 2 siguen funcionando sin cambios, como pide la consigna ("cada etapa se suma a la anterior").

## 6. Preguntas para la defensa

- **¿Por qué un árbol general?** Porque una categoría puede tener cualquier cantidad de hijos y el dominio ya es una jerarquía (criterio → categoría → juego). Un BST pide un orden total y como mucho dos hijos por nodo.
- **¿Qué hace el diccionario si ya hay un árbol?** Es un índice auxiliar: evita recorrer los hijos de la raíz para encontrar una categoría (O(c) → O(1)). El árbol sigue siendo el que representa la jerarquía y el que se recorre con `preorder`, `postorder`, `inorder` y `por_nivel`.
- **¿Qué pasa con un juego de varios géneros?** Aparece bajo cada uno de sus géneros (un nodo por pertenencia), por eso hay más nodos juego que juegos.
- **¿Cuál es la altura del árbol?** 2 (tres niveles: criterio, categoría, juego).
- **¿Qué recorrido usarías para listar el árbol "como índice"?** `preorder`. ¿Y nivel por nivel? `por_nivel`.
- **¿Qué complejidad tiene consultar una categoría?** O(1) en promedio para llegar al nodo y O(k) para leer los k juegos, contra O(n) del filtro lineal.
