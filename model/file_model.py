class FileModel:
    name: str
    full_path: str

    def __init__(self, full_path, name):
        self.name = name
        self.full_path = full_path
