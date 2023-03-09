
import ctypes
 
f_dll ="C:\\Andre\\MasterCim\\NFe.dll"

dll = ctypes.windll.LoadLibrary(f_dll)
 
rc = dll.ConsultaCep('82540020')
rc = ctypes.c_wchar_p(rc)
print(rc.value)
