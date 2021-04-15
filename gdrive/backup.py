import os
from gdrive.gdrive_api import GDriveApi
from general.local_files import LocalFiles
from model.gdrive_config_model import GDriveConfigModel
from model.general_config_model import GeneralConfigModel
from model.mysql_config_model import MysqlConfigModel


class Backup:
    MYSQL_CONFIG: MysqlConfigModel
    GDRIVE_CONFIG: GDriveConfigModel
    LOCAL_FILES: LocalFiles

    def __init__(self, mysql_config: MysqlConfigModel, gdrive_config: GDriveConfigModel, general_config: GeneralConfigModel):
        self.MYSQL_CONFIG = mysql_config
        self.GDRIVE_CONFIG = gdrive_config
        self.LOCAL_FILES = LocalFiles(mysql_config, general_config)

    def do_drive_upload(self):
        self.LOCAL_FILES.clean()
        compressed_file = self.LOCAL_FILES.prepare_backupfile()
        print("Starting upload... " + compressed_file.name)

        gdrive_api = GDriveApi(self.GDRIVE_CONFIG)
        try:
            gdrive_api.upload_file(compressed_file.name, compressed_file.full_path)
            self.LOCAL_FILES.clean()
            gdrive_api.remove_oldest_file()
        except:
            print('Error on upload')
