class Config:
    db_name = 'Konshina_BD'
    username = 'postgres'
    dialect = 'postgresql'
    password = 'alp37327'
    host = 'localhost'

    SQLALCHEMY_DATABASE_URI = f'{dialect}://{username}:{password}@{host}/{db_name}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'zxc-antimage'
