#!/bin/bash

trap 'rm *.mha' EXIT

PARAMS_FILE='params.txt'

if test ! -e ${PARAMS_FILE}; then
	echo "Parameter file not found." >&2
	exit 1
fi

# The variable we are examining.
VARIABLE_NAME=$(grep VARIABLE_NAME ${PARAMS_FILE} | awk '{ print $2 }')
# Strains available.
STRAINS=( 0.5 1.0 3.0 5.0 7.0 9.0 11.0 )
# Indices of the above array to process.
#STRAIN_INDICES_TO_EXAMINE="2"
#STRAIN_INDICES_TO_EXAMINE="$1"
STRAIN_INDICES_TO_EXAMINE=$(grep STRAIN_INDEX ${PARAMS_FILE} | awk '{ print $2 }')

#POSSIBLE_VARIABLE_VALUES="8 12 16 20 24"
#shift
#POSSIBLE_VARIABLE_VALUES="$@"
POSSIBLE_VARIABLE_VALUES=$(grep VARIABLE_VALUE ${PARAMS_FILE} | awk '{ print $2 }')

# Path to th algorithm.
ALGORITHM=./mmm-strain
# Path to the post analysis program for calculating SNRe.
ITK_STATISTICS="./itk-statistics"
# Path to a text processing script.
STRAIN_LINE_PY="./strain_line.py"

# Interpolation type.  Change this with program compilation.
INTERP=sinc

CONFIG_IN="./config.yaml.in"

# Prefix to input data files.
PREFIX=./uniform25June07_
OUTPUT_PREFIX=uniform_simulation

#TRIALSTART=1
TRIALSTART=$(grep START_TRIAL ${PARAMS_FILE} | awk '{ print $2 }')
echo "TRIALSTART = ${TRIALSTART}"
TRIALEND=$((( $TRIALSTART + 4 )))
#TRIALEND=30
#TRIALEND=10
#TRIALEND=2

die() {
  echo "$1" >&2
  exit 1
}

OVERALL_RESULTS_FILE="SNRe_${VARIABLE_NAME}.csv"
echo -n "" > ${OVERALL_RESULTS_FILE}

echo "Starting processing of ${POSSIBLE_VARIABLE_VALUES}..."
for VARIABLE_VALUE in ${POSSIBLE_VARIABLE_VALUES}
do
  echo "Starting processing of strain indices ${STRAIN_INDICES_TO_EXAMINE}..."
  for index in ${STRAIN_INDICES_TO_EXAMINE}
  do
    mkdir -p subresults
    RESULTS_FILE="subresults/SNRe_${VARIABLE_NAME}_${VARIABLE_VALUE}.csv"
    echo -n "" > ${RESULTS_FILE}
    for REG in no_regularization regularization
    do
      SUBPATH="${STRAINS[index]}_strain/${INTERP}/${REG}"
      mkdir -p ${SUBPATH}

      TRIAL=${TRIALSTART}
      while test $TRIAL -le $TRIALEND
      do
        echo "Processing trial ${TRIAL} for strain ${STRAINS[index]}, ${REG}, ${VARIABLE_NAME} = ${VARIABLE_VALUE}..."
	echo -n "${TRIAL}, " >> ${RESULTS_FILE}
        CONFIG_OUT=config_${REG}_${VARIABLE_NAME}_${VARIABLE_VALUE}_trial_${TRIAL}.yaml
        FIXED_IMAGE="pre_rf_${TRIAL}.mha"
        MOVING_IMAGE=post_${STRAINS[index]}_percent_strain_rf_${TRIAL}.mha
        OUTPUT_PREFIX_FULL=${SUBPATH}/${OUTPUT_PREFIX}_${VARIABLE_NAME}_${VARIABLE_VALUE}_trial_${TRIAL}
        if test ${REG} = "no_regularization"; then
          sed -e s%FIXED_IMAGE%${FIXED_IMAGE}% \
          -e s%MOVING_IMAGE%${MOVING_IMAGE}% \
          -e s%OUTPUT_PREFIX%${OUTPUT_PREFIX_FULL}% \
          -e s%MAXIMUM_ITERATIONS%0% \
          -e s%VARIABLE%${VARIABLE_VALUE}% ${CONFIG_IN} > ${CONFIG_OUT}
        else
          sed -e s%FIXED_IMAGE%${FIXED_IMAGE}% \
          -e s%MOVING_IMAGE%${MOVING_IMAGE}% \
          -e s%OUTPUT_PREFIX%${OUTPUT_PREFIX_FULL}% \
          -e s%MAXIMUM_ITERATIONS%2% \
          -e s%VARIABLE%${VARIABLE_VALUE}% ${CONFIG_IN} > ${CONFIG_OUT}
        fi
        ${ALGORITHM} ${CONFIG_OUT} || die "Running the algorithm failed."
	echo -n "${REG}, " >> ${RESULTS_FILE}
        ${ITK_STATISTICS} -x 0.3 -y 0.1 \
        ${OUTPUT_PREFIX_FULL}*_StrainComponent0.mha | ${STRAIN_LINE_PY} n >> ${RESULTS_FILE} || die "Measuring statistics on StrainComponent0 failed."
        ${ITK_STATISTICS} -x 0.3 -y 0.1 \
        ${OUTPUT_PREFIX_FULL}*_StrainComponent2.mha | ${STRAIN_LINE_PY} >> ${RESULTS_FILE} || die "Measuring statistics on StrainComponent2 failed."
        let 'TRIAL++'
      done
    done
    sed s%^%"${VARIABLE_VALUE}, ${STRAINS[index]}, "% ${RESULTS_FILE} >> ${OVERALL_RESULTS_FILE}
  done # strain index
done # VARIABLE_VALUE

echo "${VARIABLE_NAME}, strain percent, trial, regularization, mean axial strain, axial strain std, axial strain SNRe, mean lateral strain, lateral strain std, lateral strain SNRe" > header
cat header ${OVERALL_RESULTS_FILE} >> newresults
mv newresults ${OVERALL_RESULTS_FILE}
