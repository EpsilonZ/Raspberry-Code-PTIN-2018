import requests
import json
import subprocess

link = "https://ptin2018.herokuapp.com/api/devices/"

# Funcion usada para registrar el dispositivo en el servidor, dado el nombre y el tipos(paciente (4),doctor (1),etc)
def registra(nom, tipus):
	try:
		r = requests.post(link, data={"name": nom, "type": tipus})
		retorn = json.loads(r.content)
		return r.status_code == 200 and retorn["status"] == 201, retorn["id"], retorn["token"]
	except:
		return False, 0, 0

# Funcion usada para enviar la localizacion al servidor usando datos del GPS
def localitzacio_exterior(latitud, longitud, id, token):
	enviat = False
	while not enviat:
		try:
			r = requests.put(link+id+"/info", headers = {"Authorization": "Bearer " + token}, data = {"latitude": latitud, "longitude": longitud})
			retorn = r.status_code
                        enviat = (retorn == 200)
		except Exception:
			pass
		    
# Funcion usada para enviar la localizacion al servidor usando las funciones y datos dados por el Wifi
def localitzacio_interior(latitud, longitud, edificio, piso, id, token):
	enviat = False
	while not enviat:
		try:
                    r = requests.put(link+id+"/info", headers = {"Authorization": "Bearer " + token}, data = {"latitude": latitud, "longitude": longitud, "building": edificio, "floor": piso})
                    retorn = r.status_code
                    enviat = (retorn == 200)
		except Exception:
		    pass


