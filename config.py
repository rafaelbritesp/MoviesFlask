import os

SECRET_KEY = 'rbpereira'

SQLALCHEMY_DATABASE_URI = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD = 'mysql+mysqlconnector',
        usuario = 'root',
        senha = 'admin',
        servidor = 'localhost',
        database = 'filmesdb'
    )

UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '/uploads'