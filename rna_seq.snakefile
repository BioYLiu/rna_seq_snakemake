import pandas as pd
import os
import subprocess

import subprocess

configfile: "config/config.yaml"
include: "rules/helpers.py"


#zip them into a directory to make getting the location easier
SAMPLES = pd.read_table(config["sampleCSVpath"], sep = ",")
SAMPLES = SAMPLES.replace(np.nan, '', regex=True)

SAMPLE_NAMES = SAMPLES['sample_name'].tolist()
UNITS = SAMPLES['unit'].tolist()

rule all:
	input:
		expand(config['star_output_folder'] + "{name}/{name}_2pass.Aligned.out.bam",name = SAMPLE_NAMES),
		expand(config['star_output_folder'] + "{name}/{name}_2pass.Aligned.sorted.out.bam.bai",name = SAMPLE_NAMES)


# include: "rules/fastqc.smk"
# include: "rules/multiqc.smk"
include: "rules/fastp.smk"
include: "rules/star.smk"
include: "rules/star_second_pass.smk"
include: "rules/samtools.smk"
