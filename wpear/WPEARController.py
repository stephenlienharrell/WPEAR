import datetime
import pygrib

import DataDownloader
import DataConverter
import DataVisualizer
import DataComparator


DOWNLOAD_DIRECTORY = '/downloads'
HRRR_MAIN_URL = 'http://www.ftp.ncep.noaa.gov/'
HRRR_DIRECTORY = 'data/nccf/com/hrrr/prod/hrrr.%s' % datetime.datetime.now().strftime("%Y%m%d")

def StartRun():


    downloader = DataDownloader.DataDownloader()
    hrrr_file1 = 'hrrr.t02z.wrfsfcf00.grib2'
    hrrr_file2 = 'hrrr.t04z.wrfsfcf00.grib2'

    
    file1_url = '%s/%s' % (HRRR_DIRECTORY, hrrr_file1)
    file2_url = '%s/%s' % (HRRR_DIRECTORY, hrrr_file2)
    print "Downloading Forecast 1"
    d_file1 = downloader.download(HRRR_MAIN_URL, file1_url, DOWNLOAD_DIRECTORY)
    print "Downloading Forecast 2"
    d_file2 =  downloader.download(HRRR_MAIN_URL, file2_url, DOWNLOAD_DIRECTORY)

    # do converted file here
    print "Converting Forecast 1"
    DataConverter.convert(d_file1, 'converted/%s' % hrrr_file1)
    print "Converting Forecast 2"
    DataConverter.convert(d_file2, 'converted/%s' % hrrr_file2)
   
    print "Creating heatmap for Forecast 1"
    gribFile = 'converted/%s' % hrrr_file1
    grbs = pygrib.open(gribFile)
    grb = grbs.select(name='2 metre temperature')[0]
    file_name = "out/fore1.jpg"

    v = DataVisualizer.DataVisualizer(None)

    v.Heatmap(grb, file_name)


    print "Creating heatmap for Forecast 2"
    gribFile = 'converted/%s' % hrrr_file2
    grbs = pygrib.open(gribFile)
    grb = grbs.select(name='2 metre temperature')[0]
    file_name = "out/fore2.jpg"

    v = DataVisualizer.DataVisualizer(None)
    v.Heatmap(grb, file_name)



    print "Creating comparison between the two forecasts"
    grb = DataComparator.DataComparator('converted/%s' % hrrr_file1, 'converted/%s' % hrrr_file2)
    
    print "Creating heatmap for comparison of forecasts"
    file_name = "out/compare.jpg"

    v = DataVisualizer.DataVisualizer(None)
    v.Heatmap(grb, file_name)
