#!/bin/sh -e

INFILES="hllstr.json truckee.json wsc.json"
DATE=$(date '+%Y%m%d')

TMPDIR=$(mktemp -d)
DIR=$TMPDIR/SUSATurnpoints
mkdir $DIR
for infile in $INFILES; do
	BNAME="$(basename $infile .json)_$DATE"
	cp $infile "$DIR/$BNAME.json"
	./tocup.py < $infile > "$DIR/$BNAME.cup"
	./tokml.py < $infile > "$DIR/$BNAME.kml"
done

tar -czf "SUSATurnpoints_$DATE.tar.gz" -C $TMPDIR .
rm -rf $TMPDIR
