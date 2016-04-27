#!/bin/bash 

echo track type="bedGraph name=$(basename $1)" description="wgs max variation"
cat $1 |awk 'NR >1{print $0}'|sort -rn -k 4,4 |head -n $2 
