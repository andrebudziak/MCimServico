from app import db

class Arquivo_Versao(db.Model):
    id_arquivo_versao = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    versao = db.Column(db.String(10))
    arquivo = db.Column(db.String(400))
    data = db.Column(db.datetime)        
    
    def __init__(self, id_arquivo_versao,versao,arquivo,data):
       self.id_arquivo_versao = id_arquivo_versao
       self.versao = versao
       self.arquivo = data
       self.data = data        
    
    def get_id(self):
        return (self.id_arquivo_versao)