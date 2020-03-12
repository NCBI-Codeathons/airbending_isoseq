# Inferring-intact-transcript-structure-and-discovering-novel-isoforms-from-long-read-data
Preamble
Long-read sequencing is becoming a powerful tool to analyze genomics and transcriptomics. (PacBio, Oxford Nanopore) Specifically, long-reads allow for the identification and discovery of novel isoforms in the transcriptome. Sentence why we care about novel isoforms. However, as this technology is applied to numerous projects, the number of reads per project has increased at a nearly exponential rate. It is imperative to have tools available to process these data accurately and reproducibly to produce new 'knowledge'.

Pipelines
One issue with processing long-read sequences is the large number of alignments. 
Existing pipelines such as TALON can use alignments as an input and process them to (1) collapse what can be considered the same transcript isoforms, and (2) classify the collapsed set to indicate known and novel isoforms in the dataset. TALON, in particular, is platform-agnostic but other pipelines that tackle similar problems are designed to work best with read data obtained from a specific platform. 
SQANTI2 is another platform that uses additional parameters to further classify isoforms based on CAGE, polyA motifs, and RNA-seq data. (why does this help?)

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
