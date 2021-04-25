#!/usr/bin/env python3

import csv
import re
import sys
import xml.etree.ElementTree as ET

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

def dms(decimalDeg):
	sign = False if decimalDeg < 0 else True
	decimalDeg = abs(decimalDeg)
	d = int(decimalDeg)
	decimalDeg -= float(d)
	decimalDeg *= 60.0
	m = int(decimalDeg)
	decimalDeg -= float(m) 
	# Round least-significant figure
	s = int(decimalDeg * 60.0 + 0.5)
	
	# NOTE: seems like stx format only cares about the US and
	# West is positive degrees?
	return [d,m,s]

def parseLength(elevStr):
	if not elevStr:
		return ''
	match = re.match('(\d*[.]?\d*)(m|ft)', elevStr)
	if match.group(2) == 'm':
		return int(float(match.group(1)) * 3.28084)
	elif match.group(2) == 'ft':
		return int(float(match.group(1)))
	else:
		raise ValueError('Unknown length unit {0}'.format(group(2)))

def parseRwdir(rwdir):
	if not rwdir:
		return ''
	d = int(int(rwdir)/10)
	dd = (d + 18) % 36
	if dd == 0:
		dd = 36

	if d < 10:
		d = '0{0}'.format(d)
	if dd < 10:
		dd = '0{0}'.format(dd)
	return '{0}/{1}'.format(d, dd)

if __name__=='__main__':
	# name,code,country,lat,lon,elev,style,rwdir,rwlen,freq,desc,userdata,pics
	cvr = csv.DictReader(sys.stdin, fieldnames=['name','code','country','lat','lon','elev','style','rwdir','rwlen','freq','desc','userdata','pics'])
	# Skip first row
	next(cvr)

	cvw = csv.DictWriter(sys.stdout, fieldnames=['NUM','NAM','COM','LAT_D','LAT_M','LAT_S','LON_D','LON_M','LON_S','COD','ALT','FRE','RW_D','RW_H','RW_L','RW_S','RW_W','RW_G','ICAO','NAM_12','COM_12','CIT','CUP_COD','FAA_NAME','FRE_ATIS','FRE_AWOS','FRE_CTAF','FRE_TOWER','FRE_UNICOM','FUEL','GLIDERS','MAG','STA','STATE_ABBREV','TEL'], delimiter='	', quoting=csv.QUOTE_NONE)
	cvw.writeheader()

	rowNum = 0
	for row in cvr:
		if not row['lat']:
			continue
		rowNum += 1
		name = row['name']
		latDms = dms(parseLat(row['lat']))
		lonDms = dms(parseLon(row['lon']))
		
		outDict = {
			'NUM' : rowNum,
			'NAM' : row['name'],
			'COM' : row['desc'],
			'LAT_D' : latDms[0],
			'LAT_M' : latDms[1],
			'LAT_S' : latDms[2],
			'LON_D' : lonDms[0],
			'LON_M' : lonDms[1],
			'LON_S' : lonDms[2],
			'COD' : '',
			'ALT' : parseLength(row['elev']),
			'FRE' : row['freq'],
			'RW_D' : parseRwdir(row['rwdir']),
			'RW_H' : '',
			'RW_L' : parseLength(row['rwlen']),
			'RW_S' : '',
			'RW_W' : '',
			'RW_G' : '',
			'ICAO' : '',
			'NAM_12' : '',
			'COM_12' : '',
			'CIT' : '',
			'CUP_COD' : '',
			'FAA_NAME' : '',
			'FRE_ATIS' : '',
			'FRE_AWOS' : '',
			'FRE_CTAF' : '',
			'FRE_TOWER' : '',
			'FRE_UNICOM' : '',
			'FUEL' : '',
			'GLIDERS' : '',
			'MAG' : '',
			'STA' : '',
			'STATE_ABBREV' : '',
			'TEL' : ''
		}
		cvw.writerow(outDict)


