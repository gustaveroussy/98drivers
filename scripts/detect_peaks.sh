#!/bin/bash 

zcat $1 |cut -f1,2 | sort | uniq -c | sort -n -r -k 1 | awk -v max=$2 'BEGIN{OFS="\t"}$1 > max{print $2,$3,$3,$1}'

