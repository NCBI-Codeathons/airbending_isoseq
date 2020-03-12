# Isoseq to Isoforms
## Long-read sequencing
Long-read sequencing is becoming a powerful tool to analyze genomics and transcriptomics using technologies such as PacBio, Oxford Nanopore, and SLR-Seq. In transcriptomics, long-read sequences allow for the identification and discovery of novel isoforms that can help characterize complex transcriptomes. As this technology continues to progress and is applied to more projects, the number of reads will rise exponentially. It is imperative to have tools available to process these data accurately and reproducibly to curate new 'knowledge'.

## What is the problem?
One of the main issues with processing long-read sequences is the large number of alignments. To manually curate each alignment for novel isoforms is time consuming and redundant. 
There are current pipelines such as TALON which can use alignments as input and process them to (1) collapse what can be considered the same transcript isoforms, and (2) classify the collapsed set to indicate known and novel isoforms in the dataset. TALON, in particular, is platform-agnostic but other pipelines that tackle similar problems are designed to work best with read data obtained from a specific platform. 
Another problem with analyzing and annotating long-read data is low transcript quality that can misinform novel isoforms.
SQANTI2 pipeline can further verify and annonate isoform data to give higher confidence in transcript quality and identify

## What is Isoseq to Isoforms
This pipeline will take alignment data and use existing pipelines to collapse and classify the alignments to output a table of high-quality novel isoform transcripts. Specifically, this pipeline will pre-process alignment data and reference genomes to be compatible with the TALON pipeline. It will then post-process TALON output to be compatible with SQANTI2 classification. Finally, the SQANTI2 output is filtered to only include high-quality novel isoforms.


## Workflow
Pre-processing:

example input and output files

Postprocessing:


Filtering:


## Dependecies


## Future directions

### Team Members


What are we doing?
Final goals are:
Adapt multiple genome references to be used with TALON pipeline
to be able to run TALON pipeline to collapse reads
this means, a user would start with a bunch of alignments that will be first processed by TranscriptClean 
the 'clean' transcripts are then used by talon cleanup step to remove internal priming candidates - transcript_label
finally, run talon to collapse the transcripts 
Adapt the output of TALON to work with SQANTI2
Run SQANTI2 to classify the collapsed transcripts 
Filter SQANTI2 output to produce high-confidence novel isoforms
Benchmark this using 3 different human datasets

Issues
For the the pipeline to be compatible with data from a wide range of sources, we will need a few helper scripts that will be developed as part of this codeathon and made available. 
Genome FASTA files cannot have titles in the header lines; we will use reformat_fasta.py to process RefSeq FASTA files to produce new files that are compatible with the tools in the TALON pipeline 
RefSeq annotation GTF files lack the transcript lines; we will use the reformat_gtf.py script to add those lines
SAM files often use the extended X= notations in their CIGAR strings. These are incompatible with TranscriptClean. We will use the reformat_sam.py script to process them. 


![alt tag](https://github.com/NCBI-Codeathons/airbending_isoseq/files/4325511/Pipeline.1.pdf)
