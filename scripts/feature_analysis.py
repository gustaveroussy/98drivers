#!/env/python3 
import sys 
import argparse 
import tabix 
import os 
import csv 
import gzip
from common import * 

#==============================================================================
def run_feature_analysis(file):

	basename 			= os.path.basename(file).split(".")[0]

	with open(file,'r') as file:
		reader 			= csv.reader(file, delimiter='\t')
		
		size = 0 


		for line in reader:
			chromosom = line[0]
			start     = int(line[1])
			end       = int(line[2])
			typename  = line[3]
			name      = line[4]





		
parser = argparse.ArgumentParser(
	description="Start feature analysis on whole genom", 
	usage="python3 analysis.py feature.bed.gz"
	)

parser.add_argument("file", type=str, help="bed.gz file indexed with tabix")

args = parser.parse_args()

run_feature_analysis(args.file)
