class Config:
    db_name = 'dbaq2qoff7h4l3'
    username = 'ijxaoyrtuckmnx'
    dialect = 'postgresql'
    password = '6b55b57f8f183632ed5f8902fcdcf54546d0129a7c947f62f205004dbf1b8367'
    host = 'ec2-54-155-208-5.eu-west-1.compute.amazonaws.com'

    SQLALCHEMY_DATABASE_URI = f'{dialect}://{username}:{password}@{host}/{db_name}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'zxc-antimage'
