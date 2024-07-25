###########################################################
#                                                         #
#   Ejecutar script                                       #
#   Usar:                                                 #
#     1. Install Faker library: pip3 install Faker        #
#     2. Run the script: python3 generate_data.py         #
#     3. Run the script: python3 client_problem.py        #
#                                                         #
#   *consider the file path                               #
#                                                         #
###########################################################


"""
referencias:https://blog.unitips.cl/puntaje-ponderado#:~:text=El%20puntaje%20ponderado%20es%20la,escala%20de%20100%20a%201.000.

https://es.wikipedia.org/wiki/Media_ponderada

https://es.wikipedia.org/wiki/Normalizaci%C3%B3n_(estad%C3%ADstica)

https://nuevaescuelamexicana.sep.gob.mx/detalle-ficha/11035/

"""

import json 

ruta= "taxpayers.json"
latitud_oficina= 19.3797208
longitud_oficina= -99.1940332

def cargar_data(archivo): 
    with open(archivo) as contenido: #le ponemos el alias del contexto
        personas= json.load(contenido) 
        return personas #nos retorna una lista de diccionarios 
        
        


#valor ponderado: suma edades    edad * ponderacion   / suma de edades
def ponderacion_edad(personas):#le pasamos por parametro la carga de datos 
    ponderacion=0.10 #10%
    edad_ponderada=0 #acumulador
    edad_total=0 
    #lista para almacenar las puntuaciones ponderadas
    puntuaciones=[]#esto nos permitira acceder a la lista para que no haya error con que sea entero
    
    for persona in personas: #iteramos
        edad = persona.get('age', 0)  # Obtén la edad o 0 si no está presente 
        edad_total +=edad #sumamos todas las edades        52327
        edad_ponderada=  (edad * ponderacion ) / edad_total #cada edad  38*10% =0.10 / total=52327
        puntuaciones.append(edad_ponderada) # la edad se agrega al final de la lista
        #bandera para depurar 
        #print(f"Nombre: {persona['name']}, Edad: {persona['age']}, Ponderacion: {edad_ponderada}")
    
    return puntuaciones #retornamos la lista



#para alcular la ponderacion es sumar todo y divivirlo entre la cantidad 
def ponderacion_demografica(personas, lati, long): #necesitamos las coordenas de referencia y la carga de datos
    ponderacion= 0.10 #10%
    latitud_total = 0 #acumulador
    longitud_total = 0
    puntuaciones=[]#lista para almacenar las puntuaciones ponderadas
    
    for persona in personas: #iteramos sobre cada persona  
        
        locacion = persona.get('location', {})   #accedemos al diccionario location primero 
        latitud = locacion.get('latitude',0) #dentro de location accedemos  a las coordenas
        longitud = locacion.get('longitude',0) #dentro de location accedemos a las coordenas
        
# comparacion entre el tipo de dato de latitud y longitud y los de referencia también son números
        if isinstance(lati, (int, float)) and isinstance(long, (int, float)) == isinstance(latitud, (int, float)) and isinstance(longitud, (int, float)):
                # Sumar las latitudes y longitudes para ponderación
            latitud_total += latitud
            longitud_total += longitud
        #si es del mismo tipo que me vaya haciendo las sumas     
        else: 
            print("No son datos iguales ")

        #ponderacion del porcentaje 
        latitud_ponderada= (latitud * ponderacion) / latitud_total
        longitud_ponderada= (longitud * ponderacion) / longitud_total
        suma_distancias_ponderadas = latitud_ponderada + longitud_ponderada
        puntuaciones.append(suma_distancias_ponderadas)# la suma se agrega al final de la lista
        #bandera para depurar 
        #print(f"Nombre: {persona['name']}, Distancia: {locacion['latitude']}, {latitud_ponderada} | {locacion['longitude']},{longitud_ponderada}, Suma: {suma_distancias_ponderadas}")
        
    return puntuaciones # retorna la lista



def ponderacion_aceptadas(personas): #le pasamos por parametro la carga de datos 
    ponderacion= 0.30 #30%
    aceptadas_total=0 #acumulador
    aceptadas_poderacion=0
    puntuaciones=[]#lista para almacenar las puntuaciones ponderadas
    
    for persona in personas: #iteramos cada persona 
        
        ofertas = persona.get('accepted_offers', 0) # obtener las aceptadas o 0 si no está presente 
        aceptadas_total+= ofertas #el total de las aceptadas
        aceptadas_poderacion= (ofertas * ponderacion) / aceptadas_total#cada oferta*30% / la suma total 
        puntuaciones.append(aceptadas_poderacion) #agregamos al final de la listsa
        #bandera para depurar 
        #print(f"Nombre: {persona['name']}, Cantidad: {persona['accepted_offers']}, Ponderacion: {aceptadas_poderacion}")
    return puntuaciones #retornamos la lista



