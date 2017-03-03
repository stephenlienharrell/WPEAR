import WeatherData


class HRRRForecasts(WeatherData.WeatherData):
   
    def __init__(self, date, vars, domain, download_directory, web_directory):

        self.tag = 'hrrr_fcast'

        self.url = 'http://www.ftp.ncep.noaa.gov'

        self.url_directory = date.strftime('/data/nccf/com/hrrr/prod/hrrr.%Y%m%d/')

        self.download_file_name = 'hrrr.t{gmt_plus:02d}z.wrfsfcf{forecast_number:02d}.grib2'

        self.local_directory = web_directory + date.strftime('/%Y/%m/%d/hrrr_fcast')

        self.local_secondary_directory = web_directory + date.strftime('/hrrr_fcast/%Y/%m/%d')

        self.output_filename_format = 'hrrr_fcast.{time}.{vars}.{domain}.wrfsfcf{forecast_number:02d}.grb2'

        self.output_filename_format_heatmap_viz = 'hrrr_fcast.{time}.{vars}.{domain}.wrfsfcf{forecast_number:02d}.heatmap.png'


        self.files_to_download = []
        self.converted_files = []
        self.visualization_heatmap_files = []

        for i in range(0,24):
            for j in range(1,19):

                self.files_to_download.append(self.download_file_name.format(gmt_plus=i, forecast_number=j))

                gmt_plus = 't{gmt_plus:02d}z'.format(gmt_plus=i)
                converted_file = self.local_directory + '/' + self.output_filename_format.format(
                    time=date.strftime('%Y%m%d') + '_' + gmt_plus, vars='_'.join(vars),
                    domain=domain, forecast_number=j)
                self.converted_files.append(converted_file)

                visualization_heatmap_file = self.local_directory + '/' + self.output_filename_format_heatmap_viz.format(
                    time=date.strftime('%Y%m%d') + '_' + gmt_plus, vars='_'.join(vars),
                    domain=domain, forecast_number=j)
                self.visualization_heatmap_files.append(visualization_heatmap_file)

        var_lookup_table = {}
        var_lookup_table['2MTK'] = 54
        var_lookup_table['DPT'] = 57

        super(HRRRForecasts, self).__init__(date, vars, domain, download_directory, web_directory)


