#!/bin/bash

set -euo pipefail

while getopts i:o:g:a:h option
do
  case "${option}" in
    i ) gtf=${OPTARG} ;;
    o ) outpre=${OPTARG} ;;
    g ) genome_name=${OPTARG} ;;
    a ) anno_name=${OPTARG} ;;
    h ) echo "Usage: run_talon_initialize_database.sh -i <input_gtf>
      -o <output_prefix> -g <genome_name> -a <annotation_name>"
      exit 1 ;;
    \? ) echo "Usage: run_talon_initialize_database.sh -i <input_gtf>
      -o <output_prefix> -g <genome_name> -a <annotation_name>"
      exit 1 ;;
  esac
done

talon_initialize_database \
  --f ${gtf} \
  --g ${genome_name} \
  --a ${anno_name} \
  --o ${outpre}

