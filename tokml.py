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

if __name__=='__main__':
	# name,code,country,lat,lon,elev,style,rwdir,rwlen,freq,desc,userdata,pics
	cvr = csv.DictReader(sys.stdin)

	kmlRoot = ET.Element('kml', attrib={'xmlns' : 'http://www.opengis.net/kml/2.2', 'xmlns:gx' : 'http://www.google.com/kml/ext/2.2'})
	kmlDocument = ET.SubElement(kmlRoot, 'Document')
	kmlDocName = ET.SubElement(kmlDocument, 'name')
	kmlDocName.text = 'Document name'
	kmlDocDesc = ET.SubElement(kmlDocument, 'description')
	kmlDocDesc.text = 'Document description'

	for row in cvr:
		if not row['lat']:
			continue
		name = row['name']
		lat = parseLat(row['lat'])
		lon = parseLon(row['lon'])
		desc = row['desc']
		kmlPlacemark = ET.SubElement(kmlDocument, 'Placemark')
		kmlName = ET.SubElement(kmlPlacemark, 'name')
		kmlName.text = name
		kmlDescription = ET.SubElement(kmlPlacemark, 'description')
		kmlDescription.text = desc
		kmlPoint = ET.SubElement(kmlPlacemark, 'Point')
		kmlCoords = ET.SubElement(kmlPoint, 'coordinates')
		kmlCoords.text = '{0},{1}'.format(lon, lat)

	kmlTree = ET.ElementTree(kmlRoot)
	kmlTree.write(sys.stdout.buffer, xml_declaration=True, encoding='UTF-8')

