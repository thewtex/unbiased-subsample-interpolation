#!/bin/bash

if test $# -lt 2; then
  echo "usage: $0 <run_num> <new_attempt_num> [create_jobs]"
  exit 1
fi

RUNDATA_DIR=/home/matt/rundata/strainimg
RUN_NUM=$1
ATTEMPT=$2

for f in $(find ${RUN_NUM} -name process.log); do
  if grep -q 'return value 1' $f; then
    FAILED=$(basename $(dirname $f))
    FAILED_DATASET=$(echo $FAILED | cut -f 1 -d '-')
    FAILED_JOB=$(echo $FAILED | cut -f 2 -d '-')
    if test $# -gt 2; then
      cp -r ${RUNDATA_DIR}/${FAILED_DATASET}/${FAILED_JOB} ${RUNDATA_DIR}/${FAILED_DATASET}/${FAILED_JOB}_attempt_${ATTEMPT}
    else
      echo $FAILED failed
    fi
  fi
done
