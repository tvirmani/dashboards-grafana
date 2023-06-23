#!/bin/bash
FILE=/opt/couchbase/init/setupComplete.txt
if ! [ -f "$FILE" ]; then
  echo "Tarun Virmani"
  touch $FILE
fi