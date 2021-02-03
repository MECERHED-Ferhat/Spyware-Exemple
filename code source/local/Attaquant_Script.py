import socket, sounddevice as sd

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((socket.gethostname(), 4444))

def callback(outdata, frames, time, status):
	#336
	msg = sock.recv(1008)
	if msg:
		outdata[:] = msg
	else:
		outdata = [0 for i in range(len(outdata))]

try:
	with sd.RawOutputStream(blocksize=336, dtype="int24", callback=callback, channels=1):
		print("##########")
		print("Press Return to stop")
		print("#########")
		input()
except Exception as e:
	print(e)