#!/bin/bash
#Submit to the cluster, give it a unique name
#$ -S /bin/bash

#$ -cwd
#$ -V
#$ -l h_vmem=1.9G,h_rt=20:00:00,tmem=1.9G
#$ -pe smp 2

# join stdout and stderr output
#$ -j y
#$ -R y

if [ "$1" != "" ]; then
    RUN_NAME=$1
else
    RUN_NAME=$""
fi

FOLDER=$(date +"%Y%m%d%H%M")
mkdir -p $FOLDER
cp config/config.yaml $FOLDER/$RUN_NAME.config.yaml

snakemake -s rna_seq.snakefile \
--jobscript cluster_qsub.sh \
--cluster-config config/cluster.yaml \
--cluster-sync "qsub -l h_vmem={cluster.h_vmem},h_rt={cluster.h_rt} -pe {cluster.pe} -o $FOLDER" \
-j 500 \
--nolock \
--latency-wait 100