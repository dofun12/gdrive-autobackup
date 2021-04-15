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
import argparse


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def now():
    return datetime.now()


def now_str():
    return now().strftime("%m/%d/%Y - %H:%M:%S")


def do_backup_async(gdrive_config, mysql_config, general_config):
    now = datetime.now().strftime("%m/%d/%Y - %H:%M:%S")
    print(f'{now} Backuping....')

    gdrive_api = GDriveApi(gdrive_config)
    list = gdrive_api.list_files()
    if len(list) > gdrive_config.MAX_BACKUPS:
        gdrive_api.remove_oldest_file()

    gbackup = Backup(mysql_config, gdrive_config, general_config)
    gbackup.do_drive_upload()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Optional app description')
    parser.add_argument('--profile', type=str,
                        help='Set the profile of config.ini')
    parser.add_argument('--cron', action='store_true',
                        help='Run on cron')

    args = parser.parse_args()
    now = datetime.now().strftime("%m/%d/%Y - %H:%M:%S")
    print(f'{now} Starting...')
    default_config = 'config.ini'

    if args.profile:
        default_config = 'config_' + args.profile + '.ini'

    config = configparser.ConfigParser()
    config.read(default_config)

    iscron = args.cron

    gdrive_config = GDriveConfigModel(config)
    mysql_config = MysqlConfigModel(config)
    general_config = GeneralConfigModel(config)

    if not iscron:
        do_backup_async(gdrive_config, mysql_config, general_config)
        exit(0)
    CRON = general_config.CRON
    print(f'Starting cron... waiting for ( {CRON} )')
    while iscron:
        if pycron.is_now(CRON):
            now = datetime.now().strftime("%m/%d/%Y - %H:%M:%S")
            print(f'{now} Cronando....')
            threading.Thread(target=do_backup_async, args=(gdrive_config, mysql_config, general_config), kwargs={}).start()
        time.sleep(60)