def ponderacion_rechazadas(personas):#le pasamos por parametro la carga de datos 
    ponderacion= 0.30 #30%
    rechazadas_total=0 #acumulador
    rechazadas_poderacion=0
    puntuaciones=[]#lista para almacenar las puntuaciones ponderadas
    
    for persona in personas:#iteramos cada persona 
        
        ofertas = persona.get('canceled_offers', 0)  # Obtén las rechazadas o 0 si no está presente 
        rechazadas_total+= ofertas #el total de las rechazadas
        rechazadas_poderacion= (ofertas * ponderacion) / rechazadas_total #cada oerta*30% / la suma total 
        puntuaciones.append(rechazadas_poderacion)#agregamos al final de la lista
        #print(f"Nombre: {persona['name']}, Cantidad: {persona['canceled_offers']}, Ponderacion: {rechazadas_poderacion}")
    
    return puntuaciones #retornamos la lista



def ponderacion_respuesta(personas): #carga de datos
    ponderacion= 0.20 #20%
    respuesta_total = 0 #acumulador
    respuesta_poderacion=0
    puntuaciones=[]#lista para almacenar las puntuaciones ponderadas
    
    for persona in personas: #iteraoms cada persona
        
        respuesta= persona.get('average_reply_time', 0)# Obtén el tiempo o 0 si no está presente 
        respuesta_total+= respuesta# el tiempo total 
        respuesta_poderacion = (respuesta * ponderacion)  / respuesta_total
        puntuaciones.append(respuesta_poderacion)#agregamos al final 
        #print(f"Nombre: {persona['name']}, Tiempo: {persona['average_reply_time']}, Ponderacion: {respuesta_poderacion}")    
    
    return puntuaciones#retornamos la lista



def rango_min_max(datos): #le pasamos las puntuaciones totaltes 

#rango = max-min
#normalizar en rango de 1-10 = rango min + (valor - valor min) * (rango max - rango min) / rango 

    valor_maximo =max(datos)
    valor_minimo=min(datos)
    
    #para obtener el rango de un maximo y minimo es restar max-min
    rango = valor_maximo - valor_minimo
    datos_normalizados = [] # lista para los datos 
    
    for puntaje in datos: #iterar sobre cada uno de los puntajes 
        
        puntaje_normalizado = 1 + (puntaje - valor_minimo) * (10 - 1) / rango #formula
        datos_normalizados.append(puntaje_normalizado) #agregamos al final de la lista
    
    return datos_normalizados #retornamos la lista 



def puntaje_final(latitud,longitud): #pasmaos las coordenadas para comporbar lo de la ponderacion 
    
    personas = cargar_data(ruta) # Cargamos los datos
    
    # Obtenemos las puntuaciones ponderadas
    edad_final = ponderacion_edad(personas)
    distancia_final = ponderacion_demografica(personas, latitud, longitud)
    aceptadas_final = ponderacion_aceptadas(personas)
    rechazadas_final = ponderacion_rechazadas(personas)
    tiempo_final = ponderacion_respuesta(personas)
    puntuaciones_totales = [] #lista para almacenar las puntuaciones

    for i, persona in enumerate(personas): #iteramos tanto el indice como el valor
        puntuacion_total = ( #agrupamos la suma de todas las ponderaciones
            edad_final[i] + #hay que usar i para acceder 
            distancia_final[i] +
            aceptadas_final[i] +
            rechazadas_final[i] +
            tiempo_final[i]
        )
        puntuaciones_totales.append(puntuacion_total) #agregamos al final la agrupacion 
# usamos la funcino para normalizar y le pasamos esas puntuaciones para que calcule los valores y el rango
    puntuaciones_normalizadas = rango_min_max(puntuaciones_totales) 

    # asignamos las puntuaciones normalizadas a cada persona
    puntuaciones_finales = []
    for i, persona in enumerate(personas):#iteramos tanto el indice como el valor
        #construimos el listado de diccionarios obteniendo las propiedades se añade a la lista 
        puntuaciones_finales.append({
            'id': persona.get('id'),
            'name': persona.get('name'),
            'location': persona.get('location', {}),
            'age': persona.get('age'),
            'accepted_offers': persona.get('accepted_offers'),
            'canceled_offers': persona.get('canceled_offers'),
            'average_reply_time': persona.get('average_reply_time'),
            'score': round(puntuaciones_normalizadas[i])  # se redondea la puntuacion de cada persona por el indice
        })

    # Ordenamos de mayor a menor con el reverse mediante un afuncino anomia y que me retorne el score
    puntuaciones_finales.sort(key=lambda x: x['score'], reverse=True)
    
    # Retornamos los 10 clientes con la puntuación más alta
    return puntuaciones_finales[:10] # va desde el 0 hasta el 10 

# Llamamos a la función para obtener los resultados
clientes = puntaje_final(latitud_oficina, longitud_oficina)
print(json.dumps(clientes, indent=4)) #transormar la lista de diccionarios en un JSON con un formateo