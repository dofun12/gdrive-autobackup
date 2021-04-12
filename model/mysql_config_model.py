class MysqlConfigModel:
    TARGET_DIR = str
    HOST: str
    PORT: int
    DB_USER: str
    DB_PASS: str
    DATABASE: str

    def __init__(self, config):
        self.TARGET_DIR = config['MYSQL']['TARGET_DIR']
        self.HOST = config['MYSQL']['HOST']
        self.PORT = int(config['MYSQL']['PORT'])
        self.DB_USER = config['MYSQL']['DB_USER']
        self.DB_PASS = config['MYSQL']['DB_PASS']
        self.DATABASE = config['MYSQL']['DATABASE']
