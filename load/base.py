from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#Declaramos nuestro motor
engine = create_engine("sqlite:///newspaper.db")

#Objeto sesion, le pasamos nuestro motor
Session = sessionmaker(bind=engine)

#Clase base de la cual van a extender todos nuestros modelos
Base = declarative_base()
