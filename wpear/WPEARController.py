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

    # downloading

    hrrr_dates = [now - one_day_delta, now]
    for date in hrrr_dates:
        print 'Starting HRRR Downloading Forecasts for ' + date.strftime('%Y%m%d')
        hrrr_fcast = HRRRSurfaceForecasts.HRRRSurfaceForecasts(date,
                VARS, DOMAIN, options, testing=options.testing)
        hrrr_fcast.DownloadData()

    rtma_dates = [now - one_day_delta, now]
    for date in rtma_dates:
        print 'Starting Downloading RTMA Observations for ' + date.strftime('%Y%m%d')
        rtma_obs = RTMAObservations.RTMAObservations(date,
                VARS, DOMAIN, options, testing=options.testing)
        rtma_obs.DownloadData()

    hrrr_dates = []
    rtma_dates = []
    for i in reversed(range(0, 8)):
        hrrr_dates.append(now - (one_day_delta * i))
        rtma_dates.append(now - (one_day_delta * i))

    data_list = []
    for date in hrrr_dates:
        hrrr_fcast = HRRRSurfaceForecasts.HRRRSurfaceForecasts(date,
                VARS, DOMAIN, options, testing=options.testing)
        rtma_obs = RTMAObservations.RTMAObservations(date,
                VARS, DOMAIN, options, testing=options.testing)

        data_list.append((hrrr_fcast, rtma_obs))

        if os.path.exists(hrrr_fcast.local_directory):
            print 'Starting HRRR Forecasts for ' + date.strftime('%Y%m%d')
            hrrr_fcast.VisualizeData()
            hrrr_fcast.VisualizeAnimatedForecast()

        if os.path.exists(rtma_obs.local_directory):
            print 'Starting RTMA Observations for ' + date.strftime('%Y%m%d')
            rtma_obs.VisualizeData()
            rtma_obs.VisualizeDifference(hrrr_fcast, 'DIF')
            rtma_obs.VisualizeAnimatedDifference(hrrr_fcast, 'ADIF')
            rtma_obs.VisualizeStandardDeviation(hrrr_fcast)

        print "Generating Website"
        wg = WebsiteGenerator.WebsiteGenerator(data_list, webdir = options.web_dir)
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

