import envia	#envia.py
import os.path as path
import requests

link = "https://ptin2018.herokuapp.com/api/devices/"

# Funcion para registrar y guardar en el archivo .dades, los  datos de registro,
# tambien se envia a la funcion en envia.py llamada registra()
def registra():
	nom = raw_input("nom: ")
	tipus = raw_input("tipus de dispositiu: ")
	enviat, id, token = envia.registra(nom, tipus)
	if enviat:
		r = requests.put(link+id, headers = {"Authorization": "Bearer " + token}, data = {"enabled": "true", "deleted": "false"})
		file = open(".dades","w",0) # el 0 es por si hay algo en el fichero, borrarlo
		file.write(nom + " " + tipus + " " + id + " " + token) 
		print "El dispositiu amb nom " + nom + " i tipus " + tipus + " ha estat registrat amb id " + id + "."
	else:
		print "No s'ha pogut registrar, intenta-ho mes tard"


# Funcion que carga y obtiene los datos contenidos en .dades para su uso
def obtenir_dades():
	try:
		file = open(".dades","r")
		dades = file.read().split()		
		print "Dades del dispositiu:"
		print "    Nom:   " + dades[0]
		print "    Tipus: " + dades[1]
		print "    ID:    " + dades[2]
		return dades[0], dades[1], dades[2], dades[3]
	except:
		print "El dispositiu no esta registrat, registra'l:"
		registra()
		return obtenir_dades()

