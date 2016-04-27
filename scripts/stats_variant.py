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
		
		# Count mutation 
		mutations = set()

		# Count patients 
		patients  = set()

		# Count mutation per types 
		muttype   = {
					('C','T'): 0,
					('T','G'): 0,
					('T','A'): 0,
					('T','C'): 0,
					('C','A'): 0,
					('C','G'): 0
					}


		bases     = ('A','C','G','T')
		cannMutationCount   = 0


		for row in reader:

			ref = row[4].upper()
			alt = row[5].upper() 

			if ref in bases and alt in bases and ref != bases:
				ref,alt = cannonic_mutation((ref,alt))
				if (ref,alt) in muttype:
					muttype[(ref,alt)] += 1


			mutations.add((row[0],row[1],row[2],ref, alt))
			patients.add(row[3])

		# Compute sum of muttype
		for key in muttype.keys():
			cannMutationCount += muttype[key]

		transition   = muttype[('C','T')] + muttype[('T','C')] 
		transversion = cannMutationCount - transition


		print("patientsCount", len(patients), sep="\t")
		print("mutationCount", len(mutations), sep="\t")
		print("cannMutationCount", cannMutationCount, sep="\t")

		print("CT", muttype[('C','T')], sep="\t")
		print("TG", muttype[('T','G')], sep="\t")
		print("TA", muttype[('T','A')], sep="\t")
		print("TC", muttype[('T','C')], sep="\t")
		print("CA", muttype[('C','A')], sep="\t")
		print("CG", muttype[('C','G')], sep="\t")
		print("transition", transition  , sep="\t")
		print("transversion", transversion , sep="\t")



	
#==========================================================================
	
parser = argparse.ArgumentParser(
	description="Compute stats from bed.gz tabix", 
	usage="python3 file.bed.gz"
	)

parser.add_argument("file", type=str, help="bed.gz file indexed with tabix")

args = parser.parse_args()

# Start algo 
compute_stats(args.file)