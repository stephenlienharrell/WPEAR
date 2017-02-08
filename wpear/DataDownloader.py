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

		print('Downloading file : ' + filename)
		self.filesize = float(self.ftp.size(filename)) 
		self.fileDownloadPercent = 0.0
		self.lastShownPercent = 0.0

		with open('%s' % filename, mode='wb') as target:
			self.currsize = 0

			def callback(chunk):
				
				if self.currsize == 0:
					print 'Downloading...0.0%...',
				
				chunksize = float(len(chunk))
				target.write(chunk)
				
				self.currsize += float(chunksize)
				self.fileDownloadPercent = round(float(self.currsize/self.filesize) * 100)
				
				if self.fileDownloadPercent % 5 == 0 and self.fileDownloadPercent > self.lastShownPercent:
					print str(self.fileDownloadPercent) + '%...',
					# debug print sizes
					# print('[' + str(self.currsize) + '/' + str(self.filesize) + ']')
					self.lastShownPercent = self.fileDownloadPercent

			self.ftp.retrbinary('RETR %s' % filename, callback, 32768)



	def __del__(self):
		if hasattr(self, 'ftp'):
			self.ftp.quit()	


# debug run
# d = DataDownloader(None, None)
# d.retrieveLatestFile()	
