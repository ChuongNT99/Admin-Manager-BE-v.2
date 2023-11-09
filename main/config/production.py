class ProductionConfig:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:001122@localhost/booking'
    SECRET_KEY = 'a3d55b3111d9304cd902ea1c837be66e5d64b78f2fa0cbe38916797cd2c1fae2'
