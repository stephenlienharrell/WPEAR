#!/usr/bin/env python

import configargparse

import WPEARController

DOWNLOAD_DIRECTORY = 'temp'
WEB_DIRECTORY = 'web'
TESTING = False
CONFIG_FILE = ['wpear.conf']
WGRIB = './wgrib2'
QUIET = False
EGREP = 'egrep'



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
    parser.add('-g', '--wgrib', required=False, help='Path for wgrib2 [DEFAULT: ' + str(WGRIB) + ']')
    parser.add('-e', '--egrep', required=False, help='Path for egrep [DEFAULT: ' + str(EGREP) + ']')

    options = parser.parse_args()

    WPEARController.StartRun(options)

if __name__ == "__main__":
    main()
