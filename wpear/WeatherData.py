import errno    
import os

import DataDownloader

TEMP_DIR = 'temp'

class WeatherData(object):


    def __init__(self):
        #self.domain = config.something?
        #self.variables = '_'.join(config.something?)
        pass

    def MakeDirs(self, path):
        try:
            os.makedirs(path)
        except OSError as exception:
            if exception.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise

    def CheckVars(self, function, vars):
        for var in vars:
            if not hasattr(self, var):
                raise AttributeError('Variable self.%s not found and is needed in the %s function' % 
                        (var, function))

    def DownloadData(self, date):
        needed_vars = ['url', 'url_directory', 'files_to_download', 'local_directory']
        self.CheckVars('DownloadData', needed_vars)
        downloader = DataDownloader.DataDownloader()
       
        for file_name in self.files_to_download:
            file_directory = date.strftime(self.url_directory) + file_name
            downloader.download(self.url, file_directory, TEMP_DIR)


        #converted_dir = date.strftime(self.local_directory)
        #self.MakeDirs(converted_dir)





