# This is a sample Python script.
import configparser
import sys
import time
from datetime import datetime
import threading
import pycron

from gdrive.backup import Backup
from gdrive.gdrive_api import GDriveApi
from model.gdrive_config_model import GDriveConfigModel
from model.general_config_model import GeneralConfigModel
from model.mysql_config_model import MysqlConfigModel
from utils import dateutils


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def now():
    return datetime.now()


def now_str():
    return now().strftime("%m/%d/%Y - %H:%M:%S")

 

def do_backup_async():
    now = datetime.now().strftime("%m/%d/%Y - %H:%M:%S")
    print(f'{now} Backuping....')
    gdrive_config = GDriveConfigModel(config)
    mysql_config = MysqlConfigModel(config)
    general_config = GeneralConfigModel(config)

    gdrive_api = GDriveApi(gdrive_config)
    list = gdrive_api.list_files()
    if len(list) > gdrive_config.MAX_BACKUPS:
        gdrive_api.remove_oldest_file()

    gbackup = Backup(mysql_config,gdrive_config,general_config)
    gbackup.do_drive_upload()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    isrunning = False
    now = datetime.now().strftime("%m/%d/%Y - %H:%M:%S")
    print(f'{now} Starting...')
    default_config = 'config.ini'
    if len(sys.argv) > 1:
        profile = sys.argv[1]
        if profile.startswith('--profile='):
            default_config = 'config_' + profile.split("=")[1] + '.ini'
    config = configparser.ConfigParser()
    config.read(default_config)

    if not isrunning:
        do_backup_async()

    while(isrunning):
        if pycron.is_now('*/2 * * * *'):
            now = datetime.now().strftime("%m/%d/%Y - %H:%M:%S")
            print(f'{now} Cronando....')
            threading.Thread(target=do_backup_async, args=(), kwargs={}).start()
        time.sleep(60)





