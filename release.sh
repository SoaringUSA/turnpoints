#!/bin/sh -e

CUPFILES="hllstr.cup truckee.cup wsc.cup"
DATE=$(date '+%Y%m%d')

TMPDIR=$(mktemp -d)
DIR=$TMPDIR/SUSATurnpoints
mkdir $DIR
for cupfile in $CUPFILES; do
	BNAME="$(basename $cupfile .cup)_$DATE"
	cp $cupfile "$DIR/$BNAME.cup"
	./tokml.py < $cupfile > "$DIR/$BNAME.kml"
done

tar -czf "SUSATurnpoints_$DATE.tar.gz" -C $TMPDIR .
rm -rf $TMPDIR
