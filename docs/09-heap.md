# TP6 — Heap (cola de prioridad)

Este documento describe la heap que se incorporó en el TP6: cómo está implementada, qué complejidad tiene cada operación y por qué conviene frente a ordenar el catálogo cada vez que se necesita un ranking.

Código involucrado:

| Archivo | Qué es |
|---|---|
| `estructuras/heap.py` | La clase `Heap` (implementada a mano, sin `heapq`). |
| `tests/test_heap.py` | Pruebas de la heap. |

## 1. Qué es y cómo se guarda

Una heap binaria es un árbol binario *completo* que cumple la regla de orden: **cada elemento "va antes" que sus dos hijos**. En una heap de máximo la raíz es el mayor; en una de mínimo, el menor. La clase `Heap` acepta una función `clave` (por ejemplo `lambda j: j.rating`) y el parámetro `maximo` para elegir el sentido.

Como el árbol es completo, se guarda en una lista de Python sin nodos ni punteros. Para la posición `i`:

- hijo izquierdo: `2*i + 1`
- hijo derecho: `2*i + 2`
- padre: `(i - 1) // 2`

```text
lista:  [9.0, 7.5, 8.0, 5.0, 6.0, 4.5]

            9.0            (posición 0)
          /     \
       7.5       8.0       (posiciones 1 y 2)
      /   \      /
    5.0   6.0  4.5         (posiciones 3, 4 y 5)
```

## 2. Operaciones y complejidad

| Operación | Qué hace | Complejidad |
|---|---|---|
| `ver_raiz()` | Devuelve el primero de la prioridad sin sacarlo. | O(1) |
| `insertar(x)` | Agrega al final y lo hace **subir** hasta que se cumple la regla. | O(log n) |
| `extraer()` | Saca la raíz, pone el último en su lugar y lo hace **bajar**. | O(log n) |
| `Heap.desde_lista(lista)` | Arma la heap desde una lista ya existente (heapify). | O(n) |
| `top_n(n)` | Devuelve los `n` primeros en orden, **sin modificar** la heap. | O(n·log n) en el tamaño del pedido, no del catálogo |

El peor caso de `insertar` y `extraer` es O(log n) porque el elemento recorre, como mucho, la altura del árbol, que en un árbol completo es ⌊log₂ n⌋.

Armar la heap con `desde_lista` es O(n) (y no O(n·log n) como insertar de a uno) porque se repara desde la mitad hacia la raíz: la mayoría de los nodos están cerca de las hojas y bajan muy poco.

### Cómo funciona `top_n`

Extraer `n` veces de la heap la destruiría. En su lugar, `top_n` usa una heap auxiliar de *posiciones candidatas*: empieza con la raíz, y cada vez que saca la mejor candidata agrega sus dos hijos. Así el siguiente mejor del catálogo siempre está entre las candidatas. Se hacen `n` extracciones sobre una heap auxiliar de tamaño a lo sumo `n + 1`, por lo que el costo depende de `n` y no del tamaño del catálogo.

## 3. Heap vs. ordenar cada vez

Para mostrar el Top-10 por rating hay dos caminos:

- **Ordenar todo** el catálogo y quedarse con los primeros 10: O(n·log n) **cada vez**.
- **Armar la heap una vez** (O(n)) y pedir el Top-10 con `top_n`: cada consulta cuesta O(10·log 10), independiente de n. Si además entran juegos nuevos, `insertar` cuesta O(log n) en lugar de reordenar todo.

Mediciones en este proyecto (Top-10 por rating, promedio de varias corridas, en milisegundos):

| Catálogo | Armar la heap (una vez) | Top-10 con heap | Ordenar todo y cortar |
|---|---|---|---|
| 120 juegos | 0.07 | 0.031 | 0.012 |
| 980 juegos | 0.70 | 0.034 | 0.125 |
| 8.980 juegos | 5.48 | 0.028 | 1.69 |

Lectura de los resultados:

- El tiempo del Top-10 con heap **casi no cambia** al crecer el catálogo (≈ 0,03 ms), mientras que ordenar crece con n.
- Con catálogos chicos (120 juegos) ordenar es igual de rápido o incluso más: el `sorted` de Python está escrito en C y la heap en Python puro. La ventaja aparece cuando el catálogo crece o cuando el ranking se consulta muchas veces.
- Armar la heap cuesta una sola vez; se amortiza desde la segunda consulta con un catálogo grande.

