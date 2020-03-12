#!/bin/bash

set -euo pipefail

while getopts i:o:d:g:t:h option
do
  case "${option}" in
    i ) config=${OPTARG} ;;
    o ) outpre=${OPTARG} ;;
    d ) talon_db=${OPTARG} ;;
    g ) genome_name=${OPTARG} ;;
    t ) threads=${OPTARG} ;;
    h ) echo "Usage: run_talon.sh -i <config_file>
      -o <output_prefix> -d <talon_database_name>
      -g <genome_name> -t <threads>"
      exit 1 ;;
    \? ) echo "Usage: run_talon.sh -i <config_file>
      -o <output_prefix> -d <talon_database_name>
      -g <genome_name> -t <threads>"
      exit 1 ;;
  esac
done

talon \
  --f ${config} \
  --db ${talon_db} \
  --build ${genome_name} \
  --t ${threads} \
  --o ${outpre}
