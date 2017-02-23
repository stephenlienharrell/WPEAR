import ConfigParser

import DataDownloader
import DataVisualizer
import DataComparator
import WebsiteMaker

# args:
# config file, temp directory
# 
# modules for downloading forecasts and observations

TEMP_DIRECTORY=/some/dir

def StartRun():
    config = ConfigParser.RawConfigParser(allow_no_value=True)
    config.read(config_file)

    # Figure out what files to download and proccess

    for forecast_url, forecast_name in forecasts: 
        file_list = FindNewFiles(forecast_url)
        for file_url in file_list:
            raw_file_name = DataDownloader(file_url, temp_dir)
            convereted_file_name = DataConverter.Convert(raw_file_name)

   
    for observation_url, observation_name in observations: 
        file_list = FindNewFiles(forecast_url)
        for file_url in file_list:
            raw_file_name = DataDownloader(file_url, temp_dir)
            convereted_file_name = DataConverter.Convert(raw_file_name)

    for proccessing_time in TimesForProccessing(config):
        # stephen figures out how to find the files
        grib_compared_object = DataComparator.compare(forecast_file, observation_files)
        DataVisualizer.Heatmap(grib_compared_object, file_name)
        DataVisualizer.Heatmap(grib_object, file_name)
        DataVisualizer.Heatmap(grib_object, file_name)

        WebsiteMaker.MakePage(time, archived_obs, archived_forecast, heatmap_obs, heatmap_forecast, heatmap_compared)



def FindNewFiles(config):
    # figure out what files we need
    # make sure we dont list everything 
    DataDownloader.ListDirectory()

def TimesForProccessing(config):
    pass



