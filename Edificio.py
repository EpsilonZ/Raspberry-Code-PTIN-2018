import math

class Sitio:
    def __init__(self, nom, lat, long):
        self.nombre = nom
        self.latitud = lat
        self.longitud = long

    def get_nombre(self):
        return self.nombre

    def get_lat(self):
        return self.latitud

    def get_long(self):
        return self.longitud
    
edificiA = Sitio("Edifici A", 41.221560, 1.730029)
edificiB = Sitio("Edifici B", 41.223120, 1.735658)
Neapolis = Sitio("Neapolis", 41.223201, 1.733356)

#Funcion para calcular la distancia entre 2 puntos, dada las latitudes y longitudes de esos puntos
def haversine(lat1, lon1, lat2, lon2):
    rad = math.pi / 180
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    R = 6372.795477598
    a = (math.sin(rad * dlat / 2)) ** 2 + math.cos(rad * lat1) * math.cos(rad * lat2) * (math.sin(rad * dlon / 2)) ** 2
    distancia = 2 * R * math.asin(math.sqrt(a))
    return distancia

#Funcion que devuelve el valor menor dada 3 variables a,b,c, en caso de igualdad devuelve 0
def calcular_peq(a, b, c):
    if a < b and a < c:
        return a
    elif b < a and b < c:
        return b
    elif c < a and c < b:
        return c
    else:
        return 0

#Funcion que dada una latitud y una longitud, te devuelve de que edificio esta mas cerca
def get_edificio(latitud,longitud):
    global edificiA, edificiB, Neapolis
    distX1 = haversine(latitud, longitud, edificiA.get_lat(), edificiA.get_long())
    distX2 = haversine(latitud, longitud, edificiB.get_lat(), edificiB.get_long())
    distX3 = haversine(latitud, longitud, Neapolis.get_lat(), Neapolis.get_long())
    calc = calcular_peq(distX1, distX2, distX3)
    if calc != 0:
        if calc == distX1:
            edificio = edificiA.get_nombre()
        elif calc == distX2:
            edificio = edificiB.get_nombre()
        else:
            edificio = Neapolis.get_nombre()
    else:
        edificio = "Exterior"
    return edificio
