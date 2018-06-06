import dades    #dades.py
import envia    #envia.py
import Planta   #Planta.py
import Edificio #Edificio.py
import envia_socket #envia_socket.py
import gps
import os
import subprocess
import threading
import RPi.GPIO as GPIO
from gpiozero import LED
from gpiozero import Button
import time

session = gps.gps("localhost", "2947")
session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

_,tipus,id,token = dades.obtenir_dades()
if tipus == "4":
    socketIO = envia_socket.socket(id)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(23, GPIO.OUT)
boton = Button(26)   # Dentro cal poner el numero del GPIO que lo controla en este caso GPIO26 para el boton

latitud = 0
longitud = 0
apretado = False
activo = False

# Funcion para cambiar el booleano global "apretado" de False a True, es usado para hacer el doble click en el boton
def pulsado():
    global apretado
    apretado = True

# Funcion usada para pedir auxiliio en caso de ser un paciente a traves de SocketIO, ademas de enchegar y apagar el led
def pacient():
    global apretado, latitud, longitud
    print "Peticion de auxilio enviada"
    while apretado:
        if boton.wait_for_press(timeout=5):
            GPIO.output(23, GPIO.HIGH)
            socketIO.envia_general(latitud, longitud)
            socketIO.envia_confirmacio()
            GPIO.output(23, GPIO.LOW)
            apretado = False

# Funcion usada para pedir auxiliio en caso de ser un doctor
def doctor():
    global apretado
    apretado = False
    mensaje = socketIO.esperar_doctor()
    print mensaje

# Funcion usada para conseguir las coordenadas en interior llamando al programa codigo_posicion.py
def obtenir_coord_interior():
    #time.sleep(0.5)
    process = subprocess.Popen(['sudo' , 'python', 'codigo_posicion.py', '-i', 'wlan0'], stdout=subprocess.PIPE)
    out, err = process.communicate()
    coord = out.split(' ')
    coord[1] = coord[1][:-1]
    return coord[0], coord[1]

# funcion que se encarga de conseguir y enviar los datos de posicion al servidor web
def enviar_localizacion():
    global latitud, longitud, activo, apretado
    contador = 0
    ses = 3
    while 1:
        boton.when_pressed = pulsado
        if apretado and tipus == "4":   
            pacient()
            time.sleep(2)
            apretado = False

        elif apretado and tipus == "1":
            if not activo:
                socketIO = envia_socket.socket(id)
                GPIO.output(23, GPIO.HIGH)
                activo = True
            else:
                socketIO.desconectar(id)
                GPIO.output(23, GPIO.LOW)
                activo = False
            apretado = False
        try:
            if session.waiting(1):
                report = session.next()
                if ses == 3:
                    ses = 0
                    if report['class'] == 'TPV':
                        contador = 0
                        temp_lat = latitud
                        temp_lon = longitud             
                        if hasattr(report, 'lat'):
                            temp_lat = report.lat
                        if hasattr(report, 'lon'):
                            temp_lon = report.lon   
                        if latitud != temp_lat or longitud != temp_lon:
                            latitud = temp_lat
                            longitud = temp_lon
                            envia.localitzacio_exterior(latitud, longitud, id, token)
                            print "Localitzacio exterior lat: " + str(latitud) + " i lon: " + str(longitud)
                else:
                    ses += 1
            else:
                contador += 1
                if contador == 2:
                    contador = 0
                    latitud, longitud = obtenir_coord_interior()
                    latitud = float(latitud)
                    longitud = float(longitud)
                    edificio = Edificio.get_edificio(latitud,longitud)
                    piso = Planta.get_planta()
                    envia.localitzacio_interior(latitud, longitud, edificio, piso, id, token)
                    print "Localitzacio interior lat: " + str(latitud) + " i lon: " + str(longitud) + " " + str(edificio) + " " + str(piso)

        except:
            print "except"
            pass


def main():
    enviar_localizacion()
    
if __name__ == '__main__':
    main()
