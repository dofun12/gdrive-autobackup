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

    gbackup = Backup(mysql_config,gdrive_config)
    gbackup.init_backup()

    gdrive_api = GDriveApi(gdrive_config)

    gdrive_api.print_list()
    file = gdrive_api.get_oldest_file()
    print(f'Removing... {file}')
    gdrive_api.delete_file(file['id'])
    print('After...')
    gdrive_api.print_list()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
