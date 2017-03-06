#! /usr/bin/env python

import urllib, os, urlparse, requests
from bs4 import BeautifulSoup

# only works for HTTP links (no FTP links)

class DataDownloader():
	'Class to download forecast/observation files'

	ext = ('grib2.gz', 'grib2')

	def download(self, url, filedir, defaultdownloaddir='/sourceFileDownloads'):
		downloadDirectory = defaultdownloaddir
		if not os.path.exists(downloadDirectory):
			os.makedirs(downloadDirectory)

		fullURL = urlparse.urljoin(url, filedir)
		file = urllib.URLopener()

		fileDownloadPath = downloadDirectory + '/' + fullURL.split('/')[-1]
		file.retrieve(fullURL, fileDownloadPath)
		return fileDownloadPath


	def listDirectory(self, url):
		page = requests.get(url).text
		soup = BeautifulSoup(page, 'html.parser')
		return [url  + node.get('href') for node in soup.find_all('a') if node.get('href').endswith(self.ext)]

	
	def changeExtentions(self, newExt):
		self.ext = newExt
		print self.ext	




# test inputs
# dd = DataDownloader()
# ==== test download ====
# print dd.download('http://mrms.ncep.noaa.gov/data', 'data/3DReflPlus/MergedReflectivityQC_00.50/MRMS_MergedReflectivityQC_00.50_20170214-180435.grib2.gz')
# print dd.download('http://www.ftp.ncep.noaa.gov/data', 'data/nccf/com/hrrr/prod/hrrr.20170215/hrrr.t05z.wrfsfcf16.grib2.idx')
# ==== test listDirectory =====
# print dd.listDirectory('http://www.ftp.ncep.noaa.gov/data/nccf/com/hrrr/prod/hrrr.20170215/')
# print dd.listDirectory('http://mrms.ncep.noaa.gov/data/3DReflPlus/MergedReflectivityQC_00.50/')

