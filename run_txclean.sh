#!/bin/bash

set -euo pipefail 

while getopts i:o:g:j:t:h option
do
  case "${option}" in 
    i ) samin=${OPTARG} ;;
    o ) samout=${OPTARG} ;;
    g ) genome=${OPTARG} ;;
    j ) sjtsv=${OPTARG} ;;
    t ) threads=${OPTARG} ;;
    h ) echo "Usage: run_txclean.sh -i <input_sam> 
      -o <output_prefix> -g <genome_fasta> -j <splice_juncs> -t <threads>" 
      exit 1 ;;
    \? ) echo "Usage: run_txclean.sh -i <input_sam> 
      -o <output_prefix> -g <genome_fasta> -j <splice_juncs> -t <threads>" 
      exit 1 ;;
  esac
done

python3 /opt/TranscriptClean/TranscriptClean.py \
  --sam ${samin} \
  --genome ${genome} \
  --threads ${threads} \
  --spliceJns ${sjtsv} \
  --deleteTmp \
  --outprefix ${samout}
