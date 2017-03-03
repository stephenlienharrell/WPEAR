import datetime

import HRRRForecasts
import HRRRObservations
import RTMAObservations

DOWNLOAD_DIRECTORY = 'temp'
WEB_DIRECTORY = 'web'
VARS = ['2MT', 'DPT']
DOMAIN = 'IND90k'

def StartRun():

    now = datetime.datetime.utcnow()
    one_day_delta = datetime.timedelta(days=1)


    rtma_dates = [now, now - one_day_delta]
    for date in rtma_dates:
        print 'Starting RTMA Obsevations for ' + date.strftime('%Y%m%d')
        rtma_obs = RTMAObservations.RTMAObservations(date,
                VARS, DOMAIN, DOWNLOAD_DIRECTORY, WEB_DIRECTORY)
        rtma_obs.DownloadData()
        rtma_obs.ConvertData()
        rtma_obs.CleanupDownloads()
        rtma_obs.VisualizeData()
        
    del(rtma_obs)

    hrrr_dates = [now, now - one_day_delta]
    for date in hrrr_dates:
        print 'Starting HRRR Obsevations for ' + date.strftime('%Y%m%d')
        hrrr_obs = HRRRObservations.HRRRObservations(date,
                VARS, DOMAIN, DOWNLOAD_DIRECTORY, WEB_DIRECTORY)
        hrrr_obs.DownloadData()
        hrrr_obs.ConvertData()
        hrrr_obs.CleanupDownloads()
        hrrr_obs.VisualizeData()
        
    del(hrrr_obs)

    for date in hrrr_dates:
        print 'Starting HRRR Forecasts for ' + date.strftime('%Y%m%d')
        hrrr_fcast = HRRRForecasts.HRRRForecasts(date,
                VARS, DOMAIN, DOWNLOAD_DIRECTORY, WEB_DIRECTORY)
        hrrr_fcast.DownloadData()
        hrrr_fcast.ConvertData()
        hrrr_fcast.CleanupDownloads()
        hrrr_fcast.VisualizeData()
        
    del(hrrr_obs)
