import threading
import socket

#target = 'pythonprogramming.net'
#ip = socket.gethostbyname()
port_list = []
def portscan(port):

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)# 

    try:
        con = s.connect((socket.gethostname(),port))
        #con = s.connect(('127.0.0.1',port))
        port_list.append(port)

        #print('Port :',port,"is open")

        con.close()
    except: 
        pass
r = 1 
for x in range(1,8000): 

    t = threading.Thread(target=portscan,kwargs={'port':r}) 

    r += 1     
    t.start() 
suspicious = False
for i in range(len(port_list)):
    if port_list[i] > 4000 and port_list[i] < 5000:
        suspicious = True

if suspicious == True:
     print("SUSPICIOUS OPEN PORT DETECTED")
else: 
    print("IT'S SAFE")
    


    #print (port_list[i], "OPEN")
