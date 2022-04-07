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
		return float(match.group(1))
	elif match.group(2) == 'ft':
		return float(match.group(1)) * 0.3048
	else:
		raise ValueError('Unknown length unit {0}'.format(match.group(2)))

if __name__=='__main__':
	# A simple-as-possible json format for cup to be used as an intermediate
    # format for the scripts and tools. This way, parsing is only done once.

	cvr = csv.DictReader(sys.stdin, fieldnames=['name','code','country','lat','lon','elev','style','rwdir','rwlen','freq','desc','userdata','pics'])
	# Skip first row
	next(cvr)

	outDict = {}
	for row in cvr:
		if not row['lat']:
			continue
		name = row['name'].strip()
		outDict[name] = {
            'name' : name,
            'code' : str(row['code']).strip() if row['code'] else None,
            'country' : str(row['country']).strip() if row['country'] else None,
            'lat' : parseLat(row['lat']), # float. decimal degrees
            'lon' : parseLon(row['lon']), # float. decimal degrees
            'elev' : parseLength(row['elev']), # float. meters
            'style' : int(row['style']) if row['style'] else None,
            'rwdir' : int(row['rwdir']) if row['rwdir'] else None,
            'rwlen' : parseLength(row['rwlen']), # float. meters
            'freq' : str(row['freq']).strip() if row['freq'] else None,
            'desc' : str(row['desc']).strip() if row['desc'] else None,
            'userdata' : None,
            'pics' : None,
        }

	print(json.dumps(outDict, sort_keys=True, indent=2))
