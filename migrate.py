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

    print(json.dumps(outDict, sort_keys=False, indent=2))