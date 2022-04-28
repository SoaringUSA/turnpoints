#!/usr/bin/env python3

import jsonschema
import json
import sys

schema_v1 = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    'type' : 'object',
    'description' : 'Soaring turnpoint database in human-editable format.',
    'properties' : {
        'name' : {'type' : 'string', 'description' : 'Short name for the database'},
        'desc' : {'type' : 'string', 'description' : 'Longer description for the database'},
        'schema' : {'type' : 'integer', 'description' : 'Version of this json schema the document claims to be'},
        'turnpoints' : { 'type' : 'array', 'items' : {'$ref' : '#/definitions/turnpoint'}}
    },

    'required' : ['name', 'schema'],
    'additionalProperties' : False,

    'definitions' : {
        'turnpoint' : {
            'type' : 'object',
            'description' : 'A single turnpoint',
            'properties' : {
                'name' : {'type' : 'string', 'description' : 'User-visible name of the turnpoint'},
                'lat': {'type' : 'number', 'description' : 'Signed decimal degrees'},
                'lon': {'type' : 'number', 'description' : 'Signed decimal degrees'},
                'elev': {'type' : 'number', 'description' : 'Meters'},
                'code': {'type' : 'string', 'description' : 'Short unique code for turnpoint. Must be unique among all turnpoints.'},
                'desc': {'type' : 'string', 'description' : 'Extra details about turnpoint'},
                'landable' : {'$ref' : '#/definitions/landable'},
            },
            'required' : ['name', 'lat', 'lon', 'elev'],
            'additionalProperties' : False
        },
        'landable' : {
            'type' : 'object',
            'description' : 'If present, turnpoint is landable. If empty, landable has no runways or is a field or some secondary option.',
            'properties': {
                'freq': {'type' : 'string', 'description' : 'Frequency to monitor before landing.'},
                'runways' : {
                    'type' : 'array',
                    'items' : {'$ref' : '#/definitions/runway'},
                    'description' : 'Array of landable runways. First element is the preferred glider runway. The rest are in order of decreasing preference.'
                }
            },
            'additionalProperties' : False
        },
        'runway' : {
            'type' : 'object',
            'properties' : {
                'name' : {'type' : 'string', 'description' : 'Official designator for runway e.g "06L/24R". Must be unique in runways array.'},
                'len' : {'type' : 'number', 'description' : 'Length in meters'},
                'dir' : {'type' : 'integer', 'description' : 'Geographic heading in degrees'},
                'surface': {'enum' : ['paved', 'unpaved']}
            },
            'required' : ['name', 'surface'],
            'additionalProperties' : False
        }
    }
}

if __name__=='__main__':
    data = json.load(sys.stdin)

    # Validate schema
    jsonschema.validate(data, schema=schema_v1)

    # Validate things underneath the schema
    tpcodes = set()
    for tp in data['turnpoints']:
        if 'code' in tp:
            # Ensure turnpoint codes are unique
            if tp['code'] in tpcodes:
                print('Turnpoint code {0} not unique'.format(tp['code']), sys.stderr)
                sys.exit(1)
            else:
                tpcodes.add(tp['code'])
        if 'landable' in tp and 'runways' in tp['landable']:
            runways = tp['landable']['runways']
            rwnames = set()
            for runway in runways:
                # Ensure runway names are unique
                if runway['name'] in rwnames:
                    print('Runway name {0} not unique for turnpoint {1}'.format(runway['name'], tp['name']), sys.stderr)
                    sys.exit(1)
                else:
                    rwnames.add(runway['name'])