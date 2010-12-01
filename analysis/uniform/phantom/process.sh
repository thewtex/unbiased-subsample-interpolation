#!/bin/sh

STRAINS=( 0.5 1.0 3.0 5.0 7.0 9.0 11.0 )
AXIAL_SEARCH=50

ALGORITHM=/tmp/strainb/bin/mmm-strain

PREFIX=/home/matt/rs/data/phantoms/elastography/uniform/25_June_07/2010-07-13/uniform25June07_
OUTPUT_PREFIX=uniform_phantom

TRIALSTART=1
TRIALEND=30

for index in {0..6}
do
  SUBPATH="${STRAINS[index]}_strain"
  mkdir -p ${SUBPATH}

  RESULTS_FILE="${SUBPATH}/SNRe.csv"
  echo -n '' > ${RESULTS_FILE}
  TRIAL=${TRIALSTART}
  while test $TRIAL -le $TRIALEND
  do
    echo "Processing trial ${TRIAL} for strain ${STRAINS[index]}..."
    ls ${PREFIX}${STRAINS[index]}*pertr${TRIAL}*.rfd
    let 'TRIAL++'
  done
done
