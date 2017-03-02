import errno    
import os
import shutil

import DataDownloader


class WeatherData(object):


    def __init__(self, date, vars, domain):
        self.temp_directory =  'temp/' + self.tag + '/' + date.strftime('%Y%m%d') 
        self.date = date

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

        if not os.path.exists(self.temp_directory):
            os.makedirs(self.temp_directory)

        downloader = DataDownloader.DataDownloader()
       
        for file_name in self.files_to_download:
            file_directory = self.url_directory + file_name
            downloader.download(self.url, file_directory, self.temp_directory)
            print "Download completed for %s" % file_directory


    def ConvertData(self):
        needed_vars = ['files_to_download']
        self.CheckVars('ConvertData', needed_vars)

        if not os.path.exists(self.local_directory):
            os.makedirs(self.local_directory)

        converted_files = []
        for file_name in self.files_to_download:
            temp_file = self.temp_directory + '/' + file_name
            gmt_plus = file_name.split('.')[1][1:3]
            ### NEED TO PUT GMT_PLUS AND THE REST OF THE FORMMATING IN HERE:
            ### rtma_obs_{time}_{vars}_{domain}_2dvaranl_ndfd.grb2'    
            converted_file = self.local_directory + '/' + self.output_filename_format.format(time=date.strft
            DataConverter.convert(temp_file, converted_file)
            converted_files.append(converted_file)
            
        return converted_files    

        #converted_dir = date.strftime(self.local_directory)
        #self.MakeDirs(converted_dir)

    def CleanupTemp(self):
        shutil.rmtree(self.temp_directory)
        








