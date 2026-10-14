# TP4 — Desbalance del árbol y AVL: comparación contra el BST común

Este documento responde a la consigna del TP4: qué pasa cuando un árbol de búsqueda pierde su equilibrio, cómo lo resuelve el AVL, y qué diferencia hay medida sobre el catálogo real de NextPlay.

Código involucrado:

| Archivo | Qué es |
|---|---|
| `estructuras/arbol_busqueda_nombre.py` | BST común por nombre (TP3). En el TP4 se le sumó `altura()`. |
| `estructuras/arbol_avl.py` | AVL por nombre, con las 4 rotaciones. |
| `algoritmos/construir_arbol_avl.py` | Arma el AVL insertando los juegos de a uno. |
| `algoritmos/experimento_balance.py` | Experimento de esta sección (`python -m algoritmos.experimento_balance`). |
| `tests/test_avl.py` | Pruebas del AVL y de la altura del BST. |

## 1. Qué pasa cuando un BST se desbalancea

En un BST común la forma del árbol depende del **orden en que entran los datos**. Cada juego nuevo se compara con la raíz y baja hacia la izquierda o la derecha hasta encontrar su lugar.

Si los nombres llegan ya ordenados alfabéticamente, cada juego nuevo es mayor que todos los anteriores y siempre cuelga a la derecha del último. El resultado no es un árbol sino una **lista enlazada**:

```text
Age of Empires
        \
         Balatro
                \
                 Celeste
                         \
                          ...   (un nivel por juego)
```

Consecuencias:

- La **altura** pasa de `log₂(n)` a `n`.
- La **búsqueda** cuesta tantas comparaciones como niveles tenga el árbol, así que pasa de O(log n) a **O(n)**: igual que recorrer la lista con la búsqueda secuencial, con lo cual el árbol deja de aportar algo.
- **Armar** el árbol también se vuelve más caro: cada inserción tiene que bajar por todo el camino ya existente, por lo que insertar n juegos ordenados cuesta O(n²).

> Nota sobre la app: el BST de NextPlay no sufre esto hoy porque `construir_arbol()` ordena la lista y arma el árbol partiendo siempre por la mitad (queda balanceado). El problema aparece apenas se agregan juegos nuevos con `agregar()`, o si el árbol se arma insertando en el orden del archivo, y es justo el caso que reproduce el experimento.

## 2. Qué hace el AVL

El AVL es un BST que **se corrige solo mientras inserta**. Cada nodo guarda su altura y, después de cada inserción, se calcula el **factor de balance** de los nodos del camino recorrido:

```text
factor de balance = altura(subárbol izquierdo) − altura(subárbol derecho)
```

La regla del AVL es que en todos los nodos el factor sea −1, 0 o 1. Si una inserción deja algún nodo en 2 o −2, se aplica una rotación que lo vuelve a balancear sin romper el orden del árbol:

| Caso | Cuándo ocurre | Corrección |
|---|---|---|
| Izquierda-izquierda | el desbalance está en el hijo izquierdo del hijo izquierdo | rotación simple a la derecha |
| Derecha-derecha | en el hijo derecho del hijo derecho | rotación simple a la izquierda |
| Izquierda-derecha | en el hijo derecho del hijo izquierdo | rotación izquierda en el hijo y luego derecha en el nodo |
| Derecha-izquierda | en el hijo izquierdo del hijo derecho | rotación derecha en el hijo y luego izquierda en el nodo |

Ejemplo con tres nombres ordenados (`a`, `b`, `c`): sin corrección queda una lista de 3 niveles; el AVL detecta el factor −2 en `a` y rota a la izquierda, dejando `b` como raíz con `a` y `c` de hijos (2 niveles).

```text
a                  b
 \                / \
  b      -->     a   c
   \
    c
```

Cada rotación solo cambia unas pocas referencias (O(1)) y, como en una inserción se corrige como mucho un punto del camino, insertar en un AVL sigue costando O(log n). La altura de un AVL con n nodos nunca supera ~1,44·log₂(n + 2), así que **buscar es O(log n) siempre**, sin importar el orden de entrada.

## 3. Experimento

**Qué se hizo.** Para cada uno de los 3 catálogos de la consigna de TP2 (120, 980 y 8.980 juegos) se insertaron los juegos **de a uno con `agregar()`**, en tres órdenes, tanto en el BST común como en el AVL:

- `ordenado A-Z` y `ordenado Z-A`: el peor caso para el BST común.
- `aleatorio`: un orden "normal" (semilla fija para poder repetir la corrida).

Se midió la altura final, la cantidad de rotaciones del AVL, el tiempo de armado y el tiempo promedio de búsqueda (100 juegos existentes elegidos al azar, repetidos 3 veces, con `time.perf_counter()`).

**Cómo reproducirlo.** Desde la raíz del proyecto: `python -m algoritmos.experimento_balance` (tarda alrededor de un minuto, casi todo es el BST degenerado armándose).

> No se usó `construir_arbol()` en este experimento a propósito: esa función ordena y parte por la mitad, así que dejaría el BST balanceado y no se vería el problema.

### 3.1. Altura final

| Catálogo | Orden de inserción | Altura ideal (⌈log₂(n+1)⌉) | Altura BST | Altura AVL | Rotaciones del AVL |
|---|---|---|---|---|---|
| 120 | ordenado A-Z | 7 | **120** | 7 | 113 |
| 120 | ordenado Z-A | 7 | **120** | 7 | 113 |
| 120 | aleatorio | 7 | 12 | 8 | 64 |
| 980 | ordenado A-Z | 10 | **980** | 10 | 970 |
| 980 | ordenado Z-A | 10 | **980** | 10 | 970 |
| 980 | aleatorio | 10 | 26 | 12 | 667 |
| 8.980 | ordenado A-Z | 14 | **8.980** | 14 | 8.966 |
| 8.980 | ordenado Z-A | 14 | **8.980** | 14 | 8.966 |
| 8.980 | aleatorio | 14 | 33 | 16 | 6.311 |

