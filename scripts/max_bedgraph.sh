#!/bin/bash 


cat $1 |sort -rn -k 4,4 |head -n $2 
