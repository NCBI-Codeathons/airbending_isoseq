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

## Dependecies
Software:

[TranscriptClean](https://github.com/dewyman/TranscriptClean) to correct mismatches, microindels, and noncanonical splice junctions in long reads that have been mapped to the genome


[Talon](https://github.com/dewyman/TALON) is a pipeline to collapse and classify aligned reads


[SQANDI2](https://github.com/Magdoll/SQANTI2) is a pipeline to classify alignments based on CAGE, polyA, and RNA-seq data


DBs used in benchmarking:

SQANTI2 support data

[Support Data](https://github.com/Magdoll/images_public/tree/master/SQANTI2_support_data)


<img src="https://github.com/NCBI-Codeathons/airbending_isoseq/blob/master/Pipeline_image.png" width="245" height="480">


## Inputs
1. Alignment files (.sam) should not contain the extended X= notations in CIGAR string.

`reformat_sam.py <input_sam>`


2. Genome annotations should be in gtf format with transcript lines included.

If you have a gff3 format first convert this to gtf

`RefSeq_gff_to_gtf.sh <genome_gff3>`

Now add transcript lines to gtf file


`reformat_gtf.py <genome_gtf>`


3. Genome fasta files cannot have titles in the header and should only contain chromosome information in order to be compatible with TALON


`reformat_fasta.py <genome_fasta>`

## Workflow
TALON pipeline 

1. First clean data using TranscriptomeClean


`run_txclean.sh -i <input_sam> -o <output_prefix> -g <genome_fasta> -j <splice_juncs> -t <threads>`

2. Run talon_label_reads to remove internally primed transcripts


`run_talon_label_reads.sh -i <input_sam> -o <output_prefix> -g <genome_fasta> -r <range_size> -t <threads>`

3. Initialize the database to run talon


`run_talon_initialize_database.sh -i <input_gtf> -o <output_prefix> -g <genome_name> -a <annotation_name>`

4. Run Talon to collapse and classify alignments


`run_talon.sh -i <config_file> -o <output_prefix> -d <talon_database_name> -g <genome_name> -t <threads>`

## Output Files from TALON

Output from TALON will be a QC long and annotation table .tsv and .gtf
Hyperlink to Talon GitHub
[Talon](https://github.com/dewyman/TALON)


Postprocessing:



## SQANTI pipeline



Filtering:



Final Output:

## Future directions
Adapt multiple genome references to be used with TALON 



### Team Members
[Vamsi Kodali](https://github.com/vkkodali)


[Fairlie Reese](https://github.com/fairliereese)


[Elizabeth Hutchins](https://github.com/e-hutchins)


[Catherine Giannetti](https://github.com/cgiannetti)

