#!/usr/bin/env python3

import csv
import re
import sys

def cupReader(fileHandle):
	# name,code,country,lat,lon,elev,style,rwdir,rwlen,freq,desc,userdata,pics
	cvr = csv.DictReader(fileHandle, fieldnames=['name','code','country','lat','lon','elev','style','rwdir','rwlen','freq','desc','userdata','pics'])
	# Skip first row
	next(cvr)
	return cvr

def cupWriter(fileHandle):
	cvw = csv.DictWriter(fileHandle, fieldnames=['name','code','country','lat','lon','elev','style','rwdir','rwlen','freq','desc','userdata','pics'])
	return cvw

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
		return 0.0
	match = re.match('(\d*[.]?\d*)(m|ft)', elevStr)
	if match.group(2) == 'm':
		return float(match.group(1)) * 3.28084
	elif match.group(2) == 'ft':
		return float(match.group(1))
	else:
		raise ValueError('Unknown length unit {0}'.format(match.group(2)))

def comments(row):
    ret = ''
    #for k in ['style','rwdir','rwlen','freq','desc','userdata','pics']:
    for k in ['style','desc','userdata','pics']:
        ret += '{0},'.format(row[k])
    return ret

def location(row):
    ret = ''
    for k in ['lat','lon','elev']:
        ret += '{0},'.format(row[k])
    return ret

def readRows(cvr):
    ret = {}
    for row in cvr:
        if not row['lat']:
            continue
        ret[row['name']] = row
    return ret

if __name__=='__main__':
	
    if len(sys.argv) < 3:
        print('./cupdiff left.cup right.cup')
        print('    Summarizes the differences between cup files.')
        print('')
        exit(1)

    leftFile = open(sys.argv[1], 'r')
    rightFile = open(sys.argv[2], 'r')

    left = readRows(cupReader(leftFile))
    right = readRows(cupReader(rightFile))

    print('# CUP Diff "{0}" "{1}"'.format(sys.argv[1], sys.argv[2]))
    print('')
    print('## Deleted Turnpoints')
    print('')
    for leftName in left:
        if leftName not in right:
            print(' - "{0}"'.format(leftName))
    print('')
    print('## New Turnpoints')
    print('')
    for rightName in right:
        if rightName not in left:
            print(' - "{0}"'.format(rightName))
    print('')
    print('## Modified')
    print('')
    for name in left:
        if name not in right:
            continue
        leftCom = comments(left[name])
        rightCom = comments(right[name])
        leftLoc = location(left[name])
        rightLoc = location(right[name])

        leftLat = parseLat(left[name]['lat'])
        rightLat = parseLat(right[name]['lat'])
        leftLon = parseLon(left[name]['lon'])
        rightLon = parseLon(right[name]['lon'])
        leftAlt = parseLength(left[name]['elev'])
        rightAlt = parseLength(right[name]['elev'])

        latDiff = abs(leftLat - rightLat) > 0.001
        lonDiff = abs(leftLon - rightLon) > 0.001
        altDiff = abs(leftAlt - rightAlt) > 0.1
        different = leftCom != rightCom or latDiff or lonDiff or altDiff

        if different:
            print('### {0}'.format(name))
            print('')
            if latDiff:
                print(' - Latitude "{0:.3f}" -> "{1:.3f}"'.format(leftLat, rightLat))
            if lonDiff:
                print(' - Longitude "{0:.3f}" -> "{1:.3f}"'.format(leftLon, rightLon))
            if altDiff:
                print(' - Altitude "{0:.1f}" -> "{1:.1f}"'.format(leftAlt, rightAlt))
            if leftCom != rightCom:
                print(' - Comments "{0}" -> "{1}"'.format(leftCom, rightCom))
            print('')