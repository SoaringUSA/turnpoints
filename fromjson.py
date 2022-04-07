#!/usr/bin/env python3

import csv
import json
import sys

def cupWriter(fileHandle):
	cvw = csv.DictWriter(fileHandle, fieldnames=['name','code','country','lat','lon','elev','style','rwdir','rwlen','freq','desc','userdata','pics'], quoting=csv.QUOTE_NONE)
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
	cvr = json.load(sys.stdin)

	cvw = cupWriter(sys.stdout)
	cvw.writeheader()

	for (name, tp) in cvr.items():
		if not tp['lat']:
			continue

		outDict = {
			'name' : name,
			'code' : optionally(tp['code']),
			'country' : optionally(tp['country']),
			'lat' : parseLat(tp['lat']),
			'lon' : parseLon(tp['lon']),
			'elev' : parseElev(tp['elev']),
			'style' : str(tp['style']),
			'rwdir' : optionally(tp['rwdir']),
			'rwlen' : '{0:.1f}m'.format(tp['rwlen']) if tp['rwlen'] else '',
			'freq' : optionally(tp['freq']),
			'desc' : optionally(tp['desc']),
			'userdata' : '',
			'pics' : '',
		}
		cvw.writerow(outDict)
