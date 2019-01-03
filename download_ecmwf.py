# -*- coding: utf-8 -*-
# #!/usr/bin/env python

import os
import sys
import linecache
import datetime

from ecmwfapi import ECMWFDataServer

params = {}
params['WindU'] = '165.128'    # 10 metre U wind component
params['WindV'] = '166.128'    # 10 metre V wind component
# params['Rain'] = ''
params['Cloud'] = '164.128'     # total cloud cover
params['airtemp'] = '167.128'    # 2 metre temperature
params['Gust'] = '49.128'    # 10 metre wind gust since previous post-processing
# params['CAPE'] = ''    #
params['Wave'] = '230.140'    # Mean wave direction

steps = {}

steps['WindU'] = '0'    # 10 metre U wind component
steps['WindV'] = '0'    # 10 metre V wind component
# params['Rain'] = ''
steps['Cloud'] = '0'     # total cloud cover
steps['airtemp'] = '0'    # 2 metre temperature
steps['Gust'] = '3'    # 10 metre wind gust since previous post-processing
# params['CAPE'] = ''    #
steps['Wave'] = '0'    # Mean wave direction

types = {}

types['WindU'] = 'an'    # 10 metre U wind component
types['WindV'] = 'an'    # 10 metre V wind component
# params['Rain'] = ''
types['Cloud'] = 'an'     # total cloud cover
types['airtemp'] = 'an'    # 2 metre temperature
types['Gust'] = 'fc'    # 10 metre wind gust since previous post-processing
# params['CAPE'] = ''    #
types['Wave'] = 'an'    # Mean wave direction

streams = {}

streams['WindU'] = 'oper'    # 10 metre U wind component
streams['WindV'] = 'oper'    # 10 metre V wind component
# params['Rain'] = ''
streams['Cloud'] = 'oper'     # total cloud cover
streams['airtemp'] = 'oper'    # 2 metre temperature
streams['Gust'] = 'oper'    # 10 metre wind gust since previous post-processing
# params['CAPE'] = ''    #
streams['Wave'] = 'wave'    # Mean wave direction

def main(outfolder):
    server = ECMWFDataServer()
    a = linecache.getlines('./month.txt')
    cur = datetime.datetime.now()

    for k, v in params.items():
        for i in range(2010, cur.year):
            if i % 4 == 0:
                m = 29
            else:
                m = 28
            for j in range(1, 13):
                if j == 2:
                    b = m
                else:
                    b = a[j - 1]
                if j < 10:
                    y = '0'+ str(j)
                else:
                    y = str(j)
                date = str(i) + '-' + y + '-01/to/' + str(i) + '-' + y + '-' + str(b)
                # print(date)
                # from ecmwfapi import ECMWFDataServer
                # server = ECMWFDataServer()
                filename = str(i) + y + '01' + k + '.nc'
                path = os.path.join(outfolder, k)
                if not os.path.exists(path):
                    os.makedirs(path)
                fullpath = os.path.join(path, filename)
                if not os.path.exists(fullpath):
                    print('=====================================')
                    print('start download {0}'.format(filename))
                    server.retrieve({
                        'class': 'ei',
                        'dataset': 'interim',
                        'date': date,     # '2018-02-01/to/2018-02-28',
                        'expver': '1',
                        'grid': '0.75/0.75',
                        'levtype': 'sfc',
                        'param': v,  # '167.128',
                        'step': steps[k],  # '0',
                        'stream': streams[k], # 'oper',
                        'time': '00:00:00',
                        'type': types[k], # 'an',
                        'format': 'netcdf',
                        'target': fullpath
                    })
                    print('{0} file download success!'.format(filename))
                    print('======================================')

if __name__ == '__main__':
    outfolder = '/data/sentinel_data/ECMWF_data/data'
    main(outfolder)
