#!/usr/bin/env python3

import csv
import json
import sys

def cupWriter(fileHandle):
	cvw = csv.DictWriter(fileHandle, fieldnames=['name','code','country','lat','lon','elev','style','rwdir','rwlen','freq','desc','userdata','pics'], quoting=csv.QUOTE_MINIMAL)
	return cvw

def parseLat(deg):
	hemi = 'N' if deg >= 0.0 else 'S'
	deg = abs(deg)
	minutes = 60.0 * (deg - int(deg))
	return '{0:02d}{1:06.3f}{2}'.format(int(deg), minutes, hemi)

def parseLon(deg):
	hemi = 'E' if deg >= 0.0 else 'W'
	deg = abs(deg)
	minutes = 60.0 * (deg - int(deg))
	return '{0:02d}{1:06.3f}{2}'.format(int(deg), minutes, hemi)

def parseElev(meters):
	return '{0:.1f}m'.format(meters) if meters else ''

def optionally(val):
	return str(val) if val else ''

if __name__=='__main__':
	input = json.load(sys.stdin)

	cvw = cupWriter(sys.stdout)
	cvw.writeheader()

	for tp in input['turnpoints']:
		outDict = {
			'name' : tp['name'],
			'lat' : parseLat(tp['lat']),
			'lon' : parseLon(tp['lon']),
			'elev' : parseElev(tp['elev']),
		}
		if 'desc' in tp:
			outDict['desc'] = tp['desc']
		if 'code' in tp:
			outDict['code'] = tp['code']
		style = 1
		if 'landable' in tp:
			style = 3
			if 'freq' in tp['landable']:
				outDict['freq'] = tp['landable']['freq']
			if 'runways' in tp['landable']:
				style = 2
				rw0 = tp['landable']['runways'][0]
				if 'surface' in rw0 and rw0['surface'] == 'paved':
					style = 5
				if 'dir' in rw0:
					outDict['rwdir'] = str(rw0['dir'])
				if 'len' in rw0:
					outDict['rwlen'] = '{0:.1f}m'.format(rw0['len'])
		outDict['style'] = str(style)
		cvw.writerow(outDict)
