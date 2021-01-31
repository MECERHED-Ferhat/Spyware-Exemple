import threading
import socket
# pip install psutil
import psutil as pu

from tkinter import *
from tkinter import ttk


#main window
f = Tk()
f.title("Processus")
f.configure(width=800,height=350)
f.configure(bg="white")
f.resizable(width=0, height=0)

text = Label(f,text="Liste des processus actifs",bg="white",fg='black')
text.config(font=('times',18,'bold'))
text.place(x=270,y=0)

#tree

tree = ttk.Treeview(f, column=("column1", "column2", "column3"), show='headings')
tree.heading("#1", text="Port")
tree.heading("#2", text="Processus")
tree.heading("#3", text="Emplacement")

tree.column("#1", width=100)
tree.column("#2", width=150)
tree.column("#3", width=550)
tree.place(x=0,y=50)

#scrollbar
sb = ttk.Scrollbar(f, orient="vertical", command=tree.yview)
sb.place(x=782, y=75, height=200)
tree.configure(yscrollcommand=sb.set)

#affichage 
for sock in pu.net_connections(kind="inet"):
    if (sock.family == socket.AF_INET) and (sock.type == socket.SOCK_STREAM) and (sock.status in (pu.CONN_ESTABLISHED, pu.CONN_LISTEN)):
        process_pid = pu.Process(sock.pid)

        tree.insert("",'end',values=(sock.laddr.port, process_pid.name(),  process_pid.exe()))
        #print("{}\t{}".format(process_pid.name(), process_pid.exe()))




f.mainloop()