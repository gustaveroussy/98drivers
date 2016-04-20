#!/bin/bash 
# Input is open data as tsv.gz file format comming from icgc 

FILENAME=$1
FULL_NAME=$(basename $FILENAME)
BASE_NAME=${FULL_NAME%%.*}
FILE_DIR=$(dirname $FILENAME)


#9 		= chromosom
#10 	= start based 1 
#11		= end 
#2 		= Donor 
#16		= reference allele
#17		= alternative allele
#21		= total read count 


 
zcat $FILENAME|awk 'BEGIN{OFS="\t"; FS="\t"}NR>1{print $9,$10,$10,$2,$16,$17,$21}'|gzip > $FILE_DIR/$BASE_NAME.bed.gz
