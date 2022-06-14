# US Soaring Waypoints

Soaring waypoints for the USA

## Overview

This repo exists to bring together soaring turnpoints from the US and provide
a mechanism to collaborate to keep them updated and version-controlled.

## Getting Started

The scripts require a basic unix shell and python 3 installation. To install
extra requirements:

    pip install -r requirements.txt

Before making a pull request, please make sure all tests pass with:

    ./tests.sh

## Release

Run

    ./release.sh

to generate a .zip file containing the released turnpoints.

## Other Scripts

### combine.py

Combines multiple turnpoint files and de-duplicates entries.

### cupdiff.py

Provide a summary diff between two .cup files. Used for comparing upstream
turnpoint deliveries that arrive in .cup format.

### cut.py

Extract a subset of turnpoints based on conditions like location, state, etc.

### diff.py

Summary diff of two turnpoint files used for creating a changelog.

### fromcup.py

Import a .cup file.

### fromdat.py

Import a .dat file.

### tocup.py

Export to .cup file.

### tokml.py

Export to .kml file.

### tostx.py

Export to .stx file

## JSON Turnpoint Format

The purpose of this format is to keep the turnpoint format human-readable and
as flexible as possible while avoiding writing much custom parsing code.
The format is specified in a formal schema in `validate.py`. That script also
validates whether or not a turnpoint file adheres to the specification.

If you want to add/remove fields in the schema, you must:

  1. Modify `validate.py` to your new proposed schema.
  2. Modify `migrate.py` to move files from the previous schema to the proposed.
  3. Run the migrate script on all existing turnpoints.

## Other File Formats

[CUP File Format](http://download.naviter.com/docs/CUP-file-format-description.pdf)

