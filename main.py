from tkinter import E
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models import CONNECTION, Pessoa, Token
from secrets import token_hex

app = FastAPI()

def conectaBD():
    engine = create_engine(CONNECTION, echo=True)
    Session = sessionmaker(bind=engine)
    return Session()

@app.post('/cadastro')
def cadastrar(nome: str, user: str, senha: str):
    session = conectaBD()
    usuario = session.query(Pessoa).filter_by(usuario=user, senha=senha).all()
    if not usuario:
        x = Pessoa(nome=nome, usuario=user, senha=senha)
        session.add(x)
        session.commit()
        return {'status': 'Usuário cadastrado'}
    else:
        return {'status': 'Usuário já cadastrado'}

@app.post('/login')
def login(usuario: str, senha: str):
    session = conectaBD()
    user = session.query(Pessoa).filter_by(usuario=usuario, senha=senha)
    if not user:
        return {'status': 'Usuário inexistente'}
    
    while True:
        token = token_hex(50)
        tokenExiste = session.query(Token).filter_by(token=token).all()
        if not tokenExiste:
            pessoaExiste = session.query(Token).filter_by(id_pessoa=user[0].id).all()
            if not pessoaExiste:
                novoToken = Token(id_pessoa=user[0].id, token=token)
                session.add(novoToken)
            elif pessoaExiste:
                pessoaExiste[0].token = token
            
            session.commit()  
            break
    return token




