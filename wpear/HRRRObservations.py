import WeatherData


class HRRRObservations(WeatherData.WeatherData):
   
    def __init__(self, date, vars, domain, download_directory, web_directory):

        self.tag = 'hrrr_obs'

        self.url = 'http://www.ftp.ncep.noaa.gov'

        self.url_directory = date.strftime('/data/nccf/com/hrrr/prod/hrrr.%Y%m%d/')

        self.download_file_name = 'hrrr.t{gmt_plus:02d}z.wrfsfcf00.grib2'

        self.local_directory = web_directory + date.strftime('/%Y/%m/%d/hrrr_obs')

        self.local_secondary_directory = web_directory + date.strftime('/hrrr_obs/%Y/%m/%d')

        self.output_filename_format = 'hrrr_obs.{time}.{vars}.{domain}.wrfsfcf00.grb2'

        self.output_filename_format_heatmap_viz = 'hrrr_obs.{time}.{vars}.{domain}.wrfsfcf00.heatmap.png'


        self.files_to_download = []
        self.converted_files = []
        self.visualization_heatmap_files = []

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

        var_lookup_table = {}
        var_lookup_table['2MTK'] = 54
        var_lookup_table['DPT'] = 57

        super(HRRRObservations, self).__init__(date, vars, domain, download_directory, web_directory)


