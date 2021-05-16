#!/bin/bash
SUM=0
FILES=`find / -mount -type f -mtime -1 |xargs du -k|awk '{print $1}'`

for f in $FILES; do
	SUM=$((SUM+f));
done:

SU;=$((SUM/1024));

echo "$SUM MB"|mail -s "$HOSTNAME free space" root

