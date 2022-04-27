#!/usr/bin/env python3

import json
import sys

from wgs84 import WGS84

def help():
    print('Pare a large turnpoint set into a smaller one', sys.stderr)
    print('USAGE: ./cut.py <COMMAND> options...', sys.stderr)
    print('  COMMAND = box', sys.stderr)

def helpBox():
    print('./cut.py box <lat0> <lat1> <lon0> <lon1>', sys.stderr)
    print('  Selects all turnpoints within the lat/lon box. All coordinates are decimal degrees.', sys.stderr)

def helpRadius():
    print('./cut.py radius <lat> <lon> <radius_km>', sys.stderr)
    print('  Selects all turnpoints within <radius_km> kilometers of the given position. All coordinates are decimal degrees.', sys.stderr)

def isInBox(nameTp, lat0, lat1, lon0, lon1):
    tp = nameTp[1]
    return lat0 <= tp['lat'] and tp['lat'] <= lat1 and lon0 <= tp['lon'] and tp['lon'] <= lon1

def isInRadius(nameTp, lat, lon, radiusKm):
    tp = nameTp[1]
    x0 = WGS84.cartesian(lat, lon)
    x1 = WGS84.cartesian(tp['lat'], tp['lon'])
    d = [(a - b)**2 for (a,b) in zip(x0,x1)]
    d2 = sum(d) / 1000000.0
    return d2 <= radiusKm*radiusKm

if __name__=='__main__':
    if len(sys.argv) < 2:
        help()
        sys.exit(1)

    command = sys.argv[1]
    input = json.load(sys.stdin)

    filtFun = None
    if command == 'box':
        if len(sys.argv) < 6:
            helpBox()
            sys.exit(1)
        lat0 = float(sys.argv[2])
        lat1 = float(sys.argv[3])
        lon0 = float(sys.argv[4])
        lon1 = float(sys.argv[5])
        filtFun = lambda x: isInBox(x, lat0, lat1, lon0, lon1)
    elif command == 'radius':
        if len(sys.argv) < 5:
            helpRadius()
            sys.exit(1)
        lat = float(sys.argv[2])
        lon = float(sys.argv[3])
        distKm = float(sys.argv[4])
        filtFun = lambda x: isInRadius(x, lat, lon, distKm)
    else:
        help()
        sys.exit(1)

    outDict = {}
    for (name, tp) in filter(filtFun, input['turnpoints'].items()):
            outDict[name] = tp
    outDict = {
        'name':'',
        'desc': 'Created with: {0}'.format(sys.argv),
        'schema': 1,
        'turnpoints': dict(sorted(outDict.items()))
    }
    print(json.dumps(outDict, sort_keys=False, indent=2))