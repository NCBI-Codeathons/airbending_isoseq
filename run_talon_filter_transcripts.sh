#!/bin/bash

set -euo pipefail 

while getopts d:o:h:a option
do
  case "${option}" in 
    d ) talon_db=${OPTARG} ;;
    o ) output_prefix=${OPTARG} ;;
	  a ) annotation=${OPTARG} ;;
    h ) echo "Usage: filter_talon_db.sh -d <talon_db> 
      -o <output_prefix>" 
      exit 1 ;;
    \? ) echo "Usage: run_txclean.sh -d <talon_db> 
      -o <output_prefix>" 
      exit 1 ;;
  esac
done

talon_filter_transcripts \
    --db ${talon_db} \
    -a ${annotation} \
    --maxFracA 0.5 \
    --minCount 2 \
    --minDatasets 1 \
    --o ${output_prefix}_whitelist.csv