from estructuras.grafo import Grafo


def peso_de_relacion(a, b):
  """Cuanto se parecen dos juegos: generos en comun + plataformas en comun."""
  generos = len(set(a.genres) & set(b.genres))
  plataformas = len(set(a.platform) & set(b.platform))
  return generos + plataformas


def construir_grafo(juegos, min_generos_comunes=2):
  """Arma el grafo de juegos relacionados (JSON -> objetos -> grafo).

  - Vertice: un juego (se identifica por su id).
  - Arista: dos juegos se conectan si comparten al menos `min_generos_comunes`
    generos (por defecto 2). Con catalogos grandes conviene subirlo (3 o 4):
    ver docs/10-grafo.md.
  - Peso: generos en comun + plataformas en comun (ver peso_de_relacion).
  - Grafo no dirigido: "se parece a" es simetrico.

  Para no comparar todos contra todos (O(n^2)) se usa un indice
  genero -> juegos y el principio del palomar: si un juego tiene k generos y
  comparte al menos m con otro, entonces entre CUALQUIER subconjunto de k-m+1
  de sus generos hay al menos uno en comun. Alcanza con mirar los k-m+1
  generos menos frecuentes de cada juego para encontrar todos los candidatos,
  y despues se verifica el minimo exacto con la interseccion.
  """
  grafo = Grafo(clave=lambda j: j.id)
  for juego in juegos:
    grafo.agregar_vertice(juego)

  # genero -> posiciones de los juegos que lo tienen
  indice = {}
  for pos, juego in enumerate(juegos):
    for genero in set(juego.genres):
      indice.setdefault(genero, []).append(pos)

  conjuntos = [set(j.genres) for j in juegos]
  m = min_generos_comunes
  if m < 1:
    raise ValueError("min_generos_comunes tiene que ser al menos 1")

  for pos, juego in enumerate(juegos):
    generos = conjuntos[pos]
    k = len(generos)
    if k < m:
      continue  # no puede compartir m generos con nadie
    # los k-m+1 generos con menos juegos: la menor cantidad de candidatos
    a_mirar = sorted(generos, key=lambda g: len(indice[g]))[:k - m + 1]
    candidatos = set()
    for genero in a_mirar:
      for otro in indice[genero]:
        if otro > pos:
          candidatos.add(otro)
    for otro in candidatos:
      if len(generos & conjuntos[otro]) >= m:
        grafo.agregar_arista(juego, juegos[otro], peso_de_relacion(juego, juegos[otro]))
  return grafo
