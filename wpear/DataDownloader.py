#! /usr/bin/python

import sys

from ftplib import FTP

		

class DataDownloader():
	'Class to download forecast/observation files'

	ftpServerForForecasts = 'ftp.ncep.noaa.gov'
	defaultFTPDirectoryForForecasts = '/pub/data/nccf/com/hrrr/prod'



	def __init__(self, server, directory):
		if server is not None:
			self.ftpServerForForecasts = server
		
		if directory is not None:
			self.defaultFTPDirectoryForForecasts = directory
		
		try:
			self.ftp = FTP(self.ftpServerForForecasts)
			self.ftp.login()
		except:
			sys.exit('Error connecting to FTP server')
			
		try:
			self.ftp.cwd(self.defaultFTPDirectoryForForecasts)
		except:
			sys.exit('Error changing directory')



	# Issue: Which file to download?	
	def retrieveLatestFile(self):
		self.ftp.cwd(self.ftp.nlst('-t')[0]) # dates
		filename = self.ftp.nlst('-t')[0] # no idea what these files represent
		
		print('downloading file : ' + filename)

		with open('%s' % filename, mode='wb') as target:
			self.ftp.retrbinary('RETR %s' % filename, target.write)



	def __del__(self):
		if hasattr(self, 'ftp'):
			self.ftp.quit()	



d = DataDownloader(None, None)
d.retrieveLatestFile()	