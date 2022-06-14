#!/bin/sh -e

INFILES=$(ls turnpoints/*.json)

for file in $INFILES; do
	echo "Validating $file..."
	./validate.py < $file
	echo "  OK"
done
