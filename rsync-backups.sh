#!/bin/bash

SOURCE_DIRS="/home/ /var/"
DESTINATION="/backups"
RSYNC_CMD="rsync -avP"



for ITEM in $SOURCE_DIRS; do 
	if [ ! -d "$DESTINATION$ITEM" ]; then
		mkdir -p "$DESTINATION$ITEM"
	fi 

	$RSYNC_CMD $ITEM "$DESTINATION$ITEM"
done