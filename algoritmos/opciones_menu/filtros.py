from ui.menu import GENEROS, PLATAFORMAS
from config import GENRES, PLATFORM
from algoritmos import retorna_categoria

def filtrar(menu,arboles):
   while True:
    print(menu)
    try:
      opcion = int(input("Elegí una opción: ").strip())
              
      if opcion <= 4 and opcion > 0:
        filtros(opcion, arboles)
                
      elif opcion == 0:
        print("Volviendo al menu anteriror...")
        break

      else:
        print("Entrada inválida. Ingresá un número.")
                
    except ValueError:
      print("Entrada inválida. Ingresá un número.")

#-----------------------------------------------------------------------------------#

def filtros(opcion,arboles):

    if opcion == 1:
      resultado = opcion_1(arboles)
      print(resultado["msg"] ,resultado["categoria"])
      print(*resultado["respuesta"])
    
    elif opcion == 2:
      resultado = opcion_2(arboles)
      print(resultado["msg"] ,resultado["categoria"])
      print(*resultado["respuesta"])
      
    elif opcion == 3:
     resultado = opcion_3(arboles)
     print(resultado["msg"], resultado["rating_min"])
     print(*resultado["respuesta"])
            
    elif opcion == 4:
      try:
        dic_genero, dic_plataforma,dic_rating_min = None,None,None
        print("Ingrese un caracter para selecionar o enter para omitir")
        
        filtar_genero = input("Quiere filtrar por Genero (enter para omitir): ").strip() or None
        if filtar_genero:
          dic_genero = opcion_1(arboles)
        
        filtarr_plataforma = input("Quiere filtrar por Plataforma (enter para omitir): ").strip() or None
        if filtarr_plataforma:
          dic_plataforma = opcion_2(arboles)
        
        filtarr_rating_min = input("Quiere filtrar por Rating minimo (enter para omitir): ").strip() or None
        if filtarr_rating_min:
          dic_rating_min = opcion_3(arboles)
        genero = dic_genero["respuesta"]
        plataforma = dic_plataforma["respuesta"]
        rating_min = dic_rating_min["respuesta"]
        resultados = filtros_unificados(genero,plataforma,rating_min,arboles)
        print(f"Total por Género {dic_genero["categoria"]}:", len(genero) if genero is not None else None)
        print(f"Total por Plataforma {dic_plataforma["categoria"]}:", len(plataforma) if plataforma is not None else None)
        print(f"Total por Rating {dic_rating_min["rating_min"]}:", len(rating_min) if rating_min is not None else None)
        print("Total fitros convinados:", len(resultados))        
        print(*resultados)
        
      except ValueError:
        print("Entrada inválida. Ingresá un número.")
    
#-----------------------------------------------------------------------------------#

def opcion_1(arboles):
  print(GENEROS)
  while True:
    try:
      genero = int(input("Elegí una opción: ").strip())
      if genero <= 19 and genero > 0 :
        categoria = GENRES[genero]
        respuesta_genero = retorna_categoria(arboles["arbol_general_genres"], categoria)
        return {"respuesta" : respuesta_genero["respuesta"],"categoria":categoria, "msg":respuesta_genero["msg"]}
      else:
        print("Elegí una opción correcta")
        break
    except ValueError:            
      print("Entrada inválida. Ingresá un número.") 
#-----------------------------------------------------------------------------------#

def opcion_2(arboles):
  print(PLATAFORMAS)
  while True:
    try:
      plataforma = int(input("Elegí una opción: ").strip())
      if plataforma <= 50 and plataforma > 0:
        categoria = PLATFORM[plataforma]
        respuesta_plataforma = retorna_categoria(arboles["arbol_general_platform"], categoria)
        return {"respuesta" : respuesta_plataforma["respuesta"],"categoria":categoria, "msg":respuesta_plataforma["msg"]}
      else:
        print("Elegí una opción correcta")
        break
    except ValueError:
      print("Entrada inválida. Ingresá un número.") 
#-----------------------------------------------------------------------------------#

def opcion_3(arboles):
  while True:
    try:
      arbol_rating = arboles["arbol_BST_rating"]
      rating_min = input("Rating minimo (enter para omitir): ").strip()
      
      if rating_min == "":              
        return  {"respuesta": arbol_rating.inorder(arbol_rating.raiz), "rating_min":" " ,"msj":"Resultados de la busqueda por rating minimo: "} 
     
      elif float(rating_min) < 0 or float(rating_min) > 5:
        return {"respuesta": [], "rating_min":rating_min , "msg":"Los Video Juegos se califican del 0 al 5"}

      else:
        respuesta = arbol_rating.buscar_desde(float(rating_min))
        if len(respuesta) == 0:
          return {"respuesta": [], "rating_min":rating_min,"msg":"No se encontro resultado"} 
        else:
          return {"respuesta":respuesta,"rating_min":rating_min, "msg":"Resultados de la busqueda por rating minimo: "}
    except ValueError:
      print("Entrada inválida. Ingresá un número.")
#-----------------------------------------------------------------------------------#

def filtros_unificados(genero,plataforma,rating_min,arboles):
  listas = [lista for lista in (genero,plataforma,rating_min) if lista is not None and len(lista) != 0]
 #--------------------
  print("Len lista ")
  print(len(listas))
  #--------------------
  if not listas:
    arbol_avl = arboles["arbol_avl"]
    resultados = arbol_avl.inorder(arbol_avl.raiz)
    print("Nada que filtrar.")
    print("Listando todos los videojuegos...")
  
  elif len(listas) == 1:
    resultados = listas [0]  
  
  else:
    resultados = unir(*listas)
  return resultados
#-----------------------------------------------------------------------------------#

def unir(lista_g=None,lista_p=None,lista_r=None):
  set_id_1,set_id_2 = set(), set() 
  resultados = []
  # elimina las listas que sean None
  listas = list(filter(lambda e: e is not None and len(e) != 0 ,(lista_g,lista_p,lista_r)))
 
  # Selecciona la lista mas corta
  lista_menor = min(listas, key=len)
  # Elimaina la lista menor del resto de las listas
  otras_listas = [lista for lista in listas if lista is not lista_menor]
  # Si otras_listas tiene 2 listas crea dos set guardando los id 
  if len(otras_listas) == 2:
    set_id_1 = {game._id for game in otras_listas[0]}
    set_id_2 = {game._id  for game in otras_listas[1]}
    # Itera la lista menor y compara si el id se repite en los tres casos
    for game in lista_menor:
      if game._id  in set_id_1 and game._id  in set_id_2:
        resultados.append(game)
  else:
    # Si solo tiene una lisa crea un solo set 
    set_id_1 = {game._id for game in otras_listas[0]}
    # Itera la lista menor y compara si el id se repite en los dos casos
    for game in lista_menor:
      if game._id in set_id_1:
        resultados.append(game)  

  return resultados 