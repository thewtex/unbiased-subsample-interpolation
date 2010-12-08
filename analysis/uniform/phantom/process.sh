#!/bin/sh

STRAINS=( 0.5 1.0 3.0 5.0 7.0 9.0 11.0 )
AXIAL_SEARCH=50

ALGORITHM=/tmp/strainb/bin/mmm-strain

# change this with program compilation.
INTERP=sinc

COMMON_ARGS="-a 1 -b 30 -c 14 -j 35 -k 16 -l 0.4 -e 5500 -s 40 -t 17 -f 1.0 -u 0.15 -w 0.075"

PREFIX=/home/matt/rs/data/phantoms/elastography/uniform/25_June_07/2010-07-13/uniform25June07_
OUTPUT_PREFIX=uniform_phantom

TRIALSTART=1
TRIALEND=30
#TRIALEND=2

for index in {0..5}
#for index in 2
do
  #for REG in no_regularization
  for REG in no_regularization regularization
  do
    SUBPATH="${STRAINS[index]}_strain/${INTERP}/${REG}"
    mkdir -p ${SUBPATH}

    RESULTS_FILE="${SUBPATH}/SNRe.csv"
    echo -n '' > ${RESULTS_FILE}
    TRIAL=${TRIALSTART}
    while test $TRIAL -le $TRIALEND
    do
      echo "Processing trial ${TRIAL} for strain ${STRAINS[index]}, ${REG}..."
      if test ${REG} = "no_regularization"; then
        ${ALGORITHM} ${PREFIX}0.0*pertr${TRIAL}_*.rfd ${PREFIX}${STRAINS[index]}*pertr${TRIAL}_*.rfd -o ${SUBPATH}/trial_${TRIAL} -m 0 ${COMMON_ARGS}
      else
        ${ALGORITHM} ${PREFIX}0.0*pertr${TRIAL}_*.rfd ${PREFIX}${STRAINS[index]}*pertr${TRIAL}_*.rfd -o ${SUBPATH}/trial_${TRIAL} -m 2 ${COMMON_ARGS}
      fi
      itk-statistics -x 0.1 -y 0.3 ${SUBPATH}/trial_${TRIAL}_StrainComponent2.mha | ../../common/strain_line.py n >> ${RESULTS_FILE}
      itk-statistics -x 0.1 -y 0.3 ${SUBPATH}/trial_${TRIAL}_StrainComponent0.mha | ../../common/strain_line.py >> ${RESULTS_FILE}
      let 'TRIAL++'
    done
  done
done
