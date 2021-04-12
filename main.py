# This is a sample Python script.
import configparser
import sys
from gdrive.backup import Backup
from gdrive.gdrive_api import GDriveApi
from model.gdrive_config_model import GDriveConfigModel
from model.mysql_config_model import MysqlConfigModel
from utils import dateutils


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    default_config = 'config.ini'
    if len(sys.argv) > 1:
        profile = sys.argv[1]
        if profile.startswith('--profile='):
            default_config = 'config_' + profile.split("=")[1] + '.ini'
    config = configparser.ConfigParser()
    config.read(default_config)

    gdrive_config = GDriveConfigModel(config)
    mysql_config = MysqlConfigModel(config)

    gdrive_api = GDriveApi(gdrive_config)
    list = gdrive_api.list_files()
    if len(list) > gdrive_config.MAX_BACKUPS:
        gdrive_api.remove_oldest_file()

    gbackup = Backup(mysql_config,gdrive_config)
    gbackup.init_backup()




