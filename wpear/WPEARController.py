import datetime

import HRRRSurfaceForecasts
import HRRRSurfaceObservations
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
        print 'Starting RTMA Observations for ' + date.strftime('%Y%m%d')
        rtma_obs = RTMAObservations.RTMAObservations(date,
                VARS, DOMAIN, DOWNLOAD_DIRECTORY, WEB_DIRECTORY)
        rtma_obs.DownloadData()
        rtma_obs.ConvertData()
        rtma_obs.CleanupDownloads()
        rtma_obs.VisualizeData()
        
    hrrr_dates = [now, now - one_day_delta]
    for date in hrrr_dates:
        print 'Starting HRRR Forecasts for ' + date.strftime('%Y%m%d')
        hrrr_fcast = HRRRSurfaceForecasts.HRRRSurfaceForecasts(date,
                VARS, DOMAIN, DOWNLOAD_DIRECTORY, WEB_DIRECTORY)
        hrrr_fcast.DownloadData()
        hrrr_fcast.ConvertData()
        hrrr_fcast.CleanupDownloads()
        hrrr_fcast.VisualizeData()

    for date in hrrr_dates:
        print 'Starting HRRR Observations for ' + date.strftime('%Y%m%d')
        hrrr_obs = HRRRSurfaceObservations.HRRRSurfaceObservations(date,
                VARS, DOMAIN, DOWNLOAD_DIRECTORY, WEB_DIRECTORY)
        hrrr_obs.DownloadData()
        hrrr_obs.ConvertData()
        hrrr_obs.CleanupDownloads()
        hrrr_obs.VisualizeData()
        hrrr_obs.VisualizeDifference(hrrr_fcast, 'DIF')

