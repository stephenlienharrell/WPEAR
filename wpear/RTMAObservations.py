import datetime

import WeatherData


class RTMAObservations(WeatherData.WeatherData):
   
    def __init__(self, date, vars, domain, options, testing=False):

        self.obs = True

        self.tag = 'rtma_obs'

        #  (2-D variational), anl is short for "analysis", ndfd is National Digital Forecast Database
        self.extra_info = '2dvaranl_ndfd'

        self.url = 'http://www.ftp.ncep.noaa.gov'

        self.url_directory = date.strftime('/data/nccf/com/rtma/prod/rtma2p5.%Y%m%d/')

        self.download_file_name = 'rtma2p5.t{gmt_plus:02d}z.2dvaranl_ndfd.grb2'

        self.local_directory = options.web_dir + date.strftime('/%Y/%m/%d/rtma_obs')

        self.local_secondary_directory = options.web_dir + date.strftime('/rtma_obs/%Y/%m/%d')

        self.output_filename_format = 'rtma_obs.{time}.{vars}.{domain}.2dvaranl_ndfd.grb2'

        self.output_filename_format_heatmap_viz = 'rtma_obs.{time}.{vars}.{domain}.2dvaranl_ndfd.heatmap.png'
        self.output_filename_format_stddev_viz = 'rtma_obs.{time}.{vars}.{domain}.2dvaranl_ndfd.{fcast_tag}.stddev.png'

        self.date_format = '%Y%m%d'

        self.files_to_download = []
        self.converted_files = []
        self.visualization_heatmap_files = []
        self.visualization_difference_files = []
        self.visualization_animated_difference_files = []
        self.visualization_stddev_files = []

        for x in range(0,24):
            self.files_to_download.append(self.download_file_name.format(gmt_plus=x))


            gmt_plus = 't{gmt_plus:02d}z'.format(gmt_plus=x)
            converted_file = self.local_directory + '/' + self.output_filename_format.format(
                    time=date.strftime('%Y%m%d') + '_' + gmt_plus, vars='_'.join(vars),
                    domain=domain)
            self.converted_files.append(converted_file)

            visualization_heatmap_file = self.local_directory + '/' + self.output_filename_format_heatmap_viz.format(
                    time=date.strftime('%Y%m%d') + '_' + gmt_plus, vars='_'.join(vars),
                    domain=domain)
            self.visualization_heatmap_files.append(visualization_heatmap_file)

        if testing:
            self.files_to_download = [self.download_file_name.format(gmt_plus=0)]
            self.files_to_download.append(self.download_file_name.format(gmt_plus=1))
            self.files_to_download.append(self.download_file_name.format(gmt_plus=2))

        self.var_lookup_table = {}
        self.var_lookup_table['2MTK'] = 'TMP:2 m above ground'
        self.var_lookup_table['DPT'] = 'DPT:2 m above ground'
        super(RTMAObservations, self).__init__(date, vars, domain, options)

    # OBS Specific
    def _GetTimeOfObs(self, file_name):
        time_text = file_name.split('.')[1]
        time_format = '%Y%m%d_t%Hz'
        date = datetime.datetime.strptime(time_text, time_format)
        # What to do about timezones?
        return date
