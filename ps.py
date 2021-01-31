import threading
import socket
# pip install psutil
import psutil as pu
import os, stat
from time import sleep

#target = 'pythonprogramming.net'
#ip = socket.gethostbyname()
"""
port_list = []
def portscan(port):

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)# 

    try:
        con = s.connect((socket.gethostname(),port))
        #con = s.connect(('127.0.0.1',port))
        port_list.append(port)

        print('Port :',port,"is open")

        con.close()
    except: 
        pass
r = 1 
for x in range(1,65535): 

    t = threading.Thread(target=portscan,kwargs={'port':r}) 

    r += 1     
    t.start()
"""

def has_hidden_attribute(filepath):
    return bool(os.stat(filepath).st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN)

def find_procs_by_name(name):
    cpt = 0
    for p in pu.process_iter(['name']):
        if p.info['name'] == name:
            cpt += 1
    return cpt

possible_malware = []

for sock in pu.net_connections(kind="inet"):
    if (sock.family == socket.AF_INET) and (sock.type == socket.SOCK_STREAM) and (sock.status in (pu.CONN_ESTABLISHED, pu.CONN_LISTEN)):
        process = pu.Process(sock.pid).as_dict(['pid', 'name', 'cwd', 'exe', 'cmdline'])
        if (process['cmdline'] is not None) and (len(process['cmdline']) == 1) and has_hidden_attribute(process['exe']) and find_procs_by_name(process['name']) >= 2:
            del process['cmdline']
            possible_malware.append(process)

def kill_button(pid):
    if pu.pid_exists(pid):
        pu.Process(pid).kill()

def delete_reg_value(data):
    key_value = r'Software\Microsoft\Windows\CurrentVersion\Run'      
    key = reg.OpenKey(HKEY_CURRENT_USER,key_value,0,reg.KEY_ALL_ACCESS) 
    #in all registry key values
    for i in range(0, reg.QueryInfoKey(key)[1]):        
        val = reg.EnumValue(key, i) #tuple containing value name v[0] and its data val[1]
        if val[1] == data:
            try: #delete value      
                reg.DeleteValue(key, val[0])
            except (e):
                print (e)
    reg.CloseKey(key)
    
for i in possible_malware:
    print(i['name'])
    # data = chemin de l'exe?
