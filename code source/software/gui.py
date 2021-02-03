import threading, socket, os, stat, psutil as pu, winreg as reg
from subprocess import Popen
from time import sleep
from tkinter import *
from tkinter import ttk

def has_hidden_attribute(filepath):
		return bool(os.stat(filepath).st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN)

def find_procs_by_name(name):
		cpt = 0
		for p in pu.process_iter(['name']):
				if p.info['name'] == name:
						cpt += 1
		return cpt

#main window
f = Tk()
f.title("Processus")
f.configure(width=800,height=350)
f.configure(bg="white")
# f.resizable(width=0, height=0)

text = Label(f,text="Liste des processus actifs",bg="white",fg='black')
text.config(font=('times',18,'bold'))
text.place(x=270,y=0)

#tree

tree = ttk.Treeview(f, column=("column1", "column2", "column3"), show='headings')
tree.heading("#1", text="Port")
tree.heading("#2", text="Processus")
tree.heading("#3", text="Emplacement")

COLUMN_1 = 100
tree.column("#1", width=COLUMN_1)
COLUMN_2 = 150
tree.column("#2", width=COLUMN_2)
COLUMN_3 = 370
tree.column("#3", width=COLUMN_3)
TREE_COLUMNS = COLUMN_1 + COLUMN_2 + COLUMN_3

TREE_X = 0
TREE_Y = 50
tree.place(x=0,y=50)

def row_selected(data):
	row = None
	global current_process
	global possible_malware
	try:
		row = int(tree.item(tree.selection())['text'])
	except:
		pass
	if row is not None:
		current_process = possible_malware[row]
		kill_button['state'] = "normal"
		open_folder['state'] = "normal"
	else:
		current_process = None
		kill_button['state'] = "disabled"
		open_folder['state'] = "disabled"

tree.bind("<ButtonRelease-1>", row_selected)

#scrollbar
sb = ttk.Scrollbar(f, orient="vertical", command=tree.yview)
sb.place(x=TREE_COLUMNS - 15, y=75, height=200)
tree.configure(yscrollcommand=sb.set)

#affichage
def exec_by_user(process):
	return (process['cmdline'] is not None) and (len(process['cmdline']))
def hidden_proc(process):
	return (process['exe']) and (has_hidden_attribute(process['exe']))
def has_childs(process):
	return (process['name']) and (find_procs_by_name(process['name']) >= 2)
FILTERS = [exec_by_user, has_childs, hidden_proc]
possible_malware = []

#ports enumeration
def fill_tree():
	global possible_malware
	tree.delete(*tree.get_children())
	possible_malware = []
	for sock in pu.net_connections(kind="inet"):
		if (sock.family == socket.AF_INET) and (sock.type == socket.SOCK_STREAM) and (sock.status in (pu.CONN_ESTABLISHED, pu.CONN_LISTEN)):
			process = pu.Process(sock.pid).as_dict(['pid', 'name', 'exe', 'cmdline'])
			process['port'] = sock.laddr.port
			process['cwd'] = '\\'.join(process['exe'].split('\\')[:-1])
			candidat = True
			for fil in proc_filters:
				if fil.get() >= 0:
					candidat = FILTERS[fil.get()](process)
				if not candidat:
					break

			if candidat:
				del process['cmdline']
				possible_malware.append(process)
		possible_malware = sorted(possible_malware, key=lambda x: x["port"])

	for pm in possible_malware:
		tree.insert('', 'end', text=len(tree.get_children()), values=(pm['port'], pm['name'], pm['exe']))


#Buttons
current_process = None

def delete_reg_value(data):
	key_value = r'Software\Microsoft\Windows\CurrentVersion\Run'      
	key = reg.OpenKey(reg.HKEY_CURRENT_USER,key_value,0,reg.KEY_ALL_ACCESS) 
	#in all registry key values
	for i in range(0, reg.QueryInfoKey(key)[1]):        
		val = reg.EnumValue(key, i) #tuple containing value name v[0] and its data val[1]
		if val[1] == data:
			try: #delete value      
				reg.DeleteValue(key, val[0])
			except (e):
				print (e)
	reg.CloseKey(key)

def kill_proc(pid, exe):
	if pu.pid_exists(pid):
		pu.Process(pid).kill()

def delete_file(exe):
	if os.path.exists(exe):
		os.remove(exe)

def handle_kill_button():
	global current_process
	if current_process is not None:
		kill_proc(current_process["pid"], current_process["exe"])
		delete_reg_value(current_process["exe"])
		t = threading.Timer(3, delete_file, args=[current_process["exe"],])	
		t.start()
	current_process = None
	kill_button['state'] = "disabled"
	open_folder['state'] = "disabled"

kill_button = Button(f, text="Delete process", command=handle_kill_button)
kill_button.config(width=20)
kill_button["state"] = "disabled"
kill_button.place(x=TREE_COLUMNS + 10, y=TREE_Y + 20)

def handle_open_folder():
	if current_process is not None:
		Popen('explorer "{}"'.format(current_process["cwd"]))

open_folder = Button(f, text="Open file location", command=handle_open_folder)
open_folder.config(width=20)
open_folder["state"] = "disabled"
open_folder.place(x=TREE_COLUMNS + 10, y=TREE_Y + 80)

refresh = Button(f, text="Refresh table", command=fill_tree)
refresh.config(width=20)
refresh.place(x=TREE_COLUMNS + 10, y=TREE_Y + 140)


#CheckButtons
proc_filters = [IntVar(), IntVar(), IntVar()]

ebu_check = Checkbutton(f, text="Executed by user",
												variable=proc_filters[0],
												onvalue=0,
												offvalue=-1,
												command=fill_tree)
ebu_check.deselect()
ebu_check.place(x=50, y=300)

childs_check = Checkbutton(f, text="Has childs",
													 variable=proc_filters[1],
													 onvalue=1,
													 offvalue=-1,
													 command=fill_tree)
childs_check.deselect()
childs_check.place(x=200, y=300)

hidden_check = Checkbutton(f, text="Hidden file",
													 variable=proc_filters[2],
													 onvalue=2,
													 offvalue=-1,
													 command=fill_tree)
hidden_check.deselect()
hidden_check.place(x=350, y=300)

fill_tree()

f.mainloop()