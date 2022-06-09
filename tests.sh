#!/bin/sh -e

INFILES=$(ls turnpoints/*.json)

enable -n echo

for file in $INFILES; do
	echo -n "Validating $file..."
	./validate.py < $file
	echo "OK"
done
