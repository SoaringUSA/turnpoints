#!/usr/bin/env python3

import csv
import re
import sys
import xml.etree.ElementTree as ET

def parseLat(latStr):
	# 36:53.583N,121:15.800W
	match = re.match('(\d*\d\d):(\d\d[.]\d+)([NS]?)', latStr)
	if match:
		hemi = match.group(3) if match.group(3) else 'N'
		return '{0}{1}{2}'.format(match.group(1), match.group(2), hemi)

	# 36:53:58N,121:15:40W
	match = re.match('(\d*\d\d):(\d\d):(\d\d)([NS])', latStr)
	minutes = float(match.group(2)) + float(match.group(3)) / 60.0
	hemi = match.group(4) if match.group(4) else 'N'
	return '{0}{1:06.3f}{2}'.format(match.group(1), minutes, hemi)

def parseLon(lonStr):
	match = re.match('(\d*\d\d):(\d\d[.]\d+)([EW]?)', lonStr)
	if match:
		hemi = match.group(3) if match.group(3) else 'W'
		return '{0}{1}{2}'.format(match.group(1), match.group(2), hemi)

	match = re.match('(\d*\d\d):(\d\d):(\d\d)([EW]?)', lonStr)
	minutes = float(match.group(2)) + float(match.group(3)) / 60.0
	hemi = match.group(4) if match.group(4) else 'W'
	return '{0}{1:06.3f}{2}'.format(match.group(1), minutes, hemi)

def parseElev(elev):
	match = re.match('(\d+)(F|M)', elev)
	if not match:
		return ''
	#units = "ft" if 'F' in match.group(2) else "m"
	#return '{0}{1}'.format(match.group(1), units)
	if 'M' in match.group(2):
		return '{0}{1}'.format(match.group(1), match.group(2))
	
	feet = float(match.group(1))
	meters = feet * 0.3048
	return '{0:.1f}m'.format(meters)

def cupWriter(fileHandle):
	cvw = csv.DictWriter(fileHandle, fieldnames=['name','code','country','lat','lon','elev','style','rwdir','rwlen','freq','desc','userdata','pics'], quoting=csv.QUOTE_NONE)
	return cvw

def styleFromAttr(attr):
	# A - airport
	# L - landable
	# T,S,F - turnpoint,start,finish
	# H - home
	if 'A' in attr:
		#return 5 # hard surface runway
		return 2 # grass surface runway
	elif 'L' in attr:
		return 3 # outlanding
	elif 'T' in attr or 'S' in attr or 'F' in attr:
		return 1 # waypoint
	else:
		return 0 # unknown

if __name__=='__main__':
	# name,code,country,lat,lon,elev,style,rwdir,rwlen,freq,desc,userdata,pics
	cvr = csv.DictReader(filter(lambda row: row[0] != '*', sys.stdin), fieldnames=['index', 'lat', 'lon', 'elev', 'attr', 'name', 'comment'])

	cvw = cupWriter(sys.stdout)
	cvw.writeheader()

	for row in cvr:
		if not row['lat']:
			continue

		outDict = {
			'name' : row['name'].strip(),
			'code' : '',
			'country' : '',
			'lat' : parseLat(row['lat']),
			'lon' : parseLon(row['lon']),
			'elev' : parseElev(row['elev']),
			'style' : styleFromAttr(row['attr']),
			'rwdir' : '',
			'rwlen' : '',
			'freq' : '',
			'desc' : row['comment'].strip() if row['comment'] else '',
			'userdata' : '',
			'pics' : '',
		}
		cvw.writerow(outDict)


