#!/bin/bash
# Horuseye job.sh implemented by bash shell scripts, v0.01
# by Zing 2015  http://www.z1ng.net



#dump an image of memory with lime
KVER=$(uname -r);
LIME=$PWD/lime/src/lime-$KVER.ko;
IMAGEPATH=$PWD/image/;
FILENAME=$(date +%Y-%m-%d-%H-%M-%S)".lime";
insmod $LIME "path=$IMAGEPATH/$FILENAME format=lime";
if [ $? -ne 0 ]
then
    echo "$FILENAME image built failed." >> $WORKDIR/log/HorusEye.log;
    exit
fi
rmmod lime.ko;
echo $FILENAME










