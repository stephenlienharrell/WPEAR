# Weather Prediction Evaluation and Reporting (WPEAR) _Pronounced whipper_

The goal of this project is to create a tool that compares weather forecasts with corresponding observations and presents the results of real-time comparisons in an accessible way. Currently, the tool uses the High-Resolution Rapid Refresh ([HRRR](https://rapidrefresh.noaa.gov/hrrr/)) products for forecasts and Real-Time Mesoscale Analysis ([RTMA](http://www.nco.ncep.noaa.gov/pmb/products/rtma/)) products for observations. Upon downloading hourly forecasts/observations, the tool processes them by converting them into a common grid format and performs some useful statistical computations. The outcomes of these computations are represented as static or dynamic visualizations or graphs and updated on a website. The tool is designed to perform real-time comparisons and maintain a website that archives the results of these comparisons.

Link to the website : Under Development

## Instructions for Getting Started

The tool is created in an Ubuntu Linux environment (tested with 14.04/16.04) with [Anaconda 4.3.1](https://www.continuum.io/downloads) (Python 2.7 version). Once you have Anaconda set up, install the given dependencies. This would allow you to start running the tool with the preset configurations.  

1. [wgrib2](http://www.cpc.ncep.noaa.gov/products/wesley/wgrib2/compile_questions.html)
2. [pygrib](https://anaconda.org/conda-forge/pygrib)
3. [basemap](https://anaconda.org/anaconda/basemap)
4. [configargparse](https://pypi.python.org/pypi/ConfigArgParse)
5. [matplotlib](https://matplotlib.org/faq/installing_faq.html#how-to-install)


## Running WPEAR

### Example Command Line
The following command runs WPEAR under testing mode, which only downloads a small amount of files

$ python \_\_init\_\_.py -t

**Note**: Running without -t/--testing flag, WPEAR will download over 400 files at a time. It might take a while to
generate the running result.

Other flags allow you to config your local directory path and wgrib2 path.

### Directory Settings
* -w/--web_dir  - Set root directory where WPEAR stores generated data files
* -d/--download_dir - Set directory where WPEAR temporarily downloads needed data

### Config Wgrib2
* -w/--wgrib - Set path for wgrib2

### Config imagemagick
* -i/--imconvert - Set path for imagemagick

### Config Geo Latitudes and Longitudes (Under Development)
* -r/--maxlat - Set max latitude
* -a/--maxlon - Set max longitude
* -s/--minlat - Set min latitude
* -f/--minlon - Set min longitude

### Other Flags
* -h/--help - Display all the available flag options
* -t/--testing - Set testing mode to be true
* -q/--quiet - Silence console output
* -c/--config - Location of config file
* -e/--egrep - Path for egrep
* -p/--threads - Set maximum threads to use

### Output Directory
By default, WPEAR stores all the generated files including converted grib files, visualization files as well
as all the generated static html files under a directory called ***web*** in the current working directory. Under this directory, WPEAR stores all the converted grib files and visualization files under the day subdirectory in the format of /year/month/day.

Under the day directory, converted grib files and data visualization files are stored in different directory by their data type. Thus, all the data files related to forecast are stored under forecast directory, all the data files related to observation are stored under observation directory. Comparison results between forecast and observation are stored under comparison directory. For example, a generated static forecast visualization file on 2017.04.25 will be stored under 2017/04/25/hrrr_forecast. 

Under ***web***, there are two html files as sidebar.html and index.html. Under each day directory, there're html files as:

* day.html - Display all the generated forecast, observational, comparison visualization for the day
* demo.html - Display 4 chosen data visualization files on landing page for demo

## Main Components of WPEAR

### Task Manager

[WPEARController](https://github.com/stephenlienharrell/WPEAR/blob/master/wpear/WPEARController.py) schedules task for each component during the work flow.

### Task Setup
[HRRRSurfaceForecasts](https://github.com/stephenlienharrell/WPEAR/blob/master/wpear/HRRRSurfaceForecasts.py)defines all the hrrr forecast files to download, to convert and location to store the related files. 

[HRRRSurfaceObservations](https://github.com/stephenlienharrell/WPEAR/blob/master/wpear/HRRRSurfaceObservations.py) defines all the hrrr forecast files to download, to convert and location to store the related files.

[RTMAObservations](https://github.com/stephenlienharrell/WPEAR/blob/master/wpear/RTMAObservations.py) defines all the rtma observation files to download, to convert and location to store the related files.

### Task Handlers
[DataDownloader](https://github.com/stephenlienharrell/WPEAR/blob/master/wpear/DataDownloader.py) downloads grib files WPEARController requests in the set download directory.

[DataConverter](https://github.com/stephenlienharrell/WPEAR/blob/master/wpear/DataConverter.py) converts selected downloaded grib files by WPEARController into smaller size, which contains only data in a specific region.

[DataComparator](https://github.com/stephenlienharrell/WPEAR/blob/master/wpear/DataComparator.py) compares a set of forecast data and observational data given by WPEARController with a specified method.

[DataVisualizer](https://github.com/stephenlienharrell/WPEAR/blob/master/wpear/DataVisualizer.py) visualizes the data given by WPEARController.

[WebsiteGenerator](https://github.com/stephenlienharrell/WPEAR/blob/master/wpear/WebsiteGenerator.py) generates static html files to display generated data results

## Order of Operations in WPEAR

### Download Source Data
WPEARController calls DataDownloader to download the most recent grib data from given source.

### Convert Data
After files are downloaded, WPEARController calls DataConverter to convert the downloaded files into a smaller size grib file by selecting data under a specific region. If the DataConverter has converted this file before, WPEARController will avoid converting same file again and let the converter continue to convert other files.

### Compare Data
After both forecast data and observational data are converted well, WPEARController calls DataComparator to compare the set of data.

### Visualize Data
WPEARController passes compared result data to DataVisualizer to generated wanted data visualization and stores generated files in target place.

### Generate Webs
After all the data analysis and data visualization is done, WPEARController calls WebsiteGenerator to generate all the html files under web directory. 

## FAQs
* Does the tool need to be manually run each time?

The tool contains an intelligent system that determines the files that it needs to download and perform conversions/comparisons/visualizations on. Though it can be manually run, it is designed to be able to run all the time and archive the results on the website.


* Is there a mechanism for the tool to catch-up on previous days if the tool was not run or went down for some reason?

The tool contains an intelligent system that can detect if past downloads/conversions have failed or are missing and perform them.


* What types of comparisons can be performed?

The tool, currently, can perform 3 types of comparisons:
** Difference between a forecast and an observation
** Standard deviation and means of different forecasts against a corresponding observation
** Multi-set average for an observation given a specific geographical location


* What types of visualizations/graphs can be generated?

Here's a list of visualizations:
** Static heatmap of a forecast
** Static heatmap of an observation
** Dynamic heatmap of different forecasts of an observation (.gif)
** Static heatmap of the difference between a forecast and an observation
** Dynamic heatmap of the difference between a 1-hour forecast and its observation for multiple hours (.gif)
** Mean and Standard deviation of forecasts against the corresponding observation 


* When performing the test run, my computer is unresponsive or it is taking too long?

The test run downloads forecasts for 1 hour on 2 days (current day and day before current day). For each hour, it downloads 18 forecasts and 1 observation. Since these files are large (~115 MB each), it can take some time. However, once the conversions are performed, the converted files are much smaller and the downloaded files are deleted. In future runs, the archives are checked before any files are downloaded. The computer can get unresponsive because the conversions have been optimized to use multiple processes (upto 20) to speed up each run of the tool.



## Possible next steps
* Using more or different data sets that could be used to compare between forecasts for example
* Performing other forms of comparisons
* Creating 3-D visualizations
* Allowing on-demand comparisons/visualizations to be performed on the website
