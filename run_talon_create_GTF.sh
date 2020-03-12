#!/bin/bash

set -euo pipefail 

while getopts d:o:h:a:b:w option
do
  case "${option}" in 
    d ) talon_db=${OPTARG} ;;
    o ) output_prefix=${OPTARG} ;;
	a ) annotation=${OPTARG} ;;
	b ) genome_build=${OPTARG} ;;
	w ) whitelist=${OPTARG} ;;
    h ) echo "Usage: filter_talon_db.sh -d <talon_db> 
      -o <output_prefix>" 
      exit 1 ;;
    \? ) echo "Usage: run_txclean.sh -d <talon_db> 
      -o <output_prefix>" 
      exit 1 ;;
  esac
done

talon_create_GTF \
    --db ${talon_db} \
    -a ${annotation} \
    -b ${genome_build} \
    --whitelist ${whitelist} \
    --o ${output_prefix}