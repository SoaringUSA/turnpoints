#!/bin/sh -e

enable -n echo

INFILES="turnpoints/hllstr.json turnpoints/montag.json turnpoints/truckee.json turnpoints/wsc.json"
DATE=$(date '+%Y%m%d')

for infile in $INFILES; do
	echo -n "Validating $infile..."
	./validate.py < $infile
	echo 'OK'
done

TMPDIR=$(mktemp -d)
DIR=$TMPDIR/SUSATurnpoints
mkdir $DIR
for infile in $INFILES; do
	BNAME="$(basename $infile .json)_$DATE"
	cp $infile "$DIR/$BNAME.json"
	./tocup.py < $infile > "$DIR/$BNAME.cup"
	./tokml.py < $infile > "$DIR/$BNAME.kml"
done

# California
./combine.py 'California' turnpoints/hllstr.json turnpoints/wsc.json turnpoints/truckee.json turnpoints/montag.json > "$DIR/california_$DATE.json"
./validate.py < "$DIR/california_$DATE.json"
./tocup.py < "$DIR/california_$DATE.json" > "$DIR/california_$DATE.cup"
./tokml.py < "$DIR/california_$DATE.json" > "$DIR/california_$DATE.kml"

tar -czf "SUSATurnpoints_$DATE.tar.gz" -C $TMPDIR .
rm -rf $TMPDIR
