#!/usr/bin/env python3

import csv
import json
import sys

def schemaVersion(inputDict):
    return inputDict['schema'] if 'schema' in inputDict else 0

if __name__=='__main__':
    input = json.load(sys.stdin)
    inputSchemaVersion = schemaVersion(input)
    outputSchemaVersion = 1

    # 0->1
    if inputSchemaVersion == 0:
        outDict = {
            'name' : '',
            'desc' : '',
            'schema' : 1,
            'turnpoints' : input
        }
        inputSchemaVersion = 1
        input = outDict

    # 1->2 etc.
    if inputSchemaVersion == 1:
        tpOut = []
        for (name, tp) in input['turnpoints'].items():
            nd = {'name' : name}
            nd.update(tp)
            tpOut.append(nd)
        outDict = {
            'name' : input['name'],
            'desc' : input['desc'],
            'schema' : 2,
            'turnpoints' : sorted(tpOut, key=lambda tp: tp['name'])
        }
        inputSchemaVersion = 2
        input = outDict

    print(json.dumps(outDict, sort_keys=False, indent=2))