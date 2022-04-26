#!/usr/bin/env python3

import json
import sys

def help():
    print('Pare a large turnpoint set into a smaller one', sys.stderr)
    print('USAGE: ./cut.py <COMMAND> options...', sys.stderr)
    print('  COMMAND = box', sys.stderr)

def helpBox():
    print('./cut box <lat0> <lat1> <lon0> <lon1>', sys.stderr)
    print('  Selects all turnpoints within the lat/lon box. All coordinates are decimal degrees.', sys.stderr)

def isInBox(nameTp, lat0, lat1, lon0, lon1):
    tp = nameTp[1]
    return lat0 <= tp['lat'] and tp['lat'] <= lat1 and lon0 <= tp['lon'] and tp['lon'] <= lon1

if __name__=='__main__':
    if len(sys.argv) < 2:
        help()
        sys.exit(1)

    command = sys.argv[1]
    input = json.load(sys.stdin)
    outDict = {}

    if command == 'box':
        if len(sys.argv) < 6:
            helpBox()
            sys.exit(1)
        lat0 = float(sys.argv[2])
        lat1 = float(sys.argv[3])
        lon0 = float(sys.argv[4])
        lon1 = float(sys.argv[5])
        for (name, tp) in filter(lambda x: isInBox(x, lat0, lat1, lon0, lon1), input['turnpoints'].items()):
            outDict[name] = tp
    
    outDict = {
        'name':'',
        'desc': 'Created with: {0}'.format(sys.argv),
        'schema': 1,
        'turnpoints': dict(sorted(outDict.items()))
    }
    print(json.dumps(outDict, sort_keys=False, indent=2))