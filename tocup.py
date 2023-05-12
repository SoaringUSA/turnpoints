#!/usr/bin/env python3

import csv
import json
import sys

class CupWriter:
	def __init__(self, fileHandle):
		self.fileHandle = fileHandle
		self.fieldnames = ['name','code','country','lat','lon','elev','style','rwdir','rwlen','rwwidth','freq','desc','userdata','pics']
	def writeheader(self):
		for name in self.fieldnames:
			if name == 'name':
				self.fileHandle.write('"name"')
			else:
				self.fileHandle.write(',"{}"'.format(name))
		self.fileHandle.write('\n')
	def writerow(self, d):
		for field in self.fieldnames:
			self._writefield(field, d)
		self.fileHandle.write('\n')
	def _writefield(self, field, d):
		# First field
		if field == 'name':
				self.fileHandle.write('"{}"'.format(CupWriter.sanitized(d['name'])))
		# Quoted fields
		elif field in ['code', 'country', 'desc']:
			if field in d:
				self.fileHandle.write(',"{}"'.format(CupWriter.sanitized(d['name'])))
			else:
				self.fileHandle.write(',""')
		# Unquoted fields
		else:
			if field in d:
				self.fileHandle.write(',{}'.format(d[field]))
			else:
				self.fileHandle.write(',')
	def sanitized(s):
		return s.replace('"', '\'')

def cupWriter(fileHandle):
	return CupWriter(sys.stdout)

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
				if 'width' in rw0:
					outDict['rwwidth'] = '{0:.1f}m'.format(rw0['width'])
		outDict['style'] = str(style)
		cvw.writerow(outDict)
