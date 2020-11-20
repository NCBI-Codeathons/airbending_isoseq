#!/bin/bash

set -euo pipefail 

while getopts d:o:a:b:w:h option
do
  case "${option}" in 
    d ) talon_db=${OPTARG} ;;
    o ) output_prefix=${OPTARG} ;;
    a ) annotation=${OPTARG} ;;
    b ) genome_build=${OPTARG} ;;
    w ) whitelist=${OPTARG} ;;
    h ) echo "Usage: run_talon_create_GTF.sh -d <talon_db> 
      -o <output_prefix> -a <annotation_name> -b <genome_build> -w <whitelist>" 
      exit 1 ;;
    \? ) echo "Usage: run_talon_create_GTF.sh -d <talon_db>
      -o <output_prefix> -a <annotation_name> -b <genome_build> -w <whitelist>" 
      exit 1 ;;
  esac
done

talon_create_GTF \
    --db ${talon_db} \
    -a ${annotation} \
    -b ${genome_build} \
    --whitelist ${whitelist} \
    --o ${output_prefix}