### 3.2. Tiempos

Valores de una corrida en una sola máquina: sirven para comparar entre columnas, no como números absolutos.

| Catálogo | Orden de inserción | Búsqueda BST | Búsqueda AVL | Armado BST (total) | Armado AVL (total) |
|---|---|---|---|---|---|
| 120 | ordenado A-Z | 0,0254 ms | 0,0016 ms | 1,62 ms | 0,46 ms |
| 120 | ordenado Z-A | 0,0158 ms | 0,0015 ms | 1,37 ms | 0,45 ms |
| 120 | aleatorio | 0,0022 ms | 0,0017 ms | 0,20 ms | 0,46 ms |
| 980 | ordenado A-Z | 0,1684 ms | 0,0021 ms | 147,71 ms | 5,21 ms |
| 980 | ordenado Z-A | 0,1775 ms | 0,0035 ms | 139,77 ms | 5,74 ms |
| 980 | aleatorio | 0,0042 ms | 0,0038 ms | 2,60 ms | 5,37 ms |
| 8.980 | ordenado A-Z | 3,4577 ms | 0,0046 ms | 24.047,49 ms | 74,66 ms |
| 8.980 | ordenado Z-A | 2,4156 ms | 0,0048 ms | 22.014,36 ms | 65,44 ms |
| 8.980 | aleatorio | 0,0062 ms | 0,0041 ms | 52,62 ms | 73,43 ms |

### 3.3. Qué muestran los resultados

1. **Con datos ordenados el BST se vuelve una lista.** Su altura es exactamente n (120, 980 y 8.980 niveles, un nivel por juego), y el AVL queda en la altura ideal (7, 10 y 14).
2. **La búsqueda sigue la altura.** Con 8.980 juegos ordenados, buscar tarda 3,46 ms en el BST contra 0,0046 ms en el AVL (unas 750 veces más lento). La diferencia crece con n, tal como indican O(n) frente a O(log n).
3. **Armar el BST degenerado es carísimo:** 24 segundos contra 75 ms para el AVL con 8.980 juegos, porque cada inserción recorre toda la cadena existente (O(n²) en total).
4. **Con orden aleatorio el BST común anda bien:** su altura (12, 26 y 33) es algo mayor que la ideal pero lejos de n, y la búsqueda es casi igual de rápida que en el AVL. Ahí el AVL incluso tarda más en armar (73 ms vs 53 ms con 8.980), porque paga las rotaciones (6.311 en ese caso).
5. **El AVL mantiene la altura pegada a la ideal en los tres órdenes** (a lo sumo 2 niveles por encima en el caso aleatorio).
6. **Un detalle práctico:** en Python el BST degenerado con 8.980 juegos supera el límite de recursión por defecto (1000 llamadas) y falla con `RecursionError`. En el experimento se sube ese límite temporalmente. Es una consecuencia más de la altura n, porque `agregar` y `buscar` son recursivas y cada nivel es una llamada.

## 4. Conclusión técnica

El BST común solo es eficiente si el árbol queda **parejo**; la complejidad O(log n) de buscar depende de que la altura sea logarítmica y el BST no garantiza eso, porque la forma depende del orden de entrada. Con el peor orden posible (datos ordenados) la altura es n, la búsqueda cuesta O(n) y el árbol pierde la ventaja que tenía sobre la búsqueda secuencial.

El AVL garantiza la altura logarítmica en **cualquier** orden de inserción a cambio de un costo pequeño y acotado: guardar la altura en cada nodo y hacer algunas rotaciones de tiempo constante. En el experimento esa garantía se tradujo en búsquedas alrededor de 750 veces más rápidas en el peor caso con el catálogo grande, y el costo adicional en el caso aleatorio fue de entre 1,4 y 2,3 veces el tiempo de armado (unos milisegundos en términos absolutos), que se amortiza si se busca muchas veces.

En NextPlay el catálogo se construye una sola vez y ordenado, así que el BST balanceado de `construir_arbol()` alcanza para ese uso. El AVL aporta cuando el catálogo **crece de a un juego por vez** (por ejemplo, agregando juegos nuevos desde la app): es la única de las dos estructuras que se mantiene balanceada sin volver a ordenar y reconstruir todo. Por eso la versión 2 del CLI usa el AVL para la búsqueda por nombre exacto y para el listado alfabético (`inorder`), junto al BST para poder comparar resultados.

## 5. Preguntas para la defensa

- **¿Qué pasa si el árbol se desbalancea?** La altura crece hasta n y la búsqueda pasa de O(log n) a O(n).
- **¿Qué aporta el AVL?** Mantiene la diferencia de alturas entre subárboles de cada nodo en −1, 0 o 1 mediante rotaciones, y eso garantiza altura O(log n) y búsqueda O(log n) siempre.
- **¿Cómo se dispara el problema en el experimento?** Insertando los nombres ya ordenados con `agregar()`, no con `construir_arbol()`.
- **¿Cuántas rotaciones hay?** Cuatro casos (LL, RR, LR, RL), es decir dos rotaciones simples y dos dobles.
- **¿Por qué el AVL tarda más en armar con datos aleatorios?** Porque además de insertar actualiza alturas y rota; el BST común no paga eso.
