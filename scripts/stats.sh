#!/bin/bash 

mutation_count=$(zcat $1|cut -f1,2,3,5,6| sort -u | wc -l )
patient_count=$(zcat $1|cut -f4 | sort -u | wc -l )

echo -e mutation count'\t'$mutation_count 
echo -e patient count'\t'$patient_count 
