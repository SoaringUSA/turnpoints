#!/usr/bin/env python3

import csv
import json
import re
import sys

def parseLat(latStr):
	# 3653.583N,12115.800W
	match = re.match('(\d*)(\d\d[.]\d*)([NS])', latStr)
	deg = float(match.group(1)) + float(match.group(2)) / 60.0
	if match.group(3) == 'S':
		deg = -deg
	return deg

def parseLon(lonStr):
	match = re.match('(\d*)(\d\d[.]\d*)([EW])', lonStr)
	deg = float(match.group(1)) + float(match.group(2)) / 60.0
	if match.group(3) == 'W':
		deg = -deg
	return deg

def parseLength(elevStr):
	if not elevStr:
		return None
	match = re.match('(\d*[.]?\d*)(m|ft)', elevStr)
	if match.group(2) == 'm':
		return round(float(match.group(1)), 1)
	elif match.group(2) == 'ft':
		return round(float(match.group(1)) * 0.3048, 1)
	else:
		raise ValueError('Unknown length unit {0}'.format(match.group(2)))

def parseRwdir(rwdir):
	if not rwdir:
		return ''
	d = int(int(rwdir)/10)
	dd = (d + 18) % 36
	if dd == 0:
		dd = 36

	first = min(d,dd)
	second = max(d,dd)
	d = first
	dd = second

	if d < 10:
		d = '0{0}'.format(d)
	if dd < 10:
		dd = '0{0}'.format(dd)
	return '{0}/{1}'.format(d, dd)

if __name__=='__main__':
	# A simple-as-possible json format for cup to be used as an intermediate
    # format for the scripts and tools. This way, parsing is only done once.

	cvr = csv.DictReader(sys.stdin, fieldnames=['name','code','country','lat','lon','elev','style','rwdir','rwlen','freq','desc','userdata','pics'])
	# Skip first row
	next(cvr)

	out = []
	for row in cvr:
		if not row['lat']:
			continue
		name = row['name'].strip()
		style = int(row['style'])
		d = {
			'name' : name,
			'lat' : round(parseLat(row['lat']), 6), # float. decimal degrees
			'lon' : round(parseLon(row['lon']), 6), # float. decimal degrees
			'elev' : parseLength(row['elev']), # float. meters
		}

		if style in [2,3,5]:
			d['landable'] = {}

		if row['rwdir'] and int(row['rwdir']) != 0 and 'landable' in d:
			if row['rwlen'] and parseLength(row['rwlen']) > 0.0:
				d['landable']['runways'] = [
					{
                    	'name' : parseRwdir(row['rwdir']),
                    	'len' : parseLength(row['rwlen']),
						'dir' : int(row['rwdir']),
                    	'surface' : 'paved' if style == 5 else 'unpaved'
                	}
				]
		if row['code']:
			d['code'] = str(row['code']).strip()
		if row['freq'] and 'landable' in d:
			d['landable']['freq'] = str(row['freq']).strip()
		if row['desc']:
			d['desc'] = str(row['desc']).strip()
		#'userdata' : None,
		#'pics' : None,
		out.append(d)

	outDict = {
		'name':'',
		'desc':'',
		'schema': 2,
		'turnpoints': sorted(out, key=lambda tp: tp['name'])
	}
	print(json.dumps(outDict, sort_keys=False, indent=2))
