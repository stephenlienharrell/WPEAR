import datetime
import errno
import multiprocessing
import os
import shutil
import time

import pygrib

import DataDownloader
import DataComparator
import DataConverter
import DataVisualizer

THREAD_MAX=20

class WeatherData(object):


    def __init__(self, date, vars, domain, download_directory, web_directory):
        self.date = date
        self.vars = vars
        self.domain = domain
        self.web_directory = web_directory
        
        self.temp_directory =  download_directory + '/' + self.tag + '/' + date.strftime('%Y%m%d') 
        self.compared_viz_file_format = '{obs_tag}.{obs_date}.{obs_extra_info}_{fcast_tag}.{fcast_date}.{fcast_extra_info}f{fcast_number}_{var}.{domain}.{comp_tag}.png'
        self.compared_viz_directory = web_directory + '/%Y/%m/%d/{obs_tag}.{fcast_tag}.{comp_tag}'

        self.threads = []
        self.thread_count = 0

    def DownloadData(self):
        needed_vars = ['url', 'url_directory', 'files_to_download', 'converted_files']
        self._CheckVars('DownloadData', needed_vars)

        print "Starting data downloads"

        if not os.path.exists(self.temp_directory):
            os.makedirs(self.temp_directory)


       
        for index, file_name in enumerate(self.files_to_download):
            converted_file = self.converted_files[index]
            if os.path.exists(converted_file):
                continue

            file_directory = self.url_directory + file_name

            self._addToThreadPool(_doDownload, (self.url, file_directory, self.temp_directory))
            self._waitForThreadPool()


        self._waitForThreadPool(thread_max=0)

    def ConvertData(self):
        needed_vars = ['files_to_download', 'local_directory', 'converted_files']
        self._CheckVars('ConvertData', needed_vars)

        print "Starting data conversion"

        if not os.path.exists(self.local_directory):
            os.makedirs(self.local_directory)

        converted_files = []
        for index, file_name in enumerate(self.files_to_download):
            temp_file = self.temp_directory + '/' + file_name
            if not os.path.exists(temp_file):
                continue
            converted_file = self.converted_files[index]
            if os.path.exists(converted_file):
                continue
            self._addToThreadPool(_doConversion, (temp_file, converted_file))
            self._waitForThreadPool()

        self._waitForThreadPool(thread_max=0)
            
    def VisualizeData(self):
        needed_vars = ['vars', 'visualization_heatmap_files', 'converted_files']
        self._CheckVars('VisualizeData', needed_vars)
        print "Starting data visualization"
        for index, file_name in enumerate(self.converted_files):
            if not os.path.exists(file_name):
                continue

            out_file = self.visualization_heatmap_files[index]
            if os.path.exists(out_file):
                continue

            self._addToThreadPool(_doVisualization, (file_name, out_file))
            self._waitForThreadPool()

        self._waitForThreadPool(thread_max=0)


    def VisualizeDifference(self, forecast, comparator_tag):
        print "Starting Data Comparison"
        needed_vars = ['vars', 'converted_files', 'compared_viz_directory', 'tag', 'web_directory', 
                'compared_viz_file_format', 'date_format', 'domain', 'extra_info']
        self._CheckVars('VisualizeDifference', needed_vars)
        fcast_needed_vars = ['tag', 'max_fcast', 'vars', 'domain', 'output_filename_format', 'extra_info']
        forecast._CheckVars('VisualizeDifference', fcast_needed_vars)
        if not self.obs:
            raise ValueError('Must call VisualDifference on observations only')
        for obs_file in self.converted_files:
            obs_date = self._GetTimeOfObs(obs_file)

            out_dir = obs_date.strftime(self.compared_viz_directory)
            out_dir = out_dir.format(obs_tag=self.tag, fcast_tag=forecast.tag, comp_tag=comparator_tag)
            if not os.path.exists(out_dir):
                os.makedirs(out_dir)

            if not os.path.exists(obs_file):
                continue

            for x in range(1, forecast.max_fcast + 1, forecast.hours_between_fcasts):
                fcast_date = obs_date - datetime.timedelta(hours=x)

                gmt_plus = 't{gmt_plus:02d}z'.format(gmt_plus=fcast_date.hour)
                fcast_file =  (self.web_directory + fcast_date.strftime(forecast.local_directory_date_format) + 
                        '/' + forecast.output_filename_format.format(
                        time=fcast_date.strftime('%Y%m%d') + '_' + gmt_plus, vars='_'.join(forecast.vars),
                        domain=forecast.domain, forecast_number=x, extra_info=forecast.extra_info))

                if not os.path.exists(fcast_file):
                    continue

                ## TODO FIX VAR EVERYWHERE INCLUDING HERE
                out_file = out_dir + '/' + self.compared_viz_file_format.format(
                        obs_tag=self.tag, obs_date=obs_date.strftime(self.date_format) + obs_date.strftime('_t%Hz'), 
                        obs_extra_info=self.extra_info, fcast_tag=forecast.tag, 
                        fcast_date=fcast_date.strftime(self.date_format) + fcast_date.strftime('_t%Hz'),
                        fcast_number=x, fcast_extra_info=forecast.extra_info, var='2MTK', domain=self.domain,
                        comp_tag=comparator_tag)


                if os.path.exists(out_file):
                    continue

                self._addToThreadPool(_doCompareVisualization, (obs_file, fcast_file, out_file))
                self._waitForThreadPool()

        self._waitForThreadPool(thread_max=0)


    def CleanupDownloads(self):
        #TODO:  need to cleanup date based parent directories
        shutil.rmtree(self.temp_directory)

    def _CheckVars(self, function, vars):
        for var in vars:
            if not hasattr(self, var):
                raise AttributeError('Variable self.%s not found and is needed in the %s function' % 
                        (var, function))


    def _addToThreadPool(self, function, args):
        proc = multiprocessing.Process(target=function, args=args)
        proc.start()
        self.threads.append(proc)
        self.thread_count += 1

    def _waitForThreadPool(self, thread_max=THREAD_MAX - 1):
        count = 0
        while len(self.threads) > thread_max:
            time.sleep(.1)
            if count > len(self.threads) - 1:
                count = 0
            if self.threads[count].exitcode is not None:
                self.threads[count].join(1)
                self.threads.pop(count)
            else: 
                count += 1


def _doDownload(url, file_directory, temp_directory):
    try:
        downloader = DataDownloader.DataDownloader()
        downloader.download(url, file_directory, temp_directory)
    except IOError, e:
        try:
            if e[1] != 404:
                raise
        except:
            raise
        return
    print "Download completed for %s" % file_directory


def _doConversion(temp_file, converted_file):
    DataConverter.convert(temp_file, converted_file)
    print "Conversion completed for " + temp_file

def _doVisualization(file_name, out_file):
    visualizer = DataVisualizer.DataVisualizer(None)
    grib_loaded = pygrib.open(file_name)
    #for var in self.vars:
    grib_msg = grib_loaded.select(name='2 metre temperature')[0]
    visualizer.Heatmap(grib_msg, out_file)
    print "Visualizing " + out_file + " is complete"

def _doCompareVisualization(obs_file, fcast_file, out_file):
    visualizer = DataVisualizer.DataVisualizer(None)
    grib_msg = DataComparator.DataComparator(obs_file, fcast_file)
    visualizer.Heatmap(grib_msg, out_file)
    print "Visualizing " + out_file + " is complete"

