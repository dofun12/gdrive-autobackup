import tarfile
import os
import time

from model.file_model import FileModel
from model.general_config_model import GeneralConfigModel
from model.mysql_config_model import MysqlConfigModel


class LocalFiles:
    MYSQL_CONFIG: MysqlConfigModel
    GENERAL_CONFIG: GeneralConfigModel

    def __init__(self, mysql_config: MysqlConfigModel, general_config: GeneralConfigModel):
        self.MYSQL_CONFIG = mysql_config
        self.GENERAL_CONFIG = general_config

    def list_tar_backups(self):
        self.mkdirs(self.MYSQL_CONFIG.TARGET_DIR)
        dirs = [self.MYSQL_CONFIG.TARGET_DIR + "/{0}".format(fn) for fn in os.listdir(self.MYSQL_CONFIG.TARGET_DIR) if fn.endswith(".tar.gz")]
        return dirs

    def make_tarfile(self, source_file, output_filename):
        print(f'Compressing {source_file} >>> {output_filename}')
        tar = tarfile.open(output_filename, "w:gz")
        tar.add(source_file)
        tar.close()

    def mkdirs(self, directory):
        if not os.path.exists(directory):
            os.makedirs(directory)

    def list_sql_dumps(self):
        self.mkdirs(self.MYSQL_CONFIG.TARGET_DIR)
        dirs = [self.MYSQL_CONFIG.TARGET_DIR + "/{0}".format(fn) for fn in os.listdir(self.MYSQL_CONFIG.TARGET_DIR) if fn.endswith(".sql")]
        return dirs


    def print_sql_dumps(self):
        for dir in self.list_sql_dumps():
            print(dir)

    def prepare_backupfile(self):
        target_dir = self.MYSQL_CONFIG.TARGET_DIR
        self.mkdirs(target_dir)

        filestamp = time.strftime('%Y%m%d%H%M')
        base_filename = self.MYSQL_CONFIG.DATABASE + "_" + filestamp
        sql_file_name = f'{base_filename}.sql'
        sql_file_path = os.path.join(target_dir,sql_file_name)
        self.create_dump(sql_file_path)

        compressed_file_name = f'{base_filename}.tar.gz'
        compressed_file_path = os.path.join(target_dir,compressed_file_name)

        self.make_tarfile(sql_file_path, compressed_file_path)
        return FileModel(compressed_file_path,compressed_file_name)


    def create_dump(self, target_path):
        command = "mysqldump -h %s -P %s -u %s -p%s -A -R -E --triggers --column-statistics=0 --single-transaction > " \
                  "%s" % (
                      self.MYSQL_CONFIG.HOST,
                      self.MYSQL_CONFIG.PORT,
                      self.MYSQL_CONFIG.DB_USER,
                      self.MYSQL_CONFIG.DB_PASS,
                      target_path
                  )
        print("Running...\n" + command)
        self.run_command(command)
        print("\n|| Database dumped to " + target_path+ " || ")


    def run_command(self, command):
        os.system(command)

    def remove_oldest(self,list,max_files):
        totalFiles = len(list)
        while totalFiles > max_files:
            oldest_file = min(list, key=os.path.getctime)
            targetFile = os.path.abspath(oldest_file)
            print("Removing " + targetFile)
            os.remove(os.path.abspath(oldest_file))
            totalFiles = totalFiles - 1

    def clean(self):
        print("Cleaning...")
        if self.GENERAL_CONFIG.KEEP_LOCAL_BACKUPS:
            self.remove_oldest(self.list_tar_backups(), self.GENERAL_CONFIG.MAX_COMPRESSED_DUMPS)
            self.remove_oldest(self.list_sql_dumps(), self.GENERAL_CONFIG.MAX_SQL_DUMPS)
            return
        self.remove_oldest(self.list_tar_backups(), 0)
        self.remove_oldest(self.list_sql_dumps(), 0)