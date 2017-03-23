#! /usr/bin/env python

import shlex,os,subprocess

class DataConverter:

	FNULL=open(os.devnull, 'w')

	def extractMessages(self, inputfilepath, varlist, outputfilepath):


		cmd1 = './wgrib2 {} -s'.format(inputfilepath)
		print 'cmd1 = {}'.format(cmd1)
		pipe1 = subprocess.Popen(shlex.split(cmd1), stdout=subprocess.PIPE)
		greplist = ['grep']
		for var in varlist:
			greplist.append('-e')
			greplist.append(var)

		pipe2 = subprocess.Popen(greplist, stdin=pipe1.stdout, stdout=subprocess.PIPE)
		outputfilepath = inputfilepath.split('/')[0] + '/em_' + inputfilepath.split('/')[-1]

		cmd3 = './wgrib2 -i {} -grib {}'.format(inputfilepath, outputfilepath)
		pipe3 = subprocess.Popen(shlex.split(cmd3), stdin=pipe2.stdout, stdout=self.FNULL)



	def subsetRegion(self, inputfilepath, minlat, maxlat, minlon, maxlon, outputfilepath):
		cmd = './wgrib2 {} -small_grib {}:{} {}:{} {} -set_grib_type same'.format(inputfilepath, minlon, maxlon, minlat, maxlat, outputfilepath)
		try:
			subprocess.check_call(shlex.split(cmd), stdout=self.FNULL)
		except subprocess.CalledProcessError as e:
			print e.cmd
			print e.returncode
			print e.output




###############################################################################################
########################################### Test ##############################################
###############################################################################################
# dc = DataConverter()


###############################################################################################
######################################### extractMessages #####################################
###############################################################################################
# dc.extractMessages('sourceFileDownloads/rtma2p5.t00z.2dvaranl_ndfd.grb2', [':DPT:2 m above ground', ':TMP:2 m above ground'], 'sourceFileDownloads/em_rtma2p5.t00z.2dvaranl_ndfd.grb2')
# dc.extractMessages('sourceFileDownloads/hrrr.t00z.wrfsfcf18.grib2', [':TMP:500 mb', ':WIND:10 m above ground'], 'sourceFileDownloads/em_hrrr.t00z.wrfsfcf18.grib2')


###############################################################################################
######################################### subsetRegion ########################################
###############################################################################################
# dc.subsetRegion('sourceFileDownloads/em_rtma2p5.t00z.2dvaranl_ndfd.grb2', 38.22, 41.22, -87.79, -84.79, 'sourceFileDownloads/sem_rtma2p5.t00z.2dvaranl_ndfd.grb2')
# dc.subsetRegion('sourceFileDownloads/em_hrrr.t00z.wrfsfcf18.grib2', 38.22, 41.22, -87.79, -84.79, 'sourceFileDownloads/sem_hrrr.t00z.wrfsfcf18.grib2')











