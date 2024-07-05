import os


class Config:
    def __init__(self):
        try:
            self.username: str = os.environ['GRASS_USER']
            self.password: str = os.environ['GRASS_PASSWORD']
            self.extension_id: str = os.environ['GRASS_CRX_EXTENSION_ID']
            self.crx_name: str = os.environ['GRASS_CRX_NAME']
            if self.username == "" or self.password == "" or self.extension_id == "" or self.crx_name == "":
                raise EnvironmentError()
        except EnvironmentError:
            print('invalid environment variables')
