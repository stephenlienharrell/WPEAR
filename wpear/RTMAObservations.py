import WeatherData


class RTMAObservations(WeatherData.WeatherData):
   
    def __init__(self, date):

        self.tag = 'rtma_obs'
        self.url = 'http://www.ftp.ncep.noaa.gov'
        self.url_directory = date.strftime('/data/nccf/com/rtma/prod/rtma2p5.%Y%m%d/')
        # use self.url_directory.format(date=somedatetime.strftime(self.file_date_format)

        self.download_file_name = 'rtma2p5.t{gmt_plus:02d}z.2dvaranl_ndfd.grb2'
        # use self.file_name.format(gmt_plus='number_of_hours_after gmt')

        self.local_directory = date.strftime('web/%Y/%m/%d/rtma_obs/')
        # use strftime on datetime here
        self.local_secondary_directory = date.strftime('web/rtma_obs/%Y/%m/%d/')

        self.output_filename_format = 'rtma_obs_{time}_{vars}_{domain}_2dvaranl_ndfd.grb2'
        # time here should be in the gmt time zone and be the actual time of gmt_plus with date in the format %Y%m%d-%H

        self.files_per_day = 'rtma_obs_{time}_{vars}_{domain}_2dvaranl_ndfd.grb2'
        # some how we need to enumerate all the times??

        self.files_to_download = []
        for x in range(0,23):
            self.files_to_download.append(self.download_file_name.format(gmt_plus=x))

        var_lookup_table = {}
        var_lookup_table['2MTK'] = 3
        var_lookup_table['DPT'] = 4

        super(RTMAObservations, self).__init__(date)


