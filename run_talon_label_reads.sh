#!/bin/bash

set -euo pipefail

while getopts i:o:g:r:t:h option
do
  case "${option}" in
    i ) samin=${OPTARG} ;;
    o ) samout=${OPTARG} ;;
    g ) genome=${OPTARG} ;;
    r ) rangesize=${OPTARG} ;;
    t ) threads=${OPTARG} ;;
    h ) echo "Usage: run_talon_label_reads.sh -i <input_sam>
      -o <output_prefix> -g <genome_fasta> -r <range_size> -t <threads>"
      exit 1 ;;
    \? ) echo "Usage: run_talon_label_reads.sh -i <input_sam>
      -o <output_prefix> -g <genome_fasta> -r <range_size> -t <threads>"
      exit 1 ;;
  esac
done

talon_label_reads \
  --f ${samin} \
  --g ${genome} \
  --t ${threads} \
  --ar ${rangesize} \
  --deleteTmp \
  --o ${samout}

