#!/bin/sh -e

INFILES="turnpoints/hllstr.json turnpoints/montag.json turnpoints/truckee.json turnpoints/wsc.json turnpoints/experimental_ca.json"
DATE=$(date '+%Y%m%d')

for infile in $INFILES; do
	printf "Validating $infile..."
	./validate.py < $infile
	printf 'OK\n'
done

TMPDIR=$(mktemp -d)
DIR=$TMPDIR/SUSATurnpoints
mkdir $DIR
for infile in $INFILES; do
	BNAME="$(basename $infile .json)_$DATE"
	cp $infile "$DIR/$BNAME.json"
	./tocup.py < $infile > "$DIR/$BNAME.cup"
	./todat.py < $infile > "$DIR/$BNAME.dat"
	./tokml.py < $infile > "$DIR/$BNAME.kml"
done

# California
./combine.py 'California' turnpoints/hllstr.json turnpoints/wsc.json turnpoints/truckee.json turnpoints/montag.json > "$DIR/california_$DATE.json"
./validate.py < "$DIR/california_$DATE.json"
./tocup.py < "$DIR/california_$DATE.json" > "$DIR/california_$DATE.cup"
./todat.py < "$DIR/california_$DATE.json" > "$DIR/california_$DATE.dat"
./tokml.py < "$DIR/california_$DATE.json" > "$DIR/california_$DATE.kml"

OUTDIR=$(pwd)
#tar -czf "SUSATurnpoints_$DATE.tar.gz" -C $TMPDIR .
pushd $TMPDIR
	zip -r "SUSATurnpoints_$DATE.zip" $(basename $DIR)
	mv "SUSATurnpoints_$DATE.zip" $OUTDIR
popd
rm -rf $TMPDIR
