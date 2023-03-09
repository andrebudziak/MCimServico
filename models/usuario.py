from flask_login import UserMixin
from app import db

class Usuario(UserMixin, db.Model):
    id_usuario = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    senha = db.Column(db.String(10))
    apelido = db.Column(db.String(15))
    nome = db.Column(db.String(40))                  
    adm  = db.Column(db.String(1))                   
    nivel = db.Column(db.Integer)                    
        
    
    def __init__(self, id_usuario,senha,apelido,nome,adm,nivel):
        
        self.id_usuario = id_usuario
        self.senha = senha
        self.apelido = apelido
        self.nome = nome
        self.adm  = adm
        self.nivel = nivel
        
    
    def get_id(self):
        return (self.id_usuario)