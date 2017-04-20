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

    if options.testing:
        hrrr_fcast = HRRRSurfaceForecasts.HRRRSurfaceForecasts(now - one_day_delta,
                VARS, DOMAIN, options, testing=options.testing)
        hrrr_fcast.DownloadData()
        hrrr_fcast.ConvertData()
        hrrr_fcast.CleanupDownloads()
        hrrr_fcast.VisualizeData()
        viz_anim_fcast = hrrr_fcast.VisualizeAnimatedForecast()
        
        rtma_obs = RTMAObservations.RTMAObservations(now - one_day_delta,
                VARS, DOMAIN, options, testing=options.testing)
        rtma_obs.DownloadData()
        rtma_obs.ConvertData()
        rtma_obs.CleanupDownloads()
        rtma_obs.VisualizeData()
        # viz_diff_obs = rtma_obs.VisualizeDifference(hrrr_fcast, 'DIF')
        viz_anim_diff_obs = rtma_obs.VisualizeAnimatedDifference(hrrr_fcast, 'DIF')

        # website
        vizlist = []
        # vizlist.append('SECTION: Static Forecasts')
        # for file in hrrr_fcast.visualization_heatmap_files:
        #     if os.path.exists(file):
        #         vizlist.append([file, 'tag = {}'.format(file.split('/')[-1].split('.heatmap.png')[0])])
        #         break
        # vizlist.append('SECTION: Dynamic Forecasts')
        # vizlist.append([viz_anim_fcast, 'tag = {}'.format(viz_anim_fcast.split('/')[-1].split('.heatmap_anim.gif')[0])])
        # vizlist.append('SECTION: Observations')
        # for file in rtma_obs.visualization_heatmap_files:
        #     if os.path.exists(file):
        #         vizlist.append([file, 'tag = {}'.format(file.split('/')[-1].split('.heatmap.png')[0])])
        #         break;
        # vizlist.append('SECTION: Forecasts vs Observations')
        # vizlist.append([viz_diff_obs,'tag = {}'.format(file.split('/')[-1].split('.heatmap.png')[0])])
        # WebsiteGenerator.showWebsite(vizlist)
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

