#!/usr/bin/env python3

import csv
import re
import json
import sys

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

def parseLength(meters):
	return int(meters * 3.28084)

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
	input = json.load(sys.stdin)

	cvw = csv.DictWriter(sys.stdout, fieldnames=['NUM','NAM','COM','LAT_D','LAT_M','LAT_S','LON_D','LON_M','LON_S','COD','ALT','FRE','RW_D','RW_H','RW_L','RW_S','RW_W','RW_G','ICAO','NAM_12','COM_12','CIT','CUP_COD','FAA_NAME','FRE_ATIS','FRE_AWOS','FRE_CTAF','FRE_TOWER','FRE_UNICOM','FUEL','GLIDERS','MAG','STA','STATE_ABBREV','TEL'], delimiter='	', quoting=csv.QUOTE_NONE)
	cvw.writeheader()

	rowNum = 0
	for (name, tp) in input['turnpoints'].items():
		rowNum += 1
		latDms = dms(tp['lat'])
		lonDms = dms(tp['lon'])
		
		freq = ''
		rwdir = ''
		rwlen = ''
		if 'landable' in tp:
			if 'runways' in tp['landable'] and len(tp['landable']['runways']) > 0:
				rw0 = tp['landable']['runways'][0]
				if 'dir' in rw0:
					rwdir = rw0['dir']
				if 'len' in rw0:
					rwlen = rw0['len']
			if 'freq' in tp['landable']:
				freq = tp['landable']['freq']

		outDict = {
			'NUM' : rowNum,
			'NAM' : name,
			'COM' : tp['desc'] if 'desc' in tp else '',
			'LAT_D' : latDms[0],
			'LAT_M' : latDms[1],
			'LAT_S' : latDms[2],
			'LON_D' : lonDms[0],
			'LON_M' : lonDms[1],
			'LON_S' : lonDms[2],
			'COD' : '',
			'ALT' : parseLength(tp['elev']),
			'FRE' : freq,
			'RW_D' : rwdir,
			'RW_H' : '',
			'RW_L' : rwlen,
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


