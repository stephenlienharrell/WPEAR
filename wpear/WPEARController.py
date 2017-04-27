import datetime
import os
import HRRRSurfaceForecasts
import HRRRSurfaceObservations
import RTMAObservations
import WebsiteGenerator

VARS = ['2MT', 'DPT']
DOMAIN = 'IND90k'

def StartRun(options):

    now = datetime.datetime.utcnow()
    one_day_delta = datetime.timedelta(days=1)

    hrrr_dates = [now - one_day_delta, now]
    for date in hrrr_dates:
        print 'Starting HRRR Forecasts for ' + date.strftime('%Y%m%d')
        hrrr_fcast = HRRRSurfaceForecasts.HRRRSurfaceForecasts(date,
                VARS, DOMAIN, options, testing=options.testing)
#        hrrr_fcast.DownloadData()
#        hrrr_fcast.CleanupDownloads()
#        hrrr_fcast.VisualizeData()
        hrrr_fcast.VisualizeAnimatedForecast()

    rtma_dates = [now - one_day_delta, now]
    for date in rtma_dates:
        print 'Starting RTMA Observations for ' + date.strftime('%Y%m%d')
        rtma_obs = RTMAObservations.RTMAObservations(date,
                VARS, DOMAIN, options, testing=options.testing)
 #       rtma_obs.DownloadData()
 #       rtma_obs.CleanupDownloads()
 #       rtma_obs.VisualizeData()
        rtma_obs.VisualizeDifference(hrrr_fcast, 'DIF')
        rtma_obs.VisualizeAnimatedDifference(hrrr_fcast, 'ADIF')
        rtma_obs.VisualizeStandardDeviation(hrrr_fcast)
        
    # not sure how hrrr_fcast/rtma_obs exist out-of-scope
    # but it works
    wg = WebsiteGenerator.WebsiteGenerator(webdir = options.web_dir)
    wg.runWebManager(hrrr_fcast, rtma_obs)


#    for date in hrrr_dates:
#        print 'Starting HRRR Observations for ' + date.strftime('%Y%m%d')
#        hrrr_obs = HRRRSurfaceObservations.HRRRSurfaceObservations(date,
#                VARS, DOMAIN, options, testing=options.testing)
#        hrrr_obs.DownloadData()
#        hrrr_obs.ConvertData()
#        hrrr_obs.CleanupDownloads()
#        hrrr_obs.VisualizeData()
#        hrrr_obs.VisualizeDifference(hrrr_fcast, 'DIF')

