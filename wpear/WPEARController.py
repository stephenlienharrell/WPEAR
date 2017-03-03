import datetime
import pygrib

import DataComparator
import DataConverter
import DataDownloader
import DataVisualizer
import RTMAObservations
import WebsiteGenerator


DOWNLOAD_DIRECTORY = 'temp'
WEB_DIRECTORY = 'web'
VARS = ['2MT', 'DPT']
DOMAIN = 'IND90k'

def StartRun():

    today_rtma_obs = RTMAObservations.RTMAObservations(datetime.datetime.utcnow(),
            VARS, DOMAIN, DOWNLOAD_DIRECTORY, WEB_DIRECTORY)
    today_rtma_obs.DownloadData()
    today_rtma_obs.ConvertData()
    today_rtma_obs.CleanupDownloads()



CONVERTED_DIRECTORY = 'converted'
HRRR_MAIN_URL = 'http://www.ftp.ncep.noaa.gov/'
HRRR_DIRECTORY = 'data/nccf/com/hrrr/prod/hrrr.%s'

def StartRunOld():


    downloader = DataDownloader.DataDownloader()
    hrrr_file1 = 'hrrr.t02z.wrfsfcf00.grib2'
    hrrr_file2 = 'hrrr.t04z.wrfsfcf00.grib2'
    timestamp = datetime.datetime.now().strftime("%Y%m%d")
    hrrr_dir = HRRR_DIRECTORY % timestamp

    
    file1_url = '%s/%s' % (hrrr_dir, hrrr_file1)
    file2_url = '%s/%s' % (hrrr_dir, hrrr_file2)
    print "Downloading Forecast 1"
    d_file1 = downloader.download(HRRR_MAIN_URL, file1_url, DOWNLOAD_DIRECTORY)
    print "Downloading Forecast 2"
    d_file2 =  downloader.download(HRRR_MAIN_URL, file2_url, DOWNLOAD_DIRECTORY)

    # do converted file here
    print "Converting Forecast 1"
    converted_file1 = '%s/%s' % (CONVERTED_DIRECTORY, hrrr_file1)
    converted_file2 = '%s/%s' % (CONVERTED_DIRECTORY, hrrr_file2)
    DataConverter.convert(d_file1, converted_file1)
    print "Converting Forecast 2"
    DataConverter.convert(d_file2, converted_file2)
   
    print "Creating heatmap for Forecast 1"
    gribFile = converted_file1
    grbs = pygrib.open(gribFile)
    grb = grbs.select(name='2 metre temperature')[0]
    file_name = "out/fore1.jpg"

    v = DataVisualizer.DataVisualizer(None)

    v.Heatmap(grb, file_name)


    print "Creating heatmap for Forecast 2"
    gribFile = converted_file2
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

    print "Creating website for forecasts"
    hrrr_file1_name = "%s-%s" % (hrrr_file1, timestamp)
    hrrr_file2_name = "%s-%s" % (hrrr_file1, timestamp)
    WebsiteGenerator.showWebsite("out/fore1.jpg", hrrr_file1_name, "out/fore2.jpg", hrrr_file2_name, "out/compare.jpg")
