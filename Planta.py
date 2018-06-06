import time
import sys
import WifiScan

A_piso0 = ["00:24:97:88:04:10", "D8:B1:90:C3:2C:40" ,"64:F6:9D:B3:ED:30" , "A8:9D:21:74:68:B0", "84:B8:02:04:A5:90", "A8:9D:21:6D:B0:F0", "F0:25:72:3D:8A:A0", "70:DF:2F:14:02:70"]
A_piso1 = ["64:F6:9D:B3:EA:B0", "64:F6:9D:4A:EB:80", "A0:23:9F:9E:D7:10", "08:17:35:32:28:30", "64:F6:9D:4D:F8:10", "E8:65:49:F7:16:30", "A8:9D:21:44:22:C0", "64:F6:9D:B3:EC:50", "D0:C2:82:07:87:40", "70:DF:2F:2C:11:90", "64:F6:9D:4A:FB:70"]
A_piso2 = ["64:F6:9D:5B:E9:B0", "64:F6:9D:4A:FB:C0"]
B_piso0 = ["64:F6:9D:CE:D2:80", "64:F6:9D:4D:F8:20"]
B_piso1 = ["64:F6:9D:B3:F0:D0", "D8:B1:90:B9:26:30", "64:F6:9D:4A:FB:D0"]

#Funcion que marca dependendiendo del repetidor wifi con nombre tipo "eduroam" con mas "Calidad",
#devuelve el piso en el que se encuentra ese repetidor dentro del edificio.
def selecionar_piso(vect):
    for x in vect:
        if str(x["Name"]) == "eduroam":
            if x["Address"] in A_piso0:
                return "A_0"
            elif x["Address"] in A_piso1:
                return "A_1"
            elif x["Address"] in A_piso2:
                return "A_2"
            elif x["Address"] in B_piso0:
                return "B_0"
            elif x["Address"] in B_piso1:
                return "B_1"
    return "-1"
    

#Funcion que converte nombres simples tipo "A_0" en mensajes completos como: "Edificio A, Piso: Planta Baja"
#para cada edificio dentro de los considerados.
def str_piso(respuesta):
    planta_actual=""
    if respuesta == "A_0":
        planta_actual="Edificio A, Piso: Planta Baja"
    elif respuesta == "A_1":
        planta_actual="Edificio A, Piso: 1"
    elif respuesta == "A_2":
        planta_actual = "Edificio A, Piso: 2"
    elif respuesta == "B_0":
        planta_actual="Edificio B, Piso: Planta Baja"
    elif respuesta == "B_1":
        planta_actual ="Edificio B, Piso: 1"
    elif respuesta == "NP_AP":
        planta_actual ="Neapolis, Aparcamiento"
    elif respuesta == "NP_0":
        planta_actual ="Neapolis, Piso: Planta Baja"
    elif respuesta == "NP_1":
        planta_actual ="Neapolis, Piso: 1"
    elif respuesta == "NP_2":
        planta_actual ="Neapolis, Piso: 2"
    elif respuesta == "NP_3":
        planta_actual ="Neapolis, Piso: 3"
    elif respuesta == "NP_4":
        planta_actual ="Neapolis, Piso: 4"
    else:
        planta_actual ="No encontrado"
    return planta_actual

#Funcion principal que devolvera el resultado del piso en el que se encuentra dentro del edificio
def get_planta():
    vect = WifiScan.scan()
    planta = selecionar_piso(vect) # planta tiene el valor tipo "A_1"
    #resultado = str_piso(planta)   # resultado tiene el valor en string completo de planta tipo "Edificio A, Piso: 1"
    resultado=0
    if planta != "-1":
        resultado = int(planta[-1])	   # resultado contiene solo el numero que corresponde al piso
    else:
	resultado = int(planta)
    #WifiScan.print_cells(vect)
    return resultado
