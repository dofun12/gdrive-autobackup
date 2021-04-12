import os
import configparser
import time
import tarfile
from gdrive import gdrive_api
from gdrive.gdrive_api import GDriveApi
from model.gdrive_config_model import GDriveConfigModel
from model.mysql_config_model import MysqlConfigModel


class Backup:
    MYSQL_CONFIG: MysqlConfigModel
    GDRIVE_CONFIG: GDriveConfigModel

    def __init__(self, mysql_config: MysqlConfigModel, gdrive_config: GDriveConfigModel):
        self.MYSQL_CONFIG = mysql_config
        self.GDRIVE_CONFIG = gdrive_config

    def ensure_dir(self, directory):
        if not os.path.exists(directory):
            os.makedirs(directory)

    def list_dirs(self):
        self.ensure_dir(self.MYSQL_CONFIG.TARGET_DIR)
        dirs = [fn for fn in os.listdir(self.MYSQL_CONFIG.TARGET_DIR) if fn.endswith(".sql")]
        full_path = [self.MYSQL_CONFIG.TARGET_DIR + "/{0}".format(x) for x in dirs]
        totalFiles = 0
        for dir in dirs:
            print(dir)
            totalFiles = totalFiles + 1
        print("Total files: " + str(totalFiles))
        if totalFiles >= 10:
            oldest_file = min(full_path, key=os.path.getctime)
            targetFile = os.path.abspath(oldest_file)
            print("Removing " + targetFile)
            os.remove(os.path.abspath(oldest_file))

    def create_dump(self, filename, filepath):
        command = "mysqldump -h %s -P %s -u %s -p%s -A -R -E --triggers --column-statistics=0 --single-transaction > " \
                  "%s/%s.sql" % (
                      self.MYSQL_CONFIG.HOST,
                      self.MYSQL_CONFIG.PORT,
                      self.MYSQL_CONFIG.DB_USER,
                      self.MYSQL_CONFIG.DB_PASS,
                      self.MYSQL_CONFIG.TARGET_DIR,
                      filename
                  )
        print("Running...\n" + command)
        self.run_command(command)
        print("\n|| Database dumped to " + filepath + ".sql || ")
        return filepath

    #
    # def run_command(command):
    #    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    #
    #    (output, err) = p.communicate()
    #
    #    # This makes the wait possible
    #    p_status = p.wait()
    #
    #    # This will give you the output of the command being executed
    #    if not output:
    #        print("Command output: " + output)
    def run_command(self, command):
        os.system(command)

    def make_tarfile(self, output_filename, source_file):
        tar = tarfile.open(output_filename, "w:gz")
        tar.add(source_file)
        tar.close()

    def init_backup(self):
        self.list_dirs()

        filestamp = time.strftime('%Y-%m-%d-%H-%M')
        filename = self.MYSQL_CONFIG.DATABASE + "_" + filestamp
        filepath = self.MYSQL_CONFIG.TARGET_DIR + "/" + filename

        self.create_dump(filename, filepath)
        compressed_file = filename + ".tar.gz"
        self.make_tarfile(compressed_file, (filepath + ".sql"))
        print("Starting upload... " + compressed_file + " at " + compressed_file)
        gdrive_api = GDriveApi(self.GDRIVE_CONFIG)
        gdrive_api.upload_file(compressed_file, compressed_file)
