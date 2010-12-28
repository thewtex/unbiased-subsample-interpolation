#!/bin/bash

if test $# -lt 1; then
  echo "usage $0 <VARIABLE_NAME>"
  exit 1
fi

VARIABLE_NAME="$1"

OUTPUT=SNRe_${VARIABLE_NAME}.csv
rm -f ${OUTPUT}

head -n 1 $(find . -mindepth 2 -name "*${VARIABLE_NAME}.csv" -print | head -n 1) > ${OUTPUT}

for f in $(find . -mindepth 2 -name "*${VARIABLE_NAME}.csv" -print); do
  #echo $f
   sed '1,1d' $f >> ${OUTPUT}
done
