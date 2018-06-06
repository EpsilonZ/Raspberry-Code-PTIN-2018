# Raspberry-Code-PTIN-2018
Todos los programas necesarios para ejecutar todas las funcionalidades en la Raspberry

LISTA DE PROGRAMAS Y SU FUNCIONALIDAD
-------------------------------------

dades.py --> Recolectar los datos necesarios para el envío posterior 

codigo_posicion.py --> Nos dice su posicionamiento interior de manera exacta. Se utiliza una petición a la API de Google mediante los puntos de acceso cercanos.

Doctor.py --> Habilitar/Deshabilitar doctor

Edificio.py --> Se utiliza para conocer en que edificio se encuentra. Se conoce mediante la distancia relativa a cada edificio.

envia.py --> Enviamos al Servidor Web los datos recolectados en dades.py

envia_socket.py --> Nos permite la comunicación con el socket (el cuál nos mostrará respuestas como puede ser el envío de un doctor a una petición de ayuda).

main.py --> Programa principal

Planta.py --> Se utiliza para conocer la planta en que se encuentra el edificio mediante la potencia de señal de los puntos de acceso que se encuentran cerca (parecido al posicionamiento interior).

speech.sh --> Se utiliza para decir por voz la frase que le pasemos por parámetro. Como en el caso del codigo_posicion.py se hace mediante una petición a la API de Google.

WifiScan.py --> Conocer los puntos de acceso cercanos.
