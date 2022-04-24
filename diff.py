#!/usr/bin/env python3

import json
import sys

def comments(tp):
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
    ret = 'Landability: {0}. {1}'.format(landability, tp['desc'] if 'desc' in tp else '')
    return ret

def location(row):
    ret = ''
    for k in ['lat','lon','elev']:
        ret += '{0},'.format(row[k])
    return ret

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

    print('# Diff "{0}" "{1}"'.format(sys.argv[1], sys.argv[2]))
    print('')
    print('## Deleted Turnpoints')
    print('')
    for leftName in leftTp:
        if leftName not in rightTp:
            print(' - "{0}"'.format(leftName))
    print('')
    print('## New Turnpoints')
    print('')
    for rightName in rightTp:
        if rightName not in leftTp:
            print(' - "{0}"'.format(rightName))
    print('')
    print('## Modified')
    print('')
    for name in leftTp:
        if name not in rightTp:
            continue

        tpl = leftTp[name]
        tpr = rightTp[name]

        leftCom = comments(tpl)
        rightCom = comments(tpr)
        leftLoc = location(tpl)
        rightLoc = location(tpr)

        leftLat = tpl['lat']
        rightLat = tpr['lat']
        leftLon = tpl['lon']
        rightLon = tpr['lon']
        leftAlt = tpl['elev']
        rightAlt = tpr['elev']

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