import datetime

import HRRRSurfaceForecasts
import HRRRSurfaceObservations
import RTMAObservations

VARS = ['2MT', 'DPT']
DOMAIN = 'IND90k'


def StartRun(options):

    now = datetime.datetime.utcnow()
    one_day_delta = datetime.timedelta(days=1)

    if options.testing:
        hrrr_fcast = HRRRSurfaceForecasts.HRRRSurfaceForecasts(now - one_day_delta,
                VARS, DOMAIN, options, testing=options.testing)
        hrrr_fcast.DownloadData()
        hrrr_fcast.ConvertData()
        hrrr_fcast.CleanupDownloads()
        hrrr_fcast.VisualizeData()
        hrrr_fcast.VisualizeAnimatedForecast()
        
        rtma_obs = RTMAObservations.RTMAObservations(now - one_day_delta,
                VARS, DOMAIN, options, testing=options.testing)
        rtma_obs.DownloadData()
        rtma_obs.ConvertData()
        rtma_obs.CleanupDownloads()
        rtma_obs.VisualizeData()
        rtma_obs.VisualizeDifference(hrrr_fcast, 'DIF')
        return

    hrrr_dates = [now, now - one_day_delta]
    for date in hrrr_dates:
        print 'Starting HRRR Forecasts for ' + date.strftime('%Y%m%d')
        hrrr_fcast = HRRRSurfaceForecasts.HRRRSurfaceForecasts(date,
                VARS, DOMAIN, options, testing=options.testing)
        hrrr_fcast.DownloadData()
        hrrr_fcast.ConvertData()
        hrrr_fcast.CleanupDownloads()
        hrrr_fcast.VisualizeData()
        hrrr_fcast.VisualizeAnimatedForecast()

    rtma_dates = [now, now - one_day_delta]
    for date in rtma_dates:
        print 'Starting RTMA Observations for ' + date.strftime('%Y%m%d')
        rtma_obs = RTMAObservations.RTMAObservations(date,
                VARS, DOMAIN, options, testing=options.testing)
        rtma_obs.DownloadData()
        rtma_obs.ConvertData()
        rtma_obs.CleanupDownloads()
        rtma_obs.VisualizeData()
        rtma_obs.VisualizeDifference(hrrr_fcast, 'DIF')
        

#    for date in hrrr_dates:
#        print 'Starting HRRR Observations for ' + date.strftime('%Y%m%d')
#        hrrr_obs = HRRRSurfaceObservations.HRRRSurfaceObservations(date,
#                VARS, DOMAIN, options, testing=options.testing)
#        hrrr_obs.DownloadData()
#        hrrr_obs.ConvertData()
#        hrrr_obs.CleanupDownloads()
#        hrrr_obs.VisualizeData()
#        hrrr_obs.VisualizeDifference(hrrr_fcast, 'DIF')

