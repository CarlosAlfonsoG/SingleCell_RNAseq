#Need improvement fails latency wait time even with 300 is not enought for snakemake to find the files 
"""
Author: Carlos
Affiliation: Max Planck Institute for Immunobiology and Epigenetics
Aim: RNA velocity
Date Start: Thursday Oct 18 16:16:30 CET 2018
Run: snakemake   -s Snakefile
Latest modification:
  - add_Star_maping
"""
##-----------------------------------------------##
## Working directory                             ##
## Adapt to your needs                           ##
##-----------------------------------------------##
BASE_DIR = "/data/processing/alfonso"
WDIR = BASE_DIR + "/velocity"
workdir: WDIR
## The list of samples to be processed
##--------------------------------------------------------------------------------------##
import glob
foo = glob.glob("velocity_results/velocity_data/compressed/*_R1.substracted.fastq.gz")
SAMPLES = [x[:-24] for x in foo]
#SAMPLES = glob_wildcards("week6_wt/{smp}_R1.fastq.gz")R1.substracted.fastq.gz

rule final:
    input: expand("mapped_reads/{smp}_mp_R2", smp=SAMPLES)

rule umi_extract:
    input: R2="{smp}_R2.substracted.fastq.gz",
           Genome="/data/repository/organisms/GRCm38_ensembl/STARIndex/"
    output: OR2="mapped_reads/{smp}_mp_R2"
    message: """--- Mapping Reads o.o"""
    shell:
       """
       STAR --genomeDir {input.Genome} \
               --readFilesIn {input.R2} \
               --outSAMmultNmax 1 \
               --runThreadN 6 \
               --readNameSeparator space \
               --outSAMunmapped Within \
               --outSAMtype SAM \
               --outFileNamePrefix {output.OR2} \
               --readFilesCommand gunzip -c
       """
