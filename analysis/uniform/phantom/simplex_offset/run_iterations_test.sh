#!/bin/bash

SIMPLEX_DELTAS=$(seq 0.1 0.1 0.9)

for SIMPLEX_DELTA in ${SIMPLEX_DELTAS}
do
  sed "s/SIMPLEX_DELTA/${SIMPLEX_DELTA}/" config.yaml.in > config.yaml
  ./mmm-strain config.yaml
done
