#!/usr/bin/env python3

from difflib import SequenceMatcher
import json
import sys

from wgs84 import WGS84

def landability(tp):
    landability = 'unlandable'
    if 'landable' in tp:
        landability = 'landout'
        if 'runways' in tp['landable']:
            runways = tp['landable']['runways']
            if len(runways) > 0:
                rw0 = runways[0]
                if 'surface' in rw0 and rw0['surface'] == 'paved':
                    landability = 'paved runway'
                else:
                    landability = 'unpaved runway'
    return landability

def location(row):
    ret = ''
    for k in ['lat','lon','elev']:
        ret += '{0},'.format(row[k])
    return ret

def canonicalTpName(tp):
    # Ignore case and spaces
    ret = ''.join([c for c in tp['name'].lower() if c != ' '])
    # Ignore the stupid -U3 naming suffixes that change all the time
    return ret[0:-3] if ret[-3] == '-' else ret

def isSameTurnpoint(tpl, tpr):
    leftName = canonicalTpName(tpl)
    rightName = canonicalTpName(tpr)

    # If distance is more than 1km, consider as different
    if WGS84.geodesic((tpl['lat'], tpl['lon']), (tpr['lat'], tpr['lon'])) > 1000:
        return False
    # If distance is under 1km and names are similar, then different
    if SequenceMatcher(None, leftName, rightName).ratio() < 0.5:
        return False
    # Distance is less than 1km and names are similar. Then same.
    return True

if __name__=='__main__':
	
    if len(sys.argv) < 3:
        print('./cupdiff left.cup right.cup')
        print('    Summarizes the differences between cup files.')
        print('')
        exit(1)

    leftFile = open(sys.argv[1], 'r')
    rightFile = open(sys.argv[2], 'r')

    left = json.load(leftFile)
    right = json.load(rightFile)
    leftTp = left['turnpoints']
    rightTp = right['turnpoints']

    # Find matches. If this n^2 alg gets too slow, we can start using some
    # hashing.
    matchesLeft = {}
    matchesRight = {}
    for (leftNdx, tpl) in enumerate(leftTp):
        for (rightNdx, tpr) in enumerate(rightTp):
            if isSameTurnpoint(tpl, tpr):
                matchesLeft[leftNdx] = rightNdx
                matchesRight[rightNdx] = leftNdx
                break

    print('# Diff "{0}" "{1}"'.format(sys.argv[1], sys.argv[2]))
    print('')
    print('## Deleted Turnpoints')
    print('')
    for (ndx,tpl) in enumerate(leftTp):
        if ndx not in matchesLeft:
            print(' - "{0}"'.format(tpl['name']))
    print('')
    print('## New Turnpoints')
    print('')
    for (ndx, tpr) in enumerate(rightTp):
        if ndx not in matchesRight:
            print(' - "{0}"'.format(tpr['name']))
    print('')
    print('## Modified')
    print('')
    for (leftNdx, tpl) in enumerate(leftTp):
        if leftNdx not in matchesLeft:
            continue
        rightNdx = matchesLeft[leftNdx]
        tpr = rightTp[rightNdx]

        leftName = tpl['name']
        rightName = tpr['name']
        leftCom = tpl['desc'] if 'desc' in tpl else ''
        rightCom = tpr['desc'] if 'desc' in tpr else ''
        leftLand = landability(tpl)
        rightLand = landability(tpr)
        leftLoc = location(tpl)
        rightLoc = location(tpr)

        leftLat = tpl['lat']
        rightLat = tpr['lat']
        leftLon = tpl['lon']
        rightLon = tpr['lon']
        leftAlt = tpl['elev']
        rightAlt = tpr['elev']

        nameDiff = leftName != rightName
        latDiff = abs(leftLat - rightLat) > 0.001
        lonDiff = abs(leftLon - rightLon) > 0.001
        altDiff = abs(leftAlt - rightAlt) > 1.0
        different = nameDiff or leftCom != rightCom or leftLand != rightLand or latDiff or lonDiff or altDiff

        if different:
            print('### {0}'.format(leftName))
            print('')
            if nameDiff:
                print(' - Name "{0}" -> "{1}"'.format(leftName, rightName))
            if latDiff or lonDiff:
                print(' - Position ({0:.3f}, {1:.3f}) -> ({2:.3f}, {3:.3f})'.format(leftLat, leftLon, rightLat, rightLon))
            if altDiff:
                print(' - Altitude {0:.1f} -> {1:.1f}'.format(leftAlt, rightAlt))
            if leftLand != rightLand:
                print(' - Landability {0} -> {1}'.format(leftLand, rightLand))
            if leftCom != rightCom:
                print(' - Comments "{0}" -> "{1}"'.format(leftCom, rightCom))
            print('')