import signals


def esperar_avis(socketIO):
	missatge = socketIO.esperar_doctor()

