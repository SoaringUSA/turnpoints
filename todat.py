#!/usr/bin/env python3

import csv
import json
import re
import sys

def datWriter(fileHandle):
	cvw = csv.DictWriter(fileHandle, fieldnames=['index', 'lat', 'lon', 'elev', 'attr', 'name', 'comment'], quoting=csv.QUOTE_MINIMAL)
	return cvw

def parseLat(deg):
	hemi = 'N' if deg >= 0.0 else 'S'
	deg = abs(deg)
	minutes = 60.0 * (deg - int(deg))
	return '{0:02d}:{1:06.3f}{2}'.format(int(deg), minutes, hemi)

def parseLon(deg):
	hemi = 'E' if deg >= 0.0 else 'W'
	deg = abs(deg)
	minutes = 60.0 * (deg - int(deg))
	return '{0:02d}:{1:06.3f}{2}'.format(int(deg), minutes, hemi)

def parseElev(meters):
	return '{0:.1f}M'.format(meters) if meters else ''

if __name__=='__main__':
	input = json.load(sys.stdin)

	cvw = datWriter(sys.stdout)

	index = 0
	for tp in input['turnpoints']:
		index += 1
		outDict = {
			'index' : index,
			'name' : tp['name'],
			'lat' : parseLat(tp['lat']),
			'lon' : parseLon(tp['lon']),
			'elev' : parseElev(tp['elev']),
		}
		if 'desc' in tp:
			outDict['comment'] = tp['desc']
		attr = 'T'
		if 'landable' in tp:
			attr = 'L'
			if 'runways' in tp['landable']:
				style = 'A'
		outDict['attr'] = attr
		cvw.writerow(outDict)
