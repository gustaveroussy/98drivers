#!/env/python3 
import sys 
import argparse 
import tabix 
import os 
import csv 
import gzip
from common import * 

#==============================================================================
def run_analysis(file):

	basename 			= os.path.basename(file).split(".")[0]

	with gzip.open(file,'r') as file:
		reader 			= csv.reader(io.TextIOWrapper(file, newline=""), delimiter='\t')
		output = compute_info(reader)

		for key in sorted(output.keys()):
			print(key, end="\t")

		print("")

		for key in sorted(output.keys()):
			print(output[key], end="\t")

		print("")


		
parser = argparse.ArgumentParser(
	description="Start variant analysis on whole genom", 
	usage="python3 analysis.py file.bed.gz"
	)

parser.add_argument("file", type=str, help="bed.gz file indexed with tabix")

args = parser.parse_args()

run_analysis(args.file)
