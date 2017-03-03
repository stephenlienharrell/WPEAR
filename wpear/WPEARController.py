import datetime

import DataDownloader
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
        
    del(rtma_obs)
