#!/bin/bash

#if test $# -lt 1; then
  #echo "usage $0 <variable_name>"
  #exit 1
#fi

# Change the following before running the script.
VARIABLE_NAME=scaleByStrain
#VARIABLE_VALUES=$(seq 0.7 0.1 1.5)
VARIABLE_VALUES="true false"
STRAIN_INDICES=$(seq 0 6)
START_TRIALS=$(seq 1 5 6)

DATASET_DIR=dataset_uniform_phantom_${VARIABLE_NAME}
PARAMS="params.txt.in"

create_job() {
	DESTDIR="${DATASET_DIR}/${VARIABLE_NAME}_${VARIABLE_VALUE}_strain_index_${STRAIN_INDEX}"
	mkdir -p ${DESTDIR}
	sed -e s%MY_VARIABLE_VALUE%${VARIABLE_VALUE}% \
		-e s%MY_STRAIN_INDEX%${STRAIN_INDEX}% \
                -e s%MY_VARIABLE_NAME%${VARIABLE_NAME}% \
                -e s%MY_START_TRIAL%${START_TRIAL}% \
		${PARAMS} > ${DESTDIR}/params.txt
}

for VARIABLE_VALUE in ${VARIABLE_VALUES}; do
	for STRAIN_INDEX in ${STRAIN_INDICES}; do
          for START_TRIAL in ${START_TRIALS}; do
		create_job
          done
	done
done
