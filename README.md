# Weather Prediction Evaluation and Reporting (WPEAR) _Pronounced whipper_

The goal of this project is to create a tool that compares weather forecasts with corresponding observations and presents the results of real-time comparisons in an accessible way. Currently, the tool uses the High-Resolution Rapid Refresh ([HRRR](https://rapidrefresh.noaa.gov/hrrr/)) products for forecasts and Real-Time Mesoscale Analysis ([RTMA](http://www.nco.ncep.noaa.gov/pmb/products/rtma/)) products for observations. Upon downloading hourly forecasts/observations, the tool processes them by converting them into a common grid format and performs some useful statistical computations. The outcomes of these computations are represented as visualizations or graphs and updated on a website. The tool is designed to perform real-time comparisons and maintain a website that archives the results of these comparisons.

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

### Other Flags
* -h/--help - Display all the available flag options
* -t/--testing - Set testing mode to be true
* -q/--quiet - Silence console output
* -c/--config - Location of config file
* -e/--egrep - Path for egrep

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

## Trouble Shooting 
Troubleshooting tips and possible next steps
