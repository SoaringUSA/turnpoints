#!/usr/bin/env python3

import csv
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

def cupReader(fileHandle):
	# name,code,country,lat,lon,elev,style,rwdir,rwlen,freq,desc,userdata,pics
	cvr = csv.DictReader(fileHandle, fieldnames=['name','code','country','lat','lon','elev','style','rwdir','rwlen','freq','desc','userdata','pics'])
	# Skip first row
	next(cvr)
	return cvr

def cupWriter(fileHandle):
	cvw = csv.DictWriter(fileHandle, fieldnames=['name','code','country','lat','lon','elev','style','rwdir','rwlen','freq','desc','userdata','pics'])
	return cvw

def absNorm(a, b):
	return abs(a[0] - b[0]) + abs(a[1] - b[1])

if __name__=='__main__':
	data = []
	for fileNo in range(1,len(sys.argv)):
		filename = sys.argv[fileNo]
		cvr = cupReader(open(filename))
		rows = []
		for row in cvr:
			if not row['lat']:
				continue
			rows.append(row)
		data.append(rows)

	# Prefer data in order of input. Take all rows from first file. Take
	# rows from other files in order if not duplicates
	outData = data[0]
	for fileNo in range(1, len(data)):
		noDupeData = []
		for row in data[fileNo]:	
			a = [parseLat(row['lat']), parseLon(row['lon'])]
			isDuplicate = False
			for oldRow in outData:
				b = [parseLat(oldRow['lat']), parseLon(oldRow['lon'])]
				# 1 minute of arc (1 nm latitude, 0-1 nm longitude)
				if absNorm(a,b) < 1.0 / 60.0:
					isDuplicate = True
					print('Waypoint "{0}" detected as duplicate of "{1}"'.format(row['name'], oldRow['name']), file=sys.stderr)
					break
			if not isDuplicate:
				noDupeData.append(row)
		outData.extend(noDupeData)

	# Sort data
	outData = sorted(outData, key=lambda row: row['name'])
	#print(outData)

	# Write cup
	cw = cupWriter(sys.stdout)	
	cw.writeheader()
	cw.writerows(outData)
	print('-----Related Tasks-----')
