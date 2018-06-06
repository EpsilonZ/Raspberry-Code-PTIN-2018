from socketIO_client_nexus import SocketIO

# Clase usada para enviar y recibir informacion a traves de SocketIO, tanto para el servicio en paciente
# como el uso para el servicio de doctor
class socket:
	def __init__(self, id):
		self.id = id
		self.socketIO = None
		self.token = None
		self.missatge_doctor = None
		self.esperar = True
		self.createsocket(id)


	def desconectar(self, id):
		self.socketIO.emit('disconnect', {'id':id})


	
	def createsocket(self, id):
		print id
		self.socketIO = SocketIO('https://ptin2018.herokuapp.com', params={"id":id})
		print "Socket creado"
		self.socketIO.wait(seconds = 3)

	def receive_general(self, *args):
		print "Recibido"
		print args[0]
		self.token = args[0]

	def response(self,*args):
		print "response"
		print args

	def response_doctor(self, *args):
		print "response doctor"
		print args
		self.missatge_doctor = args
		self.esperar = False
		

	def envia_confirmacio(self):
		self.socketIO.wait(seconds=1)
		self.socketIO.emit('generalAuthentication', {'requester':self.id, 'token':self.token})
		self.socketIO.on("generalResponse", self.response)
		self.socketIO.wait(seconds = 1)


	def esperar_doctor(self):
		self.socketIO.on('pacientLocation', self.response_doctor)
		while self.esperar:
			self.socketIO.wait(seconds = 3)
		self.esperar = True
		return self.missatge_doctor



	def envia_general(self, lat, lon):
		self.socketIO.emit('alarm', {'type':2, 'latitude': lat, 'longitude': lon})
		print self.socketIO
		self.socketIO.on("generalAuthentication", self.receive_general)
		self.socketIO.wait(seconds = 1)



