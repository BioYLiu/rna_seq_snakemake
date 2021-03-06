import re
import pandas as pd
import os
import numpy as np

def get_fastq_names(DATA):
    samples = pd.read_table(DATA, sep = ",")
    #take all the fasqs and combine them to a list remove any nas
    fastq_list = samples.fast1.dropna().tolist() + samples.fast2.dropna().tolist()
    #if there are any missing values pandas gets annoyed so replace nans with empty string
    samples = samples.replace(np.nan, '', regex=True)
    #get the associated sample and unit name for each fastq using and or operator to get either fast1 or fast2, works for both single-end and paired end this way
    unit_name = [samples.loc[(samples['fast1'] == fq)| (samples['fast2'] == fq)].unit.iloc[0] for fq in fastq_list]
    #strip it down to just the name of the file bit
    stripped = [re.sub(".fastq.gz","",strpd.rpartition('/')[2]) for strpd in fastq_list]
    #now combine these three lists to get a meaningfull and unique string for each fastq file
    
    return(stripped, fastq_list, unit_name)

def return_fastq_location(wildcards):
	#return the file location from the fastq name
	return(ORDER_DICT[wildcards])

def return_parsed_extra_params(extra_params):
    #starting blank
    cmd = ""
    #for key in extra parameters
    for key in extra_params:
        #append the key value pair if it's a parmeter that needed something
        if extra_params[key]:
            cmd += " --{0} {1}".format(key,extra_params[key])
        else: #otherwise if it's parameter that's just a flag, append just the flag
            cmd += " --{0}".format(key)
    return(cmd)



def get_trimmed(name):
    #the trimmed file is the output, and the unit, we find it from the sample and and the unit which snakemake wildcards are going through
    trimmed_1 = [os.path.join(config["fastp_trimmed_output_folder"],\
                              SAMPLES.loc[(SAMPLES.fast1 == fq),'unit'].tolist()[0],\
                              re.sub(".fastq.gz","",fq.rpartition('/')[2]) + \
                              "_trimmed.fastq.gz") for fq in SAMPLES.loc[(SAMPLES.sample_name == name),\
                                                                         'fast1'].tolist()]
    #if we have paired end data there will also be a trimmed 2, same thing, using the fast2 column instead
    if config['end_type'] == "pe":
        
        trimmed_2 = [os.path.join(config["fastp_trimmed_output_folder"],\
                              SAMPLES.loc[(SAMPLES.fast2 == fq),'unit'].tolist()[0],\
                              re.sub(".fastq.gz","",fq.rpartition('/')[2]) + \
                              "_trimmed.fastq.gz") for fq in SAMPLES.loc[(SAMPLES.sample_name == name),\
                                                                         'fast2'].tolist()]
        #trimmed files is a list of the two
        trimmed_files = [trimmed_1, trimmed_2]

    else:
        trimmed_files = [trimmed_1]
        
    return(trimmed_files)


def get_genome_directory(species):
    temp = pd.read_table("config/star_genomes_species.csv",sep = ",")
    return(temp.genome[temp.species == species].tolist()[0])

def return_first_passing_splice_junctions_list(name):
    SAMPLES = pd.read_table(config["sampleCSVpath"], sep = ",")
    #return a comma separate list of all the splice junction out tabs
    sample_list = list(set(SAMPLES.sample_name))
    return(",".join([config['star_output_folder'] + s + "/" + s + ".SJ.out.tab" for s in sample_list]))

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1