class GDriveConfigModel:
    SCOPES = []
    BACKUP_FOLDER_ID: str
    CREDENTIAL_PATH: str
    TOKEN_PICK_PATH: str
    MAX_BACKUPS: int

    def __init__(self, config):
        protocol = config['GDRIVE']['SCOPE_PROTOCOL']
        host = config['GDRIVE']['SCOPE_HOST']
        paths = config['GDRIVE']['SCOPE_PATHS']
        for path in paths.split(','):
            self.SCOPES.append(f'{protocol}://{host}{path}')
        self.BACKUP_FOLDER_ID = config['GDRIVE']['BACKUP_FOLDER_ID']
        self.CREDENTIAL_PATH = config['GDRIVE']['CREDENTIAL_PATH']
        self.TOKEN_PICK_PATH = config['GDRIVE']['TOKEN_PICK_PATH']
        self.MAX_BACKUPS = int(config['GDRIVE']['MAX_BACKUPS'])
