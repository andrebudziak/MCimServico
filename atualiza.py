import ftplib
import json
import os.path

remote_path_versao = "/mastercim.com.br/public/version/atualizacao.json"

def download(ftp,local_path,remote_path):
    file = open(local_path, 'wb')
    # TYPE A for ASCII mode
    ftp.sendcmd('TYPE I') 
   
    def file_write(data):
        file.write(data)        
    
    ftp.retrbinary("RETR " + remote_path, file_write)
    file.close()  
    
def upload(ftp,local_path,remote_path):
    file = open(local_path, 'wb')
    # TYPE A for ASCII mode
    ftp.sendcmd('TYPE I') 
   
    def file_write(data):
        file.write(data)        
    
    ftp.storbinary("STOR " + remote_path, file_write)
    file.close()  
    

def atualizar(app):
    ftp = ftplib.FTP("ftp.mastercim.com.br")
    ftp.login("mastercim", "Mastercim@2019")
    
    os.remove('atualizacao.json')
    download(ftp,'atualizacao.json',remote_path_versao)
        
    data = json.loads(open('atualizacao.json').read())
    for i in range (0, len(data)):
        if data[i]['app'] == app:
            for j in range(0, len(data[i]['arquivos'])):
                print("Baixando: "+data[i]['arquivos'][j])
                download(ftp,data[i]['arquivos'][j],data[i]['path_versao']+data[i]['arquivos'][j])
         
    return "OK"        
    print("Atualizacao Concluida")
    ftp.close()  

def versao(app):
    ftp = ftplib.FTP("ftp.mastercim.com.br")
    ftp.login("mastercim", "Mastercim@2019")
    
    os.remove('atualizacao.json')
    download(ftp,'atualizacao.json',remote_path_versao)
        
    data = json.loads(open('atualizacao.json').read())
    for i in range (0, len(data)):
        if data[i]['app'] == app:
            return data[i]['num_versao']
                
    ftp.close()  
    