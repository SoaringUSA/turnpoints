#!/usr/bin/env python3

import json
import re
import sys
import xml.etree.ElementTree as ET

def styleRef(tp):
    if 'landable' in tp:
        landable = tp['landable']
        if 'runways' in landable and len(landable['runways']) > 0:
            rw0 = landable['runways'][0]
            if 'surface' in rw0 and rw0['surface'] == 'paved':
                return '#pavedAirfield'
            else:
                return '#unpavedAirfield'
        else:
            return '#landout'
    else:
        return '#waypoint'

if __name__=='__main__':
	input = json.load(sys.stdin)

	kmlRoot = ET.Element('kml', attrib={'xmlns' : 'http://www.opengis.net/kml/2.2', 'xmlns:gx' : 'http://www.google.com/kml/ext/2.2'})
	kmlDocument = ET.SubElement(kmlRoot, 'Document')
	kmlDocName = ET.SubElement(kmlDocument, 'name')
	kmlDocName.text = 'Document name'
	kmlDocDesc = ET.SubElement(kmlDocument, 'description')
	kmlDocDesc.text = 'Document description'

	# Placemark styles
	style = ET.SubElement(kmlDocument, 'Style', attrib={'id' : 'waypoint'})
	icon = ET.SubElement(style, 'Icon')
	href = ET.SubElement(icon, 'href')
	href.text = 'https://maps.google.com/mapfiles/kml/pushpin/red-pushpin.png'

	style = ET.SubElement(kmlDocument, 'Style', attrib={'id' : 'landout'})
	icon = ET.SubElement(style, 'Icon')
	href = ET.SubElement(icon, 'href')
	href.text = 'https://maps.google.com/mapfiles/kml/paddle/ylw-circle.png'

	style = ET.SubElement(kmlDocument, 'Style', attrib={'id' : 'unpavedAirfield'})
	icon = ET.SubElement(style, 'Icon')
	href = ET.SubElement(icon, 'href')
	href.text = 'https://maps.google.com/mapfiles/kml/paddle/grn-circle.png'

	style = ET.SubElement(kmlDocument, 'Style', attrib={'id' : 'pavedAirfield'})
	icon = ET.SubElement(style, 'Icon')
	href = ET.SubElement(icon, 'href')
	href.text = 'https://maps.google.com/mapfiles/kml/shapes/airports.png'

	for (name, tp) in input.items():
		lat = tp['lat']
		lon = tp['lon']
		kmlPlacemark = ET.SubElement(kmlDocument, 'Placemark')
		kmlName = ET.SubElement(kmlPlacemark, 'name')
		kmlName.text = name
		if 'desc' in tp:
			kmlDescription = ET.SubElement(kmlPlacemark, 'description')
			kmlDescription.text = tp['desc']
		kmlPoint = ET.SubElement(kmlPlacemark, 'Point')
		kmlCoords = ET.SubElement(kmlPoint, 'coordinates')
		kmlCoords.text = '{0},{1}'.format(lon, lat)
		styleUrl = ET.SubElement(kmlPlacemark, 'styleUrl')
		styleUrl.text = styleRef(tp)
		

	kmlTree = ET.ElementTree(kmlRoot)
	kmlTree.write(sys.stdout.buffer, xml_declaration=True, encoding='UTF-8')

