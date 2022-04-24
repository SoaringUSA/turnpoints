#!/usr/bin/env python3

import json
import re
import sys

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
		noDupeData = {}
		for (name, tp) in input.items():	
			a = [tp['lat'], tp['lon']]
			isDuplicate = False
			# Name dedupe
			if name in outData:
				print('Name collision "{0}"'.format(name), file=sys.stderr)
				newName = '{0}-1'.format(name)
				newNameId = 1
				while newName in outData:
					newNameId += 1
					newName = '{0}-{1}'.format(name, newNameId)
				print('  Renaming "{0}" to "{1}"'.format(name, newName), file=sys.stderr)
				name = newName
			# Position dedupe
			for (oldName, oldTp) in outData.items():
				b = [oldTp['lat'], oldTp['lon']]
				# 1 minute of arc (1 nm latitude, 0-1 nm longitude)
				if absNorm(a,b) < 1.0 / 60.0:
					isDuplicate = True
					print('Waypoint "{0}" detected as duplicate of "{1}"'.format(name, oldName), file=sys.stderr)
					break
			if not isDuplicate:
				noDupeData[name] = tp
		outData.update(noDupeData)

	# Sort data
	outData = dict(sorted(outData.items()))

	description = 'Combined turnpoints of'
	for filename in sys.argv[1:]:
		description += ' ' + filename
	outDict = {
		'name' : outputName,
		'desc' : description,
		'schema' : 1,
		'turnpoints' : outData
	}
	print(json.dumps(outDict, sort_keys=False, indent=2))
