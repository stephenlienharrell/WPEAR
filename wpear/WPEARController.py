#import ConfigParser
import datetime
import pygrib

import DataDownloader
import DataConverter
import DataVisualizer
import DataComparator

# args:
# config file, temp directory
# 
# modules for downloading forecasts and observations

DOWNLOAD_DIRECTORY = '/downloads'
HRRR_MAIN_URL = 'http://www.ftp.ncep.noaa.gov/'
HRRR_DIRECTORY = 'data/nccf/com/hrrr/prod/hrrr.%s' % datetime.datetime.now().strftime("%Y%m%d")

def StartRun():
#    config = ConfigParser.RawConfigParser(allow_no_value=True)
#    config.read(config_file)


    downloader = DataDownloader.DataDownloader()
#    todays_files = downloader.listDirectory(HRRR_MAIN_URL)
    hrrr_file1 = 'hrrr.t02z.wrfsfcf00.grib2'
    hrrr_file2 = 'hrrr.t04z.wrfsfcf00.grib2'

    file1_url = '%s/%s' % (HRRR_DIRECTORY, hrrr_file1)
    file2_url = '%s/%s' % (HRRR_DIRECTORY, hrrr_file2)
    d_file1 = downloader.download(HRRR_MAIN_URL, file1_url, DOWNLOAD_DIRECTORY)
    d_file2 =  downloader.download(HRRR_MAIN_URL, file2_url, DOWNLOAD_DIRECTORY)

    # do converted file here
    DataConverter.convert(d_file1, 'converted/%s' % hrrr_file1)
    DataConverter.convert(d_file2, 'converted/%s' % hrrr_file2)
    
    gribFile = 'converted/%s' % hrrr_file1
    grbs = pygrib.open(gribFile)
    grb = grbs.select(name='2 metre temperature')[0]
    file_name = "out/fore1.jpg"

    v = DataVisualizer.DataVisualizer(None)

    v.Heatmap(grb, file_name)


    gribFile = 'converted/%s' % hrrr_file2
    grbs = pygrib.open(gribFile)
    grb = grbs.select(name='2 metre temperature')[0]
    file_name = "out/fore2.jpg"

    v = DataVisualizer.DataVisualizer(None)
    v.Heatmap(grb, file_name)



    grb = DataComparator.DataComparator('converted/%s' % hrrr_file1, 'converted/%s' % hrrr_file2)
    
    file_name = "out/compare.jpg"

    v = DataVisualizer.DataVisualizer(None)
    v.Heatmap(grb, file_name)






    # Figure out what files to download and proccess

    # sketch of proccess:

#    for forecast_url, forecast_name in forecasts: 
#        file_list = FindNewFiles(forecast_url)
#        for file_url in file_list:
#            raw_file_name = DataDownloader(file_url, temp_dir)
#            convereted_file_name = DataConverter.Convert(raw_file_name)

   
#    for observation_url, observation_name in observations: 
#        file_list = FindNewFiles(forecast_url)
#        for file_url in file_list:
#            raw_file_name = DataDownloader(file_url, temp_dir)
#            convereted_file_name = DataConverter.Convert(raw_file_name)
#
#    for proccessing_time in TimesForProccessing(config):
#        # stephen figures out how to find the files
#        grib_compared_object = DataComparator.compare(forecast_file, observation_files)
#        DataVisualizer.Heatmap(grib_compared_object, file_name)
#        DataVisualizer.Heatmap(grib_object, file_name)
#        DataVisualizer.Heatmap(grib_object, file_name)
#
#        WebsiteMaker.MakePage(time, archived_obs, archived_forecast, heatmap_obs, heatmap_forecast, heatmap_compared)



#def FindNewFiles(config):
    # figure out what files we need
    # make sure we dont list everything 
#    DataDownloader.ListDirectory()

#def TimesForProccessing(config):
#    pass



