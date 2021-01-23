import socket, pickle, sounddevice as sd

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((socket.gethostname(), 4444))


def callback(outdata, frames, time, status):
	#336
	msg = sock.recv(1497)
	if msg:
		msg = pickle.loads(msg)
		outdata[:] = msg
	else:
		outdata.fill(0)

try:
	with sd.OutputStream(blocksize=336, callback=callback, channels=1):
		print("##########")
		print("Press Return to stop")
		print("#########")
		input()
except Exception as e:
	print(e)
