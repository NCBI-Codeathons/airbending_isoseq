#!/bin/bash

#takes gff3 file as input and outputs gtf file including transcript lines

set -euo pipefail

while getopts i:h option
do
  case "${option}" in
    i ) gtf=${OPTARG} ;;
    h ) echo "Usage: RefSeq_gff3_to_gtf.sh -i <gff3_file>"
      exit 1 ;;
    \? ) echo "Usage: RefSeq_gff3_to_gtf.sh -i <config_file>"
      exit 1 ;;
  esac
done

#save file name
prefix=$(basename ${gtf} | sed 's/.gff//')

#convert to genePred format
gff3ToGenePred ${gtf} ${prefix}.genePred.tmp

#convert to gtf
genePredToGtf file ${prefix}.genePred.tmp ${prefix}.gtf.tmp

#pull transcript lines
awk '$3=="transcript"' ${prefix}.gtf.tmp > ${prefix}.transcriptsOnly.gtf.tmp

#add to gtf
cat ${gtf} ${prefix}.transcriptsOnly.gtf.tmp > ${prefix}.withTranscripts.gtf

#remove tmp files
rm *.tmp

