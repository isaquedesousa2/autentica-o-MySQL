from email.policy import default
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

USUARIO = 'root'
SENHA = ''
HOST = 'localhost'
PORT = '3306'
DB = 'autenticacao'
CONNECTION = f'mysql+pymysql://{USUARIO}:{SENHA}@{HOST}:{PORT}/{DB}'

engine = create_engine(CONNECTION, echo=True)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Pessoa(Base):
    __tablename__ = 'Pessoa'
    id = Column(Integer, primary_key=True)
    nome = Column(String(50))
    usuario = Column(String(20))
    senha = Column(String(100))

class Token(Base):
    __tablename__ = 'Token'
    id = Column(Integer, primary_key=True)
    id_pessoa = Column(Integer, ForeignKey('Pessoa.id'))
    token = Column(String(100))
    data = Column(DateTime, default=datetime.datetime.utcnow())

Base.metadata.create_all(engine)
