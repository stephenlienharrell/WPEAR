import errno    
import os
import shutil

import DataDownloader
import DataConverter


class WeatherData(object):


    def __init__(self, date, vars, domain, download_directory, web_directory):
        self.temp_directory =  download_directory + '/' + self.tag + '/' + date.strftime('%Y%m%d') 
        self.date = date
        self.vars = vars
        self.domain = domain

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

    def DownloadData(self):
        needed_vars = ['url', 'url_directory', 'files_to_download']
        self.CheckVars('DownloadData', needed_vars)

        print "Starting data downloads"

        if not os.path.exists(self.temp_directory):
            os.makedirs(self.temp_directory)

        downloader = DataDownloader.DataDownloader()

       
        for index, file_name in enumerate(self.files_to_download):
            converted_file = self.converted_files[index]
            if os.path.exists(converted_file):
                continue

            file_directory = self.url_directory + file_name
            try:
                downloader.download(self.url, file_directory, self.temp_directory)
            except IOError, e:
                try:
                    if e[1] != 404:
                        raise
                except:
                    raise
                continue

            print "Download completed for %s" % file_directory


    def ConvertData(self):
        needed_vars = ['files_to_download']
        self.CheckVars('ConvertData', needed_vars)

        print "Starting data conversion"

        if not os.path.exists(self.local_directory):
            os.makedirs(self.local_directory)

        converted_files = []
        for index, file_name in enumerate(self.files_to_download):
            temp_file = self.temp_directory + '/' + file_name
            if not os.path.exists(temp_file):
                continue
            converted_file = self.converted_files[index]
            if os.path.exists(converted_file):
                continue
            DataConverter.convert(temp_file, converted_file)
            print "Conversion completed for " + temp_file
            converted_files.append(converted_file)
            
        return converted_files

    def VisualizeData(self):
        pass
        

    def CleanupDownloads(self):
        #TODO:  need to cleanup date based parent directories
        shutil.rmtree(self.temp_directory)
