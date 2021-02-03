# add script to the registry 
  

from winreg import *  
import winreg as reg  
import os              
  
def AddToRegistry(address):
    key_value = r'Software\Microsoft\Windows\CurrentVersion\Run'
      
    # open the key to make changes to 
    open = reg.OpenKey(HKEY_CURRENT_USER,key_value,0,reg.KEY_ALL_ACCESS) 
      
    # modifiy the opened key 
    reg.SetValueEx(open, "System32", 0, reg.REG_SZ, address) 
      
    # now close the opened key 
    reg.CloseKey(open) 
  
#  main
if __name__=="__main__": 
    AddToRegistry() 