#!/bin/bash

set -euo pipefail

while getopts i:a:g:l:p:c:s:t:h option
do
  case "${option}" in
    i ) input_gtf=${OPTARG} ;;
    a ) annotation=${OPTARG} ;;
    g ) genome=${OPTARG} ;;
    l ) polyA_list=${OPTARG} ;;
    p ) polyA_peak=${OPTARG} ;;
    c ) cage_peak=${OPTARG} ;;
    s ) splice_junctions=${OPTARG} ;;
    t ) threads=${OPTARG} ;;
    h ) echo "Usage: run_squanti.sh -i <input_gtf>
      -a <annotation> -g <genome_fasta>
      -l <polyA_motif_list> -p <polyA_peak>
      -c <cage_peaks> -s <splice_junctions> -t <threads>"
      exit 1 ;;
    \? ) echo "Usage: run_squanti.sh -i <input_gtf>
      -a <annotation> -g <genome_fasta>
      -l <polyA_motif_list> -p <polyA_peak>
      -c <cage_peaks> -s <splice_junctions> -t <threads>"
      exit 1 ;;
  esac
done


#add path to cDNA_Cupcake
export PYTHONPATH=$PATH:/opt/cDNA_Cupcake/sequence:/opt/cDNA_Cupcake/rarefaction


python3 /opt/SQANTI2/sqanti_qc2.py -t ${threads} -n ${threads} --gtf ${input_gtf} \
     ${annotation} ${genome} \
     --polyA_motif_list ${polyA_list} \
     --polyA_peak ${polyA_peak} \
     --cage_peak ${cage_peak} \
     -c ${splice_junctions}

