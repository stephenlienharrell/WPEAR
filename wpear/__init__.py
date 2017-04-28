#!/usr/bin/env python

from distutils.spawn import find_executable
import sys

import configargparse

import WPEARController

DOWNLOAD_DIRECTORY = 'temp'
WEB_DIRECTORY = 'web'
TESTING = False
CONFIG_FILE = ['wpear.conf']
WGRIB = 'wgrib2'
QUIET = False
EGREP = 'egrep'
CONVERT='convert'
MINLAT = 38.22
MAXLAT = 41.22
MINLON = -87.79
MAXLON = -84.79
VAR = '2MTK'
THREAD_MAX = 4


def main():
    parser = configargparse.ArgParser(default_config_files=CONFIG_FILE,
            config_file_parser_class=configargparse.YAMLConfigFileParser)
    parser.add('-c', '--config', required=False, is_config_file=True, 
            help='Config file path [DEFAULT: ' + CONFIG_FILE[0] + ']')
    parser.add('-w', '--web_dir', required=False, default=WEB_DIRECTORY, 
            help='Root of web directory [DEFAULT: ' + WEB_DIRECTORY + ']')
    parser.add('-d', '--download_dir', required=False, default=DOWNLOAD_DIRECTORY,
            help='Directory for temporary downloads [DEFAULT: ' + DOWNLOAD_DIRECTORY + ']')
    parser.add('-t', '--testing', required=False, action='store_true',
            help='Testing mode (only download a small amount of files) [DEFAULT: ' + str(TESTING) + ']')
    parser.add('-q', '--quiet', action='store_true', help='Silence console output [DEFAULT: ' + str(QUIET) + ']')
    parser.add('-g', '--wgrib', required=False, help='Path for wgrib2 [DEFAULT: ' + str(WGRIB) + ']',
            default=WGRIB)
    parser.add('-e', '--egrep', required=False, default=EGREP,
            help='Path for egrep [DEFAULT: ' + str(EGREP) + ']')
    parser.add('-i', '--imconvert', required=False, default=CONVERT,
            help='Path for imagemagick Convert [DEFAULT: ' + str(CONVERT) + ']')
    parser.add('-r', '--maxlat', type=float, required=False, default=MAXLAT,
            help='Maximum latitude [DEFAULT: ' + str(MAXLAT) + ']')
    parser.add('-a', '--maxlon', type=float, required=False, default=MAXLON,
            help='Maximum longitude [DEFAULT: ' + str(MAXLON) + ']')
    parser.add('-s', '--minlat', type=float, required=False, default=MINLAT,
            help='Minimum latitude [DEFAULT: ' + str(MINLAT) + ']')
    parser.add('-f', '--minlon', type=float, required=False, default=MINLON, 
            help='Minimum longitude [DEFAULT: ' + str(MINLON) + ']')
    # not implemented yet
    #parser.add('-v', '--variable', required=False, default=VAR,
    #        help='Weather variable to use [DEFAULT: ' + str(VAR) + ']')
    parser.add('-p', '--threads', type=int, required=False, default=THREAD_MAX,
            help='Maximum threads to use [DEFAULT: ' + str(THREAD_MAX) + ']')

    options = parser.parse_args()

    if find_executable(options.wgrib) is None:
        print "ERROR: Cannot find wgrib"
        sys.exit(0)

    if find_executable(options.imconvert) is None:
        print "ERROR: Cannot find convert"
        sys.exit(0)

    if find_executable(options.egrep) is None:
        print "ERROR: Cannot find egrep"
        sys.exit(0)

    WPEARController.StartRun(options)

if __name__ == "__main__":
    main()
