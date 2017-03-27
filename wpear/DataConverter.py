#! /usr/bin/env python

import os
import shlex
import shutil
import subprocess
import sys

WGRIB_PATH='./wgrib'
EGREP_PATH='egrep'
GREP_PATH='grep'

NCEP_GRID_TYPE=3
# http://www.nco.ncep.noaa.gov/pmb/docs/on388/tableb.html

class DataConverter:

    FNULL=open(os.devnull, 'w')

    def __init__(self, wgrib_path=WGRIB_PATH, egrep_path=EGREP_PATH, grep_path=GREP_PATH, ncep_grid_type=NCEP_GRID_TYPE):
        self.wgrib_path = wgrib_path
        self.egrep_path = egrep_path
        self.grep_path = grep_path
        self.grid_type = ncep_grid_type

    def interploateGrid(self, inputfilepath, outputfilepath):
        # This isn't working. to fix maybe http://www.ftp.cpc.ncep.noaa.gov/wd51we/wgrib2/tricks.wgrib2 #21
        cmd1 = '{} {} -new_grid ncep grid {} {}'.format(self.wgrib_path, inputfilepath, self.grid_type, outputfilepath)
        ps = subprocess.check_output(shlex.split(cmd1), stderr=subprocess.STDOUT)

    def extractMessages(self, inputfilepath, varlist, outputfilepath):

        cmd1 = '{} {} -s'.format(self.wgrib_path, inputfilepath)
        try:    
            ps = subprocess.check_output(shlex.split(cmd1), stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            # check if the e.output starts with :*** FATAL ERROR: Statistical processing bad n=0 ***
            # http://www.ftp.cpc.ncep.noaa.gov/wd51we/wgrib2/tricks.wgrib2
            # this may happen several times. in future, handle as many times as no of error messages
            text = os.linesep.join([s for s in e.output.splitlines() if s])
            print text
            if text.startswith('*** FATAL ERROR: Statistical processing bad n=0 ***') :
                lastline = text.splitlines()[-1]
                errmsgno = int(str(lastline.split(':')[0]).strip())
                # creating new file without error msg
                newinputfilepath = os.path.splitext(inputfilepath)[0] + 'fixstat' + os.path.splitext(inputfilepath)[1]
                newfilecmd1 = '{} {} -pdt'.format(self.wgrib_path, inputfilepath)
                newfilecmd2 = '{} -v ^{}:'.format(self.egrep_path, errmsgno)
                newfilecmd3 = '{} -i {} -grib {}'.format(self.wgrib_path, inputfilepath, newinputfilepath)    
                p1 = subprocess.Popen(shlex.split(newfilecmd1), stdout=subprocess.PIPE)
                p2 = subprocess.Popen(shlex.split(newfilecmd2), stdin=p1.stdout, stdout=subprocess.PIPE)
                p3 = subprocess.Popen(shlex.split(newfilecmd3), stdin=p2.stdout, stdout=self.FNULL)
                p3.wait()
                inputfilepath = newinputfilepath
                cmd1 = '{} {} -s'.format(self.wgrib_path, newinputfilepath)
            else:
                print 'extract1message failed for file = {}\n'.format(inputfilepath)

        pipe1 = subprocess.Popen(shlex.split(cmd1), stdout=subprocess.PIPE)
        greplist = [self.grep_path]
        for var in varlist:
            print var
            greplist.append('-e')
            greplist.append(var)

        pipe2 = subprocess.Popen(greplist, stdin=pipe1.stdout, stdout=subprocess.PIPE)
        cmd3 = '{} -i {} -grib {}'.format(self.wgrib_path, inputfilepath, outputfilepath)
        pipe3 = subprocess.Popen(shlex.split(cmd3), stdin=pipe2.stdout, stdout=self.FNULL)
        pipe3.wait()

    def subsetRegion(self, inputfilepath, minlat, maxlat, minlon, maxlon, outputfilepath):
        cmd = '{} {} -small_grib {}:{} {}:{} {} -set_grib_type same'.format(self.wgrib_path, inputfilepath, minlon, maxlon, minlat, maxlat, outputfilepath)
        try:
            subprocess.check_call(shlex.split(cmd), stdout=self.FNULL)
        except subprocess.CalledProcessError as e:
            print e.cmd
            print e.returncode
            print e.output


    def extractMessagesAndSubsetRegion(self, inputfilepath, varlist, tempfiledir, minlat, maxlat, minlon, maxlon, outputfilepath):

        if not os.path.exists(tempfiledir):
            os.makedirs(tempfiledir)

        if tempfiledir.endswith('/'):
            tempfilepath = tempfiledir + inputfilepath.split('/')[-1]
            tempfilepath2 = tempfiledir + inputfilepath.split('/')[-1] + 'temp2'
        else:
            tempfilepath = tempfiledir + '/' + inputfilepath.split('/')[-1]
            tempfilepath2 = tempfiledir + '/' + inputfilepath.split('/')[-1] + 'temp2'


#        self.interploateGrid(inputfilepath, tempfilepath2)
        self.subsetRegion(inputfilepath, minlat, maxlat, minlon, maxlon, tempfilepath)
        self.extractMessages(tempfilepath, varlist, outputfilepath)
        os.remove(tempfilepath)
#        os.remove(tempfilepath2)



###############################################################################################
########################################### Test ##############################################
###############################################################################################
# dc = DataConverter()


###############################################################################################
######################################### extractMessages #####################################
###############################################################################################
# dc.extractMessages('sourceFileDownloads/rtma2p5.t00z.2dvaranl_ndfd.grb2', [':DPT:2 m above ground', ':TMP:2 m above ground'], 'sourceFileDownloads/em_rtma2p5.t00z.2dvaranl_ndfd.grb2')
# dc.extractMessages('sourceFileDownloads/hrrr.t00z.wrfsfcf18.grib2', [':TMP:500 mb', ':WIND:10 m above ground'], 'sourceFileDownloads/em_hrrr.t00z.wrfsfcf18.grib2')
# dc.extractMessages('sourceFileDownloads/hrrr.t00z.wrfsfcf00.grib2', [':TMP:500 mb', ':WIND:10 m above ground'], 'sourceFileDownloads/em_hrrr.t00z.wrfsfcf00.grib2')


###############################################################################################
######################################### subsetRegion ########################################
###############################################################################################
# dc.subsetRegion('sourceFileDownloads/em_rtma2p5.t00z.2dvaranl_ndfd.grb2', 38.22, 41.22, -87.79, -84.79, 'sourceFileDownloads/sem_rtma2p5.t00z.2dvaranl_ndfd.grb2')
# dc.subsetRegion('sourceFileDownloads/em_hrrr.t00z.wrfsfcf18.grib2', 38.22, 41.22, -87.79, -84.79, 'sourceFileDownloads/sem_hrrr.t00z.wrfsfcf18.grib2')
# dc.subsetRegion('sourceFileDownloads/em_hrrr.t00z.wrfsfcf00.grib2', 38.22, 41.22, -87.79, -84.79, 'sourceFileDownloads/sem_hrrr.t00z.wrfsfcf00.grib2')


###############################################################################################
############################### extractMessagesAndSubsetRegion ################################
###############################################################################################
# dc.extractMessagesAndSubsetRegion('sourceFileDownloads/rtma2p5.t00z.2dvaranl_ndfd.grb2', [':DPT:2 m above ground', ':TMP:2 m above ground'], 'temp/', 38.22, 41.22, -87.79, -84.79, 'sourceFileDownloads/sem_rtma2p5.t00z.2dvaranl_ndfd.grb2')
# dc.extractMessagesAndSubsetRegion('sourceFileDownloads/hrrr.t00z.wrfsfcf00.grib2', [':TMP:500 mb', ':WIND:10 m above ground'], 'temp', 38.22, 41.22, -87.79, -84.79, 'sourceFileDownloads/sem_hrrr.t00z.wrfsfcf00.grib2')

