import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY') or 'secret-key-123'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or \
      'mysql+mysqlconnector://root:password@localhost/clinica_estetica_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False