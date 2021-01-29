import threading
import socket
# pip install psutil
import psutil as pu

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

for sock in pu.net_connections(kind="inet"):
    if (sock.family == socket.AF_INET) and (sock.type == socket.SOCK_STREAM) and (sock.status in (pu.CONN_ESTABLISHED, pu.CONN_LISTEN)):
        process_pid = pu.Process(sock.pid)
        print("{}\t{}".format(process_pid.name(), process_pid.exe()))