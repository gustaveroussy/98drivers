#!/env/python3 
import sys 
import argparse 
import tabix 
import os 
import csv 
import gzip
from common import * 
#==========================================================================
def compute_stats(file):

	with gzip.open(file,'r') as file:
		reader = csv.reader(io.TextIOWrapper(file, newline=""), delimiter='\t')
		mutations = set()
		patients  = set()
		muttype   = dict()

		for row in reader:

			ref = row[4]
			alt = row[5]


			mutations.add((row[0],row[1],row[2],ref, alt))
			patients.add(row[3])


		print("mutationCount", len(mutations), sep="\t")
		print("patientsCount", len(patients), sep="\t")



	
#==========================================================================
	
parser = argparse.ArgumentParser(
	description="Compute stats from bed.gz tabix", 
	usage="python3 file.bed.gz"
	)

parser.add_argument("file", type=str, help="bed.gz file indexed with tabix")

args = parser.parse_args()

# Start algo 
compute_stats(args.file)