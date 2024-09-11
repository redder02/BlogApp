from secret import DATABASE_PASSWORD, SECRET_KEY, JWT_SECRET_KEY

class Config:
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://root:{DATABASE_PASSWORD}@localhost/blogdb'
    SECRET_KEY = SECRET_KEY
    JWT_SECRET_KEY = JWT_SECRET_KEY
