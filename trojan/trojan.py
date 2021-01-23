import socket, pickle, sounddevice as sd
from time import sleep

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((socket.gethostname(), 4444))
sock.listen(5)

clientsocket, clientaddress = None, None

def callback(indata, frames, time, status):
	global connected
	msg = pickle.dumps(indata)
	try:
		clientsocket.send(msg)
	except Exception:
		connected = False

connected = False
while True:
	try:
		clientsocket, clientaddress = sock.accept()
		connected = True

		#blocksize=336
		with sd.InputStream(blocksize=336, callback=callback, channels=1):
			while connected:
				sleep(1)

		clientsocket.close()
	except Exception as e:
		exit()