#!/bin/bash 

zcat $1 |cut -f1,2 | sort | uniq -c | sort -n -r -k 1 | head -n $2 | awk 'BEGIN{OFS="\t"}{print $2,$3,$3,$1}'

