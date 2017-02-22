#! /usr/bin/env python

import pygrib, os
import numpy as np

outputFolderPath = 'convertedFiles/'

def convert(outputFilePath):
	gfile = pygrib.open('sourceFileDownloads/hrrr.t02z.wrfsfcf01.grib2')
	gobj = gfile.select(name='2 metre temperature')[0]
	lats = gobj.latlons()[0]
	lons = gobj.latlons()[1]

	# extract the required region = Indiana
	reqdata, reqlats, reqlons = gobj.data(lat1=38.22,lat2=41.22,lon1=-87.79,lon2=-84.79)
	# print reqdata.shape, lats.min(), lats.max(), lons.min(), lons.max()

	# initialize new data array with extracted data
	newdata = np.zeros(gobj.values.shape, dtype=np.float32)
	totalsize = len(lats)*len(lats[0])
	rowsize = len(lats[0])
	reqdatacount = 0
	for i in range(totalsize):
		r = i / rowsize
		c = i % rowsize
		if lats[r][c] == reqlats[reqdatacount] and lons[r][c] == reqlons[reqdatacount]:
			newdata[r][c] = reqdata[reqdatacount]
			reqdatacount = reqdatacount + 1
			# print '(r,c) = (' + str(r) + ',' + str(c) + '), reqdatacount = ' + str(reqdatacount)
		if reqdatacount >= len(reqdata):
			break

	# set data array with new data array
	# ISSUE : rounds off to 1 d.p. <<<<<<<<<<<<<<<<
	gobj.values = newdata

	# save message object in file
	msg = gobj.tostring()
	gfile.close()
	fullFilePath = outputFolderPath + outputFilePath
	if not os.path.exists(outputFolderPath):
			os.makedirs(outputFolderPath)
	grbout = open(fullFilePath,'wb')
	grbout.write(msg)
	grbout.close()

	# return file name
	return fullFilePath



print convert('out1.grib2')