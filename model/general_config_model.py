class GeneralConfigModel:
    MAX_SQL_DUMPS: int
    MAX_COMPRESSED_DUMPS: int
    KEEP_LOCAL_BACKUPS: bool

    def __init__(self, config):
        self.MAX_SQL_DUMPS = int(config['GENERAL']['MAX_SQL_DUMPS'])
        self.MAX_COMPRESSED_DUMPS = int(config['GENERAL']['MAX_COMPRESSED_DUMPS'])
        self.KEEP_LOCAL_BACKUPS = 'true' == config['GENERAL']['KEEP_LOCAL_BACKUPS']
