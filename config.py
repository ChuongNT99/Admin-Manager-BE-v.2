class Config:
    SECRET_KEY = 'MteRlo-Xyrv221m57onZ_g4rd-Omfv37'
    DEBUG = True
    # Các cấu hình khác mà bạn muốn thêm vào đây

class ProductionConfig(Config):
    DEBUG = False
    # Các cấu hình riêng cho môi trường production nếu cần

class DevelopmentConfig(Config):
    # Các cấu hình riêng cho môi trường development nếu cần
    pass

class TestingConfig(Config):
    TESTING = True
    # Các cấu hình riêng cho môi trường testing nếu cần