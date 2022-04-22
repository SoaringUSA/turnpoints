#!/usr/bin/env python3

import csv
import json
import re
import sys

def parseLat(latStr):
	# 36:53.583N,121:15.800W
	match = re.match('(\d*\d\d):(\d\d[.]\d+)([NS]?)', latStr)
	if match:
		hemi = match.group(3) if match.group(3) else 'N'
		deg = float(match.group(1)) + float(match.group(2)) / 60.0
		deg *= 1.0 if hemi == 'N' else -1.0
		return deg

	# 36:53:58N,121:15:40W
	match = re.match('(\d*\d\d):(\d\d):(\d\d)([NS])', latStr)
	minutes = float(match.group(2)) + float(match.group(3)) / 60.0
	hemi = match.group(4) if match.group(4) else 'N'
	deg = float(match.group(1)) + minutes / 60.0
	deg *= 1.0 if hemi == 'N' else -1.0
	return '{0}{1:06.3f}{2}'.format(match.group(1), minutes, hemi)

def parseLon(lonStr):
	match = re.match('(\d*\d\d):(\d\d[.]\d+)([EW]?)', lonStr)
	if match:
		hemi = match.group(3) if match.group(3) else 'W'
		deg = float(match.group(1)) + float(match.group(2)) / 60.0
		deg *= -1.0 if hemi == 'W' else 1.0
		return deg

	match = re.match('(\d*\d\d):(\d\d):(\d\d)([EW]?)', lonStr)
	minutes = float(match.group(2)) + float(match.group(3)) / 60.0
	hemi = match.group(4) if match.group(4) else 'W'
	deg = float(match.group(1)) + minutes / 60.0
	deg *= -1.0 if hemi == 'W' else 1.0
	return deg

def parseElev(elev):
	match = re.match('(\d+)(F|M)', elev)
	if not match:
		return ''
	#units = "ft" if 'F' in match.group(2) else "m"
	#return '{0}{1}'.format(match.group(1), units)
	if 'M' in match.group(2):
		return match.group(1)
	
	feet = float(match.group(1))
	meters = feet * 0.3048
	return meters

if __name__=='__main__':
	cvr = csv.DictReader(filter(lambda row: row[0] != '*', sys.stdin), fieldnames=['index', 'lat', 'lon', 'elev', 'attr', 'name', 'comment'])

	outDict = {}
	for row in cvr:
		if not row['lat']:
			continue

		name = row['name'].strip()
		d = {
			'lat' : parseLat(row['lat']),
			'lon' : parseLon(row['lon']),
			'elev' : parseElev(row['elev']),
		}
		if 'comment' in row:
			d['desc'] = row['comment'].strip()
		# A - airport
		# L - landable
		# T,S,F - turnpoint,start,finish
		# H - home
		attr = row['attr']
		if 'A' in attr or 'L' in attr:
			d['landable'] = {}
		
		outDict[name] = d
	
	outDict = dict(sorted(outDict.items()))
	print(json.dumps(outDict, sort_keys=False, indent=2))