Las dos opciones cumplen el requisito de la historia de usuario (Top-10 en menos de 1 segundo con 10.000 elementos); la heap es la que escala mejor y la que además permite insertar sin reordenar.

## 4. Alternativas consideradas

| Alternativa | Costo de armar | Costo de un Top-N | Costo de insertar uno nuevo |
|---|---|---|---|
| Ordenar el catálogo cada vez | — | O(n·log n) | — |
| Lista ordenada mantenida | O(n·log n) | O(N) | O(n) (hay que desplazar) |
| BST por rating (TP3) | O(n·log n) promedio | O(log n + N) | O(log n) promedio, O(n) si se desbalancea |
| AVL por rating | O(n·log n) | O(log n + N) | O(log n) garantizado |
| **Heap** | **O(n)** | **O(N·log N)** | **O(log n) garantizado** |

La heap no sirve para buscar un elemento cualquiera (eso es O(n)); sólo da acceso rápido al de mayor prioridad. Por eso **no reemplaza** a los árboles de búsqueda: los complementa en la parte de ranking.

## 5. Integración en NextPlay — Versión 4

La heap se integra en el menú principal de NextPlay, versión 4. Al ingresar, se muestra automáticamente un Top-5 de los videojuegos con mayor rating. Además, la opción 6 permite generar rankings dinámicos, seleccionando la cantidad de videojuegos y el orden según su rating, de mayor a menor o de menor a mayor.

### Función de prioridad

La función `prioridad(juego)` devuelve el atributo `_rating` del videojuego. Este valor se utiliza como clave para determinar la prioridad de cada elemento.

```python
def prioridad(juego):
    return juego._rating
```

### Generación del ranking

La función `nuevo_ranking(juegos)` solicita al usuario la cantidad de videojuegos que desea consultar y el sentido del ranking: de mayor a menor rating o de menor a mayor rating.

La función `mostrar_ranking(juegos, func, maximo, n)` crea la heap mediante `crear_ranking()`, obtiene los primeros `n` elementos con `top_n(n)` y muestra los videojuegos con su posición, nombre y rating.

Las tres primeras posiciones se destacan mediante medallas.

### Complejidad de la integración

En la implementación actual, cada consulta construye la heap a partir del catálogo y luego obtiene los primeros `n` elementos.

Por lo tanto, el costo total incluye la construcción de la heap, O(n), y la consulta Top-N, O(k log k), donde `n` es el tamaño del catálogo y `k` la cantidad solicitada, según la implementación de `top_n()`.

El costo total esperado es O(n + k log k). La heap se vuelve a construir en cada consulta, por lo que actualmente no se reutiliza entre distintas solicitudes.

## 6. Respuestas para la defensa

### ¿Por qué elegimos una heap?

Porque permite obtener rankings por rating sin ordenar completamente el catálogo. Es una estructura adecuada para consultar elementos según su prioridad.

### ¿Por qué no ordenar todo el catálogo?

Ordenar todos los videojuegos tiene un costo O(n log n) por consulta. La heap permite obtener solamente los primeros elementos sin ordenar el catálogo completo.

### ¿Qué alternativas consideramos?

Consideramos ordenar el catálogo, mantener una lista ordenada y utilizar árboles de búsqueda por rating. La heap complementa estas alternativas porque está especialmente orientada a las consultas por prioridad.

### ¿Cuál es el costo de las operaciones?

- Consultar la raíz: O(1).
- Insertar un elemento: O(log n).
- Extraer la raíz: O(log n).
- Construir la heap mediante heapify: O(n).
- Obtener un Top-N con una heap auxiliar de candidatos: O(N log N).

### ¿Cuál es el peor caso?

Insertar y extraer tienen un peor caso O(log n), porque el elemento puede recorrer la altura del árbol. Buscar un elemento arbitrario en la heap puede costar O(n).

### ¿La heap reemplaza al BST o al AVL?

No. Los árboles de búsqueda permiten localizar elementos por una clave, mientras que la heap facilita el acceso a los elementos de mayor o menor prioridad. Son estructuras complementarias.

### ¿Qué demuestran las mediciones?

Las mediciones permiten comparar el rendimiento de la heap con la ordenación del catálogo. La ventaja depende del tamaño del catálogo, la cantidad solicitada y el costo de construir la estructura en cada consulta.

## 7. Conclusión

La heap se incorpora a NextPlay para generar rankings de videojuegos según su rating. Su implementación permite aplicar una cola de prioridad y comparar su rendimiento con otras estrategias, complementando las estructuras de búsqueda desarrolladas en las versiones anteriores.
