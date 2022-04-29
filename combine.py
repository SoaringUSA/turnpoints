#!/usr/bin/env python3

import json
import re
import sys

from wgs84 import WGS84

def absNorm(a, b):
	return abs(a[0] - b[0]) + abs(a[1] - b[1])

def help():
	print('Usage: ./combine.py <output name> [file.json]...')

if __name__=='__main__':
	if len(sys.argv) < 2:
		help()
		sys.exit(1)

	numInputs = len(sys.argv) - 1
	outputName = sys.argv[1]
	data = []
	for filename in sys.argv[2:]:
		input = json.load(open(filename))
		data.append(input['turnpoints'])

	# Prefer data in order of input. Take all rows from first file. Take
	# rows from other files in order if not duplicates
	outData = data[0]
	for input in data[1:]:
		for tp in input:
			a = [tp['lat'], tp['lon']]
			isDuplicate = False
			# Position dedupe
			for oldTp in outData:
				b = [oldTp['lat'], oldTp['lon']]
				# 1km radius for dupes
				if WGS84.geodesic(a, b) < 1000:
					isDuplicate = True
					print('Waypoint "{0}" detected as duplicate of "{1}"'.format(tp['name'], oldTp['name']), file=sys.stderr)
					break
			if not isDuplicate:
				outData.append(tp)

	# Sort turnpoints by name
	outData = sorted(outData, key=lambda tp: tp['name'])

	description = 'Combined turnpoints of'
	for filename in sys.argv[1:]:
		description += ' ' + filename
	outDict = {
		'name' : outputName,
		'desc' : description,
		'schema' : 2,
		'turnpoints' : outData
	}
	print(json.dumps(outDict, sort_keys=False, indent=2))
