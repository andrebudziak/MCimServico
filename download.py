import ftplib
import progressbar

ftp = ftplib.FTP("ftp.mastercim.com.br")
ftp.login("mastercim", "Mastercim@2019")

local_path = ""
remote_path = ""
#remote_path_versao = "/mastercim.com.br/public/version/atualizacao.json"
#local_path_versao = "atualizacao.json"

file = open(local_path, 'wb')
# TYPE A for ASCII mode
ftp.sendcmd('TYPE I') 
size = ftp.size(remote_path)
bar = progressbar.ProgressBar(max_value=size)
bar.start()
    
def file_write(data):
    file.write(data)
    global bar
    bar += len(data)   

ftp.retrbinary("RETR " + remote_path, file_write)
ftp.quit()
file.close()
