import WeatherData


class HRRRSurfaceForecasts(WeatherData.WeatherData):
   
    def __init__(self, date, vars, domain, options, testing=False):

        self.obs = False

        self.tag = 'hrrr_fcast'

        # WRF surface
        self.extra_info = 'wrfsfc' 

        self.url = 'http://www.ftp.ncep.noaa.gov'

        self.url_directory = date.strftime('/data/nccf/com/hrrr/prod/hrrr.%Y%m%d/')

        self.download_file_name = 'hrrr.t{gmt_plus:02d}z.wrfsfcf{forecast_number:02d}.grib2'

        self.local_directory_date_format = '/%Y/%m/%d/hrrr_fcast'

        self.local_directory = options.web_dir + date.strftime(self.local_directory_date_format)

        self.local_secondary_directory = options.web_dir + date.strftime('/hrrr_fcast/%Y/%m/%d')

        self.output_filename_format = 'hrrr_fcast.{time}.{vars}.{domain}.{extra_info}f{forecast_number:02d}.grb2'

        self.output_filename_format_heatmap_viz = 'hrrr_fcast.{time}.{vars}.{domain}.{extra_info}f{forecast_number:02d}.heatmap.png'
        self.output_filename_format_heatmap_animation_viz = 'hrrr_fcast.{time}.{vars}.{domain}.{extra_info}.heatmap_anim.gif'

        self.date_format = '%Y%m%d'

        self.files_to_download = []
        self.converted_files = []
        self.visualization_heatmap_files = []
        self.converted_files_by_hour = []
        self.forecast_animation_files = []

        for i in range(0,24):

            self.converted_files_by_hour.append([])
            gmt_plus = 't{gmt_plus:02d}z'.format(gmt_plus=i)
            self.forecast_animation_files.append(
                    self.local_directory + '/' + self.output_filename_format_heatmap_animation_viz.format(
                    time=date.strftime(self.date_format) + '_' + gmt_plus, vars='_'.join(vars),
                    domain=domain, extra_info=self.extra_info))

            for j in range(1,19):

                self.files_to_download.append(self.download_file_name.format(gmt_plus=i, forecast_number=j))

                converted_file = self.local_directory + '/' + self.output_filename_format.format(
                    time=date.strftime(self.date_format) + '_' + gmt_plus, vars='_'.join(vars),
                    domain=domain, forecast_number=j, extra_info=self.extra_info)
                self.converted_files.append(converted_file)
                self.converted_files_by_hour[i].append(converted_file)

                visualization_heatmap_file = self.local_directory + '/' + self.output_filename_format_heatmap_viz.format(
                    time=date.strftime(self.date_format) + '_' + gmt_plus, vars='_'.join(vars),
                    domain=domain, forecast_number=j, extra_info=self.extra_info)
                self.visualization_heatmap_files.append(visualization_heatmap_file)

        self.var_lookup_table = {}
        self.var_lookup_table['2MTK'] = ':TMP:2 m above ground'
        self.var_lookup_table['DPT'] = ':DPT:2 m above ground'


        if testing:
            self.files_to_download = []
            for i in range(0,19):
                self.files_to_download.append(self.download_file_name.format(gmt_plus=0, forecast_number=i))

        #justforecastthings
        self.max_fcast = 18
        self.hours_between_fcasts = 1

        super(HRRRSurfaceForecasts, self).__init__(date, vars, domain, options)
