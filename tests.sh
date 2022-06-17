#!/bin/sh -e

INFILES=$(ls turnpoints/*.json)

for file in $INFILES; do
	printf "Validating $file..."
	./validate.py < $file
	printf "OK\n"
done

# California
printf "Validating California..."
./combine.py 'California' turnpoints/hllstr.json turnpoints/wsc.json turnpoints/truckee.json turnpoints/montag.json 2> /dev/null | ./validate.py
printf "OK\n"