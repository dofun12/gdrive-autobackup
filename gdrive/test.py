from gdrive import gdrive_api

if __name__=="__main__":
    service = gdrive_api.init_api()
    gdrive_api.list_files(service)